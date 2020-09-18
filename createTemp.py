from cvs.models import Cv
from django.contrib.auth.models import User
import re
import json
from urllib import request

html = open("cv2.html")
css = open("cv2.css")

cv = Cv(name="cv2", css=css.read() , html=html.read())
rg = r"<[^~]+\<head\>[^~]+(?P<temp_name>temp_name)[^~]+(?P<temp_css>temp_css)[^~]+(?P<hum_name>hum_name)[^~]+(?P<prof_bullet>prof_bullet)[^~]+(?P<prof_address>prof_address)\s\s(?P<prof_phone>prof_phone)[^~]+?(?P<link_item>\<p\>\<i\sclass=\"fab\s(?P<link_type>link_type)\"\>\<\/i\>\s(?P<link_name>link_name)\/(?P<link_id>link_id)\<\/p\>)[^~]+(?P<prof_desc>prof_descript)[^~]+?(?P<hum_bar>\<div\>[^~]+(?P<bar_title>bar_title)[^~]+?(?P<bar_item>\<i[^~]+(?P<bar_style>bar_style)[^~]+(?P<bar_name>bar_name)<\/li>)[^~]+?<\/div>)(?P<unimp0>[^~]+?)(?P<exp_item>\<li\>[^~]+(?P<exp_date>exp_date)[^~]+(?P<exp_role>exp_role)[^~]+(?P<exp_desc>exp_desc)[^~]+?\<\/li\>)(?P<unimp1>[^~]+?)(?P<award_item>\<li\>[^~]+(?P<award_name>award_name)[^~]+(?P<award_date>award_date)[^~]+?\<\/li\>)(?P<unimp2>[^~]+?)(?P<educ_item>\<li\>[^~]+(?P<educ_date>educ_date)[^~]+(?P<educ_name>educ_name)[^~]+(?P<educ_desc>educ_desc)[^~]+?\<\/li\>)(?P<unimp3>[^~]+?)(?P<project_item>\<li\>[^~]+(?P<project_name>project_name)[^~]+(?P<project_role>project_role)[^~]+(?P<project_desc>project_desc)[^~]+?\<\/li\>)[^~]+src=\"(?P<img>img)(?P<last>[^~]+)"

loc_data = {}
for match in re.finditer(rg, cv.html):
    names = list(match.groupdict().keys())
    print(match.groupdict())
    for idx in range(len(match.groups())):
        loc_data[names[idx]] = match.span(idx+1)
cv.loc_data = json.dumps(loc_data)
print(cv.loc_data)
cv.save()

