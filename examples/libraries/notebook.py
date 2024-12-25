"""Notebook"""

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


def assess_quality_gates_are_met():
    return all(quality_results)


def notebook_file_exists():
    return notebook in fake_fs
