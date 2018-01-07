# programme séquenceur : ce programme a pour but de jouer des sons à des temps déterminés.
# version 1 modifiée par LR le 30/10/17 : version autonome
# version 2 modifiée par LR le 31/10/17 : version autonome avec paramétrage nombre de canaux et contrôle du nombre de canaux libres
# version 3 modifiée par LR le 31/10/17 : version utilisable en multiprocessing
# version 4 modifiée par LR le 1/11/17 : ajout de la demande "remplissage tampon" du séquenceur.
# version 5 modifiee par LR le 2/11/17 : ajout de time.sleep dans les boucles while
# version 1d

import pygame.mixer #calling for pygame mixer to play audio files
import time			#calling for time to provide delays in program
import os


def sequenceur(bout_feuille,ordre,etat):
	""" processus chargé de jouer les sons envoyés sur des feuilles"""
	pygame.mixer.init(44100, -16, 2, 1024)	#initializing audio mixer
	papier_musique=[]
	feuille=[]
	nbre_canaux=32
	pygame.mixer.set_num_channels(nbre_canaux)
	mode="normal" #on peut aussi être en mode "debug" pour test avec le __main__ en bas de fichier
	h=0.1 #temps du battement d'horloge en s
	pas=1 #taille du pas
	avance=max(int(1/(h*pas)),3) #chargement amont du papier à musique (pour avoir environ 1 sec d'avance)
	for i in range(0,avance):
		ligne=[('tictictic.wav',0.8)]
		channels=[]
		for trou in ligne:
			fichier,vol = trou
			fichier="baguette/"+fichier
			ch=pygame.mixer.find_channel()
			son=pygame.mixer.Sound(fichier)
			ch.play(son)
			ch.set_volume(vol)
			ch.pause()
			channels.append(ch)
		papier_musique.append(channels)
	t0=time.time()
	t1=time.time()
	o="rien"
	while o!="go": # attente de l'ordre de démarrage
		o=ordre.get()
		if o=="debug":
			mode="debug"
			print("mode={}".format(mode)) #pour debug

	e="OK"
	envoi1 = False
	envoi2 = False
	n=0
	while o!="stop" and (e=="OK" or mode=="normal"): #bouclage tant que pas d'ordre d'arret
		# à faire à chaque pas
		if time.time()-t0>pas*h:
			t0=time.time()
			if papier_musique!=[]: #si c'est vide, c'est vide ! on ne joue rien
				for ch in papier_musique[0]:
					if ch!=[]: # sinon c'est un silence
						ch.unpause()
				#élimination de la ligne de trous jouée
				del papier_musique[0]
				time.sleep(0.002) # pour permettre à la boucle de détecter une variation de temps
				#delta_t=str(1E3*(time.time()-t0)) # pour debug
				#etat.put("on joue:{} pendant {} ms".format(n,delta_t)) # pour debug
				#etat.put("la feuille a une longueur  de :{}".format(len(feuille))) # pour debug
				#etat.put("le papier musique a une longueur  de :{}".format(len(papier_musique))) # pour debug
				#etat.put("flag envoi1:{} ; flag envoi2:{}".format(envoi1,envoi2)) # pour debug
				#n+=1 # pour debug
		# à faire à chaque demi pas
		if time.time()-t1>pas*h/10:
			t1=time.time()
			#prépartion des trous suivants
			if len(feuille)>0 and len(papier_musique)<=avance:
				ligne=feuille[0]
				channels=[]
				for trou in ligne:
					fichier,vol = trou
					fichier="fichiers_sons/"+fichier
					ch=pygame.mixer.find_channel()
					if ch==None:
						raise ChannelError("Le nombre maximal de canaux audios disponibles ({}) est dépassé".format(nbre_canaux))
					son=pygame.mixer.Sound(fichier)
					ch.play(son)
					ch.set_volume(vol)
					ch.pause()
					channels.append(ch)
				papier_musique.append(channels)
				#elimination de la ligne entrante
				del feuille[0]
				#e="feuille restante : "+str(len(feuille))+"envoi = "+str(envoi) #pour debug	
				#if mode == "debug":
					#print(e) #pour debug
				#else:
					#etat.put(e)
			#échange avec processus parent
			if ordre.empty()==False:
				try:
					o=ordre.get(False)
				except queue.Empty:
					e="queue ordre est vide"
					if mode == "debug":
						print(e) #pour debug
					else:
						etat.put(e)
					pass
			if bout_feuille.empty()==False:
				try:
					bout=bout_feuille.get(False)
				except queue.Empty:
					e="queue bout_feuille est vide"
					if mode == "debug":
						print(e) #pour debug
					else:
						etat.put(e)					   
					pass
				feuille.append(bout)
				envoi1=False
				envoi2=False
			if len(feuille)<avance and not envoi1: 
				envoi1=True
				e="demande_papier"	
				if mode == "debug":
					print(e) #pour debug
				else:
					for i in range (1, avance-len(feuille)):
						etat.put(e)
			if len(feuille)==0 and not envoi2: #le tampon est complètement vide !
				envoi2=True
				e="fin_papier"	
				if mode == "debug":
					print(e) #pour debug
				else:
					etat.put(e)
		time.sleep(0.002) # pour permettre à la boucle de détecter une variation de temps
	
	t3=time.time()
	while len(papier_musique)>0: #bouclage tant qu'on est pas arrivé à la fin du papier
		if time.time()-t3>pas*h:
			t3=time.time()
			for ch in papier_musique[0]:
				if ch!=[]:
					ch.unpause()
			#élimination de la ligne de trous jouée
			del papier_musique[0]
		time.sleep(0.002) # pour permettre à la boucle de détecter une variation de temps
	
	time.sleep(5)# pour permettre aux sons en cours de se terminer
	etat.put("fin")
			
class ChannelError(Exception):			  
	""" Exception qui est levée quand on cherche à utilser plus de canaux que définis dans l'interface audio """
	def __init__(self, message):
		""" stockage du message d'erreur """
		self.message = message
	def __str__(self):
		""" on renvoie le message """
		return self.message


if __name__ == "__main__":
	import queue
	fq=queue.Queue()
	oq=queue.Queue()
	eq=queue.Queue()
	feuille = [[('accord_pro2_orgue_poly_lo-fi_G7.wav',0.2),('percu-basse_pro_2_sher_DSI-ra_Rydm_Gb.wav',0.1)],[('percu-basse_pro_2_sher_DSI-ra_Rydm_Gb.wav',0.2)],[],[],[('percu-basse_pro_2_sher_DSI-ra_Rydm_Gb.wav',0.2),('koto_stable_B_04.wav',0.1)]]

	for ligne in feuille:
		fq.put(ligne)
		print(ligne)

	oq.put("debug")
	oq.put("go")
	
	sequenceur(fq,oq,eq)
	e="OK"
	while e!="fin":
		e=eq.get()
	print("\n \n ****** Fin *********")

