#!/bin/python3
# -*- coding: utf-8 -*-

import re
import sqlite3
import threading
import time
from math import ceil, sqrt

import requests


URL = 'http://bac.onec.dz/index.php'
id_go = 39064553  # start from this id in order
# id_end = 39069999  # last id to fetch in order
id_count = 100  # how many id to get
lock = threading.RLock()  # mutex

p_fname = re.compile('.*?الاسم : (.*)?مكان.*', re.DOTALL)
p_lname = re.compile('.*?اللقب : (.*)?الاسم.*', re.DOTALL)
p_birth_date = re.compile(
  '.*?تاريخ الميلاد : (\d\d-\d\d-\d\d\d\d).*?(ألف|راسب).*', re.DOTALL)
p_birth_place = re.compile('.*?مكان الميلاد : (.*)?تاريخ.*', re.DOTALL)
p_field = re.compile('.*?الشعبة : (.*)?اللقب.*', re.DOTALL)
p_grade = re.compile('.*?المعدل : (.*)?الملاحظة.*', re.DOTALL)


def run(n):
  global id_go

  db = sqlite3.connect('data.db')
  db.execute("PRAGMA busy_timeout = 300000")  # avoid db locked exception

  i = 0
  while i < n:
    i += 1

    # locking out id_go for concurrent access
    lock.acquire()
    id_current = id_go
    id_go += 1
    lock.release()

    # post data model
    data = {'matriculebac': str(id_current), 'dobac': "استظهار+النتيجة"}

    try:
      r = requests.post(URL, data=data).text
    except Exception:
      time.sleep(2)
      print('Couldnt fetch {}'.format(id_current))
      continue

    # extract data
    fname = p_fname.match(r)
    lname = p_lname.match(r)
    birth_date = p_birth_date.match(r)
    birth_place = p_birth_place.match(r)
    field = p_field.match(r)
    grade = p_grade.match(r)
    if fname:
      try:
        db.execute('''INSERT INTO grades VALUES(?,?,?,?,?,?,?)''',
                   (data['matriculebac'],
                    fname.group(1).replace('\\n', ''),
                    lname.group(1).replace('\\n', ''),
                    birth_date.group(1).replace('\\n', ''),
                    birth_place.group(1).replace('\\n', ''),
                    field.group(1).replace('\\n', ''),
                    grade.group(1).replace('\\n', '')
                    ))
        db.commit()
        print('{}, {},{},{},{}, {}, {}'
              .format(data['matriculebac'],
                      fname.group(1).replace('\\n', ''),
                      lname.group(1).replace('\\n', ''),
                      birth_date.group(1).replace('\\n', ''),
                      birth_place.group(1).replace('\\n', ''),
                      field.group(1).replace('\\n', ''),
                      grade.group(1).replace('\\n', '')))

      except sqlite3.OperationalError:
        print('db locked waiting 5s')
        time.sleep(5)

      except Exception as e:
        # pass
        print(str(e))
        # print('{} exists'.format(data['matriculebac']))

    else:
      print('not found {}'.format(data['matriculebac']))


if __name__ == '__main__':
  # number of total IDs to fetch
  id_total = id_end - id_go \
    if (('id_end' in globals()) and (id_end > id_go)) \
    else id_count

  # scale number of threads according to requests number
  threads_count = ceil(sqrt(id_total))

  print('Total IDs to fetch: {}, using {} threads'
        .format(id_total, threads_count))

  thrds = [threading.Thread(
    target=run,
    # all threads get the same amount of requests to make
    args=(int(id_total / threads_count),)) for i in range(threads_count)]

  for thread in thrds:
    thread.start()
