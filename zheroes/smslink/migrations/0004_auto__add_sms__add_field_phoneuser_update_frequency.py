# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'SMS'
        db.create_table(u'smslink_sms', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('phone_user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['smslink.PhoneUser'])),
            ('text', self.gf('django.db.models.fields.CharField')(max_length=170)),
        ))
        db.send_create_signal(u'smslink', ['SMS'])

        # Adding field 'PhoneUser.update_frequency'
        db.add_column(u'smslink_phoneuser', 'update_frequency',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting model 'SMS'
        db.delete_table(u'smslink_sms')

        # Deleting field 'PhoneUser.update_frequency'
        db.delete_column(u'smslink_phoneuser', 'update_frequency')


    models = {
        u'foodproviders.entryrequirement': {
            'Meta': {'object_name': 'EntryRequirement'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'requirement': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '2'})
        },
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
            'last_contacted': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'number': ('django.db.models.fields.CharField', [], {'max_length': '20', 'db_index': 'True'}),
            'post_code': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['foodproviders.PostCode']", 'null': 'True', 'blank': 'True'}),
            'requirements_satisfied': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['foodproviders.EntryRequirement']", 'symmetrical': 'False'}),
            'update_frequency': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'smslink.sms': {
            'Meta': {'object_name': 'SMS'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'phone_user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['smslink.PhoneUser']"}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '170'})
        }
    }

    complete_apps = ['smslink']