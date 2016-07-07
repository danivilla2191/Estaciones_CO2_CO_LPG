import Adafruit_DHT
from time import sleep
from datetime import datetime,timedelta

#Se intenta medir la humedad y la temperatura una vez por minuto
#el script se detiene directo en el servicio que lo controla
'''No hay mucho control sobre la toma de muestras del sensor de temperatura y
   humedad debido a las veces que se intenta obtener las lecturas del sensor,
   para ajustar esto debe modificarse los scripts que se enccuentra en la 
   carpeta sensor de humedad, en donde estan los modulos en C utilizados,
   que controlan la adquisicion de datos del sensor. Debido a que la humedad 
   y la temperatura en este estudio no representan factores de gran 
   relevancia no se le dio mucho enfasis a la frecuencia de muestreo'''

filename = "/root/datos/humedad/{}"
tiempo_de_muestreo = timedelta(minutes=5)  #en minutos
humedad,temperatura = [],[]     #contenedores

while True:
  fecha = datetime.now()
  fecha1 = fecha
  while (fecha1 - fecha) < tiempo_de_muestreo:
   fecha1 = datetime.now()
   humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, "P8_11")
   if humidity is not None and temperature is not None:
     humedad.append(humidity)
     temperatura.append(temperature)
   #por si se desea hacer algo en caso de que la medida falle
   if humidity is None and temperature is None: pass     
   sleep(1)
  
  #Guardando Datos
  f = open(filename.format(fecha.date()),"a")
  f.write("{0},{1},{2} \n".format(fecha1.isoformat().split('.')[0],
                                  str(sum(humedad)/len(humedad)),
                                  str(sum(temperatura)/len(temperatura))))
  f.close()

  #vaciando contenedores de datos
  del humedad[:]
  del temperatura[:]

  sleep(0.01)
                              
 
    
  
