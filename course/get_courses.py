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

def parse_subjects(term=default_term, should_store=False):
    data = get_subjects_raw(term)
    data = handle_xml(data,methods[1])
    subjects = {}
    root = ET.fromstring(data)
    subs = root.findall('Subject')
    for sub in subs:
        subjects[sub.find('Acronym').text] = sub.find('Name').text
    return subjects


def parse_courses(subject, term=default_term, keywords=''):
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
        if not description:
            description = ''

        schedule_nodes = course_node.findall('Schedules/Schedule')
        # Save course if it has schedule
        if schedule_nodes:
            course_db = Course(subject=subject_code,
                               subject_name=subject_name,
                               CNBR=CNBR,
                               title=title,
                               description=description,
                               credit=credit,)
            course_db.term = Term.objects.get(description=term)
            course_db.save()
        #TODO deal with schedule_nodes


def parse_all_courses(term=default_term):
    subjects = parse_subjects(term)
    for subject in subjects:
        print 'Doing', subject
        parse_courses(subject,term)


def create_term(term_str):
    code = convert_term_to_code(term_str)
    term = Term(code=code, description=term_str)
    term.save()
