#Author: Jonathan Ramirez
#Course Number: COSC 499
#Date Completed:4/7/2023
#Description: This program essentially creates the website and local Url so that we are able to put the wanted info onto our site
#Input:N/A
#output: Makes the website exist through http://127.0.0.1:8000 when ran all together with the other files
#things that need attention: being able to change the given Url


from flask import Flask
from views import views
from destiny import rate 

#registers and records operations to executed( activates website)
app = Flask(__name__)
app.register_blueprint(views, url_prefix="")

@app.route("/")
def home:
    return "Hello"
#  this provides the Url and runs the website
if __name__ == '__main__':
    app.run(debug=True, port=8000)
