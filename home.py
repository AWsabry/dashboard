from flask import Flask, redirect, url_for, render_template, request
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import uuid
import pyrebase
from getpass import getpass
from google.cloud.firestore_v1 import Increment

app = Flask(__name__)

cred = credentials.Certificate(
    "x-eats-4a034-firebase-adminsdk-7rdrx-329e05b70d.json")

firebaseConfig = {
    'apiKey': "AIzaSyAQpbI7MDkObxXnHkcwQ7wNGqT3i-wIVic",
    'authDomain': "x-eats-4a034.firebaseapp.com",
    'databaseURL': "https://x-eats-4a034-default-rtdb.firebaseio.com",
    'projectId': "x-eats-4a034",
    'storageBucket': "x-eats-4a034.appspot.com",
    'messagingSenderId': "900670833493",
    'appId': "1:900670833493:web:b3dcee553a6ff88090e5dc",
    'measurementId': "G-93L34JXS0F"

}
firebase_admin.initialize_app(cred)
firebase = pyrebase.initialize_app(firebaseConfig)
storage = firebase.storage()


db = firestore.client()




@app.route('/', methods=['GET', 'POST'])

@app.route("/users")
def users():
    from google.cloud import firestore
    docs = db.collection(u'users').order_by(
        u'firstName', direction=firestore.Query.ASCENDING).stream()
    return render_template('users.html', docs=docs)


@app.route("/orders")
def orders():
    from google.cloud import firestore
    docs = db.collection(u'orders').order_by(
        u'CreatedAt', direction=firestore.Query.DESCENDING).stream()
    return render_template('orders.html', docs=docs)


@app.route("/trueorders")
def trueorders():
    from google.cloud import firestore
    docs = db.collection(u'orders').where(u'Paid', u'==', True).stream()
    return render_template('trueorders.html', docs=docs)



@app.route("/products")
def products():
    docs = db.collection(u'products').order_by(u'category').stream()
    auth = firebase.auth()
    print(auth.current_user)
    # ID = uuid.uuid4()
    delete = db.collection(u'products').document()
    return render_template('products.html', docs=docs, delete=delete)


@app.route("/addProduct", methods=['POST', 'GET'])
def addProduct():
    if request.method == "POST":
        try:
            pname = request.form['pname']
            Description = request.form['Description']
            Price = request.form['Price']
            id = request.form['id']
            img = request.files['img']
            auth = firebase.auth()
            email = "admin@admin.com"
            password = "123456"
            path_on_cloud = pname
            path_local = img            
            user = auth.sign_in_with_email_and_password(email, password)
            storage.child(path_on_cloud).put(path_local, user['idToken'])
            url = storage.child(path_on_cloud).get_url(user['idToken'])
            new_doc_ref = db.collection('products').document(id)
            category = request.form['Category']
            if category == 'a':
                category = 'sandwitches'
            elif category == 'b':
                category = "meals"
            new_doc_ref.set({
                'name': pname,
                'price': int(Price),
                'image': url,
                'id': int(id),
                'description': Description,
                'category': category
            })
            print(pname)
            print(Description)
            print(Price)
        except Exception as e:
            print(str(e))
    else:
        print("ERROR")
    return render_template('addProduct.html', title='addProduct')



if __name__ == '__main__':

    app.run(port=5000, debug=True)
