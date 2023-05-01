import random
import time
def mochila_pd(objetos, peso_max):
    
    n = len(objetos)
    # Crear tabla para almacenar los valores máximos que pueden ser obtenidos por cada peso 
    # y numero de objetos
    pd = [[0 for j in range(peso_max+1)] for i in range(n+1)]
    
    # Llenado de la tabla con programacion dinamica
    for i in range(1, n+1):
        for j in range(1, peso_max+1):
            peso, valor, nombre = objetos[i-1]
            # Condicional para incluir o no el artículo
            if peso <= j:
                pd[i][j] = max(pd[i-1][j], valor + pd[i-1][j-peso])
            
            else:
                pd[i][j] = pd[i-1][j]
    
    # Se busca en la tabla los nombres de los objetos seleccionados
    selec_objetos = []
    i = n
    j = peso_max
    while i > 0 and j > 0:
        peso, valor, nombre = objetos[i-1]
        if pd[i][j] != pd[i-1][j]:
            selec_objetos.append(nombre)
            j -= peso
        i -= 1
    
    return sorted(selec_objetos), pd[n][peso_max], sum([objetos[i-1][0] for i in range(1, n+1) if objetos[i-1][2] in selec_objetos])
#Con este ejemplo de abajo, se ve que el algoritmo greedy no siempre da la solución exacta
#objetos = [(10, 60, 'objeto1'), (20, 100, 'objeto2'), (30, 120, 'objeto3'),(10,50,'objeto4'),(25,80,'objeto5'),(30,150, 'objeto6'),(20, 120,'objeto7'),(50,200,'objeto8')]
objetos = []
for i in range(100000000):
    peso = random.randint(1, 51)
    valor = random.randint(1, 251)
    nombre = "objeto" + str(i+1)
    objetos.append((peso, valor, nombre))
peso_max = 80
t1=time.time()
selec_objetos, total_valor, total_peso = mochila_pd(objetos, peso_max)
t2=time.time()
print("Objetos seleccionados:", selec_objetos)
print("Valor total:", total_valor)
print("Peso total:",total_peso)
print("Tiempe de ejecucion", t2-t1, "segundos")
