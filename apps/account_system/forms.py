# -*- encoding: utf-8 -*-
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.utils.translation import ugettext, ugettext_lazy as _
from allauth.utils import set_form_field_order
from allauth.account.forms import   PasswordField, SetPasswordField
from .models import User
from parsley.decorators import parsleyfy

##############################Forms CustomUser#################################################################
class CustomUserCreationForm(forms.ModelForm):
    """
    A form that creates a user, with no privileges, from the given username and
    password.
    """
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


##############################Forms Allauth################################################################# 

#Extencion para el account signup 
class SignupExtendForm(forms.Form):
    first_name = forms.CharField(max_length=30, label='Voornaam',required=True)
    last_name = forms.CharField(max_length=30, label='Achternaam',required=False)

    def signup(self, request, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()

#Estas llamadas deben realizarse en este orden debido a que la clase SignuPExtendForm se usa posterioromente
# en la llamada de las librerias
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
@parsleyfy
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


