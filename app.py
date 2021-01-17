from flask import Flask, render_template, request, url_for, flash, redirect
from pymongo import MongoClient



client = MongoClient("mongodb+srv://root:root@don.lf9z1.mongodb.net/don_db?retryWrites=true&w=majority")
db = client.get_database('don_db')
records = db.don_collecte
inscrits = db.abonnes


app = Flask(__name__)

@app.route('/')
def main():
    return render_template('main.html')

@app.route('/info')
def info():
    post = {"info": "value_info"}
    return render_template('info.html', post=post)

@app.route('/form',methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        nom = request.form['nom']
        prenom = request.form['prenom']
        mail = request.form['mail']
        valeur = float(request.form['valeur'])
        records.insert_one({'nom': nom, 'prenom': prenom, 'mail': mail, 'valeur': valeur})
    return render_template('form.html')

@app.route('/register',methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        inscrits.insert_one({'email': email, 'password': password})
    return render_template('register.html')

@app.route('/result',methods = ['POST', 'GET'])
def result():
    tot_don = records.aggregate([{"$group":{"_id":"La valeur totale des dons :","La valeur total des dons :":{"$sum":"$don"}}}])
    for total in tot_don:
      return render_template("result.html",result = total)

if __name__ == '__main__':
   app.run(debug = True)