import httplib
import xml.etree.ElementTree as ET
from course.models import Course, Term, Schedule, Section, Meeting
from xml.sax.saxutils import unescape

base_url = 'www.emilstefanov.net'
service_url = '/Projects/PurdueCourses/CoursesInfoService.svc'

methods = ['SearchCourses', 'GetSubjects']

def get_subjects_raw(term='Spring2014'):
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

def search_courses_raw(subject, term='Spring2014', keywords=''):
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

def parse_subjects(data):
    subjects = {}
    root = ET.fromstring(data)
    subs = root.findall('Subject')
    for sub in subs:
        subjects[sub.find('Acronym').text] = sub.find('Name').text
        Course.create

    return subjects
