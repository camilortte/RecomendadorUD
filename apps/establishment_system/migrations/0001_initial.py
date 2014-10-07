# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Categoria'
        db.create_table(u'establishment_system_categoria', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nombre', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
            ('tag', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'establishment_system', ['Categoria'])

        # Adding model 'SubCategoria'
        db.create_table(u'establishment_system_subcategoria', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nombre', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
            ('tag', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('categorias', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['establishment_system.Categoria'])),
        ))
        db.send_create_signal(u'establishment_system', ['SubCategoria'])

        # Adding model 'Establecimiento'
        db.create_table(u'establishment_system_establecimiento', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nombre', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75, null=True, blank=True)),
            ('web_page', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=100, unique=True, null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('position', self.gf('geoposition.fields.GeopositionField')(max_length=42)),
            ('sub_categorias', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['establishment_system.SubCategoria'])),
        ))
        db.send_create_signal(u'establishment_system', ['Establecimiento'])

        # Adding model 'Imagen'
        db.create_table(u'establishment_system_imagen', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('imagen', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('establecimientos', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['establishment_system.Establecimiento'])),
        ))
        db.send_create_signal(u'establishment_system', ['Imagen'])


    def backwards(self, orm):
        # Deleting model 'Categoria'
        db.delete_table(u'establishment_system_categoria')

        # Deleting model 'SubCategoria'
        db.delete_table(u'establishment_system_subcategoria')

        # Deleting model 'Establecimiento'
        db.delete_table(u'establishment_system_establecimiento')

        # Deleting model 'Imagen'
        db.delete_table(u'establishment_system_imagen')


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