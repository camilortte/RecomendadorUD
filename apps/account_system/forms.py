# -*- encoding: utf-8 -*-
from django import forms
from .models import User
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.utils.translation import ugettext, ugettext_lazy as _
from parsley.decorators import parsleyfy
from notifications.models import Notification
from django.conf import settings


##############################Forms CustomUser########################################################
class CustomUserCreationForm(forms.ModelForm):
    """
    A form that creates a user, with no privileges, from the given username and
    password.
    """

    MIN_CHARS_FIRST_NAME=3
    MIN_CHARS_LAST_NAME=3

    error_messages = {
        'duplicate_username': _("A user with that username already exists."),
        'password_mismatch': _("The two password fields didn't match."),
    }
    username = forms.RegexField(label=_("Username"), max_length=30,
        regex=r'^[\w.@+-]+$',
        help_text=_("Required. 30 characters or fewer. Letters, digits and "
                      "@/./+/-/_ only."),
        error_messages={
            'invalid': _("This value may contain only letters, numbers and "
                         "@/./+/-/_ characters.")})
    password1 = forms.CharField(label=_("Password"),
        widget=forms.PasswordInput)
    password2 = forms.CharField(label=_("Password confirmation"),
        widget=forms.PasswordInput,
        help_text=_("Enter the same password as above, for verification."))

    class Meta:
        # Point to our CustomUser here instead of default `User`
        model = User
        fields = ("username",)

    def clean_username(self):
        # Since User.username is unique, this check is redundant,
        # but it sets a nicer error message than the ORM. See #13147.
        username = self.cleaned_data["username"]
        try:
            # Refer to our CustomUser here instead of default `User`
            User._default_manager.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(self.error_messages['duplicate_username'])

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'])
        return password2

    def clean_first_name(self):
        diccionario_limpio = self.cleaned_data      
        nombre = diccionario_limpio.get('first_name')     

        if len(first_name) < self.MIN_CHARS_FIRST_NAME:
            raise forms.ValidationError("El campo nombre debe ser mayor de "+
                self.MIN_CHARS_FIRST_NAME+ 
                " caracteres")
        elif self.hasNumbers(first_name):
            raise forms.ValidationError("El campo no puede tener numeros")
     
        return first_name 

    def clean_last_name(self):
        diccionario_limpio = self.cleaned_data      
        apellido = diccionario_limpio.get('last_name')     

        if len(last_name) < self.MIN_CHARS_FIRST_NAME:
            raise forms.ValidationError("El campo apellido debe ser mayor de "+
                self.MIN_CHARS_LAST_NAME+ 
                " caracteres")
        elif self.hasNumbers(last_name):
            raise forms.ValidationError("El campo no puede tener numeros")
     
        return last_name 

    def hasNumbers(self,inputString):
        return any(char.isdigit() for char in inputString)


    def save(self, commit=True):
        print "Entro"
        # Make sure we pass back in our CustomUserCreationForm and not the
        # default `UserCreationForm`
        user = super(CustomUserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class CustomUserChangeForm(forms.ModelForm):
    username = forms.RegexField(
        label=_("Username"), max_length=30, regex=r"^[\w.@+-]+$",
        help_text=_("Required. 30 characters or fewer. Letters, digits and "
                      "@/./+/-/_ only."),
        error_messages={
            'invalid': _("This value may contain only letters, numbers and "
                         "@/./+/-/_ characters.")})
    password = ReadOnlyPasswordHashField(label=_("Password"),
        help_text=_("Raw passwords are not stored, so there is no way to see "
                    "this user's password, but you can change the password "
                    "using <a href=\"password/\">this form</a>."))

    class Meta:
        # Point to our CustomUser here instead of default `User`
        model = User

    def __init__(self, *args, **kwargs):
        # Make sure we pass back in our CustomUserChangeForm and not the
        # default `UserChangeForm`
        super(CustomUserChangeForm, self).__init__(*args, **kwargs)
        f = self.fields.get('user_permissions', None)
        if f is not None:
            f.queryset = f.queryset.select_related('content_type')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


##############################Forms Allauth######################################################

#Extencion para el account signup 
class SignupExtendForm(forms.Form):

    MIN_CHARS_FIRST_NAME=3
    MIN_CHARS_LAST_NAME=3

    first_name = forms.CharField(max_length=200, label='Nombres',required=True)
    last_name = forms.CharField(max_length=200, label='Apellidos',required=True)

    def signup(self, request, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()

    class Meta:
        model = User 

    def clean_first_name(self):
        diccionario_limpio = self.cleaned_data      
        first_name = diccionario_limpio.get('first_name')     

        if len(first_name) < self.MIN_CHARS_FIRST_NAME:
            raise forms.ValidationError("El campo nombre debe ser mayor de "+
                str(self.MIN_CHARS_FIRST_NAME)+ 
                " caracteres")
        elif self.hasNumbers(first_name):
            raise forms.ValidationError("El campo no puede tener numeros")
     
        return first_name 

    def clean_last_name(self):
        diccionario_limpio = self.cleaned_data      
        last_name = diccionario_limpio.get('last_name')     

        if len(last_name) < self.MIN_CHARS_FIRST_NAME:
            raise forms.ValidationError("El campo apellido debe ser mayor de "+
                str(self.MIN_CHARS_LAST_NAME)+ 
                " caracteres")
        elif self.hasNumbers(last_name):
            raise forms.ValidationError("El campo no puede tener numeros")
     
        return last_name 

    def hasNumbers(self,inputString):
        return any(char.isdigit() for char in inputString)



#Estas llamadas deben realizarse en este orden debido a que la clase
# SignuPExtendForm se usa posterioromente en la llamada de las librerias
from allauth.utils import set_form_field_order
from allauth.account.forms import   PasswordField, SetPasswordField
from allauth.account.forms import LoginForm
from allauth.account.forms import SignupForm
from allauth.socialaccount.forms import SignupForm as SingupFormSoialAccount


#Sobrecarga de el formulario de login allAuth
@parsleyfy
class CustomLoginForm(LoginForm):   
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class':'input-block-level',
            'required':True,'placeholder':'Pass'}))
    remember = forms.BooleanField(label=_("Remember Me"),
                                  required=False)
    error_css_class = 'error'
    required_css_class = 'required'

    def  __init__(self, *args, **kwargs):
        super(CustomLoginForm, self).__init__(*args, **kwargs)        
        #seleccionamos los campos que queremos que aparescan
        login_widget = forms.TextInput(attrs={'placeholder':
                                          _('Username'),
                                          'autofocus': 'autofocus',
                                          'class':'input-block-leveel',
                                          'required':True})
        login_field = forms.CharField(label=_("Username"),
                                          widget=login_widget,
                                          max_length=30)
        self.fields["login"] = login_field
        set_form_field_order(self,  ["login", "password", "remember",])


#Sobrecargar del formulario Signup de Allauth

class SignupFormMio(SignupForm):

    def __init__(self, *args, **kwargs):
        super(SignupFormMio, self).__init__(*args, **kwargs)

      

#Sobrecarga del formulaio signup social de Allauth
class SignupFormSocial(SingupFormSoialAccount):

    def __init__(self, *args, **kwargs):
        super(SignupFormSocial, self).__init__(*args, **kwargs)


"""This forms is about de update user profile by own user"""
@parsleyfy
class EditAccountForm(forms.ModelForm):    
    first_name=forms.CharField(label='Nombres', min_length=3, max_length=100,required=True)
    last_name=forms.CharField(label='Apellidos', min_length=3, max_length=100,required=True)
    username=forms.CharField(
        label='Nombre de usuario', 
        min_length=settings.ACCOUNT_USERNAME_MIN_LENGTH, 
        max_length=30,
        required=True)
    class Meta:
        model = User
        fields = ('username','email','first_name', 'last_name')#,'password1', 'password2')
        # or 
        #exclude = ('is_superuser',) #and whatever else you wish to exclude.


"""Form to change password own """
class ChangePasswordForm(forms.Form):
    oldpassword = PasswordField(label=_("Current Password"))
    password1 = SetPasswordField(label=_("New Password"))
    password2 = PasswordField(label=_("New Password (again)"))

    def clean_password2(self):
        if ("password1" in self.cleaned_data
                and "password2" in self.cleaned_data):
            if (self.cleaned_data["password1"]
                    != self.cleaned_data["password2"]):
                raise forms.ValidationError(_("You must type the same password"
                                              " each time."))
        return self.cleaned_data["password2"]

#Prueba de la app parslefy
@parsleyfy
class MyValidatedForm(forms.Form):
    surname = forms.CharField(label='Surname', min_length=3, max_length=20,required=True)
    age = forms.DecimalField(min_value=18, max_value=99)

# from django.core.exceptions import ValidationError
# def validate_even(value):
#     print "Lleeeeeeeeeeeeeeeeeeeeeeeeeeega: ",value
#     if value == "-1":
#         pass
#     else:
#         if User.objects.filter(id=int(value)):
#             pass
#         else:
#             raise ValidationError(u'Selecciona una opción valida.')



class NotificationForm(forms.ModelForm):
    """
        Formuilario del admin para las notificaciones
        Se modifico el __init__ para permitir crear notificaciones para todos los usuarios
    """   
    author = forms.ModelChoiceField(
        label=_("Autor"),
        queryset=User.objects.all().order_by('username'),
        widget=forms.Select(),
        help_text=u'De parte de')
    destinario = forms.ModelChoiceField(
        label=_("Destinatario"),
        queryset=User.objects.all().order_by('username'),
        help_text=u'Destinado al usuario (Si la opcion "Todos los usuarios" esta activa, esta opción será ignorada)')
    titulo = forms.CharField(
        label=_("Titulo"),
        max_length=255,
        help_text=u'Titulo de la notificacion')
    descripcion=forms.CharField(
        label=_("Descripcion"),
        widget = forms.Textarea, 
        required=False,
        help_text=u'Descripcion de la notificación')
    todos= forms.BooleanField(
        label=_("Totodos los usuarios"),
        help_text=u'Seleccionar esta opcion para enviar a todos los usuarios activos del sistema.'
        )

    es_instancea=False
    class Meta:
        model= Notification
        fields = ('author','destinario','level', 'titulo','descripcion','unread','public','timestamp')

 
    def __init__(self, *args, **kwargs):
        """
            Agregamos los items de envio a todos
        """
        super(NotificationForm, self).__init__(*args, **kwargs)
        # self.fields['destinario'].choices = \
        #     list(self.fields['destinario'].choices) + [('-1', 'Todos')]
        
        try:
            instance=kwargs['instance']
        except Exception:
            instance=False

        if instance:
            self.es_instancea=True            

            #self.fields['author'].widget.attrs['disabled'] = "disable"
            #self.fields['destinario'].widget.attrs['disabled'] = "disable"

            self.fields['descripcion'].initial=instance.description
            self.fields['titulo'].initial=instance.verb
            self.fields['author'].initial=instance.actor
            self.fields['destinario'].initial=instance.recipient
            self.fields['todos'].widget = forms.HiddenInput()

        
    def clean(self):
        """
            Validamos que si se selecciono todos, entonces borramos los errores de
            destinatarios, de lo contrario borramos los errores de todos y retornamos
            la data
        """
        cleaned_data = super(NotificationForm, self).clean()
        if not self.es_instancea:   
            print "Entro en clean"         
            todos = cleaned_data.get("todos")
            destinario = cleaned_data.get("destinario")

            print "TODOS: ",todos
            print "Destinario: ", destinario

            if todos:
                try:
                    del self.errors['destinario']
                except Exception:
                    pass
                return cleaned_data
            else: 
                if destinario:
                    del self._errors['todos']
        else:
            del self._errors['todos']
        
        return cleaned_data
            
        

