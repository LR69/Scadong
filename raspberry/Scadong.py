# Normalement il faudrait ici définir l'objectif et les fonctionnalités de ce programme "Scadong"
# Mais là, vraiment, cela prendrait trop de place...
# Pour tout renseignement contacter Anthony CLERC à thyonan1 <thyonan1@hotmail.fr>
# 21/11/17 : ajout des communications réseau via des sockets. Scadong joue le rôle de serveur.
# 12/04/18 : bug problèmes de pas
# 25/07/18 ajout de la connexion à la base de données
# 19/08/18 modification de l'initialisation de la base de donnée : peut-être appelée par l'interface web
# 28/08/18 prise en compte des différentes options de lancement (--run, --camera, --loglevel)
#			si loglevel = 0 : log comprend les initialisation, démarrage, et changements de mode
#			si loglevel = 1 : log comprend la même chose que 0 +  les changements d'étapes + sons joués
#			si loglevel = 2 : log comprend la même chose que 1 +  les messages du fournisseurs

import grafcet
import fournisseur
import os
import time
import multiprocessing as mp
import queue
import mysql.connector
from datetime import datetime
import argparse 



# récupération des options de commande
parser = argparse.ArgumentParser()
parser.add_argument("-r", "--run", help="demarrage directement en run du programme Scadong",action="store_true")
parser.add_argument("-c", "--camera", help="demarrage avec prise en charge de la camera",action="store_true")
parser.add_argument("--loglevel", type = int,  choices = range(0,3), help="niveau moyen d'enregistrement des logs (0 : mini ; 2 : maxi)",)

args = parser.parse_args()

if args.camera:
	import PiEye

if args.loglevel == None:
	args.loglevel = 0

def initialisation_BDD():
	""" Connexion à la base de donnée SQL et insertion des instruments dans la BDD """
	try:
		conn=mysql.connector.connect(host="192.168.1.100",user="scapi", password="scapi", database="Scadong")
		cursor = conn.cursor()
		#effacement des bases de données initiales
		ref=(num_Scapi,)
		cursor.execute("""SELECT Son_nom FROM Scapi_sons WHERE Scapi_id=%s; """,ref)
		rows = cursor.fetchall()
		print(" les sons initialement présents :\n {}".format(rows))
		for row in rows:
			cursor.execute(""" DELETE FROM Sons WHERE nom_du_son = %s;""",row)
		cursor.execute(""" DELETE FROM Scapi_sons WHERE Scapi_id = %s;""",ref)
		cursor.execute(""" DELETE FROM Instrument WHERE Scapi_id = %s;""",ref)

		for g7 in grafcets:
			# mise à jour de la table des instruments
			print("g7.nom={}, num_Scapi={}, g7.typeG7={}".format(g7.nom, num_Scapi, g7.typeG7))
			instrum = (g7.nom, num_Scapi, g7.typeG7, 0.0)
			cursor.execute(""" INSERT INTO Instrument VALUES(%s, %s, %s, NULL, NULL, NULL, NULL, NULL, NULL, %s);""",instrum)
			# mise à jour de la liste des sons
			fichier_des_sons = "/home/pi/Scadong/raspberry/fichiers_csv/" + g7.nom + "_id_son.csv"
			ref = (fichier_des_sons, ',' , '\r\n', 1)
			cursor.execute(""" LOAD DATA LOCAL INFILE %s INTO TABLE Sons FIELDS TERMINATED BY %s LINES TERMINATED BY %s IGNORE %s LINES; """,ref)
		# mise à jour de la table des fichiers sons présents dans le scapi
		cursor.execute("""SELECT nom_du_son FROM Sons; """)
		rows = cursor.fetchall()
		chemin_sons="fichiers_sons/" 
		liste_fichiers_sons = os.listdir(chemin_sons)
		noms_sons =[fichier.rpartition(".")[0] for fichier in liste_fichiers_sons] #liste des sons présents dans le dossier liste_fichiers_sons
		#print(noms_sons) #pour debug
		for row in rows:
			#print("le son {}".format(row[0])) #pour debug
			if row[0] in noms_sons:
				#print("est présent dans la liste") #pour debug
				scapi_son = (num_Scapi, row[0])
				cursor.execute(""" INSERT INTO Scapi_sons VALUES( NULL,%s, %s);""",scapi_son)
		scapi_mode_update = ("pause",num_Scapi)
		cursor.execute(""" UPDATE Scapi SET mode=%s WHERE id=%s;""",scapi_mode_update) 
		conn.commit()

		Cnx = True
	except mysql.connector.errors.InterfaceError as e:
		Cnx = False
		print("Error %d: %s" % (e.args[0],e.args[1]))
		pass
	finally:
		# On ferme la connexion
		if conn:
			conn.close()
		return Cnx

def recup_consign_BDD():
	""" récupération des consignes provenant de la BDD """
	mode_pi = "run" # si pas de connexion avec le serveur, on lance quand même le programme.
	motBP=0
	try:
		conn=mysql.connector.connect(host="192.168.1.100",user="scapi", password="scapi", database="Scadong")
		cursor = conn.cursor()
		cursor.execute("""SELECT mode,cmde_BP FROM Scapi WHERE id=%s;""",[num_Scapi])
		tab = cursor.fetchall()
		#print(tab) # pour debug
		if len(tab)>0:
			if len(tab[0])>1:
				mode_pi = tab[0][0]
				motBP = tab[0][1]
	except mysql.connector.errors.InterfaceError as e:
		print("Error %d: %s" % (e.args[0],e.args[1]))
		pass
	finally:
		# On ferme la connexion
		if conn:
			conn.close()
		cons_BPa = motBP & 1
		cons_BPb = motBP>>1 & 1
		cons_BPc = motBP>>2 & 1
		return (mode_pi,cons_BPa,cons_BPb,cons_BPc)

def env_data_BDD(mt_IO, mvt, mde, consBPa,consBPb, consBPc):
	""" acquittement des consignes provenant de la BDD et écritures des entrées du Scadong """
	consBP = consBPc << 2 | consBPb <<1 | consBPa
	mvt_str = "{:.1f}".format(mvt)
	try:
		conn=mysql.connector.connect(host="192.168.1.100",user="scapi", password="scapi", database="Scadong")
		cursor = conn.cursor()
		scapi_update = (mt_IO, mvt_str, mde, consBP, num_Scapi)
		# on envoie aussi l'heure du serveur, et pas celle du Scapi, car le but est de comporer les temps pour déterminer l'inactivité du Scapi
		cursor.execute(""" UPDATE Scapi SET ETOR=%s, mvmt=%s, time=NOW(), mode_acquit=%s, cmde_BP_acquit = %s WHERE id=%s;""",scapi_update) 
		conn.commit()
		Cnx = True
	except mysql.connector.errors.InterfaceError as e:
		Cnx = False
		print("Error %d: %s" % (e.args[0],e.args[1]))
		pass
	finally:
		# On ferme la connexion
		if conn:
			conn.close()
		return (Cnx)

def maj_instrums_BDD(instrs, etaps, recets,ligne_infos):
	""" mises à jour des étapes et recettes en cours des différents instruments """
	try:
		conn=mysql.connector.connect(host="192.168.1.100",user="scapi", password="scapi", database="Scadong")
		cursor = conn.cursor()
		for instr in instrs:
			i = instrs.index(instr)
			etap = etaps[i]
			recet = recets[i]
			instrum_update = (etap,recet,instr)
			cursor.execute(""" UPDATE Instrument SET etape_en_cours=%s, recette_en_cours=%s WHERE nom_instrum=%s;""",instrum_update)
			if len(ligne_infos)>i:
				if len(ligne_infos[i])>0:
					sequenc = ligne_infos[i][0][0]
					trig = ligne_infos[i][0][1]
					filtr = ligne_infos[i][0][2]
					fich_son = ligne_infos[i][0][3]
					volu = ligne_infos[i][0][4]
					instrum_update = (sequenc,trig,filtr,fich_son,volu,instr)
					cursor.execute(""" UPDATE Instrument SET sequence_en_cours=%s, trig_en_cours=%s, filtre_en_cours=%s, Son_nom=%s, volume_en_cours =%s WHERE nom_instrum=%s;""",instrum_update)
		conn.commit()
		Cnx = True
	except mysql.connector.errors.InterfaceError as e:
		Cnx = False
		print("Error %d: %s" % (e.args[0],e.args[1]))
		pass
	finally:
		# On ferme la connexion
		if conn:
			conn.close()
		return (Cnx)


# Programme Principal
if __name__ == "__main__":
	# initialisation de la caméra
	if args.camera:
		Oeil=PiEye.PiEye() # initialisation de la caméra
	# première acquisition des entrées TOR
	mot_IO = 0
	mot_IO = grafcet.AcquisitionETOR(mot_IO)
	chemin="fichiers_csv/" 
	### initialisation des grafcets
	chemin="fichiers_csv/" 
	mode="normal" # "debug" ou "normal"
	#récupération du numéro de Scapi
	hstnme=open("/etc/hostname",'r')
	nom_rpi=hstnme.read().rstrip()
	num_Scapi = int(nom_rpi[len(nom_rpi)-1])
	# inventaire des grafcets à créer sur la base des fichiers déposés
	liste_fichiers = os.listdir(chemin)
	fin ="conditions.csv"
	noms_instruments =[fichier.rpartition("_")[0] for fichier in liste_fichiers if fichier.endswith(fin)]
	presentement = datetime.now()
	presentement_date = presentement.strftime("%d/%m/%y")
	presentement_heure = presentement.strftime("%H:%M:%S")
	# création du fichier de logs
	with open("Scadong.log",'w') as log:
		log.write("Fichier de log du programme scadong lancé le {} à {}, heure du raspberry concerné : {}\n\n". format(presentement_date,presentement_heure,nom_rpi))
		log.write("Programme lancé avec les options suivantes : \n\t\t- mode run :{}\n\t\t- mode camera:{}\n\t\t- loglevel:{}".format(args.run, args.camera, args.loglevel))
		log.write("\nLa lecture des fichiers *.csv a permis d'inventorier les instruments suivants :\n")
		log.write(str(noms_instruments))

	# création des grafcets
	grafcets=[]
	for nom_instrum in noms_instruments:
		fichier_type = chemin+nom_instrum+"_"+"type.csv"
		fichier_etapes = chemin+nom_instrum+"_"+"etapes.csv"
		fichier_conditions = chemin+nom_instrum+"_"+"conditions.csv"
		fichier_transitions = chemin+nom_instrum+"_"+"transitions.csv"
		g7=grafcet.Grafcet(nom_instrum,fichier_type, fichier_etapes, fichier_conditions, fichier_transitions, mode)
		grafcets.append(g7)
	# initialisation des grafcets
	msg=""
	for g7 in grafcets:
		g7.start_init()
		msg+="\n On crée et on initialise le grafcet {}\n".format(g7.nom)
		
	# initialisation des instruments dans la base de donnée SQL
	if not args.run:
		BDD_rdy=initialisation_BDD()
		with open("Scadong.log",'a') as log:
			log.write(msg)
			log.write("\n Base de donnée correctement initialisée : {}\n".format(BDD_rdy))
	
	
	# mode par défaut : run
	mode_Scapi = "run"

	### processus fournissant les sons 
	ctx = mp.get_context('spawn')
	q_instrum = ctx.Queue() 
	q_etap = ctx.Queue()
	q_recet = ctx.Queue()
	q_ordre = ctx.Queue()
	q_etat = ctx.Queue()
	pfournisseur = ctx.Process(target=fournisseur.fournir_sons, args=(q_instrum,q_etap,q_recet,q_ordre,q_etat))
	pfournisseur.start()
	# Lancement du processus fournissant des feuilles au séquenceur
	q_instrum.put(noms_instruments)
	q_ordre.put("init")
	#cycle automate
	e=""
	mode_Scapi=""
	flag_run = True
	flag_run_send = False
	flag_pause_send = False
	t0=datetime.now()
	format_date = "%d/%m/%y %H:%M:%S"
	with open("Scadong.log",'a') as log:
		log.write("\nOn démarre le cycle automate à :{}, t={}\n".format(t0.strftime(format_date),time.time()))
	while e!="termine" and mode_Scapi!="stop" :
		if mode_Scapi=="init" and not args.run:
			# initialisation des instruments dans la base de donnée SQL
			BDD_rdy=initialisation_BDD()
			with open("Scadong.log",'a') as log:
				log.write(msg)
				log.write("\n {} : Base de donnée correctement initialisée : {}\n".format(time.time(),BDD_rdy))
		msg_log=""

		# acquistion caméra
		if args.camera:
			mouvement = Oeil.voir()
		else:
			mouvement = 0
		if args.loglevel>0:
			msg_log+="\n\n\nt = {}\n".format(time.time())
			msg_log+="\t mouvement = {:.1f}\n".format(mouvement)
		# acquisition des entrées TOR
		mot_IO = grafcet.AcquisitionETOR(mot_IO)
		if args.loglevel>0:
			msg_log+="\t mot_IO = {}\n".format(mot_IO)
		#récupération des consignes du serveur
		if args.run:
			mode_Scapi = "run"
		else:
			(mode_Scapi,consigne_BPa,consigne_BPb,consigne_BPc)=recup_consign_BDD()

			# acquitement et recopie des entrées du pi (GPIO et mvmt) sur le serveur 
			BDD_rdy=env_data_BDD(mot_IO,mouvement,mode_Scapi, consigne_BPa, consigne_BPb, consigne_BPc)
			if args.loglevel>0:
				msg_log+="\t consignes BDD : mode_Scapi = {},consigne_BPa = {},consigne_BPb ={},consigne_BPc={}\n".format(mode_Scapi,consigne_BPa,consigne_BPb,consigne_BPc)
				msg_log+="Message Base de donnée correctement acquittée: {} \n".format(BDD_rdy)
		# gestion des modes de marche
		if mode_Scapi == "run": # pas d'évolution du grafcet si pas en run
			if not flag_run and not flag_run_send: # si le séquenceur n'était pas en run
				q_ordre.put("dmd_run") # on demande le passage en run du séquenceur
				t1=datetime.now()
				msg_log+="\n\n {} :".format(t1.strftime(format_date))
				msg_log+="!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! ON DEMANDE LE PASSAGE EN RUN $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$\n\n"
				flag_run_send = True
		else:
			if flag_run and not flag_pause_send: # si on était en run
				t2=datetime.now()
				msg_log+="\n\n {} :".format(t2.strftime(format_date))
				msg_log+="\n\n??????????????????????????????????????? ON DEMANDE LE PASSAGE EN PAUSE §§§§§§§§§§§§§§§§§§§§§§§§§§§§§§\n\n"
				q_ordre.put("dmd_pause") #on demande au séquenceur de passer en pause
				flag_pause_send = True
		#scrutation des grafcets
		etapes=[]
		recettes=[]
		line=[]
		newsline=[]
		if args.loglevel>0:
			msg_log+="scrutation des grafcets :\n"
		for g7 in grafcets:
			if mode_Scapi == "run":
				g7.scrutation(mouvement,mot_IO) 
				etapes.append(g7.etape)
				recettes.append(g7.recette)
			if args.loglevel>0:
				msg_log+="grafcet {} de type {}:\n".format(g7.nom, g7.typeG7)
				msg_log+="\t l'étape en cours est : {}\n".format(g7.etape)
				msg_log+="\t la recette en cours est : {}\n".format(g7.recette)
		# actions
		if mode_Scapi == "run": # pas d'évolution du grafcet si pas en run
			q_etap.put(etapes)
			q_recet.put(recettes)
			q_ordre.put("nouvelle_etape")
		# recupération messages processus fournisseur
		e="rien pour le moment"
		while len(e) > 0:
			e=""
			try:
				e=q_etat.get(False)
				if args.loglevel>1:
					msg_log+="\n\n################ début message fournisseur ##############################\n"
					msg_log+=str(e)
				if e =="ligne":
					line=q_etat.get()
					newsline=q_etat.get()#[0]
					if args.loglevel>1:
						msg_log+="line : {}".format(line) # pour debug
						msg_log+="newsline : {}\n".format(newsline) # pour debug
					if not args.run:
						# Mise à jour de la BDD avec l'étape et la recette en cours
						BDD_rdy = maj_instrums_BDD(noms_instruments, etapes, recettes, newsline)
						if args.loglevel>1:
							msg_log+="\n\n mise à jour BDD instruments : {}\n\n".format(BDD_rdy)
				if e == "run_OK":
					flag_run = True
					flag_run_send = False
				if e == "pause_OK":
					flag_run = False
					flag_pause_send = False
			except queue.Empty:
				pass
		# mise à jour fichier de logs
		with open("Scadong.log",'a') as log:
			log.write(msg_log)
		# affichage console
		os.system('clear')
		print("mouvement détecté par la caméra :{:.3f}\n\n\n".format(mouvement))
		print("mot_IO={}".format(mot_IO))
		for g7 in grafcets:
			print("grafcet {} de type {}:".format(g7.nom, g7.typeG7))
			print("\t l'étape en cours est : {}".format(g7.etape))
			print("\t la recette en cours est : {}".format(g7.recette))
		#time.sleep(0.001)
	q_ordre.put("dmd_arret")
	pfournisseur.join()
	presentement = datetime.now()
	presentement_date = presentement.strftime("%d/%m/%y")
	presentement_heure = presentement.strftime("%H:%M:%S")
	with open("Scadong.log",'w') as log:
		log.write("# FIN du programme scadong  le {} à {}, heure du raspberry concerné : {}\n\n". format(presentement_date,presentement_heure,nom_rpi))
	print("\n \n ****** Fin Processus principal *********")
