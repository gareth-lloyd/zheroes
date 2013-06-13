# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding M2M table for field requirements_satisfied on 'PhoneUser'
        m2m_table_name = db.shorten_name(u'smslink_phoneuser_requirements_satisfied')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('phoneuser', models.ForeignKey(orm[u'smslink.phoneuser'], null=False)),
            ('entryrequirement', models.ForeignKey(orm[u'foodproviders.entryrequirement'], null=False))
        ))
        db.create_unique(m2m_table_name, ['phoneuser_id', 'entryrequirement_id'])


        # Changing field 'PhoneUser.post_code'
        db.alter_column(u'smslink_phoneuser', 'post_code_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['foodproviders.PostCode'], null=True))

    def backwards(self, orm):
        # Removing M2M table for field requirements_satisfied on 'PhoneUser'
        db.delete_table(db.shorten_name(u'smslink_phoneuser_requirements_satisfied'))


        # Changing field 'PhoneUser.post_code'
        db.alter_column(u'smslink_phoneuser', 'post_code_id', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['foodproviders.PostCode']))

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
            'number': ('django.db.models.fields.CharField', [], {'max_length': '20', 'db_index': 'True'}),
            'post_code': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['foodproviders.PostCode']", 'null': 'True', 'blank': 'True'}),
            'requirements_satisfied': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['foodproviders.EntryRequirement']", 'symmetrical': 'False'})
        }
    }

    complete_apps = ['smslink']