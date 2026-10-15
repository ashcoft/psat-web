# Changelog

All notable changes to this project are documented in this file. This file is generated automatically by [semantic-release](https://github.com/semantic-release/semantic-release) from the commit history.

# 1.0.0 (2026-10-15)


### Bug Fixes

* bump vulnerable transitive deps via overrides ([6cd1e7e](https://github.com/ashcoft/psat-web/commit/6cd1e7e1840a21957a5a13e1abd7366b2818b8fd))
* **ci:** bump react-dom to 19.3.0 to match react ([187208e](https://github.com/ashcoft/psat-web/commit/187208ecad26040c8dfa4d64bc39a46c7364bad3))
* correct symbol types and properties for tests ([dd1e850](https://github.com/ashcoft/psat-web/commit/dd1e850f5dedac78484f5e1493d8b4b2cdb5e0e5))
* **deps:** bump react-dom to 19.3.1 to match react 19.3.1 ([148eb68](https://github.com/ashcoft/psat-web/commit/148eb6826d60ad6b00702f78273f133a7ea8ed40)), closes [#182](https://github.com/ashcoft/psat-web/issues/182)
* **deps:** restore missing @next/swc-win32-arm64-msvc lockfile entry ([29fe107](https://github.com/ashcoft/psat-web/commit/29fe107cf5cfab157cb1b24d48e3c7162ea111ab))
* downgrade eslint to v9 for Next.js compatibility ([c483998](https://github.com/ashcoft/psat-web/commit/c4839984095376357d0bbf790dfc91406b17e5c7))
* patch postcss vulnerability with npm override ([6e99244](https://github.com/ashcoft/psat-web/commit/6e992444f0c78aabe616ee4cc07496b9c739147f))
* resolve type errors and add Playwright E2E tests ([06c9f32](https://github.com/ashcoft/psat-web/commit/06c9f3238da56ccbcaa4ec6a991bbc007fddca0a))
* resolve vitest v5 peer dependency conflict ([8c27e65](https://github.com/ashcoft/psat-web/commit/8c27e65210286df6203468e3aa228385235d4677))
* resolve workflow conflicts and make Python checks advisory ([704234e](https://github.com/ashcoft/psat-web/commit/704234e15c2e2b83adf7824212fb0f9b964ad51c))
* simplify Playwright workflow - use webServer config ([4170c25](https://github.com/ashcoft/psat-web/commit/4170c25b22edd3d82727828cfff952523976920c))
* use Chromium-only for Playwright (browser compatibility) ([51fce12](https://github.com/ashcoft/psat-web/commit/51fce12bbbf4c7ac5ec86b3681c2a0117849fc27))


### Features

* Add comprehensive IEC symbol library and Python test workflow ([1b9136c](https://github.com/ashcoft/psat-web/commit/1b9136c2d8590d907233c80bfec36cdd338e4fc2))
* Add Continuation Power Flow (CPF) module ([342d4c3](https://github.com/ashcoft/psat-web/commit/342d4c35fac8cc86dd6f7c3b529a1be4a69aa4b0))
* Add Fault Analysis module ([3da3da0](https://github.com/ashcoft/psat-web/commit/3da3da04a6757f041d6a605ae7b012ae6b6a74d1))
* Add graphical editor hooks and report generation ([2a6c5e9](https://github.com/ashcoft/psat-web/commit/2a6c5e92953f9dcb6ab57e843e78fc6523aa67a7))
* Add multiple power flow methods (DC, Fast-Decoupled, Gauss-Seidel, Newton-Raphson) ([6ac4b90](https://github.com/ashcoft/psat-web/commit/6ac4b902277ac53f983a0ac4b85639f0e3190c55))
* Add Optimal Power Flow (OPF) module ([3c7bac4](https://github.com/ashcoft/psat-web/commit/3c7bac468c5b9fcfe3f586fb81e225532a4f99f9))
* Add Small Signal Stability Analysis module ([9a31eb5](https://github.com/ashcoft/psat-web/commit/9a31eb5443a6132b352bec67aa422b91d31f9a26))
* Add Time Domain Simulation module ([486e13a](https://github.com/ashcoft/psat-web/commit/486e13ac946799d908d8aad5c753b659ad828166))
* Implement PSAT/IEEE standard electrical symbols ([688d918](https://github.com/ashcoft/psat-web/commit/688d918f6138fe83a7fd3f5f927f20f7edc94bc0))
