from os import getenv

MYSQL_DATABASE= getenv('MYSQL_DATABASE')
JWT_EXPIRES = "expires"
JWT_ROLE = "role"
JWT_USERNAME = "expires"
JWT_EXPIRE_TIME = 60 * 60 * 24
JWT_SECRET_KEY = f"arand0mshitim4d3upSOITWILLBEHARD"
PASSWORD_PEPPER = f"UrThep3pp3r2mys4lt"
REQUESTS_AUTH_TOKEN="authorization"
ORDERS_TABLE_NAME = "reports"
SQL_CONNECTION_STRING = f"mysql+mysqlconnector://root:password@mysql_container/{MYSQL_DATABASE}"
USERS_TABLE_NAME = "users"
MOCK_TOKEN = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHBpcmVzIjoxNjk3MDIyMjMwLCJyb2xlIjoxfQ.7CPV-kIrx7nRjGpFOoTvzD_hwC7LQjjdEHXEx-umS4I'
MOCK_USER = 'a'
MOCK_PASSWORD = 'a5b70203ccfc438b202e6ac3c467df3394a6e45d2a9b733bcf97b4265c3e0f1c'
MOCK_CIVILIAN_TOKEN =  'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHBpcmVzIjoxNjk3MDI5MjM2LCJyb2xlIjoyfQ.1WpIpGrSZ-3GxeB9BRgZVYHKae9VlSvlw3kLOspyM6A'