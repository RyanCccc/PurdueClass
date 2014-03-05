from django.db import models

# Create your models here.
class Course(models.Model):
    subject = models.CharField(max_length=10)
    subject_name = models.CharField(max_length=50)
    CNBR = models.CharField(max_length=10)
    credit = models.IntegerField()
    term = models.ManyToManyField(
        Term,
    )


class Term(models.Model):
    code = models.IntegerField()
    description = models.CharField(max_length=20)


class Schedule(models.Model):
    course = models.ForeignKey(Course)

    type_id = models.CharField(max_length=10)
    type_name = models.CharField(max_length=20)


class Section(models.Model):
    schedule = models.ForeignKey(schedule)

    name = models.CharField(max_length=100)
    number = models.CharField(max_length=100)
    crn = models.CharField(max_length=10)

    link_sections = models.ManyToManyField(
        Section,
    )


class Meeting(models.Model)
    section = models.ForeignKey(Section)

    DayOfWeek = models.CharField(max_length=10)
    instructor = models.CharField(max_length=50)
    building = models.CharField(max_length=50)
    room = models.CharField(max_length=10)
    start_t = models.IntegerField()
    end_t = models.IntegerField()
