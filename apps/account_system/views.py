# -*- encoding: utf-8 -*-
from apps.account_system.models import User
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from .forms import CustomLoginForm, ChangePasswordForm
from allauth.account.views import LoginView, SignupView
from .forms import SignupFormSocial, EditAccountForm, MyValidatedForm
from allauth.socialaccount.views import SignupView as SignupSocialAccountView
from allauth.socialaccount.models import SocialAccount
from django.contrib.auth import logout
from django.views.generic.edit import UpdateView
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.views.generic.base import View, TemplateView
from django.contrib import messages
from notifications import notify
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from .forms import SignupFormMio
from django.contrib.auth.decorators import login_required


"""Home"""
def home(request):        
    ctx= {'user': request.user}
    try:
        notifications = request.user.notifications.unread().order_by('-timestamp')[:10]          
        ctx['notifications']=notifications
    except( Exception ):
        print "A error occurred : Anonimous user"
    
    return render(request,'main/home.html', ctx)
                             
"""Cierra sesión del usuario"""
@login_required(login_url='home_url')
def logout_view(request):
    logout(request)  
    return redirect('home_url')

    

#sobrecarga de la vista login de allAuth
class LoginViewWithCustomForm(LoginView):
    form_class = CustomLoginForm
    template_name = "account/login.html"
    success_url = None
    redirect_field_name = "next"




"""View signup from local account """
class SignupViewMio(SignupView):
    template_name = "account/signup.html"
    form_class = SignupFormMio
    redirect_field_name = "next"
    success_url = None


"""View to singup from social account"""   
class SignupSocialView(SignupSocialAccountView):
    template_name = "socialaccount/signup.html"
    form_class = SignupFormSocial


""" View to update profile"""
class ProfileUpdate(UpdateView):
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


"""View to change password"""
@login_required(login_url='home_url')
def change_password(request):
    user_is_social=SocialAccount.objects.filter(
        user=User.objects.get(username=request.user.username))

    if not user_is_social:
        if request.method=='POST':
            formulario= ChangePasswordForm(request.POST)
            if formulario.is_valid():
                try:
                    password=formulario.cleaned_data['oldpassword']
                    user = auth.authenticate(username=request.user, password=password)
                    if user == None:
                        print "Error contraseña no coincide"
                        return render(request, 'account/password_own_set.html', 
                        {'form': formulario,'user':request.user,
                        'error':'Old Password dont match.'})   
                    else:
                        user = User.objects.get(email__exact=request.user.email)
                        password=formulario.cleaned_data['password1']
                        user.set_password(password)
                        user.save()
                        print "SE CAMBIO EL PASSWORD"
                        return render(request, 'account/login.html', 
                            {'form': formulario,'ok':'se cabmio la contraseña correctamente'})
                except Exception:
                    print "Error "
                    return render(request, 'account/password_own_set.html')
            else:
                print "el formulario no es valido"
                formulario=ChangePasswordForm(data=request.POST)
        else:
            formulario= ChangePasswordForm()
        return render(request, 'account/password_own_set.html', {'form':formulario})
    else:
        return redirect('home_url')

#pruebas
class probe(View):

    def get(self, request):
        # TODO: GET ACTIONS
        print "ENTRI EN GET"
        return self.hacer(request)

    def post(self, request):
        print "ENTRI EN POST"
        return self.hacer(request)
 
    def put(self, request):
        # TODO: PUT ACTIONS
        return self.hacer(request)
 
    def delete(self, request):
        # TODO: DELETE ACTIONS
        return self.hacer(request)


    def hacer(self,request):
        form=  MyValidatedForm()
        print "ENtro en probe"
        return render(request,"pruebas.html",{'form':form})

"""class probe(SubscribeFormView):
    template_name = 'pruebas.html'
    form = MyValidatedForm"""

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

    #notify.send(CustomUser.objects.get(id=4), recipient=CustomUser.objects.get(id=1),
    #   verb="Hola, esto es una notificacion", description="Esto es una notificacion que envia hace un buen rato", level="error")

    return redirect('home_url')


"""Marca como leido toas las notificaciones"""
@login_required
def mark_as_read_all(request):
    request.user.notifications.unread().mark_all_as_read()
    return HttpResponseRedirect(reverse('home'))

"""MArca las url como leidas mediante GET"""
@login_required
def marcar_notificacion_como_leida(request):
    try:
        usuario=request.user
        #obtengo el id
        id_notificacion=request.GET.get('id')
        notificacion=usuario.notifications.filter(id=id_notificacion)
        notificacion.mark_all_as_read()
    except Exception:
        print "Usuario anonimo "
    return redirect('home_url')

#Anadir message:
#messages.add_message(request, messages.INFO, 'Hello world.')   