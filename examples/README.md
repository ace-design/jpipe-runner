# Examples

This folder contains example models, library scripts, and workflows.

## Folder organization

```text
.
├── README.md                          # Folder README
├── images                             # Model images
│   ├── fair.png
│   ├── notebook_quality.png
│   ├── pep8_linear.png
│   ├── pinned_paths.png
│   ├── reproducible.png
│   └── slides.png
├── libraries                          # Library scripts for jPipe Runner
│   ├── notebook.py
│   └── slides.py
├── models                             # Model JD files
│   ├── 01_slides.jd                   # Used in workflow step: `Justify Slides`
│   ├── 01_slides.json
│   ├── 02_quality_full.jd             # Used in workflow step: `Justify Notebook Quality`
│   ├── 03_quality_compo.jd
│   └── 04_pattern.jd
└── workflows -> ../.github/workflows  # Symlinked example workflows folder
```

## Action Workflow Usage

For example, consider the `Justify Slides` check in [workflows/runner.yml](../.github/workflows/runner.yml).

```yaml
  - name: Justify Slides
    uses: ace-design/jpipe-runner@main
    with:
      jd_file: "examples/models/01_slides.jd"
      variable: |
        signature:jason
        available:ready
      library: |
        examples/libraries/slides.py
```

The first step is to make sure that it `uses` the correct jpipe runner action:

```yaml
uses: ace-design/jpipe-runner@main
```

The version of jpipe runner action is pointed to the `main` branch for convenience, but any other valid version tag or git commit is also available.

Then, users need to define:

- `jd_file`: which JD file to justify with the runner.
- `variable`: all the required variables, separated by colon:
  - E.g., `var_name:var_value`, var_value can be any valid literal structures like `foo:i-am-a-string` or `bar:12345`.
  - Python literal structures: strings, bytes, numbers, tuples, lists, dicts, sets, booleans, and None.
- `library`: paths to all required library scripts with wildcard support.

For more detailed jPipe Runner action arguments, please refer to the `inputs` field in the [action.yml](../action.yml).

### Use in Poetry Environment

When working with Poetry or other Python env management tools, users must first manually set up their Python env.

```yaml
  - name: Create/Set up Poetry environment
    run: |
      cd examples
      poetry init -n
      poetry config virtualenvs.in-project true
      poetry add rich

  - name: Justify Notebook Quality
    uses: ace-design/jpipe-runner@main
    with:
      jd_file: "models/02_quality_full.jd"
      python_path: "poetry run python"
      working_directory: "./examples"
      variable: |
        notebook:notebook.ipynb
      library: |
        libraries/notebook.py
```

Also, there are additional options that may need to be specified:

- `python_path`: the Python path you want to use to run jpipe-runner.
- `working_directory`: the path to your Python project, leave empty if it's in the current directory.
