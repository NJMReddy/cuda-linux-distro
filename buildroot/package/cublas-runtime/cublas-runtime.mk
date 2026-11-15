CUBLAS_RUNTIME_VERSION = 12.4.5.8
CUBLAS_RUNTIME_SITE = https://developer.download.nvidia.com/compute/cuda/redist/libcublas/linux-x86_64
CUBLAS_RUNTIME_SOURCE = libcublas-linux-x86_64-12.4.5.8-archive.tar.xz
CUBLAS_RUNTIME_LICENSE = NVIDIA proprietary license
CUBLAS_RUNTIME_LICENSE_FILES = LICENSE
CUBLAS_RUNTIME_REDISTRIBUTE = NO
define CUBLAS_RUNTIME_INSTALL_TARGET_CMDS
	$(INSTALL) -d $(TARGET_DIR)/usr/lib
	test -d $(@D)/lib
	cp -a $(@D)/lib/libcublas*.so* $(TARGET_DIR)/usr/lib/
	$(INSTALL) -D -m 0644 $(@D)/LICENSE $(TARGET_DIR)/usr/share/licenses/cublas-runtime/LICENSE
endef
$(eval $(generic-package))
