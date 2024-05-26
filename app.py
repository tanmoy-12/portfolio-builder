from flask import Flask, render_template, request, send_file
from werkzeug.utils import secure_filename
import os
import shutil
from scripts.generate_portfolio import generate_portfolio

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def index():
    return render_template('form.html')

@app.route('/generate', methods=['POST'])
def generate():
    form_data = request.form.to_dict()
    files = request.files

    if 'photo' in files and files['photo'].filename != '':
        photo = files['photo']
        photo_filename = secure_filename(photo.filename)
        photo_path = os.path.join(app.config['UPLOAD_FOLDER'], photo_filename)
        photo.save(photo_path)
        form_data['photo_path'] = photo_path

    if 'resume' in files and files['resume'].filename != '':
        resume = files['resume']
        resume_filename = secure_filename(resume.filename)
        resume_path = os.path.join(app.config['UPLOAD_FOLDER'], resume_filename)
        resume.save(resume_path)
        form_data['resume_path'] = resume_path

    zip_path = generate_portfolio(form_data)

    shutil.rmtree(UPLOAD_FOLDER)

    return send_file(zip_path, as_attachment=True, attachment_filename=os.path.basename(zip_path))

if __name__ == '__main__':
    app.run(debug=True)
