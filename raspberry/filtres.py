""" Module "Filtres" contenant toutes les fonctions de filtrage des sons"""

def filtre_duree(inventaire, mini, maxi):
	""" fonction retournant la liste des sons de l'inventaire dont la durée est comprise entre mini et maxi"""
	resultat2 = [element for element in inventaire if element["Durée (sec)"].isdigit()] #on vérifie qu'il s'agit bien d'un nombre
	resultat=[element for element in resultat2 if (int(element["Durée (sec)"])>= mini and int(element["Durée (sec)"])<= maxi)]
	return resultat

def filtre_motcle(inventaire, texte_cherche):
	""" fonction retournant la liste des sons de l'inventaire contenant le texte cherché dans les mots clés"""
	resultat=[]
	for i in range(1,18): # 18 mots clés de "Motcle 1" à "Motcle 18" 
		key = 'Motcle '+str(i)
		resultat2 = [element for element in inventaire if element[key].__contains__(texte_cherche)]
		if resultat2 != []: # on évite de rajouter des listes vides
			resultat.extend(resultat2)
	return resultat

def filtre_nuance(inventaire, texte_cherche):
	""" fonction retournant la liste des sons de l'inventaire contenant le texte cherché dans les nuances"""
	resultat=[]
	for i in range(1,7): # 7 nuances de "Nuance 1" à Nuance 7" 
		key = 'Nuance '+str(i)
		resultat2 = [element for element in inventaire if element[key].__contains__(texte_cherche)]
		if resultat2 != []: # on évite de rajouter des listes vides
			resultat.extend(resultat2)
	return resultat

def filtre_attaque(inventaire, texte_cherche):
	""" fonction retournant la liste des sons de l'inventaire contenant le type d'attaque cherchée"""
	resultat=[]
	for i in range(1,3): # 3 attaques de "Attaque 1" à "Attaque 3" 
		key = 'Attaque '+str(i)
		resultat2 = [element for element in inventaire if element[key].__contains__(texte_cherche)]
		if resultat2 != []: # on évite de rajouter des listes vides
			resultat.extend(resultat2)
	return resultat

def filtre_relachement(inventaire, texte_cherche):
	""" fonction retournant la liste des sons de l'inventaire contenant le type de relâchement cherchée"""
	resultat=[]
	for i in range(1,3): # 3 relâchements de "Relâchement 1" à "Relâchement 3"
		key = 'Relâchement '+str(i)
		resultat2 = [element for element in inventaire if element[key].__contains__(texte_cherche)]
		if resultat2 != []: # on évite de rajouter des listes vides
			resultat.extend(resultat2)
	return resultat

def filtre_noteF(inventaire, texte_cherche):
	""" fonction retournant la liste des sons de l'inventaire contenant la note fondamentale cherchée"""
	resultat=[]
	for i in range(1,13): # 13 notes fondamentales de "Note Fondamental 1" à "Note Fondamental 13"
		key = 'Note Fondamental '+str(i)
		resultat2 = [element for element in inventaire if element[key].__contains__(texte_cherche)]
		if resultat2 != []: # on évite de rajouter des listes vides
			resultat.extend(resultat2)
	return resultat

def filtre_phraseMus(inventaire):
	""" fonction retournant la liste des sons de l'inventaire ayant un phrasé musical"""
	resultat=[element for element in inventaire if element['Phrase Musical ?'] == "True"]
	return resultat

def filtre_not_phraseMus(inventaire):
	""" fonction retournant la liste des sons de l'inventaire n'ayant pas un phrasé musical"""
	resultat=[element for element in inventaire if element['Phrase Musical ?'] == "False"]
	return resultat

def filtre_phrase(inventaire, texte_cherche):
	""" fonction retournant la liste des sons de l'inventaire correspondant à un phrasé donné (staccato, lié,...) """
	resultat=[element for element in inventaire if element['Phrasé'] == texte_cherche]
	return resultat

def filtre_accord(inventaire, texte_cherche):
	""" fonction retournant la liste des sons de l'inventaire contenant la note dans l'accord cherchée"""
	resultat=[]
	for i in range(1,12): # 12 notes dans l'accord de "note dans l'Accord 1" à "note dans l'Accord 12"
		key = 'note dans l\'Accord '+str(i)
		resultat2 = [element for element in inventaire if element[key].__contains__(texte_cherche)]
		if resultat2 != []: # on évite de rajouter des listes vides
			resultat.extend(resultat2)
	return resultat

def filtre_tempo(inventaire, mini, maxi):
	""" fonction retournant la liste des sons de l'inventaire dont le tempo est compris entre mini et maxi"""
	for element in inventaire:
		digts=element["Tempo"].replace(".","")
		if not digts.isdigit():
			element["Tempo"]="0.0"
	resultat=[element for element in inventaire if (float(element["Tempo"])>= mini and float(element["Tempo"])<= maxi )] #on vérifie qu'il s'agit bien d'un nombre
	return resultat

def filtre_variTempo(inventaire, texte_cherche):
	""" fonction retournant la liste des sons ayant la variation de tempo (accélération, déccélération,...) recherchée """
	if texte_cherche == "":
		texte_cherche = "nc"
	resultat=[element for element in inventaire if element['Variation de Tempo'] == texte_cherche]
	return resultat

def filtrage(liste_sons_1,filtre):
	colonnes_filtres=['nom du filtre','Durée mini (sec)','Durée maxi (sec)','Motcle 1','Motcle 2','Motcle 3','Motcle 4','Motcle 5','Motcle 6','Motcle 7','Motcle 8','Motcle 9','Motcle 10','Motcle 11','Motcle 12','Motcle 13','Motcle 14','Motcle 15','Motcle 16','Motcle 17','Motcle 18','Nuance 1','Nuance 2','Nuance 3','Nuance 4','Nuance 5','Nuance 6','Nuance 7','Attaque 1','Attaque 2','Attaque 3','Relâchement 1','Relâchement 2','Relâchement 3','Note Fondamental 1','Note Fondamental 2','Note Fondamental 3','Note Fondamental 4','Note Fondamental 5','Note Fondamental 6','Note Fondamental 7','Note Fondamental 8','Note Fondamental 9','Note Fondamental 10','Note Fondamental 11','Note Fondamental 12','Note Fondamental 13','Phrase Musical ?','Phrasé','note dans l\'Accord 1','note dans l\'Accord 2','note dans l\'Accord 3','note dans l\'Accord 4','note dans l\'Accord 5','note dans l\'Accord 6','note dans l\'Accord 7','note dans l\'Accord 8','note dans l\'Accord 9','note dans l\'Accord 10','note dans l\'Accord 11','note dans l\'Accord 12','Tempo min','Tempo max','Variation de Tempo','priorité (de 0 à 100)']

	# filtrage suivant la durée
	liste_sons_2= filtre_duree(liste_sons_1,float(filtre['Durée mini (sec)']),float(filtre['Durée maxi (sec)']))
	liste_sons_1= liste_sons_2
	#print("filtre durée:{}".format(len(liste_sons_2)))

	
	# filtrage suivant les mot clefs
	j=0
	for i in range(1,18): # 18 mots clés de "Motcle 1" à "Motcle 18" 
		key = 'Motcle '+str(i)
		if (filtre[key] != "" and filtre[key] != "nc"):
			#print(key) # pour debug
			#print(filtre[key]) # pour debug
			if(j%2==1):
				liste_sons_2 = filtre_motcle(liste_sons_1, filtre[key])
				#sortie="sortie = liste_sons_2" # pour debug
			else:
				liste_sons_1 = filtre_motcle(liste_sons_2, filtre[key])
				#sortie="sortie = liste_sons_1" # pour debug
			j+=1
			#print(j) # pour debug
	#print(sortie)
	if(j%2==0):
		liste_sons_1=liste_sons_2 
		#print("interversion")
	else:
		liste_sons_2=liste_sons_1
	#print("filtre mots clé:{}".format(len(liste_sons_2)))
	

	# filtrage suivant les nuances
	j=0
	for i in range(1,7): # 7 nuances de "Nuance 1" à "Nuance 7" 
		key = 'Nuance '+str(i)
		if (filtre[key] != "" and filtre[key] != "nc"):
			#print(key) # pour debug
			#print(filtre[key]) # pour debug
			if(j%2==1):
				liste_sons_2 = filtre_nuance(liste_sons_1, filtre[key])
				#sortie="sortie = liste_sons_2" # pour debug
			else:
				liste_sons_1 = filtre_nuance(liste_sons_2, filtre[key])
				#sortie="sortie = liste_sons_1" # pour debug
			j+=1
			#print(j) # pour debug
	#print(sortie)
	if(j%2==0):
		liste_sons_1=liste_sons_2 
		#print("interversion")
	else:
		liste_sons_2=liste_sons_1
	#print("filtre nuance:{}".format(len(liste_sons_2)))
	
	
	# filtrage suivant les attaques
	j=0
	for i in range(1,3): # 3 Attaques de "Attaque 1" à "Attaque 3" 
		key = 'Attaque '+str(i)
		if (filtre[key] != "" and filtre[key] != "nc"):
			#print(key) # pour debug
			#print(filtre[key]) # pour debug
			if(j%2==1):
				liste_sons_2 = filtre_attaque(liste_sons_1, filtre[key])
				#sortie="sortie = liste_sons_2" # pour debug
			else:
				liste_sons_1 = filtre_attaque(liste_sons_2, filtre[key])
				#sortie="sortie = liste_sons_1" # pour debug
			j+=1
			#print(j) # pour debug
	#print(sortie)
	if(j%2==0):
		liste_sons_1=liste_sons_2 
		#print("interversion")
	else:
		liste_sons_2=liste_sons_1
	#print("filtre attaques:{}".format(len(liste_sons_2)))
	
	
	# filtrage suivant les relachements
	j=0
	for i in range(1,3): # 3 relâchements de "Relâchement 1" à "Relâchement 3"
		key = 'Relâchement '+str(i)
		if (filtre[key] != "" and filtre[key] != "nc"):
			#print(key) # pour debug
			#print(filtre[key]) # pour debug
			if(j%2==1):
				liste_sons_2 = filtre_relachement(liste_sons_1, filtre[key])
				#sortie="sortie = liste_sons_2" # pour debug
			else:
				liste_sons_1 = filtre_relachement(liste_sons_2, filtre[key])
				#sortie="sortie = liste_sons_1" # pour debug
			j+=1
			#print(j) # pour debug
	#print(sortie)
	if(j%2==0):
		liste_sons_1=liste_sons_2 
		#print("interversion")
	else:
		liste_sons_2=liste_sons_1
	#print("filtre relachement:{}".format(len(liste_sons_2)))
	
	
	# filtrage suivant la note fondamentale
	j=0
	for i in range(1,13): # 13 notes fondamentales de "Note Fondamental 1" à "Note Fondamental 13"
		key = 'Note Fondamental '+str(i)
		if (filtre[key] != "" and filtre[key] != "nc"):
			#print(key) # pour debug
			#print(filtre[key]) # pour debug
			if(j%2==1):
				liste_sons_2 = filtre_relachement(liste_sons_1, filtre[key])
				#sortie="sortie = liste_sons_2" # pour debug
			else:
				liste_sons_1 = filtre_relachement(liste_sons_2, filtre[key])
				#sortie="sortie = liste_sons_1" # pour debug
			j+=1
			#print(j) # pour debug
	#print(sortie)
	if(j%2==0):
		liste_sons_1=liste_sons_2 
		#print("interversion")
	else:
		liste_sons_2=liste_sons_1
	#print("filtre note fondamentale:{}".format(len(liste_sons_2)))
	
	
	# Filtrage suivant le phrasé musical 
	if filtre['Phrase Musical ?']=="True":
		liste_sons_2= filtre_phraseMus(liste_sons_1)
		liste_sons_1= filtre_phrase(liste_sons_2,filtre['Phrasé'])
		liste_sons_2=liste_sons_1
	#print("filtre phrasé:{}".format(len(liste_sons_2)))
	
	# filtrage suivant la note fondamentale dans l'accord
	j=0
	for i in range(1,12): # 12 notes dans l'accord de "note dans l'Accord 1" à "note dans l'Accord 12"
		key = 'note dans l\'Accord '+str(i)
		if (filtre[key] != "" and filtre[key] != "nc"):
			#print(key) # pour debug
			#print(filtre[key]) # pour debug
			if(j%2==1):
				liste_sons_2 = filtre_relachement(liste_sons_1, filtre[key])
				#sortie="sortie = liste_sons_2" # pour debug
			else:
				liste_sons_1 = filtre_relachement(liste_sons_2, filtre[key])
				#sortie="sortie = liste_sons_1" # pour debug
			j+=1
			#print(j) # pour debug
	#print(sortie)
	if(j%2==0):
		liste_sons_1=liste_sons_2 
		#print("interversion")
	else:
		liste_sons_2=liste_sons_1
	#print("filtre note dondamentale:{}".format(len(liste_sons_2)))
	
	# filtrage suivant la tempo
	liste_sons_2= filtre_tempo(liste_sons_1,float(filtre['Tempo min']),float(filtre['Tempo max']))
	liste_sons_1= liste_sons_2
	#print("min:{}".format(float(filtre['Tempo min'])))
	#print("max:{}".format(float(filtre['Tempo max'])))
	#print("filtre tempo:{}".format(len(liste_sons_2)))
	
	
	# filtrage suivant la variation de la tempo 
	#print("variation de la tempo:{}".format(filtre['Variation de Tempo']))
	#print([element['Variation de Tempo'] for element in liste_sons_1])
	liste_sons_2= filtre_variTempo(liste_sons_1,filtre['Variation de Tempo'])
	liste_sons_1=liste_sons_2
	#print("filtre variation de la tempo:{}".format(len(liste_sons_2)))
	
	
	return(liste_sons_2)

	
def test_filtres(inventaire_sons,inventaire_filtres):
	""" test Filtres disponibles """
	print("\n \n liste des sons comportant le mot cle \"clavier\" :")
	print([element['nom du son'] for element in filtre_motcle(inventaire_sons, "clavier")])


	print("\n \n liste des sons dont la durée est comprise entre 3 et 8 secondes :")
	print([element['nom du son'] for element in filtre_duree(inventaire_sons,3,8)])

	print("\n \n liste des sons dont la durée est comprise entre 3 et 8 secondes et contenant le mot cle \"clavier\":")
	print([element['nom du son'] for element in filtre_duree(filtre_motcle(inventaire_sons, "clavier"),3,8)])


	print("\n \n liste des sons dont la nuance est \"piano\" :")
	print([element['nom du son'] for element in filtre_nuance(inventaire_sons, "piano")])


	print("\n \n liste des sons dont l'attaque est \"rapide\" :")
	print([element['nom du son'] for element in filtre_attaque(inventaire_sons, "rapide")])



	print("\n \n liste des sons dont le relâchement est \"net\" :")
	print([element['nom du son'] for element in filtre_relachement(inventaire_sons, "net")])

	print("\n \n liste des sons dont la note fondamentale est \"do\" :")
	print([element['nom du son'] for element in filtre_noteF(inventaire_sons, "do")])

	print("\n \n liste des sons ayant un phrasé musical	 :")
	print([element['nom du son'] for element in filtre_phraseMus(inventaire_sons)])

	print("\n \n liste des sons ayant un phrasé lié	 :")
	print([element['nom du son'] for element in filtre_phrase(filtre_phraseMus(inventaire_sons),"lie")])

	print("\n \n liste des sons dont la note dans l'accord est \"fa\" :")
	print([element['nom du son'] for element in filtre_accord(inventaire_sons, "fa")])

	print("\n \n liste des sons ayant un tempo minimum de 100 fixe :")
	print([element['nom du son'] for element in filtre_tempo(filtre_variTempo(inventaire_sons,"fixe"),100,99999)])
