## [0.5.1](https://github.com/Bornegrim/hivebox/compare/v0.5.0...v0.5.1) (2025-07-29)


### Bug Fixes

* **ci:** pin black version to 25.1.0 and add conditional for Docker image push ([354439a](https://github.com/Bornegrim/hivebox/commit/354439a58ddbc42591e14ef2c38374d75ee748a8))
* restore black installation in CI and ensure it's listed in requirements ([07e4330](https://github.com/Bornegrim/hivebox/commit/07e43308d0de901962d52aff9590fdce1d8651ca))

# [0.5.0](https://github.com/Bornegrim/hivebox/compare/v0.4.1...v0.5.0) (2025-07-29)


### Bug Fixes

* add permissions for security-events in semgrep job to enable SARIF uploads ([d364e54](https://github.com/Bornegrim/hivebox/commit/d364e54cb7ebfd7ed49f17e31fc3dc9cfcf039f2))
* update release job dependencies to include security-scan ([ed1261f](https://github.com/Bornegrim/hivebox/commit/ed1261f58691c86e34c848f034391c5430d9b1b7))
* update SARIF upload action to v3 for improved functionality ([be5021d](https://github.com/Bornegrim/hivebox/commit/be5021d7905d3c5394ef07f8a70f808b98530f92))


### Features

* add semgrep job for security scanning in CI pipeline ([f6c5037](https://github.com/Bornegrim/hivebox/commit/f6c50374a7c1db2f4054add624a318668bf630d3))
* enhance Dockerfile by creating a non-root user for improved security ([25137bc](https://github.com/Bornegrim/hivebox/commit/25137bc8c361d94b410b12144a2c66418c7e2b84))

## [0.4.1](https://github.com/Bornegrim/hivebox/compare/v0.4.0...v0.4.1) (2025-07-29)


### Bug Fixes

* update coverage source path in test results for accurate reporting ([8d08fa4](https://github.com/Bornegrim/hivebox/commit/8d08fa43ff4a36092152e26b5b48001f7a58e3f9))

# [0.4.0](https://github.com/Bornegrim/hivebox/compare/v0.3.0...v0.4.0) (2025-07-29)


### Features

* add Go feature to dev container configuration ([e844749](https://github.com/Bornegrim/hivebox/commit/e84474987fbf3714eef517f4558bf544ffa76def))
* add initial VSCode settings for Python testing and SonarLint integration ([7772824](https://github.com/Bornegrim/hivebox/commit/7772824cdc236edb26a12c662bb28fb1cbade581))
* add permissions for security events in CI lint job ([5e94c25](https://github.com/Bornegrim/hivebox/commit/5e94c2530d42a9acaae46ebea8e6855ff62f4350))
* create hadolint reports directory before linting Dockerfile ([0c0c819](https://github.com/Bornegrim/hivebox/commit/0c0c819f09a620681087c17320f0f8c21df84521))
* enhance CI pipeline with detailed Hadolint reporting and update Python version to 3.13 ([246f5a3](https://github.com/Bornegrim/hivebox/commit/246f5a3ea471352960021166d45c051cd76f2809))
* replace manual Hadolint linting with Hadolint GitHub Action for improved report generation ([4d3365a](https://github.com/Bornegrim/hivebox/commit/4d3365ad7e4ffcdc08889a7c6717902dced4b466))

# [0.3.0](https://github.com/Bornegrim/hivebox/compare/v0.2.0...v0.3.0) (2025-07-29)


### Features

* enhance CI pipeline with test result reporting and coverage directory structure ([cea7871](https://github.com/Bornegrim/hivebox/commit/cea7871c0a444d96f8d14ccffd086e082939204f))

# [0.2.0](https://github.com/Bornegrim/hivebox/compare/v0.1.2...v0.2.0) (2025-07-29)


### Features

* enhance CI pipeline with coverage reporting and update Python version ([a8f58d2](https://github.com/Bornegrim/hivebox/commit/a8f58d28197db1c7e3d2b6f3832a9475d84597a1))

## [0.1.2](https://github.com/Bornegrim/hivebox/compare/v0.1.1...v0.1.2) (2025-07-29)


### Bug Fixes

* add missing permission for publishing Docker images ([6c1b3af](https://github.com/Bornegrim/hivebox/commit/6c1b3aff5785dba4e5f2565ff73b8150b07c2a57))

## [0.1.1](https://github.com/Bornegrim/hivebox/compare/v0.1.0...v0.1.1) (2025-07-28)


### Bug Fixes

* update Docker image repository owner in release job ([a7d5efd](https://github.com/Bornegrim/hivebox/commit/a7d5efd6af58876097ace9a035379b1ab1b0e9c2))

# [0.1.0](https://github.com/Bornegrim/hivebox/compare/v0.0.0...v0.1.0) (2025-07-28)


### Bug Fixes

* remove security-scan dependency from release job ([9caa92c](https://github.com/Bornegrim/hivebox/commit/9caa92c4474dfd307edd9a8b5e31abca6065b055))
* remove temporary Docker image saving and retrieval steps from CI workflow ([f2f923c](https://github.com/Bornegrim/hivebox/commit/f2f923c52cbb58807b8106264802629768bca91b))
* simplify test execution by removing unnecessary image loading step ([225f6dc](https://github.com/Bornegrim/hivebox/commit/225f6dc5be28150b78bb31691304cfb401169a6f))
* update semantic release step to use dry run and simplify execution ([3a76fb0](https://github.com/Bornegrim/hivebox/commit/3a76fb0e60609839809cde839d5df2e979f9e25b))
* update version endpoint test to use current commit SHA ([1c5199a](https://github.com/Bornegrim/hivebox/commit/1c5199a2349057bb0f026bb6a7cf1e7d87e7ce7c))


### Features

* add APP_VERSION argument and environment variable to Dockerfile ([4974355](https://github.com/Bornegrim/hivebox/commit/497435513f16e831e3b12b28daf252f60be64c81))
* enhance CI workflow by adding artifact preparation and temporary Docker image storage ([eb56c88](https://github.com/Bornegrim/hivebox/commit/eb56c881c40c14cab007d2f3940a217954cca6c4))
