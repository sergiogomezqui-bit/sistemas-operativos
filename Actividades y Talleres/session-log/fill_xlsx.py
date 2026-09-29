# -*- coding: utf-8 -*-
import openpyxl
import copy

PATH = r"C:\Users\Sergio Gomez\Downloads\UAO\SISTEMAS OPERATIVOSD\ComandosUnixAGOSTO25_2026.xlsx"

# row_number -> (Descripcion, Solaris, FreeBSD, OracleLinux)
DATA = {
4: ("Muestra en pantalla el texto o el valor de variables que se le indiquen.", "SI", "SI", "SI"),
5: ("Crea un nombre corto (alias) para un comando o secuencia de comandos.", "SI", "SI", "SI"),
6: ("Lenguaje de procesamiento de texto orientado a patrones; extrae y transforma columnas de datos.", "SI", "SI", "SI"),
7: ("Reanuda un trabajo detenido y lo continua ejecutando en segundo plano.", "SI", "SI", "SI"),
8: ("Muestra un calendario del mes o del anio actual en la terminal.", "SI", "SI", "SI (paquete util-linux/ncal, no siempre preinstalado)"),
9: ("Concatena y muestra el contenido de uno o mas archivos en pantalla.", "SI", "SI", "SI"),
10: ("Cambia el grupo propietario de un archivo o directorio.", "SI", "SI", "SI"),
11: ("Cambia los permisos de lectura, escritura y ejecucion de un archivo o directorio.", "SI", "SI", "SI"),
12: ("Cambia el usuario propietario (y opcionalmente el grupo) de un archivo o directorio.", "SI", "SI", "SI"),
13: ("Limpia la pantalla de la terminal.", "SI", "SI", "SI"),
14: ("Copia archivos o directorios de un lugar a otro.", "SI", "SI", "SI"),
15: ("Empaqueta o extrae archivos en formato cpio, usado tradicionalmente para copias de respaldo.", "SI", "SI (bsdcpio)", "SI (paquete cpio)"),
16: ("Edita o lista las tareas programadas (cron) de un usuario.", "SI", "SI", "SI"),
17: ("Extrae columnas o campos especificos de cada linea de un archivo de texto.", "SI", "SI", "SI"),
18: ("Muestra el espacio usado y disponible en los sistemas de archivos montados.", "SI", "SI", "SI"),
19: ("Igual que df, pero presenta los tamanios en formato legible (KB, MB, GB).", "SI", "SI", "SI"),
20: ("Compara dos archivos linea por linea y muestra las diferencias entre ellos.", "SI", "SI", "SI"),
21: ("Muestra en pantalla el texto o el valor de variables que se le indiquen.", "SI", "SI", "SI"),
22: ("Muestra las variables de entorno actuales, o ejecuta un programa con un entorno modificado.", "SI", "SI", "SI"),
23: ("Marca una variable de shell para que quede disponible en los procesos hijos (variable de entorno).", "SI", "SI", "SI"),
24: ("Lista las tablas de particiones de los discos del sistema.", "SI (x86; en SPARC se usa format)", "SI (uso limitado; FreeBSD usa gpart)", "SI"),
25: ("Trae al primer plano de la terminal un trabajo que estaba en segundo plano o detenido.", "SI", "SI", "SI"),
26: ("Busca archivos y directorios en un arbol de directorios segun criterios (nombre, tipo, fecha, etc.).", "SI", "SI", "SI"),
27: ("Implementacion de awk de GNU, con extensiones adicionales sobre el awk tradicional.", "NO (trae nawk/oawk; gawk se instala aparte)", "NO (trae one-true-awk en base; gawk via pkg)", "SI (es el awk por defecto)"),
28: ("Comprime o descomprime archivos usando el algoritmo DEFLATE (extension .gz).", "SI", "SI", "SI"),
29: ("Detiene el sistema operativo (apaga la maquina).", "SI", "SI", "SI"),
30: ("Muestra las primeras lineas de un archivo (10 por defecto).", "SI", "SI", "SI"),
31: ("Muestra el historial de comandos ejecutados en la sesion de shell.", "SI", "SI", "SI"),
32: ("Muestra o configura las interfaces de red del sistema.", "SI (nativo)", "SI (nativo, herramienta principal)", "SI (obsoleto; requiere paquete net-tools, se recomienda 'ip')"),
33: ("Muestra estadisticas de uso de CPU y de entrada/salida de los dispositivos de disco.", "SI", "SI", "SI (requiere paquete sysstat)"),
34: ("Lista los trabajos (jobs) activos en la sesion actual de la shell.", "SI", "SI", "SI"),
35: ("Envia una senial (por defecto SIGTERM) a un proceso para terminarlo o controlarlo.", "SI", "SI", "SI"),
36: ("Envia la senial SIGKILL al proceso indicado, forzando su terminacion inmediata.", "SI", "SI", "SI"),
37: ("Muestra el historial de inicios y cierres de sesion de los usuarios (lee /var/log/wtmp).", "SI", "SI", "SI"),
38: ("Muestra el contenido de un archivo de texto pagina por pagina, con desplazamiento en ambas direcciones.", "SI", "SI", "SI"),
39: ("Muestra las conexiones de red activas, con direcciones IP y puertos en forma numerica.", "SI", "SI", "SI (obsoleto; net-tools, alternativa: ss -n)"),
40: ("Crea un enlace duro entre archivos.", "SI", "SI", "SI"),
41: ("Crea un enlace simbolico (symlink) que apunta a otro archivo o directorio.", "SI", "SI", "SI"),
42: ("Busca archivos por nombre usando una base de datos indexada previamente (updatedb).", "NO (no incluido por defecto)", "SI (incluido en el sistema base)", "SI (requiere paquete mlocate/plocate)"),
43: ("Lista el contenido de un directorio.", "SI", "SI", "SI"),
44: ("Lista el contenido del directorio padre (un nivel arriba).", "SI", "SI", "SI"),
45: ("Lista el contenido del directorio actual.", "SI", "SI", "SI"),
46: ("Lista el contenido del directorio /bin, donde estan los binarios esenciales del sistema.", "SI", "SI", "SI"),
47: ("Lista el contenido de un directorio en formato largo (permisos, dueño, tamanio, fecha).", "SI", "SI", "SI"),
48: ("Lista el contenido de un directorio en formato largo, ordenado por fecha de modificacion (mas reciente primero).", "SI", "SI", "SI"),
49: ("Lista en orden inverso los archivos de /etc que empiezan por 't'.", "SI", "SI", "SI"),
50: ("Muestra las paginas de manual (documentacion) de un comando o funcion del sistema.", "SI", "SI", "SI (requiere man-db/man-pages en instalaciones minimas)"),
51: ("Crea uno o mas directorios nuevos.", "SI", "SI", "SI"),
52: ("Mueve o renombra archivos y directorios.", "SI", "SI", "SI"),
53: ("Muestra el estado de las conexiones de red, tablas de rutas y estadisticas de interfaces.", "SI", "SI", "SI (obsoleto; net-tools, alternativa moderna: ss)"),
54: ("En Solaris/FreeBSD muestra estadisticas de buffers de red (STREAMS/mbufs); en Linux esta opcion no existe en net-tools.", "SI (estadisticas STREAMS)", "SI (estadisticas de mbufs)", "NO (opcion -m no soportada por net-tools)"),
55: ("Muestra la tabla de rutas (routing table) del sistema.", "SI", "SI", "SI (requiere net-tools; alternativa: ip route)"),
56: ("Muestra la tabla de rutas junto con estadisticas resumidas del subsistema de red.", "SI", "SI", "SI (requiere net-tools)"),
57: ("Muestra estadisticas detalladas del protocolo TCP (conexiones, segmentos, retransmisiones, etc.).", "SI", "SI", "SI (requiere net-tools; sintaxis puede variar)"),
58: ("Une lineas de varios archivos en columnas, generalmente separadas por tabulador.", "SI", "SI", "SI"),
59: ("No corresponde a un comando estandar de Unix/Linux; probablemente sea un error de digitacion por 'pwd' o 'cd' en el enunciado original.", "NO", "NO", "NO"),
60: ("Imprime en pantalla el valor de las variables de entorno.", "SI", "SI", "SI"),
61: ("Muestra todos los procesos del sistema con informacion detallada (usuario, %CPU, %MEM, etc.) en sintaxis BSD.", "SI (via /usr/ucb/ps; el ps nativo SVR4 usa -ef)", "SI (sintaxis nativa)", "SI (procps soporta sintaxis BSD y SysV)"),
62: ("Muestra todos los procesos del sistema, incluidos los que no tienen terminal asociada (sintaxis BSD).", "SI (via /usr/ucb/ps)", "SI (nativo)", "SI"),
63: ("Muestra los procesos del sistema organizados en forma de arbol jerarquico (padre-hijo).", "SI (incluido en Solaris 11)", "NO (requiere instalar el paquete pstree)", "SI (paquete psmisc)"),
64: ("Elimina archivos o directorios.", "SI", "SI", "SI"),
65: ("Elimina directorios vacios.", "SI", "SI", "SI"),
66: ("Editor de flujo (stream editor) para transformar texto linea por linea mediante expresiones.", "SI", "SI", "SI"),
67: ("Ordena las lineas de un archivo de texto alfabetica o numericamente.", "SI", "SI", "SI"),
68: ("Abre una sesion remota segura (Secure Shell) hacia otro equipo.", "SI", "SI", "SI"),
69: ("Muestra informacion sobre el uso del espacio de intercambio (swap): tamanio total, usado y disponible.", "SI (comando nativo)", "SI (comando nativo)", "NO (no existe en Linux; equivalente: 'free -h' o 'swapon --show')"),
70: ("Muestra las ultimas lineas de un archivo (10 por defecto).", "SI", "SI", "SI"),
71: ("Muestra las ultimas 300 lineas del archivo de log de correo (maillog), util para depurar el servicio de mail.", "SI", "SI", "SI"),
72: ("Empaqueta (y opcionalmente comprime) archivos y directorios en un unico archivo .tar.", "SI", "SI", "SI"),
73: ("Muestra en tiempo real los procesos que mas recursos (CPU/memoria) estan consumiendo.", "SI", "SI", "SI"),
74: ("Crea un archivo vacio si no existe, o actualiza su fecha de modificacion si ya existe.", "SI", "SI", "SI"),
75: ("Muestra la ruta (saltos de red) que siguen los paquetes hasta llegar a un host destino.", "SI", "SI", "SI (requiere paquete traceroute)"),
76: ("Muestra la estructura de directorios y archivos en forma de arbol.", "NO (requiere instalar el paquete tree)", "NO (requiere instalar el paquete tree)", "NO (requiere instalar el paquete tree)"),
77: ("Muestra la version (release) del kernel del sistema operativo.", "SI", "SI", "SI"),
78: ("Muestra toda la informacion del sistema: kernel, version, arquitectura, nombre de host, etc.", "SI", "SI", "SI"),
79: ("Muestra cuanto tiempo lleva encendido el sistema y la carga promedio (load average).", "SI", "SI", "SI"),
80: ("Muestra estadisticas de memoria virtual, procesos, CPU y E/S del sistema.", "SI", "SI", "SI"),
81: ("No es un comando de shell de usuario; en Solaris/SPARC es la instruccion del firmware OpenBoot (ok boot) para arrancar el sistema.", "SI (a nivel de firmware OpenBoot, no como comando de shell)", "NO (FreeBSD usa el menu del loader)", "NO (el arranque lo gestiona GRUB, no un comando de shell)"),
82: ("Muestra estadisticas de vmstat en formato ancho (wide), actualizando cada 5 segundos.", "SI", "NO (no soporta -w; el intervalo se da como argumento: vmstat 5)", "SI (segun version de procps-ng)"),
83: ("Cuenta lineas, palabras y caracteres/bytes de un archivo de texto.", "SI", "SI", "SI"),
84: ("Muestra la ruta completa del ejecutable que se invocaria al escribir un comando.", "SI", "SI", "SI"),
85: ("Muestra que usuarios estan actualmente conectados al sistema.", "SI", "SI", "SI"),
86: ("Muestra el nombre del usuario con el que se esta ejecutando la sesion actual.", "SI", "SI", "SI"),
87: ("Compara dos archivos linea por linea y muestra las diferencias entre ellos.", "SI", "SI", "SI"),
88: ("Compara dos archivos byte a byte e indica la primera diferencia encontrada.", "SI", "SI", "SI"),
89: ("Compara dos archivos ordenados linea por linea y muestra lineas comunes y exclusivas de cada uno.", "SI", "SI", "SI"),
90: ("Muestra los mensajes del buffer circular del kernel (arranque, hardware, errores).", "SI", "SI", "SI"),
91: ("Crea (formatea) un sistema de archivos sobre un dispositivo o particion.", "SI (interfaz generica sobre herramientas especificas de cada FS)", "NO (FreeBSD usa 'newfs' en lugar de mkfs)", "SI (interfaz generica, ej. mkfs.ext4)"),
92: ("Transfiere datos hacia o desde un servidor usando protocolos como HTTP, HTTPS, FTP, etc.", "SI (incluido desde Solaris 11.1)", "NO (no viene en el sistema base; FreeBSD trae 'fetch'; se instala via pkg)", "SI"),
93: ("Descarga archivos desde la web de forma no interactiva (HTTP, HTTPS, FTP).", "NO (no incluido por defecto; se instala via pkg)", "NO (no incluido en el sistema base; FreeBSD trae 'fetch'; se instala via pkg)", "SI"),
94: ("Muestra informacion sobre la arquitectura de CPU (nucleos, hilos, sockets, cache).", "NO (Solaris usa psrinfo/prtconf/isainfo)", "NO (FreeBSD usa 'sysctl hw.model' y 'sysctl hw.ncpu')", "SI"),
}

wb = openpyxl.load_workbook(PATH)
ws = wb.active

# Use row 3 (the filled 'pwd' example) as the style template
template_cells = {col: copy.copy(ws.cell(row=3, column=col)._style) for col in range(2, 7)}

for row, (desc, sol, fbsd, ol) in DATA.items():
    values = {3: desc, 4: sol, 5: fbsd, 6: ol}
    for col, val in values.items():
        cell = ws.cell(row=row, column=col)
        cell.value = val
        cell._style = copy.copy(template_cells[col])

wb.save(PATH)
print("Workbook updated:", PATH)
print("Rows written:", len(DATA))
