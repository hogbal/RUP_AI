from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import auth

def firebase_update():
	uid = "5aefF22EfVdWslKaWQ7CSZecUjW2"
	if db.reference('Users2').get().get(uid):
		user = db.reference('Users2/'+uid)
		point = str(int(user.get()['point'])+1)
		user.update({'point':point})
	else:
		print('error')

