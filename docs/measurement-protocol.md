# Measurement protocol

No measurement results are prefilled. Use the same physical host, GPU, firmware, vCPU/RAM limits, CPU governor, driver/CUDA libraries, workload and data sizes for Ubuntu 22.04 and the custom image. Record image provenance and hashes, UTC collection time, commands, trial count, warmups and dispersion. Do not equate Ubuntu container results with booting Ubuntu or the custom kernel.

| Metric | Collection / definition |
|---|---|
| Raw logical image bytes | `stat -c %s image.img`; includes partition free space |
| Allocated image bytes | `du -B1 image.img`; depends on sparse allocation/filesystem |
| Compressed bytes | `zstd -T1 -19 -c image.img > image.img.zst`; measure result with stat; same compression for both |
| Used rootfs bytes | Boot both and record `df -B1 /`; distinguish capacity from used bytes |
| Idle RAM KiB | `free -k` at identical idle interval; retain MemTotal/MemAvailable and definition |
| Boot ms | QEMU process start to actual login prompt; same acceleration/firmware; report multiple cold trials |
| Package count | Buildroot show-info selected target package records versus Ubuntu dpkg-query; disclose different package granularity |
| Kernel bytes | stat the booted bzImage/vmlinuz, not an uncompressed ELF |
| GPU throughput | Same vector-add dimensions/iterations; retain JSON, nvidia-smi and correctness result |
| Power/latency | Actual nvidia-smi samples and whole application wall clock; not kernel-only CUDA event time |

`scripts/compare-distros.sh stock.json custom.json` accepts measured values only. Both files require an identical `measurement_definition` string documenting the matched setup. Keys: raw_logical_bytes, allocated_bytes, compressed_bytes, rootfs_used_bytes, ram_idle_kib, boot_ms, package_count, kernel_bytes, gpu_gbps. Omit missing values; they remain NOT TESTED. Do not insert target values into these files.

Reduction (%) = ((Stock Size − Custom Size) / Stock Size) × 100. Choose the assignment's image metric explicitly before evaluating 40%. A 4 GiB filesystem capacity does not mean 4 GiB used or compressed. The historical 3,200 MB versus 1,450 MB claim is withdrawn pending actual comparable artifacts. If reduction falls short, use `make graph-size`, review unused debugging/framework packages, rebuild, and explain the essential GPU library cost with actual size reports.
