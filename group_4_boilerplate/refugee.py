

class Address:
    def __init__(self, address1='', address2='', city='', region='',
                 postal_code='', country='', **_):
        self.address1 = address1
        self.address2 = address2
        self.city = city
        self.region = region
        self.postal_code = postal_code
        self.country = country


class CampLocation:
    def __init__(self, shelter_number='', block='', section='', **_):
        self.shelter_number = shelter_number
        self.block = block
        self.section = section


class Person:
    def __init__(self, name='', date_of_birth='', marital_status='',
                 citizenship='', education='', occupation='', religion='',
                 ethnic_origin='', date_of_arrival='', place_of_origin=None,
                 camp_location=None, **_):
        self.name = name
        self.date_of_birth = date_of_birth
        self.marital_status = marital_status
        self.citizenship = citizenship
        self.education = education
        self.occupation = occupation
        self.religion = religion
        self.ethnic_origin = ethnic_origin
        self.date_of_arrival = date_of_arrival
        self.place_of_origin = place_of_origin or Address()
        self.camp_location = camp_location or CampLocation()

    def setPlaceOfOrigin(self, *args, **kwargs):
        self.place_of_origin = Address(*args, **kwargs)

    def setCampLocation(self, *args, **kwargs):
        self.camp_location = CampLocation(*args, **kwargs)
