# version 3 mas rapido

import pyautogui
import pyperclip as clipboard
import time
import datetime
import os
from tkinter import messagebox as MessageBox
from tkinter.filedialog import asksaveasfile

def clics_solo():
    """
    Perform clicks a specified number of times with a specified time interval.
    """
    puntos = int(input("\033[32mCuantas veces \033[34m"))
    tiempo = int(input('\033[32mcada cuantos segundos?\033[34m'))
    posiciones =[]
    print("\033[32mPunto para el mouse\033[35m")
    input()
    px, py = pyautogui.position()
    posiciones.append((px, py))
    x = 0
    while x <= puntos:
        x += 1
        pyautogui.moveTo(px, py)
        pyautogui.click()
        time.sleep(tiempo)
        print(progressbar(x, puntos), end='\r')
    MessageBox.showwarning("Finish", 'Finalizado')

def clics_pegar():
    """
    Perform clicks and paste a list of cases.
    """
    print("\033[32mIngrese el listado de Casos:\033[39m") #INGRESO DE URL'S
    list = []  #ARREGLO DE URL
    while True:
        inputs = input()
        if inputs:
            list.append(inputs)
        else:
            break
    print("\033[32mPunto para 'Add Ticket'")
    input()
    px, py = pyautogui.position()
    print("\033[32mPunto para primer Ticket\033[35m")
    input()
    pxd, pyd = pyautogui.position()
    time.sleep(1)
    x = 0
    for caso in list:
        if x == 0:
            pyautogui.moveTo(pxd, pyd)
            pyautogui.click()
            clipboard.copy(caso)
            pyautogui.hotkey('ctrl', 'v')
            time.sleep(0.3)
            x += 1
            continue
        pyautogui.moveTo(px, py, 1)
        pyautogui.click()
        time.sleep(0.3)
        if x == 10:
            MessageBox.showwarning("Finish", "Acepte las condiciones \n(Ojo, primero acepte en FM, luego acepte esta ventana emergente!!!)")
            pyautogui.moveTo(px, py)
            pyautogui.click()
            time.sleep(0.3)
            clipboard.copy(caso)
            pyautogui.hotkey('ctrl', 'v')
            x += 1
            continue
        clipboard.copy(caso)
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(0.3)
        x += 1
        print(progressbar(x, len(list)), end='\r')
    MessageBox.showwarning("Finish", 'Finalizado')

def clics_inf():
    """
    Perform clicks at multiple points for a specified number of times.
    """
    puntos = int(input("\033[35mCuantos puntos? \033[39m"))
    t = input("\033[32mPor defecto (d) o tiempo en segundos (numero)?\033[39m ")
    posiciones =[]
    for x in range(puntos):
        print("\033[36mPunto ", str(x), " para el mouse\033[35m")
        input()
        px, py = pyautogui.position()
        posiciones.append((px, py))
    hora_ini = datetime.datetime.now().replace(microsecond=0)

    for x in range(30):
        for i in range(5):
            for p in posiciones:
                xp, yp = p
                pyautogui.moveTo(xp, yp, 1)
                pyautogui.click()
                tiempo = (60 - puntos) // puntos
                match t:
                    case "d":
                        time.sleep(tiempo)
                    case _:
                        time.sleep(int(t))
            if t == 1:time.sleep(3) 
        hora_actual = datetime.datetime.now().replace(microsecond=0)
        print(progressbar(x, 30), hora_actual - hora_ini, end='\r')
    MessageBox.showwarning("Finish", f'empezo a las:{hora_ini}')

def clics_copiar():
    """
    Copy URLs from a specified number of cases.
    """
    print("\033[35mCuantas URLS desea copiar \033[39m") #INGRESO DE URL'S
    x = int(input())
    list =''
    print("Punto para 'url'")
    input()
    px, py = pyautogui.position()
    print("Punto para 'Dismiss''\033[32m")
    input()
    pxd, pyd = pyautogui.position()
    time.sleep(0.3)
    for caso in range(x):
        pyautogui.moveTo(px, py)
        pyautogui.click()
        time.sleep(0.3)
        pyautogui.hotkey('ctrl', 'a')
        time.sleep(0.3)
        pyautogui.hotkey('ctrl', 'c')
        url = clipboard.paste()
        list = list + f'{url}\n'
        time.sleep(0.3)
        pyautogui.moveTo(pxd, pyd)
        pyautogui.click()
        time.sleep(1)
        print(progressbar(caso, x), end='\r')
    save(list)

def save(list): 
    """
    Save the list of URLs to a file.
    """
    files = [('CSV Files', '*.csv'),  
             ('All Files', '*.*')] 
    file = asksaveasfile(filetypes = files, defaultextension = files)
    file.write(list)
    file.close()

def clean_news():
    """
    Clean news by performing clicks and key presses.
    """
    puntos = int(input("\033[35mCuantos casos? \033[39m"))
    t = 1
    print("\033[35mPunto para el caso 1")
    input()
    px, py = pyautogui.position()
    print("Punto para la flecha")
    input()
    px2, py2 = pyautogui.position()
    x = 0
    while x <= puntos:
        if x == 0:
            pyautogui.moveTo(px, py, t)
            pyautogui.click()
            pyautogui.press('enter')
        else:
            pyautogui.moveTo(px2, py2, t)
            pyautogui.click()
            time.sleep(0.3)
            pyautogui.press('enter')
            time.sleep(0.3)
            pyautogui.press('enter')
            time.sleep(0.3)
            pyautogui.press('space')
        x += 1
        
        print(progressbar(x, puntos), end='\r')

def progressbar(part, total):
    """
    Generate a progress bar based on the current progress and total count.
    """
    frac = part / total
    completed = int(frac * 30)
    miss = 30 - completed
    bar = f"[{'#'* completed}{'-'* miss}]{frac:.1%}"
    return bar

if __name__ == '__main__':
    while True:
        try:
            os.system('cls')
            print("\n\033[49m\033[1m\033[32mClic, version 4\nElija una opción:\n\033[34m1) Solo dar clics n veces\n2) Enviar listado de casos\n3) Varios puntos\n4) Copiar Urls \n5) Clean News \n6) Salir!")
            entrada = int(input("\033[32mOpcion 1 al 6?: \033[39m"))
            match entrada:
                case 1:clics_solo()
                case 2:clics_pegar()
                case 3:clics_inf()
                case 4:clics_copiar()
                case 5:clean_news()
                case 6:
                    print("\n\033[32m\033[45mNospi!\033[39m\033[49m")
                    os.system('cmd exit()')
                    break
                case _:
                    print("Seleccion inválida. Inténtalo nuevamente.")
                    continue
        except ValueError:
            print("Entrada inválida. Inténtalo nuevamente.")
        except KeyboardInterrupt:
            print("\n\nComenzemos de Nuevo!\n")
            continue
