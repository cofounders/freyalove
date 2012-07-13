# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Wink'
        db.create_table('users_wink', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('to_profile', self.gf('django.db.models.fields.related.ForeignKey')(related_name='wink_to', to=orm['users.Profile'])),
            ('from_profile', self.gf('django.db.models.fields.related.ForeignKey')(related_name='wink_from', to=orm['users.Profile'])),
            ('received', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('users', ['Wink'])

        # Adding field 'Profile.profile'
        db.add_column('users_profile', 'profile',
                      self.gf('django.db.models.fields.TextField')(default='', blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting model 'Wink'
        db.delete_table('users_wink')

        # Deleting field 'Profile.profile'
        db.delete_column('users_profile', 'profile')


    models = {
        'users.blocked': {
            'Meta': {'object_name': 'Blocked'},
            'belongs_to': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['users.Profile']"}),
            'block_profile_id': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'users.friendship': {
            'Meta': {'unique_together': "(('to_profile', 'from_profile'),)", 'object_name': 'Friendship'},
            'added': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2012, 7, 13, 0, 0)'}),
            'from_profile': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_unused_'", 'to': "orm['users.Profile']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'to_profile': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'friends'", 'to': "orm['users.Profile']"})
        },
        'users.profile': {
            'Meta': {'object_name': 'Profile'},
            'age': ('django.db.models.fields.CharField', [], {'max_length': '3', 'blank': 'True'}),
            'banned': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'fb_id': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'fb_link': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'fb_profile_pic': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'fb_username': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'profile': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        'users.wink': {
            'Meta': {'object_name': 'Wink'},
            'from_profile': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'wink_from'", 'to': "orm['users.Profile']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'received': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'to_profile': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'wink_to'", 'to': "orm['users.Profile']"})
        }
    }

    complete_apps = ['users']