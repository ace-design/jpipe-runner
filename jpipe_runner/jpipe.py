"""
jpipe_runner.jpipe
~~~~~~~~~~~~~~~~~~

This module contains the core of jPipe Runner.
"""

from collections import deque
from copy import deepcopy
from typing import (Any,
                    Optional,
                    Callable,
                    Iterable,
                    Iterator)

import networkx as nx

from jpipe_runner.enums import (ClassType,
                                VariableType,
                                StatusType)
from jpipe_runner.exceptions import (InvalidJustificationException,
                                     JustificationTraverseException,
                                     FunctionException)
from jpipe_runner.models import JustificationDef, ClassDef
from jpipe_runner.parser import load_jd_file, parse_jd_json_file
from jpipe_runner.runtime import PythonRuntime
from jpipe_runner.utils import sanitize_string


class Justification(nx.DiGraph):
    node_attr_map = {
        VariableType.CONCLUSION: dict(fillcolor="lightgrey",
                                      shape="rect",
                                      style="filled"),
        VariableType.STRATEGY: dict(fillcolor="palegreen",
                                    shape="parallelogram",
                                    style="filled"),
        VariableType.SUB_CONCLUSION: dict(color="dodgerblue",
                                          shape="rect"),
        VariableType.EVIDENCE: dict(fillcolor="lightskyblue2",
                                    shape="rect",
                                    style="filled"),
        VariableType.SUPPORT: dict(fillcolor="lightcoral",
                                   shape="rect",
                                   style="filled"),
    }

    def justify_order(self,
                      data: bool = False,
                      ) -> Iterable[str | tuple[str, dict]]:
        order: list[str | tuple[str, dict]] = []

        def callback(n, d):
            order.append((n, d)
                         if data else n)
            return True

        self.layered_traverse(callback)
        return order

    def layered_traverse(self,
                         callback: Optional[Callable[[str, dict], bool]] = None,
                         ) -> None:

        if callback is None:
            callback = lambda n, d: True

        # noinspection PyCallingNonCallable
        # start with all evidence nodes.
        start_nodes = (n for n in self.nodes(data=False)
                       if self.in_degree(n) == 0)

        visited = set()
        queue = deque(start_nodes)

        while queue:
            node = queue.popleft()

            # node already visited.
            if node in visited:
                continue

            # run callback function.
            if not callback(node, self.nodes[node]):
                raise JustificationTraverseException(
                    f"callback returns false when traversing to '{node}'")

            # save visited node.
            visited.add(node)

            # check successor nodes.
            for child in self.successors(node):
                all_parents_visited = True
                for parent in self.predecessors(child):
                    if parent not in visited:
                        all_parents_visited = False
                        break

                if all_parents_visited and child not in visited:
                    queue.append(child)  # ready to enqueue.

        assert len(visited) == len(self.nodes)

    # noinspection PyCallingNonCallable
    def validate(self) -> None:
        conclusion_nodes = [n for n, d in self.nodes(data=True) if d["var_type"] == VariableType.CONCLUSION]
        if len(conclusion_nodes) != 1:
            raise InvalidJustificationException(
                f"justification '{self.name}' must have only one conclusion, but got {len(conclusion_nodes)}")

        if not nx.is_directed_acyclic_graph(self):
            raise InvalidJustificationException(
                f"justification '{self.name}' must be a DAG (directed acyclic graph)")

        conclusion = conclusion_nodes[0]

        for n, d in self.nodes(data=True):
            match d["var_type"]:
                case VariableType.EVIDENCE:
                    if self.in_degree(n) != 0:  # check in-degree
                        raise InvalidJustificationException(
                            f"evidence '{n}' is not allowed to be supported by others")
                    if not nx.has_path(self, n, conclusion):
                        raise InvalidJustificationException(
                            f"evidence '{n}' does not reach the conclusion '{conclusion}'")
                    for out in self.successors(n):
                        if (out_var_type := self.nodes[out]['var_type']) != VariableType.STRATEGY:
                            raise InvalidJustificationException(
                                f"evidence '{n}' can only support strategy, found '{out_var_type}'")
                case VariableType.STRATEGY:
                    if self.in_degree(n) == 0:
                        raise InvalidJustificationException(
                            f"strategy '{n}' must be supported by others")
                    supports = tuple(self.successors(n))
                    if len(supports) == 0:
                        raise InvalidJustificationException(
                            f"strategy '{n}' does not support any node, must have 1 out-edge")
                    if len(supports) > 1:
                        raise InvalidJustificationException(
                            f"strategy '{n}' supports multiple nodes, but only 1 out-edge allowed")
                    if (out_var_type := self.nodes[supports[0]]['var_type']) not in \
                            (VariableType.SUB_CONCLUSION, VariableType.CONCLUSION):
                        raise InvalidJustificationException(
                            f"strategy '{n}' can only support sub-conclusion or conclusion, found '{out_var_type}'.")
                case VariableType.SUB_CONCLUSION:
                    if self.in_degree(n) == 0:
                        raise InvalidJustificationException(
                            f"sub-conclusion '{n}' must be supported by others")
                    if not nx.has_path(self, n, conclusion):
                        raise InvalidJustificationException(
                            f"sub-conclusion '{n}' does not reach the conclusion '{conclusion}'")
                    for out in self.successors(n):
                        if (out_var_type := self.nodes[out]['var_type']) != VariableType.STRATEGY:
                            raise InvalidJustificationException(
                                f"sub-conclusion '{n}' can only support strategy, found '{out_var_type}'")
                case VariableType.CONCLUSION:
                    pass
                case VariableType.SUPPORT:
                    raise InvalidJustificationException(
                        f"abstract support '{n}' should not be included in a justification class")

    def export_to_image(self,
                        path: Optional[Any] = None,
                        format: Optional[str] = None,
                        ) -> bytes | None:
        try:
            from networkx.drawing.nx_agraph import to_agraph
        except ImportError as e:
            raise ImportError("pygraphviz is required to enable this feature") from e

        agraph = to_agraph(self)

        agraph.graph_attr.update(
            size="5",
            rankdir="BT",  # Bottom-to-Top
            dpi="500",
            label=self.name,
            fontsize="15",
            labelloc="bottem"
        )
        agraph.edge_attr.update(
            color="black",
            arrowhead="normal",
        )

        for n, d in self.nodes(data=True):
            attr = self.node_attr_map[d["var_type"]]
            agraph_node = agraph.get_node(n)
            agraph_node.attr.update({
                (k, v)
                for k, v in attr.items()
                if v is not None
            })

        return agraph.draw(path=path, format=format, prog="dot")


class JPipeEngine:

    def __init__(self,
                 jd_file: str,
                 ):
        """TODO:
        Currently JPipeEngine only supports to load and parse .jd files.
        To extend the ability to support a more general form of justification
        representation such as JSON files, A `parse_jd_json_file` function
        is added in the parser module, which can be imported like
        `from parser import parse_jd_json_file`. This function works just like
        the `load_jd_file` or `parse_jd_file` function, but for JSON file
        format instead. The format of the JSON content is similar to the .jd
        justification file and an example can be found in
        `examples/models/01_slides.json`.

        E.g., with the following line to parse the JSON justification file directly.
        >>> self._model = parse_jd_json_file(filename=jd_file)
        """
        self._model = load_jd_file(filename=jd_file)
        self._justifications: dict[str, Justification] = {}
        self._init_model()

    def _init_model(self) -> None:
        for cls in self._model.class_defs.values():
            match cls.class_type:
                case ClassType.JUSTIFICATION:
                    jd = self._build_justification(cls)
                    self._justifications[cls.name] = jd
                case ClassType.PATTERN:
                    # ignore pattern class.
                    pass
                case ClassType.COMPOSITION:
                    # ignore composition class.
                    pass

    def _find_pattern(self, pattern: str) -> JustificationDef:
        for cls in self._model.class_defs.values():
            if cls.class_type == ClassType.PATTERN and cls.name == pattern:
                assert isinstance(cls.body, JustificationDef)
                return cls.body
        raise InvalidJustificationException(f"pattern {pattern} not found")

    def _build_justification(self, jd_cls: ClassDef) -> Justification:
        jd = Justification(name=jd_cls.name)

        supports = deepcopy(jd_cls.body.supports)
        variables = deepcopy(jd_cls.body.variables)

        # expand justification with pattern.
        if jd_cls.pattern is not None:
            pattern_jd: JustificationDef = self._find_pattern(jd_cls.pattern)
            supports.update(i for i in pattern_jd.supports)
            variables.update((k, v) for k, v in pattern_jd.variables.items()
                             if v.var_type != VariableType.SUPPORT)

        for name, item in variables.items():
            jd.add_node(name,
                        label=item.description,
                        var_type=item.var_type,
                        status=None,  # init
                        )

        def check_vars(*args):
            for v in args:
                if v not in variables:
                    raise InvalidJustificationException(
                        f"variable ID '{v}' not found")

        for support in supports:
            check_vars(support.left, support.right)
            jd.add_edge(support.left, support.right)

        jd.validate()
        return jd

    @property
    def justifications(self) -> dict[str, Justification]:
        return self._justifications

    def justify(self,
                diagram: str,
                /,
                dry_run: bool = False,
                runtime: PythonRuntime = None,
                ) -> Iterator[dict]:
        jd = self.justifications[diagram]

        for node, attr in jd.justify_order(data=True):

            # get all statuses of its predecessors
            pre_statuses = [
                jd.nodes[i]['status']
                for i in jd.predecessors(node)
            ]

            # check if predecessors have set status
            assert None not in pre_statuses

            # check if all predecessors have passed
            all_passed = all(x is StatusType.PASS for x in pre_statuses)

            # skip all other parts if conditions are not met
            if dry_run or not all_passed:
                attr['status'] = StatusType.SKIP
                yield dict(name=node, **attr)
                continue

            match attr['var_type']:
                case VariableType.EVIDENCE | VariableType.STRATEGY:
                    exception = None
                    fn_name = sanitize_string(attr['label'])
                    # initiate to PASS
                    attr['status'] = StatusType.PASS
                    try:
                        if not (res := runtime.call_function(fn_name)):
                            raise FunctionException(
                                f"function '{fn_name}' returns non-true result: {res}")
                    except Exception as e:
                        exception = f'{type(e).__name__}: {e}'
                        # set to FAIL due to exceptions
                        attr['status'] = StatusType.FAIL
                    yield dict(name=node,
                               exception=exception,
                               **attr)
                case VariableType.SUB_CONCLUSION | VariableType.CONCLUSION:
                    attr['status'] = StatusType.PASS
                    yield dict(name=node, **attr)
