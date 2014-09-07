# -*- encoding: utf-8 -*-
from django.db import models
import re
from django.contrib.auth.models import (AbstractBaseUser, PermissionsMixin,
                                        UserManager)
from django.core.mail import send_mail
from django.core import validators
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.utils.http import urlquote


class Tipo(models.Model):

    name=models.CharField(_('Name'), max_length=30, unique=True,
        help_text=_('Nombre tag Tipo de usuario'),editable=False)
    tag=models.CharField(_('Tag'), max_length=30, unique=True,
        help_text=_('Tipo de usuario'))


    class Meta:
        verbose_name = _('Tipo')
        verbose_name_plural = _('Tipos')

    def __unicode__(self):
        return self.tag
    

class User(AbstractBaseUser, PermissionsMixin):
    """
    A custom user class that basically mirrors Django's `AbstractUser` 

    http://www.w3.org/International/questions/qa-personal-names
    """
    username = models.CharField(_('username'), max_length=30, unique=True,
        help_text=_('Required. 30 characters or fewer. Letters, numbers and '
                    '@/./+/-/_ characters'),
        validators=[
            validators.RegexValidator(re.compile('^[\w.@+-]+$'), _('Enter a valid username.'), 'invalid')
        ])
    first_name=models.CharField(_('First name'), max_length=100, blank=True)
    last_name=models.CharField(_('Last name'),max_length=100,blank=True)
    email= models.EmailField(_('Email address'), max_length=254, unique=True, blank=False, 
        help_text='Ingresa un correo')

    is_staff = models.BooleanField(_('staff status'), default=False,
        help_text=_('Designates whether the user can log into this admin '
                    'site.'))

    is_active = models.BooleanField(_('active'), default=True,
        help_text=_('Designates whether this user should be treated as '
                    'active. Unselect this instead of deleting accounts.'))

    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = UserManager()

    tipos= models.ForeignKey(Tipo,default=1)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __unicode__(self):
        return self.username

    def get_absolute_url(self):
        return "/users/%s/" % urlquote(self.username)

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = self.first_name+ " "+self.last_name
        return full_name.strip()

    def get_short_name(self):
        "Returns the short name for the user."
        return self.email.strip()

    def email_user(self, subject, message, from_email=None):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email])

    """Sobrecarca del metodo save para cuando se modifica el estado del usuario"""
    def save(self,*args, **kwargs):
        

        if self.tipos.name == 'user_register':
            self.change_to_register()
        elif self.tipos.name == 'user_organizational':
            self.change_to_organizational()
        elif self.tipos.name=='user_administrator':
            self.change_to_admin()
    
        return super(User, self).save(*args, **kwargs)

    def __init__(self, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)

    def change_to_admin(self):
        self.is_staff = True
        self.is_superuser = True

    def change_to_register(self):
        self.is_staff = False
        self.is_superuser = False

    def change_to_organizational(self):
        self.is_staff = False
        self.is_superuser = False

        
    def is_organizacional(self):
        if(self.tipos.name=="user_organizational"):
            return True



