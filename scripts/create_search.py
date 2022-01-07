import os
from bs4 import BeautifulSoup as bs
import sqlite3

con = sqlite3.connect('/home/imconfusednow/cv_project/db.sqlite3')
cur = con.cursor()

cur.execute("DELETE FROM mywork_site_contents")
con.commit()


pages = {
    "cv" : "About Me",
    "contact": "Contact",
    "ecommerce": "Ecommerce",
    "projects" : "Hobby Projects"
}

def get_templates():
    return os.listdir("/home/imconfusednow/cv_project/mywork/templates/mywork")

def write_template(template):
    tags = {}
    file = open("/home/imconfusednow/cv_project/mywork/templates/mywork/" + template).read()
    soup = bs(file, 'html.parser')
    for i in soup.find_all():
        if i.name == "Script":continue
        if i.name in tags:
            tags[i.name] += 1
        else:
            tags[i.name] = 0
        write_record(i.name, tags[i.name], i.string, template)

def write_record(tag, number, content, template):
    template = template.split(".")[0]
    name = pages[template]
    con = sqlite3.connect('/home/imconfusednow/cv_project/db.sqlite3')
    cur = con.cursor()
    cur.execute(f"INSERT INTO mywork_site_contents (link, result, number, tag, name) VALUES('{template}', '{content}', {number}, '{tag}', '{name}')")
    con.commit()

templates = get_templates()

for t in templates:
    if (t.split(".")[0] in pages):
        write_template(t)


con.close()