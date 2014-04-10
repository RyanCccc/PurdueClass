import httplib
import urllib
import urllib2
import re
from lxml import etree
from util import convert_code_to_term, convert_term_to_code

select_term_url = 'https://selfservice.mypurdue.purdue.edu/prod/bwckschd.p_disp_dyn_sched'
subject_url = 'https://selfservice.mypurdue.purdue.edu/prod/bwckgens.p_proc_term_date'
section_url = 'https://selfservice.mypurdue.purdue.edu/prod/bwckschd.p_get_crse_unsec'
default_term = 'Fall2014'

def get_conn(url, ref_url, param, encode=False):
	req = urllib2.Request(url)
	req.add_header('Referer', ref_url)
	data = param
	if not encode:
		data = urllib.urlencode(param)
	resp = urllib2.urlopen(req, data)
	return resp

def get_subjects(term=default_term):
	subjects = []
	p_calling_proc = 'bwckschd.p_disp_dyn_sched'
	p_term = convert_term_to_code(term)
	param = {'p_calling_proc' : p_calling_proc, 'p_term' : p_term}
	resp = get_conn(subject_url, select_term_url, param);
	if resp.code != 200:
		return None
	else:
		content = resp.read()
		tree = etree.HTML(content)
		subject_set = tree.xpath('.//select[@name="sel_subj"]')[0].findall('option')
		for option in subject_set:
			sub_code = option.attrib['value']
			sub_name = option.text[len(sub_code):].strip('\n\r- ')
			subjects.append([sub_code,sub_name])
		return subjects

def get_sections(subject, term=default_term):
	term_code = convert_term_to_code(term)
	param = 'term_in={0}&sel_subj=dummy&sel_day=dummy&sel_schd=dummy&sel_insm=dummy&sel_camp=dummy&sel_levl=dummy&sel_sess=dummy&sel_instr=dummy&sel_ptrm=dummy&sel_attr=dummy&sel_subj={1}&sel_crse=&sel_title=&sel_schd=%25&sel_from_cred=&sel_to_cred=&sel_camp=%25&sel_ptrm=%25&sel_instr=%25&sel_sess=%25&sel_attr=%25&begin_hh=0&begin_mi=0&begin_ap=a&end_hh=0&end_mi=0&end_ap=a'
	param = param.format(term_code, subject)
	resp = get_conn(section_url, subject_url, param, True);
	if resp.code !=200:
		return None
	else:
		content = resp.read()
		tree = etree.HTML(content)
		#return tree
		table = tree.xpath('./body/div/table[@class="datadisplaytable"]')[0]
		courses = {}
		rows = table.findall('tr');
		for index in range(0, len(rows), 2):
			section = {}
			title_row = rows[index]
			element_a_set = title_row.findall('th/a')
			title = element_a_set[0].text

			crn = re.findall(' - \d{5} - ',title)[0]
			section['crn']=crn.strip(' -');
			section_name = title[:title.find(crn)]
			section['name']=section_name
			title = title[title.find(crn)+len(crn):]
			_strs = title.split(' - ')
			#section['subject']=_strs[0].split(' ')[0]
			cnbr = _strs[0].split(' ')[1]
			section['number']=_strs[1]

			if len(element_a_set) > 1:
				_iter = title_row.itertext()
				_iter.next()
				_iter.next()
				link_id = _iter.next()
				link_id = link_id.strip(u'\xa0').split(': ')[1]
				section['linked_id'] = link_id
				_iter.next()
				required_link_id = _iter.next()
				required_link_id = required_link_id.strip('()');
				section['required_link_id'] = required_link_id;

			detail_row = rows[index+1]
			schedule_tables = detail_row.find('td/table').findall('tr')[1:]
			meetings = []
			for schedule_table in schedule_tables:
				meeting = {}
				_iter = schedule_table.itertext()
				for i in range(3):
					_iter.next()
				meeting['time'] = _iter.next()
				_iter.next()
				meeting['days'] = _iter.next().replace(u'\xa0','None')
				_iter.next()
				meeting['location'] = _iter.next()
				_iter.next()
				meeting['date'] = _iter.next()
				_iter.next()
				meeting['type'] = _iter.next()
				_iter.next()
				instructor = _iter.next().strip(' (')
				meeting['instructor'] = re.sub(' +',' ', instructor)
				meetings.append(meeting)
			section['meetings'] = meetings

			if courses.has_key(cnbr):
				courses[cnbr]['sections'].append(section)
				#if not section_name == courses[cnbr]['name']:
				#	raise Exception('Different name for same course %s %s' %(subject, cnbr))
			else:
				courses[cnbr] = {}
				courses[cnbr]['sections'] = [section,]
				courses[cnbr]['name'] = section_name
		return courses


def get_all_subjects(term=default_term):
	subjects = get_subjects(term)
	all_courses = []
	for subject in subjects:
		all_courses.append([subject[0], subject[1], get_sections(subject[0],term)])
		print 'Finished %s' % subject[0]
	term_code = convert_term_to_code(term)
	f = open('%s.json'%term_code, 'w')
	import json
	j = json.dumps(all_courses)
	f.write(j)
	f.flush()
	f.close()
	return all_courses

















