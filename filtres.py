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
    resultat2 = [element for element in inventaire if element["Tempo"].isdigit()] #on vérifie qu'il s'agit bien d'un nombre
    resultat=[element for element in resultat2 if (int(element["Tempo"])>= mini and int(element["Tempo"])<= maxi)]
    return resultat

def filtre_variTempo(inventaire, texte_cherche):
    """ fonction retournant la liste des sons ayant la variation de tempo (accélération, déccélération,...) recherchée """
    resultat=[element for element in inventaire if element['Variation de Tempo'] == texte_cherche]
    return resultat
