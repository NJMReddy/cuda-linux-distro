# Kernel size verification

NOT TESTED: no rebuilt bzImage or comparable Ubuntu kernel was available. The earlier 12.8/4.6 MB, 2,840/82-module and boot-time tables are retained only under docs/historical and must not be submitted as measurements.

After compilation save Linux's final `.config` from `buildroot-src/output/build/linux-6.6.18/`, `stat -c %s buildroot-src/output/images/bzImage`, the installed module list and compiler/version details. Compare the same compressed-kernel metric with the Ubuntu kernel actually booted on the matched test host. `kernel/linux.config` is the requested input, not proof of resolved options or a complete build.
