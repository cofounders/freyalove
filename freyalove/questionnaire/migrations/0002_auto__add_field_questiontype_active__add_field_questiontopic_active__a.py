# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'QuestionType.active'
        db.add_column('questionnaire_questiontype', 'active',
                      self.gf('django.db.models.fields.BooleanField')(default=True),
                      keep_default=False)

        # Adding field 'QuestionTopic.active'
        db.add_column('questionnaire_questiontopic', 'active',
                      self.gf('django.db.models.fields.BooleanField')(default=True),
                      keep_default=False)

        # Adding field 'Question.publish'
        db.add_column('questionnaire_question', 'publish',
                      self.gf('django.db.models.fields.BooleanField')(default=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'QuestionType.active'
        db.delete_column('questionnaire_questiontype', 'active')

        # Deleting field 'QuestionTopic.active'
        db.delete_column('questionnaire_questiontopic', 'active')

        # Deleting field 'Question.publish'
        db.delete_column('questionnaire_question', 'publish')


    models = {
        'questionnaire.answer': {
            'Meta': {'object_name': 'Answer', '_ormbases': ['questionnaire.Question']},
            'answer': ('django.db.models.fields.CharField', [], {'max_length': '300', 'blank': 'True'}),
            'comment': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'matches': ('django.db.models.fields.CharField', [], {'max_length': '300', 'blank': 'True'}),
            'profile': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['users.Profile']"}),
            'public': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'for_question'", 'to': "orm['questionnaire.Question']"}),
            'question_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['questionnaire.Question']", 'unique': 'True', 'primary_key': 'True'})
        },
        'questionnaire.question': {
            'Meta': {'object_name': 'Question'},
            'choice_1': ('django.db.models.fields.CharField', [], {'max_length': '300', 'blank': 'True'}),
            'choice_2': ('django.db.models.fields.CharField', [], {'max_length': '300', 'blank': 'True'}),
            'choice_3': ('django.db.models.fields.CharField', [], {'max_length': '300', 'blank': 'True'}),
            'choice_4': ('django.db.models.fields.CharField', [], {'max_length': '300', 'blank': 'True'}),
            'help_text': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'publish': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'question_topic': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['questionnaire.QuestionTopic']"}),
            'question_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['questionnaire.QuestionType']"})
        },
        'questionnaire.questiontopic': {
            'Meta': {'object_name': 'QuestionTopic'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'questionnaire.questiontype': {
            'Meta': {'object_name': 'QuestionType'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
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

    complete_apps = ['questionnaire']