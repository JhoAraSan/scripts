"""
Este script permite mezclar imágenes a partir de una URL y una imagen local.

Requisitos:
- Para instalar las librerías necesarias en Python Fedora 36, ejecuta el siguiente comando:
    $ sudo dnf install opencv opencv-contrib opencv-doc python3-opencv python3-matplotlib python3-numpy

Funcionalidad:
- El usuario debe ingresar una dirección web.
- El script carga una imagen local llamada 'url.png' y otra imagen local llamada 'im.png'.
- Luego, agrega la dirección web ingresada a la imagen 'url.png' utilizando la función cv2.putText().
- A continuación, redimensiona las imágenes 'url.png' y 'im.png' para que tengan el mismo ancho mínimo.
- Finalmente, concatena verticalmente las imágenes redimensionadas y guarda el resultado en un archivo llamado 'resized.jpg'.

Nota: Los comentarios en el código que están actualmente desactivados (comentados con '#') son opciones adicionales que puedes utilizar para visualizar el resultado.

"""

import cv2

url_1 = input('Ingrese la dirección web:')
imgUrl = cv2.imread('url.png')
img = cv2.imread('im.png')

cv2.putText(imgUrl,url_1, (174,24), cv2.FONT_HERSHEY_PLAIN, 1, (255,255,255), 1)


def vconcat_resize(img_list, interpolation=cv2.INTER_CUBIC):
        w_min = min(img.shape[1] for img in img_list) #busca el ancho min de las imagenes

        im_list_resize = [cv2.resize(img,(w_min, int(img.shape[0] * w_min / img.shape[1])), interpolation=interpolation) for img in img_list]

        return cv2.vconcat(im_list_resize)


img_v_resize = vconcat_resize([imgUrl, img])

cv2.imwrite('resized.jpg', img_v_resize)
#cv2.waitKey() #Es la forma en que se puede ver el resultado
#cv2.destroyAllWindows()