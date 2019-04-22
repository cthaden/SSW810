#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created April 2019

@author: Courtney Thaden
"""

import os
import sys
from collections import defaultdict
from prettytable import PrettyTable
import sqlite3
from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def hello():
    return "Hello world! This is Flask!"


@app.route('/instructor_courses')
def instructor_courses():
    """ processes instructor information from database
    """
    query = """select d.CWID, d.Name, d.Dept, d.Course, f.Students
               from
               (select distinct i.CWID, i.Name, i.Dept, g.Course
               from Instructors i
               join Grades g on g.Instructor_CWID=i.CWID) d
               join (select Course, Students
               from(select Course, count(Course) Students from Grades
               where Student_CWID = Grade not null
               group by Course)) f on d.Course=f.Course"""

    db_path = os.path.join("/Users/courtneythaden/Desktop/ssw_810/hw", "810_startup.db")
    db = sqlite3.connect(db_path)
    results = db.execute(query)

    # convert the query results into list  of dictionaries
    data = [{'cwid': cwid, 'name': name, 'department': department, 'course': course, 'students': students}
            for cwid, name, department, course, students in results]
    
    db.close()

    return render_template('parameters.html',
                           title="Stevens Repository",
                           table_title="Number of students by course and instructor",
                           instructors=data)


app.run(debug=True)
