from flask import Flask

app = Flask(__name__)
app.secret_key = "anything-super-secret"  

from app import routes  
