from lxml import etree
from get_class import get_conn, get_subjects
from util import convert_code_to_term, convert_term_to_code

catalog_display_url = 'https://selfservice.mypurdue.purdue.edu/prod/bwckctlg.p_display_courses'
catalog_search_url ='https://selfservice.mypurdue.purdue.edu/prod/bwckctlg.p_disp_cat_term_date'
default_term = 'Fall2014'
param ='term_in={0}&call_proc_in=bwckctlg.p_disp_dyn_ctlg&sel_subj=dummy&sel_levl=dummy&sel_schd=dummy&sel_coll=dummy&sel_divs=dummy&sel_dept=dummy&sel_attr=dummy&sel_subj={1}&sel_crse_strt=&sel_crse_end=&sel_title=&sel_levl=%25&sel_schd=%25&sel_coll=%25&sel_divs=%25&sel_dept=%25&sel_from_cred=&sel_to_cred=&sel_attr=%25'

def get_catalogs(subject, term=default_term):
    term_code = convert_term_to_code(term)
    param ='term_in={0}&call_proc_in=bwckctlg.p_disp_dyn_ctlg&sel_subj=dummy&sel_levl=dummy&sel_schd=dummy&sel_coll=dummy&sel_divs=dummy&sel_dept=dummy&sel_attr=dummy&sel_subj={1}&sel_crse_strt=&sel_crse_end=&sel_title=&sel_levl=%25&sel_schd=%25&sel_coll=%25&sel_divs=%25&sel_dept=%25&sel_from_cred=&sel_to_cred=&sel_attr=%25'
    param = param.format(term_code, subject)
    resp = get_conn(catalog_display_url, catalog_search_url, param, True);
    if resp.code !=200:
        return None
    else:
        content = resp.read()
        tree = etree.HTML(content)
        table = tree.xpath('./body/div/table[@class="datadisplaytable"]')[0]
        catalogs = []
        rows = table.findall('tr');
        for index in range(0, len(rows), 2):
            title_row = rows[index]
            element_a_set = title_row.findall('td/a')
            title = element_a_set[0].text
            # handle title
            split_index = title.find(' - ')
            course = title[:split_index].replace(' ','')
            name = title[split_index+3:]

            detail_row = rows[index+1]
            _iter = detail_row.itertext()
            _iter.next()
            description = _iter.next()
            description = description.strip('\n')

            catalog = {
                'course': course,
                'name': name,
                'description': description,
            }
            catalogs.append(catalog)
        return catalogs

def get_all_catalogs(term=default_term):
    subjects = get_subjects(term)
    all_catalogs = {}
    for subject in subjects:
        catalogs = get_catalogs(subject[0], term)
        for catalog in catalogs:
            all_catalogs[catalog['course']]=catalog
        print 'Finished %s' % subject[0]
    term_code = convert_term_to_code(term)
    f = open('%s_catalogs.json'%term_code, 'w')
    import json
    j = json.dumps(all_catalogs)
    f.write(j)
    f.flush()
    f.close()