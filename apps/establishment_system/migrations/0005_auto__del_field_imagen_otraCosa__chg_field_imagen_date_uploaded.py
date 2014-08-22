# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Imagen.otraCosa'
        db.delete_column(u'establishment_system_imagen', 'otraCosa')


        # Changing field 'Imagen.date_uploaded'
        db.alter_column(u'establishment_system_imagen', 'date_uploaded', self.gf('django.db.models.fields.DateTimeField')())

    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'Imagen.otraCosa'
        raise RuntimeError("Cannot reverse this migration. 'Imagen.otraCosa' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'Imagen.otraCosa'
        db.add_column(u'establishment_system_imagen', 'otraCosa',
                      self.gf('django.db.models.fields.CharField')(max_length=30),
                      keep_default=False)


        # Changing field 'Imagen.date_uploaded'
        db.alter_column(u'establishment_system_imagen', 'date_uploaded', self.gf('django.db.models.fields.DateField')(auto_now_add=True))

    models = {
        u'establishment_system.categoria': {
            'Meta': {'object_name': 'Categoria'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'tag': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'establishment_system.establecimiento': {
            'Meta': {'object_name': 'Establecimiento'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '100', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'position': ('geoposition.fields.GeopositionField', [], {'max_length': '42'}),
            'sub_categorias': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['establishment_system.SubCategoria']"}),
            'web_page': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        u'establishment_system.imagen': {
            'Meta': {'object_name': 'Imagen'},
            'date_uploaded': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'establecimientos': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['establishment_system.Establecimiento']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'imagen': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'})
        },
        u'establishment_system.subcategoria': {
            'Meta': {'object_name': 'SubCategoria'},
            'categorias': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['establishment_system.Categoria']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'tag': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['establishment_system']