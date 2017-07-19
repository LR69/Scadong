# Programme PiEye v2.c
from picamera.array import PiRGBArray
from picamera import PiCamera
import numpy
import pygame.mixer
import time
import cv2
import sys
import select

def redim(tab_image,largeur=100):
# redimensionne un numpy.array en respectant le ratio largeur x hauteur
	ratio = largeur / tab_image.shape[1]
	dim = (largeur, int(tab_image.shape[0]*ratio))
	tab_redim = cv2.resize(tab_image, dim, interpolation = cv2.INTER_AREA)
	return tab_redim

# initialisation de la camera native du raspberry
camera = PiCamera()
rawCapture = PiRGBArray(camera)

# initialisation d'un son
pygame.mixer.init(48000, -16, 1, 1024)  #initialisation du lecteur
audio1 = pygame.mixer.Sound("Nick_Waterhouse.wav")      # fichier à jouer
audio1.set_volume(0.5) # on place le volume à une valeur médiane
audio1.play() # on lance la lecture
# initialisation de la première image
firstFrame = None

print("Acquisition en cours. Appuyer sur la touche Enter pour quitter")
# acquisition continue des images de la caméra
count = 0
while True:
	time.sleep(0.1)
	# capture d'une image
	rawCapture = PiRGBArray(camera)
	camera.capture(rawCapture, format="bgr")
	frame = rawCapture.array
	# redimensionnement de l'image
	frame = redim(tab_image=frame, largeur=500)
	# conversion en nuances de gris
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	gray = cv2.GaussianBlur(gray, (21, 21), 0)
	# si première image : initialisation et on quitte la boucle
	if firstFrame is None:
		firstFrame = gray
		continue
	# Différence absolue entre l'image actuelle et la précédente
	frameDelta = cv2.absdiff(firstFrame, gray)
	# seuillage
	thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
	# dilatation de l'image pour combler les trous
	thresh = cv2.dilate(thresh, None, iterations=2)
	# calcul et affichage de la couleur moyenne de l'image
	moyenne_par_col = numpy.average(thresh, axis = 0)
	moyenne=numpy.average(moyenne_par_col, axis = 0)
	print("moyenne : %.2f" % float(moyenne))
	volume = float(moyenne/255.0)
	audio1.set_volume(volume)
	
	## enregistrement des images seuillées avec affichage de la moyenne
	#thresh_RGB = cv2.cvtColor(thresh, cv2.COLOR_GRAY2BGR)
	#cv2.putText(thresh_RGB, "moyenne: %.2f" % float(moyenne), (10, 20),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
	#cv2.imwrite("frames/Thresh%03d.jpg" % count, thresh_RGB)
	
	count += 1

	# sortie de la boucle en cas d'appui sur Enter
	if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
		line=input()
		break
