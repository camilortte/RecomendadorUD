"""
Por eliminar
"""

# from dajax.core import Dajax
# from dajaxice.utils import deserialize_form
# from .forms import ComentarioForm
# from dajaxice.decorators import dajaxice_register

# # @dajaxice_register
# # def send_form(request, form):
# #     dajax = Dajax()
# #     form = ComentarioForm(deserialize_form(form))
# #     print form

# #     if form.is_valid():
# #         dajax.remove_css_class('#my_form input', 'error')
# #         dajax.alert("Form is_valid(), your username is: %s" % form.cleaned_data.get('username'))
# #         print "entor Is valid"
# #     else:
# #         dajax.remove_css_class('#my_form input', 'error')
# #         print "Errores: ",form.errors
# #         for error in form.errors:
# #             #print "El error: ",error
# #             #dajax.add_css_class('#id_%s' % error, 'error')
# #             dajax.append('#boton', 'innerHTML', 'errorssssssssssss')
# #             dajax.assign('#boton', 'value', 'Click here!')
# #             dajax.assign('#result', 'value',"ASIGNO LO QUE SE ME VENGA EN GANA")
# #         print "ENtro noes valids"

# #     return dajax.json()
