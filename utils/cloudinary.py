from os import environ

import cloudinary
import cloudinary.uploader
from cloudinary.utils import cloudinary_url


CLOUD_NAME = environ.get('CLOUDINARY_CLOUD_NAME')
API_KEY = environ.get('CLOUDINARY_API_KEY')
API_SECRET = environ.get('CLOUDINARY_API_SECRET')

# Configuration       
cloudinary.config( 
    cloud_name = CLOUD_NAME,
    api_key = API_KEY,
    api_secret = API_SECRET,
    secure=True
)

def upload_to_cloudinary(file, public_id=None):
    r = cloudinary.uploader.upload(file, public_id=public_id)
    return r['secure_url']