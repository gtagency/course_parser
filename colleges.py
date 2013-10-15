import re,json

raw_html = open("oscar_courseform.htm", "r").read()

#html_regex = "<OPTION VALUE=\"(.*)\">(.*)"
html_regex = "<option value=\"(.*)\">(.*)"

colleges = re.findall(html_regex,raw_html)

for college in colleges:
	print "'" + college[0] +"' => '" + college[1] + "',"