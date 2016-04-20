#!/usr/bin/python

"""
format_convert.py: allows a user to convert between various file formats
"""

__author__  = "Shaila Haque"

import sys, os
import argparse
import csv
import json
from xml.etree.ElementTree import Element
from xml.etree.ElementTree import tostring
from cStringIO import StringIO
import xml.dom.minidom as minidom

class FormatConvertApp(object):

    def __init__(self):
        super(FormatConvertApp, self).__init__()

    def convertToDict(self, inputType, inputFile):
        """
        Convert input file to dictionary
        """

         # create a dictionary where key: People, values: array of the people
        dict = {"People":[]}
        if inputType == "csv":
            csv_data = csv.reader(open(inputFile))
            rowCount = 0
            header = []
            people = dict["People"]
            for row in csv_data:
                if rowCount == 0:
                    for col in row:
                        header.append(col)
                if not rowCount == 0:
                    person = {}
                    i = 0
                    for col in row:
                        person[header[i]] = col
                        i += 1
                    people.append(person)
                rowCount+=1

        elif inputType == "json":
            json_data = open(inputFile).read()
            dict = json.loads(json_data)

        else:
            raise IOError("Format not accepted. Sorry!")

        return dict

    def dictToType(self, dict, outputType):
        """
        Convert dict to requested format type
        """

        if outputType == "csv":
            dataIO=StringIO()
            w = csv.writer(dataIO)
            header = []
            for People, entry  in dict.items():
                for data in entry:
                    header = data.keys()
                    w.writerow(header)
                    break
                for data in entry:
                    peopleData = data.values()
                    w.writerow(peopleData)
            outputData = dataIO.getvalue()

        elif outputType == "json":
            outputData = json.dumps(dict, indent=4, sort_keys=True)

        elif outputType == "xml":
            root = "People"
            elem = Element(root)
            for person in dict["People"]:
                personData = Element("person")
                for k, v in person.items():
                    child = Element(k)
                    child.text = str(v)
                    personData.append(child)
                elem.append(personData)
            xmlData = tostring(elem, "utf-8")
            formattedData = minidom.parseString(xmlData)
            outputData = formattedData.toprettyxml(indent="\t")

        else:
            raise IOError("Invalid output type. Try again.")

        return outputData

    def publish(self, data, publishType):
        # create/overwrite file on disk
        if publishType == "txtfile":
            convertedFile = "convertedOutput.txt"
            f = open(convertedFile, 'w')
            f.writelines(data)
            f.close()
            print ("All data has been successfully serialized: " + convertedFile)
        # or write out data to console, default option if not specified
        else:
            print data


    def main(self):
        parser = argparse.ArgumentParser(description="Converter for file format types." +
                    " Input types: csv, json.  Output types: csv, json, xml.")
        parser.add_argument("-types", action="store_true", required=False,
                    help="get a list of all supported format types")
        parser.add_argument("-input", type=str, required=False,
                    help="full path for input file to convert, ex: /path/to/file.csv")
        parser.add_argument("-output", type=str, required=False,
                    help="output file type, ex: json")
        parser.add_argument("-publish", type=str, required=False, default = "console",
                    help="print output to 'console' or 'txtfile'. default = console.")

        args = parser.parse_args()
        inputFile = args.input
        outputType = args.output
        publishType = args.publish

        # check for valid args
        if len(sys.argv) == 1:
            raise IOError("Flags required. Use -h for options.")

        if (inputFile and not outputType) or (not inputFile and outputType):
            raise IOError("Input file and output format type required.")

        supportedInput = ['csv', 'json']
        supportedOutput = ['csv', 'json', 'xml']
        if args.types:
            print("The following output format types are supported: ")
            for s in supported:
                print s
            return

        # attempt to run conversion if input file exists
        if os.path.exists(inputFile):
            # check file input
            inputType = os.path.splitext(inputFile)[1][1:]
            if not (inputType in supportedInput) or not (outputType in supportedOutput):
                raise IOError("Format type not supported. Try again.")
            if inputType == outputType:
                raise IOError("Input same as output. Conversion not needed.")

            # convert input type to dictionary
            dict = self.convertToDict(inputType, inputFile)
            outputData = self.dictToType(dict, outputType)

            # write results to file or console
            self.publish(outputData, publishType)
        else:
            raise IOError("Invalid input file. Try again.")


if __name__ == '__main__':
    FormatConvertApp().main()
