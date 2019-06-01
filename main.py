from numpy import loadtxt
ECG = loadtxt("Grupo03_b.txt",'\t')

FM = 250                                            #Frecuencia de Muestreo = 500 Hz
GAN = 250                                           #Ganancia del amplificador
VREFH = 3.3
VREFL = 0
N = 10

# PICOS DEL ECG
picos = 0
posPicos = []                                       #Posición en Muestras
umbral = (max(ECG)-min(ECG))*0.8+min(ECG)           #umbral = 80% de la señal
i = 2
while i<len(ECG)-2:                                
    if ECG[i]>=ECG[i-1] and ECG[i]>ECG[i-2] and ECG[i]>=ECG[i+1] and ECG[i]>ECG[i+2] and ECG[i]>umbral:
        picos+=1                                    
        posPicos.append(i)                         
        i+=5                                        #En caso exista dos picos (muestras seguidas) en el mismo nivel de cuantización
    i+=1

#print('Numero de picos: ',picos)
#print('Posicion de los picos en muestras: ',posPicos,'\n')
print('#################### RESULTADOS ####################\n')

# FRECUENCIA CARDIACA PROMEDIO
picoIni = posPicos[0]
picoFin = posPicos[len(posPicos)-1]
t = (picoFin - picoIni)/FM                          #Tiempo en seg, del primer al ultimo pico
ciclosTotal = picos - 1
fcp = (ciclosTotal * 60)/t                          #Regla de tres simple
fcp = round(fcp)
print('Frecuencia Cardiaca promedio:', fcp, 'bpm\n')

# FRECUENCIA CARDIACA INSTATANEA
bpmCiclos = []                                      #Lista con las frecuencias cardiacas instantáneas
segCiclos = []                                      #Lista con el tiempo entre ciclos en seg
for i in range(picos-1):
    picoIni = posPicos[i]
    picoFin = posPicos[i+1]
    t = (picoFin - picoIni)/FM
    ciclosTotal = 1
    fcp = (ciclosTotal * 60)/t
    fcp = round(fcp)
    print('Frecuencia Cardiaca Instantanea numero', i+1,': ', fcp, ' bpm')
    segCiclos.append(t)
    bpmCiclos.append(fcp)
print('\n')

#DETECCION DE ARRITMIA, BRADICARDIA O TAQUICARDIA
aux = False
for i in range(len(segCiclos)-1):
    arritmia = abs(segCiclos[i]-segCiclos[i+1])
    if arritmia > 0.040:
        print('Ritmo Cardiaco: Presenta arritmia')
        aux = True
        break
if aux == False:
    for i in range(len(bpmCiclos)):
        if bpmCiclos[i]>100:
            print('Ritmo Cardiaco: Presenta Taquicardia')
            aux = True
            break
        if bpmCiclos[i]<60:
            print('Ritmo Cardiaco: Presenta Bradicardia')
            aux = True
            break
if aux == False:
    print('Ritmo Cardiaco: Normal')
print('\n')

#AMPLITUD QRS
prom = []
for i in range(len(posPicos)-1):                    
    prom.append(posPicos[i+1]-posPicos[i])
promCiclo = round(sum(prom)/len(prom))              #Se halla el promedio de duración del ciclo cardiaco, en muestras
delta = round(promCiclo/2)                          # delta = la mitad de un ciclo cardiaco promedio, en muestras

for i in range(picos):                              #desde los picos se suma y resta el delta, para extraer los datos del
    pos1 = posPicos[i]-delta                        #      ECG, de cada ciclo cardiaco, guardado en la variable "cicloCard"    
    if pos1<0:
        pos1 = 0
    pos2 = posPicos[i]+delta
    if pos2>len(ECG)-1:
        pos2 = len(ECG)-1

    cicloCard = ECG[pos1 : pos2]
    maxLocal = max(cicloCard,default=0)
    minLocal = min(cicloCard,default=0)
    print(maxLocal,minLocal)
    ampQRS = (  (maxLocal - minLocal ) * (VREFH - VREFL) / (2**N) ) / GAN
    print('Amplitud QRS numero', i+1, ' :', "%.2f"%(ampQRS * 1000), 'mV')