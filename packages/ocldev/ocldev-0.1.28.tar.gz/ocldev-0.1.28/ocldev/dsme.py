"""
Generic script to convert a CSV file to OCL-formatted JSON.
"""
import oclcsvtojsonconverter
import oclfleximporter
import pprint
import json

# csv_filename = 'dsme-test.csv'
csv_filename = 'plm-poc.csv'
verbose = False

csv_converter = oclcsvtojsonconverter.OclStandardCsvToJsonConverter(csv_filename=csv_filename, verbose=verbose)
import_list = csv_converter.process_by_definition()

# pprint.pprint(import_list[7])

if not verbose:
	for import_item in import_list:
	    print(json.dumps(import_item))

ocl_api_token = '737133c0d15ad287081bc0954d497948d01bef33'
ocl_env = 'https://api.demo.openconceptlab.org'

# bulk_import_request = oclfleximporter.OclBulkImporter.post(input_list=import_list, api_url_root=ocl_env, api_token=ocl_api_token)
# task_id = bulk_import_request.json()['task']
# import_results = oclfleximporter.OclBulkImporter.get_bulk_import_results(task_id=task_id, api_url_root=ocl_env, api_token=ocl_api_token)

importer = oclfleximporter.OclFlexImporter(
	input_list=import_list, api_url_root=ocl_env, api_token=ocl_api_token,
	test_mode=False, verbosity=2, do_update_if_exists=True)
importer.process()
