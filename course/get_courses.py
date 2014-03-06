import httplib
import xml.etree.ElementTree as ET
from xml.sax.saxutils import unescape

from course.models import Course, Term, Schedule, Section, Meeting
from course.util import convert_term_to_code

base_url = 'www.emilstefanov.net'
service_url = '/Projects/PurdueCourses/CoursesInfoService.svc'
default_term = 'Spring2014'

methods = ['SearchCourses', 'GetSubjects']

def get_subjects_raw(term=default_term):
    conn = httplib.HTTPConnection(base_url)
    headers = {
        'Content-type': 'text/xml',
        'soapaction': 'urn:CoursesInfoService/GetSubjects',
    }
    content = '<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/"><s:Body><GetSubjects><term>%s</term></GetSubjects></s:Body></s:Envelope>'%term
    conn.request('POST', service_url, content, headers)
    response = conn.getresponse()
    data =  response.read()
    conn.close()
    return data

def search_courses_raw(subject, term=default_term, keywords=''):
    conn = httplib.HTTPConnection(base_url)
    headers = {
        'Content-type': 'text/xml',
        'soapaction': 'urn:CoursesInfoService/SearchCourses',
    }
    content = '<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/"><s:Body><SearchCourses><term>{0}</term><subject>{1}</subject><keywords>{2}</keywords></SearchCourses></s:Body></s:Envelope>'.format(term,subject,keywords)
    conn.request('POST', service_url, content, headers)
    response = conn.getresponse()
    data =  response.read()
    conn.close()
    return data


def handle_xml(data, method, filename=None):
    data = data.replace('&#xD;','')
    data = unescape(data)
    #data = data.replace('&','&amp;')
    data = data[data.find('<?xml'):]
    data = data[:data.find('</%s'%method)]
    if filename:
        f = open(filename,'w')
        f.write(data)
        f.flush()
        f.close()
    return data

def parse_subjects(term=default_term):
    data = get_subjects_raw(term)
    data = handle_xml(data,methods[1])
    subjects = {}
    root = ET.fromstring(data)
    subs = root.findall('Subject')
    for sub in subs:
        subjects[sub.find('Acronym').text] = sub.find('Name').text
    return subjects


def parse_courses(subject, term=default_term, keywords=''):
    course_db, schedule_db, section_db, meeting_db = None, None, None, None
    data = search_courses_raw(subject, term, keywords)
    data = handle_xml(data,methods[0])
    course_nodes = []
    root = ET.fromstring(data)
    course_nodes = root.findall('Course')
    for course_node in course_nodes:
        # Basic course info
        CNBR = course_node.find('Number').text
        title = course_node.find('Title').text
        credit = course_node.find('Credits').text
        description = course_node.find('Description').text
        subject_node = course_node.find('Subject')
        subject_code = subject_node.find('Acronym').text
        subject_name = subject_node.find('Name').text
        subject_unique_code = subject_code+CNBR
        if Course.objects.filter(code=subject_unique_code).exists():
            print subject_unique_code, 'exists already!'
            continue

        schedule_nodes = course_node.findall('Schedules/Schedule')
        
        # Save course if it has schedule
        if schedule_nodes:
            # Course is valid
            print 'Saving', subject_unique_code

            course_db = Course.objects.create_course(
                subject=subject_code,
                subject_name=subject_name,
                CNBR=CNBR,
                title=title,
                description=description,
                credit=credit,
                term=term,
            )

            # Deal with schedules
            for schedule_node in schedule_nodes:
                type_id = schedule_node.find('TypeId').text
                type_name = schedule_node.find('TypeName').text
                schedule_db = Schedule.objects.create(
                    type_id=type_id,
                    type_name=type_name,
                    course=course_db,
                )

                section_nodes = schedule_node.findall('Sections/Section')

                # Deal with sections
                for section_node in section_nodes:
                    name = section_node.find('Name').text
                    number = section_node.find('Number').text
                    crn = section_node.find('RegistrationNumber').text
                    link_id = None
                    required_link_id = None
                    if section_node.find('LinkId') is not None:
                        link_id = section_node.find('LinkId').text
                    if section_node.find('RequiredLinkId') is not None:
                        required_link_id = section_node.find('RequiredLinkId').text

                    section_db = Section.objects.create(
                        name=name,
                        number=number,
                        crn=crn,
                        link_id=link_id if link_id else None,
                        required_link_id=required_link_id if required_link_id else None,
                        schedule=schedule_db,
                    )

                    meeting_nodes = section_node.findall('Meetings/Meeting')

                    # Deal with meetings
                    for meeting_node in meeting_nodes:
                        DayOfWeekIsKnown = meeting_node.find('DayOfWeekIsKnown').text
                        DayOfWeek = 'Unknown'
                        if DayOfWeekIsKnown == 'true':
                            DayOfWeek = meeting_node.find('DayOfWeek').text

                        instructor = 'Unknown'
                        if meeting_node.find('Instructors') is not None:
                            instructor = meeting_node.find('Instructors').text

                        building = 'Unknown'
                        if meeting_node.find('BuildingName') is not None:
                            building = meeting_node.find('BuildingName').text

                        room = 'Unknown'
                        if meeting_node.find('Room') is not None:
                            room = meeting_node.find('Room').text

                        TimeRangeIsKnown = meeting_node.find('TimeRangeIsKnown').text
                        start_t, end_t = 0, 0
                        if TimeRangeIsKnown == 'true':
                            start_t_raw = meeting_node.find('StartTime').text
                            end_t_raw = meeting_node.find('EndTime').text
                            start_t = Meeting.convert_raw_time_to_int(start_t_raw)
                            end_t = Meeting.convert_raw_time_to_int(end_t_raw)

                        meeting_db = Meeting.objects.create(
                            DayOfWeek=DayOfWeek,
                            instructor=instructor,
                            building=building,
                            room=room,
                            start_t=start_t,
                            end_t=end_t,
                            section=section_db,
                        )


def parse_all_courses(term=default_term):
    subjects = parse_subjects(term)
    import operator
    sorted_subjects = sorted(subjects.iteritems(), key=operator.itemgetter(0))
    for subject in sorted_subjects:
        print 'Doing', subject[0]
        parse_courses(subject[0],term)


def create_term(term_str):
    code = convert_term_to_code(term_str)
    term = Term(code=code, description=term_str)
    term.save()

def clear_db():
    Course.objects.all().delete()
    Schedule.objects.all().delete()
    Section.objects.all().delete()
    Meeting.objects.all().delete()