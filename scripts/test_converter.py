import unittest
from converter import getNotebooks, updateCell, updateNotebook

class tester(unittest.TestCase):
	''' Testing the methods in converter.py '''

	def test_get_notebooks(self):
		rootdir = "../testbricks/"
		files = getNotebooks(rootdir)
		self.assertEqual(len(files), 21)

	def test_update_notebook(self):
		testfile = "Delete Duplicate Rows in Pandas DataFrame.ipynb"
		updateNotebook("../testbricks/", testfile)

	def test_update_cell_key_code(self):
		orig = {'cell_type': 'markdown', 'metadata': {}, 'source': ['# Key Code&']}
		new = dict(orig)
		updateCell(new)
		self.assertTrue('the new key code' in new['source'][0])
		self.assertNotEqual(orig['source'], new['source'])

	def test_update_cell_example(self):
		orig = {'cell_type': 'markdown', 'metadata': {}, 'source': ['# Example&']}
		new = dict(orig)
		updateCell(new)
		self.assertTrue('the new example' in new['source'][0])
		self.assertNotEqual(orig['source'], new['source'])

	def test_update_cell_learn_more(self):
		orig = {'cell_type': 'markdown', 'metadata': {}, 'source': ['# Learn More&']}
		new = dict(orig)
		updateCell(new)
		self.assertTrue('the new learn more' in new['source'][0])
		self.assertNotEqual(orig['source'], new['source'])

	def test_get_info(self):
		pass



if __name__ == '__main__':
    unittest.main()
