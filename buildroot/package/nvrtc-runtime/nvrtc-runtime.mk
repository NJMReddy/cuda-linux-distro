NVRTC_RUNTIME_VERSION = 12.4.127
NVRTC_RUNTIME_SITE = https://developer.download.nvidia.com/compute/cuda/redist/cuda_nvrtc/linux-x86_64
NVRTC_RUNTIME_SOURCE = cuda_nvrtc-linux-x86_64-12.4.127-archive.tar.xz
NVRTC_RUNTIME_LICENSE = NVIDIA proprietary license
NVRTC_RUNTIME_LICENSE_FILES = LICENSE
NVRTC_RUNTIME_REDISTRIBUTE = NO
define NVRTC_RUNTIME_INSTALL_TARGET_CMDS
	$(INSTALL) -d $(TARGET_DIR)/usr/lib
	test -d $(@D)/lib
	cp -a $(@D)/lib/libnvrtc*.so* $(TARGET_DIR)/usr/lib/
	$(INSTALL) -D -m 0644 $(@D)/LICENSE $(TARGET_DIR)/usr/share/licenses/nvrtc-runtime/LICENSE
endef
$(eval $(generic-package))
