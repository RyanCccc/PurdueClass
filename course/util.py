# Fix third-party lib path
import fix_path

from bs4 import BeautifulSoup as BS
import urllib
import urllib2
import re

from PCS import settings
from class_time import Time_Interval, Class_Time

class ParserException(Exception):
    pass

def get_resp(crn, term):
    url_head = 'https://selfservice.mypurdue.purdue.edu/prod/bzwsrch.p_schedule_detail'
    param = {'crn' : crn, 'term' : term}
    url = url_head + '?' + urllib.urlencode(param) 
    try:
        resp = urllib2.urlopen(url)
    except:
        raise ParserException('Cannot open url %s' % url)
    if resp.code == 200:
        return resp
    raise ParserException('Response incorrect, code: %s' % resp.code)

def get_parser(resp):
    html = resp.read()
    return BS(html)

def get_table(parser):
    try:
        table = parser.find_all('table')[3]
    except:
        raise ParserException('Unable to find the table')
    return table

def get_seats_row(parser):
    table = get_table(parser)
    try:
        seats_row = table.find_all('tr')[1]
    except:
        raise ParserException('Cannot find the seats row')
    return seats_row

def get_waitlist_row(parser):
    table = get_table(parser)
    try:
        w_seats_row = table.find_all('tr')[1]
    except:
        raise ParserException('Cannot find the waitlist seats row')
    return w_seats_row

def get_max_seats(parser):
    seats_row = get_seats_row(parser)
    try:
        max_cell = seats_row.find_all('td')[0]
    except:
        raise ParserException('Cannot find max_cell')
    return int(max_cell.text)

def get_current_seats(parser):
    seats_row = get_seats_row(parser)
    try:
        curr_cell = seats_row.find_all('td')[1]
    except:
        raise ParserException('Cannot find max_cell')
    return int(curr_cell.text)

def get_seats(crn, term):
    resp = get_resp(crn, term)
    parser = get_parser(resp)
    max_num = get_max_seats(parser)
    curr_num = get_current_seats(parser)
    return max_num, curr_num

def get_all(crn, term):
    resp = get_resp(crn, term)
    parser = get_parser(resp)
    try:
        results = parser.find_all('table')[2].th.text.split(' - ')
    except:
        raise ParserException('Cannot find this CRN')
    sec_name = results[0]
    if not results[1] == str(crn):
        raise ParserException('Result not correct')
    sec_code = results[2]
    sec_num = results[3]
    max_num = get_max_seats(parser)
    curr_num = get_current_seats(parser) 
    return max_num, curr_num, sec_name, sec_code, sec_num

def get_all_secs_by_class(sub, cnbr, term='CURRENT', timeout=None):
    url = "https://selfservice.mypurdue.purdue.edu/prod/bzwsrch.p_search_schedule?term=%s&cnbr=%s&subject=%s" % (term, cnbr, sub)
    classes = []
    try:
        if timeout:
            resp = urllib2.urlopen(url, timeout=timeout)
        else:
            resp = urllib2.urlopen(url)
        data = resp.read()
        ps = BS(data)

        # Get class name, crn, code, number
        all_table = ps.find_all('th')
        total = len(all_table)
        for i in xrange(0, total, 8):
            current_table = all_table[i]
            content = current_table.a.text
            content = content.split(' - ')
            cl = dict(
                name = content[0],
                crn = content[1],
                code = content[2],
                number = content[3]
            )
            classes.append(cl)

        # Get class time, type
        all_table = ps.select('.datadisplaytable')
        count = 0 
        for i in range(1,len(all_table)-1):
            table = all_table[i]
            info_table = table.select('tr')[1]
            time_raw = info_table.select('td')[1].text
            class_time = Time_Interval(time_raw)
            type_ = info_table.select('td')[5].text
            classes[count]['class_time'] = class_time
            classes[count]['class_type'] = type_
            count += 1
    except Exception as e:
        raise ParserException(e.message)
    return classes

def convert_classname(in_str):
    in_str = in_str.replace(' ','')
    r = re.compile("([a-zA-Z]+)([0-9]+)")
    m = r.match(in_str)
    try:
        sub = m.group(1).upper()
        cnbr = m.group(2)
    except AttributeError as e:
        raise ParserException('Incorrect class name format')
    if len(cnbr) < 5:
        cnbr += '00'
    return sub, cnbr

def convert_term_to_code(term_str):
    term_str = term_str.replace(' ','')
    if term_str.lower().strip() == 'current':
        return settings.CURRENT_TERM
    dic = {
        'SU' : 30,
        'SP' : 20,
        'FA' : 10,
    }
    semester = 'FA'
    year = 2013
    r = re.compile("([a-zA-Z]+)([0-9]+)")
    m = r.match(term_str)
    if m:
        semester = m.group(1)
        year = m.group(2)
    else:
        r = re.compile("([0-9]+)([a-zA-Z]+)")
        m = r.match(term_str)
        if not m:
            return settings.CURRENT_TERM
        else:
            semester = m.group(2)
            year = m.group(1)

    for k, i in dic.iteritems():
       if k.lower() in semester.lower():
           semester = str(i)
           break

    year = int(year)

    if len(str(year)) == 2:
        year += 2000

    if semester == '10':
        year += 1

    term = str(year) + semester
    return term


def convert_code_to_term(code):
    year = int(code[:4])
    sem = int(code[4:])
    dic = {
        'Summer' : 30,
        'Spring' : 20,
        'Fall' : 10,
    }
    for k, i in dic.iteritems():
        if i == sem:
            if i == 10:
                year -= 1
            sem = k
            break
    return sem + ' ' + str(year) 
