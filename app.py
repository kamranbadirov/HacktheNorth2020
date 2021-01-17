from flask import Flask, render_template, request, redirect
from htn_ml import extract_info
import googleapi
import flask, httplib2, json
from oauth2client import client
import os
# pip install oauth2client
# pip install httplib2
#pip install flask
#pip install googleapi
app = Flask(__name__,static_url_path='/static')
IMG_FOLDER = os.path.join('static', 'img')
app.config['UPLOAD_FOLDER'] = IMG_FOLDER


@app.route('/')
def index():
    if 'credentials' not in flask.session:
      return flask.redirect(flask.url_for('oauth2callback'))
    credentials = client.OAuth2Credentials.from_json(flask.session['credentials'])
    if credentials.access_token_expired:
        return flask.redirect(flask.url_for('oauth2callback'))
    full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'gregorlogo.png')
    # print(full_filename)
    return flask.render_template('index.html',logo_path=full_filename)

#Begin oauth callback route
@app.route('/oauth2callback')
def oauth2callback():
  flow = client.flow_from_clientsecrets(
      'credentials.json',
      scope='https://www.googleapis.com/auth/calendar',
      redirect_uri=flask.url_for('oauth2callback', _external=True))
  if 'code' not in flask.request.args:
    auth_uri = flow.step1_get_authorize_url()
    return flask.redirect(auth_uri)
  else:
    auth_code = flask.request.args.get('code')
    credentials = flow.step2_exchange(auth_code)
    flask.session['credentials'] = credentials.to_json()
    return flask.redirect(flask.url_for('index'))


@app.route("/", methods=['POST'])
def caption():
    if(request.method == "POST"):
        f = request.files["image"]
        path = "./static/{}".format(f.filename)
        f.save(path)
        
        a=(request.form.get("t1"))
        b=(request.form.get("t2"))
        r=extract_info(path)
        
        try:
            credentials = client.OAuth2Credentials.from_json(flask.session['credentials'])
        except credError:
            print ("did not assign credentials")
        http_auth = credentials.authorize(httplib2.Http())
        link=""
        # print(r)
        link=googleapi.master(r[0],a,b,r[1],r[2],r[3],r[4], http_auth)
        
        # print(link)
        full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'gregorlogo.png')
    return render_template("index.html", link = link,logo_path=full_filename)


@app.route("/home")
def home():
    return redirect("/")

if __name__ == "__main__":
    app.debug = True
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    

    app.run(host="0.0.0.0")
