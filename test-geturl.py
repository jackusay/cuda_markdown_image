import unittest
#from . import __init__ as home #error
#from . import __init__         #error
#from . import init             #error
#from __init__ import get_url   #error
#from .mdimg import *           #error
from cuda_markdown_image.__init__ import get_url
    #if use exec(open("filename.py").read()) to execute script, import part need to use absolute path!!!


class GetUrlTestCase(unittest.TestCase):
    def test_get_url(self):
        expected = r"https://octodex.github.com/images/stormtroopocat.jpg"
        result = get_url(r'some idea ![Stormtroopocat](https://octodex.github.com/images/stormtroopocat.jpg "The Stormtroopocat") do it.')
        self.assertEqual(result, expected)
    def test_get_url_include_space(self):
        expected = r"https://octodex.github.com/Ims/ca t"
        result = get_url(r'some idea ![Stocat](https://octodex.github.com/Ims/ca t "The Storocat") do it.')
        self.assertEqual(result, expected)
    def test_get_url_include_backslash(self):
        expected = r"C:\Users\Downloads\New folder\cuda_hilite"
        result = get_url(r'some idea ![Stocat](C:\Users\Downloads\New folder\cuda_hilite "The Storocat") do it.')
        self.assertEqual(result, expected)

suite = unittest.TestSuite()
suite.addTest(GetUrlTestCase('test_get_url'))
suite.addTest(GetUrlTestCase('test_get_url_include_space'))
suite.addTest(GetUrlTestCase('test_get_url_include_backslash'))

unittest.TextTestRunner(verbosity=2).run(suite)
