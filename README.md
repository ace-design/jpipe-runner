# jPipe Runner

```text
     _ ____  _               ____                              
   (_)  _ \(_)_ __   ___   |  _ \ _   _ _ __  _ __   ___ _ __ 
   | | |_) | | '_ \ / _ \  | |_) | | | | '_ \| '_ \ / _ \ '__|
   | |  __/| | |_) |  __/  |  _ <| |_| | | | | | | |  __/ |   
  _/ |_|   |_| .__/ \___|  |_| \_\\__,_|_| |_|_| |_|\___|_|   
 |__/        |_|                                              
```

A Justification Runner designed for jPipe.

## Features

- Fully compatible with existing jPipe syntax/grammar.
    - Support `load`, `justification`, `pattern`, and `composition`.
- A keyword-driven operational justification diagram framework.

## Motivation

In the current Justification Diagram of [jPipe](https://github.com/ace-design/jpipe), the primary focus is on describing
_what justification_ to perform and the _reasoning relationship_ between justification and conclusion. However, it does
not elaborate on _how_ to actually execute these justifications in code, resulting in .jd files that are mainly a visual
representation of reasoning — **lacking the capacity to run the justification process** in practice.

In contrast, [Robot Framework](https://github.com/robotframework/robotframework) is a generic automation framework for
acceptance testing. It uses a simple plain-text syntax and can be extended with various libraries.

- It maps the "keyword" that appears in the test case to a Python (or other language) function for execution.
- This allows the "verification function" to be called directly when writing the test script and get the execution
  result (Pass/Fail), thus enabling an executable test/verification process.

**Inspired by Robot Framework's keyword-driven approach**, we propose to implement a jpipe-runner to make the jPipe
Justification Diagram executable and operational. With this extension, each _justification evidence/strategy_ could be
mapped to corresponding executable code, transforming jPipe from a purely visual reasoning tool into a fully automated
CI/CD-style justification framework.

## Installation

jPipe Runner requires:

- Python (version 3.12 or later)
- [Graphviz](https://www.graphviz.org/) (version 2.46 or later)
- C/C++ Compiler

> [!NOTE]
> These instructions assume you have Python, Graphviz and a C/C++ Compiler on your computer.

### Pip

```shell
$ pip3 install https://github.com/xjasonlyu/jpipe-runner.git
```

### Docker

We currently do not provide jpipe-runner images on the public registry, so you will need to build it yourself.

```shell
$ docker build -t jpipe-runner:latest .
```

### Actions

Alternatively, you can simply integrate jpipe runner into your actions.

```yaml
steps:
- uses: xjasonlyu/jpipe-runner@main
  with:
    jd_file: "/path/to/your/justification.jd"
    variable: |
      key:value
    library: |
      path/to/libraries/*.py
    diagram: "*"
    dry_run: false
```
