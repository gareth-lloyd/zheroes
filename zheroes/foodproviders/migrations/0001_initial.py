# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'PostCode'
        db.create_table(u'foodproviders_postcode', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('outward', self.gf('django.db.models.fields.CharField')(max_length=5, db_index=True)),
            ('inward', self.gf('django.db.models.fields.CharField')(max_length=5)),
            ('location', self.gf('django.contrib.gis.db.models.fields.PointField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'foodproviders', ['PostCode'])

        # Adding unique constraint on 'PostCode', fields ['outward', 'inward']
        db.create_unique(u'foodproviders_postcode', ['outward', 'inward'])

        # Adding model 'EntryRequirement'
        db.create_table(u'foodproviders_entryrequirement', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('requirement', self.gf('django.db.models.fields.CharField')(unique=True, max_length=2)),
        ))
        db.send_create_signal(u'foodproviders', ['EntryRequirement'])

        # Adding model 'FoodProvider'
        db.create_table(u'foodproviders_foodprovider', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('zheroes_id', self.gf('django.db.models.fields.IntegerField')()),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('cost', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('food_type', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('organisation_type', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('time', self.gf('django.db.models.fields.CharField')(max_length=512, null=True, blank=True)),
            ('means_of_entry', self.gf('django.db.models.fields.CharField')(max_length=512, null=True, blank=True)),
            ('eligibility', self.gf('django.db.models.fields.CharField')(max_length=512, null=True, blank=True)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('post_code', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['foodproviders.PostCode'], null=True, blank=True)),
            ('email', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
            ('website', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
            ('telephone', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
        ))
        db.send_create_signal(u'foodproviders', ['FoodProvider'])

        # Adding M2M table for field requirements on 'FoodProvider'
        m2m_table_name = db.shorten_name(u'foodproviders_foodprovider_requirements')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('foodprovider', models.ForeignKey(orm[u'foodproviders.foodprovider'], null=False)),
            ('entryrequirement', models.ForeignKey(orm[u'foodproviders.entryrequirement'], null=False))
        ))
        db.create_unique(m2m_table_name, ['foodprovider_id', 'entryrequirement_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'PostCode', fields ['outward', 'inward']
        db.delete_unique(u'foodproviders_postcode', ['outward', 'inward'])

        # Deleting model 'PostCode'
        db.delete_table(u'foodproviders_postcode')

        # Deleting model 'EntryRequirement'
        db.delete_table(u'foodproviders_entryrequirement')

        # Deleting model 'FoodProvider'
        db.delete_table(u'foodproviders_foodprovider')

        # Removing M2M table for field requirements on 'FoodProvider'
        db.delete_table(db.shorten_name(u'foodproviders_foodprovider_requirements'))


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
            'means_of_entry': ('django.db.models.fields.CharField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'organisation_type': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'post_code': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['foodproviders.PostCode']", 'null': 'True', 'blank': 'True'}),
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