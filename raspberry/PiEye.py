from picamera.array import PiRGBArray
from picamera import PiCamera
import numpy
import time
import cv2
import sys
#import select
import platform #pour savoir sur quel processeur/système s'exécute le programme
import subprocess #pour savoir si la caméra est présente

class PiEye:
        """ classe permettant de gérer la caméra du pi afin de détecter les mouvements des
                spectateurs
                version 2d : transformation en classe.
        """
        def __init__(self):
                # initialisation de la camera native du raspberry
                self.camera = PiCamera()
                self.rawCapture = PiRGBArray(self.camera)
                self.firstFrame = None
                self.count = 0 # nombre de vues sauvegardées depuis l'initialisation (option)
                self.presence_cam = 0 # pour détection camera
                self.detect_cameraPI() # pour détection camera
                                
        
        def redim(self,tab_image,largeur=100):
        # redimensionne un numpy.array en respectant le ratio largeur x hauteur
                ratio = largeur / tab_image.shape[1]
                dim = (largeur, int(tab_image.shape[0]*ratio))
                tab_redim = cv2.resize(tab_image, dim, interpolation = cv2.INTER_AREA)
                return tab_redim

        def detect_cameraPI(self):
                if platform.machine().startswith('arm'):
                        c = subprocess.check_output(["vcgencmd","get_camera"])
                        int(c.strip()[-1]) #-- Removes the final CR character and gets only the "0" or "1" from detected status
                        if (c):
                            print("Camera detected")
                            self.presence_cam = 1
                            return True
                        else:
                            print("not detected")
                            self.presence_cam = 0
                            return False
                else:
                        print("le programme doit fonctionner sur un raspberry !")
                        self.presence_cam = 0


        def voir(self):
                if (self.presence_cam):
                        # capture d'une image
                        self.rawCapture = PiRGBArray(self.camera)
                        self.camera.capture(self.rawCapture, format="bgr")
                        frame = self.rawCapture.array
                        # redimensionnement de l'image
                        frame = self.redim(tab_image=frame, largeur=500)
                        # conversion en nuances de gris
                        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                        gray = cv2.GaussianBlur(gray, (21, 21), 0)
                        # si première image : initialisation et on quitte la fonction
                        if self.firstFrame is None:
                                self.firstFrame = gray
                                return 0.0
                        # Différence absolue entre l'image actuelle et la précédente
                        frameDelta = cv2.absdiff(self.firstFrame, gray)
                        # seuillage
                        thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
                        # dilatation de l'image pour combler les trous
                        thresh = cv2.dilate(thresh, None, iterations=2)
                        # calcul et affichage de la couleur moyenne de l'image
                        moyenne_par_col = numpy.average(thresh, axis = 0)
                        moyenne=numpy.average(moyenne_par_col, axis = 0)
                        # print("moyenne : %.2f" % float(moyenne))
                        mouvement =100.0 * float(moyenne/255.0)
                        
                        # mémorisation de l'image pour l'appel suivant 
                        self.firstFrame = gray
                        ## enregistrement des images seuillées avec affichage de la moyenne 
                        #thresh_RGB = cv2.cvtColor(thresh, cv2.COLOR_GRAY2BGR) # pour debug
                        #cv2.putText(thresh_RGB, "moyenne: %.2f" % float(moyenne), (10, 20),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2) #pour debug
                        #cv2.imwrite("frames/Thresh%03d.jpg" % self.count, thresh_RGB) # pour debug
                        #self.count += 1 # pour debug
                else:
                        print("ATTENTION : Caméra non insérée")

                return mouvement

                        

                
                                

if __name__ == "__main__":
        Oeil=PiEye()
        while 1:
                print("le mouvement devant la caméra vaut :{}".format(Oeil.voir()))
                time.sleep(1)
                # sortie de la boucle en cas d'appui sur Enter
                #if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
                        #line=input()
                        #break
