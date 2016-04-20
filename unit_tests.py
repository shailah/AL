#!/usr/bin/python

"""
unit_tests.py: unit tests for convert.py
"""

__author__  = "Shaila Haque"

import unittest
from convert import FormatConvertApp

class UnitTests(unittest.TestCase):
    def setUp(self):
        self.app = FormatConvertApp()

    def testConvertToDict(self):
        """
        Unit test to convert requested type to dictionary
        """

        goodJson = {
          "People": [
            {
              "Name": "Jane Smith",
              "Address": "10th Avenue, Los Angeles, CA 99999",
              "Phone": "222-2222"
            },
            {
              "Name": "John Doe",
              "Address": "5 Main Street, Houston, TX 77777",
              "Phone": "111-1111"
            }
          ]
        }
        result = self.app.convertToDict("json", "people.json")
        self.assertEqual(result, goodJson)

        badJson = {
          "NOT_People": [
            {
              "Name": "Jane Smith",
              "Address": "10th Avenue, Los Angeles, CA 99999",
              "Phone": "222-2222"
            },
            {
              "Name": "John Doe",
              "Address": "5 Main Street, Houston, TX 77777",
              "Phone": "111-1111"
            }
          ]
        }
        result = self.app.convertToDict("json", "people.json")
        self.assertNotEqual(result, badJson)


    def testDictToType(self):
        """
        Unit test for converting dictionary to requested type
        """

        # valid input dict
        peopleDict = {
          "People": [
            {
              "Name": "Jane Smith",
              "Address": "10th Avenue, Los Angeles, CA 99999",
              "Phone": "222-2222"
            },
            {
              "Name": "John Doe",
              "Address": "5 Main Street, Houston, TX 77777",
              "Phone": "111-1111"
            }
          ]
        }

        result = self.app.dictToType(peopleDict, "json")


    def testPublish(self):
        """
        Unit test for publish function
        """
        # output, in json form
        data = {
            "People": [
                {
                    "Address": "5 Main Street, Houston, TX 77777",
                    "Name": "John Doe",
                    "Phone": "111-1111"
                },
                {
                    "Address": "10th Avenue, Los Angeles, CA 99999",
                    "Name": "Jane Smith",
                    "Phone": "222-2222"
                }
            ]
        }
        self.app.publish(data, "txtfile")

    def tearDown(self):
        self.app = None

if __name__ == '__main__':
    unittest.main()
