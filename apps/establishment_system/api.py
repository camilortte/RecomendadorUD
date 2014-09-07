from apps.establishment_system.models  import SubCategoria, Establecimiento
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from .serializers import SubCategoriaSerializer, EstablecimientoSerializer

 
    

class SubCategoriaViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = SubCategoria.objects.all()
    serializer_class = SubCategoriaSerializer
    authentication_classes = (  SessionAuthentication, BasicAuthentication,)
    permission_classes = (IsAuthenticated,)

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
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Establecimiento.objects.all()
    serializer_class = EstablecimientoSerializer
    #authentication_classes = (BasicAuthentication,)
    #permission_classes = (IsAuthenticated,)


