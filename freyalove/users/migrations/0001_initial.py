# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Profile'
        db.create_table('users_profile', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('age', self.gf('django.db.models.fields.CharField')(max_length=3, blank=True)),
            ('fb_username', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('fb_link', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('fb_id', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
        ))
        db.send_create_signal('users', ['Profile'])

        # Adding model 'Friendship'
        db.create_table('users_friendship', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('to_profile', self.gf('django.db.models.fields.related.ForeignKey')(related_name='friends', to=orm['users.Profile'])),
            ('from_profile', self.gf('django.db.models.fields.related.ForeignKey')(related_name='_unused_', to=orm['users.Profile'])),
            ('added', self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2012, 6, 15, 0, 0))),
        ))
        db.send_create_signal('users', ['Friendship'])

        # Adding unique constraint on 'Friendship', fields ['to_profile', 'from_profile']
        db.create_unique('users_friendship', ['to_profile_id', 'from_profile_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'Friendship', fields ['to_profile', 'from_profile']
        db.delete_unique('users_friendship', ['to_profile_id', 'from_profile_id'])

        # Deleting model 'Profile'
        db.delete_table('users_profile')

        # Deleting model 'Friendship'
        db.delete_table('users_friendship')


    models = {
        'users.friendship': {
            'Meta': {'unique_together': "(('to_profile', 'from_profile'),)", 'object_name': 'Friendship'},
            'added': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2012, 6, 15, 0, 0)'}),
            'from_profile': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_unused_'", 'to': "orm['users.Profile']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'to_profile': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'friends'", 'to': "orm['users.Profile']"})
        },
        'users.profile': {
            'Meta': {'object_name': 'Profile'},
            'age': ('django.db.models.fields.CharField', [], {'max_length': '3', 'blank': 'True'}),
            'fb_id': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'fb_link': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'fb_username': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['users']