
import app
import unittest
from flask import json


class AppTestCase(unittest.TestCase):

    def setUp(self):
        app.app.testing = True
        self.app = app.app.test_client()

    def test_reg2db(self):
        """
        Test /reg2db.

        In the future /reg2db will update the database with the form data from
        /reg2. But for now, /reg2db takes the post data from /reg2 and prints
        it back out to the page.

        This test makes sure that when /reg2db parses the data from /reg2, that
        the output is the same thing that was put into it.
        """
        payload = {
            'new_entity': '0',
            'name': 'John M Doe',
            'date_of_birth': '2010-10-20',
            'marital_status': 'married',
            'citizenship': 'American',
            'education': 'High School',
            'occupation': 'Mason',
            'religion': 'Agnostic',
            'ethnic_origin': 'White',
            'address1': '123 Pleasant St',
            'address2': '',
            'city': 'Sharpsburg',
            'region': 'MD',
            'postal_code': '12345',
            'country': 'US',
            'shelter_number': '23F',
            'block': 'D',
            'section': '4',
            'date_of_arrival': '2017-11-16'
            }

        response = self.app.post('/reg2db', data=payload)

        obj = json.loads(response.data)
        assert obj == payload

if __name__ == '__main__':
    unittest.main()
