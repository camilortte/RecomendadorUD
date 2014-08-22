# -*- encoding: utf-8 -*-
from django import forms
from .models import SubCategoria,Categoria,Establecimiento
from django.utils.translation import ugettext, ugettext_lazy as _


"""Formuilario del admin para las notificaciones"""
class CategoriasForm(forms.ModelForm):
   
    #categorias = forms.ModelChoiceField(queryset=Categoria.objects.all(),cache_choices=True)   
    #sub_categorias= forms.ModelChoiceField(queryset=SubCategoria.objects.all(),cache_choices=True)

    class Meta:
        model = Establecimiento

    """def clean(self):
            	    super(CategoriasForm, self).clean() 	    
            	    self.query=SubCategoria.objects.filter(categorias=self.cleaned_data['categorias'])
            	    self.fields['sub_categorias'].queryset =self.query
            	    print self.query
            	    #categoriasss=self.categorias
            	    return self.cleaned_data """
	        

