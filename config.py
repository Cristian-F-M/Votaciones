import os

class Config:
    clave_secreta = os.urandom(24)
    SECRET_KEY = clave_secreta
    SQLALCHEMY_DATABASE_URI = 'mysql://root:BG6Adg4eDF-b4ADFC343H4B12GHgbCaG@monorail.proxy.rlwy.net:57991/votacionescgao'
    SQLALCHEMY_TRACK_MODIFICATIONS = False