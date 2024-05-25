from flask_frozen import Freezer
from app import app

freezer = Freezer(app)

# Define the URLs that should be frozen
@freezer.register_generator
def url_generator():
    # Add specific routes here
    yield '/'

if __name__ == '__main__':
    freezer.freeze()
