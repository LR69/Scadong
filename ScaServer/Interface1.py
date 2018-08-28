#/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import MySQLdb

from flask import Flask, render_template, request
from werkzeug import secure_filename
app = Flask(__name__)
app.debug = True
db = MySQLdb.connect(host="localhost",    # your host, usually localhost
                     user="root",         # your username
                     passwd="root",  # your password
                     db="Scadong")        # name of the data base
cur = db.cursor()
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
                <form action = "http://192.168.10.254:5000/upload" method = "POST" 
				enctype = "multipart/form-data">
				<input type="submit" name="ongl2" value="Upload">
				</form>
				</td>
				<td>
				<form action = "http://192.168.10.254:5000/graphset" method = "POST" 
				enctype = "multipart/form-data">
				<input type="submit" name="ongl2" value="Visualisation des clients">
				</form>
				</td>
				<td>
				<form action = "http://192.168.10.254:5000/controle" method = "POST" 
				enctype = "multipart/form-data">
				<input type="submit" name="ongl2" value="Controle des clients">
				</form>
				</td>
				<td>
				<form action = "http://192.168.10.254:5000/broadcast" method = "POST" 
				enctype = "multipart/form-data">
				<input type="submit" name="ongl2" value="Diffusion broadcast">
				</form>
				</td>
				<td>
				<form action = "http://192.168.10.254:5000/video" method = "POST" 
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
                <form action = "http://192.168.10.254:5000/upload/csv" method = "POST" 
				enctype = "multipart/form-data">
				<input type="submit" name="ongl2" value=".csv">
				</form>
				</td>
				<td>
				<form action = "http://192.168.10.254:5000/upload/rp1" method = "POST" 
				enctype = "multipart/form-data">
				<input type="submit" name="ongl2" value="musique RPI1">
				</form>
				</td>
				<td>
				<form action = "http://192.168.10.254:5000/upload/rp2" method = "POST" 
				enctype = "multipart/form-data">
				<input type="submit" name="ongl2" value="musique RPI2">
				</form>
				</td>
				<td>
				<form action = "http://192.168.10.254:5000/upload/rp3" method = "POST" 
				enctype = "multipart/form-data">
				<input type="submit" name="ongl2" value="musique RPI3">
				</form>
				</td>
				</tr>
				</table>
				</body>
				</html>"""
@app.route('/graphset', methods = ['GET', 'POST'])
def graphset():
   cur.execute("SELECT * FROM Scapi ")
   data = cur.fetchall()
   return render_template('oui.html', data=data)
				
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
                <form action = "http://192.168.10.254:5000/RP1on" method = "POST" 
				enctype = "multipart/form-data">
				<input type="submit" name="ongl2" value="ON RP1">
				</form>
				</td>
				<td>
				<form action = "http://192.168.10.254:5000/RP2on" method = "POST" 
				enctype = "multipart/form-data">
				<input type="submit" name="ongl2" value="ON RP2">
				</form>
				</td>
				<td>
				<form action = "http://192.168.10.254:5000/RP3on" method = "POST" 
				enctype = "multipart/form-data">
				<input type="submit" name="ongl2" value="ON RP3">
				</form>
				</td>
				<td>
				<form action = "http://192.168.10.254:5000/ALLon" method = "POST" 
				enctype = "multipart/form-data">
				<input type="submit" name="ongl2" value="ON ALL">
				</form>
				</td>
				</tr>
				<tr>
                <td>
                <form action = "http://192.168.10.254:5000/RP1ps" method = "POST" 
				enctype = "multipart/form-data">
				<input type="submit" name="ongl2" value="PAUSE RP1">
				</form>
				</td>
				<td>
				<form action = "http://192.168.10.254:5000/RP2ps" method = "POST" 
				enctype = "multipart/form-data">
				<input type="submit" name="ongl2" value="PAUSE RP2">
				</form>
				</td>
				<td>
				<form action = "http://192.168.10.254:5000/RP3ps" method = "POST" 
				enctype = "multipart/form-data">
				<input type="submit" name="ongl2" value="PAUSE RP3">
				</form>
				</td>
				<td>
				<form action = "http://192.168.10.254/ALLps" method = "POST" 
				enctype = "multipart/form-data">
				<input type="submit" name="ongl2" value="PAUSE ALL">
				</form>
				</td>
				</tr>
				<tr>
                <td>
                <form action = "http://192.168.10.254/RP1off" method = "POST" 
				enctype = "multipart/form-data">
				<input type="submit" name="ongl2" value="OFF RP1">
				</form>
				</td>
				<td>
				<form action = "http://192.168.10.254:5000/RP2off" method = "POST" 
				enctype = "multipart/form-data">
				<input type="submit" name="ongl2" value="OFF RP2">
				</form>
				</td>
				<td>
				<form action = "http://192.168.10.254:5000/RP3off" method = "POST" 
				enctype = "multipart/form-data">
				<input type="submit" name="ongl2" value="OFF RP3">
				</form>
				</td>
				<td>
				<form action = "http://192.168.10.254:5000/ALLoff" method = "POST" 
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
                <form action = "http://192.168.10.254:5000/upload-csv-uploaded" method = "POST" 
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
                <form action = "http://192.168.10.254:5000/upload/rp2/uploaded" method = "POST" 
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
                <form action = "http://192.168.10.254:5000/upload/rp3/uploaded" method = "POST" 
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
                <form action = "http://192.168.10.254:5000/broadcast/uploaded" method = "POST" 
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

	
@app.route('/video', methods = ['GET', 'POST'])
def fluxvideo():
	return  """<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<title>Draw.io Diagram</title>
<meta http-equiv="refresh" content="0;URL='https://www.draw.io/#G1xuYxujKCMeLJPSVjUAx_gAy5DjpPnthM'"/>
<meta charset="utf-8"/>
</head>
<body>
<div class="mxgraph" style="max-width:100%;border:1px solid transparent;" data-mxgraph="{&quot;highlight&quot;:&quot;#0000ff&quot;,&quot;nav&quot;:true,&quot;resize&quot;:true,&quot;xml&quot;:&quot;&lt;mxfile userAgent=\&quot;Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36\&quot; version=\&quot;8.5.11\&quot; editor=\&quot;www.draw.io\&quot; type=\&quot;google\&quot;&gt;&lt;diagram id=\&quot;ac8aae07-9126-7c23-4172-57555d112afe\&quot; name=\&quot;Page-1\&quot;&gt;7VzBkqM2EP0aH+NCCElw3J3dJJdUpWpSlexRC7JNLYYphll78vURRmAjbIyxoRWYuYzVmBa817SeWsIL/LTd/5byl80fSSCihW0F+wX+srBtRJkr/+WW98LiMlIY1mkYqC8dDc/hv0IZLWV9CwPxWvtiliRRFr7UjX4Sx8LPajaepsmu/rVVEtV7feFr0TA8+zxqWv8Og2yjrIh6xwO/i3C9UV27NisOfOf+j3WavMWqv4WNvcNfcXjLS1/qRl83PEh2Jyb8dYGf0iTJik/b/ZOIcmxL2Irzfr1wtLruVMRZlxOocJDvWwRb3Fo5zPtFefjJozdR3sLhQrP3EpzD7YncgbXAn3ebMBPPL9zPj+5kOEjbJttGsoXkR+VOpJnYX7xGVN25jCiRbEWWvsuvqBNsS4H1rrV3J9RQZducsOIoG1fRsK5cHxGRHxQoHQGyzQcI25AAOeYDRCgkQMR8gBwHEiDsXUdIxMGnPNHLVpzE4hwiImgk+at4nNwvOXO7pS0VEc/Cn3X35zBQPfyZhLLjCm5XS2iuhuJr8pb6Qp10mr01PwjZ9hIT23MQYtRhFmn3m/F0LbKG3wNBFQg9n3prXpw5Vn/OyNI94Qy3+x2Ssw6D/ZQ4I/YwnDX8DslZB/0xJc6qUefu3Ijb/Q7JWQdJ1MqZ2IfZP7kYWBLV+qakQVc2ZV8H3C5cISjjTp1xynoyfjV0hqS4g6hrpziWnZ9wnDe/jUW/utYCnymHiKf5GTNxU6MjBIpZm7nLg3J1XTvP1nUF62BvyY7q1nV7ZobWTjBp7WTImGAfMXE+kS/RRbpIO103jBYtnUh2gGKCdMgTY5cHKoFrRAWOdHhqoBGCLcER13yEgGtwHUpM0AjBFuHKjgwdm64o2jJHtEraItVCjXKYPkjUOghO1dJ7S0jTVDDEu0HVev1ob+9DE7XeeBFhf0TEGbaodYOm7RkR7X1oknbEiMDmjbWuY5KipQaumeoIwSpaauCiqY4QrKKlBs4bdYSAFa3Z1ZYrirbMEa2Ktki1YGOc+yBFyzCgou0wd56hfvHQ8Iq2vQ84RXvvdpSJRoQ9vKJt7wNM0ZZ5DXBB18yZLfLqZXPWszhPyg2zpV8ZTWQ8eu8uavxv6fWQNwK9nlbpHJneeysUppPoaLIb9d331HA04o4KZmDVQC/ZupDTGXb3rqILsuS2SUvrfISBzkf08NVp6LyVDHA6wu7dWGR8snoMR9e4HpKiIXf2POhBdCAp1jfm0b773QG3b7Ehi0cPIrlY9gdc4aixw/qqDp1lb0SWhyz+PIjlohQOOOuvs9x3f7buiKIRaZ76C0bOg0iCG1TLIeKDohufo4ajIUma+gtEOkl9h7SrY+OQJNnzIqm3urwqUx9HEhMrRleU4FXAMf/Oz7x2/5fYZw2estxYI+c1S5Mf4imJkvRI3iqMIs3Eo3Ady6YvORPS/jkvhIQ+jz6pA9swCPJuzpZR6oUWda13vXCsiTxUltRPSynWmZjRH5w+pZQG+s1KyrzQr9og6DcrHPNCv9q/CYJ+s3gxL/QJhkS/WVWYNvoUmZT30dyGXR1+2MSPmsp0XvDDZn7UXGGbF/ywqR/NTXV62KjcPzfZqcMPnPvnpjt1+IFz/9yEpw4/cO5vLkBMG/7Goh6BhL90Ohv4deUDDP/cpl168hkSftk8/nxsUZo+/kYv/vof&lt;/diagram&gt;&lt;/mxfile&gt;&quot;,&quot;toolbar&quot;:&quot;pages zoom layers lightbox&quot;,&quot;page&quot;:0}"></div>
<a style="position:absolute;top:50%;left:50%;margin-top:-128px;margin-left:-64px;" href="https://www.draw.io/#G1xuYxujKCMeLJPSVjUAx_gAy5DjpPnthM" target="_blank"><img border="0" src="https://www.draw.io/images/drawlogo128.png"/></a>
</body>
</html>"""

if __name__ == '__main__':
    app.run(host='192.168.10.254')


