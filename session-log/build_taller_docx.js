const fs = require("fs");
const {
  Document, Packer, Paragraph, TextRun, HeadingLevel,
  Table, TableRow, TableCell, WidthType, ShadingType, BorderStyle,
} = require("docx");

const PAGE = { size: { width: 12240, height: 15840 } }; // US Letter

function h1(text) {
  return new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun({ text, bold: true })] });
}
function h2(text) {
  return new Paragraph({ heading: HeadingLevel.HEADING_2, spacing: { before: 240 }, children: [new TextRun({ text, bold: true })] });
}
function p(text, opts = {}) {
  return new Paragraph({ children: [new TextRun({ text, ...opts })], spacing: { after: 120 } });
}
function label(text) {
  return new TextRun({ text, bold: true });
}
function answer(text) {
  return new TextRun({ text: "  " + text, color: "1155CC", bold: true });
}
function qa(question, ans) {
  return new Paragraph({
    children: [label(question), answer(ans)],
    spacing: { after: 80 },
  });
}
function outputBlock(lines) {
  return new Paragraph({
    shading: { type: ShadingType.CLEAR, fill: "F2F2F2" },
    border: {
      top: { style: BorderStyle.SINGLE, size: 4, color: "999999" },
      bottom: { style: BorderStyle.SINGLE, size: 4, color: "999999" },
      left: { style: BorderStyle.SINGLE, size: 4, color: "999999" },
      right: { style: BorderStyle.SINGLE, size: 4, color: "999999" },
    },
    spacing: { after: 200 },
    children: lines.map((l, i) => new TextRun({ text: l, font: "Consolas", size: 18, break: i === 0 ? 0 : 1 })),
  });
}

const doc = new Document({
  sections: [
    {
      properties: { page: { size: PAGE.size } },
      children: [
        new Paragraph({ heading: HeadingLevel.TITLE, children: [new TextRun({ text: "Taller - Agosto 25 2026" })] }),
        p("Sistemas Operativos - UAO. Taller resuelto y verificado sobre una maquina Linux (Ubuntu 26.04 via WSL2)."),

        h1("Punto 1"),
        p("Una vez encendida la maquina con un sistema operativo LINUX, ejecute un comando que permita saber donde esta usted ubicado; y desde esa misma ubicacion ejecute los comandos que identifiquen el nombre de la maquina; y de informacion del sistema; y alli mismo ejecute las instrucciones para verificar las variables del SHELL actual; ahora escriba la instruccion que limpie la pantalla de la terminal:"),

        qa("Comando para saber donde esta ubicado:", "pwd"),
        outputBlock(["$ pwd", "/mnt/c/Users/Sergio Gomez/Downloads/UAO/SISTEMAS OPERATIVOSD"]),

        qa("Comando que identifica el nombre de la maquina:", "hostname"),
        outputBlock(["$ hostname", "DESKTOP-8T2JB98"]),

        qa("Comando que da informacion del sistema:", "uname -a"),
        outputBlock(["$ uname -a", "Linux DESKTOP-8T2JB98 6.18.33.2-microsoft-standard-WSL2 #1 SMP PREEMPT_DYNAMIC", "Thu Jun 18 21:54:43 UTC 2026 x86_64 GNU/Linux"]),

        qa("Instruccion para verificar las variables del SHELL actual:", "echo $SHELL   (o tambien: env | grep -i shell)"),
        outputBlock(["$ env | grep -i shell", "SHELL=/bin/bash"]),

        qa("Instruccion que limpia la pantalla de la terminal:", "clear"),
        p("clear borra el contenido visible de la terminal reposicionando el cursor; no produce salida de texto capturable, ya que su efecto es visual sobre la pantalla."),

        h1("Punto 2"),
        p("Realice una instruccion que imprima en pantalla los procesos de usuario; y con otro comando muestre las estadisticas de CPU; ahora ejecute un comando que imprima en pantalla el inicio y cierre de sesion de los usuarios conectados a la maquina; identifique y relacione los procesos zombis que estan en el sistema; cambie y describa un cambio de prioridad en un proceso cualquiera; se requiere leer un archivo, que comando ejecutaria?; cree un archivo con tres columnas de datos y por medio de un mandato AWK imprima en pantalla la segunda columna; y por ultimo al ejecutar la orden SWAPINFO que informacion obtengo?"),

        qa("Comando que imprime los procesos de usuario:", "ps aux"),
        outputBlock([
          "$ ps aux",
          "USER   PID %CPU %MEM  VSZ  RSS TTY   STAT START TIME COMMAND",
          "root     1  8.0  0.1 24084 15372 ?    Ss   19:13 0:00 /sbin/init",
          "root    46  1.3  0.1 33836 13068 ?    S<s  19:14 0:00 systemd-journald",
          "root   452  0.2  0.0  6136  5368 pts/1 Ss+ 19:14 0:00 -bash",
          "...   (lista completa de procesos del sistema, formato BSD extendido)",
        ]),

        qa("Comando que muestra estadisticas de CPU:", "vmstat"),
        outputBlock([
          "$ vmstat",
          "procs -----------memory---------- ---swap-- -----io---- -system-- -------cpu-------",
          " r  b   swpd   free   buff  cache   si   so    bi    bo   in   cs us sy id wa st gu",
          " 0  0      0 6829060  49152 548248    0    0 29413   554 7752    3  3  6 90  1  0  0",
        ]),

        qa("Comando para inicio/cierre de sesion de usuarios conectados:", "last"),
        p("Nota tecnica: last es el comando estandar en Solaris, FreeBSD y en instalaciones tradicionales de Linux/OracleLinux (lee /var/log/wtmp). Esta instalacion minima de Ubuntu 26.04 (WSL) no trae wtmp ni el binario last preinstalados, por lo que se verifico con el comando equivalente who, que muestra las sesiones activas en este momento:"),
        outputBlock(["$ who", "(sin salida: no hay sesiones interactivas abiertas via login en este contenedor WSL)"]),

        qa("Identificacion de procesos zombis:", "ps -eo pid,ppid,stat,cmd | awk '$3 ~ /Z/ {print}'"),
        p("Se genero un proceso hijo deliberadamente huerfano (fork() sin wait()) para forzar un zombie de prueba:"),
        outputBlock([
          "$ perl -e 'if (fork()==0){exit 0} else {sleep 3}' &",
          "$ ps -eo pid,ppid,stat,cmd | awk '$3 ~ /Z/ {print}'",
          "  420   418 Z+   [perl] <defunct>",
        ]),
        p("El estado Z (o Z+) en la columna STAT identifica un proceso zombie: termino su ejecucion pero su proceso padre (PPID 418) aun no ha leido su codigo de salida con wait(), por lo que el kernel conserva su entrada en la tabla de procesos."),

        qa("Cambio de prioridad de un proceso:", "renice -n 5 -p PID"),
        outputBlock([
          "$ sleep 100 &",
          "$ ps -o pid,ni,cmd -p 423",
          "  PID  NI CMD",
          "  423   0 sleep 100",
          "$ renice -n 5 -p 423",
          "423 (process ID) old priority 0, new priority 5",
          "$ ps -o pid,ni,cmd -p 423",
          "  PID  NI CMD",
          "  423   5 sleep 100",
        ]),
        p("renice cambia el valor de 'nice' (NI) de un proceso ya en ejecucion. El rango va de -20 (maxima prioridad, solo root) a 19 (minima prioridad). Aqui se subio el NI de 0 a 5, bajando su prioridad de planificacion: el scheduler le asignara relativamente menos tiempo de CPU frente a otros procesos."),

        qa("Comando para leer un archivo:", "cat archivo"),
        outputBlock(["$ echo -e 'linea1\\nlinea2' > /tmp/demo.txt", "$ cat /tmp/demo.txt", "linea1", "linea2"]),

        qa("Archivo de 3 columnas + AWK imprimiendo la segunda columna:", "awk '{print $2}' archivo"),
        outputBlock([
          "$ printf 'ana 25 bogota\\njuan 30 medellin\\nluis 22 cali\\n' > /tmp/datos.txt",
          "$ cat /tmp/datos.txt",
          "ana 25 bogota",
          "juan 30 medellin",
          "luis 22 cali",
          "$ awk '{print $2}' /tmp/datos.txt",
          "25",
          "30",
          "22",
        ]),

        qa("Que informacion da SWAPINFO:", "no es un comando nativo de Linux"),
        p("swapinfo es el comando nativo de FreeBSD (y de HP-UX) para reportar el espacio de intercambio (swap): dispositivo/archivo de swap, tamanio total, espacio usado y espacio libre, en formato tabular. Verificado en vivo: en Solaris NO existe swapinfo tampoco -- Solaris usa 'swap -s' / 'swap -l' (se confirmo con acceso root real a la VM de Solaris: 'swap -s' devolvio 'total: 549904k bytes allocated + 363016k reserved = 912920k used, 5608124k available'). En Linux (incluido Oracle Linux) el binario tampoco existe; el equivalente funcional es free -h o swapon --show, verificado a continuacion:"),
        outputBlock([
          "$ swapinfo",
          "bash: swapinfo: command not found",
          "$ free -h",
          "              total   used   free  shared  buff/cache  available",
          "Mem:          7.6Gi  620Mi  6.6Gi   3.5Mi       569Mi      7.0Gi",
          "Swap:         2.0Gi     0B  2.0Gi",
        ]),

        h1("Metodologia"),
        p("Todos los comandos de este taller se ejecutaron realmente sobre una maquina Ubuntu 26.04 (WSL2) preparada para el curso, y las salidas mostradas en los recuadros son la salida real capturada, no simulada. Ver session-log/GRAPH_REPORT.md y sesion_2026-08-19.md para el detalle completo del entorno preparado (VirtualBox, VMs de Solaris y FreeBSD, WSL/Ubuntu)."),
      ],
    },
  ],
});

Packer.toBuffer(doc).then((buf) => {
  fs.writeFileSync("Taller_agosto25_2026_RESUELTO.docx", buf);
  console.log("Written Taller_agosto25_2026_RESUELTO.docx");
});
