# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Term'
        db.create_table(u'course_term', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('code', self.gf('django.db.models.fields.IntegerField')()),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=20)),
        ))
        db.send_create_signal(u'course', ['Term'])

        # Adding model 'Course'
        db.create_table(u'course_course', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('subject', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('subject_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('CNBR', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('credit', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'course', ['Course'])

        # Adding M2M table for field term on 'Course'
        m2m_table_name = db.shorten_name(u'course_course_term')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('course', models.ForeignKey(orm[u'course.course'], null=False)),
            ('term', models.ForeignKey(orm[u'course.term'], null=False))
        ))
        db.create_unique(m2m_table_name, ['course_id', 'term_id'])

        # Adding model 'Schedule'
        db.create_table(u'course_schedule', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('course', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['course.Course'])),
            ('type_id', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('type_name', self.gf('django.db.models.fields.CharField')(max_length=20)),
        ))
        db.send_create_signal(u'course', ['Schedule'])

        # Adding model 'Section'
        db.create_table(u'course_section', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('schedule', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['course.Schedule'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('number', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('crn', self.gf('django.db.models.fields.CharField')(max_length=10)),
        ))
        db.send_create_signal(u'course', ['Section'])

        # Adding M2M table for field link_sections on 'Section'
        m2m_table_name = db.shorten_name(u'course_section_link_sections')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_section', models.ForeignKey(orm[u'course.section'], null=False)),
            ('to_section', models.ForeignKey(orm[u'course.section'], null=False))
        ))
        db.create_unique(m2m_table_name, ['from_section_id', 'to_section_id'])

        # Adding model 'Meeting'
        db.create_table(u'course_meeting', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('section', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['course.Section'])),
            ('DayOfWeek', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('instructor', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('building', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('room', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('start_t', self.gf('django.db.models.fields.IntegerField')()),
            ('end_t', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'course', ['Meeting'])


    def backwards(self, orm):
        # Deleting model 'Term'
        db.delete_table(u'course_term')

        # Deleting model 'Course'
        db.delete_table(u'course_course')

        # Removing M2M table for field term on 'Course'
        db.delete_table(db.shorten_name(u'course_course_term'))

        # Deleting model 'Schedule'
        db.delete_table(u'course_schedule')

        # Deleting model 'Section'
        db.delete_table(u'course_section')

        # Removing M2M table for field link_sections on 'Section'
        db.delete_table(db.shorten_name(u'course_section_link_sections'))

        # Deleting model 'Meeting'
        db.delete_table(u'course_meeting')


    models = {
        u'course.course': {
            'CNBR': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'Meta': {'object_name': 'Course'},
            'credit': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'subject_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'term': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['course.Term']", 'symmetrical': 'False'})
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