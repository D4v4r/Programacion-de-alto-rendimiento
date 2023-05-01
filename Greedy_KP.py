import random
import time

def mochila_voraz(objetos, peso_max):
    objetos_ordenados = sorted(objetos, key=lambda x: x[1]/x[0], reverse=True)
    selec_objetos = []
    total_valor = 0
    total_peso = 0
    for objeto in objetos_ordenados:
        if total_peso + objeto[0] <= peso_max:
            selec_objetos.append(objeto[2])
            total_valor += objeto[1]
            total_peso += objeto[0]
    return sorted(selec_objetos), total_valor, total_peso

# Ejemplo de uso
objetos = []
for i in range(1000000):
    peso = random.randint(1, 51)
    valor = random.randint(1, 251)
    nombre = "objeto" + str(i+1)
    objetos.append((peso, valor, nombre))
peso_max = 80
t1=time.time()
selec_objetos, total_valor, total_peso = mochila_voraz(objetos, peso_max)
t2=time.time()

print("Objetos seleccionados:", selec_objetos)
print("Valor total:", total_valor)
print("Peso total:", total_peso)
print("Tiempo de ejecucion: ", t2-t1, "segundos")
