import pp
import random
import time
import multiprocessing

num_procs = multiprocessing.cpu_count()
job_server = pp.Server(ncpus=num_procs)
print("Procesadores:", num_procs)
#Se define la funcion con el algortimo Cooperation Greedy Monkey Algorithm
def CGM(peso_max, pesos, valores):
    n = len(pesos)
    objetos = list(range(n))
    #Aquí se usa el enfoque greedy
    objetos.sort(key=lambda i: -valores[i] / pesos[i])

    peso = 0
    valor = 0
    selec_objetos = []
    for i in objetos:
        if peso + pesos[i] <= peso_max:
            selec_objetos.append(i)
            peso += pesos[i]
            valor += valores[i]

    return selec_objetos, peso, valor

def sol_KP(peso_max, pesos, valores, num_procs):
    job_server = pp.Server(num_procs)

    n = len(pesos)
    particiones = n // num_procs

    jobs = []
    for i in range(num_procs):
        start = i * particiones
        end = (i + 1) * particiones if i < num_procs - 1 else n
        sub_pesos = pesos[start:end]
        sub_valores = valores[start:end]

        job = job_server.submit(CGM, (peso_max, sub_pesos, sub_valores))
        jobs.append(job)

    results = [job() for job in jobs]

    job_server.destroy()

    selec_objetos, peso, valor = max(results, key=lambda result: result[2])
    return sorted(selec_objetos), peso, valor
#Se inicializan los parametros del problema 
if __name__ == '__main__':
    random.seed(123)
    peso_max = 50
    #se usa random.choices puesto que es mas eficiente que randint
    pesos = random.choices(range(1, 51), k=10000000)
    valores = random.choices(range(1, 251), k=10000000)
    print("Cantidad de elementos", len(pesos))

    num_procs = 16

    t1 = time.time()
    selec_objetos, peso, valor = sol_KP(peso_max, pesos, valores, num_procs)
    t2 = time.time()

    print(f'Selected objetos: {selec_objetos}')
    print(f'Total peso: {peso}')
    print(f'Total valor: {valor}')
    print(f'Tiempo de ejecucion: {t2 - t1} segundos')
