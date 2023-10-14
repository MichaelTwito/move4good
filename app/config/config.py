from os import getenv

class ConfigClass:
    MYSQL_DATABASE= getenv('MYSQL_DATABASE')
    REQUESTS_AUTH_TOKEN= "authorization"
    MYSQL_USER = getenv('MYSQL_USER')
    MYSQL_ROOT_PASSWORD = getenv('MYSQL_ROOT_PASSWORD')
    MYSQL_HOST = getenv('MYSQL_HOST')
    JWT_EXPIRES = "expires"
    JWT_EXPIRE_TIME = 60 * 60 * 24
    JWT_ROLE = "role"
    JWT_USERNAME = "username"
    JWT_SECRET_KEY = f"arand0mshitim4d3upSOITWILLBEHARD"
    PASSWORD_PEPPER = f"UrThep3pp3r2mys4lt"
    # SQL_CONNECTION_STRING = f"mysql+mysqlconnector://{MYSQL_USER}:{MYSQL_ROOT_PASSWORD}@{MYSQL_HOST}/{MYSQL_DATABASE}"
    SQL_CONNECTION_STRING = f"mysql+mysqlconnector://admin:admin@localhost/move4good"