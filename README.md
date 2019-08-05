# MicroUtils

1. hay que ajustar en la linea 81 las dimensiones de la pantalla:
   size = w, h = 480, 320
   
2. este script usa dos imagenes que funcionan como layout: bg.png y bga.png
   hay que crear esas imàgenes con las mismas dimensiones de la pantalla,
   las bandas laterales son los botones que la gui muestra detras de la previsualización
   mientras está en modo de espera (bg.png) y cuando está ocupado (bga.png)

3. el script muestra al inicio la previsualización con
      -una franja/boton amarillo para hacer un timelapse
      -un boton/franja verde para hacer un video
   en ambos casos, tras comenzar el video o timelapse, los botones cambian a rojo
   que significa paro. tras detener cualquiera de estas tareas la gui vuelve al modo inicio

4. crea un par de directorios /home/pi/timelapses/ y /home/pi/videos/ donde guarda lo registrado

# Para hacer autoejecutable al inicio:

a. crear un archivo /home/pi/autostart.sh con el contenido siguiente:
#!/bin/bash

PATH=/usr/local/bin:$PATH

cd /home/pi/W/python/handicam/

python hcam.py &

b. en la penultima linea cambiar a la ruta donde se encuentra el script hcam.py

c. hacerlo autoejecutable con:

chmod +x autostart.sh

d. editar el archivo sudo /home/pi/.config/lxsession/LXDE-pi/autostart con:

sudo nano /home/pi/.config/lxsession/LXDE-pi/autostart

e. añadir al final la línea:

@/bin/bash /home/pi/autostart.sh

f. reiniciar
