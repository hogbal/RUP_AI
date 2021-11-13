from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import auth

def firebase_update(uid):
	if db.reference('User').get().get(uid):
		user = db.reference('User/'+uid)
		point = int(user.get()['point'])+1
		user.update({'point':point})
	else:
		print('Firebase Error')

