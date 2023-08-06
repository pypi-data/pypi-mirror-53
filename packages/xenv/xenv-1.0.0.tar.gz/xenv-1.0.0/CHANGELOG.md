# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed
- Replace `optparse` with `argparse` (!3, #1)

### Added
- Allow scripts derived from `xenv` to print their version (!5)

### Fixed
- Fix crash in expansion of self referencing variable (#5, !11)
- Fix loading of Python2 generated `.xenvc` from Python3 (#4, !10)
- Preserve the system's environment (!4, #3)


## [0.0.4] - 2018-12-20
### Fixed
- Fix crash in expansion of self referencing variable (#5, !12)


## [0.0.3] - 2018-12-09
### Fixed
- Actually Fix loading of Python2 generated `.xenvc` from Python3 (#4, !9)


## [0.0.2] - 2018-12-07
### Fixed
- Fix loading of Python2 generated `.xenvc` from Python3 (!8)


## 0.0.1 - 2018-02-21
First release as a stand-alone project (outside of [Gaudi](gaudi/Gaudi)).

### Added
- fixed Python 3 support
- Gitlab-CI automatic testing and packaging
- setuptools based configuration to allow installation via [pip](https://pypi.org/project/pip/)


[Unreleased]: https://gitlab.cern.ch/gaudi/xenv/compare/0.0.4...master
[0.0.4]: https://gitlab.cern.ch/gaudi/xenv/compare/0.0.3...0.0.4
[0.0.3]: https://gitlab.cern.ch/gaudi/xenv/compare/0.0.2...0.0.3
[0.0.2]: https://gitlab.cern.ch/gaudi/xenv/compare/0.0.1...0.0.2
