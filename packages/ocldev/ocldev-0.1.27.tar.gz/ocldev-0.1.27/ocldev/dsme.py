"""
Generic script to convert a CSV file to OCL-formatted JSON.
"""
import oclcsvtojsonconverter
import pprint
import json

csv_filename = 'dsme-test.csv'
verbose = True

csv_converter = oclcsvtojsonconverter.OclStandardCsvToJsonConverter(csv_filename=csv_filename, verbose=verbose)
results = csv_converter.process_by_definition()

if not verbose:
	for result in results:
	    print(json.dumps(result))
