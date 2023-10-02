def primo(n):
    p=[]
    x=2
    while x<=n:
        p.append(x)
        x+=1
    sn=int(n**0.5)
    for i in range(2,sn+1):
        for j in range(2,n//i+1):
            if i*j in p:
                p.remove(i*j)
    return p

def factorizar(a):
    a=int(a)
    factor=[]
    num=0
    ip=iter(primo(a))
    while a != 1:
        xp=next(ip)
        if xp<=a:
            while a % xp == 0:
                a=a//xp
                factor.append(xp)
        else:
            break
    return factor

def unir(listas):
    resultado = {}
    # Recorrer cada lista en listas
    for numeros in listas:
        # Crear un contador para esta lista
        contador = {}
        for numero in numeros:
            contador[numero] = contador.get(numero, 0) + 1

        # Actualizar el resultado
        for numero, cantidad in contador.items():
            if numero not in resultado or cantidad > resultado[numero]:
                resultado[numero] = cantidad

    # Crear la lista final basada en el resultado
    resultado_lista = sorted([numero for numero, cantidad in resultado.items() for _ in range(cantidad)])
    return resultado_lista

def interseccion(listas):
    resultado=[]
    # Contabilizar los factores primos en todas las listas
    for elemento in set(listas[0]):
        cantidad_comun = min(lista.count(elemento) for lista in listas)
        resultado.extend([elemento] * cantidad_comun)
    return resultado

def mcdym(a):
    if isinstance(a,list):
        a=sorted([int(x) for x in a])
        lf,lfc,md,mm=[],[],1,1
        msm=''
        for i in a:
            lf.append(factorizar(i))
            msm+=f'Factores de {i} son: {factorizar(i)}\n'
        lfc=interseccion(lf)
        [md:=md*n for n in lfc]
        msm+=f'Los factores del MCD son: {lfc}, MCD={md}\n'
        lfu=unir(lf)
        [mm:=mm*n for n in lfu]
        msm+=f'Los factores del mcm son: {lfu}, mcm={mm}\n'
        print()
    else:
        msm='Error'
    return msm

def prueba():
    listas = [[2, 3, 3, 4, 5], [3, 3, 4, 4, 5, 6], [1, 2, 3, 3, 4, 4, 5]]

    # Inicializar una lista para almacenar los elementos comunes y sus cantidades
    resultado = []

    # Contar la cantidad de veces que se repiten los elementos en todas las listas
    for elemento in set(listas[0]):
        cantidad_comun = min(lista.count(elemento) for lista in listas)
        resultado.extend([elemento] * cantidad_comun)

    # Imprimir el resultado
    print(resultado)

if __name__ == '__main__':
    while True:
        try:
            entrada = int(input("Que desea hacer?: \n1) Numeros primos hasta n \n2) Factores de n \n3) mcm y mcd \n4) Salir \nElija: "))
            match entrada:
                case 1: 
                    a=int(input("Escriba el numero: "))
                    print(primo(a))
                case 2:
                    a=int(input("Escriba el numero: "))
                    print(factorizar(a))
                case 3:
                    a=input("Escriba los numeros separados por ',': ")
                    nums=a.split(',')
                    print(mcdym(nums))
                case 4:
                    print("Vemos!!!\nWii\nWii\nWii\nWii")
                    quit()
                case 5:
                    prueba()
                case _:
                    print("Seleccion inválida. Inténtalo nuevamente.")
                    continue
        except ValueError:
            print("Entrada inválida. Inténtalo nuevamente.")
        except KeyboardInterrupt:
            print("\n\nComenzemos de Nuevo!\n")
            continue


