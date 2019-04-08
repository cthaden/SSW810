#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created March 2019

@author: Courtney Thaden

   HW09 Tests
"""
import io
import sys
import unittest
from HW09_Thaden import Student
from HW09_Thaden import Instructor
from HW09_Thaden import University
from prettytable import PrettyTable


class HW09Test(unittest.TestCase):
    """ test for HW09 """
    maxDiff = None

    def test_students(self):
        s1 = Student(cwid=11658, name="Kelly, P", major="SSW")
        self.assertEqual(s1.cwid, 11658)
        self.assertEqual(s1.name, "Kelly, P")
        self.assertEqual(s1.major, "SSW")
        self.assertEqual(s1.grades, {})
        self.assertEqual(s1.array_format(), [11658, "Kelly, P", []])
        s1.add_course_grade(course="SSW-555", final_grade="A")
        self.assertEqual(s1.grades, {"SSW-555": "A"})
        s1.add_course_grade(course="SSW-565", final_grade="")
        self.assertEqual(s1.grades, ({"SSW-555": "A", "SSW-565": ""}))
        self.assertEqual(s1.array_format(), 
                         [11658, "Kelly, P", ["SSW-555", "SSW-565"]])
    
    def test_instructors(self):
        I1 = Instructor(cwid=98765, name="Einstein, A", dept="SFEN")
        self.assertEqual(I1.cwid, 98765)
        self.assertEqual(I1.name, "Einstein, A")
        self.assertEqual(I1.dept, "SFEN")
        self.assertEqual(I1.courses, {})
        I1.add_course_student(course="SSW-540")
        self.assertEqual(I1.courses, {"SSW-540": 1})
        I1.add_course_student(course="SSW-540")
        self.assertEqual(I1.courses, {"SSW-540": 2})
        I1.add_course_student(course="SSW-567")
        self.assertEqual(I1.courses, {"SSW-540": 2, "SSW-567": 1})
  
    def test_university(self):
        uni = University("")
        self.assertEqual(uni.students, {})
        self.assertEqual(uni.instructors, {})
        uni.dir_path = "/Users/courtneythaden/Desktop/ssw_810"
        self.assertEqual(uni.dir_path, "/Users/courtneythaden/Desktop/ssw_810")
        uni.student_process("students.txt")
        self.assertEqual(uni.students["11658"].cwid, "11658")
        self.assertEqual(uni.students["11658"].name, "Kelly, P")
        self.assertEqual(uni.students["11658"].major, "SYEN")
        self.assertEqual(uni.students["11658"].grades, {})
        uni.instructor_process("instructors.txt")
        self.assertEqual(uni.instructors["98765"].cwid, "98765")
        self.assertEqual(uni.instructors["98765"].name, "Einstein, A")
        self.assertEqual(uni.instructors["98765"].dept, "SFEN")
        self.assertEqual(uni.instructors["98765"].courses, {})
        uni.grade_process("grades.txt")
        self.assertEqual(uni.students["11658"].grades, {"SSW 540": "F"})
        self.assertEqual(uni.instructors["98765"].courses, {"SSW 567": 4, 
                                                            "SSW 540": 3})

if __name__ == '__main__':
        # note: there is no main(). Only test cases here
    unittest.main(exit=False, verbosity=2)