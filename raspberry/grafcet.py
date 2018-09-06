""" Module grafcet_simple, 
version 4 : modifié le 29/10/17 par LR : ajout de l'onglet transition
version 5 : version multiprocessing : ajout d'une queue pour transmettre les numéros d'étapes, et les recettes associées
version 6 : ajout de PiEye, et de toutes les autres conditions figurant dans le fichier interface_exel_15 (à l'exception de "nombre de séquences mini"
version 7 : utilisation des IO du RPi au lieu des touches du clavier. 
version 8 : suppression de l'écoute clavier pour la version rpi 
version 9 : prise en compte de la possibilité de faire jouer plusieurs grafcets simultanément

"""

import time
import os
import Scadong_utils
#import PiEye
import RPi.GPIO as IO  #calling for header file which helps in using GPIOs of PI


# déclaration de constantes (adressages E/S)

Bouton_A = 16 #GPIO16 bouton 1
Bouton_B = 20 #GPIO20 bouton 2
Bouton_C = 21 #GPIO21 bouton 3

WahWah_SeuilHH = 13 #GPIO13 bouton 9
WahWah_SeuilH = 19 #GPIO19 bouton 8
WahWah_SeuilL = 26 #GPIO26 bouton 7

Piezo_SeuilHH = 17 #GPIO17 bouton 6
Piezo_SeuilH = 27 #GPIO27 bouton 5
Piezo_SeuilL = 22 #GPIO22 bouton 4

# initialisation des entrées
IO.setwarnings(False)  #do not show any warnings
IO.setmode(IO.BCM)     #programming the GPIO by BCM pin numbers. (like PIN29 as'GPIO5')
IO.setup(Bouton_A, IO.IN,pull_up_down=IO.PUD_UP)  #initialize GPIO as an input with Pull Up internal resistor
IO.setup(Bouton_B, IO.IN,pull_up_down=IO.PUD_UP)  #idem
IO.setup(Bouton_C, IO.IN,pull_up_down=IO.PUD_UP)  #idem
IO.setup(WahWah_SeuilHH, IO.IN)  #initialize GPIO as an input
IO.setup(WahWah_SeuilH, IO.IN)  #idem
IO.setup(WahWah_SeuilL, IO.IN)  #idem
IO.setup(Piezo_SeuilHH, IO.IN)  #idem
IO.setup(Piezo_SeuilH, IO.IN)  #idem
IO.setup(Piezo_SeuilL, IO.IN)  #idem


class Grafcet:
	""" Classe permettant d'exécuter n'importe quel grafcet, tant que celui-ci ne comporte que des sélections de séquences.
		Les étapes et les transitions sont importées avec des fichiers .csv devant comporter les noms de colonnes suivants :
	"""
	#Liste des colonnes du fichier des étapes :
	colonnes_etapes=['nom_etape','nom_recette']

	#Liste des colonnes du fichier des conditions :
	colonnes_conditions=['nom_condition','nombre_lectures_sequence_mini','bouton','seuil_camera_mini','seuil_camera_maxi','temps_attente']

	#Liste des colonnes du fichier des transitions :
	colonnes_transitions=['etape_precedente','etape_suivante','condition1','operateur','condition2']

	
	def __init__(self, nom, fichier_type, fichier_etapes, fichier_conditions, fichier_transitions,mode):
		self.nom = nom
		self.typeG7 = self.lire_type(fichier_type)
		print("on importe le fichier étapes : {}".format(fichier_etapes))
		self.liste_etapes = Scadong_utils.import_csv(fichier_etapes, Grafcet.colonnes_etapes) # import csv des étapes et actions
		self.liste_conditions = Scadong_utils.import_csv(fichier_conditions, Grafcet.colonnes_conditions) # import csv des réceptivités 
		self.liste_transitions = Scadong_utils.import_csv(fichier_transitions, Grafcet.colonnes_transitions) # import csv des transitions
		self.liste_transitions_suivantes = [] # pour alléger la scrutation
		self.arret = True # arrêt scrutation
		self.debut_tempo = 0 # initialisé à l'activation d'une étape
		self.mode = mode
		self.etape = ""
		self.recette = ""

	def lire_type(self, file):
		f = open(file)
		txt = f.read().strip().encode('ascii','ignore').decode('utf8').replace(' ','_')
		f.close()
		return txt

	def chang_etape(self, etape_suivante):
		""" Fonction à l'activation d'une étape """
		# Initialisation de l'étape
		self.etape = etape_suivante
		self.liste_transitions_suivantes = [element for element in self.liste_transitions if element['etape_precedente']==self.etape]
		if self.liste_transitions_suivantes == []:
			raise EtapeError("Le nom d'étape {} n'est pas répertorié dans la liste des étapes".format(etape_suivante))
		else:
			self.debut_tempo = time.time()
		# Exécution des actions
		for element in self.liste_etapes:
			if element['nom_etape'] == self.etape:
				self.recette = element['nom_recette']
				if self.mode == "debug":
					print("Passage l'etape {} : lancement de la recette \"{}\" ".format(self.etape,element['nom_recette']))


	def start_init(self):
		self.arret = False
		self.chang_etape("init")

	def scrutation(self,mvmt,mot_I):
		condition = False
		for element in self.liste_transitions_suivantes:
			if self.mode == "debug":
				print("vecteur transition : {}".format(element)) # pour debug
			if element['condition1']!="nc":
				condition1=self.verifier(mvmt,mot_I,element['condition1'],element['etape_precedente'],element['etape_suivante'])
				if self.mode == "debug":
					print("condition 1={} vaut {}\n".format(element['condition1'],condition1))#pour debug
			if element['condition2']!="nc":
				condition2=self.verifier(mvmt,mot_I,element['condition2'],element['etape_precedente'],element['etape_suivante'])
				if self.mode == "debug":
					print("condition 2={} vaut {}\n".format(element['condition2'],condition2))#pour debug
			if element['condition1']!="nc" and element['condition2']!="nc":
				if element['operateur']=="and":
					condition = condition1 and condition2
				elif element['operateur']=="or":
					condition = condition1 or condition2
				elif element['operateur']=="and_not":
					condition = condition1 and not condition2
				elif element['operateur']=="or_not":
					condition = condition1 or not condition2
				else:
					raise EtapeError("Le format de l'opérateur {} n'est pas correct".format(element['operateur']))
			elif element['condition1']!="nc":
				condition=condition1
			elif element['condition2']!="nc":
				condition=condition2
			else:
				condition=False
			if condition:
				self.chang_etape(element['etape_suivante'])		  #franchissement de la transition
				break
	
	def verifier(self,mvmt,mot_I,condition,etape_prec,etape_suiv):
		Cond_Tempo=False
		Cond_Bouton=False
		Cond_Camera=False
		for element in self.liste_conditions:
			if element['nom_condition']==condition:
				### test tempo
				tempo_txt = element['temps_attente']
				if (len(tempo_txt.strip())==0): #chaine vide ou composée seulement de blancs
					tempo_txt = '0.0'
				try:
					tempo = float(tempo_txt)
					tempo = tempo / 1000 # passage de millisecondes à tempo
					#print("temporisation à l'étape {}:{} s".format(self.etape,tempo))#pour débug
				except ValueError:
					print("Erreur de saisie de la temporisation de {}s dans la transition de {} à {}".format(tempo_txt, etape_prec, etape_suiv))
				temps_ecoule = time.time() - self.debut_tempo
				if ( tempo >= 0) and (temps_ecoule >= tempo - 0.1):# on retranche -0.1 pour se laisser le temps d'exécuter la transition
					#print("temps_ecoulé : {} s ; tempo : {}".format(temps_ecoule, tempo)) # pour debug
					Cond_Tempo=True
				
				### test Boutons et autres entrées TOR
				message1 = ""
				if (element['bouton'].strip()=="1"):
					if mot_I & 1 != 0:
						Cond_Bouton=True
						message1 = "  A"
				elif (element['bouton'].strip()=="2"):
					if mot_I & 1 << 1 != 0:
						Cond_Bouton=True
						message1 += "  B"
				elif (element['bouton'].strip()=="3"):
					if mot_I & 1 << 2 != 0:
						Cond_Bouton=True
						message1 += "  C"
				elif (element['bouton'].strip()=="4"):
					if mot_I & 1 << 3 != 0 and mot_I & 1 << 4 == 0 and mot_I & 1 << 5 == 0:
						Cond_Bouton=True
						message1 += "  Piezo Seuil L"
				elif (element['bouton'].strip()=="5"):
					if mot_I & 1 << 4 != 0 and mot_I & 1 << 5 == 0:
						Cond_Bouton=True
						message1 += "  Piezo Seuil H"
				elif (element['bouton'].strip()=="6"):
					if mot_I & 1 << 5 != 0:
						Cond_Bouton=True
						message1 += "  Piezo Seuil HH"
				elif (element['bouton'].strip()=="7"):
					if mot_I & 1 << 6 != 0 and mot_I & 1 << 7 == 0 and mot_I & 1 << 8 == 0:
						Cond_Bouton=True
						message1 += "  WahWah Seuil L"
				elif (element['bouton'].strip()=="8"):
					if mot_I & 1 << 7 != 0 and mot_I & 1 << 8 == 0:
						Cond_Bouton=True
						message1 += "  WahWah Seuil H"
				elif (element['bouton'].strip()=="9"):
					if mot_I & 1 << 8 != 0:
						Cond_Bouton=True
						message1 += "  WahWah Seuil HH"
				elif (element['bouton'].strip()=="0") or (len(element['bouton'].strip())==0): #chaine vide ou composée seulement de blancs
					Cond_Bouton=True
				else : # caractère autre
					raise TransitionError("Le bouton {} n'est pas répertorié dans la liste des boutons".format(element['bouton'])) 
				### test Caméra
				try:
					seuil_bas = float(element['seuil_camera_mini'])
				except ValueError:
					print("Erreur de saisie de la valeur {}% du seuil bas de la caméra dans la transition de {} à {}".format(element['seuil_camera_mini'], etape_prec, etape_suiv))
				
				try:
					seuil_haut = float(element['seuil_camera_maxi'])
				except ValueError:
					print("Erreur de saisie de la valeur {}% du seuil haut de la caméra dans la transition de {} à {}".format(element['seuil_camera_maxi'], etape_prec, etape_suiv))
				
				if (mvmt >= seuil_bas) and  (mvmt <= seuil_haut):
					Cond_Camera=True
				
				### bilan
				if(self.mode == "debug"):
					print("temps écoule={} >= {} : {}".format(temps_ecoule,tempo,Cond_Tempo))
					message2 = "Cond_Bouton:{}".format(Cond_Bouton)
					if Cond_Bouton and len(message1) > 0:
						message2 = message2 + " : appui sur " + message1
					print(message2)
					print("{} <= mouvement Camera:{} <= {} :{}".format(seuil_bas,mvmt,seuil_haut,Cond_Camera))
				
				### Valeur booléenne renvoyée
				if Cond_Tempo and Cond_Bouton and Cond_Camera :
					return True
				else :
					return False
	

	def __repr__(self):
		""" représentation de l'objet grafcet """
		return "liste des étapes et actions associées :\n{}\
		\n \n \
liste des transisitions et réceptivités:\n{} \n \n".format(self.liste_etapes, self.liste_conditions)

	
class EtapeError(Exception):
	""" Exception qui est levée quand on cherche à appeler une étape dont le nom n'est pas répertoirié dans liste_étapes """
	def __init__(self, message):
		""" stockage du message d'erreur """
		self.message = message
	def __str__(self):
		""" on renvoie le message """
		return self.message

class TransitionError(Exception):
	""" Exception qui survient lors du passage d'une transition """
	def __init__(self, message):
		""" stockage du message d'erreur """
		self.message = message
	def __str__(self):
		""" on renvoie le message """
		return self.message

def AcquisitionETOR(entrees):
	entrees = 0
	if (IO.input(Bouton_A) == 0):
		entrees |= 1
	if (IO.input(Bouton_B) == 0):
		entrees |= 1 << 1
	if (IO.input(Bouton_C) == 0):
		entrees |= 1 << 2
	if (IO.input(Piezo_SeuilL) == 1):
		entrees |= 1 << 3
	if (IO.input(Piezo_SeuilH) == 1):
		entrees |= 1 << 4
	if (IO.input(Piezo_SeuilHH) == 1):
		entrees |= 1 << 5
	if (IO.input(WahWah_SeuilL) == 1):
		entrees |= 1 << 6
	if (IO.input(WahWah_SeuilH) == 1):
		entrees |= 1 << 7
	if (IO.input(WahWah_SeuilHH) == 1):
		entrees |= 1 << 8
	return entrees


# test grafcet "instrumentiste" en python
if __name__ == "__main__":
	# initialisation de la caméra
	#Oeil=PiEye.PiEye() # initialisation de la caméra
	# première acquisition des entrées
	mot_IO = 0
	mot_IO = AcquisitionETOR(mot_IO)
	chemin="fichiers_csv/" 
	mode="normal"
	# inventaire des grafcets à créer sur la base des fichiers déposés
	liste_fichiers = os.listdir(chemin)
	fin ="conditions.csv"
	noms_instruments =[fichier.rpartition("_")[0] for fichier in liste_fichiers if fichier.endswith(fin)]
	print(noms_instruments)
	# création des grafcets
	grafcets=[]
	for nom_instrum in noms_instruments:
		fichier_type = chemin+nom_instrum+"_"+"type.csv"
		fichier_etapes = chemin+nom_instrum+"_"+"etapes.csv"
		fichier_conditions = chemin+nom_instrum+"_"+"conditions.csv"
		fichier_transitions = chemin+nom_instrum+"_"+"transitions.csv"
		g7=Grafcet(nom_instrum,fichier_type, fichier_etapes, fichier_conditions, fichier_transitions, mode)
		grafcets.append(g7)
	# initialisation des grafcets
	for g7 in grafcets:
		g7.start_init()
		print("On démarre le grafcet {}".format(g7.nom))

	#cycle automate
	while True:
		# acquistion caméra
		#mouvement = Oeil.voir()
		mouvement = 0
		# acquisition entrées TOR
		mot_IO = AcquisitionETOR(mot_IO)
		# scrutation des grafcets
		for g7 in grafcets:
			os.system('clear')
			print("mouvement détecté par la caméra :{:.3f}\n\n\n".format(mouvement))
			print("mot_IO={}".format(mot_IO))
			print("grafcet {} de type {}:".format(g7.nom, g7.typeG7))
			print("\t l'étape en cours est : {}".format(g7.etape))
			print("\t la recette en cours est : {}".format(g7.recette))
			g7.scrutation(mouvement, mot_IO)
			# temps d'affichage
			time.sleep(1)

	print("\n \n ****** Fin *********")
