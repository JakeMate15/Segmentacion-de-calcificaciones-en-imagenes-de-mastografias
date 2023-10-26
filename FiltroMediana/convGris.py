import cv2

imagen = cv2.imread('imgN.gif')

gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)

cv2.imwrite('gris.gif', gris)