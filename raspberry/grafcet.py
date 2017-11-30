""" Module grafcet_simple, 
version 4 : modifié le 29/10/17 par LR : ajout de l'onglet transition
version 5 : version multiprocessing : ajout d'une queue pour transmettre les numéros d'étapes, et les recettes associées
version 6 : mise en commentaires de l'écoute clavier pour la version rpi 
"""
#from pynput import keyboard
import time
import Scadong_utils


class Grafcet:
        """ Classe permettant d'exécuter n'importe quel grafcet, tant que celui-ci ne comporte que des sélections de séquences.
                Les étapes et les transitions sont importées avec des fichiers .csv devant comporter les noms de colonnes suivants :
        """
        #Liste des colonnes du fichier des étapes :
        colonnes_etapes=['nom_etape','nom_recette']

        #Liste des colonnes du fichier des conditions :
        colonnes_conditions=['nom_condition','nombre_lectures_sequence_mini','bouton','seuil_camera_mini','seuil_camera_maxi','temps_attente']

        #Liste des colonnes du fichier des transitions :
        colonnes_transitions=['etape_precedente','etape_suivante','condition1','operateur','condition2']
        
        def __init__(self, fichier_etapes, fichier_conditions, fichier_transitions,q_et,q_rec,mode):
                self.liste_etapes = Scadong_utils.import_csv(fichier_etapes, Grafcet.colonnes_etapes) # import csv des étapes et actions
                self.liste_conditions = Scadong_utils.import_csv(fichier_conditions, Grafcet.colonnes_conditions) # import csv des réceptivités 
                self.liste_transitions = Scadong_utils.import_csv(fichier_transitions, Grafcet.colonnes_transitions) # import csv des transitions
                self.liste_transitions_suivantes = [] # pour alléger la scrutation
                self.etape = "init" # l'étape initiale doit forcément porter ce nom
                self.touche = "" # à remplacer plus tard par bouton GPIO
                self.arret = True # arrêt scrutation
                self.debut_tempo = 0 # initialisé à l'activation d'une étape
                self.mode = mode
                self.q_etape = q_et
                self.q_recette = q_rec

        def chang_etape(self, etape_suivante):
                """ Fonction à l'activation d'une étape """
                # Initialisation de l'étape
                self.etape = etape_suivante
                self.liste_transitions_suivantes = [element for element in self.liste_transitions if element['etape_precedente']==self.etape]
                if self.liste_transitions_suivantes == []:
                        raise EtapeError("Le nom d'étape {} n'est pas répertorié dans la liste des étapes".format(etape_suivante))
                else:
                        self.debut_tempo = time.time()
                        self.touche=""
                # Exécution des actions
                for element in self.liste_etapes:
                        if element['nom_etape'] == self.etape:
                                if self.mode == "debug":
                                        print("Etape {} : lancement de la recette \"{}\" ".format(self.etape,element['nom_recette']))
                                else:
                                        self.q_etape.put(self.etape) 
                                        self.q_recette.put(element['nom_recette']) 


        def start_init(self):
                self.arret = False
                self.chang_etape("init")

        def scrutation(self):
                condition = False
                for element in self.liste_transitions_suivantes:
                        if element['condition1']!="nc":
                                condition1=self.verifier(element['condition1'])
                                #print("condition 1={} vaut {}".format(element['condition1'],condition1))#pour debug
                        if element['condition2']!="nc":
                                condition2=self.verifier(element['condition2'])
                                #print("condition 2={} vaut {}".format(element['condition2'],condition2))#pour debug
                        if element['condition1']!="nc" and element['condition2']!="nc":
                                if element['operateur']=="and":
                                        condition = condition1 and condition2
                                elif element['operateur']=="or":
                                        condition = condition1 or condition2
                                else:
                                        raise EtapeError("Le format de l'opérateur {} n'est pas correct".format(element['operateur']))
                        elif element['condition1']!="nc":
                                condition=condition1
                        elif element['condition2']!="nc":
                                condition=condition2
                        else:
                                condition=False
                        if condition:
                                #print("activation de l'étape {}".format(element['etape_suivante'])) # pour débug
                                self.chang_etape(element['etape_suivante'])               #franchissement de la transition
                                break
        
        def verifier(self,condition):
                for element in self.liste_conditions:
                        if element['nom_condition']==condition:
                                try:
                                        tempo = float(element['temps_attente'])
                                        #print("temporisation à l'étape {}:{} s".format(self.etape,tempo))#pour débug
                                except TypeError:
                                        print("Erreur de saisie de la temporisation dans la transition de {} à {}".format(element['etape_prec'],element['etape_suiv']))
                                temps_ecoule = time.time() - self.debut_tempo
                                if ( tempo >= 0) and (temps_ecoule >= tempo - 0.1):# on retranche -0.1 pour se laisser le temps d'exécuter la transition
                                        #print("temps_ecoulé : {} s ; tempo : {}".format(temps_ecoule, tempo)) # pour debug
                                        return True
                                #print("touche attendue :{} ; touche appuyée : {} ; égalité : {}". format(self.touche, element['touche'],self.touche == element['touche'])) # pour debug
                                #elif self.touche == "b" and (element['bouton']=="2" or element['bouton']=="3"): 
                                        #print("appui sur la bonne touche")
                                        #return True
                                ##########       A faire elif (element['bouton']==1 or element['bouton']==3): appui sur GPIO ###########
                                ##########       A faire : try camera() ###########
                                ##########       A faire : nombre de séquences #################
                                else :
                                        return False
        

        # def on_press(self, key):
                # try:
                        # self.touche = key.char
                        # self.touche.lower()
                        # print("\n appui sur touche {}\n".format(self.touche))
                        ##print('alphanumeric key {0} pressed'.format(key.char))
                # except AttributeError:
                        # print('special key {0} pressed'.format(key))

        # def on_release(self, key):
                # if key == keyboard.Key.esc:
                        # self.arret=True
                        # print("arrêt vaut {}".format(self.arret))
                        ##Stop listener
                        # return False

        def __repr__(self):
                """ représentation de l'objet grafcet """
                return "liste des étapes et actions associées :\n{}\
                \n \n \
liste des transisitions et réceptivités:\n{} \n \n".format(self.liste_etapes, self.liste_conditions)

        
class EtapeError(Exception):
        """ Exception qui est levée quand on cherche à appeler une étape dont le nom n'est pas répertoirié dans liste_étapes """
        def __init__(self, message):
                """ stockage du message d'erreur """
                self.message = message
        def __str__(self):
                """ on renvoie le message """
                return self.message


# test grafcet "instrumentiste" en python
if __name__ == "__main__":
        import queue
        q_r=queue.Queue()
        q_e=queue.Queue()
        chemin="fichiers_csv/" 
        g7=Grafcet(chemin+"etapes.csv", chemin+"conditions.csv",chemin+"transitions.csv",q_e,q_r,"debug")
        #keyboard.Listener(on_press=g7.on_press, on_release=g7.on_release).start()
        g7.start_init()
                                
        while (not g7.arret):
                g7.scrutation()

        print("\n \n ****** Fin *********")
