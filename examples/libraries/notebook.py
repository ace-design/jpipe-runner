"""Notebook"""

from rich import print

# This var will be set from CLI
notebook = None

fake_fs = {
    "notebook.ipynb": {
        "pep8_standard": True,
        "linear_exec_order": True,
    },
    "README.md": {},
}

quality_results = []


def check_pep8_coding_standard():
    res = fake_fs[notebook]["pep8_standard"]
    quality_results.append(res)
    return res


def verify_notebook_has_linear_execution_order():
    res = fake_fs[notebook]["linear_exec_order"]
    quality_results.append(res)
    return res


def assess_quality_gates_are_met():
    print("Assessing all quality gates!")
    return all(quality_results)


def notebook_file_exists():
    global notebook
    if notebook not in fake_fs:
        raise FileNotFoundError(f"notebook '{notebook}' not found")
    return True
