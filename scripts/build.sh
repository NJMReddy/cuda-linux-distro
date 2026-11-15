#!/usr/bin/env bash
set -euo pipefail
PROJECT_ROOT=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)
BUILDROOT_DIR="$PROJECT_ROOT/buildroot-src"
BR2_EXTERNAL="$PROJECT_ROOT/buildroot"
VERSION=2024.02
SHA256=3e6364c062551e35e72e935dae42b969aa594e407898f2f769a7aaaadf0316af
check_dependencies() {
    [[ $(uname -s) == Linux ]] || { echo 'BLOCKED: Buildroot requires Linux; use Ubuntu 22.04/WSL2 on a Linux filesystem.' >&2; return 1; }
    [[ $EUID != 0 ]] || { echo 'Do not build as root.' >&2; return 1; }
    local dep missing=()
    for dep in git make gcc g++ wget cpio file bc rsync unzip python3 bison flex patch perl tar xz gzip bzip2 sha256sum nproc; do
        command -v "$dep" >/dev/null || missing+=("$dep")
    done
    if ((${#missing[@]})); then
        echo "Missing: ${missing[*]}" >&2
        echo 'Ubuntu: sudo apt install build-essential wget cpio file bc rsync unzip python3 bison flex patch perl xz-utils bzip2 libelf-dev libssl-dev libncurses-dev' >&2
        return 1
    fi
    # Compile AND link probes, not merely header-existence checks.
    printf '#include <gelf.h>\nint main(void){return elf_version(EV_CURRENT)==EV_NONE;}\n' |
        gcc -x c - -lelf -o /dev/null || { echo 'Install libelf-dev (objtool needs gelf.h and libelf).' >&2; return 1; }
    printf '#include <openssl/ssl.h>\nint main(void){return OPENSSL_init_ssl(0,0)!=1;}\n' |
        gcc -x c - -lssl -lcrypto -o /dev/null || { echo 'Install libssl-dev.' >&2; return 1; }
}
check_dependencies
if [[ ${1:-} == --check-host ]]; then exit 0; fi
[[ ${ACCEPT_NVIDIA_LICENSES:-0} == 1 ]] || {
    echo 'Read docs/licenses.md. Set ACCEPT_NVIDIA_LICENSES=1 only after reviewing the NVIDIA terms.' >&2; exit 1;
}
mkdir -p "$PROJECT_ROOT/dl" "$PROJECT_ROOT/verification"
archive="$PROJECT_ROOT/dl/buildroot-$VERSION.tar.xz"
if [[ ! -d "$BUILDROOT_DIR" ]]; then
    [[ -f $archive ]] || wget -O "$archive" "https://buildroot.org/downloads/buildroot-$VERSION.tar.xz"
    echo "$SHA256  $archive" | sha256sum -c -
    tar -xJf "$archive" -C "$PROJECT_ROOT"
    mv "$PROJECT_ROOT/buildroot-$VERSION" "$BUILDROOT_DIR"
    echo "$SHA256" > "$BUILDROOT_DIR/.cuda-source-sha256"
else
    [[ -f "$BUILDROOT_DIR/.cuda-source-sha256" ]] &&
        [[ $(cat "$BUILDROOT_DIR/.cuda-source-sha256") == "$SHA256" ]] || {
            echo 'Existing buildroot-src is not identified as the pinned source. Preserve it by renaming it, then retry.' >&2; exit 1;
        }
fi
# ZIP extraction does not reliably preserve Unix executable bits.
chmod +x "$PROJECT_ROOT"/scripts/*.sh "$BR2_EXTERNAL"/board/cuda-distro/*.sh
make -C "$BUILDROOT_DIR" BR2_EXTERNAL="$BR2_EXTERNAL" cuda_distro_defconfig
python3 "$PROJECT_ROOT/scripts/check-config.py" "$BUILDROOT_DIR/.config"
stamp=$(date -u +%Y%m%dT%H%M%SZ)
make -C "$BUILDROOT_DIR" BR2_EXTERNAL="$BR2_EXTERNAL" -j"${JOBS:-$(nproc)}" 2>&1 | tee "$PROJECT_ROOT/verification/build-$stamp.log"
python3 "$PROJECT_ROOT/scripts/verify-project.py" --target "$BUILDROOT_DIR/output/target" --images "$BUILDROOT_DIR/output/images"
make -C "$BUILDROOT_DIR" BR2_EXTERNAL="$BR2_EXTERNAL" legal-info
cp "$BUILDROOT_DIR/output/build/linux-6.6.18/.config" "$PROJECT_ROOT/verification/linux.resolved.config"
make --no-print-directory -s -C "$BUILDROOT_DIR" BR2_EXTERNAL="$BR2_EXTERNAL" show-info > "$PROJECT_ROOT/verification/package-manifest.json"
cp "$BUILDROOT_DIR/.config" "$PROJECT_ROOT/verification/buildroot.resolved.config"
echo 'PASS build and artifact checks. Boot and GPU execution are separate tests.'
