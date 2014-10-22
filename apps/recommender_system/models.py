# -*- encoding: utf-8 -*-
"""
    
    models: modelos del sistema recmendador.

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
from __future__ import unicode_literals
from django.db import models
from apps.account_system.models import User
from django.contrib.sites.models import Site
from django.utils.encoding import python_2_unicode_compatible
from recommends.providers import recommendation_registry, RecommendationProvider
from recommends.algorithms.pyrecsys import RecSysAlgorithm

from apps.establishment_system.models import Establecimiento
from apps.externals.djangoratings.models import Vote as votos
from django.contrib.sites.models import Site

# @python_2_unicode_compatible
# class Product(models.Model):
#     """A generic Product"""
#     name = models.CharField(blank=True, max_length=100)
#     sites = models.ManyToManyField(Site)

#     def __str__(self):
#         return self.name

#     @models.permalink
#     def get_absolute_url(self):
#         return ('product_detail', [self.id])

#     def sites_str(self):
#         return ', '.join([s.name for s in self.sites.all()])
#     sites_str.short_description = 'sites'


# @python_2_unicode_compatible
# class Vote(models.Model):
#     """A Vote on a Product"""
#     user = models.ForeignKey(User, related_name='votos')
#     product = models.ForeignKey(Product)
#     site = models.ForeignKey(Site)
#     score = models.FloatField()

#     def __str__(self):
#         return "Vote"


# class ProductRecommendationProvider(RecommendationProvider):

#     algorithm=RecSysAlgorithm()

#     def get_users(self):
#         return User.objects.filter(is_active=True, votos__isnull=False).distinct()

#     def get_items(self):
#         return Product.objects.all()

#     def get_ratings(self, obj):
#         return Vote.objects.filter(product=obj)

#     def get_rating_score(self, rating):
#         return rating.score

#     def get_rating_site(self, rating):
#         return rating.site

#     def get_rating_user(self, rating):
#         return rating.user

#     def get_rating_item(self, rating):
#         return rating.product



class EstablecimientosRecommender(RecommendationProvider):

    #k=100 por defecto
    algorithm=RecSysAlgorithm()

    def get_users(self):
        print "Entro get_users"
        return User.objects.filter(is_active=True).distinct()

    def get_items(self):
        print "Entro get_items"
        return Establecimiento.objects.all()

    def get_ratings(self, obj):
        print "Entro get_ratings"
        return obj.rating.get_ratings()

    def get_rating_score(self, rating):
        print "Entro get_rating_score"
        return rating.score

    def get_rating_site(self, rating):        
        print "Entro get_rating_site"
        return Site.objects.get_current()#rating.ip_address

    def get_rating_user(self, rating):
        print "Entro get_rating_user"
        return rating.user

    def get_rating_item(self, rating):
        print "Entro get_rating_item"
        return rating.product


#recommendation_registry.register(Vote, [Product], ProductRecommendationProvider)
recommendation_registry.register(votos, [Establecimiento], EstablecimientosRecommender)



"""
from apps.recommender_system.models import EstablecimientosRecommender
from apps.account_system.models import User

recomendador_instance=EstablecimientosRecommender()
recomendador_instance.precompute()

recomendador_instance.storage.get_recommendations_for_user(User.objects.get(id=2))

"""