# -*- encoding: utf-8 -*-
from django.contrib import admin
from .models import Categoria, Establecimiento, SubCategoria
from .forms import CategoriasForm

from django import forms
from apps.djadmin_ext.helpers import BaseAjaxModelAdmin
from apps.djadmin_ext.admin_forms import BaseAjaxModelForm


class EstablecimientoAdminForm(BaseAjaxModelForm):
    
    ajax_change_fields = ["categorias"]
    categorias = forms.ModelChoiceField(queryset=Categoria.objects.all(),cache_choices=True)
    sub_categorias= forms.ModelChoiceField(queryset=SubCategoria.objects.all(),cache_choices=True)

    @property
    def dynamic_fields(self):
        selecte_categoria=  self.get_selected_value('categorias')
        if not selecte_categoria:
            return {}

        sub_categorias = SubCategoria.objects.filter(categorias=selecte_categoria)
        fields = {}
        fields['sub_categorias'] = lambda:forms.ModelChoiceField(queryset=sub_categorias,cache_choices=True)
        return fields

    def create_field_and_assign_initial_value(self, queryset, selected_value):
        return lambda: super(EstablecimientoAdminForm, self).create_field_and_assign_initial_value(queryset, selected_value)

    class Meta(object):
        model = Establecimiento

class EstablecimientoAdmin(BaseAjaxModelAdmin):
    form=EstablecimientoAdminForm


admin.site.register(Categoria)
admin.site.register(Establecimiento,EstablecimientoAdmin)
admin.site.register(SubCategoria)

