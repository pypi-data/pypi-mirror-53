# mercurial-litf

A litf compatible plugin for the [Mercurial](https://www.mercurial-scm.org/) test runner.

It can be used with [Balto: BAlto is a Language independent Test Orchestrator](https://lothiraldan.github.io/balto/).

# Installation


You can install "mercurial-litf" via
[pip](https://pypi.python.org/pypi/pip/) from
[PyPI](https://pypi.python.org/pypi):

```
    $ pip install mercurial-litf
```

# Configuration

The mercurial-litf CLI need to find where the Mercurial test-runner is located. It reads the `MERCURIAL_RUN_TESTS_PATH` environment variable in order to do so, please ensure it's defined in your environment.
