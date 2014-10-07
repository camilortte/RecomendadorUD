# -*- encoding: utf-8 -*-

"""
    
    Views: Encontramos todas las vistas del sistema de usuarios.

    @author     Camilo Ramírez
    @contact    camilolinchis@gmail.com 
                camilortte@hotmail.com
                @camilortte on Twitter
    @copyright  Copyright 2014-2015, RecomendadorUD
    @license    GPL
    @date       2014-10-10
    @satus      Pre-Alpha
    @version=   0..215


"""

#Django 
from django.shortcuts import redirect, get_object_or_404
from django.utils.decorators import method_decorator
from django.views.generic.edit import UpdateView
from django.contrib.auth.decorators import login_required
from django.views.generic.base import View, TemplateView
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse,lazy

#External apps
from notifications import notify
from allauth.account.views import LoginView, SignupView, PasswordSetView
from allauth.socialaccount.views import SignupView as SignupSocialAccountView
from allauth.socialaccount.models import SocialAccount

#Internal apps
from apps.account_system.models import User

#Forms
from .forms import SignupFormSocial, EditAccountForm, SignupFormMio, CustomLoginForm
                         
    
class LoginViewWithCustomForm(LoginView):
    u"""
        sobrecarga de la vista login de allAuth
    """
    form_class = CustomLoginForm
    template_name = "account/login.html"
    success_url = None
    redirect_field_name = "next"


class RegistroConvencioanl(SignupView):
    u"""
        View signup from local account 
    """
    template_name = "account/signup.html"
    form_class = SignupFormMio
    redirect_field_name = "next"
    success_url = None



class RegistroSocial(SignupSocialAccountView):
    u"""
        View to singup from social account
    """   
    template_name = "socialaccount/signup.html"
    form_class = SignupFormSocial


class ProfileUpdate(UpdateView):
    u""" 
        View to update profile
    """
    model = User
    form_class = EditAccountForm
    template_name = 'account/edit_my_profile_user.html'
    success_url="/home/"

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        ctx = super(ProfileUpdate, self).get_context_data(**kwargs)
        usuario=self.request.user
        cuentas=SocialAccount.objects.filter(user=usuario)
        print "Cuentas: ",cuentas
        if  cuentas:
            print "Cuentas no vacio"
            ctx['social_accounts'] = cuentas

        return ctx

    @method_decorator(login_required(login_url='home_url'))
    def dispatch(self, *args, **kwargs):
        return super(ProfileUpdate, self).dispatch(*args, **kwargs)


class ChangePass(PasswordSetView):
    """
        DEPRECATE
        ----------
        No funciona, nunca entra, solo llama al padre
    """
    template_name = "account/password_redasdset.html"
    success_url=lazy(reverse, str)("profile_url")


class MarcarTodasNotificacionesLeidas(View):
    u"""
        Marca como leido toas las notificaciones
    """
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(MarcarTodasNotificacionesLeidas, self).dispatch(*args, **kwargs)

    def get(self, request):
        # TODO: GET ACTIONS
        request.user.notifications.unread().mark_all_as_read()
        return redirect('notificaciones_url')


class MarcarNotificacionLeida(View):
    u"""
        Marca como leido toas las notificaciones
    """
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(MarcarNotificacionLeida, self).dispatch(*args, **kwargs)

    def get(self, request):
        # TODO: GET ACTIONS
        try:
            usuario=request.user
            #obtengo el id
            id_notificacion=request.GET.get('id')
            notificacion=usuario.notifications.filter(id=id_notificacion)
            notificacion.mark_all_as_read()
        except Exception:
            print "Usuario anonimo "
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))



class ProfileUser(TemplateView):
    u"""
        Clase encargada de mostrar el perfil del usuario activo
    """
    template_name="account/profile.html"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ProfileUser, self).dispatch(*args, **kwargs)


class PorfilesUsers(TemplateView):
    u"""
        Clase que se encarga de mostrar los perfiles del usuario seleccionado
    """
    template_name="account/profiles.html"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(PorfilesUsers, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        """
            Se agrega el contexto del usuario
        """
        print "El contexto es: ",kwargs['pk']
        context = super(PorfilesUsers, self).get_context_data(**kwargs)
        #context['now'] = timezone.now()
        context['usuario']= get_object_or_404(User,pk=kwargs['pk'])
        return context


class NotificacionesView(TemplateView):
    u"""
        Vista de todas las notificaciones del usuario
    """
    template_name="account/notificaciones.html"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(NotificacionesView, self).dispatch(*args, **kwargs)

 


#########################################################################################################################
#####################################################                 ###################################################
#####################################################    SIGNALS      ###################################################
#####################################################                 ###################################################
#########################################################################################################################
from django.db.models.signals import post_save,pre_delete
from django.dispatch.dispatcher import receiver
from .models import User
from apps.establishment_system.models import Comentario
from datetime import datetime
from apps.externals.djangoratings.models import Vote
from apps.recommender_system.models import EstablecimientosRecommender


@receiver(post_save, sender=User)
def created_user(sender, instance, created, **kwargs):
    u"""
        Cuando una establecimiento se borra tambíen se borrara los votos
    """    
    if created:
        saludo=u"Bienvenido "+instance.first_name+". De parte del equipo de RecomendadorUD te queremos dar un gran "\
        " saludo de bienvenida, esperamos que tu estadía sea lo más prolongada posible y que te la pases de lo mejor.\n"\
        "Gracias :D ".decode('utf-8')
        notify.send(
                    instance,
                    recipient=instance,
                    verb="Bienvenida",                    
                    description=saludo,
                    timestamp=datetime.now()
                ) 

@receiver(pre_delete, sender=User)
def delete_user(sender,instance,using,**kwargs):
    #Eliminamos sus comentarios
    Comentario.objects.filter(author=instance.id).delete()

    #Eliminamos sus votos    
    Vote.objects.filter(user=instance.id).delete()    
    recommender=EstablecimientosRecommender()    
    recommender.precompute()


#########################################################################################################################
#####################################################                 ###################################################
#####################################################    TEST         ###################################################
#####################################################                 ###################################################
#########################################################################################################################

# """View to change password"""
# @login_required(login_url='home_url')
# def change_password(request):
#     user_is_social=SocialAccount.objects.filter(
#         user=User.objects.get(username=request.user.username))

#     if not user_is_social:
#         if request.method=='POST':
#             formulario= ChangePasswordForm(request.POST)
#             if formulario.is_valid():
#                 try:
#                     password=formulario.cleaned_data['oldpassword']
#                     user = auth.authenticate(username=request.user, password=password)
#                     if user == None:
#                         print "Error contraseña no coincide"
#                         return render(request, 'account/password_own_set.html', 
#                         {'form': formulario,'user':request.user,
#                         'error':'Old Password dont match.'})   
#                     else:
#                         user = User.objects.get(email__exact=request.user.email)
#                         password=formulario.cleaned_data['password1']
#                         user.set_password(password)
#                         user.save()
#                         print "SE CAMBIO EL PASSWORD"
#                         return render(request, 'account/login.html', 
#                             {'form': formulario,'ok':'se cabmio la contraseña correctamente'})
#                 except Exception:
#                     print "Error "
#                     return render(request, 'account/password_own_set.html')
#             else:
#                 print "el formulario no es valido"
#                 formulario=ChangePasswordForm(data=request.POST)
#         else:
#             formulario= ChangePasswordForm()
#         return render(request, 'account/password_own_set.html', {'form':formulario})
#     else:
#         return redirect('home_url')


#pruebas
class probe(View):

    def get(self, request):
        # TODO: GET ACTIONS
        print "ENTRI EN GET"
        return self.hacer(request)

#DEV
"""Envia notificaciones """
@login_required
def send_notification(request):
    messages.success(request, "Send notificaction")    
    recipient_username = request.POST.get('recipient_username', None)

    if recipient_username:
        recipients = User.objects.filter(username=recipient_username)
    else:
        recipients = User.objects.all()

    for recipient in recipients:
        print "Request user ",request.user, "Tipo=",type(request.user)

        print "Recipient ", recipient ,"Tipo=",type(recipient)
        notify.send(
            request.user,
            recipient=recipient,
            verb="request.POST.get('verb', '')"
        )


    return redirect('home_url')

# """Cierra sesión del usuario"""
# @login_required(login_url='home_url')
# def logout_view(request):
#     logout(request)  
#     return redirect('home_url')

#Anadir message:
#messages.add_message(request, messages.INFO, 'Hello world.')   
