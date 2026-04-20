from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest
import time

class NewVisitorTest(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_can_start_searching_and_view_results(self):
        self.browser.get('http://localhost:8000')
        self.assertIn('BioInference', self.browser.title)

        inputbox = self.browser.find_element("name", "q")
        self.assertEqual(
             inputbox.get_attribute('placeholder'),
             'Enter DNA pattern (e.g. ATGC)'
        )
        
        inputbox.send_keys('ATGC')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        body = self.browser.find_element("tag name", "body").text
        self.assertIn('Marker ATGC found!', body)
        self.assertIn('High coding potential', body)
     
        inputbox = self.browser.find_element("name", "q")
        inputbox.clear()
        inputbox.send_keys('ZZZZ')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)
    
        body = self.browser.find_element("tag name", "body").text
        self.assertIn('Marker not found.', body)

if __name__ == '__main__':
    unittest.main()
