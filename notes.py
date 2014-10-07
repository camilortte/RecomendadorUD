from django.contrib.sites.models import Site
Site.objects.create(domain='localhost:8000',name='localhost:8000')
id_site=Site.objects.get(name='localhost:8000')

from allauth.socialaccount.models import SocialApp

t1=SocialApp.objects.create(provider='twitter',name='Twitter',client_id='6cO8HoMTIuOaMAyFNT1yxSea0',secret='XolegaJvDWvyGREcziHv8q7GkyKsXNUjEmJh0lVRY4HM8B2N0c')
t1.sites.add(id_site)

f1=SocialApp.objects.create(provider='facebook',name='Facebook',client_id='543350239130783',secret='7a6bc2911c658b8418131d057ab44335')
f1.sites.add(id_site)

g1=SocialApp.objects.create(provider='google',name='Google',client_id='481544714964-9jtarg0p2l7qm4ep7ea4u3ors9hpd43b.apps.googleusercontent.com',secret='HY5M6bs8qpX02dcSsqKtCJ3-')
g1.sites.add(id_site)
#Despues de esto es necesario agregar agregar localhost:8000m a cada elemento de socalaccount
