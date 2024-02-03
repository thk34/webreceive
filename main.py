import os
from flask import Flask, request, render_template
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = 'received'
# you can edit the whitelisted extensions here, I think you can allow all extensions if you put * or smth like that
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'mp4', 'mp3', 'sh', 'exe'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return render_template('index.html', message='No file part')
        file = request.files['file']
        if file.filename == '':
            return render_template('index.html', message='No selected file')
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return render_template('index.html', message='File uploaded successfully')

    return render_template('index.html', message='')


if __name__ == '__main__':
    input("Press Enter to start the script...")

    if not os.path.exists('received'):
        os.makedirs('received')

    try:
        app.run(host='192.168.0.10', port=8081)
    except KeyboardInterrupt:
        print("\nServer terminated by user. Cleaning up...")
