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
