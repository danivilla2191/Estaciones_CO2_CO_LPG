import Adafruit_BBIO.GPIO as GPIO
from time import sleep
from datetime import datetime,timedelta
from subprocess import call

GPIO.setup("P9_11", GPIO.IN)
GPIO.setup("P9_13", GPIO.OUT)
GPIO.add_event_detect("P9_11", GPIO.FALLING)

#Intervalo de Medicion
Int = timedelta(minutes=20)
Vehiculos = "/root/datos/Vehiculos/{0}"
Inicio = datetime.now()
Arch = open(Vehiculos.format(Inicio.date()),"a")
Arch.close()
conteo = 0
flag = 1

#funcion de prueba de conteo para verificar el funcionamiento del switch
def prueba(conteo):
  ''' Se crea un archivo para ver instantaneamente el conteo que se lleva a
      cabo'''
  f = open("/root/datos/Vehiculos/prueba.txt","a")
  f.write(str(conteo) + "\n")
  f.close
  
def alarma():
  conteo = 30  #segundos que va a demorar la alarma aproximadamente
  while True:
    GPIO.output("P9_13", GPIO.HIGH)
    sleep(0.5)  
    GPIO.output("P9_13", GPIO.LOW)
    sleep(0.5)
    conteo-=1
    if conteo == 0:
        break
    
while flag:
  Inicio = datetime.now()
  while True:
    Hora = datetime.now()
    if GPIO.event_detected("P9_11"):
      conteo += 1
      #prueba(conteo)
    if Hora >= (Inicio + Int):
      print "Hola"
      Hora = datetime.now()
      Arch = open(Vehiculos.format(Inicio.date()),"a")
      Arch.write("{0},{1},{2} \n".format(Inicio.isoformat(),Hora.isoformat(),
                                      conteo))
      Arch.close()
      
      #Extermina la medicion
      x = call("systemctl stop sensor.service",shell=True) #para determinar si se murio el proceso
      z = call("systemctl stop humedad.service",shell=True)
      cuenta = 0
      while (x != 0) and (z != 0):
       cuenta += 1
       #por si no se cierra
       if x != 0:
         x = call("systemctl stop sensor.service",shell=True)
       if z != 0:
         z = call("systemctl stop humedad.service",shell=True)
       elif cuenta == 10:    #10 intentos
         break #para romper el ciclo que extermina los servicios
       sleep(1)
      cuenta = 0
      break      #Para romper el loop de medicion
    #print conteo
    sleep(0.01)
  '''Alarma visual con led, avisa que se va a entrar en el loop de espera
     da el tiempo para que se limpeen los pines utilizados'''
  alarma()
  sleep(2)
  GPIO.cleanup() 
  sleep(15)
  #call("python /root/scripts/espera.py > /dev/null 2>&1&",shell=True)
  call("systemctl start espera.service",shell=True)
  sleep(1)
  break  #para romper el loop principal
  sleep(0.01)



