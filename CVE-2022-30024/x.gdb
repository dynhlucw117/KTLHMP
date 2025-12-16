set architecture mips
set endian big
set follow-fork-mode parent
file ./reverse/httpd
b*0x0047A294
b*0x0047A500
target extended-remote 192.168.1.1:1111