"""
Por eliminar
"""

# from .models import Categoria,SubCategoria,Establecimiento
# from selectable.base import ModelLookup 
# from selectable.registry import registry

# class EstablecimientoLookUp(ModelLookup):
#     model = Establecimiento
#     search_fields = ('nombre__icontains','email', )

# class SubCategoriaLookUp(ModelLookup):
#     model = SubCategoria
#     search_fields = ('tag__icontains', )

#     def get_query(self, request, term):
#         results = super(SubCategoriaLookUp, self).get_query(request, term)
#         print request.GET
#         categoria = request.GET.get('categorias', '')        
#         print "Categoria: ",categoria
#         if categoria:
#             results = results.filter(categorias=categoria)
#         else:
#             results = results.none()
#         return results

# class CategoriaLookUp(ModelLookup):
#     model = Categoria
#     search_fields = ('tag__icontains', )



# registry.register(EstablecimientoLookUp)
# registry.register(SubCategoriaLookUp)
# registry.register(CategoriaLookUp)