# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Course.title'
        db.add_column(u'course_course', 'title',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=100),
                      keep_default=False)

        # Adding field 'Course.description'
        db.add_column(u'course_course', 'description',
                      self.gf('django.db.models.fields.TextField')(default=''),
                      keep_default=False)


        # Changing field 'Course.credit'
        db.alter_column(u'course_course', 'credit', self.gf('django.db.models.fields.IntegerField')(null=True))

    def backwards(self, orm):
        # Deleting field 'Course.title'
        db.delete_column(u'course_course', 'title')

        # Deleting field 'Course.description'
        db.delete_column(u'course_course', 'description')


        # Changing field 'Course.credit'
        db.alter_column(u'course_course', 'credit', self.gf('django.db.models.fields.IntegerField')(default=0))

    models = {
        u'course.course': {
            'CNBR': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'Meta': {'object_name': 'Course'},
            'credit': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'subject_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'term': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['course.Term']", 'symmetrical': 'False'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'course.meeting': {
            'DayOfWeek': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'Meta': {'object_name': 'Meeting'},
            'building': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'end_t': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instructor': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'room': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'section': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['course.Section']"}),
            'start_t': ('django.db.models.fields.IntegerField', [], {})
        },
        u'course.schedule': {
            'Meta': {'object_name': 'Schedule'},
            'course': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['course.Course']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'type_id': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'type_name': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        u'course.section': {
            'Meta': {'object_name': 'Section'},
            'crn': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link_sections': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['course.Section']", 'symmetrical': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'number': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'schedule': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['course.Schedule']"})
        },
        u'course.term': {
            'Meta': {'object_name': 'Term'},
            'code': ('django.db.models.fields.IntegerField', [], {}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['course']