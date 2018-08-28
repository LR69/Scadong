import re

def remplacer_couleur(line):
	pat = r'#FFFFFF'
	alt = r'#706b64'
	return re.sub(pat,alt,line)


def insert_jinja(line):
	lettres="ABCDEF"
	for i in range(1,9):
		for l in range(0,5):
			pattern = r'bgcolor="#706b64">Recette.*' + str(i) +' &ndash; '+ lettres[l] + r'</td>'
			rempl = r'{% if Recette_Couleur.recette == "R' + str(i) +lettres[l] + r'" %} bgcolor={{Recette_Couleur.couleur}} {% else %} bgcolor="#706b64" {% endif %} >Recette ' + str(i) + lettres[l] + r'</td>'
			line=re.sub(pattern,rempl,line)
	return line

def arranger_grafcet(chemin,fichier_ini,fichier_modif):
	with open(fichier_modif,'w') as fichier2:
		with open(chemin+"templates/header.html",'r') as header:
			entete = header.read()
			fichier2.write(entete)
		rep='None'
		with open(fichier_ini,'r') as fichier:
			while rep == 'None':
				ligne = fichier.readline()
				pattern = r'^<table'
				res=re.search(pattern,ligne)
				rep=str(res)
			rep = 'None'
	
			while rep == 'None':
				ligne = remplacer_couleur(ligne)
				ligne = insert_jinja(ligne)
				ligne = '\t\t' + ligne
				fichier2.write(ligne)
				ligne = fichier.readline()
				pattern = r'^</table'
				res=re.search(pattern,ligne)
				rep=str(res)
			ligne = '\t\t' + ligne
			remplacer_couleur(ligne)
			insert_jinja(ligne)
			fichier2.write(ligne)
		with open(chemin+"templates/footer.html",'r') as footer:
			piedpage = footer.read()
			fichier2.write(piedpage)

# Programme Principal
if __name__ == "__main__":
	arranger_grafcet("","upload_html/percussion1_grafcet.html","templates/percussion1_grafcet2.html")
