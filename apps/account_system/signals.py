# -*- encoding: utf-8 -*-
from allauth.account.signals import user_signed_up, user_logged_in, email_confirmed
from allauth.socialaccount.signals import pre_social_login
from django.dispatch import receiver
from django.db.models import signals
from apps.recommender_system.models import EstablecimientosRecommender
from .models import User
from django.db.models.signals import post_save
from notifications import notify
from avatar.models import Avatar
import urllib, cStringIO
from PIL import Image
# When account is created via social, fire django-allauth signal to populate Django User record.
 
@receiver(user_signed_up)
def user_signed_up_(request, user, sociallogin=None, **kwargs):
    '''
    When a social account is created successfully and this signal is received,
    django-allauth passes in the sociallogin param, giving access to metadata on the remote account, e.g.:
 
    sociallogin.account.provider  # e.g. 'twitter' 
    sociallogin.account.get_avatar_url()
    sociallogin.account.get_profile_url()
    sociallogin.account.extra_data['screen_name']
 
    See the socialaccount_socialaccount table for more in the 'extra_data' field.
    '''
    print "Entro, esto es lo que vale user="
    if sociallogin:
        # Extract first / last names from social nets and store on User record
        print "Entro, esto es lo que vale user=",user
        if sociallogin.account.provider == 'twitter':
            name = sociallogin.account.extra_data['name']
            user.full_name = name.split()[0]
            user.short_name = name.split()[1]
 
        if sociallogin.account.provider == 'facebook':
            user.full_name = sociallogin.account.extra_data['first_name']
            user.short_name = sociallogin.account.extra_data['last_name']
 
        if sociallogin.account.provider == 'google':
            user.full_name = sociallogin.account.extra_data['given_name']
            user.short_name = sociallogin.account.extra_data['family_name']
        
        #user.is_active=0

        user.save()
        print "GUARDO ",user
        print "GUARDO ",user.full_name
        print "GUARDO ",user.short_name
        print sociallogin.account.extra_data

@receiver(user_logged_in)
def set_gender(sender, user, **kwargs):
    print "USER LOGEGEADO\n"


@receiver(pre_social_login)
def cosa(sender,sociallogin=None,request=None, **kwargs):
    print "PRE SOCIAL LOGIn "


@receiver(email_confirmed)
def email_confirmed(sender,**kwargs):
    print "mail confirmado"





# def change_imagen(url,user):    
#     avatar = Avatar(user=user, primary=True)
#     file = cStringIO.StringIO(urllib.urlopen(url).read())
#     image_file = Image.open(file) 
#     avatar.avatar.save(user.name+user.id, image_file)
#     avatar.save()
#     #avatar_updated.send(sender=Avatar, user=request.user, avatar=avatar)


#    https://graph.facebook.com/10203117078182580/picture?type=square&height=600&width=600&return_ssl_resources=1