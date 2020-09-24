from cvs.models import Cv
from django.contrib.auth.models import User
import re
import json
from urllib import request

html = open("cv3.html")
css = open("cv3.css")

cv = Cv(name="cv3", css=css.read() , html=html.read())
rg = r"<[^~]+\<head\>[^~]+(?P<temp_name>temp_name)[^~]+(?P<temp_css>temp_css)[^~]+(?P<hum_name>hum_name)[^~]+src=\"(?P<img>img)[^~]+(?P<prof_bullet>prof_bullet)[^~]+(?P<prof_desc>prof_descript)[^~]+(?P<prof_phone>prof_phone)[^~]+?(?P<prof_address>prof_address)[^~]+?(?P<hum_mail>hum_mail)[^~]+?(?P<link_item>\<h4\>\<i\sclass=\"fab\s(?P<link_type>link_type)\"\>\<\/i\>\s(?P<link_name>link_name)\/(?P<link_id>link_id)\<\/h4\>)(?P<unimp0>[^~]+?)(?P<hum_bar>\<h3\>(?P<bar_title>bar_title)[^~]+?(?P<bar_item><li[^~]+?(?P<bar_name>bar_name)[^~]+?(?P<bar_style_without_num>bar_style_without_num)[^~]+?<\/li>)[^~]+?)(?P<unimp1>[^~]+?)(?P<exp_item>\<li\>[^~]+(?P<exp_date>exp_date)[^~]+(?P<exp_role>exp_role)[^~]+(?P<exp_desc>exp_desc)[^~]+?\<\/li\>)(?P<unimp2>[^~]+?)(?P<educ_item>\<li\>[^~]+(?P<educ_date>educ_date)[^~]+(?P<educ_name>educ_name)[^~]+(?P<educ_desc>educ_desc)[^~]+?\<\/li\>)(?P<last>[^~]+)"

loc_data = {}
for match in re.finditer(rg, cv.html):
    names = list(match.groupdict().keys())
    print(match.groupdict())
    for idx in range(len(match.groups())):
        loc_data[names[idx]] = match.span(idx+1)
cv.loc_data = json.dumps(loc_data)
print(cv.loc_data)
cv.save()

