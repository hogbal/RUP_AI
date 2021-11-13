from firebase_admin import credentials
import firebase_admin
from firebase_admin import db
from firebase_admin import auth


cred = credentials.Certificate("../firebase_sdk/rup-ver2-81b50-firebase-adminsdk-tuwg4-592225897b.json")
default_app = firebase_admin.initialize_app(cred,{
	'databaseURL' : 'https://rup-ver2-81b50-default-rtdb.firebaseio.com/'
})

print(db.reference('User').get().get('02Gz1h2mkq6ffRLLPHDTcMHvBbOb2'))
for i in range(1000):
	user = db.reference('User/2Gz1h2mkq6ffRLLPHDTcMHvBbOb2')
	point = int(user.get()['point'])+1
	user.update({'point':point})
