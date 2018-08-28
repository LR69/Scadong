import csv

def import_csv(fichier, colonnes):
	""" importe un fichier .csv et le retourne sous forme de liste
		Version 2 (modifiée le 29/10/17 par LR
		"""
	liste=[]
	with open(fichier,'r',encoding='utf-8-sig') as csvfile:	
		# encoding 'utf-8-sig' : pour résoudre les problèmes de u'\xa0' et u'\ufeff' liés à l'export avec BOM
		reader = csv.DictReader(csvfile)
		for row in reader:
			nom=[valeur for label,valeur in row.items() if label==colonnes[0]][0]
			#if nom!="": # pour debug
				#print("nom={}".format(nom)) # pour debug
				#input("bingo")  # pour debug
			if ((nom)!="nc" and nom!=""):# pour ignorer les lignes sans signification
				liste.append(row) 
				#print("on ajoute le nom à la liste")  # pour debug
				#print("liste:{}".format(liste))
	# remplacement des "," par des "."
	# print("liste finale:{}".format(liste)) #pour debug
	for element in liste:
		try:
			for colonne in colonnes:
				element[colonne]=element[colonne].replace(",",".")
		except KeyError:
			print("la colonne '{}' n'est pas définie dans le fichier '{}'".format(colonne, fichier))
			raise

	# print(liste) #pour débug
	return liste

	
def export_csv(nouveau_fichier, inventaire, colonnes):
	with open(nouveau_fichier, 'w',newline="\n", encoding=None) as csvfile:
		writer = csv.DictWriter(csvfile, fieldnames=colonnes)
		writer.writeheader()
		for row in inventaire:
			writer.writerow(row)

# test d'import
if __name__ == "__main__":
	colonnes_filtres=['nom du filtre','Durée mini (sec)','Durée maxi (sec)','Motcle 1','Motcle 2','Motcle 3','Motcle 4','Motcle 5','Motcle 6','Motcle 7','Motcle 8','Motcle 9','Motcle 10','Motcle 11','Motcle 12','Motcle 13','Motcle 14','Motcle 15','Motcle 16','Motcle 17','Motcle 18','Nuance 1','Nuance 2','Nuance 3','Nuance 4','Nuance 5','Nuance 6','Nuance 7','Attaque 1','Attaque 2','Attaque 3','Relâchement 1','Relâchement 2','Relâchement 3','Note Fondamental 1','Note Fondamental 2','Note Fondamental 3','Note Fondamental 4','Note Fondamental 5','Note Fondamental 6','Note Fondamental 7','Note Fondamental 8','Note Fondamental 9','Note Fondamental 10','Note Fondamental 11','Note Fondamental 12','Note Fondamental 13','Phrase Musical?','Phrasé','note dans l\'Accord 1','note dans l\'Accord 2','note dans l\'Accord 3','note dans l\'Accord 4','note dans l\'Accord 5','note dans l\'Accord 6','note dans l\'Accord 7','note dans l\'Accord 8','note dans l\'Accord 9','note dans l\'Accord 10','note dans l\'Accord 11','note dans l\'Accord 12','Tempo min','Tempo max','Variation de Tempo','priorité (de 0 à 100)']
	liste_filtres = import_csv("fichiers_csv/filtres.csv", colonnes_filtres) # import csv des réceptivités
	print(liste_filtres)
	for element in liste_filtres:
		for colonne in colonnes_filtres:
			a=element[colonne]
			print("{} est de type{}".format(a,type(a)))
	print("\n \n ****** Fin *********")
