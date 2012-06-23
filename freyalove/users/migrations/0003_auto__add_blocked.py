# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Blocked'
        db.create_table('users_blocked', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('belongs_to', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['users.Profile'])),
            ('block_profile_id', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('users', ['Blocked'])


    def backwards(self, orm):
        # Deleting model 'Blocked'
        db.delete_table('users_blocked')


    models = {
        'users.blocked': {
            'Meta': {'object_name': 'Blocked'},
            'belongs_to': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['users.Profile']"}),
            'block_profile_id': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'users.friendship': {
            'Meta': {'unique_together': "(('to_profile', 'from_profile'),)", 'object_name': 'Friendship'},
            'added': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2012, 6, 23, 0, 0)'}),
            'from_profile': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_unused_'", 'to': "orm['users.Profile']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'to_profile': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'friends'", 'to': "orm['users.Profile']"})
        },
        'users.profile': {
            'Meta': {'object_name': 'Profile'},
            'age': ('django.db.models.fields.CharField', [], {'max_length': '3', 'blank': 'True'}),
            'fb_id': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'fb_link': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'fb_profile_pic': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'fb_username': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['users']