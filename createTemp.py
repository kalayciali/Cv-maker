from cvs.models import Cv
from django.contrib.auth.models import User
import re
import json

html = open("cv1.html")
css = open("cv1.css")
cv = Cv(name="cv1", css=css.read(), html=html.read())
rg = r"[^~]+\<head\>[^~]+(?P<temp_name>---)[^~]+(?P<temp_css>---)[^~]+src=\"(?P<img>---)\"[^~]+(?P<hum_name>---)[^~]+(?P<prof_bullet>---)[^~]+(?P<prof_address>---)[^~]+(?P<hum_bar>\<div.+resume_skills[^~]+(?P<bar_title>---)[^~]+?(?P<bar_item><li[^~]+(?P<bar_name>---)[^~]+(?P<bar_style>---)[^~]+(?P<bar_star>---)[^~]+?<\/li>)[^~]+)<div id=\"links[^~]+(?P<link_item><li id=\"link\"[^~]+(?P<link_type>---)[^~]+(?P<link_name>---)[^~]+(?P<link_id>---)[^~]+?\<\/li\>)[^~]+(?P<prof_desc>---)[^~]+?(?P<exp_item>\<li\>[^~]+(?P<exp_date>---)[^~]+(?P<exp_role>---)[^~]+(?P<exp_desc>---)[^~]+?\<\/li\>)[^~]+?(?P<educ_item>\<li\>[^~]+(?P<educ_date>---)[^~]+(?P<educ_name>---)[^~]+(?P<educ_desc>---)[^~]+?\<\/li\>)"
loc_data = {}
for match in re.finditer(rg, cv.html):
    names = list(match.groupdict().keys())
    print(match.groupdict())
    for idx in range(len(match.groups())):
        loc_data[names[idx]] = match.span(idx+1)
cv.loc_data = json.dumps(loc_data)
cv.save()

