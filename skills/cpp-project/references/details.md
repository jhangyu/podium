# C++ Project Scaffolding — Detailed Reference

Cross-compile toolchain and dev-tool configuration detail for the `cpp-project` skill.
See `../SKILL.md` for the navigation/quick-start entry point.

## Android NDK Toolchain

**cmake/toolchains/android-arm64.cmake**:

```cmake
set(CMAKE_SYSTEM_NAME Android)
set(CMAKE_SYSTEM_VERSION 24)
set(CMAKE_ANDROID_ARCH_ABI arm64-v8a)
set(CMAKE_ANDROID_STL_TYPE c++_static)

if(NOT CMAKE_ANDROID_NDK)
    if(DEFINED ENV{ANDROID_NDK_HOME})
        set(CMAKE_ANDROID_NDK $ENV{ANDROID_NDK_HOME})
    else()
        message(FATAL_ERROR "Set ANDROID_NDK_HOME or pass -DCMAKE_ANDROID_NDK=...")
    endif()
endif()
```

## Dev Tool Configs

**.clang-format**:

```yaml
BasedOnStyle: Google
IndentWidth: 4
ColumnLimit: 100
AllowShortFunctionsOnASingleLine: Empty
AllowShortIfStatementsOnASingleLine: Never
BreakBeforeBraces: Attach
PointerAlignment: Left
SortIncludes: CaseSensitive
IncludeBlocks: Regroup
```

**.clang-tidy**:

```yaml
Checks: >
  -*,
  bugprone-*,clang-analyzer-*,cppcoreguidelines-*,
  misc-*,modernize-*,performance-*,readability-*,
  -modernize-use-trailing-return-type,
  -readability-magic-numbers,
  -cppcoreguidelines-avoid-magic-numbers
WarningsAsErrors: ''
HeaderFilterRegex: '.*'
```

**.gitignore**:

```
build*/
cmake-build-*/
.cache/
compile_commands.json
*.o *.a *.so *.dylib *.dll
.DS_Store
.vscode/ .idea/
```

**scripts/build.sh**:

```bash
#!/usr/bin/env bash
set -euo pipefail
PRESET="${1:-debug}"
cmake --preset "$PRESET"
cmake --build --preset "$PRESET" -j "$(nproc 2>/dev/null || sysctl -n hw.ncpu)"
[[ "$PRESET" == "debug" ]] && ctest --preset debug
```
