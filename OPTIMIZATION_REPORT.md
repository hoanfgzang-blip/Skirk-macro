# Electron frontend size audit

## Executive summary

The existing Windows unpacked build is **356.45 MiB**. The frontend application
archive is about 0.36 MiB; the main contributors are the bundled Python
executable (215.06 MiB, explicitly out of scope) and Electron/Chromium runtime.

This change keeps only the English and Vietnamese Chromium locale packs. A
fresh production package measured **310.94 MiB**, down **45.51 MiB (12.8%)**
from 356.45 MiB, while retaining the languages relevant to this application.

## Findings and implemented changes

### Chromium locales

**Problem:** Electron 43 supplied 55 locale packs totaling 46.63 MiB.

**Impact:** Retaining `en-US` and `vi` removes 45.33 MiB of locale data. It also
reduces installed-file count and installer payload. Other Chromium UI locales
will fall back to English.

**Change:** `build.win.electronLanguages` now explicitly includes `en-US` and
`vi`. This is an electron-builder-supported option and applies before artifacts
are created.

**Risk:** Low, provided English/Vietnamese are the intended supported Chromium
locales.

### Duplicate image asset

**Problem:** `logo.png` and `icon.png` had the same SHA-256 and were each
0.182 MiB.

**Impact:** Removes one 0.182 MiB asset from the packaged application.

**Change:** The visible logo now references `icon.png`; `logo.png` was removed
from the package allow-list. The unused source file can be deleted separately.

**Risk:** Low. The files were byte-identical.

### Packaging rules

**Problem:** ASAR was enabled by electron-builder defaults but not declared;
the project only produced an unpacked directory despite installer size being a
priority.

**Impact:** Explicit ASAR protects the small frontend payload from accidental
unpacking. `pnpm package:win:installer` now creates an NSIS installer; maximum
compression is selected for distribution artifacts. It may increase build time
and does not reduce the unpacked app.

**Change:** Added `asar`, `compression`, an installer script, and retained the
strict runtime file allow-list. Tests, source maps, documentation, Git files,
and `node_modules` are not packaged.

**Risk:** Low. The existing `pnpm package:win` directory build remains intact.

### Renderer security and startup work

**Problem:** The renderer enabled Node integration and disabled context
isolation despite using only browser APIs. The main process eagerly loaded
shutdown-only modules.

**Impact:** No material installer-size change; reduces renderer privilege and
avoids loading `http` and `execSync` until shutdown.

**Change:** Enabled `contextIsolation` and sandboxing, disabled Node
integration, and lazily require shutdown-only APIs. Localhost JSON requests
are unchanged.

**Risk:** Low, verified statically against `fe.js`: it contains no `require`,
`process`, or Electron API access.

## High priority changes

1. Keep only `en-US` and `vi` Electron locales (implemented and measured).
2. Build distribution artifacts with `pnpm package:win:installer` after
   validating the unpacked build.

## Medium priority changes

1. Keep the explicit ASAR and strict runtime file allow-list (implemented).
2. Keep the duplicate logo out of the package (implemented).

## Low priority changes

1. Retain lazy shutdown-only imports and the hardened renderer configuration
   (implemented; negligible size effect).
2. Benchmark a pinned alternate Electron version only in a separate
   compatibility-tested change.

## Measured size contributors before optimization

| Component | Size |
| --- | ---: |
| Python backend executable (out of scope) | 215.06 MiB |
| Chromium locales | 46.63 MiB |
| DirectX shader compiler | 24.43 MiB |
| Chromium licenses | 19.37 MiB |
| ICU data | 10.37 MiB |
| App resources (including backend copy) | 9.29 MiB |
| Remaining Electron runtime | 31.30 MiB |
| **Total** | **356.45 MiB** |

## Estimated size reduction

| Optimization | Estimated / measured reduction |
| --- | ---: |
| Remove unused Electron locales | 45.33 MiB measured |
| Remove duplicate packaged image | 0.18 MiB measured |
| Installer maximum compression | Not measured; generally small |
| JavaScript/startup cleanup | Negligible size |
| **Total unpacked reduction** | **45.51 MiB measured** |

## Recommendations not applied

| Finding | Reason not applied | Expected reduction | Risk |
| --- | --- | ---: | --- |
| Remove `LICENSES.chromium.html` | Legal notices should be retained. | 19.37 MiB | High/legal |
| Remove `dxcompiler.dll`, `dxil.dll`, Vulkan, or SwiftShader | Electron may use these for GPU/WebGL fallback; the UI must remain identical. | Up to 32 MiB | Medium–High |
| Change Electron version | No compatibility test matrix or alternate binary size was provided. Upgrades can increase or decrease runtime size. | Unknown | Medium |
| Replace Electron | Would alter the architecture and risks behavior regressions. | Large but not justified | High |

## Dependency audit

`src/UI/package.json` declares only `electron` and `electron-builder`, both as
development dependencies. The packaged app contains no runtime `node_modules`;
the frontend uses no third-party renderer package. The root `package.json`
contains a separate Electron dependency, but the build scripts install and use
`src/UI`; remove the root dependency only after confirming it is not used by
another developer workflow.

## Implementation order

1. Package and smoke-test the locale-restricted directory build.
2. Generate and QA the NSIS installer with `pnpm package:win:installer`.
3. If further reduction is essential, benchmark an Electron version change;
   do not delete GPU/runtime or legal files without targeted test coverage.

## Validation checklist

- Run `pnpm package:win` from `src/UI` and confirm `locales` contains only
  `en-US.pak` and `vi.pak`.
- Launch `build/app/win-unpacked/Cryss.exe`.
- Confirm the Python executable starts and `/run`, `/save`, and `/shutdown`
  requests still use the existing localhost JSON protocol.
- Confirm the UI matches the pre-change build and key binding/local storage
  still work.
- Run `pnpm package:win:installer` to produce the compressed NSIS installer.
