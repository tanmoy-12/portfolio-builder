from flask import Flask, render_template, request, send_file
from jinja2 import Template
import os
import zipfile
import shutil

app = Flask(__name__)

# Directory to store generated portfolios
output_dir = 'output'

@app.route('/')
def home():
    return render_template('form.html')

@app.route('/generate', methods=['POST'])
def generate_portfolio():
    name = request.form.get('name')
    profession = request.form.get('profession')
    bio = request.form.get('bio')
    education = request.form.get('education')
    skills = request.form.get('skills', '').split(',')
    research = request.form.get('research', '')
    interests = request.form.get('interests', '')
    awards = request.form.get('awards', '')
    email = request.form.get('email')
    phone = request.form.get('phone')
    address = request.form.get('address')
    social_media = request.form.get('social_media', '')
    projects = request.form.getlist('projects')
    experience = request.form.get('experience')
    color_theme = request.form.get('color_theme')
    photo = request.files.get('photo')
    resume = request.files.get('resume')

    # Prepare the output directory
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    portfolio_path = os.path.join(output_dir, f'{name}_portfolio')
    if not os.path.exists(portfolio_path):
        os.makedirs(portfolio_path)

    # Save photo
    photo_path = None
    if photo:
        photo_path = os.path.join(portfolio_path, 'photo.jpg')
        photo.save(photo_path)

    # Save resume
    resume_path = None
    if resume:
        resume_path = os.path.join(portfolio_path, 'resume.pdf')
        resume.save(resume_path)

    # Load and render the HTML template
    with open('portfolio_templates/index.html', 'r') as file:
        template = Template(file.read())
    rendered_html = template.render(
        name=name, profession=profession, bio=bio, education=education, skills=skills,
        research=research, interests=interests, awards=awards, email=email, phone=phone,
        address=address, social_media=social_media, projects=projects, experience=experience,
        color_theme=color_theme, photo_path=photo_path, resume_path=resume_path
    )

    # Write the rendered HTML to the file
    with open(os.path.join(portfolio_path, 'index.html'), 'w') as file:
        file.write(rendered_html)

    # Copy the CSS file
    css_src = 'portfolio_templates/style.css'
    css_dst = os.path.join(portfolio_path, 'style.css')
    if os.path.exists(css_src):
        shutil.copyfile(css_src, css_dst)

    # Create a zip file
    zip_path = os.path.join(output_dir, f'{name}_portfolio.zip')
    with zipfile.ZipFile(zip_path, 'w') as zipf:
        zipf.write(os.path.join(portfolio_path, 'index.html'), 'index.html')
        zipf.write(os.path.join(portfolio_path, 'style.css'), 'style.css')
        if photo_path:
            zipf.write(photo_path, 'photo.jpg')
        if resume_path:
            zipf.write(resume_path, 'resume.pdf')

    return send_file(zip_path, as_attachment=True)

@app.route('/preview', methods=['POST'])
def preview_portfolio():
    name = request.form.get('name')
    profession = request.form.get('profession')
    bio = request.form.get('bio')
    education = request.form.get('education')
    skills = request.form.get('skills', '').split(',')
    research = request.form.get('research', '')
    interests = request.form.get('interests', '')
    awards = request.form.get('awards', '')
    email = request.form.get('email')
    phone = request.form.get('phone')
    address = request.form.get('address')
    social_media = request.form.get('social_media', '')
    projects = request.form.getlist('projects')
    experience = request.form.get('experience')
    color_theme = request.form.get('color_theme')
    photo = request.files.get('photo')
    resume = request.files.get('resume')

    photo_path = None
    if photo:
        photo_path = os.path.join(output_dir, 'photo.jpg')
        photo.save(photo_path)

    resume_path = None
    if resume:
        resume_path = os.path.join(output_dir, 'resume.pdf')
        resume.save(resume_path)

    with open('portfolio_templates/index.html', 'r') as file:
        template = Template(file.read())
    rendered_html = template.render(
        name=name, profession=profession, bio=bio, education=education, skills=skills,
        research=research, interests=interests, awards=awards, email=email, phone=phone,
        address=address, social_media=social_media, projects=projects, experience=experience,
        color_theme=color_theme, photo_path=photo_path, resume_path=resume_path
    )

    return render_template('preview.html', rendered_html=rendered_html, form_data=request.form)

@app.route('/<path:path>')
def catch_all(path):
    return render_template(f'{path}.html')

if __name__ == '__main__':
    app.run(debug=True)
