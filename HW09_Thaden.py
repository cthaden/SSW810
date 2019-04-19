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


def file_reader(dir, n, separator=",", is_header=False):
    """ returns each line of a file after stripping it and splitting it
    based on the separator
    """
    line_count = 0
    try:
        fp = open(dir, 'r')
    except:
        raise FileNotFoundError("Can't open", dir)
    else:
        with fp:
            if is_header and line_count == 0:
                line_count += 1
            else:
                for line in fp:
                    x = line.strip("\r\n").split(separator)
                    if len(x) != n:
                        line_count += 1
                        raise ValueError(f" {dir} has {len(x)} on line \
                                         {line_count} but expected {n}.")
                    else:
                        yield x
                    line_count += 1


class Student:
    """ Student class that stores cwid, name, major, and a container
    of courses and grades.
    """
    def __init__(self, cwid="", name="", major=""):
        """ student has cwid, name, and major, and courses and grades"""
        self.cwid = cwid
        self.name = name
        self.major = major
        self.grades = defaultdict(str)
        self.completed_courses = set()
        self.courses_to_complete = set()
        self.electives = set()

    def add_course_grade(self, course="", final_grade=""):
        """ function to add a final grade for a course in student class
        """
        self.grades[course] = final_grade
        if final_grade in ["A", "A-", "B+", "B", "B-", "C+", "C"]:
            self.completed_courses.add(course)

    def courses_required_add(self, course=""):
        """ add course to courses to complete if not already passed
        """
        if course not in self.completed_courses:
            self.courses_to_complete.add(course)

    def courses_elective_add(self, course=""):
        """ add course to courses to complete if not already passed
        """
        self.electives.add(course)

    def array_format(self):
        """ returns array that can be used for prettytable"""
        elective_taken = False
        for courses in self.completed_courses:
            if courses in self.electives:
                elective_taken = True
                break
        if elective_taken is True:
            elective_left = "None"
        else:
            elective_left = sorted(self.electives)
        return[self.cwid, self.name, self.major,
               sorted(self.completed_courses),
               sorted(self.courses_to_complete), elective_left]


class Instructor:
    """ Instructor class that stores cwid, name, department, and a container
    of courses taught and number of students in each course
    """
    def __init__(self, cwid="", name="", dept=""):
        """ instructor has cwid, name, department, and courses and number
        of students in each course
        """
        self.cwid = cwid
        self.name = name
        self.dept = dept
        self.courses = defaultdict(int)

    def add_course_student(self, course=""):
        """ function to add a student to a particular course for instructor
        class
        """
        self.courses[course] += 1

    def array_format(self):
        """ returns array that can be used for prettytable"""
        for course in sorted(self.courses):
            yield [self.cwid, self.name, self.dept, course,
                   self.courses[course]]


class Major:
    """ Major class
    """
    def __init__(self, official_major=""):
        """ major has a name, required courses, and elective
            courses
        """
        self.major = official_major
        self.required = set()
        self.elective = set()

    def courses_required_elective(self, course="", flag=""):
        """ separates required courses into a list and
            elective courses into a list
        """
        if flag == "R":
            self.required.add(course)
        elif flag == "E":
            self.elective.add(course)

    def array_format(self):
        """ returns array that can be used for prettytable"""
        return[self.major, sorted(self.required), sorted(self.elective)]


class University:
    """ University class holds all data for a specific organization
    """
    def __init__(self, dir_path):
        """ university has a directory path that points to where to find
        the following files: students.txt, instructors.txt, grades.txt
        """
        self.students = {}
        self.instructors = {}
        self.majors = {}
        if dir_path != "":
            self.load_from_path(dir_path)

    def student_process(self):
        """ processes student information from database
        """
        try:
            students = self._db.execute("select CWID, NAME, MAJOR from \
                                         STUDENTS")
        except sqlite3.OperationalError:
            print("Unable to load the students data from the database.")
        else:
            for cwid, name, major in students:
                self.students[cwid] = Student(cwid, name, major)

    def instructor_process(self):
        """ processes instructor information from database
        """
        try:
            instructors = self._db.execute("select CWID, NAME, DEPT from \
                                            INSTRUCTORS")
        except sqlite3.OperationalError:
            print("Unable to load the instructors data from the database.")
        else:
            for cwid, name, dept in instructors:
                self.instructors[cwid] = Instructor(cwid, name, dept)

    def grade_process(self):
        """ processes grade information from database, adds to student info,
        adds an additional person to instructor's course count
        """
        try:
            grades = self._db.execute("select STUDENT_CWID, COURSE, GRADE, \
                                       INSTRUCTOR_CWID from GRADES")
        except sqlite3.OperationalError:
            print("Unable to load the grades data from the database.")
        else:
            for g_details in grades:
                if g_details[0] in self.students.keys():
                    self.students[g_details[0]].add_course_grade(
                                                    course=g_details[1],
                                                    final_grade=g_details[2])
                if g_details[3] in self.instructors.keys():
                    self.instructors[g_details[3]].add_course_student(
                                                   course=g_details[1])

    def major_process(self):
        """ processes major information from database
        """
        try:
            majors = self._db.execute("select MAJOR, COURSE from MAJORS")
        except sqlite3.OperationalError:
            print("Unable to load the majors data from the database.")
#        else:
#            for official_major, course in majors:
#                for s in self.students.keys():
#                    if self.students[s].major == official_major:
#                        if flag is "R":
#                            self.students[s].courses_required_add(course)
#                        elif flag is "E":
#                            self.students[s].courses_elective_add(course)
#                if official_major not in self.majors.keys():
#                    self.majors[official_major] = Major(official_major)
#                self.majors[official_major].courses_required_elective(course,
#                                                                      flag)

#    def student_prettytable(self):
#        """ This prints the prettytable for students
#        """
#        pt = PrettyTable(field_names=['CWID', 'Name', 'Major',
#                                      'Completed Courses',
#                                      'Remaining Required',
#                                      'Remaining Electives'])
#        for s in self.students.keys():
#            pt.add_row(self.students[s].array_format())
#        return pt

    def instructor_prettytable(self):
        """ This prints the prettytable for instructors
        """
        pt = PrettyTable(field_names=['CWID', 'Name', 'Dept', 'Course',
                                      'Students'])
        for i in self.instructors.keys():
            for c in self.instructors[i].array_format():
                pt.add_row(c)
        return pt

    def major_prettytable(self):
        """ This prints the prettytable for majors
        """
        pt = PrettyTable(field_names=['Dept', 'Required', 'Electives'])
        for major in self.majors.keys():
            pt.add_row(self.majors[major].array_format())
        return pt
    
    def load_from_path(self, dir_path):
        """ load all necessary files
        """
        db_path = os.path.join(dir_path, "810_startup.db")
        self._db = sqlite3.connect(db_path)
#       self.student_process()
        self.instructor_process()
        self.grade_process()
#        self.majors_process()


if __name__ == '__main__':
    """ print students and print instructors
    """
    uni = University(dir_path="/Users/courtneythaden/Desktop/ssw_810/hw")
    print(uni.instructor_prettytable())
