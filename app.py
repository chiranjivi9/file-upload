import os
from flask import Flask, flash, request, redirect, url_for, render_template,send_from_directory
from werkzeug.utils import secure_filename
from firebase import firebase
from firebase.firebase import FirebaseApplication
from werkzeug.utils import secure_filename
from form import Uploadfiles

firebase = FirebaseApplication('https://fileupload-7a83f.firebaseio.com/', authentication=None)

UPLOAD_FOLDER = 'upload_files'

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__, instance_relative_config=True)
app.secret_key = os.urandom(24)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# APP_ROOT= os.path.dirname(os.path.asbpath(__file__))

count = 0
@app.route('/', methods=['POST', 'GET'])
def fupload():
    form= Uploadfiles()
    if request.method=='POST':
        global count
        count += 1
        putData={
            'URL': form.download_URL.data
        }
        firebase.put('/UPLOAD_URL',f'uploads-{count}', putData)
        return 'check firebase DB for url'
    return render_template('uploadstry.html', form=form)







def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
@app.route('/uploads', methods=['GET', 'POST'])
def upload_file():
    global filename
    if request.method == 'POST':
        # storageRef=upload_file()
        # check if the post request has the file part
        if 'file' not in request.files:
            print('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            print('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))


            return "success"
    return render_template('uploadstry.html')
