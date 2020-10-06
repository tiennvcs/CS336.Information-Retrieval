import os
import re
import json


def load_categories(path):
    f = open(path)
    data = json.loads(f.read())
    return data


def get_info(article):

    link_rg_str = '(?<=href=\").*?(?=\")'
    link_regex = re.compile(link_rg_str, flags=re.I | re.S)

    link_content = re.findall(link_regex, article)[0]
    title_rg_str = '(?<=>).*?(?=\<)'
    title_regex = re.compile(title_rg_str, flags=re.I | re.S)
    title_content = re.findall(title_regex, article)[1]  # vi don gian no o vi tri thu 1
    return {
        "url": "https://dantri.com.vn{pa}".format(pa=link_content),
        "title": title_content.strip(),
    }


def generate_url(cateName, day=1):
    # if cateName == 'cong-nghe' or cateName == 'the-thao':
    #     return 'https://{sub}.data.vn/{cate}/xem-theo-ngay/{day}-9-2020.htm'.format(sub=cateName.replace('-',''),cate=cateName, day=day)

    return 'https://dantri.com.vn/{cate}/{day}-9-2020.htm'.format(cate=cateName, day=day)
    # return "https://vnexpress.net/category/day?cateid={cate}&fromdate=1598979600&todate=1601485199&allcate=0&page={page}".format(
    #     cate=cateid, page=page)


def save_data(data, filepath):
	print("[INFO] Saving data to {} directory...".format(filepath))
	filepath = os.path.join(os.getcwd(), filepath)
	f = open(filepath, "w+", encoding='utf-8')
	f.write(json.dumps(data, ensure_ascii=False))
	f.close()
	return filepath