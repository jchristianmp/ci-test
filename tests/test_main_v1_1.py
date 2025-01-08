import unittest
from my_app.main_app_v1_1 import add

class TestMain(unittest.TestCase):
    def test_add(self):
        self.assertAlmostEqual(add(1,2),3)
        self.assertAlmostEqual(add(-1,1),0)
        self.assertAlmostEqual(add(0,0),0)

if __name__=='__main__':
    unittest.main()