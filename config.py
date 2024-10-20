import os


class Config:
    BASE_DIR = os.path.abspath(
        path=os.path.dirname(p=__file__)
    )
    CSRF_ENABLED = True
    CSRF_SESSION_KEY = 'eb0d34205e0a439ec61b670e569dc5bde960b51029c4d5395a50914c89ed6a4d'
    SECRET_KEY = '8ef29ca19723fd725980bad98d2dbd71d3b74d4805af99494dbc346aeec29b5d'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = 'uploads'


class DevConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(Config.BASE_DIR, 'app.db')
    


class ProdConfig(Config):
    DEBUG = False
    # Database URLs:    dialect+driver://username:password@host:port/database
    # MySQL: 
    #   default:        mysql://username:password@host:port/database
    #   mysqlclient:    mysql+mysqldb://username:password@host:port/database
    #   PyMySQL:        mysql+pymysql://username:password@host:port/database
    # PostgreSQL:
    #   default:        postgresql://username:password@host:port/database
    #   psycopg2:       postgresql+psycopg2://username:password@host:port/database
    #   pg8000:         postgresql+pg8000://username:password@host:port/database
    SQLALCHEMY_DATABASE_URI = ...
    