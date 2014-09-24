# -*- encoding: utf-8 -*-
"""
    
    forms.py: Se ecnuentran todos los formularios del sistema de establecimeintos.

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
from django import forms
from django.utils.translation import ugettext, ugettext_lazy as _

#External apps
from haystack.forms import SearchForm

#Models
from .models import (
    SubCategoria,Establecimiento, Categoria, 
    Solicitud,Comentario, Imagen, EstablecimientoTemporal)




class EstablecimientoForm(forms.ModelForm):
    """
        Formuilario de adicion de establecimeintos
    """    
    telefono = forms.RegexField(regex=r'^\+?1?\d{7,15}$', 
                                error_message = ("Numero de telefono invalido."))   
    categorias = forms.ModelChoiceField(queryset=Categoria.objects.all(),
        widget=forms.Select(attrs={'id': 'categoria'}))
    sub_categorias= forms.ModelChoiceField(queryset=SubCategoria.objects.none())
    position = forms.CharField(widget=forms.HiddenInput())


    def __init__(self, *args, **kwargs):   
        super(EstablecimientoForm, self).__init__(*args, **kwargs)          
        try:
            sub_categorias=kwargs.get('instance').sub_categorias  
            try:                    
                sub_categorias = kwargs.get('data').get('sub_categorias')
            except Exception, e:
                print e
            
        except Exception, e:                    
            print "ERROR: ", e   
            try:
                sub_categorias=args[0]['sub_categorias']                
            except Exception, e:
                try:                    
                    sub_categorias = kwargs.get('data').get('sub_categorias')
                except Exception, e:
                    print e
                    return None
        try:
            categoria=SubCategoria.objects.get(id=sub_categorias.id)
        except Exception, e:
            categoria=SubCategoria.objects.get(id=sub_categorias)
        
        
        categoria=Categoria.objects.get(id=categoria.categorias.id)        
        query=Categoria.objects.all()
        query2=SubCategoria.objects.filter(categorias=categoria.id)
        self.fields['categorias']= forms.ModelChoiceField(queryset=query, initial=categoria.id,widget=forms.Select(attrs={'id': 'categoria'}))  
        self.fields['sub_categorias']= forms.ModelChoiceField(queryset=query2, initial=sub_categorias) 

            
    class Meta:
        model = Establecimiento
        fields=['nombre','email','web_page','telefono','address','description','position','categorias','sub_categorias']



class EstablecimientoAdminForm(forms.ModelForm):
    """
        Formulario de establecimientos para el admin de django. 
    """
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





class ComentarioForm(forms.ModelForm):    
    """
        Formulario para crear comentarios
    """
    body= forms.CharField(label="Comentario",min_length=5,  widget=forms.Textarea, 
        max_length=Comentario._meta.get_field('body').max_length)

    class Meta:
        model = Comentario
        fields = ("body",)


class SolicitudAdminForm(forms.ModelForm):
    """
        TODO
        ----
        Formulario de solicitud en el administrador
    """
    class Meta:
        model= Solicitud


class SolicitudForm(forms.ModelForm):
    """
        TODO
        ----
        Formulario de solicitud en el administrador
    """
    class Meta:
        model= Solicitud
        fields=['contenido']



class CategoriasFilterForm(forms.Form):
    """
        Formulario de categorias y subcategorias para el filtro mediante AJAX
    """
    categorias = forms.ModelChoiceField(queryset=Categoria.objects.all(),cache_choices=True,
        widget=forms.Select(attrs={'id': 'categoria'}))
    sub_categorias= forms.ModelChoiceField(queryset=SubCategoria.objects.none(),cache_choices=True,
        widget=forms.Select(attrs={'id': 'id_sub_categorias'})
         )


class EstablecimientoTemporalForm(forms.ModelForm):
    """
        Formulario del establecimiento temporal 
    """
    telefono = forms.RegexField(regex=r'^\+?1?\d{7,15}$', 
                                error_message = ("Numero de telefono invalido."))   
    categorias = forms.ModelChoiceField(queryset=Categoria.objects.all(),
        widget=forms.Select(attrs={'id': 'categoria'}))
    sub_categorias= forms.ModelChoiceField(queryset=SubCategoria.objects.none())
    position = forms.CharField(widget=forms.HiddenInput())


    def __init__(self, *args, **kwargs):   
        super(EstablecimientoTemporalForm, self).__init__(*args, **kwargs)          
        try:
            sub_categorias=kwargs.get('instance').sub_categorias  
            try:                    
                sub_categorias = kwargs.get('data').get('sub_categorias')
            except Exception, e:
                print e
            
        except Exception, e:                    
            print "ERROR: ", e   
            try:
                sub_categorias=args[0]['sub_categorias']                
            except Exception, e:
                try:                    
                    sub_categorias = kwargs.get('data').get('sub_categorias')
                except Exception, e:
                    print e
                    return None
        try:
            categoria=SubCategoria.objects.get(id=sub_categorias.id)
        except Exception, e:
            categoria=SubCategoria.objects.get(id=sub_categorias)
        
        
        categoria=Categoria.objects.get(id=categoria.categorias.id)        
        query=Categoria.objects.all()
        query2=SubCategoria.objects.filter(categorias=categoria.id)
        self.fields['categorias']= forms.ModelChoiceField(queryset=query, initial=categoria.id,widget=forms.Select(attrs={'id': 'categoria'}))  
        self.fields['sub_categorias']= forms.ModelChoiceField(queryset=query2, initial=sub_categorias) 

            
    class Meta:
        model = EstablecimientoTemporal
        fields=['nombre','email','web_page','telefono','address','description','position','categorias','sub_categorias']




class EstablecimientoSearchForm(SearchForm):
    """

    """

    def no_query_found(self):
        return self.searchqueryset.all()


class UploadImageForm(forms.ModelForm):        
    """
        Formulario para subir imagenes.
    """
    class Meta:
        model=Imagen
        fields = ('imagen',)



"""
    Esto lo tengo por si algo falla es debido a la app de selecteble
"""
# import selectable.forms as selectable
# from lookup import EstablecimientoLookUp, SubCategoriaLookUp
# class CategoriasForm2(forms.ModelForm):
    
#     categorias = forms.ModelChoiceField(queryset=Categoria.objects.all(),cache_choices=True,
#         widget=forms.Select(attrs={'id': 'categoria'}))
#     # sub_categorias= forms.ModelChoiceField(queryset=SubCategoria.objects.none(),cache_choices=True
#     #      )
#     autocomplete = forms.CharField(
#         label='Type the name of a fruit (AutoCompleteWidget)',
#         widget=selectable.AutoCompleteWidget(EstablecimientoLookUp),
#         required=False,
#     )
        

#     sub_categorias = selectable.AutoCompleteSelectField(
#         lookup_class=SubCategoriaLookUp,
#         label='SubCategoria',
#         required=False,
#         widget=selectable.AutoComboboxSelectWidget
#     )
#     # categorias = USStateField(widget=USStateSelect, required=False)

#     class Meta:
#         model = Establecimiento
#         fields=['nombre','email','web_page','address','description','position','categorias','sub_categorias']