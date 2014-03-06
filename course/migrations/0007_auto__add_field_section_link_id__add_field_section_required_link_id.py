# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Section.link_id'
        db.add_column(u'course_section', 'link_id',
                      self.gf('django.db.models.fields.CharField')(max_length=20, null=True),
                      keep_default=False)

        # Adding field 'Section.required_link_id'
        db.add_column(u'course_section', 'required_link_id',
                      self.gf('django.db.models.fields.CharField')(max_length=20, null=True),
                      keep_default=False)

        # Removing M2M table for field link_sections on 'Section'
        db.delete_table(db.shorten_name(u'course_section_link_sections'))


    def backwards(self, orm):
        # Deleting field 'Section.link_id'
        db.delete_column(u'course_section', 'link_id')

        # Deleting field 'Section.required_link_id'
        db.delete_column(u'course_section', 'required_link_id')

        # Adding M2M table for field link_sections on 'Section'
        m2m_table_name = db.shorten_name(u'course_section_link_sections')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_section', models.ForeignKey(orm[u'course.section'], null=False)),
            ('to_section', models.ForeignKey(orm[u'course.section'], null=False))
        ))
        db.create_unique(m2m_table_name, ['from_section_id', 'to_section_id'])


    models = {
        u'course.course': {
            'CNBR': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'Meta': {'object_name': 'Course'},
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20'}),
            'credit': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
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
            'link_id': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'number': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'required_link_id': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True'}),
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