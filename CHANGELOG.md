# Changelog

<!--
    You should *NOT* be adding new change log entries to this file, this
    file is managed by towncrier. You *may* edit previous change logs to
    fix problems like typo corrections or such.
    To add a new change log entry, please see
    https://pip.pypa.io/en/latest/development/contributing/#news-entries
    we named the news folder "changelog.d", and use Markdown to format
    entries.

    WARNING: Don't drop the next directive!
-->

<!-- Towncrier release notes start -->

## [Pyright Analysis 1.0.0](https://github.com/mjpieters/pyright-analysis/tree/v1.0.0) (2025-01-22)


### Features

- Added a footer linking back to the project ([#71](https://github.com/mjpieters/pyright-analysis/issues/71))


## [Pyright Analysis 1.0.0rc3](https://github.com/mjpieters/pyright-analysis/tree/v1.0.0rc3) (2025-01-01)


### Bugfixes

- Output intended for stderr now actually goes to stderr. ([#42](https://github.com/mjpieters/pyright-analysis/issues/42))


## [Pyright Analysis 1.0.0rc2](https://github.com/mjpieters/pyright-analysis/tree/v1.0.0rc2) (2024-12-30)


### Features

- When exporting to HTML, JSON or an image the target filename is reported to
  stderr. ([#26](https://github.com/mjpieters/pyright-analysis/issues/26))



### Bugfixes

- Fix format selection for image exports with an explicit filename. ([#24](https://github.com/mjpieters/pyright-analysis/issues/24))


## [Pyright Analysis 1.0.0rc1](https://github.com/mjpieters/pyright-analysis/tree/v1.0.0rc1) (2024-12-28)


### Features

- Add a --version option ([#14](https://github.com/mjpieters/pyright-analysis/issues/14))



### Bugfixes

- Improve handling of kaleido browser detection failures in the cli, providing
  feedback only when trying to export a graph to an image. ([#1](https://github.com/mjpieters/pyright-analysis/issues/1))
- Avoid using itemgetter with Pydantic, fixes pyright JSON parsing in Python
  3.12. ([#2](https://github.com/mjpieters/pyright-analysis/issues/2))
- Mark all optional fields in the pyright typeCompletenessReport object as such. ([#3](https://github.com/mjpieters/pyright-analysis/issues/3))


## [Pyright Analysis 1.0.0a0](https://github.com/mjpieters/pyright-analysis/tree/v1.0.0a0) (2024-12-26)

_Initial release_.
