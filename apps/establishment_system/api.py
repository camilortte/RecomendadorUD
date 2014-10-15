# -*- encoding: utf-8 -*-

"""
    
    api.py: Tenemos las APIS REST del sistema de establecimientos

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
#External apps
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets

#Internal apps
from apps.establishment_system.models  import SubCategoria, Establecimiento, Imagen

#Serializers
from .serializers import SubCategoriaSerializer, EstablecimientoSerializer, ImagenSerializer

     
class SubCategoriaViewSet(viewsets.ReadOnlyModelViewSet):
    """
        API Rest de las subcategorias, requiere permisos para ver
    """
    queryset = SubCategoria.objects.all()
    serializer_class = SubCategoriaSerializer
    #authentication_classes = (  SessionAuthentication, BasicAuthentication,)
    #permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        try:
            queryset = SubCategoria.objects.all()
            categoria = self.request.QUERY_PARAMS.get('categoria', None)        
            if categoria is not None:
                queryset = SubCategoria.objects.filter(categorias=categoria)
        except Exception,e:
            print e
            return SubCategoria.objects.none()

        return queryset




class EstablecimientoViewSet(viewsets.ModelViewSet):
    """
        DEPRECATE
        ---------
        API Rest de los establecimientos
    """
    queryset = Establecimiento.objects.all()
    serializer_class = EstablecimientoSerializer


class ImagenViewSet(viewsets.ModelViewSet):
    """
        API Rest de las imagenes
    """
    queryset = Imagen.objects.all()
    serializer_class = ImagenSerializer