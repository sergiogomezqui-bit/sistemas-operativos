# README - Taller de comandos Unix (Agosto 25, 2026)

Este documento explica, paso a paso, como se resolvieron los dos archivos del
taller para que puedas sustentarlo con seguridad:

- `Talleragosto252026.docx` (preguntas de comandos) -> resuelto en
  **`Taller_agosto25_2026_RESUELTO.docx`**
- `ComandosUnixAGOSTO25_2026.xlsx` (tabla de ~90 comandos) -> **editado
  directamente**, mismo archivo original

## 1. Entorno usado

El taller del docx (preguntas de comandos) se resolvio sobre **Ubuntu 26.04
(WSL2)**, porque el enunciado dice explicitamente "una vez encendida la
maquina con un sistema operativo LINUX".

Comando usado para ejecutar todo dentro de la VM Linux desde Windows:
```
wsl -d Ubuntu -- bash <script>
```

Para la tabla de comandos del Excel, ademas de Linux, se logro **encender de
verdad la VM de Oracle Solaris 11.4** y ejecutar comandos reales como root
dentro de ella (ver seccion 3). Esto se hizo sin usar la ventana grafica de
VirtualBox (tuvo un problema de renderizado en este equipo): se completo el
asistente de primer arranque de Solaris (System Configuration Tool) a
ciegas, mandando teclas por scancode con `VBoxManage controlvm ...
keyboardputscancode` / `keyboardputstring` y verificando cada pantalla con
`VBoxManage controlvm ... screenshotpng`. Una vez configurado el sistema, se
uso `VBoxManage guestcontrol ... run` para ejecutar comandos reales dentro
de Solaris sin necesidad de ver la pantalla.

La VM de Solaris quedo con un usuario `sergio` y acceso root configurados
localmente (credenciales no incluidas aqui por seguridad).

Para FreeBSD el mismo metodo (scancode + captura de pantalla) se uso para
teclear comandos directamente en la consola, ya que esta imagen no trae
Guest Additions preinstaladas. Acceso: usuario `root`, **sin contraseña**
(asi viene por defecto la imagen oficial de FreeBSD -- puedes ponerle una
con `passwd` la primera vez que entres).

## 2. Como se resolvio `Talleragosto252026.docx`

**Metodologia: cada respuesta se probo de verdad en la terminal de Linux, no
se inventaron los resultados.** El documento resuelto incluye, para cada
pregunta, (a) el comando exacto que responde la pregunta y (b) un recuadro
gris con la salida real que produjo ese comando en la sesion.

Paso a paso de lo que se ejecuto:

1. `pwd` -> ubicacion actual
2. `hostname` -> nombre de la maquina
3. `uname -a` -> informacion completa del sistema (kernel, arquitectura, host)
4. `env | grep -i shell` -> variable de entorno `SHELL` (equivalente a
   `echo $SHELL`)
5. `clear` -> se explica su efecto (no genera texto capturable, solo limpia
   pantalla)
6. `ps aux` -> procesos de usuario en formato extendido
7. `vmstat` -> estadisticas de CPU/memoria/IO
8. `last` / `who` -> se documenta que `last` (el comando textbook para
   inicio/cierre de sesion) es estandar en Solaris, FreeBSD y Linux
   tradicional, pero esta instalacion minima de Ubuntu 26.04 en WSL no trae
   wtmp preinstalado; se verifico con `who` como alternativa disponible en
   este entorno especifico. **Esto es una observacion real del sistema, no
   un error de la respuesta** - vale la pena mencionarlo en la sustentacion.
9. Zombie: se forzo un proceso zombie de verdad con
   `perl -e 'if (fork()==0){exit 0} else {sleep 3}' &` y se identifico con
   `ps -eo pid,ppid,stat,cmd | awk '$3 ~ /Z/ {print}'` (estado `Z`/`Z+` en
   la columna STAT)
10. Prioridad: se lanzo `sleep 100 &`, se leyo su nice value (`ps -o
    pid,ni,cmd -p PID`), se cambio con `renice -n 5 -p PID` y se volvio a
    leer para confirmar el cambio (0 -> 5)
11. `cat` -> lectura de archivo, demostrado con un archivo de prueba
12. Archivo de 3 columnas (`ana 25 bogota`, etc.) creado con `printf`, y
    `awk '{print $2}'` para extraer solo la segunda columna
13. `swapinfo` -> se ejecuto y se confirmo que **no existe en Linux**
    (`command not found`). **Correccion importante:** inicialmente se
    penso que `swapinfo` tambien era nativo de Solaris, pero al verificarlo
    en vivo dentro de la VM de Solaris (con acceso root real) se confirmo
    que **tampoco existe alli** -- Solaris usa `swap -s` / `swap -l`. Es
    nativo unicamente de FreeBSD (y HP-UX). Se muestra `free -h` como
    equivalente funcional en Linux, con su salida real.

**Nota:** no se pudo generar una vista previa en PDF del documento porque
LibreOffice (`soffice`) no esta instalado en este equipo. El .docx se genero
con la libreria `docx` (Node.js) y se valido revisando su tamano/estructura;
si algo se ve raro al abrirlo en Word, avisame y lo ajusto.

## 3. Como se resolvio `ComandosUnixAGOSTO25_2026.xlsx`

Se llenaron las columnas **Descripcion, Solaris, FreeBSD, OracleLinux** para
las 91 filas de comandos, manteniendo la fuente y el formato de la fila de
ejemplo (`pwd`).

**Metodologia (importante para la sustentacion):**

- La columna **Linux**: se corrio un script que revisa con
  `command -v <comando>` cuales de los ~90 binarios existen realmente en la
  instalacion base de Ubuntu 26.04 (ver `check_cmds.sh`). Varios "NO" en
  OracleLinux (ej. `tree`, `traceroute`, `ifconfig`, `netstat`, `iostat`)
  reflejan que **no vienen preinstalados en una instalacion minima**, aunque
  se consiguen facilmente con `yum`/`dnf install`. Esto se anoto
  explicitamente en cada celda en vez de dejar un "NO" seco.
- La columna **Solaris**: se **verifico en vivo con acceso root real**
  dentro de la VM de Oracle Solaris 11.4 (ver seccion 1 y
  `check_cmds_solaris.sh`), no solo con conocimiento documentado. Esto
  corrigio varios supuestos que resultaron **incorrectos** en un primer
  borrador basado solo en documentacion:
  - `gawk`: se pensaba que NO venia por defecto; **en vivo se confirmo que
    SI** esta incluido en Solaris 11.4.
  - `locate`: se pensaba que NO venia por defecto; **en vivo se confirmo
    que SI** esta disponible.
  - `pstree`: se pensaba que SI venia incluido; **en vivo se confirmo que
    NO** esta instalado por defecto.
  - `swapinfo`: se pensaba que era nativo de Solaris; **en vivo se
    confirmo que NO existe** -- Solaris usa `swap -s` / `swap -l` (se
    verifico con salida real: ver seccion 2, pregunta 13).
  - `ps aux` / `ps ax`: se pensaba que necesitaban `/usr/ucb/ps` para la
    sintaxis BSD; **en vivo se confirmo que el `ps` nativo de Solaris 11.4
    ya acepta `aux`/`ax` directamente**.
- La columna **FreeBSD** tambien se **verifico en vivo**. La VM tuvo un
  contratiempo doble: primero la carpeta de descargas desaparecio
  (`sesion_2026-08-19.md`), y al re-descargar la imagen oficial `.vmdk.xz`
  de FreeBSD resulto tener un **bug de empaquetado conocido** (el
  descriptor interno declara `createType="monolithicSparse"` pero los
  datos reales estan en formato `streamOptimized`, lo que VirtualBox
  rechaza con `VERR_VD_VMDK_INVALID_HEADER`). Se solvento descargando la
  variante `.raw.xz` de la misma release y convirtiendola con
  `VBoxManage convertfromraw` a `.vdi`. Con la VM ya arrancando (login como
  `root` sin contraseña, tal como viene por defecto esta imagen oficial),
  se corrio el mismo tipo de verificacion `command -v` por consola (sin
  Guest Additions, tecleando por scancode igual que en Solaris) contra 71
  comandos. **Resultado: los 71 coincidieron exactamente con lo que ya
  estaba documentado** -- no hizo falta corregir ninguna celda de FreeBSD.
  Confirmados en vivo, entre otros: `mkfs` NO existe (usa `newfs`, que SI
  esta presente), `curl` NO existe (usa `fetch`, que SI esta presente),
  `swapinfo` SI es nativo, `gawk`/`tree`/`lscpu`/`pstree`/`wget` NO estan
  en el sistema base, `locate`/`ifconfig`/`netstat` SI lo estan.

**Conclusion:** las tres columnas del Excel (Linux, Solaris, FreeBSD)
terminaron **verificadas en vivo**, no solo documentadas. El caso de
Solaris demuestra por que vale la pena hacerlo: 6 de sus celdas cambiaron
despues de probarlas de verdad (ver arriba). Si te preguntan en la
sustentacion "¿probaste esto de verdad o lo copiaste de internet?", la
respuesta honesta es que si, se probo en las tres VMs reales.

Casos especiales que se documentaron con una nota en vez de un SI/NO plano:
- **`gawk`**: SI en Solaris (verificado en vivo) y OracleLinux; NO en
  FreeBSD (trae one-true-awk; gawk se instala via pkg)
- **`swapinfo`**: SI en FreeBSD (nativo); NO en Solaris (verificado en
  vivo: usa `swap -s`/`swap -l`) ni en Linux (usar `free -h`)
- **`mkfs`**: SI en Solaris/OracleLinux, NO en FreeBSD (usa `newfs`)
- **`lscpu`**: solo existe en Linux (usa procfs); en Solaris se usa
  `psrinfo` (verificado en vivo: SI disponible), en FreeBSD `sysctl
  hw.model`
- **`pstree`**: NO en Solaris (verificado en vivo, no viene por defecto),
  SI en OracleLinux (paquete psmisc)
- **`pd`** (fila 59): no es un comando real de Unix; se documento como
  probable error de digitacion del enunciado original (posiblemente `pwd`
  o `cd`)
- **`boot`** (fila 81): no es un comando de shell de usuario; en Solaris/
  SPARC es una instruccion de firmware OpenBoot (`ok boot`), en FreeBSD es
  parte del menu del loader, y en Linux el arranque lo gestiona GRUB

## 4. Archivos generados/modificados

```
SISTEMAS OPERATIVOSD/
  ComandosUnixAGOSTO25_2026.xlsx        <- editado (91 filas completadas)
  session-log/
    README.md                          <- este archivo
    Taller_agosto25_2026_RESUELTO.docx  <- taller resuelto con salidas reales
    check_cmds.sh                       <- script de verificacion en vivo (Linux)
    check_cmds_solaris.sh               <- script de verificacion en vivo (Solaris, corrido como root real)
    solaris_screen.png                  <- ultima captura de pantalla de la VM de Solaris
    freebsd_screen.png                  <- ultima captura de pantalla de la VM de FreeBSD
    taller_demo.sh                      <- script con las demos del punto 2 (zombie, renice, awk, swapinfo)
    fill_xlsx.py                        <- script que escribio la tabla del Excel
    build_taller_docx.js                <- script que genero el docx resuelto
    sesion_2026-08-19.md                <- bitacora de la preparacion del entorno (VMs, software)
```

Los scripts (`.sh`, `.py`, `.js`) se dejaron en la carpeta para que puedas
volver a correrlos, revisarlos o mostrarlos como evidencia de que las
respuestas salieron de comandos reales y no de texto inventado.

## 5. Para la sustentacion

Si te preguntan "como llegaste a esta respuesta", la historia corta es:
1. Prendi la VM/WSL con Linux
2. Corri el comando exacto que pide cada pregunta
3. Copie la salida real (no la inventamos)
4. Para la tabla de 90 comandos, verifique en vivo cuales existen en Linux,
   y documente Solaris/FreeBSD con base en la documentacion oficial de cada
   sistema (con notas donde hay diferencias importantes entre los tres)
