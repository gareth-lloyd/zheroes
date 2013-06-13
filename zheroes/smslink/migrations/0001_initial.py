# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'PhoneUser'
        db.create_table(u'smslink_phoneuser', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('number', self.gf('django.db.models.fields.CharField')(max_length=20, db_index=True)),
            ('post_code', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['foodproviders.PostCode'])),
        ))
        db.send_create_signal(u'smslink', ['PhoneUser'])


    def backwards(self, orm):
        # Deleting model 'PhoneUser'
        db.delete_table(u'smslink_phoneuser')


    models = {
        u'foodproviders.postcode': {
            'Meta': {'unique_together': "(('outward', 'inward'),)", 'object_name': 'PostCode'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inward': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'location': ('django.contrib.gis.db.models.fields.PointField', [], {'null': 'True', 'blank': 'True'}),
            'outward': ('django.db.models.fields.CharField', [], {'max_length': '5', 'db_index': 'True'})
        },
        u'smslink.phoneuser': {
            'Meta': {'object_name': 'PhoneUser'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'number': ('django.db.models.fields.CharField', [], {'max_length': '20', 'db_index': 'True'}),
            'post_code': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['foodproviders.PostCode']"})
        }
    }

    complete_apps = ['smslink']