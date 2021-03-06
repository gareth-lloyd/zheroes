# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'FoodProvider.post_code'
        db.delete_column(u'foodproviders_foodprovider', 'post_code_id')

        # Adding field 'FoodProvider.location'
        db.add_column(u'foodproviders_foodprovider', 'location',
                      self.gf('django.contrib.gis.db.models.fields.PointField')(null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'FoodProvider.post_code'
        db.add_column(u'foodproviders_foodprovider', 'post_code',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['foodproviders.PostCode'], null=True, blank=True),
                      keep_default=False)

        # Deleting field 'FoodProvider.location'
        db.delete_column(u'foodproviders_foodprovider', 'location')


    models = {
        u'foodproviders.entryrequirement': {
            'Meta': {'object_name': 'EntryRequirement'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'requirement': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '2'})
        },
        u'foodproviders.foodprovider': {
            'Meta': {'object_name': 'FoodProvider'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'cost': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'eligibility': ('django.db.models.fields.CharField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'food_type': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.contrib.gis.db.models.fields.PointField', [], {'null': 'True', 'blank': 'True'}),
            'means_of_entry': ('django.db.models.fields.CharField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'organisation_type': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'requirements': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['foodproviders.EntryRequirement']", 'symmetrical': 'False'}),
            'telephone': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'time': ('django.db.models.fields.CharField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'}),
            'website': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'zheroes_id': ('django.db.models.fields.IntegerField', [], {})
        },
        u'foodproviders.postcode': {
            'Meta': {'unique_together': "(('outward', 'inward'),)", 'object_name': 'PostCode'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inward': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'location': ('django.contrib.gis.db.models.fields.PointField', [], {'null': 'True', 'blank': 'True'}),
            'outward': ('django.db.models.fields.CharField', [], {'max_length': '5', 'db_index': 'True'})
        }
    }

    complete_apps = ['foodproviders']