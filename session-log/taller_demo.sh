#!/bin/bash
echo '### crear zombie de ejemplo ###'
perl -e 'if (fork()==0){exit 0} else {sleep 3}' &
sleep 1
ps -eo pid,ppid,stat,cmd | awk '$3 ~ /Z/ {print}'
echo

echo '### renice demo ###'
sleep 100 &
PID=$!
echo "PID de prueba: $PID, prioridad actual:"
ps -o pid,ni,cmd -p $PID
renice -n 5 -p $PID
ps -o pid,ni,cmd -p $PID
kill $PID
echo

echo '### cat para leer archivo ###'
echo -e 'linea1\nlinea2' > /tmp/demo.txt
cat /tmp/demo.txt
echo

echo '### awk 3 columnas, imprimir columna 2 ###'
printf 'ana 25 bogota\njuan 30 medellin\nluis 22 cali\n' > /tmp/datos.txt
cat /tmp/datos.txt
echo '--- awk imprime columna 2 ---'
awk '{print $2}' /tmp/datos.txt
echo

echo '### swapinfo (no nativo en linux) ###'
swapinfo 2>&1 || echo 'swapinfo: command not found (no es comando nativo de Linux)'
echo '--- equivalente en Linux: free -h ---'
free -h
