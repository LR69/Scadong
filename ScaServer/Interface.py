#/usr/bin/env python
# -*- coding:utf-8 -*-

import os
from flask import Flask, render_template, request
from werkzeug import secure_filename
app = Flask(__name__)
app.debug = True
@app.route('/')
def accueil():
    return """<!DOCTYPE html>
                <html>
                <head>
                <meta charset="utf-8" />
                <title>Interface Web Scadong</title>
                </head>
                <body>
                <h1>Interface Web Scadong</h1>
                <table>
				<tr>
                <td>
                <form action = "http://localhost:5000/upload" method = "POST" 
				enctype = "multipart/form-data">
				<input type="submit" name="ongl2" value="Upload">
				</form>
				</td>
				<td>
				<form action = "http://localhost:5000/graphset" method = "POST" 
				enctype = "multipart/form-data">
				<input type="submit" name="ongl2" value="Visualisation des clients">
				</form>
				</td>
				<td>
				<form action = "http://localhost:5000/controle" method = "POST" 
				enctype = "multipart/form-data">
				<input type="submit" name="ongl2" value="Controle des clients">
				</form>
				</td>
				<td>
				<form action = "http://localhost:5000/broadcast" method = "POST" 
				enctype = "multipart/form-data">
				<input type="submit" name="ongl2" value="Diffusion broadcast">
				</form>
				</td>
				<td>
				<form action = "http://localhost:5000/video" method = "POST" 
				enctype = "multipart/form-data">
				<input type="submit" name="ongl2" value="Flux video">
				</form>
				</td>
				</tr>
				</table>
				</body>
				</html>"""

@app.route('/upload', methods = ['GET', 'POST'])
def upload():
   return """<!DOCTYPE html>
                <html>
                <head>
                <meta charset="utf-8" />
                <title>Upload</title>
                </head>
                <body>
                <h1>Upload</h1>
                <table>
				<tr>
                <td>
                <form action = "http://localhost:5000/upload/csv" method = "POST" 
				enctype = "multipart/form-data">
				<input type="submit" name="ongl2" value=".csv">
				</form>
				</td>
				<td>
				<form action = "http://localhost:5000/upload/rp1" method = "POST" 
				enctype = "multipart/form-data">
				<input type="submit" name="ongl2" value="musique RPI1">
				</form>
				</td>
				<td>
				<form action = "http://localhost:5000/upload/rp2" method = "POST" 
				enctype = "multipart/form-data">
				<input type="submit" name="ongl2" value="musique RPI2">
				</form>
				</td>
				<td>
				<form action = "http://localhost:5000/upload/rp3" method = "POST" 
				enctype = "multipart/form-data">
				<input type="submit" name="ongl2" value="musique RPI3">
				</form>
				</td>
				</tr>
				</table>
				</body>
				</html>"""
				
@app.route('/controle', methods = ['GET', 'POST'])
def controle():
   return """<!DOCTYPE html>
                <html>
                <head>
                <meta charset="utf-8" />
                <title>Contrôle des RPIs</title>
                </head>
                <body>
                <h1>Contrôle des RPIs</h1>
                <table>
				<tr>
                <td>
                <form action = "http://localhost:5000/RP1on" method = "POST" 
				enctype = "multipart/form-data">
				<input type="submit" name="ongl2" value="ON RP1">
				</form>
				</td>
				<td>
				<form action = "http://localhost:5000/RP2on" method = "POST" 
				enctype = "multipart/form-data">
				<input type="submit" name="ongl2" value="ON RP2">
				</form>
				</td>
				<td>
				<form action = "http://localhost:5000/RP3on" method = "POST" 
				enctype = "multipart/form-data">
				<input type="submit" name="ongl2" value="ON RP3">
				</form>
				</td>
				<td>
				<form action = "http://localhost:5000/ALLon" method = "POST" 
				enctype = "multipart/form-data">
				<input type="submit" name="ongl2" value="ON ALL">
				</form>
				</td>
				</tr>
				<tr>
                <td>
                <form action = "http://localhost:5000/RP1ps" method = "POST" 
				enctype = "multipart/form-data">
				<input type="submit" name="ongl2" value="PAUSE RP1">
				</form>
				</td>
				<td>
				<form action = "http://localhost:5000/RP2ps" method = "POST" 
				enctype = "multipart/form-data">
				<input type="submit" name="ongl2" value="PAUSE RP2">
				</form>
				</td>
				<td>
				<form action = "http://localhost:5000/RP3ps" method = "POST" 
				enctype = "multipart/form-data">
				<input type="submit" name="ongl2" value="PAUSE RP3">
				</form>
				</td>
				<td>
				<form action = "http://localhost:5000/ALLps" method = "POST" 
				enctype = "multipart/form-data">
				<input type="submit" name="ongl2" value="PAUSE ALL">
				</form>
				</td>
				</tr>
				<tr>
                <td>
                <form action = "http://localhost:5000/RP1off" method = "POST" 
				enctype = "multipart/form-data">
				<input type="submit" name="ongl2" value="OFF RP1">
				</form>
				</td>
				<td>
				<form action = "http://localhost:5000/RP2off" method = "POST" 
				enctype = "multipart/form-data">
				<input type="submit" name="ongl2" value="OFF RP2">
				</form>
				</td>
				<td>
				<form action = "http://localhost:5000/RP3off" method = "POST" 
				enctype = "multipart/form-data">
				<input type="submit" name="ongl2" value="OFF RP3">
				</form>
				</td>
				<td>
				<form action = "http://localhost:5000/ALLoff" method = "POST" 
				enctype = "multipart/form-data">
				<input type="submit" name="ongl2" value="OFF ALL">
				</form>
				</td>
				</tr>
				</table>
				</body>
				</html>"""

@app.route('/upload/csv', methods = ['GET', 'POST'])
def uploadcsv():
   return """<!DOCTYPE html>
                <html>
                <head>
                <meta charset="utf-8" />
                <title>Upload</title>
                </head>
                <body>
                <h1>Upload csv</h1>
                <table>
				<tr>
                <td>
                <form action = "http://localhost:5000/upload-csv-uploaded" method = "POST" 
				enctype = "multipart/form-data">
				<input type = "file" name = "file" />
				<input type = "submit"/>
				</form>
				</td>
				</tr>
				</table>
				</body>
				</html>"""

@app.route('/upload/rp1', methods = ['GET', 'POST'])
def uploadrp1():
   return """<!DOCTYPE html>
                <html>
                <head>
                <meta charset="utf-8" />
                <title>Upload</title>
                </head>
                <body>
                <h1>Upload RP1</h1>
                <table>
				<tr>
                <td>
                <form action = "http://192.168.10.254:5000/upload/rp1/uploaded" method = "POST" 
				enctype = "multipart/form-data">
				<input type = "file" name = "file" />
				<input type = "submit"/>
				</form>
				</td>
				</tr>
				</table>
				</body>
				</html>"""
				
@app.route('/upload/rp2', methods = ['GET', 'POST'])
def uploadrp2():
   return """<!DOCTYPE html>
                <html>
                <head>
                <meta charset="utf-8" />
                <title>Upload</title>
                </head>
                <body>
                <h1>Upload RP2</h1>
                <table>
				<tr>
                <td>
                <form action = "http://localhost:5000/upload/rp2/uploaded" method = "POST" 
				enctype = "multipart/form-data">
				<input type = "file" name = "file" />
				<input type = "submit"/>
				</form>
				</td>
				</tr>
				</table>
				</body>
				</html>"""
				
@app.route('/upload/rp3', methods = ['GET', 'POST'])
def uploadrp3():
   return """<!DOCTYPE html>
                <html>
                <head>
                <meta charset="utf-8" />
                <title>Upload RP3</title>
                </head>
                <body>
                <h1>Upload RP3</h1>
                <table>
				<tr>
                <td>
                <form action = "http://localhost:5000/upload/rp3/uploaded" method = "POST" 
				enctype = "multipart/form-data">
				<input type = "file" name = "file" />
				<input type = "submit"/>
				</form>
				</td>
				</tr>
				</table>
				</body>
				</html>"""
				
@app.route('/broadcast', methods = ['GET', 'POST'])
def uploadbroadcast():
   return """<!DOCTYPE html>
                <html>
                <head>
                <meta charset="utf-8" />
                <title>Upload</title>
                </head>
                <body>
                <h1>Upload Broadcast</h1>
                <table>
				<tr>
run(host                <td>
                <form action = "http://localhost:5000/broadcast/uploaded" method = "POST" 
				enctype = "multipart/form-data">
				<input type = "file" name = "file" />
				<input type = "submit"/>
				</form>
				</td>
				</tr>
				</table>
				</body>
				</html>"""

@app.route('/upload/rp1/uploaded', methods = ['GET', 'POST'])
def uploadedrp1():
	UPLOAD_FOLDER = '/home/pi/RPI1/' #chemin vers dossier RP1
	app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
	if request.method == 'POST':
			f = request.files['file']
			f.save(os.path.join(app.config['UPLOAD_FOLDER'],f.filename))
			os.system("sshpass -p raspberry scp -r -p /home/pi/RPI1/* pi@192.168.10.12:/home/pi") #chemin à changer
			return 'file uploaded successfully'

@app.route('/upload/rp2/uploaded', methods = ['GET', 'POST'])
def uploadedrp2():
	UPLOAD_FOLDER = 'E:\projet\RP2' #chemin vers dossier RP2
	app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
	if request.method == 'POST':
			f = request.files['file']
			f.save(os.path.join(app.config['UPLOAD_FOLDER'],f.filename))
			os.system("scp -r -p user@localhost:path/to/file user@rpi1:path/to/file") #chemin à changer
			return 'file uploaded successfully'  

@app.route('/upload/rp3/uploaded', methods = ['GET', 'POST'])
def uploadedrp3():
	UPLOAD_FOLDER = 'E:\projet\RP3' #chemin vers dossier RP1
	app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
	if request.method == 'POST':
			f = request.files['file']
			f.save(os.path.join(app.config['UPLOAD_FOLDER'],f.filename))
			os.system("scp -r -p user@localhost:path/to/file user@rpi1:path/to/file") #chemin à changer
			return 'file uploaded successfully'  

@app.route('/broadcast/uploaded', methods = ['GET', 'POST'])
def uploadedbrcast():
	UPLOAD_FOLDER = 'E:\projet\broadcast' #chemin vers dossier Broadcast
	app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
	if request.method == 'POST':
			f = request.files['file']
			f.save(os.path.join(app.config['UPLOAD_FOLDER'],f.filename))
			os.system("scp -r -p user@localhost:path/to/file user@rpi1:path/to/file") #chemin à changer
			os.system("scp -r -p user@localhost:path/to/file user@rpi2:path/to/file") #chemin à changer
			os.system("scp -r -p user@localhost:path/to/file user@rpi3:path/to/file") #chemin à changer
			return 'file uploaded successfully'  
			
@app.route('/upload/csv/uploaded', methods = ['GET', 'POST'])
def uploadedcsv():
	UPLOAD_FOLDER = 'E:\projet\CSV' #chemin vers dossier csv
	ALLOWED_EXTENSIONS = set(['csv'])
	app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
	if request.method == 'POST':
			f = request.files['file']
			f.save(os.path.join(app.config['UPLOAD_FOLDER'],f.filename))
			return 'file uploaded successfully'  

@app.route('/graphset', methods = ['GET', 'POST'])
def graphset():
	#return import grafcet.py
	return 'grafcet'
	
@app.route('/video', methods = ['GET', 'POST'])
def fluxvideo():
	return 'video'
if __name__ == '__main__':
    app.run(host='192.168.10.254')


