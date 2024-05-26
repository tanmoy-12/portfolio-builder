import os
from jinja2 import Template
import zipfile
import shutil

def generate_portfolio(data):
    output_dir = 'output'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    portfolio_path = os.path.join(output_dir, f"{data['name']}_portfolio")
    if not os.path.exists(portfolio_path):
        os.makedirs(portfolio_path)

    with open('portfolio_templates/index.html', 'r') as file:
        template = Template(file.read())
    rendered_html = template.render(data)

    with open(os.path.join(portfolio_path, 'index.html'), 'w') as file:
        file.write(rendered_html)

    with open(os.path.join('static', 'style.css'), 'r') as file:
        css_content = file.read()

    with open(os.path.join(portfolio_path, 'style.css'), 'w') as file:
        file.write(css_content)

    zip_path = os.path.join(output_dir, f"{data['name']}_portfolio.zip")
    with zipfile.ZipFile(zip_path, 'w') as zipf:
        zipf.write(os.path.join(portfolio_path, 'index.html'), 'index.html')
        zipf.write(os.path.join(portfolio_path, 'style.css'), 'style.css')
        if 'photo_path' in data:
            zipf.write(data['photo_path'], 'photo.jpg')
        if 'resume_path' in data:
            zipf.write(data['resume_path'], 'resume.pdf')

    return zip_path
