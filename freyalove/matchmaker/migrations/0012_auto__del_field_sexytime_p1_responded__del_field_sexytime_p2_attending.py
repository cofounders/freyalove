# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'SexyTime.p1_responded'
        db.delete_column('matchmaker_sexytime', 'p1_responded')

        # Deleting field 'SexyTime.p2_attending'
        db.delete_column('matchmaker_sexytime', 'p2_attending')

        # Deleting field 'SexyTime.p1_attending'
        db.delete_column('matchmaker_sexytime', 'p1_attending')

        # Deleting field 'SexyTime.p2_responded'
        db.delete_column('matchmaker_sexytime', 'p2_responded')

        # Adding field 'SexyTime.p1_response'
        db.add_column('matchmaker_sexytime', 'p1_response',
                      self.gf('django.db.models.fields.CharField')(default='notset', max_length=10),
                      keep_default=False)

        # Adding field 'SexyTime.p2_response'
        db.add_column('matchmaker_sexytime', 'p2_response',
                      self.gf('django.db.models.fields.CharField')(default='notset', max_length=10),
                      keep_default=False)

        # Adding field 'SexyTime.success'
        db.add_column('matchmaker_sexytime', 'success',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'SexyTime.rejected'
        db.add_column('matchmaker_sexytime', 'rejected',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'SexyTime.p1_responded'
        db.add_column('matchmaker_sexytime', 'p1_responded',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'SexyTime.p2_attending'
        db.add_column('matchmaker_sexytime', 'p2_attending',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'SexyTime.p1_attending'
        db.add_column('matchmaker_sexytime', 'p1_attending',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'SexyTime.p2_responded'
        db.add_column('matchmaker_sexytime', 'p2_responded',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Deleting field 'SexyTime.p1_response'
        db.delete_column('matchmaker_sexytime', 'p1_response')

        # Deleting field 'SexyTime.p2_response'
        db.delete_column('matchmaker_sexytime', 'p2_response')

        # Deleting field 'SexyTime.success'
        db.delete_column('matchmaker_sexytime', 'success')

        # Deleting field 'SexyTime.rejected'
        db.delete_column('matchmaker_sexytime', 'rejected')


    models = {
        'matchmaker.match': {
            'Meta': {'object_name': 'Match'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'initial_signal': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'matchmaker': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'matchmaker'", 'to': "orm['users.Profile']"}),
            'p1': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'prospect1'", 'to': "orm['users.Profile']"}),
            'p1_response': ('django.db.models.fields.CharField', [], {'default': "'notset'", 'max_length': '10'}),
            'p2': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'prospect2'", 'to': "orm['users.Profile']"}),
            'p2_response': ('django.db.models.fields.CharField', [], {'default': "'notset'", 'max_length': '10'}),
            'rejected': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'success': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'})
        },
        'matchmaker.matchproposal': {
            'Meta': {'object_name': 'MatchProposal'},
            'from_profile': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'from'", 'to': "orm['users.Profile']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'match': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['matchmaker.Match']", 'null': 'True'}),
            'quality': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'to_profile': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'to'", 'to': "orm['users.Profile']"})
        },
        'matchmaker.sexytime': {
            'Meta': {'object_name': 'SexyTime'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'initial_signal': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'match': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['matchmaker.Match']", 'null': 'True'}),
            'matchmaker': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'maker'", 'to': "orm['users.Profile']"}),
            'notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'p1': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'date1'", 'to': "orm['users.Profile']"}),
            'p1_response': ('django.db.models.fields.CharField', [], {'default': "'notset'", 'max_length': '10'}),
            'p2': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'date2'", 'to': "orm['users.Profile']"}),
            'p2_response': ('django.db.models.fields.CharField', [], {'default': "'notset'", 'max_length': '10'}),
            'rejected': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'success': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'when': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'where': ('django.db.models.fields.CharField', [], {'max_length': '300', 'blank': 'True'})
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
            'is_matchmaker': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'matchmaker_score': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
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

    complete_apps = ['matchmaker']