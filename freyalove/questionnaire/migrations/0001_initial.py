# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'QuestionTopic'
        db.create_table('questionnaire_questiontopic', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('questionnaire', ['QuestionTopic'])

        # Adding model 'QuestionType'
        db.create_table('questionnaire_questiontype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('questionnaire', ['QuestionType'])

        # Adding model 'Question'
        db.create_table('questionnaire_question', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('question_topic', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['questionnaire.QuestionTopic'])),
            ('question_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['questionnaire.QuestionType'])),
            ('choice_1', self.gf('django.db.models.fields.CharField')(max_length=300, blank=True)),
            ('choice_2', self.gf('django.db.models.fields.CharField')(max_length=300, blank=True)),
            ('choice_3', self.gf('django.db.models.fields.CharField')(max_length=300, blank=True)),
            ('choice_4', self.gf('django.db.models.fields.CharField')(max_length=300, blank=True)),
            ('help_text', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('questionnaire', ['Question'])

        # Adding model 'Answer'
        db.create_table('questionnaire_answer', (
            ('question_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['questionnaire.Question'], unique=True, primary_key=True)),
            ('profile', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['users.Profile'])),
            ('question', self.gf('django.db.models.fields.related.ForeignKey')(related_name='for_question', to=orm['questionnaire.Question'])),
            ('answer', self.gf('django.db.models.fields.CharField')(max_length=300, blank=True)),
            ('matches', self.gf('django.db.models.fields.CharField')(max_length=300, blank=True)),
            ('comment', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('public', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('questionnaire', ['Answer'])


    def backwards(self, orm):
        # Deleting model 'QuestionTopic'
        db.delete_table('questionnaire_questiontopic')

        # Deleting model 'QuestionType'
        db.delete_table('questionnaire_questiontype')

        # Deleting model 'Question'
        db.delete_table('questionnaire_question')

        # Deleting model 'Answer'
        db.delete_table('questionnaire_answer')


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
            'question_topic': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['questionnaire.QuestionTopic']"}),
            'question_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['questionnaire.QuestionType']"})
        },
        'questionnaire.questiontopic': {
            'Meta': {'object_name': 'QuestionTopic'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'questionnaire.questiontype': {
            'Meta': {'object_name': 'QuestionType'},
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