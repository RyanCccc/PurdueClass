# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Course.term'
        db.add_column(u'course_course', 'term',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['course.Term'], null=True),
                      keep_default=False)

        # Removing M2M table for field term on 'Course'
        db.delete_table(db.shorten_name(u'course_course_term'))


    def backwards(self, orm):
        # Deleting field 'Course.term'
        db.delete_column(u'course_course', 'term_id')

        # Adding M2M table for field term on 'Course'
        m2m_table_name = db.shorten_name(u'course_course_term')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('course', models.ForeignKey(orm[u'course.course'], null=False)),
            ('term', models.ForeignKey(orm[u'course.term'], null=False))
        ))
        db.create_unique(m2m_table_name, ['course_id', 'term_id'])


    models = {
        u'course.course': {
            'CNBR': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'Meta': {'object_name': 'Course'},
            'credit': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'subject_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'term': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['course.Term']", 'null': 'True'}),
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