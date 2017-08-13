#""" --- DEFINITION DE LA SUPER CLASSE SON --- """
# Version : 06b
# modficition du 10-08-17 : utilisation boucles for pour déterminer si un son créé est conforme


class Son:
	""" classe définissant les caractéristique d'un son 
	c'est un Super Class mais pourquoi ?
	- Tous les attributs de type liste [], sont capables de "s'autogérer" il n'acceptent pas forcément tout ce qu'on leur donnent, il reffusent ce qui n'est pas inscrit dans leur liste de possibilités 
	- Attention des erreurs peuvet survenir si vous rentrer des variables exemple sample avec une virgule un point ou tout autre chose attacher au nom.Votre paramêtre ne sera alors pas pris en compte
	- Attention pour que les attribut ce gere correctement il  faut impérativement utiliser le code "nom de l'objet de claas Son".add_"attribut"(variable) et non : "nom de l'objet de class Son".attribut = variable
	Attribut :
	- nom : le nom du son (string ou nc)
	- duree : la durée du son en seconde (entier >0 ou -1)
	- motcle : ["nc", "percution", "synthetique", "instrumental", "bruitiste", "voix", "ensemble", "sample", "texte", "soundDesign", "vent", "cuivre", "corde", "metalique", "peau", "bois", "frotte", "pince", "frappe"]
	- nuance : ["nc", "pianissimo", "piano", "mezzo", "forte", "fortissimo", "crescendo", "descrescendo"]
	- att : ["nc", "net", "rapide", "lent"] quel type d'attaque possède le son
	- relachement : ["nc", "net", "rapide", "lent"] quel type de relachement(arret du son) possède le son
	- noteF : ["nc", "bruit", "do", "reb", "re", "mib", "mi", "fa", "solb", "sol", "lab", "la", "sib", "si"]
	- phraseMus : [true(1), false(0), -1]s'agit t-il d'une phrases musical (succession de note) oui / non (booleen)
	- phrase  : ["nc", "lie", "staccato", "tenuNote"] phrasé de la phrase musical 
	- accord : ["nc", "do", "reb", "re", "mib", "mi", "fa", "solb", "sol", "lab", "la", "sib", "si"]
	- tempo : tempo de la phrase (entier >0 ou -1) tempo moyen de la phrase si applicable
	- variTempo : ["nc", "fixe", "accleration", "ralentissement", "chaotique"]

	poss_"x" gère les valeur accepter ou non comme mot clé il est possible d'en rajouter mais les modification doivent être réaliser ci dessus dans le code et non à chaud.
		si on rentre une valeur "x" qui n'est pas inscrite dans poss_"x" alors la valeur n'est pas rajouter à la liste"""

	#""" ---LISTE DES POSSIBILITES --- """	
	poss_motcle=["nc", "percution", "synthetique", "instrumental", "bruitiste", "voix", "ensemble", "sample", "texte", "soundDesign", "vent", "cuivre", "corde", "metalique", "peau", "bois", "frotte", "pince", "frappe"] #  --- LISTE DES POSSIBLES --- motcle
	poss_nuance=["nc", "pianissimo", "piano", "mezzo", "forte", "fortissimo", "crescendo", "descrescendo"] # --- LISTE DES POSSIBLES --- Nuance
	poss_att=["nc", "net", "rapide", "lent"] #  --- LISTE DES POSSIBLES ---  att
	poss_relachement=["nc", "net", "rapide", "lent"] #  --- LISTE DES POSSIBLES --- relachement
	poss_noteF=["nc", "bruit", "do", "reb", "re", "mib", "mi", "fa", "solb", "sol", "lab", "la", "sib", "si"]#  --- LISTE DES POSSIBLES --- noteF
	poss_accord=["nc", "do", "reb", "re", "mib", "mi", "fa", "solb", "sol", "lab", "la", "sib", "si"] # --- LISTE DES POSSIBLES --- accord
	poss_phrase=["nc", "lie", "staccato", "tenuNote"] # --- LISTE DES POSSIBLES --- phrase (phrasé musical)
	poss_variTempo=["nc", "fixe", "accleration", "ralentissement", "chaotique"]  # --- LISTE DES POSSIBLES --- variTempo

	#""" ---INVENTAIRE DES OBJETS CREES--- """
	inventaire=[]
	
	def __init__(self, nom):
		if Son.inventaire.__contains__(nom):
			raise SonExistantError("Création du son {} impossible, un son aillant le même nom existe déjà.\n Veuillez choisir un autre nom.".format(nom))
		else:
			Son.inventaire.append(nom)      
			self._nom = nom
			self._duree = -1
			self._motcle = ["nc"] 
			self._nuance = ["nc"]
			self._att = ["nc"]
			self._relachement = ["nc"]
			self._noteF = ["nc"]
			self._accord = ["nc"]
			self._phraseMus = -1
			self._phrase = ["nc"]
			self._tempo = -1
			self._variTempo = ["nc"]
		
		
		
	
	def add_motcle(self,motcle): 
		""" ajoute un mot clef au son. """

		try:
			motcle = motcle.split()
		except: 
			print("mot(s) clef(s) saisi(s) \"{}\": erreur de format, motcle fixé à [\"nc\"]".format(motcle))
			motcle = ["nc"] # peut être pas super utile ?
			
		if type(motcle) == list :
			for m in motcle:
				if Son.poss_motcle.__contains__(m):
					self._motcle.append(m)
				else:
					print("mot clef \"{}\" incorrect".format(m))

			if len(self._motcle)>1 and self._motcle.__contains__("nc"):
				self._motcle.remove("nc")
			
	
	def add_nuance(self,nuance):
		"""ajoute une nuance au son. """
		

		try:
			nuance = nuance.split()
		except: 
			print("nuance(s) saisie(s) \"{}\": erreur de format, nuance fixée à [\"nc\"]".format(nuance))
			nuance = ["nc"] # peut être pas super utile ?
			
		if type(nuance) == list :
			for m in nuance:
				if Son.poss_nuance.__contains__(m):
					self._nuance.append(m)
				else:
					print("nuance \"{}\" incorrecte".format(m))

			if len(self._nuance)>1 and self._nuance.__contains__("nc"):
				self._nuance.remove("nc")

	
	def add_att(self,att):
		"""ajoute une attaque au son. """
		try:
			att = att.split()
		except: 
			print("attaque(s) saisie(s) \"{}\": erreur de format, attaque fixé à [\"nc\"]".format(att))
			att = ["nc"] # peut être pas super utile ?
			
		if type(att) == list :
			for m in att:
				if Son.poss_att.__contains__(m):
					self._att.append(m)
				else:
					print("attaque \"{}\" incorrecte".format(m))

			if len(self._att)>1 and self._att.__contains__("nc"):
				self._att.remove("nc")
				
	def add_relachement(self,relachement):
		"""ajoute un relâchement au son."""
		try:
			relachement = relachement.split()
		except: 
			print("relâchement(s) saisi(s) \"{}\": erreur de format, relachement fixé à [\"nc\"]".format(relachement))
			relachement = ["nc"] # peut être pas super utile ?
			
		if type(relachement) == list :
			for m in relachement:
				if Son.poss_relachement.__contains__(m):
					self._relachement.append(m)
				else:
					print("relachement \"{}\" incorrect".format(m))

			if len(self._relachement)>1 and self._relachement.__contains__("nc"):
				self._relachement.remove("nc")

				
	def add_noteF(self,noteF):
		"""ajoute une note fondamentale au son."""
		try:
			noteF = noteF.split()
		except: 
			print("Note fondamentale saisie \"{}\": erreur de format, fondamentale fixée à [\"nc\"]".format(noteF))
			noteF = ["nc"] # peut être pas super utile ?
			
		if type(noteF) == list :
			for m in noteF:
				if Son.poss_noteF.__contains__(m):
					self._noteF.append(m)
				else:
					print("note fondamentale \"{}\" incorrecte".format(m))

			if len(self._noteF)>1 and self._noteF.__contains__("nc"):
				self._noteF.remove("nc")

				
	def add_accord(self,accord):
		"""ajoute un accord au son."""
		try:
			accord = accord.split()
		except: 
			print("accord(s) saisi(s) \"{}\": erreur de format, accord fixé à [\"nc\"]".format(accord))
			accord = ["nc"] # peut être pas super utile ?
			
		if type(accord) == list :
			for m in accord:
				if Son.poss_accord.__contains__(m):
					self._accord.append(m)
				else:
					print("accord \"{}\" incorrect".format(m))

			if len(self._accord)>1 and self._accord.__contains__("nc"):
				self._accord.remove("nc")

				
	def add_phrase(self,phrase):
		"""ajoute une phrase au son."""
		try:
			phrase = phrase.split()
		except: 
			print("phrase(s) saisie(s) \"{}\": erreur de format, phrase fixée à [\"nc\"]".format(phrase))
			phrase = ["nc"] # peut être pas super utile ?
			
		if type(phrase) == list :
			for m in phrase:
				if Son.poss_phrase.__contains__(m):
					self._phrase.append(m)
				else:
					print("phrase \"{}\" incorrecte".format(m))

			if len(self._phrase)>1 and self._phrase.__contains__("nc"):
				self._phrase.remove("nc")

				
	def add_variTempo(self,variTempo):
		"""ajoute une variation de tempo au son."""
		try:
			variTempo = variTempo.split()
		except: 
			print("variation tempo(s) saisie(s) \"{}\": erreur de format, variTempo fixé à [\"nc\"]".format(variTempo))
			variTempo = ["nc"] # peut être pas super utile ?
			
		if type(variTempo) == list :
			for m in variTempo:
				if Son.poss_variTempo.__contains__(m):
					self._variTempo.append(m)
				else:
					print("Variation Tempo \"{}\" incorrecte".format(m))

			if len(self._variTempo)>1 and self._variTempo.__contains__("nc"):
				self._variTempo.remove("nc")
			
			
			
	#""" --- Variable de la class Son qui n'ont pas de liste --- """
	
	
	def add_duree(self, duree) :
		if type(duree) != int :
			try: 
				duree = int(duree)
			except:
				duree = -1
		if type(duree) == int :
			self._duree = duree
				
				
	def add_phraseMus(self,phraseMus) :
			if phraseMus != 0 and phraseMus != 1 : # si phraseMus n'est pas un booleen
				try :
					phraseMus = int(phraseMus)
				except :	
					self._phraseMus = -1
			if phraseMus ==  0 or phraseMus == 1: 
				self._phraseMus = phraseMus
				
	
	def add_tempo(self,tempo) :
		if type(tempo) != int :
			try :
				tempo = int(tempo)
			except:
				tempo = -1
		if type(tempo) == int :
			self._tempo = tempo
			
	
	
	#""" --- Représentation Des Objets De La Class Son ---"""
	
	
	def __repr__(self):
		""" représentation de notre objet dans l'interpreteur pour debug et vérif"""
		return "nom : {}\
		\nduree : {}\
		\nmotcle : {}\
		\nnuance : {}\
		\natt : {}\
		\nrelachement : {}\
		\nnoteF : {}\
		\naccord : {}\
		\nphraseMus : {}\
		\nphrase : {}\
		\ntempo : {}\
		\nvariTempo : {}\n".format(self._nom, self._duree, self._motcle, self._nuance, self._att, self._relachement, self._noteF, self._accord, self._phraseMus, self._phrase, self._tempo, self._variTempo)
		
class SonExistantError(Exception):
	""" Exception qui est levée quand on cherche à instancier un son avec un nom déjà existant """
	def __init__(self, message):
		""" stockage du message d'erreur """
		self.message = message
	def __str__(self):
		""" on renvoie le message """
		return self.message

