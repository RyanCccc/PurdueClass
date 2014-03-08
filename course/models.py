from django.db import models


class CourseManager(models.Manager):
    def create_course(
        self,
        subject,
        subject_name,
        CNBR,
        title,
        description,
        credit,
        term,
    ):
        if not description:
            description = ''
        code = subject + CNBR
        course = self.create(
            subject=subject,
            subject_name=subject_name,
            CNBR=CNBR,
            title=title,
            description=description,
            credit=credit,
            code=code,
            term=Term.objects.get(description=term),
        )
        return course


# Create your models here.
class Term(models.Model):
    code = models.IntegerField()
    description = models.CharField(max_length=20)

    def dump_data(self):
        term = {
            'code': self.code,
            'description': self.description,
        }
        return term


class Course(models.Model):
    subject = models.CharField(max_length=10)
    subject_name = models.CharField(max_length=50)
    CNBR = models.CharField(max_length=10)
    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    credit = models.CharField(max_length=15)
    code = models.CharField(max_length=20, unique=True)
    term = models.ForeignKey('Term')
    objects = CourseManager()

    def dump_data(self):
        course = {
            'subject': self.subject,
            'subject_name': self.subject_name,
            'CNBR': self.CNBR,
            'title': self.title,
            'description': self.description,
            'credit': self.credit,
            'code': self.code,
        }
        schedule_data = []
        for schedule in self.schedule_set.all():
            schedule_data.append(schedule.dump_data())
        course['schedules'] = schedule_data
        return course


class Schedule(models.Model):
    course = models.ForeignKey('Course')

    type_id = models.CharField(max_length=20)
    type_name = models.CharField(max_length=50)

    def dump_data(self):
        schedule = {
            'type_id': self.type_id,
            'type_name': self.type_name,
        }
        section_data = []
        for section in self.section_set.all():
            section_data.append(section.dump_data())
        schedule['sections'] = section_data
        return schedule


class Section(models.Model):
    schedule = models.ForeignKey('Schedule')

    name = models.CharField(max_length=500)
    number = models.CharField(max_length=50)
    crn = models.CharField(max_length=10)
    link_id = models.CharField(max_length=20, null=True)
    required_link_id = models.CharField(max_length=20, null=True)

    def dump_data(self, need_link=True):
        section = {
            'name': self.name,
            'number': self.number,
            'crn': self.crn,
        }
        if need_link:
            linked_secs = self.get_linked_sections()
            linked_secs_all_data = []
            if linked_secs:
                for secs in linked_secs:
                    linked_secs_data = []
                    for sec in secs:
                        linked_secs_data.append(sec.dump_data(False))
                    linked_secs_all_data.append(linked_secs_data)
                section['linked_sections'] = linked_secs_all_data
        meeting_data = []
        for meeting in self.meeting_set.all():
            meeting_data.append(meeting.dump_data())
        section['meetings'] = meeting_data    
        return section


    def get_linked_sections(self):
        if self.required_link_id:
            linked_secs_all = []
            course = self.schedule.course
            schedules = course.schedule_set.all()
            link_id = self.link_id
            required_link_id_list = set([self.required_link_id,])
            while required_link_id_list:
                required_link_id = required_link_id_list.pop()
                linked_secs = []
                for schedule in schedules:
                    for sec in schedule.section_set.all():
                        if sec.link_id == required_link_id:
                            linked_secs.append(sec)
                            if not sec.required_link_id == link_id:
                                required_link_id_list.add(sec.required_link_id)
                linked_secs_all.append(linked_secs)
            return linked_secs_all
        else:
            return None

class Meeting(models.Model):
    section = models.ForeignKey('Section')

    DayOfWeek = models.CharField(max_length=50)
    instructor = models.CharField(max_length=500)
    building = models.CharField(max_length=500)
    room = models.CharField(max_length=50)
    start_t = models.IntegerField()
    end_t = models.IntegerField()
    
    def dump_data(self):
        meeting = {
            'DayOfWeek': self.DayOfWeek,
            'instructor': self.instructor,
            'building': self.building,
            'room': self.room,
            'start_t': self.start_t,
            'end_t': self.end_t,
        }
        return meeting

    @staticmethod
    def convert_raw_time_to_int(raw_time):
        times = raw_time.split('T')[1].split(':')
        return int(times[0])*60+int(times[1])

    @staticmethod
    def convert_int_to_time(time_int):
        return int(time_int)/60, int(time_int)%60
