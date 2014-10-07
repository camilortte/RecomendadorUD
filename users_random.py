from apps.account_system.models import User

for x in xrange(0,100):
	try:
		usuario=User.objects.create_user(
			first_name="Nombre"+str(x),
			last_name="Apelldo"+str(x),
			username="usuario"+str(x),
			email="Usuario"+str(x)+"@hotmail.com"
		)
		usernamesuario.set_password("123456")
		usuario.save()
	except Exception, e:
		print e
		x=x-1

	
 

