from jinja2 import Template
import os
import zipfile
import shutil

# Directory to store generated portfolios
output_dir = 'output'

def generate_portfolio(data, photo=None, resume=None):
    name = data.get('name')
    profession = data.get('profession')
    bio = data.get('bio')
    education = data.get('education')
    skills = data.get('skills', '').split(',')
    research = data.get('research', '')
    interests = data.get('interests', '')
    awards = data.get('awards', '')
    email = data.get('email')
    phone = data.get('phone')
    address = data.get('address')
    social_media = data.get('social_media', '')
    projects = data.get('projects', [])
    experience = data.get('experience')
    color_theme = data.get('color_theme')

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
        with open(photo_path, 'wb') as f:
            f.write(photo)

    # Save resume
    resume_path = None
    if resume:
        resume_path = os.path.join(portfolio_path, 'resume.pdf')
        with open(resume_path, 'wb') as f:
            f.write(resume)

    # Load and render the HTML template
    with open('templates/index.html', 'r') as file:
        template = Template(file.read())
    rendered_html = template.render(
        name=name, profession=profession, bio=bio, education=education, skills=skills,
        research=research, interests=interests, awards=awards, email=email, phone=phone,
        address=address, social_media=social_media, projects=projects, experience=experience,
        color_theme=color_theme, photo_path='photo.jpg' if photo else None,
        resume_path='resume.pdf' if resume else None
    )

    # Write the rendered HTML to the file
    with open(os.path.join(portfolio_path, 'index.html'), 'w') as file:
        file.write(rendered_html)

    # Copy the CSS file
    css_src = 'templates/style.css'
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

    return zip_path

# Example usage
if __name__ == '__main__':
    sample_data = {
        'name': 'John Doe',
        'profession': 'Software Developer',
        'bio': 'A passionate developer...',
        'education': 'B.Sc. in Computer Science',
        'skills': 'Python, Flask, HTML, CSS',
        'research': 'My research on AI...',
        'interests': 'AI, Machine Learning',
        'awards': 'Best Developer 2023',
        'email': 'john.doe@example.com',
        'phone': '+1234567890',
        'address': '123 Main St, Anytown, USA',
        'social_media': 'https://github.com/johndoe',
        'projects': [
            {'name': 'Project 1', 'date': '2022', 'details': 'A cool project', 'website': 'https://project1.com'}
        ],
        'experience': '5 years of software development',
        'color_theme': 'blue'
    }
    
    # These should be actual bytes of the files
    sample_photo = None
    sample_resume = None

    zip_file_path = generate_portfolio(sample_data, sample_photo, sample_resume)
    print(f'Portfolio generated and saved to {zip_file_path}')
