import sqlite3
import os
import sys
import csv

import refugee

DATABASE_CON = os.path.join(os.getcwd(),"pythonsqlite.db")

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return None


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def create_tables(database):
    """ declare sqlite schema
    """

    create_person_table = """ CREATE TABLE IF NOT EXISTS Person (
                                        person_id integer PRIMARY KEY,
                                        name text NOT NULL,
                                        date_of_birth text NOT NULL,
                                        marital_status text NOT NULL,
                                        citizenship text NOT NULL,
                                        education text NOT NULL,
                                        occupation text NOT NULL,
                                        religion text NOT NULL,
                                        ethnic_origin text NOT NULL,
                                        date_of_arrival text NOT NULL
                                    ); """

    create_origin_address_table = """CREATE TABLE IF NOT EXISTS Origin_Address (
                                    addr_id integer PRIMARY KEY,
                                    address text NOT NULL,
                                    region text NOT NULL,
                                    city text NOT NULL,
                                    postal_code text NOT NULL,
                                    country text NOT NULL
                                );"""

    create_camp_locations_table = """CREATE TABLE IF NOT EXISTS Camp_Locations (
                                    camp_id integer PRIMARY KEY,
                                    shelter_number text NOT NULL,
                                    block text NOT NULL,
                                    section text NOT NULL
                                );"""

    create_person_origin_table = """CREATE TABLE IF NOT EXISTS Person_Origin (
                                    unique_id  integer PRIMARY KEY,
                                    person_id integer NOT NULL,
                                    addr_id integer NOT NULL,
                                    FOREIGN KEY (person_id) REFERENCES Person(person_id),
                                    FOREIGN KEY (addr_id) REFERENCES Origin_Address(addr_id)
                                );"""

    create_person_camp_table = """CREATE TABLE IF NOT EXISTS Person_Camp (
                                    unique_id integer PRIMARY KEY,
                                    person_id integer NOT NULL,
                                    camp_id integer NOT NULL,
                                    FOREIGN KEY (person_id) REFERENCES Person(person_id),
                                    FOREIGN KEY (camp_id) REFERENCES Camp_Locations(camp_id)
                                );"""

    # create a database connection
    conn = create_connection(database)
    if conn is not None:
        # create projects table
        create_table(conn, create_person_table)
        create_table(conn, create_origin_address_table)
        create_table(conn, create_camp_locations_table)
        create_table(conn, create_person_origin_table)
        create_table(conn, create_person_camp_table)
    else:
        print("Error! cannot create the database connection.")
    conn.commit()
    conn.close()



def refugee_db_insertion(prsn, database):
    """ Add a row to database to verify table creation
        Args: person object to add into database
    """
    keys = dict()
    conn = create_connection(database)
    print(repr(prsn))

    if not conn:
        sys.exit('Error, cannon create db connection')
    cur = conn.cursor()

    cur.execute("""INSERT INTO Person (name,
                                        date_of_birth,
                                        marital_status,
                                        citizenship,
                                        education,
                                        occupation,
                                        religion,
                                        ethnic_origin,
                                        date_of_arrival) VALUES (?,?,?,?,?,?,?,?,?);""", (prsn.name,
                                                                                        prsn.date_of_birth,
                                                                                        prsn.marital_status,
                                                                                        prsn.citizenship,
                                                                                        prsn.education,
                                                                                        prsn.occupation,
                                                                                        prsn.religion,
                                                                                        prsn.ethnic_origin,
                                                                                        prsn.date_of_arrival))
    keys['person_id'] = cur.lastrowid

    cur.execute("""INSERT INTO Origin_Address (address,
                                               city,
                                               region,
                                               postal_code,
                                               country) VALUES (?,?,?,?,?);""", (prsn.place_of_origin.address1,
                                                                               prsn.place_of_origin.city,
                                                                               prsn.place_of_origin.region,
                                                                               prsn.place_of_origin.postal_code,
                                                                               prsn.place_of_origin.country))
    keys['addr_id'] = cur.lastrowid

    cur.execute("""INSERT INTO Camp_Locations (shelter_number,
                                               block,
                                               section) VALUES (?,?,?);""", (prsn.camp_location.shelter_number,
                                                                             prsn.camp_location.block,
                                                                             prsn.camp_location.section))
    keys['camp_id'] = cur.lastrowid

    cur.execute("""INSERT INTO Person_Origin (person_id,
                                               addr_id) VALUES (?,?);""", (keys['person_id'],keys['addr_id']))

    cur.execute("""INSERT INTO Person_Camp (person_id,
                                               camp_id) VALUES (?,?);""", (keys['person_id'],keys['camp_id']))

    conn.commit()
    conn.close()


def refugee_db_selection(person_id, database):

    conn = create_connection(database)

    if not conn:
        sys.exit('Error, cannon create db connection')
    cur = conn.cursor()

    result = cur.execute("""SELECT p.person_id, p.name, p.date_of_birth, p.marital_status,
                       p.citizenship, p.education, p.occupation, p.religion, p.ethnic_origin,
                       p.date_of_arrival,
                       oa.address, oa.city, oa.region, oa.postal_code, oa.country,
                       cl.shelter_number, cl.block, cl.section
                       FROM Person p
                       INNER JOIN Person_Origin po ON po.person_id = p.person_id
                       INNER JOIN Origin_Address oa ON oa.addr_id = po.addr_id
                       INNER JOIN Person_Camp pc ON pc.person_id = p.person_id
                       INNER JOIN Camp_Locations cl ON cl.camp_id = pc.camp_id
                       WHERE p.person_id=?;""", person_id)
    result = list(result)

    if len(result) != 1:
        raise Exception("Database selection returned invalid number of results")

    result = result[0]

    newP = refugee.Person(*result[1:10])
    newP.setPlaceOfOrigin(result[10], '', *result[11:15])
    newP.setCampLocation(*result[15:])

    return newP


def execute_test_join(database):
    """ test table creation by making join based queries
    """

    conn = create_connection(database)

    if not conn:
        sys.exit('Error, cannon create db connection')
    cur = conn.cursor()

    print(cur.execute("""SELECT * FROM Person p
                      INNER JOIN Person_Camp pc
                      ON p.person_id = pc.person_id
                      INNER JOIN Camp_Locations cl
                      ON pc.camp_id = cl.camp_id""").fetchall())
    print(cur.execute("""SELECT * FROM Person_Camp""").fetchall())
    print(cur.execute("""SELECT * FROM Camp_Locations""").fetchall())
    print(cur.execute("""SELECT * FROM Person""").fetchall())
    conn.close()


def fill_db_with_mock_data(file, database_con):
    """ fill database with "mock" data
    """

    person_attributes = set(('name', 'date_of_birth', 'marital_status', 'citizenship',
                             'education', 'occupation', 'religion', 'ethnic_origin', 'date_of_arrival'))
    place_of_orig_attrs = set(('address1', 'city', 'region', 'postal_code', 'country'))
    camp_loc_attrs = set(('shelter_number', 'block', 'section'))

    # use context manager to open csv data
    with open(file, newline='') as csvfile:

        fo = csv.reader(csvfile, delimiter=',')
        column_names = next(fo)
        for row in fo:
            person_dict = dict()
            place_orig_dict = dict()
            camp_loc_dict = dict()

            for i in zip(column_names, row):
                if i[0] in person_attributes:
                    person_dict[i[0]] = i[1]
                elif i[0] in place_of_orig_attrs:
                    place_orig_dict[i[0]] = i[1]
                elif i[0] in camp_loc_attrs:
                    camp_loc_dict[i[0]] = i[1]
                else:
                    sys.exit('invalid value found in csv column header: {}'.format(i[0]))

            person_dict['place_of_origin'] = refugee.Address(**place_orig_dict)
            person_dict['camp_location'] = refugee.CampLocation(**camp_loc_dict)
            person = refugee.Person(**person_dict)
            refugee_db_insertion(person, database_con)

if __name__ == '__main__':

    person = refugee.Person('John M Doe', '2010-10-20', 'married', 'American',
                    'High School', 'Mason', 'Agnostic', 'White',
                    '2017-11-16')
    person.setPlaceOfOrigin('123 Pleasant St', '', 'Sharpsburg',
                            'MD', '12345', 'US')
    person.setCampLocation('23F', 'D', '4')



    create_tables(DATABASE_CON)
    fill_db_with_mock_data('MOCK_DATA.csv', DATABASE_CON)
    execute_test_join(DATABASE_CON)
