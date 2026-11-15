# Feature Regression Checklist

Run `python3 scripts/verify-project.py`, `python3 scripts/test-regressions.py`, a clean build, image validation, firmware QEMU smoke, verify-runtime, real GPU vector-add, separate cuDNN inference, container-smoke and matched Ubuntu comparison. Preserve raw logs. Use `--release` to reject incomplete verification. See final-audit-report.md for actual status.
