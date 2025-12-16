#!/bin/bash
sudo ip link add br0 type dummy
sudo sh -c "echo 0 > /proc/sys/kernel/randomize_va_space"
sudo sh -c "echo 1 > /proc/sys/vm/legacy_va_layout"
sudo mount --bind /proc /home/user/Tenda-AC18/squashfs-root/proc
sudo mount --bind /sys /home/user/Tenda-AC18/squashfs-root/sys
sudo mount --bind /dev /home/user/Tenda-AC18/squashfs-root/dev
sudo chroot /home/user/Tenda-AC18/squashfs-root /bin/sh -c "LD_PRELOAD=/hooks.so /etc_ro/init.d/rcS"