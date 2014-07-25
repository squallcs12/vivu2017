# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):
    def forwards(self, orm):
        # Adding model 'User'
        db.create_table(u'accounts_user', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('last_login', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('username', self.gf('django.db.models.fields.CharField')(unique=True, max_length=30)),
            ('fullname', self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True)),
            ('avatar', self.gf('awesome_avatar.fields.AvatarField')(max_length=100)),
            ('homepage', self.gf('django.db.models.fields.URLField')(default='', max_length=200, blank=True)),
            ('gender', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('birthday', self.gf('django.db.models.fields.DateField')(default=None, null=True, blank=True)),
        ))
        db.send_create_signal(u'accounts', ['User'])


    def backwards(self, orm):
        # Deleting model 'User'
        db.delete_table(u'accounts_user')


    models = {
        u'accounts.user': {
            'Meta': {'object_name': 'User'},
            'avatar': ('awesome_avatar.fields.AvatarField', [], {'max_length': '100'}),
            'birthday': ('django.db.models.fields.DateField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'fullname': (
            'django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'gender': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'homepage': (
            'django.db.models.fields.URLField', [], {'default': "''", 'max_length': '200', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        }
    }

    complete_apps = ['accounts']