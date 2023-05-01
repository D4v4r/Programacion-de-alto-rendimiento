import pp
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

def mochila_pd_par(objetos, peso_max, num_procs):
    job_server = pp.Server(num_procs)

    n = len(objetos)
    particiones = n // num_procs

    jobs = []
    for i in range(num_procs):
        start = i * particiones
        end = (i + 1) * particiones if i < num_procs - 1 else n
        sub_objetos = objetos[start:end]

        job = job_server.submit(mochila_pd, (sub_objetos, peso_max))
        jobs.append(job)

    results = [job() for job in jobs]

    job_server.destroy()

    selec_objetos, total_valor, total_peso = max(results, key=lambda result: result[1])
    return selec_objetos, total_valor, total_peso

objetos = []
for i in range(100000000):
    peso = random.choices(range(1, 51), k=10000000)
    valor = random.choices(range(1, 251), k=10000000)
    nombre = "objeto" + str(i+1)
    objetos.append((peso, valor, nombre))
peso_max = 80
num_procs = 16

t1 = time.time()
selec_objetos, total_valor, total_peso = mochila_pd_par(objetos, peso_max, num_procs)
t2 = time.time()

print("Objetos seleccionados:", selec_objetos)
print("Valor total:", total_valor)
print("Peso total:", total_peso)
print("Tiempo de ejecucion:", t2-t1, "segundos")
