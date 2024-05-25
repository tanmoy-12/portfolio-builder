from flask_frozen import Freezer
from app import app

freezer = Freezer(app)

@freezer.register_generator
def url_generator():
    yield '/'

if __name__ == '__main__':
    freezer.freeze()
