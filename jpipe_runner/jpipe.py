"""
jpipe_runner.jpipe
~~~~~~~~~~~~~~~~~~

This module contains the core of jPipe Runner.
"""

from copy import deepcopy
from typing import Optional

import networkx as nx
from networkx.drawing.nx_agraph import to_agraph

from jpipe_runner.enums import ClassType, VariableType
from jpipe_runner.exceptions import InvalidJustificationException
from jpipe_runner.models import JustificationDef, ClassDef
from jpipe_runner.parser import load_jd_file


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

    def validate(self) -> None:
        pass

    def export_to_image(self,
                        path: Optional[str] = None,
                        format: Optional[str] = None,
                        ) -> bytes | None:
        agraph = to_agraph(self)

        agraph.graph_attr.update(
            size="8，8",
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

        for node in self.nodes(data=True):
            attr = self.node_attr_map[node[1]["var_type"]]
            agraph_node = agraph.get_node(node[0])
            agraph_node.attr.update({
                (k, v)
                for k, v in attr.items()
                if v is not None
            })

        return agraph.draw(path=path, format=format, prog="dot")


class JPipe:

    def __init__(self,
                 jd_file: str,
                 ):
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
                        )

        for support in supports:
            jd.add_edge(support.left, support.right)

        jd.validate()
        return jd
