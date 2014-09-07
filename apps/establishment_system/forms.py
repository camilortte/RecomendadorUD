# -*- encoding: utf-8 -*-
from django import forms
from .models import SubCategoria,Categoria,Establecimiento, Categoria, Solicitud
from django.utils.translation import ugettext, ugettext_lazy as _
from .models import Comentario, Imagen

"""Formuilario del admin para las notificaciones"""
class EstablecimientoForm(forms.ModelForm):
    
    telefono = forms.RegexField(regex=r'^\+?1?\d{7,15}$', 
                                error_message = ("Numero de telefono invalido."))
    categorias = forms.ModelChoiceField(queryset=Categoria.objects.all(),cache_choices=True,
        widget=forms.Select(attrs={'id': 'categoria'}))
    sub_categorias= forms.ModelChoiceField(queryset=SubCategoria.objects.none(),cache_choices=True
         )

    def __init__(self, *args, **kwargs):        
        
        super(EstablecimientoForm, self).__init__(*args, **kwargs)   
        try: 
            categoria_id=kwargs.get('data').get('categorias')   
            query=SubCategoria.objects.filter(categorias=Categoria.objects.get(id=categoria_id))
            self.fields['sub_categorias']= forms.ModelChoiceField(queryset=query,cache_choices=True)  
                        
        except Exception, e:            
            print "ERROR: ", e
            #raise e
             

    class Meta:
        model = Establecimiento
        fields=['nombre','email','web_page','telefono','address','description','position','categorias','sub_categorias']


class EstablecimientoAdminForm(forms.ModelForm):
    telefono = forms.RegexField(regex=r'^\+?1?\d{7,15}$', 
                                error_message = ("Numero de telefono invalido."),required=False)
    categorias = forms.ModelChoiceField(queryset=Categoria.objects.all(),cache_choices=True,
        widget=forms.Select(attrs={'id': 'categoria'}))
    sub_categorias= forms.ModelChoiceField(queryset=SubCategoria.objects.none(),cache_choices=True
         )

    def __init__(self, *args, **kwargs):        
        
        super(EstablecimientoAdminForm, self).__init__(*args, **kwargs)   
        try: 
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
        fields=['nombre','administradores','email','telefono','web_page','address','description','visible','position','categorias','sub_categorias']


import selectable.forms as selectable
from lookup import EstablecimientoLookUp, SubCategoriaLookUp
class CategoriasForm2(forms.ModelForm):
    
    categorias = forms.ModelChoiceField(queryset=Categoria.objects.all(),cache_choices=True,
        widget=forms.Select(attrs={'id': 'categoria'}))
    # sub_categorias= forms.ModelChoiceField(queryset=SubCategoria.objects.none(),cache_choices=True
    #      )
    autocomplete = forms.CharField(
        label='Type the name of a fruit (AutoCompleteWidget)',
        widget=selectable.AutoCompleteWidget(EstablecimientoLookUp),
        required=False,
    )
        

    sub_categorias = selectable.AutoCompleteSelectField(
        lookup_class=SubCategoriaLookUp,
        label='SubCategoria',
        required=False,
        widget=selectable.AutoComboboxSelectWidget
    )
    # categorias = USStateField(widget=USStateSelect, required=False)

    class Meta:
        model = Establecimiento
        fields=['nombre','email','web_page','address','description','position','categorias','sub_categorias']


class ComentarioForm(forms.ModelForm):    
    body= forms.CharField(label="Comentario",min_length=5,  widget=forms.Textarea, 
        max_length=Comentario._meta.get_field('body').max_length)
    class Meta:
        model = Comentario
        fields = ("body",)


class SolicitudAdminForm(forms.ModelForm):
    class Meta:
        model= Solicitud

# from django.contrib.comments.forms import CommentForm

# class CommentForm(CommentForm):
#     ottras= "cosa"

# CommentForm.base_fields.pop('email')
# CommentForm.base_fields.pop('url')


from haystack.forms import SearchForm


class EstablecimientoSearchForm(SearchForm):

    def no_query_found(self):
        return self.searchqueryset.all()


class UploadImageForm(forms.ModelForm):        

    class Meta:
        model=Imagen
        fields = ('imagen',)