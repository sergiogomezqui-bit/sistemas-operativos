#!/usr/bin/bash
for c in echo alias awk gawk nawk bg cal cat chgrp chmod chown clear cp cpio crontab cut df diff env export fdisk fg find gzip halt head ifconfig iostat kill last less netstat ln locate ls man mkdir mv paste printenv ps pstree rm rmdir sed sort ssh swapinfo tail tar top touch traceroute tree uname uptime vmstat wc which who whoami cmp comm dmesg mkfs curl wget lscpu psrinfo jobs; do
  if command -v "$c" >/dev/null 2>&1; then echo "$c: SI"; else echo "$c: NO"; fi
done
echo "---ps aux test---"
ps aux 2>&1 | head -2
echo "---ps ax test---"
ps ax 2>&1 | head -2
