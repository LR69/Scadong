# Normalement il faudrait ici définir l'objectif et les fonctionnalités de ce programme "Scadong"
# Mais là, vraiment, cela prendrait trop de place...
# Pour tout renseignement contacter Anthony CLERC à thyonan1 <thyonan1@hotmail.fr>
# 21/11/17 : ajout des communications réseau via des sockets. Scadong joue le rôle de serveur.
# 12/04/18 : bug problèmes de pas
import grafcet
import sequenceur
import Scadong_utils
import csv
import random
import time
from math import *
from filtres import *
#from pynput import keyboard
from multiprocessing import Process, Queue
import Serveur_Scadong # AJR

#variables globales
chemin_csv = "fichiers_csv/" #pour pouvoir trouver le chemin des fichiers



def fournir_feuille(q_li,q_or,q_et):
        """ ce processus fournit des sons au séquenceur quand celui-ci en fait la demande """
        Feuille_papier_musique=[] # la feuille qui contient tous les sons que le séquenceur doit jouer.
        ligne=[] # une ligne de la feuille
        fq=Queue() # queue de transfert des sons au séquenceur
        oq=Queue() # queue de transfert des ordres au séquenceur
        eq=Queue() # queue de transfert des états depuis le séquenceur
        
        # Lancement du séquenceur
        psequenceur = Process(target=sequenceur.sequenceur, args=(fq,oq,eq)) # fq = canal des feuilles, oq canal des ordres donnés au séquenceur, eq canal états séquenceur
        psequenceur.start()
        oq.put("go")
        o=""
        e=""
        while o!="arret":
                ### échanges avec processus parent
                if q_or.empty()==False:
                        try:
                                o=q_or.get(False) # non bloquant
                                #print("ordre du pgme principal au fournisseur : {}".format(o)) #pour debug
                        except queue.Empty:
                                pass
                # On jette la feuille papier musique sur ordre du processus parent
                if o=="flush":
                        Feuille_papier_musique=[] 
                        #oq.put("flush")
                if q_li.empty()==False:
                        try:
                                ligne=q_li.get(False) # non bloquant
                                Feuille_papier_musique.append(ligne) # on rajoute la ligne reçue au tampon
                                #print("ligne reçue du programme ppal : {}".format(ligne)) #pour debug
                        except queue.Empty:
                                pass
                # échanges avec le processus Enfant
                if eq.empty()==False:
                        try:
                                e=eq.get(False)  # non bloquant
                                #print("message du séquenceur : {}".format(e)) #pour debug
                        except queue.Empty:
                                pass
                if (e=="demande_papier" or e=="fin_papier") and Feuille_papier_musique!=[]: #on ne peut fournir des sons que si on en a en réserve.
                        ligne=Feuille_papier_musique[0]
                        fq.put(ligne) #envoi d'une ligne au séquenceur
                        #print("envoi au séquenceur de la ligne : {}".format(ligne)) 
                        del Feuille_papier_musique[0] # la igne a été envoyée, elle est retirée du tampon d'envoi.
                time.sleep(0.002)
        # demande d'arrêt du séquenceur
        oq.put("stop")
        while e!="fin":
                e=eq.get()
        #print("message2 : {}".format(e)) #pour debug
        q_et.put("termine") # on prévient le processus parent qu'on sort
        print("\n \n ****** Fin séquenceur *********")
        psequenceur.join()


def traitement_grafcet(q_etape,q_recette,q_ordre,q_etat):#AJR
        """ Ce processus gère toute la partie logique séquentielle du programme ainsi que les E/S
        """
        instrumentiste=grafcet.Grafcet(chemin_csv+"etapes.csv", chemin_csv+"conditions.csv",chemin_csv+"transitions.csv",q_etape,q_recette,"normal")
        #keyboard.Listener(on_press=instrumentiste.on_press, on_release=instrumentiste.on_release).start()
        instrumentiste.start_init()
        ordre=""
        while (not instrumentiste.arret and ordre!="arret"):
                instrumentiste.scrutation()
                time.sleep(0.002) # pour permettre à la boucle de détecter une variation de temps
                try: #AJR
                        while q_ordre.empty()==False: #pour disposer de la dernière info
                            ordre=q_ordre.get(False)
                except queue.Empty:
                    e="queue recette est vide"
                    print(e) #pour debug
                    pass
        q_recette.put("nc") #pour informer le processus principal
        q_etape.put("fin") #pour informer le processus principal
        
    

# test grafcet "instrumentiste" en python
if __name__ == "__main__":
        # import csv des sons
        colonnes_sons=['nom du son','Durée (sec)','Motcle 1','Motcle 2','Motcle 3','Motcle 4','Motcle 5','Motcle 6','Motcle 7','Motcle 8','Motcle 9','Motcle 10','Motcle 11','Motcle 12','Motcle 13','Motcle 14','Motcle 15','Motcle 16','Motcle 17','Motcle 18','Nuance 1','Nuance 2','Nuance 3','Nuance 4','Nuance 5','Nuance 6','Nuance 7','Attaque 1','Attaque 2','Attaque 3','Relâchement 1','Relâchement 2','Relâchement 3','Note Fondamental 1','Note Fondamental 2','Note Fondamental 3','Note Fondamental 4','Note Fondamental 5','Note Fondamental 6','Note Fondamental 7','Note Fondamental 8','Note Fondamental 9','Note Fondamental 10','Note Fondamental 11','Note Fondamental 12','Note Fondamental 13','Phrase Musical ?','Phrasé','note dans l\'Accord 1','note dans l\'Accord 2','note dans l\'Accord 3','note dans l\'Accord 4','note dans l\'Accord 5','note dans l\'Accord 6','note dans l\'Accord 7','note dans l\'Accord 8','note dans l\'Accord 9','note dans l\'Accord 10','note dans l\'Accord 11','note dans l\'Accord 12','Tempo','Variation de Tempo','priorité (de 0 à 100)']
        inventaire_sons = Scadong_utils.import_csv(chemin_csv+"inventaire_sons.csv", colonnes_sons) #import csv des sons
        #print(inventaire_sons) # pour debug
        print("import csv des sons OK")
        colonnes_filtres=['nom du filtre','Durée mini (sec)','Durée maxi (sec)','Motcle 1','Motcle 2','Motcle 3','Motcle 4','Motcle 5','Motcle 6','Motcle 7','Motcle 8','Motcle 9','Motcle 10','Motcle 11','Motcle 12','Motcle 13','Motcle 14','Motcle 15','Motcle 16','Motcle 17','Motcle 18','Nuance 1','Nuance 2','Nuance 3','Nuance 4','Nuance 5','Nuance 6','Nuance 7','Attaque 1','Attaque 2','Attaque 3','Relâchement 1','Relâchement 2','Relâchement 3','Note Fondamental 1','Note Fondamental 2','Note Fondamental 3','Note Fondamental 4','Note Fondamental 5','Note Fondamental 6','Note Fondamental 7','Note Fondamental 8','Note Fondamental 9','Note Fondamental 10','Note Fondamental 11','Note Fondamental 12','Note Fondamental 13','Phrase Musical ?','Phrasé','note dans l\'Accord 1','note dans l\'Accord 2','note dans l\'Accord 3','note dans l\'Accord 4','note dans l\'Accord 5','note dans l\'Accord 6','note dans l\'Accord 7','note dans l\'Accord 8','note dans l\'Accord 9','note dans l\'Accord 10','note dans l\'Accord 11','note dans l\'Accord 12','Tempo min','Tempo max','Variation de Tempo','priorité (de 0 à 100)']
        inventaire_filtres = Scadong_utils.import_csv(chemin_csv+"filtres.csv", colonnes_filtres) #import csv des filtres
        #print(inventaire_filtres) # pour debug
        print("import csv des filtres OK")
        #test_filtres(inventaire_sons,inventaire_filtres) #pour debug
        
        colonnes_recettes=['nom de recette','filtre','séquence','départ séquence','type de lecture','nbre de canal de lecture max','départ vers effet A','départ vers effet B','départ vers effet C','départ vers effet D','départ vers effet E','départ vers effet F','départ vers effet G','départ vers effet H']
        inventaire_recettes = Scadong_utils.import_csv(chemin_csv+"recettes.csv", colonnes_recettes) #import csv des recettes
        #print(inventaire_recettes) # pour debug
        print("import csv des recettes OK")
        
        colonnes_sequences=['nom séquence','taille du pas','longueur séquence','nombre de boucle séquence(-1 = inf)','trig','temps du trig (en pas)','volume (vélocité)','filtre','chance de jeu (entre 0 et 100)','départ vers effet A','départ vers effet B','départ vers effet C','départ vers effet D','départ vers effet E','départ vers effet F','départ vers effet G','départ vers effet H']
        inventaire_sequences = Scadong_utils.import_csv(chemin_csv+"sequences.csv", colonnes_sequences) #import csv des sequences
        print([element['nom séquence'] for element in inventaire_sequences])
        print("import csv des sequences OK")
        
        # Lancement du processus fournissant des feuilles au séquenceur
        q_ligne = Queue()
        q_ordre = Queue()
        q_etat = Queue()
        pfournisseur = Process(target=fournir_feuille, args=(q_ligne,q_ordre,q_etat))
        pfournisseur.start()
        
        
        # Lancement du processus serveur pour pilotage à distance de scadong
        etape="" #AJR
        recette="" #AJR
        ordre="" #AJR
        etat="" #AJR
        qs_etape = Queue() #AJR
        qs_recette = Queue() #AJR
        qs_son = Queue() #AJR
        qs_ordre = Queue()
        qs_etat = Queue()
        pserveur = Process(target=Serveur_Scadong.traitement_serveur, args=(qs_etape,qs_recette,qs_son,qs_ordre,qs_etat))#AJR
        pserveur.start() #AJR
        # attente d'un ordre de démarrage
        while(ordre!="go"):#AJR
                try:
                        while qs_ordre.empty()==False: #pour disposer de la dernière info
                            ordre=qs_ordre.get(False)
                except queue.Empty:
                    e="queue recette est vide"
                    print(e) #pour debug
                    pass
        
        #début du programme instrumentiste (=grafcet)
        qrecette = Queue()
        qetape = Queue()
        qordre = Queue()
        qetat = Queue()
        pinstrumentiste = Process(target=traitement_grafcet, args=(qetape,qrecette,qetape,qetat))
        pinstrumentiste.start()
        print("c'est parti !") # pour debug
        
        while (ordre!="stop") and (etape != "fin"):#AJR
                etape = qetape.get()
                recette = qrecette.get()
                print("etape en cours : {}".format(etape))
                print("recette en cours : {}".format(recette))
                q_ordre.put("flush") # on vide la liste des sons en attente
                liste_sons_filtres=[] # 1er tri
                liste_sons_filtres2=[] # 2nd tri
                liste_sons_filtres3=[] # 3ème tri
                ### Application de la recette
                if(recette != "" and recette != "nc"):
                        #recette trouvée dans la liste des recettes à partir du nom de la recette
                        recette_dans_liste=[element for element in inventaire_recettes if element['nom de recette']==recette][0] # on trouve la recette en cours dans l'inventaire des recettes
                        print("recette trouvée dans la liste = {}".format(recette_dans_liste)) # pour debug
                        filtre_recette_nom = recette_dans_liste['filtre']
                        if (filtre_recette_nom != "" and filtre_recette_nom != "nc"):
                                filtre_recette=[element for element in inventaire_filtres if element['nom du filtre']==filtre_recette_nom][0] 
                                #print("Filtre applicable au niveau de la recette : {}".format(filtre_recette)) # pour debug
                                #premier filtrage des sons :
                                liste_sons_filtres=filtrage(inventaire_sons,filtre_recette)
                                print("Nom du filtre applicable au niveau de la recette : {}".format(filtre_recette_nom)) # pour debug
                                print("nombre de sons après filtrage recette : {}".format(len(liste_sons_filtres)))     # pour debug
                                #print([element['nom du son'] for element in liste_sons_filtres]) # pour debug
                        else:
                                liste_sons_filtres=inventaire_sons #pas de premier filtrage
                ### Application de la séquence
                #séquence trouvée dans la liste des séquences à partir du nom de la séquence figurant dans la recette
                sequences_dans_liste=[element for element in inventaire_sequences if element['nom séquence']==recette_dans_liste['séquence']] # on trouve la liste des séquences de nom 'nom séquence'
                print("Nom de la séquence applicable au niveau de la recette : {}".format([element['nom séquence'] for element in sequences_dans_liste][0])) # pour debug
                print("Nombre de trigs: {}".format(len([element['nom séquence'] for element in sequences_dans_liste]))) # pour debug
                longueur_sequence = int([element['longueur séquence'] for element in sequences_dans_liste][0])
                print("longueur séquence :{}".format(longueur_sequence)) # pour debug
                taille_pas = int([element['taille du pas'] for element in sequences_dans_liste][0])
                print("taille du pas :{}".format(taille_pas)) # pour debug
                for tic in range(1,longueur_sequence): # tic = pas
                        #print("pas = {} ; ".format(tic)) # pour debug
                        sequences_au_tic = [element for element in sequences_dans_liste if int(element['temps du trig (en pas)'])==tic] #on trouve les séquences à jouer pour ce pas de temps
                        #print("Nombre de trig: {} au pas : {}".format(len([element['nom séquence'] for element in sequences_au_tic]),tic)) # pour debug
                        ligne_trous=[] # une nouvelle ligne de trous dans le papier à musique
                        for sequence in sequences_au_tic:
                                volume = float(sequence['volume (vélocité)'])/100.0 #volume compris entre 0 et 1
                                filtre_sequence = [element for element in inventaire_filtres if element['nom du filtre']==sequence['filtre']][0]
                                #print("un filtre applicable au tic:{} est :{}".format(tic, filtre_sequence['nom du filtre'])) #pour debug
                                #print("le volume à jouer est :{}".format(volume))
                                #second filtrage des sons :
                                liste_sons_filtres2=filtrage(liste_sons_filtres,filtre_sequence)
                                if len(liste_sons_filtres)>0:
                                        print("nombre de sons après filtrage séquence : {}".format(len(liste_sons_filtres2)))   # pour debug
                                #print("noms des sons triés au niveau de la séquence : ") # pour debug
                                #print([element['nom du son'] for element in liste_sons_filtres2]) # pour debug
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
                                        #print("noms des sons triés et prioritaires : ") # pour debug
                                        #print([element['nom du son'] for element in liste_sons_filtres3]) # pour debug
                                        index_alea=random.randint(1,len(liste_sons_filtres3)) # random.randint(a, b) Return a random integer N such that a <= N <= b. Alias for randrange(a, b+1).
                                        #print(index_alea) # pour debug
                                        for i in range(0,index_alea):
                                                son_a_jouer=liste_sons_filtres3.pop()
                                        #print("son à jouer : {}".format(son_a_jouer['nom du son'])) # pour debug
                                        fichier_son_a_jouer=son_a_jouer['nom du son']+".wav"
                                        trou = (fichier_son_a_jouer, volume)
                                        #on fait un trou sur ligne de trous dans le papier à musique
                                        ligne_trous.append(trou)
                        if ligne_trous != [] :
                                print("sons à jouer au trig{}:{}".format(tic,ligne_trous))
                        q_ligne.put(ligne_trous)
                print("\n \n") # pour debug
                #gestion des communications réseau avec le client
                qs_etape.put(etape) #AJR
                qs_recette.put(recette) #AJR
                qs_son.put(fichier_son_a_jouer) #AJR
                try: #AJR
                        while qs_ordre.empty()==False: #pour disposer de la dernière info
                            ordre=qs_ordre.get(False)
                except queue.Empty:
                    e="queue recette est vide"
                    print(e) #pour debug
                    pass
                time.sleep(0.002) # pour permettre à la boucle de détecter une variation de temps
        qs_etape.put("init") #AJR
        q_ordre.put("arret") # on arrete le fournisseur de feuilles
        qordre.put("arret") # AJR on arrete l'instrumentiste
        while e!="termine":
                e=q_etat.get()
                #print("message2 : {}".format(e)) #pour debug
        print("\n \n ****** Fin *********")
        pfournisseur.join()
        pinstrumentiste.join()
        pserveur.join(3)
