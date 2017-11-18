import sqlite3
import os

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
        


def main():
    PATH = os.getcwd()

    database = os.path.join(PATH,"pythonsqlite.db")
 
    create_person_table = """ CREATE TABLE IF NOT EXISTS Person (
                                        person_id integer PRIMARY KEY,
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
        
    keys = dict()
    cur = conn.cursor()
    cur.execute("""INSERT INTO Person (date_of_birth,
                                        marital_status,
                                        citizenship,
                                        education,
                                        occupation,
                                        religion,
                                        ethnic_origin,
                                        date_of_arrival) VALUES (?,?,?,?,?,?,?,?);""", ("jan","mar","usa","col","na","na","na","apr")) 
    keys['person_id'] = cur.lastrowid
    
    cur.execute("""INSERT INTO Origin_Address (address,
                                               city,
                                               postal_code,
                                               country) VALUES (?,?,?,?);""", ("jan","mar","usa","col"))
    keys['addr_id'] = cur.lastrowid
    
    cur.execute("""INSERT INTO Camp_Locations (shelter_number,
                                               block,
                                               section) VALUES (?,?,?);""", ("jan","mar","usa"))
    keys['camp_id'] = cur.lastrowid
    
    cur.execute("""INSERT INTO Person_Origin (person_id,
                                               addr_id) VALUES (?,?);""", (keys['person_id'],keys['addr_id']))
    
    cur.execute("""INSERT INTO Person_Camp (person_id,
                                               camp_id) VALUES (?,?);""", (keys['person_id'],keys['camp_id']))
    
    print(cur.execute("""SELECT * FROM Person p 
                      INNER JOIN Person_Camp pc
                      ON p.person_id = pc.person_id
                      INNER JOIN Camp_Locations cl
                      ON pc.camp_id = cl.camp_id""").fetchall())
    print(cur.execute("""SELECT * FROM Person_Camp""").fetchall())
    print(cur.execute("""SELECT * FROM Camp_Locations""").fetchall())
    

if __name__ == '__main__':
    main()