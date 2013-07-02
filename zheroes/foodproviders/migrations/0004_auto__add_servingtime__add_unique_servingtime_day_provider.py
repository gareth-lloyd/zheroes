# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ServingTime'
        db.create_table(u'foodproviders_servingtime', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('day', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('provider', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['foodproviders.FoodProvider'])),
            ('breakfast', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('morning', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('lunch', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('afternoon', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('dinner', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'foodproviders', ['ServingTime'])

        # Adding unique constraint on 'ServingTime', fields ['day', 'provider']
        db.create_unique(u'foodproviders_servingtime', ['day', 'provider_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'ServingTime', fields ['day', 'provider']
        db.delete_unique(u'foodproviders_servingtime', ['day', 'provider_id'])

        # Deleting model 'ServingTime'
        db.delete_table(u'foodproviders_servingtime')


    models = {
        u'foodproviders.entryrequirement': {
            'Meta': {'object_name': 'EntryRequirement'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'requirement': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '64'})
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
        },
        u'foodproviders.servingtime': {
            'Meta': {'unique_together': "(('day', 'provider'),)", 'object_name': 'ServingTime'},
            'afternoon': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'breakfast': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'day': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'dinner': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lunch': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'morning': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'provider': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['foodproviders.FoodProvider']"})
        }
    }

    complete_apps = ['foodproviders']