

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
    def __init__(self, file_number='', name='', date_of_birth='', marital_status='',
                 citizenship='', education='', occupation='', religion='',
                 ethnic_origin='', date_of_arrival='', place_of_origin=None,
                 camp_location=None, **_):
        self.file_number = file_number
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

    def build_person_from_form(self, form):
        self.name = form.name.data
        self.date_of_birth = form.date_of_birth.data
        self.marital_status = form.marital_status.data
        self.citizenship = form.citizenship.data
        self.education = form.education.data
        self.occupation = form.occupation.data
        self.religion = form.religion.data
        self.ethnic_origin = form.ethnic_origin.data
        self.date_of_arrival = form.date_of_arrival.data
        self.place_of_origin = Address(form.address1.data, '', form.city.data, form.region.data, form.postal_code.data, form.country.data)
        self.camp_location = CampLocation(form.shelter_number.data, form.block.data, form.section.data)


    def __repr__(self):
        return "{},{},{}".format(self.name, self.date_of_birth, self.date_of_arrival)
