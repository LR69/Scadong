# programme séquenceur : ce programme a pour but de jouer des sons à des temps déterminés.
# 		Ce programme utilise :
#				les fichiers .wav présents dans le dossier 'fichiers_sons'
#				le fichier 'tictictic.wav' doit obligatoirement être présent dans le dossier 'fichiers_sons'
# version 1 modifiée par LR le 30/10/17 : version autonome
# version 2 modifiée par LR le 31/10/17 : version autonome avec paramétrage nombre de canaux et contrôle du nombre de canaux libres
# version 3 modifiée par LR le 31/10/17 : version utilisable en multiprocessing
# version 4 modifiée par LR le 1/11/17 : ajout de la demande "remplissage tampon" du séquenceur.
# version 5 modifiee par LR le 2/11/17 : ajout de time.sleep dans les boucles while
# version 6 modifiée par LR le 13/07/18 : modification du main pour un fonctionnement par multiprocessing en mode debug
# version 7 modifiée par LR le 23/07/18 : conformisation au fichier patron_multiprocessV4.pdf


import pygame.mixer #calling for pygame mixer to play audio files
import time			#calling for time to provide delays in program
import os
import multiprocessing as mp
import queue

def sequenceur(Buf,q_data, q_result,q_ordre,q_etat):
	""" processus chargé de jouer les sons envoyés sur des feuilles"""
	pygame.mixer.init(44100, -16, 2, 1024)	#initializing audio mixer
	papier_musique=[]
	feuille=[]
	nbre_canaux=512
	pygame.mixer.set_num_channels(nbre_canaux)
	mode="normal" #on peut aussi être en mode "debug" pour test avec le __main__ en bas de fichier
	h=0.006 #temps du battement d'horloge en s

	# récupération du mode 
	o=q_ordre.get()
	if o=="debug" and mode=="normal":
		mode="debug"
		q_etat.put("mode={}".format(mode)) #pour debug
		q_etat.put("la valeur de l'horloge vaut {}s".format(h))
	# remplissage du tampon
	os.system("cp -f baguette/tictictic.wav fichiers_sons/") # au cas où le fichier aurait été effacé
	un_peu_d_attention_SVP = []
	for i in range(1, 4*Buf+1):
		un_peu_d_attention_SVP.append(('tictictic.wav',0.8))
	if mode == "debug":
		q_etat.put(un_peu_d_attention_SVP)
	for trou in un_peu_d_attention_SVP:
		channels=[]
		nom_son,vol = trou
		fichier="fichiers_sons/"+nom_son
		if mode == "debug":
			q_etat.put("un nouveau trou : {}".format(nom_son))#pour debug
		ch=pygame.mixer.find_channel()
		if ch==None:
			raise ChannelError("Le nombre maximal de canaux audios disponibles ({}) est dépassé".format(nbre_canaux))
		son=pygame.mixer.Sound(fichier)
		ch.play(son)
		ch.set_volume(vol)
		ch.pause()
		channels.append((nom_son,ch)) #on compose la ligne de trous
		papier_musique.append(channels) # ajout ligne trous sur papier musique
	#print("longueur papier à musique:{}".format(len(papier_musique))) # pour debug
	
	# attente de l'ordre de lancement
	o=""
	while (o!="go"):
		o = q_ordre.get()
	q_etat.put("c_parti")
	o=""
	e="dmd_data"
	n=0
	t0=time.time()
	while(o!="stop"):
		if ((time.time()-t0)>h/2) and e!="dmd_OK":
			if (len(papier_musique)<=Buf): # à faire à la 1/2 horloge
				if e=="dmd_data":
					for i in range(1,Buf+1):
						#q_etat.put("remplissage tampon")
						vide=False
						try: #récupération données à traiter
							nv=q_data.get(False)
						except queue.Empty:
							vide=True
							if mode == "debug":
								q_etat.put("TAMPON VIDE !")
							papier_musique.append([])
							papier_musique.append([])
							pass
						if not vide:
							# if mode == "debug":
							# 	print("nv={}".format(nv))#pour debug
							channels=[]
							for trou in nv:
								nom_son,vol = trou
								fichier="fichiers_sons/"+nom_son
								if mode == "debug":
									q_etat.put("un nouveau trou : {}".format(nom_son))#pour debug
								ch=pygame.mixer.find_channel()
								if ch==None:
									raise ChannelError("Le nombre maximal de canaux audios disponibles ({}) est dépassé".format(nbre_canaux))
								son=pygame.mixer.Sound(fichier)
								ch.play(son)
								ch.set_volume(vol)
								ch.pause()
								channels.append((nom_son,ch)) #on compose la ligne de trous
							papier_musique.append(channels) # ajout ligne trous sur papier musique
					e="dmd_OK"
				else:
					q_etat.put("dmd_data")
					e="dmd_data"

		if ((time.time()-t0)>h): # à faire à l'horloge
			t0 = time.time()
			ligne=papier_musique.pop(0)
			e="son_joue"
			#traitement donnée reçue
			for hole in ligne: 
				nm,ch=hole
				ch.unpause() 
				top_arrivee = time.time()
				#q_etat.put("top_arrivee :{}".format(top_arrivee))
				if mode == "debug":
					q_etat.put("temps n°{} \ton joue:{} ".format(n,nm))# pour debug
			n+=1 # compteur d'horloge, théoriquement sans limite sous py3
			time.sleep(0.001)#minimum requis pour stabilité
			if len(papier_musique)==0:
				o="stop"
	
	tf=time.time()
	while len(papier_musique)>0: #bouclage tant qu'on est pas arrivé à la fin du papier
		if time.time()-tf>h:
			tf=time.time()
			n+=1
			ligne=papier_musique.pop(0)
			for hole in ligne:
				nm,ch =hole
				ch.unpause()
				if mode == "debug":
					q_etat.put("temps n°{} \ton joue:{} ".format(n,nm))# pour debug
		time.sleep(0.001) # pour permettre à la boucle de détecter une variation de temps
	
	time.sleep(2)# pour permettre aux sons en cours de se terminer
	q_etat.put("\n \n ****** Fin processus sequenceur *********")
	q_etat.put("c_fini")
			
			
class ChannelError(Exception):			  
	""" Exception qui est levée quand on cherche à utilser plus de canaux que définis dans l'interface audio """
	def __init__(self, message):
		""" stockage du message d'erreur """
		self.message = message
	def __str__(self):
		""" on renvoie le message """
		return self.message


if __name__ == "__main__":
	listwav = os.listdir("fichiers_sons")
	feuille =[]
	# for wav in listwav:
	for i in range(0,4000):
		elt = [("piano_pre_sat01.wav",0.5)]
		#elt = [(str(wav),0.5)]
		feuille.append(elt)
		elt =[]
		for i in range(0,10):
			feuille.append(elt)
	# wav = listwav.pop()
	# elt = [(str(wav),0.3)]
	# feuille.append(elt)
	
	print(feuille)
	
	Tampon = 4
	ctx = mp.get_context('spawn')
	qd = ctx.Queue()
	qr = ctx.Queue()
	qo = ctx.Queue()
	qe = ctx.Queue()
	
	# Lancement du séquenceur
	psequenceur = ctx.Process(target=sequenceur, args=(Tampon,qd,qr,qo,qe)) # fq = canal des feuilles, oq canal des ordres donnés au séquenceur, eq canal états séquenceur
	psequenceur.start()
	qo.put("debug")
	time.sleep(3)
	qo.put("go")
	e=""
	while (e!="c_parti"):
		e = qe.get()
	
	### envoi par paquets 
	e=""
	while (e!="c_fini"):
		e=""
		try:
			e=qe.get(False)
			print(e)
		except queue.Empty:
			pass
		
		if (e=="dmd_data" and len(feuille)>0):
			top_depart = time.time()
			print("top_depart : {} \t |||||||||||||||||||||||| -------------------- ||||||||||||||||||".format(top_depart))
			d = feuille.pop()	
			qd.put(d)
			print("envoi ligne : {}".format(d))#ajtp
			for i in range(1,1+Tampon*10):
				l=[]
				qd.put(l)

	psequenceur.join()
	print("\n \n ****** Fin processus parent *********")

