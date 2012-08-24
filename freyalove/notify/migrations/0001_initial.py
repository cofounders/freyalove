# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Note'
        db.create_table('notify_note', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('belongs_to', self.gf('django.db.models.fields.related.ForeignKey')(related_name='belongs', to=orm['users.Profile'])),
            ('actor', self.gf('django.db.models.fields.related.ForeignKey')(related_name='actor', null=True, to=orm['users.Profile'])),
            ('verb', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('unread', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'], null=True)),
            ('object_id', self.gf('django.db.models.fields.PositiveIntegerField')(null=True)),
        ))
        db.send_create_signal('notify', ['Note'])


    def backwards(self, orm):
        # Deleting model 'Note'
        db.delete_table('notify_note')


    models = {
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'notify.note': {
            'Meta': {'object_name': 'Note'},
            'actor': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'actor'", 'null': 'True', 'to': "orm['users.Profile']"}),
            'belongs_to': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'belongs'", 'to': "orm['users.Profile']"}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']", 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            'unread': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'verb': ('django.db.models.fields.CharField', [], {'max_length': '300'})
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
        }
    }

    complete_apps = ['notify']