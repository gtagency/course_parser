import re,json,urllib2

# This creates a list of colleges to use when POSTing the Oscar page
colleges_html = open("oscar_courseform.htm", "r").read()
colleges_regex = "<option value=\"(.*)\">(.*)"
colleges = re.findall(colleges_regex,colleges_html)

courses = []

# Oscar URL to post request
url = "https://oscar.gatech.edu/pls/bprod/bwckctlg.p_display_courses"
for college in colleges:
	# Some hacking to figure this out
	data = "term_in=201308&call_proc_in=bwckctlg.p_disp_dyn_ctlg&sel_subj=dummy&sel_levl=dummy&sel_schd=dummy&sel_coll=dummy&sel_divs=dummy&sel_dept=dummy&sel_attr=dummy&sel_subj=" + college[0] + "&sel_crse_strt=&sel_crse_end=&sel_title="
	urlsoc = urllib2.urlopen(url,data)
	raw_html = urlsoc.read()
	urlsoc.close()

	# College name
	print college[1]

	courses_html = raw_html.split("<td CLASS=\"nttitle\"")[1:]
	course_regex = "<a href=\".*\">([A-Z]*) ([\w]*) - (.*)</a>"
	credit_regex = "([\d]\.[\d]+) Credit hours"

	# Each course_html is a block of raw html for each course
	for course_html in courses_html:
		# List of captured components from out Regex
		raw_course = re.findall(course_regex,course_html)[0]	
		course = {}

		course["college"] = raw_course[0]
		course["id"] =  raw_course[1] 
		course["title"] = raw_course[2]
		credits = re.findall(credit_regex,course_html)
		# Some courses are weird and have no "Credit hours". 
		# This just sets credits to 0 if there are none 
		if len(credits) < 1:
			course["credit"] = credits[0]
		else:
			course["credit"] = 0.000
		courses.append(course)

		print course

courses_json_str = json.dumps(courses)
# print courses
open("courses.json", "w").write(courses_json_str)

