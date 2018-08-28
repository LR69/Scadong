import sequenceur
import Scadong_utils
import filtres
import time
import random
import multiprocessing as mp
import queue
import os



class Sequence:
	""" Classe permettant de décrire une séquence telle qu'elle est définie dans l'onglet "séquence" 
	"""
	def __init__(self, nom, taille_pas, longueur, bouclage, depart, seq_base, num_pas, num_boucle):
		self.nom = nom # le nom de la séquence
		self.taille_pas = taille_pas # la taille_du_pas : si pas = 2 , on à un temps de 2 * l'horloge h entre 2 lignes
		self.longueur = longueur # la longueur de la séquence
		self.bouclage = bouclage # le type de bouclage. contient le nombre maximal de fois ou une séquence est jouée à une étape du grafcet. une valeur de -1 correspond à un bouclage infini 
		self.depart = depart # correspond à la valeur de "départ séquence" dans l'onglet recette. les valeurs possibles sont : "begin" dans le cas d'une lecture de la séquence à partir de sa première ligne ; "continu" pour le cas d'une lecture à partir de l'index de la séquence précédente ; "random" pour une lecture partant n'importe où dans la séquence.
		self.seq_base = seq_base # la séquence de base. Tableau contenant les sons à jouer à chaque pas, ainsi que leur volume, sous la forme d'un tuple ("fichier_son", volume)
		self.num_pas = num_pas # le pas en cours
		self.num_boucle = num_boucle # la boucle en cours
	def __repr__(self):
		return "sequence {} : \n {} \n \à jouer avec un pas de {}, type bouclage : {}, type de lecture : {} ".format(self.nom, self.seq_base, self.taille_pas, self.bouclage, self.depart)

def fournir_sequence(etape,recette,inventaire):
	liste_sons_filtres=[] # 1er tri
	liste_sons_filtres2=[] # 2nd tri
	liste_sons_filtres3=[] # 3ème tri
	feuille=[] # contient la séquence de base
	journal=[] # contient les infos pour le serveur
	### Application de la recette
	if(recette != "" and recette != "nc"):
		#recette trouvée dans la liste des recettes à partir du nom de la recette
		recette_dans_liste=[element for element in inventaire['recettes'] if element['nom de recette']==recette][0] # on trouve la recette en cours dans l'inventaire des recettes
		# print("recette trouvée dans la liste = {}".format(recette_dans_liste)) # pour debug
		filtre_recette_nom = recette_dans_liste['filtre']
		if (filtre_recette_nom != "" and filtre_recette_nom != "nc"):
			filtre_recette=[element for element in inventaire['filtres'] if element['nom du filtre']==filtre_recette_nom][0] 
			# print("Filtre applicable au niveau de la recette : {}".format(filtre_recette)) # pour debug
			#premier filtrage des sons :
			liste_sons_filtres=filtres.filtrage(inventaire['sons'],filtre_recette)
			# print("Nom du filtre applicable au niveau de la recette : {}".format(filtre_recette_nom)) # pour debug
			# print("nombre de sons après filtrage recette : {}".format(len(liste_sons_filtres)))	# pour debug
			# print([element['nom du son'] for element in liste_sons_filtres]) # pour debug
		else:
			liste_sons_filtres=inventaire['sons'] #pas de premier filtrage
			# print("pas de premier filtrage") # pour debug
	### Application de la séquence
	#séquence trouvée dans la liste des séquences à partir du nom de la séquence figurant dans la recette
	depart = recette_dans_liste['départ séquence']
	# print("recette_dans_liste['séquence']:{}, type de départ :{}".format(recette_dans_liste['séquence'],depart)) #pour debug
	sequences_dans_liste=[element for element in inventaire['sequences'] if element['nom séquence']==recette_dans_liste['séquence']] # on trouve la liste des séquences de nom 'nom séquence'
	# print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@  sequences_dans_liste:{}".format(sequences_dans_liste)) # pour debug
	if len(sequences_dans_liste)>0:
		nom_sequence = [element['nom séquence'] for element in sequences_dans_liste][0]
		# print("Nom de la séquence applicable au niveau de la recette : {}".format(nom_sequence)) # pour debug
		# print("Nombre de trigs: {}".format(len([element['nom séquence'] for element in sequences_dans_liste]))) # pour debug
		longueur_sequence = int([element['longueur séquence'] for element in sequences_dans_liste][0])
		# print("longueur séquence :{}".format(longueur_sequence)) # pour debug
		taille_pas = int([element['taille du pas'] for element in sequences_dans_liste][0])
		# print("taille du pas :{}".format(taille_pas)) # pour debug
		bouclage = int([element['nombre de boucle séquence(-1 = inf)'] for element in sequences_dans_liste][0])
		# print("type de bouclage :{}".format(bouclage)) # pour debug
		for tic in range(1,longueur_sequence+1): # tic = pas
			# print("pas = {} ; ".format(tic)) # pour debug
			sequences_au_tic = [element for element in sequences_dans_liste if int(element['temps du trig (en pas)'])==tic] #on trouve les séquences à jouer pour ce pas de temps
			# print("Nombre de trig: {} au pas : {}".format(len([element['nom séquence'] for element in sequences_au_tic]),tic)) # pour debug
			ligne_trous=[] # une nouvelle ligne de trous dans le papier à musique
			ligne_infos=[] # les infos pour le serveur
			for sequence in sequences_au_tic:
				volume = float(sequence['volume (vélocité)'])/100.0 #volume compris entre 0 et 1
				filtre_sequence = [element for element in inventaire['filtres'] if element['nom du filtre']==sequence['filtre']][0]
				# print("un filtre applicable au tic:{} est :{}".format(tic, filtre_sequence['nom du filtre'])) #pour debug
				# print("le volume à jouer est :{}".format(volume))
				#second filtrage des sons :
				# print("liste_sons_filtres:{}".format([element['nom du son'] for element in liste_sons_filtres])) # pour debug
				# 
				# print("filtre_sequence:{}".format(filtre_sequence)) # pour debug
				liste_sons_filtres2=filtres.filtrage(liste_sons_filtres,filtre_sequence)
				# if len(liste_sons_filtres)>0:
				# 	print("nombre de sons après filtrage séquence : {}".format(len(liste_sons_filtres2)))	# pour debug
				# print("noms des sons triés au niveau de la séquence : ") # pour debug
				# print([element['nom du son'] for element in liste_sons_filtres2]) # pour debug
				#tri des sons par priorité
				if liste_sons_filtres2!=[]:
					score=0
					for element in liste_sons_filtres2:
						score_temp = int(element['priorité (de 0 à 100)'])
						#print("score temp= {}".format(score_temp)) # pour debug
						if score_temp > score:
							score = score_temp
					#print("score = {}".format(score)) # pour debug
					liste_sons_filtres3=[element for element in liste_sons_filtres2 if int(element['priorité (de 0 à 100)'])==score]
					# print("noms des sons triés et prioritaires : ") # pour debug
					# print([element['nom du son'] for element in liste_sons_filtres3]) # pour debug
					index_alea=random.randint(1,len(liste_sons_filtres3)) # random.randint(a, b) Return a random integer N such that a <= N <= b. Alias for randrange(a, b+1).
					#print(index_alea) # pour debug
					for i in range(0,index_alea):
						son_a_jouer=liste_sons_filtres3.pop()
					#print("son à jouer : {}".format(son_a_jouer['nom du son'])) # pour debug
					fichier_son_a_jouer=son_a_jouer['nom du son']+".wav"
					trou = (fichier_son_a_jouer, volume)
					#on fait un trou sur ligne de trous dans le papier à musique
					ligne_trous.append(trou)
					#on garde les infos propres à la ligne du séquenceur pour les communiquer au serveur
					infos = (sequence['nom séquence'], sequence['trig'], sequence['filtre'], fichier_son_a_jouer, volume)
					ligne_infos.append(infos)
			#if ligne_trous != [] :
				# print("sons à jouer au trig{}:{}".format(tic,ligne_trous))
			feuille.append(ligne_trous)
			journal.append(ligne_infos)
		# élaboration de la séquence
		# A faire !!!: gestion du type de départ !!!!!!!
		seq = Sequence(nom_sequence,taille_pas,longueur_sequence,bouclage,depart,feuille,1,1) # Attention on commence au pas 1 pour correspondre aux valeurs du tableau
		return (seq,journal)
	else:
		return ([],[])


def fournir_ligne(indx, liste_sequences, jrnaux):
	""" cette fonction fournit la ligne à jouer en fonction d'un tableau de séquence"""
	ligne=[] # une ligne à jouer
	infos_ligne =[]
	for seq in liste_sequences:
		if isinstance(seq,Sequence):#on teste si la séquence est du bon type
			if indx % seq.taille_pas == 0:
				if (seq.bouclage<0) or (seq.num_boucle <= seq.bouclage):
					#on a un bouclage infini ou on a pas atteint le nombre de boucles prévues
					#print("index={},seq.num_pas:{}/{}".format(indx,seq.num_pas,seq.longueur))
					tr = seq.seq_base[seq.num_pas-1]
					if len(tr)>0:
						ligne.append(tr[0]) # on va jouer ce son
					# on récupère les infos propre à ce son
					idx_jrnal = liste_sequences.index(seq)
					jrnal = jrnaux[idx_jrnal]# journal propre à la séquence
					news = jrnal[seq.num_pas-1] # les infos propres au son
					if len(news) > 0:
						infos_ligne.append(news)
					if (seq.num_pas < seq.longueur):
						seq.num_pas+=1 # on avance d'un pas dans la séquence
					else:# on réinitialise la séquence
						seq.num_pas = 1 
						seq.num_boucle += 1
						# on part de 1 pour que les numéros correspondent à ceux de l'onglet séquence
	return (ligne, infos_ligne)


def generer_inventaire(instrum):
	chemin_csv = "fichiers_csv/" #pour pouvoir trouver le chemin des fichiers
	inventaire = {} #stockage sous la forme d'un dico
	# import csv des sons
	colonnes_sons=['nom du son','Durée (sec)','Motcle 1','Motcle 2','Motcle 3','Motcle 4','Motcle 5','Motcle 6','Motcle 7','Motcle 8','Motcle 9','Motcle 10','Motcle 11','Motcle 12','Motcle 13','Motcle 14','Motcle 15','Motcle 16','Motcle 17','Motcle 18','Nuance 1','Nuance 2','Nuance 3','Nuance 4','Nuance 5','Nuance 6','Nuance 7','Attaque 1','Attaque 2','Attaque 3','Relâchement 1','Relâchement 2','Relâchement 3','Note Fondamental 1','Note Fondamental 2','Note Fondamental 3','Note Fondamental 4','Note Fondamental 5','Note Fondamental 6','Note Fondamental 7','Note Fondamental 8','Note Fondamental 9','Note Fondamental 10','Note Fondamental 11','Note Fondamental 12','Note Fondamental 13','Phrase Musical?','Phrasé','note dans l\'Accord 1','note dans l\'Accord 2','note dans l\'Accord 3','note dans l\'Accord 4','note dans l\'Accord 5','note dans l\'Accord 6','note dans l\'Accord 7','note dans l\'Accord 8','note dans l\'Accord 9','note dans l\'Accord 10','note dans l\'Accord 11','note dans l\'Accord 12','Tempo','Variation de Tempo','priorité (de 0 à 100)']
	inventaire['sons'] = Scadong_utils.import_csv(chemin_csv+instrum+"_"+"id_son.csv", colonnes_sons) #import csv des sons
	#print(inventaire_sons) # pour debug
	#print("import csv des sons OK") # pour debug
	colonnes_filtres=['nom du filtre','Durée mini (sec)','Durée maxi (sec)','Motcle 1','Motcle 2','Motcle 3','Motcle 4','Motcle 5','Motcle 6','Motcle 7','Motcle 8','Motcle 9','Motcle 10','Motcle 11','Motcle 12','Motcle 13','Motcle 14','Motcle 15','Motcle 16','Motcle 17','Motcle 18','Nuance 1','Nuance 2','Nuance 3','Nuance 4','Nuance 5','Nuance 6','Nuance 7','Attaque 1','Attaque 2','Attaque 3','Relâchement 1','Relâchement 2','Relâchement 3','Note Fondamental 1','Note Fondamental 2','Note Fondamental 3','Note Fondamental 4','Note Fondamental 5','Note Fondamental 6','Note Fondamental 7','Note Fondamental 8','Note Fondamental 9','Note Fondamental 10','Note Fondamental 11','Note Fondamental 12','Note Fondamental 13','Phrase Musical?','Phrasé','note dans l\'Accord 1','note dans l\'Accord 2','note dans l\'Accord 3','note dans l\'Accord 4','note dans l\'Accord 5','note dans l\'Accord 6','note dans l\'Accord 7','note dans l\'Accord 8','note dans l\'Accord 9','note dans l\'Accord 10','note dans l\'Accord 11','note dans l\'Accord 12','Tempo min','Tempo max','Variation de Tempo','priorité (de 0 à 100)']
	inventaire['filtres'] = Scadong_utils.import_csv(chemin_csv+instrum+"_"+"filtre.csv", colonnes_filtres) #import csv des filtres
	#print("inventaire filtres:{}".format(inventaire['filtres'])) # pour debug
	#print("import csv des filtres OK") # pour debug
	#test_filtres(inventaire_sons,inventaire_filtres) #pour debug
	
	colonnes_recettes=['nom de recette','filtre','séquence','départ séquence','type de lecture','nbre de canal de lecture max','départ vers effet A','départ vers effet B','départ vers effet C','départ vers effet D','départ vers effet E','départ vers effet F','départ vers effet G','départ vers effet H']
	inventaire['recettes'] = Scadong_utils.import_csv(chemin_csv+instrum+"_"+"recette.csv", colonnes_recettes) #import csv des recettes
	#print("inventaire recettes :{}".format(inventaire['recettes'])) # pour debug
	#print("import csv des recettes OK") # pour debug
	
	colonnes_sequences=['nom séquence','taille du pas','longueur séquence','nombre de boucle séquence(-1 = inf)','trig','temps du trig (en pas)','volume (vélocité)','filtre','chance de jeu (entre 0 et 100)','départ vers effet A','départ vers effet B','départ vers effet C','départ vers effet D','départ vers effet E','départ vers effet F','départ vers effet G','départ vers effet H']
	inventaire['sequences'] = Scadong_utils.import_csv(chemin_csv+instrum+"_"+"sequence.csv", colonnes_sequences) #import csv des sequences
	#print("import csv des séquences OK") # pour debug
	return(inventaire)

def fournir_sons(q_instruments,q_etapes,q_recettes,q_or,q_et):
	""" ce processus fournit des sons au séquenceur quand celui-ci en fait la demande """
	#fanion = 0 #ajtp
	o=""
	e=""
	while o!="init":
		#échanges avec processus parent
		if q_or.empty()==False:
			try:
				o=q_or.get(False) # non bloquant
				# print("ordre du pgme principal au fournisseur : {}".format(o)) #pour debug
			except queue.Empty:
				pass
		if o=="init":
			#print("ordre du pgme principal au fournisseur : initialisation séquenceur") #pour debug
			try:
				instruments=q_instruments.get() # bloquant
				#print("instruments reçus du programme ppal : {}".format(instruments)) #pour debug
			except queue.Empty:
				pass
	
	#initialisation des liste en fonction du nombre d'instruments
	sequences=[]
	etapes=[]
	recettes=[]
	journaux=[]
	for instrument in instruments:
		sequences.append('')
		etapes.append('')
		recettes.append('')
		journaux.append('')
	#print("les séquences sont initialisées à :{}".format(sequences)) #pour debug
	#print("les étapes sont initialisées à :{}".format(etapes)) #pour debug
	#print("les séquences sont initialisées à :{}".format(recettes)) #pour debug
	#print("les journaux sont initialisés à :{}".format(journaux)) #pour debug
	
	
	
	# génération des inventaires de sons, filtres, recettes et séquences pour chaque instrument
	inventaire={} # dico des inventaires
	for instr in instruments:
		inventaire[instr] = generer_inventaire(instr)
	# print("l'inventaire est initialisé à : {}".format(inventaire)) #pour debug
	
	Tampon = 5
	ctx = mp.get_context('spawn')
	qd = ctx.Queue()
	qr = ctx.Queue()
	qo = ctx.Queue()
	qe = ctx.Queue()
	
	# Lancement du séquenceur
	psequenceur = ctx.Process(target=sequenceur.sequenceur, args=(Tampon,qd,qr,qo,qe)) # fq = canal des feuilles, oq canal des ordres donnés au séquenceur, eq canal états séquenceur
	psequenceur.start()
	qo.put("normal") # en normal, le sequenceur, n'envoie que des demandes "dmd_data"
	#qo.put("debug") # en debug, le sequenceur renvoie au fournisseur les lignes qu'il joue et les messages de tampon vide
	
	qo.put("go")
	t0 = time.time()
	e=""
	while (e!="c_parti"):
		e = qe.get()
		#print(e)
	bout_feuille=[]
	flag_run = True
	flag_arret = False
	#initialisation de l'index global
	index = 0 
	#boucle principale : écoute le process ppal et fournit des lignes au séquenceur
	#q_et.put("on rentre dans la boucle ppale de fournir sons, o = {}\n".format(o))
	while (e!="c_fini"):
		#échanges avec processus parent
		o=""
		if q_or.empty()==False:
			try:
				#print("un ordre est reçu du processus maitre")#pour debug
				o=q_or.get(False) # non bloquant
				q_et.put("ordre du pgme principal au fournisseur : {}\n".format(o))
			except queue.Empty:
				pass
		if o=="nouvelle_etape":
			q_et.put("nouvelle étape\n")
			etapes_old = etapes
			try:
				etapes=q_etapes.get() # bloquant
				q_et.put("etapes reçues du programme ppal : {}\n".format(etapes))
			except queue.Empty:
				pass
			try:
				recettes=q_recettes.get() # bloquant
				q_et.put("recettes reçues du programme ppal : {}\n".format(recettes))
			except queue.Empty:
				pass
			for instrument in instruments:
				i=instruments.index(instrument)
				# print(" Quelques infos :\n \t instrument = {} \n \t i ={} \n\t etapes[i] = {} \n\t recettes[i] = {} \n\t longueur  inventaire[instrument] = {} \n\n".format(instrument, i, etapes[i],recettes[i],len(inventaire[instrument]))) # pour debug 
				if etapes[i] != etapes_old[i]: #si pour l'instrument donné on a changé d'étape
					# if fanion == 0: #ajtp
					# 	top_depart = time.time()
					# 	q_et.put("top_depart = {}".format(top_depart))
					q_et.put("instrument :{}".format(instrument))
					q_et.put("i = {}".format(i))
					q_et.put("etapes :{}".format(etapes[i]))
					q_et.put("recettes :{}".format(recettes[i]))
					#q_et.put("inventaire : {}".format(inventaire[instrument]))
					# if fanion == 0: #ajtp
					# 	top_inter1 = time.time()
					# 	q_et.put("top_inter1 : {}".format(top_inter1))
					(sequences[i],journaux[i]) = fournir_sequence(etapes[i],recettes[i],inventaire[instrument])
					# if fanion == 0: #ajtp
					# 	top_inter2 = time.time()
					# 	q_et.put("top_inter2 : {}".format(top_inter2))
					# 	fanion = 1
					q_et.put(str(sequences[i]))
					q_et.put(str(journaux[i]))
			q_et.put("nouvelles sequences : {}\n".format(sequences))
		if o=="dmd_arret":
			flag_arret = True
		if o=="dmd_pause" and flag_run: # si on reçoit une demande de pause et qu'on était en run
			q_et.put(" §§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§ PAUSEEEEEE §§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§")
			q_et.put("pause_OK") # on acquite la demande de pause
			flag_run = False # on baisse le flag
		if o == "dmd_run" and not flag_run: # on reçoit une demande de run on n'était pas en run
			q_et.put(" £££££££££££££££££££££££££££££££££££££££££££££  RUN ££££££££££££££££££££££££££££££££££££££££££££££")
			q_et.put("run_OK") # on signale qu'on passe en run
			flag_run = True # on lève le flag
			t0 = time.time()
		# échanges avec le processus Enfant
		#print("échange avec processus enfant, index = {}".format(index))#pour debug
		if (len(bout_feuille)<=1):
			for i in range(1,Tampon+1):
				if flag_run: # on est en run, on envoie les sons
					(ligne, infos_ligne) = fournir_ligne(index, sequences, journaux)
					if len(infos_ligne)>0:
						q_et.put("ligne")
						q_et.put(ligne)
						q_et.put(infos_ligne)
				else: 
					ligne =[]
				#print("index={};ligne={}".format(index,ligne))#ajtp
				bout_feuille.append(ligne)
				index+=1
		e=""
		msg_seq = ""
		#try:
		while qe.empty() == False:
			t0 = time.time()
			e=qe.get(False)
			if (e=="dmd_data") and not flag_arret: #si demande d'arret, on ne répond pas
				for i in range(1,min(Tampon+1,len(bout_feuille))):
					d = bout_feuille.pop(0)	
					qd.put(d)
				# if fanion == 1: #ajtp
				# 	top_inter3 = time.time()
				# 	q_et.put("top_inter3 : {}".format(top_inter3))
				# 	fanion = 2
			msg_seq += "message_sequenceur :"+e +"\n"
			q_et.put(msg_seq)
		# except queue.Empty:
		# 	pass
		
		# Watchdog
		t1 = time.time()
		if t1 - t0 > 5 and flag_run :
			q_et.put("WATCHDOG SEQUENCEUR")


	
		#time.sleep(0.5)
	psequenceur.join()
	q_et.put("\n \n ****** Fin processus Fournisseur *********")
	# print("\n \n ****** Fin processus fournir son *********")

if __name__ == "__main__":
	### programme de test
	ctx = mp.get_context('spawn')
	q_instrum = ctx.Queue() 
	q_etap = ctx.Queue()
	q_recet = ctx.Queue()
	q_ordre = ctx.Queue()
	q_etat = ctx.Queue()
	pfournisseur = ctx.Process(target=fournir_sons, args=(q_instrum,q_etap,q_recet,q_ordre,q_etat))
	pfournisseur.start()
	# Lancement du processus fournissant des feuilles au séquenceur
	instruments = ["test_horloge"]# à modifier suivants fichiers présents dans le Scapi
	q_instrum.put(instruments)
	q_ordre.put("init")

	etapes = ["1C"]# à modifier suivants fichiers présents dans le Scapi
	recettes = ["recette_normal"]#  à modifier suivants fichiers présents dans le Scapi "ryth_solo"
	# etape = input("étape en cours ?")
	# recette = input("recette en cours ?")
	# print("instrument \"{}\" etape en cours : {}".format(instrum,etape))
	# print("instrument \"{}\" recette en cours : {}".format(instrum,recette))
	q_etap.put(etapes)
	q_recet.put(recettes)
	q_ordre.put("nouvelle_etape")
	e=""
	flg1 = False
	flg2 = False
	t_init = time.time()
	while e!="termine" or e!="WATCHDOG SEQUENCEUR":
		try:
			e=q_etat.get(False)
			#os.system('clear')
			print(e)
			if e =="ligne":
				line=q_etat.get()
				newsline=q_etat.get()[0]
				print("##################### line ###################\n{}".format(line)) # pour debug
				print("##################### newsline ###################\n{}".format(newsline)) # pour debug
		except queue.Empty:
			pass
		t_actu = time.time()
		if t_actu-t_init > 10 and not flg1:
			q_ordre.put("dmd_pause")
			flg1 = True # un seul envoi
		if t_actu - t_init > 15 and not flg2:
			q_ordre.put("dmd_arret")
			flg2 = True # un seul envoi
		time.sleep(0.001)
		
	pfournisseur.join()
	# print("\n \n ****** Fin fournisseur *********")
