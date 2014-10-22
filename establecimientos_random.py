from apps.establishment_system.models import Establecimiento, SubCategoria
import random
def random_float(low, high):
	return random.random()*(high-low) + low


for x in xrange(1,100):
	try:
		x1=random_float(4.569001,4.580145)
		y1=random_float(-74.166523,-74.142748)

		establecimiento = Establecimiento(
			nombre="Establecimiento"+str(x),
			email="establecimient"+str(x)+"@hotmail.com",
			address="Direccion inventada "+str(x),
			description="Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod"\
				"tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam,"\
				"quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo"\
				"consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse"\
				"cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non"\
				"proident, sunt in culpa qui officia deserunt mollit anim id est laborum."+str(x),
			position="POINT (-73.0371090000000009 3.1283569999999998)",
			sub_categorias=SubCategoria.objects.get(id=10), 
			web_page="http://establecimiento"+str(x)+".com"
		)
		establecimiento.save()
	except Exception, e:
		print e
		x=x-1
	