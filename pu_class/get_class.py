import httplib
import urllib
import urllib2
from lxml import etree
from util import convert_code_to_term, convert_term_to_code

select_term_url = 'https://selfservice.mypurdue.purdue.edu/prod/bwckschd.p_disp_dyn_sched'
subject_url = 'https://selfservice.mypurdue.purdue.edu/prod/bwckgens.p_proc_term_date'
default_term = 'Fall2014'

def get_conn(url, ref_url, param):
	req = urllib2.Request(url)
	req.add_header('Referer', ref_url)
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
			subjects.append({sub_code:sub_name})
		return subjects
