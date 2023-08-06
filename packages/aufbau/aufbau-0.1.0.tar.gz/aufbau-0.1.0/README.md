aufbau
======

[![Build Status][shield-travis]][info-travis]

A build task runner similar to make/rake/psake/cake/grunt aimed primarily
(for now at least) at creating build scripts for .NET projects in Python.

Usage
-----
Create a Python file in your project called `aufbaufile` or `aufbaufile.py`.

This should contain one or more targets. Each target is a Python function
decorated with the `@target` decorator and taking one argument, `ctx`.

To run the build
----------------
Sample usage:

```python
aufbau [--file FILE] [target [target]]
```

 * `file` is an optional path to a specific aufbau file (rather than the default
   `aufbaufile` or `aufbaufile.py`).
 * `target` is a list of targets to run.

Sample script
-------------

```python
import aufbau
from aufbau.tasks.process import Execute

@target
def clean(ctx):
    ctx.task(Execute).run('rm', '-rf', './output')

@target
@depends_on(clean)
def build(ctx):
    ctx.task(Execute).run('dotnet', 'build')

@target
@depends_on(build)
def test(ctx):
    ctx.task(Execute).run('dotnet', 'test')

@target
@depends_on(test)
def pack(ctx):
    ctx.task(Execute).run('dotnet', 'pack')
```

The `ctx` argument is a class giving some context information on the currently
running task and its build scripts. Properties include:

 * `target`: the target being built. This in turn has the following properties:
   * `name`: the name of the target
   * `action`: the action method being run
   * `deps`: the targets on which this target depends
 * `root`: the root directory, by default the directory containing the build
   script
 * `abspath(self, relpath)`: gets the absolute path to a file or folder relative
   to the build script.
 * `task(self, taskClass)`: initialises a task ready to run it. Common tasks are
   included in the `aufbau.tasks` module and submodules.

[info-travis]:   https://travis-ci.org/jammycakes/aufbau
[shield-travis]: https://img.shields.io/travis/jammycakes/aufbau.svg