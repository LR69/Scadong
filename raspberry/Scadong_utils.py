import csv

def import_csv(fichier, colonnes):
	""" importe un fichier .csv et le retourne sous forme de liste
        Version 2 (modifiée le 29/10/17 par LR
        """
	liste=[]
	with open(fichier,'r') as csvfile:	
		reader = csv.DictReader(csvfile)
		for row in reader:
			nom=[valeur for label,valeur in row.items()][0]
			if ((nom)!="nc" and nom!=""):# pour ignorer les lignes sans signification
				liste.append(row)
	# remplacement des "," par des "."
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
	colonnes_conditions=['nom_condition','nombre_lectures_sequence_mini','bouton','seuil_camera_mini','seuil_camera_maxi','temps_attente']
	liste_conditions = import_csv("conditions.csv", colonnes_conditions) # import csv des réceptivités
	print(liste_conditions)
	for element in liste_conditions:
		for colonne in colonnes_conditions:
			a=element[colonne]
			print("{} est de type{}".format(a,type(a)))
	print("\n \n ****** Fin *********")
