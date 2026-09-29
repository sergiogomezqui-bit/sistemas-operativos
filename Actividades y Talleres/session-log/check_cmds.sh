#!/bin/bash
for c in echo alias awk bg cal cat chgrp chmod chown clear cp cpio crontab cut df diff env export fdisk fg find gawk gzip halt head ifconfig iostat kill last less netstat ln locate ls man mkdir mv paste printenv ps pstree rm rmdir sed sort ssh swapinfo tail tar top touch traceroute tree uname uptime vmstat wc which who whoami cmp comm dmesg mkfs curl wget lscpu jobs boot; do
  if command -v "$c" >/dev/null 2>&1; then echo "$c: SI"; else echo "$c: NO"; fi
done
