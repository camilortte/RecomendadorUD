# -*- encoding: utf-8 -*-
from django import forms
from .models import SubCategoria,Categoria,Establecimiento, Categoria
from django.utils.translation import ugettext, ugettext_lazy as _
from .models import Comentario

"""Formuilario del admin para las notificaciones"""
class CategoriasForm(forms.ModelForm):
    
    categorias = forms.ModelChoiceField(queryset=Categoria.objects.all(),cache_choices=True,
        widget=forms.Select(attrs={'id': 'categoria'}))
    sub_categorias= forms.ModelChoiceField(queryset=SubCategoria.objects.none(),cache_choices=True
         )

    def __init__(self, *args, **kwargs):        
        
        super(CategoriasForm, self).__init__(*args, **kwargs)   
        try:            
            print kwargs
            try:
                categoria_id=kwargs.get('data').get('categorias')   
                query=SubCategoria.objects.filter(categorias=Categoria.objects.get(id=categoria_id))
                self.fields['sub_categorias']= forms.ModelChoiceField(queryset=query,cache_choices=True)  
            except Exception:
                #Admin
                try:
                    categoria_id= args[0].get('categorias')
                    query=SubCategoria.objects.filter(categorias=Categoria.objects.get(id=categoria_id))
                    self.fields['sub_categorias']= forms.ModelChoiceField(queryset=query,cache_choices=True)  
                except Exception,e:
                    #Admin update
                    #print e
                    sub_categoria=kwargs.get('instance').sub_categorias
                    #print "Sub categorias: ",sub_categoria
                    categoria_initial_id=SubCategoria.objects.get(tag=sub_categoria).categorias_id
                    #categoria_initial_tag= SubCategoria.objects.get(tag=sub_categoria).tag
                    #print "CAtegoria intial tag: ",categoria_initial_tag
                    self.fields['categorias'] = forms.ModelChoiceField(
                        queryset=Categoria.objects.all(),
                        widget=forms.Select(attrs={'id': 'categoria'}),
                        initial=categoria_initial_id
                    )   

                    sub_categoria_id=SubCategoria.objects.get(tag=sub_categoria).id
                    self.fields['sub_categorias'] = forms.ModelChoiceField(
                        queryset=SubCategoria.objects.filter(categorias=Categoria.objects.filter(
                            id=categoria_initial_id)),
                            initial=sub_categoria_id                         
                    )      
                    
             
        except Exception, e:            
            print "ERROR: ", e
            #raise e
        
          
             

    class Meta:
        model = Establecimiento



class ComentarioForm(forms.ModelForm):    
    body= forms.CharField(min_length=5,  widget=forms.Textarea, 
        max_length=Comentario._meta.get_field('body').max_length)
    class Meta:
        model = Comentario
        fields = ("body",)

from django.contrib.comments.forms import CommentForm

class CommentForm(CommentForm):
    ottras= "cosa"

CommentForm.base_fields.pop('email')
CommentForm.base_fields.pop('url')
