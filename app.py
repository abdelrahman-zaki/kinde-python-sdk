from datetime import date
from flask import Flask, render_template
import os
from dotenv import load_dotenv

from kinde_sdk.auth.oauth import OAuth

load_dotenv()

app = Flask(__name__)

kinde_oauth = OAuth(
    framework="flask",
    app=app
)

def get_authorized_data(kinde_oauth):
    user = kinde_oauth.get_user_info()
    return {
        "id": user.get("id"),
        "user_given_name": user.get("given_name"),
        "user_family_name": user.get("family_name"),
        "user_email": user.get("email"),
        "user_picture": user.get("picture"),
    }

@app.route('/')
def index():
    data = {"current_year": date.today().year}
    template = "logged_out.html"
    if kinde_oauth.is_authenticated():
        data.update(get_authorized_data(kinde_oauth))        
        template = "home.html"
    return render_template(template, **data)

if __name__ == '__main__':
    app.run(debug=True)