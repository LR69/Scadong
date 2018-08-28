#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Flask, request, render_template, redirect, flash, url_for, send_from_directory
#from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
import os
import time
import arrange_grafcet

CURRENT_FOLDER = '/home/pi/Scaserver' # user à changer pour serveur final

UPLOAD_FOLDER_CSV = CURRENT_FOLDER+'/upload_csv'
DOWNLOAD_FOLDER_CSV = '/home/pi/Scadong/raspberry/fichiers_csv'
ALLOWED_EXTENSIONS_CSV = set(['txt', 'csv'])

UPLOAD_FOLDER_SONS = CURRENT_FOLDER+'/upload_sons'
DOWNLOAD_FOLDER_SONS = '/home/pi/Scadong/raspberry/fichiers_sons'
ALLOWED_EXTENSIONS_SONS = set(['wav'])

UPLOAD_FOLDER_HTML = CURRENT_FOLDER+'/upload_html'
ALLOWED_EXTENSIONS_HTML = set(['htm', 'html'])

TEMPLATE_FOLDER = CURRENT_FOLDER+'/templates'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost/Scadong'
app.config['UPLOAD_FOLDER_CSV'] = UPLOAD_FOLDER_CSV
app.config['UPLOAD_FOLDER_SONS'] = UPLOAD_FOLDER_SONS
app.config['UPLOAD_FOLDER_HTML'] = UPLOAD_FOLDER_HTML

app.secret_key = b'message%ultra%secret'

db = SQLAlchemy(app)




class Scapi(db.Model):
	__tablename__ = 'Scapi'
	id=db.Column(db.INT, primary_key=True)
	ETOR=db.Column(db.INT, nullable =False)
	mvmt=db.Column(db.FLOAT, nullable =False)
	IP_address=db.Column(db.VARCHAR(16), nullable =False)
	time=db.Column(db.DATETIME, nullable =False)
	CONNECTED=db.Column(db.BOOLEAN, nullable =False)
	mode=db.Column(db.VARCHAR(64), nullable =True)
	mode_acquit=db.Column(db.VARCHAR(64), nullable =True)
	cmde_BP=db.Column(db.INT, nullable =True)
	cmde_BP_acquit=db.Column(db.INT, nullable =True)


	# def __init__(id,connected,mode):
	# 	self.id=id
	# 	self.connected=connected
	# 	self.mode=mode
	# 
	# def __repr__(self):
	# 	return '<id %r>' % self.id

class Scapi_sons(db.Model):
	__tablename__ = 'Scapi_sons'
	id=db.Column(db.INT, primary_key=True)
	Scapi_id=db.Column(db.INT, nullable =False)
	Son_nom=db.Column(db.VARCHAR(255), nullable =False)

	# def __init__(id,Scapi_id,Son_nom):
	# 	self.id=id
	# 	self.Scapi_id=Scapi_id
	# 	self.Son_nom=Son_nom
	# 
	# def __repr__(self):
	# 	return '<id %r>' % self.id

class Instrum(db.Model):
	__tablename__ = 'Instrument'
	nom_instrum=db.Column(db.VARCHAR(255), primary_key=True)
	Scapi_id=db.Column(db.INT, nullable =False)
	TypeG7=db.Column(db.VARCHAR(255), nullable =False)
	etape_en_cours=db.Column(db.VARCHAR(255), nullable =True)
	recette_en_cours=db.Column(db.VARCHAR(255), nullable =True)
	sequence_en_cours=db.Column(db.VARCHAR(255), nullable =True)
	trig_en_cours=db.Column(db.INT, nullable =True)
	filtre_en_cours=db.Column(db.VARCHAR(255), nullable =True)
	Son_nom=db.Column(db.VARCHAR(255), nullable =True)
	volume_en_cours=db.Column(db.FLOAT, nullable =False)


class Sons(db.Model):
	__tablename__ = 'Sons'
	nom_du_son=db.Column(db.VARCHAR(255), primary_key=True)
	Duree=db.Column(db.FLOAT, nullable =True)
	Motcle_1=db.Column(db.VARCHAR(255), nullable =True)
	Motcle_2=db.Column(db.VARCHAR(255), nullable =True)
	Motcle_3=db.Column(db.VARCHAR(255), nullable =True)
	Motcle_4=db.Column(db.VARCHAR(255), nullable =True)
	Motcle_5=db.Column(db.VARCHAR(255), nullable =True)
	Motcle_6=db.Column(db.VARCHAR(255), nullable =True)
	Motcle_7=db.Column(db.VARCHAR(255), nullable =True)
	Motcle_8=db.Column(db.VARCHAR(255), nullable =True)
	Motcle_9=db.Column(db.VARCHAR(255), nullable =True)
	Motcle_10=db.Column(db.VARCHAR(255), nullable =True)
	Motcle_11=db.Column(db.VARCHAR(255), nullable =True)
	Motcle_12=db.Column(db.VARCHAR(255), nullable =True)
	Motcle_13=db.Column(db.VARCHAR(255), nullable =True)
	Motcle_14=db.Column(db.VARCHAR(255), nullable =True)
	Motcle_15=db.Column(db.VARCHAR(255), nullable =True)
	Motcle_16=db.Column(db.VARCHAR(255), nullable =True)
	Motcle_17=db.Column(db.VARCHAR(255), nullable =True)
	Motcle_18=db.Column(db.VARCHAR(255), nullable =True)
	Nuance_1=db.Column(db.VARCHAR(255), nullable =True)
	Nuance_2=db.Column(db.VARCHAR(255), nullable =True)
	Nuance_3=db.Column(db.VARCHAR(255), nullable =True)
	Nuance_4=db.Column(db.VARCHAR(255), nullable =True)
	Nuance_5=db.Column(db.VARCHAR(255), nullable =True)
	Nuance_6=db.Column(db.VARCHAR(255), nullable =True)
	Nuance_7=db.Column(db.VARCHAR(255), nullable =True)
	Attaque_1=db.Column(db.VARCHAR(255), nullable =True)
	Attaque_2=db.Column(db.VARCHAR(255), nullable =True)
	Attaque_3=db.Column(db.VARCHAR(255), nullable =True)
	Relachement_1=db.Column(db.VARCHAR(255), nullable =True)
	Relachement_2=db.Column(db.VARCHAR(255), nullable =True)
	Relachement_3=db.Column(db.VARCHAR(255), nullable =True)
	Note_Fondamental_1=db.Column(db.VARCHAR(255), nullable =True)
	Note_Fondamental_2=db.Column(db.VARCHAR(255), nullable =True)
	Note_Fondamental_3=db.Column(db.VARCHAR(255), nullable =True)
	Note_Fondamental_4=db.Column(db.VARCHAR(255), nullable =True)
	Note_Fondamental_5=db.Column(db.VARCHAR(255), nullable =True)
	Note_Fondamental_6=db.Column(db.VARCHAR(255), nullable =True)
	Note_Fondamental_7=db.Column(db.VARCHAR(255), nullable =True)
	Note_Fondamental_8=db.Column(db.VARCHAR(255), nullable =True)
	Note_Fondamental_9=db.Column(db.VARCHAR(255), nullable =True)
	Note_Fondamental_10=db.Column(db.VARCHAR(255), nullable =True)
	Note_Fondamental_11=db.Column(db.VARCHAR(255), nullable =True)
	Note_Fondamental_12=db.Column(db.VARCHAR(255), nullable =True)
	Note_Fondamental_13=db.Column(db.VARCHAR(255), nullable =True)
	Phrase_Musical=db.Column(db.VARCHAR(255), nullable =True)
	Phrase=db.Column(db.BOOLEAN, nullable =True)
	note_dans_Accord_1=db.Column(db.VARCHAR(255), nullable =True)
	note_dans_Accord_2=db.Column(db.VARCHAR(255), nullable =True)
	note_dans_Accord_3=db.Column(db.VARCHAR(255), nullable =True)
	note_dans_Accord_4=db.Column(db.VARCHAR(255), nullable =True)
	note_dans_Accord_5=db.Column(db.VARCHAR(255), nullable =True)
	note_dans_Accord_6=db.Column(db.VARCHAR(255), nullable =True)
	note_dans_Accord_7=db.Column(db.VARCHAR(255), nullable =True)
	note_dans_Accord_8=db.Column(db.VARCHAR(255), nullable =True)
	note_dans_Accord_9=db.Column(db.VARCHAR(255), nullable =True)
	note_dans_Accord_10=db.Column(db.VARCHAR(255), nullable =True)
	note_dans_Accord_11=db.Column(db.VARCHAR(255), nullable =True)
	note_dans_Accord_12=db.Column(db.VARCHAR(255), nullable =True)
	Tempo=db.Column(db.VARCHAR(255), nullable =True)
	Variation_de_Tempo=db.Column(db.VARCHAR(255), nullable =True)
	priorite=db.Column(db.FLOAT, nullable =True)

@app.route('/')
def index():
	Scapis = Scapi.query.all()
	return render_template("index.html",Scapis=Scapis)

@app.route('/scapis')
def scapis():
	Scapis = Scapi.query.all()
	return render_template("scapis.html", Scapis=Scapis )

@app.route("/scapis2" , methods=['GET', 'POST'])
def scapis2():
	Scapis = Scapi.query.all()
	Scapi_num = request.form.get('comp_select')
	Instruments_scapi = Instrum.query.filter_by(Scapi_id=Scapi_num)
	return render_template("scapis2.html", Scapis = Scapis, Instruments_scapi = Instruments_scapi, Scapi_num = Scapi_num ) # just to see what select is

@app.route("/instrument", methods=['GET', 'POST'])
def instrument():
	instrum_nom = request.form.get('comp_select')
	Scapi_num = request.form.get('comp_field')
	# print("instrum_nom vaut :{}".format(instrum_nom))
	# print("Scapi_num vaut :{}".format(Scapi_num))
	recette_tupple = Instrum.query.with_entities(Instrum.etape_en_cours).filter_by(Scapi_id=Scapi_num).filter_by(nom_instrum=instrum_nom).one()
	recette_en_crs = 'R'+ recette_tupple[0]
	instrument_en_crs = Instrum.query.filter_by(Scapi_id=Scapi_num).filter_by(nom_instrum=instrum_nom).one()
	# print("recette en cours :{}".format(recette_en_crs))
	Recette_Couleur = {'recette': recette_en_crs , 'couleur': "#00FF00"}
	# print("recette couleur : {}".format(Recette_Couleur))
	nom_template = instrum_nom + "_grafcet2.html"
	return render_template(nom_template,instrument_en_crs=instrument_en_crs, Recette_Couleur=Recette_Couleur, instrum_nom = instrum_nom, Scapi_num = Scapi_num)

@app.route('/run_rpi', methods=['GET', 'POST'])
def run_rpi():
	Scapis = Scapi.query.all()
	Scapi_num = request.form.get('comp_select2')
	if request.method == 'POST':
		scapi = Scapi.query.filter_by(id=Scapi_num).first()
		scapi.mode = 'run'
		db.session.commit()
	Instruments_scapi = Instrum.query.filter_by(Scapi_id=Scapi_num)
	return render_template("scapis2.html", Scapis = Scapis, Instruments_scapi = Instruments_scapi, Scapi_num = Scapi_num ) # just to see what select is
	
@app.route('/pause_rpi', methods=['GET', 'POST'])
def pause_rpi():
	Scapis = Scapi.query.all()
	Scapi_num = request.form.get('comp_select3')
	if request.method == 'POST':
		scapi = Scapi.query.filter_by(id=Scapi_num).first()
		scapi.mode = 'pause'
		db.session.commit()
	Instruments_scapi = Instrum.query.filter_by(Scapi_id=Scapi_num)
	return render_template("scapis2.html", Scapis = Scapis, Instruments_scapi = Instruments_scapi, Scapi_num = Scapi_num ) # just to see what select is
	
def allowed_file_csv(filename): #vérifie que l'extension du fichier uploadé est .txt ou .csv
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS_CSV

def allowed_file_sons(filename): #vérifie que l'extension du fichier uploadé est .wav 
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS_SONS

def allowed_file_html(filename): #vérifie que l'extension du fichier uploadé est .htm ou .html
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS_HTML

def enlever_extension(filename): # enlève l'extension wav du nom du fichier pour le retrouver dans le csv
	return filename.rsplit('.',1)[0]

def verifier_son(filename): # vérifie la conformité du son
		nom_son = enlever_extension(filename) # 
		if Sons.query.filter_by(nom_du_son=nom_son).first() != None:
			return True
		else:
			return False

@app.route('/upload', methods=['GET', 'POST'])
def up_load():
	Scapis = Scapi.query.all()
	return render_template("upload.html", Scapis=Scapis )


@app.route('/upload_csv', methods=['GET', 'POST'])
def upload_csv():
	Scapis = Scapi.query.all()
	if request.method == 'POST':
		Scapi_num = request.form.get('comp_select')
		#print("Scapi_num :{}".format(Scapi_num))
		# check if the post request has the file part
		if 'file' not in request.files:
			flash('No file part')
			return redirect(request.url)
		file = request.files['file']
		# if user does not select file, browser also
		# submit an empty part without filename
		if file.filename == '':
			flash('No selected file')
			return redirect(request.url)
		if file and allowed_file_csv(file.filename):
			#filename = secure_filename(file.filename)
			filename = file.filename
			file.save(os.path.join(app.config['UPLOAD_FOLDER_CSV'], filename))
			##### zone en com pour test sans RPi
			ip_address = Scapi.query.filter_by(id=Scapi_num).one().IP_address 
			#print("adresse IP :{}".format(ip_address))
			#print(ip_address)
			cmd="sshpass -p raspberry scp "+ UPLOAD_FOLDER_CSV + "/" + filename + " pi@" + ip_address + ":" + DOWNLOAD_FOLDER_CSV
			#print("commande ssh :{}".format(cmd))
			os.system(cmd)
			#####
			msg = "Fichier " + filename + " correctement uploadé"
			flash(msg)
			return redirect(url_for('up_load'))
		else:
			msg = "le fichier " + file.filename + " n'a pas une extension .csv" 
			flash(msg)
	return render_template("upload.html", Scapis=Scapis)

@app.route('/upload_sons', methods=['GET', 'POST'])
def upload_sons():
	Scapis = Scapi.query.all()
	if request.method == 'POST':
		Scapi_num = request.form.get('comp_select2')
		#print("Scapi_num :{}".format(Scapi_num))
		# check if the post request has the file part
		if 'file' not in request.files:
			flash('No file part')
			return redirect(request.url)
		file = request.files['file']
		# if user does not select file, browser also
		# submit an empty part without filename
		if file.filename == '':
			flash('No selected file')
			return redirect(request.url)
		if file and allowed_file_sons(file.filename):
			#filename = secure_filename(file.filename)
			if verifier_son(file.filename):
				filename = file.filename
				son_nom = enlever_extension(filename)
				file.save(os.path.join(app.config['UPLOAD_FOLDER_SONS'], filename))
				##### zone en com pour test sans RPi
				ip_address = Scapi.query.filter_by(id=Scapi_num).one().IP_address
				#print("adresse IP :{}".format(ip_address))
				#print(ip_address)
				cmd="sshpass -p raspberry scp "+ UPLOAD_FOLDER_SONS + "/" + filename + " pi@" + ip_address + ":" + DOWNLOAD_FOLDER_SONS
				#print("commande ssh :{}".format(cmd))
				os.system(cmd)
				##### 
				
				# fin
				msg = "Fichier " + filename + " correctement uploadé"
				flash(msg)
				return redirect(url_for('up_load'))
			else:
				msg = "le son " + enlever_extension(file.filename) + " n'est pas répertorié dans la base de données" # test OK 19/08/18
				flash(msg)
		else:
			msg = "le fichier " + file.filename + " n'a pas une extension .wav" # test OK 19/08/18
			flash(msg)
	return render_template("upload.html", Scapis=Scapis)

@app.route('/init_rpi', methods=['GET', 'POST'])
def init_rpi():
	if request.method == 'POST':
		Scapi_num = request.form.get('comp_select3')
		scapi = Scapi.query.filter_by(id=Scapi_num).first()
		scapi.mode = 'init'
		db.session.commit()
		#rows_changed = Scapi.query.filter_by(id=Scapi_num).update(dict(mode='init'))
		#print("mise à jour du raspberry effectuée")
		Scapis = Scapi.query.all()
		sons_du_serveur = Sons.query.all()
		sons_du_scapi = Scapi_sons.query.filter_by(Scapi_id=Scapi_num).all()
		#print("sons_du_scapi:{}".format(sons_du_scapi))
		return render_template("upload.html", Scapis=Scapis, sons_du_serveur=sons_du_serveur, sons_du_scapi=sons_du_scapi)

@app.route('/upload_html', methods=['GET', 'POST'])
def upload_html():
	Scapis = Scapi.query.all()
	if request.method == 'POST':
		Scapi_num = request.form.get('comp_select4')
		#print("Scapi_num :{}".format(Scapi_num))
		# check if the post request has the file part
		if 'file' not in request.files:
			flash('No file part')
			return redirect(request.url)
		file = request.files['file']
		# if user does not select file, browser also
		# submit an empty part without filename
		if file.filename == '':
			flash('No selected file')
			return redirect(request.url)
		if file and allowed_file_html(file.filename):
			#filename = secure_filename(file.filename)
			filename = file.filename
			file.save(os.path.join(app.config['UPLOAD_FOLDER_HTML'], filename))
			### Mise en forme du grafcet pour template
			fichier_ini = UPLOAD_FOLDER_HTML + "/" + filename
			nom_fichier = enlever_extension(filename)
			fichier_modif = TEMPLATE_FOLDER + "/" + nom_fichier + "2.html"
			cmd="cp " + fichier_ini + " " + fichier_modif
			os.system(cmd)
			chemin = CURRENT_FOLDER + "/"
			arrange_grafcet.arranger_grafcet(chemin,fichier_ini,fichier_modif)
			msg = "Fichier " + filename + " correctement uploadé"
			flash(msg)
			return redirect(url_for('up_load'))
		else:
			msg = "le fichier " + file.filename + " n'a pas une extension .csv" 
			flash(msg)
	return render_template("upload.html", Scapis=Scapis)


@app.route('/diagnostic')
def diagnostic():
	Scapis = Scapi.query.all()
	return render_template("diagnostic.html", Scapis=Scapis )

@app.route("/diagnostic2" , methods=['GET', 'POST'])
def diagnostic2():
	Scapi_num = request.form.get('comp_select')
	scapi = Scapi.query.filter_by(id=Scapi_num).first()
	return render_template("diagnostic2.html", scapi = scapi, Scapi_num = Scapi_num) # just to see what select is

if __name__ == '__main__':
	app.run(host='0.0.0.0',debug=True)
	
