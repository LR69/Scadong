### Client Scadong graphique - version 4
from tkinter import *
import time
import random
from multiprocessing import Process, Queue
import socket





class App():
    def __init__(self):
        self.root = Tk()
        self.root.title('Scadong')
        # Serveur Scadong
        self.hote = "192.168.1.102"
        self.port = 49147 #ding
        # Création d'un widget Canvas (zone graphique)
        self.photo = PhotoImage(file="grafcet.gif")
        self.Canevas = Canvas(self.root,width = 665, height =610)
        self.item = self.Canevas.create_image(0,0,anchor=NW, image=self.photo)
        self.Canevas.pack()
        #affichage de l'heure
        self.heure_label = Label(text="")
        self.heure_label.place(x=600, y=10, anchor=NW)
        # Affichage des recettes
        self.label_recettes=[]
        self.label_recette_init = Label(self.root, text='.',padx=2,pady=0,bg='#E6E6FF',width=13)
        self.label_recette_init.place(x=179, y=53, anchor=NW)
        self.label_recettes.append(self.label_recette_init)
        self.label_recette_1A = Label(self.root, text='.',padx=4,pady=0,bg='#E6E6FF',width=17)
        self.label_recette_1A.place(x=37, y=158, anchor=NW)
        self.label_recettes.append(self.label_recette_1A)
        self.label_recette_1B = Label(self.root, text='.',padx=4,pady=0,bg='#E6E6FF',width=17)
        self.label_recette_1B.place(x=289, y=158, anchor=NW)
        self.label_recettes.append(self.label_recette_1B)
        self.label_recette_1C = Label(self.root, text='.',padx=4,pady=0,bg='#E6E6FF',width=17)
        self.label_recette_1C.place(x=522, y=158, anchor=NW)
        self.label_recettes.append(self.label_recette_1C)  
        self.label_recette_2A = Label(self.root, text='.',padx=4,pady=0,bg='#E6E6FF',width=17)
        self.label_recette_2A.place(x=37, y=263, anchor=NW)
        self.label_recettes.append(self.label_recette_2A)
        self.label_recette_2B = Label(self.root, text='.',padx=4,pady=0,bg='#E6E6FF',width=17)
        self.label_recette_2B.place(x=289, y=263, anchor=NW)
        self.label_recettes.append(self.label_recette_2B)
        self.label_recette_2C = Label(self.root, text='.',padx=4,pady=0,bg='#E6E6FF',width=17)
        self.label_recette_2C.place(x=522, y=263, anchor=NW)
        self.label_recettes.append(self.label_recette_2C) 
        self.label_recette_3A = Label(self.root, text='.',padx=4,pady=0,bg='#E6E6FF',width=17)
        self.label_recette_3A.place(x=37, y=368, anchor=NW)
        self.label_recettes.append(self.label_recette_3A)
        self.label_recette_3B = Label(self.root, text='.',padx=4,pady=0,bg='#E6E6FF',width=17)
        self.label_recette_3B.place(x=289, y=368, anchor=NW)
        self.label_recettes.append(self.label_recette_3B)
        self.label_recette_3C = Label(self.root, text='.',padx=4,pady=0,bg='#E6E6FF',width=17)
        self.label_recette_3C.place(x=522, y=368, anchor=NW)
        self.label_recettes.append(self.label_recette_3C)     
        self.label_recette_4A = Label(self.root, text='.',padx=4,pady=0,bg='#E6E6FF',width=17)
        self.label_recette_4A.place(x=37, y=473, anchor=NW)
        self.label_recettes.append(self.label_recette_4A)
        self.label_recette_4B = Label(self.root, text='.',padx=4,pady=0,bg='#E6E6FF',width=17)
        self.label_recette_4B.place(x=289, y=473, anchor=NW)
        self.label_recettes.append(self.label_recette_4B)
        self.label_recette_4C = Label(self.root, text='.',padx=4,pady=0,bg='#E6E6FF',width=17)
        self.label_recette_4C.place(x=522, y=473, anchor=NW)
        self.label_recettes.append(self.label_recette_4C)
        self.etape_en_crs=self.label_recette_init #initialisation du grafcet
        # Affichage des sons joués
        self.son_joue= ""
        #self.nature=""
        self.label2 = Label(text="Son joué :")
        self.label2.pack(side = LEFT,padx=10,pady=10)
        self.boite = Text(width=50,height=5, relief=RAISED )
        #self.boite.grid(column=1,row=2)
        self.boite.pack(side = LEFT,padx=10,pady=3)
        self.compteur=0
        # Création des boutons permettant de passer une transition
        self.BoutonStart = Button(self.root, text ='go', command = self.cmdBouton_go)
        self.BoutonStart.pack(side = LEFT, padx = 10, pady = 10)
        self.BoutonStop = Button(self.root, text ='stop', command = self.cmdBouton_stop)
        self.BoutonStop.pack(side = LEFT, padx = 10, pady = 10)
        self.BoutonStop.configure(state = DISABLED)
        #Définition du serveur
        print("point 1") # pour debug
        time.sleep(0.1) # pour debug
        self.connexion_avec_serveur = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        print("point 2") # pour debug
        time.sleep(0.1) # pour debug
        self.connexion_avec_serveur.connect((self.hote, self.port))
        print("point 3") # pour debug
        time.sleep(0.1) # pour debug
        self.update_clock()
        self.root.mainloop()

    def cmdBouton_go(self):
        msg_a_envoyer = "go".encode()
        # On envoie le message
        self.connexion_avec_serveur.send(msg_a_envoyer)
        msg_recu = self.connexion_avec_serveur.recv(1024)
        msg_recu = msg_recu.decode()
        if msg_recu == "lancement":
            self.BoutonStart.configure(state = DISABLED)
            self.BoutonStop.configure(state = NORMAL)

    def cmdBouton_stop(self):
        msg_a_envoyer = "stop".encode()
        # On envoie le message
        self.connexion_avec_serveur.send(msg_a_envoyer)
        msg_recu = self.connexion_avec_serveur.recv(1024)
        msg_recu = msg_recu.decode()
        if msg_recu == "init":
            self.changeCouleurEtape(msg_recu)
            self.BoutonStart.configure(state = DISABLED)
            self.BoutonStop.configure(state = NORMAL)

    def changeCouleurEtape(self,numero):
        if numero!="nada":
            for lbl in self.label_recettes:
                lbl.configure(bg='#E6E6FF')        
            nom_label="self.label_recette_"+numero
            try:
                self.etape_en_crs=eval(nom_label)
                self.etape_en_crs.configure(bg='#00FF00')
            except NameError:
                print("Mauvais nom")
                pass
            
        
    def update_clock(self):
        now = time.strftime("%H:%M:%S")
        self.heure_label.configure(text=now)
        
        # On demande l'étape en cours au serveur 
        msg_a_envoyer = "etape".encode()
        self.connexion_avec_serveur.send(msg_a_envoyer)
        msg_recu=""
        time.sleep(0.1)
        msg_recu = self.connexion_avec_serveur.recv(1024)
        msg_recu = msg_recu.decode()
        print("message recu suite à une requête d'étape : {}".format(msg_recu))
        if msg_recu != "":
            self.changeCouleurEtape(msg_recu)
        # On demande le son en cours au serveur 
        msg_a_envoyer = "son".encode()
        self.connexion_avec_serveur.send(msg_a_envoyer)
        msg_recu=""
        time.sleep(0.1)
        msg_recu = self.connexion_avec_serveur.recv(1024)
        msg_recu = msg_recu.decode()
        if msg_recu != "":
            if msg_recu != self.son_joue and msg_recu != "nada":
                self.son_joue = msg_recu
                self.boite.insert('1.0',str(self.compteur)+" : "+self.son_joue+'\n')
                self.compteur+=1
        # On demande la recette en cours au serveur 
        msg_a_envoyer = "recette".encode()
        self.connexion_avec_serveur.send(msg_a_envoyer)
        msg_recu=""
        time.sleep(0.1)
        msg_recu = self.connexion_avec_serveur.recv(1024)
        msg_recu = msg_recu.decode()
        if msg_recu != "" and msg_recu != "nada":
            self.etape_en_crs.configure(text=msg_recu)
        self.root.after(1000, self.update_clock)

if __name__ == "__main__":
    app=App()
    print("Fermeture de la connexion")
    #connexion_avec_serveur.close()
    print("*********  fin *********")
