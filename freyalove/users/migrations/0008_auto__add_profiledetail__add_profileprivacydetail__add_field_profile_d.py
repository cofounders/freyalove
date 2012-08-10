# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ProfileDetail'
        db.create_table('users_profiledetail', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date_of_birth', self.gf('django.db.models.fields.CharField')(max_length=10, blank=True)),
            ('about', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('points', self.gf('django.db.models.fields.IntegerField')(max_length=3, null=True)),
            ('location', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('origin', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('languages', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('likes', self.gf('django.db.models.fields.CharField')(max_length=300, blank=True)),
            ('likes_activities', self.gf('django.db.models.fields.CharField')(max_length=300, blank=True)),
            ('likes_athletes', self.gf('django.db.models.fields.CharField')(max_length=300, blank=True)),
            ('likes_books', self.gf('django.db.models.fields.CharField')(max_length=300, blank=True)),
            ('likes_games', self.gf('django.db.models.fields.CharField')(max_length=300, blank=True)),
            ('likes_people', self.gf('django.db.models.fields.CharField')(max_length=300, blank=True)),
            ('likes_interests', self.gf('django.db.models.fields.CharField')(max_length=300, blank=True)),
            ('likes_movies', self.gf('django.db.models.fields.CharField')(max_length=300, blank=True)),
            ('likes_sportsteams', self.gf('django.db.models.fields.CharField')(max_length=300, blank=True)),
            ('likes_sports', self.gf('django.db.models.fields.CharField')(max_length=300, blank=True)),
            ('likes_tv', self.gf('django.db.models.fields.CharField')(max_length=300, blank=True)),
            ('likes_quotes', self.gf('django.db.models.fields.CharField')(max_length=300, blank=True)),
        ))
        db.send_create_signal('users', ['ProfileDetail'])

        # Adding model 'ProfilePrivacyDetail'
        db.create_table('users_profileprivacydetail', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('last_name', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('photo', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('date_of_birth', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('about', self.gf('django.db.models.fields.TextField')(default=False)),
            ('points', self.gf('django.db.models.fields.IntegerField')(default=False)),
            ('location', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('origin', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('languages', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('likes', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('likes_activities', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('likes_athletes', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('likes_books', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('likes_games', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('likes_people', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('likes_interests', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('likes_movies', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('likes_sportsteams', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('likes_sports', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('likes_tv', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('likes_quotes', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('users', ['ProfilePrivacyDetail'])

        # Adding field 'Profile.details'
        db.add_column('users_profile', 'details',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['users.ProfileDetail'], null=True),
                      keep_default=False)

        # Adding field 'Profile.permissions'
        db.add_column('users_profile', 'permissions',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['users.ProfilePrivacyDetail'], null=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting model 'ProfileDetail'
        db.delete_table('users_profiledetail')

        # Deleting model 'ProfilePrivacyDetail'
        db.delete_table('users_profileprivacydetail')

        # Deleting field 'Profile.details'
        db.delete_column('users_profile', 'details_id')

        # Deleting field 'Profile.permissions'
        db.delete_column('users_profile', 'permissions_id')


    models = {
        'users.blocked': {
            'Meta': {'object_name': 'Blocked'},
            'belongs_to': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['users.Profile']"}),
            'block_profile_id': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'users.friendship': {
            'Meta': {'unique_together': "(('to_profile', 'from_profile'),)", 'object_name': 'Friendship'},
            'added': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2012, 8, 10, 0, 0)'}),
            'from_profile': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_unused_'", 'to': "orm['users.Profile']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'to_profile': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'friends'", 'to': "orm['users.Profile']"})
        },
        'users.profile': {
            'Meta': {'object_name': 'Profile'},
            'age': ('django.db.models.fields.CharField', [], {'max_length': '3', 'blank': 'True'}),
            'banned': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'details': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['users.ProfileDetail']", 'null': 'True'}),
            'email': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'fb_id': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'fb_link': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'fb_profile_pic': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'fb_username': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'permissions': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['users.ProfilePrivacyDetail']", 'null': 'True'}),
            'profile': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        'users.profiledetail': {
            'Meta': {'object_name': 'ProfileDetail'},
            'about': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'date_of_birth': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'languages': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'likes': ('django.db.models.fields.CharField', [], {'max_length': '300', 'blank': 'True'}),
            'likes_activities': ('django.db.models.fields.CharField', [], {'max_length': '300', 'blank': 'True'}),
            'likes_athletes': ('django.db.models.fields.CharField', [], {'max_length': '300', 'blank': 'True'}),
            'likes_books': ('django.db.models.fields.CharField', [], {'max_length': '300', 'blank': 'True'}),
            'likes_games': ('django.db.models.fields.CharField', [], {'max_length': '300', 'blank': 'True'}),
            'likes_interests': ('django.db.models.fields.CharField', [], {'max_length': '300', 'blank': 'True'}),
            'likes_movies': ('django.db.models.fields.CharField', [], {'max_length': '300', 'blank': 'True'}),
            'likes_people': ('django.db.models.fields.CharField', [], {'max_length': '300', 'blank': 'True'}),
            'likes_quotes': ('django.db.models.fields.CharField', [], {'max_length': '300', 'blank': 'True'}),
            'likes_sports': ('django.db.models.fields.CharField', [], {'max_length': '300', 'blank': 'True'}),
            'likes_sportsteams': ('django.db.models.fields.CharField', [], {'max_length': '300', 'blank': 'True'}),
            'likes_tv': ('django.db.models.fields.CharField', [], {'max_length': '300', 'blank': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'origin': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'points': ('django.db.models.fields.IntegerField', [], {'max_length': '3', 'null': 'True'})
        },
        'users.profileprivacydetail': {
            'Meta': {'object_name': 'ProfilePrivacyDetail'},
            'about': ('django.db.models.fields.TextField', [], {'default': 'False'}),
            'date_of_birth': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'languages': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_name': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'likes': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'likes_activities': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'likes_athletes': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'likes_books': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'likes_games': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'likes_interests': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'likes_movies': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'likes_people': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'likes_quotes': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'likes_sports': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'likes_sportsteams': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'likes_tv': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'location': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'origin': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'photo': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'points': ('django.db.models.fields.IntegerField', [], {'default': 'False'})
        },
        'users.wink': {
            'Meta': {'object_name': 'Wink'},
            'accepted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'from_profile': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'wink_from'", 'to': "orm['users.Profile']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'received': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'to_profile': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'wink_to'", 'to': "orm['users.Profile']"})
        }
    }

    complete_apps = ['users']