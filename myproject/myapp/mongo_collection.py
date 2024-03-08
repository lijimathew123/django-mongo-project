

from django.db import models
from .mongo_connection import db

person_collection = db['democollection']