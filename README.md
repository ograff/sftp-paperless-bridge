# sftp-paperless-bridge

[![Release](https://img.shields.io/github/v/release/ograff/sftp-paperless-bridge)](https://img.shields.io/github/v/release/ograff/sftp-paperless-bridge)
[![Build status](https://img.shields.io/github/actions/workflow/status/ograff/sftp-paperless-bridge/main.yml?branch=main)](https://github.com/ograff/sftp-paperless-bridge/actions/workflows/main.yml?query=branch%3Amain)
[![codecov](https://codecov.io/gh/ograff/sftp-paperless-bridge/branch/main/graph/badge.svg)](https://codecov.io/gh/ograff/sftp-paperless-bridge)
[![Commit activity](https://img.shields.io/github/commit-activity/m/ograff/sftp-paperless-bridge)](https://img.shields.io/github/commit-activity/m/ograff/sftp-paperless-bridge)
[![License](https://img.shields.io/github/license/ograff/sftp-paperless-bridge)](https://img.shields.io/github/license/ograff/sftp-paperless-bridge)

This hosts an sftp server that uploads documents to paperless using the HTTP API

- **Github repository**: <https://github.com/ograff/sftp-paperless-bridge/>
- **Documentation** <https://ograff.github.io/sftp-paperless-bridge/>

## Getting started with your project

First, create a repository on GitHub with the same name as this project, and then run the following commands:

```bash
git init -b main
git add .
git commit -m "init commit"
git remote add origin git@github.com:ograff/sftp-paperless-bridge.git
git push -u origin main
```

Finally, install the environment and the pre-commit hooks with

```bash
make install
```

You are now ready to start development on your project!
The CI/CD pipeline will be triggered when you open a pull request, merge to main, or when you create a new release.

To finalize the set-up for publishing to PyPI or Artifactory, see [here](https://fpgmaas.github.io/cookiecutter-poetry/features/publishing/#set-up-for-pypi).
For activating the automatic documentation with MkDocs, see [here](https://fpgmaas.github.io/cookiecutter-poetry/features/mkdocs/#enabling-the-documentation-on-github).
To enable the code coverage reports, see [here](https://fpgmaas.github.io/cookiecutter-poetry/features/codecov/).

---

Repository initiated with [fpgmaas/cookiecutter-poetry](https://github.com/fpgmaas/cookiecutter-poetry).
