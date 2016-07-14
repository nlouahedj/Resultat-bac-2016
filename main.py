#!/bin/python

import requests
import time
import threading
import re
import sqlite3


url = 'http://bac.onec.dz/index.php'

p_fname = re.compile('.*?الاسم : (.*)?مكان.*', re.DOTALL)
p_lname = re.compile('.*?اللقب : (.*)?الاسم.*', re.DOTALL)
p_birth_date = re.compile('.*?تاريخ الميلاد : (\d\d-\d\d-\d\d\d\d).*?(ألف|راسب).*', re.DOTALL)
p_birth_place = re.compile('.*?مكان الميلاد : (.*)?تاريخ.*', re.DOTALL)
p_field = re.compile('.*?الشعبة : (.*)?اللقب.*', re.DOTALL)
p_grade = re.compile('.*?المعدل : (.*)?الملاحظة.*', re.DOTALL)
# To start from this id in order
mat = 31116933


def run():
    global mat
    db = sqlite3.connect('data.db')
    db.execute("PRAGMA busy_timeout = 300000") # To avoid db locked exception
    while mat <= 39050000:
        m = mat
        mat += 1
        data = {
            'matriculebac': str(m),
            'dobac' : "استظهار+النتيجة"
        }
        try:
            r = requests.post(url, data=data).text
        except Exception:
            time.sleep(2)
            continue
        m_fname = p_fname.match(r)
        m_lname = p_lname.match(r)
        m_birth_date = p_birth_date.match(r)
        m_birth_place = p_birth_place.match(r)
        m_field = p_field.match(r)
        m_grade = p_grade.match(r)
        if m_fname:
            try:
                db.execute('''INSERT INTO grades VALUES(?,?,?,?,?,?,?)''', 
                           (data['matriculebac'],
                            m_fname.group(1).replace('\\n', ''),
                            m_lname.group(1).replace('\\n', ''),
                            m_birth_date.group(1).replace('\\n', ''),
                            m_birth_place.group(1).replace('\\n', ''),
                            m_field.group(1).replace('\\n', ''),
                            m_grade.group(1).replace('\\n', '')
                            ))
                db.commit()
                print('{}, {},{},{},{}, {}, {}'.format(data['matriculebac'],
                                                       m_fname.group(1).replace('\\n', ''),
                                                       m_lname.group(1).replace('\\n', ''),
                                                       m_birth_date.group(1).replace('\\n', ''),
                                                       m_birth_place.group(1).replace('\\n', ''),
                                                       m_field.group(1).replace('\\n', ''),
                                                       m_grade.group(1).replace('\\n', '')))
            except sqlite3.OperationalError:
                print('db locked waiting 5s')
                time.sleep(5)
            except Exception as e:
                pass
                # print(str(e))
                print('{} exists'.format(data['matriculebac']))


if __name__ == '__main__':
    threads = [threading.Thread(target=run) for i in range(5)]

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()


