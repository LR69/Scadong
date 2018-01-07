import socket
import select
from multiprocessing import Process, Queue
import time

class Serveur_Scadong:
    """ classe associée à un insrumentiste, et qui permet de transmettre à une machine distante des informations le concernant
    """
    
    

    def __init__(self,port, q_etape, q_recette, q_son, q_ordre, q_etat):   
        self.port = port
        self.connexion_principale = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.hote = ''
        self.connexion_principale.bind((self.hote, self.port))
        self.connexion_principale.listen(5)
        self.q_etape=q_etape # pour communiquer l'étape en cours au client
        self.q_recette=q_recette # pour communiquer la recette en cours au client
        self.q_son=q_son # pour communiquer le son joué au client
        self.q_ordre=q_ordre # pour donner un ordre de forçage au grafcet
        self.q_etat=q_etat # pour communiquer un état particulier du grafcet
        
    def lancer_serveur(self):
        print("Le serveur écoute à présent sur le port {}".format(self.port))
        serveur_lance = True
        clients_connectes = []
        while serveur_lance:
            etape="nada"
            recette="nada"
            son="nada"
            # On va vérifier que de nouveaux clients ne demandent pas à seconnecter
            # Pour cela, on écoute la connexion_principale en lecture
            # On attend maximum 50ms
            connexions_demandees, wlist, xlist =select.select([self.connexion_principale],[], [], 0.05)
            for connexion in connexions_demandees:
                connexion_avec_client, infos_connexion = connexion.accept()
                # On ajoute le socket connecté à la liste des clients
                clients_connectes.append(connexion_avec_client)
            # Maintenant, on écoute la liste des clients connectés
            # Les clients renvoyés par select sont ceux devant être lus(recv)
            # On attend là encore 50ms maximum
            # On enferme l'appel à select.select dans un bloc try
            # En effet, si la liste de clients connectés est vide, une exception
            # Peut être levée
            clients_a_lire = []
            try:
                clients_a_lire, wlist, xlist = select.select(clients_connectes,[], [], 0.05)
            except select.error:
                pass
            else:
                # On parcourt la liste des clients à lire
                for client in clients_a_lire:
                    # Client est de type socket
                    msg_recu = client.recv(1024)
                    # Peut planter si le message contient des caractèresspéciaux
                    msg_recu = msg_recu.decode()
                    #print("Reçu {}".format(msg_recu))#pour debug
                    if msg_recu == "etape":
                        try:
                                while self.q_etape.empty()==False: #pour disposer de la dernière info
                                        etape=self.q_etape.get(False)
                                        
                        except queue.Empty:
                                e="queue etape est vide"
                                print(e) #pour debug
                                pass
                        client.send(etape.encode()) # AJR
                    elif msg_recu == "recette":
                        try:
                                while self.q_recette.empty()==False: #pour disposer de la dernière info
                                    recette=self.q_recette.get(False)
                                    
                        except queue.Empty:
                                e="queue recette est vide"
                                print(e) #pour debug
                                pass
                        client.send(recette.encode())
                    elif msg_recu == "son":
                        try:
                                while self.q_son.empty()==False: #pour disposer de la dernière info
                                    son=self.q_son.get(False)
                                    
                        except queue.Empty:
                                e="queue recette est vide"
                                print(e) #pour debug
                                pass
                        client.send(son.encode())
                    elif msg_recu == "init":
                        self.q_ordre.put(msg_recu)
                        client.send("grafcet réinitialisé".encode())
                    elif msg_recu == "go":
                        self.q_ordre.put(msg_recu)
                        client.send("lancement".encode())
                    elif msg_recu == "stop":
                        self.q_ordre.put(msg_recu)
                        serveur_lance = False
                    else:
                        message="le message envoyé \'{}\' n\'est pas clair ".format(msg_recu)
                        client.send(message.encode())
        print("Fermeture des connexions")
        for client in clients_connectes:
            client.close()
            self.connexion_principale.close()

def traitement_serveur(q_etape,q_recette,q_son,q_ordre,q_etat):
    #initialisation du serveur
    serveur_scadong=Serveur_Scadong(49147,q_etape,q_recette,q_son,q_ordre,q_etat)
    #lancement du serveur
    serveur_scadong.lancer_serveur()
    

# test serveur "Scadong" en console python
if __name__ == "__main__":
    qetape = Queue()
    qrecette = Queue()
    qson = Queue()
    qordre = Queue()
    qetat = Queue()
    pserveur = Process(target=traitement_serveur, args=(qetape,qrecette,qson,qordre,qetat))
    pserveur.start()
    ordre="go"
    i=1
    while(i<10):
        etape="etape{}".format(i)
        recette="recette{}".format(i)
        qetape.put(etape)
        qrecette.put(recette)
        time.sleep(5)
        try:
            while qordre.empty()==False: #pour disposer de la dernière info
                ordre=qordre.get(False)
        except queue.Empty:
            e="queue recette est vide"
            print(e) #pour debug
            pass
        if ordre=="init":
            i=1
            print("i vaut à présent:{}".format(i))
            ordre=""
        else:
            i+=1
    
    qetape.put("fin")
    qrecette.put("")
    pserveur.join()
    print("\n \n ****** Fin *********")
    
