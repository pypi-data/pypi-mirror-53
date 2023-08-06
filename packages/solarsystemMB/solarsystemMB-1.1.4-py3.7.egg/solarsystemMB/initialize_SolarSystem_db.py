"""Populate the database with available solar system data.i
Tables are created for Solar System Objects and naif_ids.
A SSObject datatype is also created."""
import glob
import os
import os.path
import psycopg2
from astropy.io import ascii
import sys
import types


def database_connect(database=None, port=None, return_con=True):
    """Wrapper for psycopg2.connect() that determines which database and port to use.

    :param database: Default = None to use value from config file
    :param port: Default = None to use value from config file
    :param return_con: False to return database name and port instead of connection
    :return: Database connection with autocommit = True unless return_con = False
    """
    configfile = os.path.join(os.environ['HOME'], '.nexoclom')
    config = {}
    if os.path.isfile(configfile):
        for line in open(configfile, 'r').readlines():
            key, value = line.split('=')
            config[key.strip()] = value.strip()

        if (database is None) and ('database' in config):
            database = config['database']
        else:
            pass

        if (port is None) and ('port' in config):
            port = int(config['port'])
        else:
            pass
    else:
        pass

    if database is None:
        database = 'thesolarsystemmb'
    else:
        pass

    if port is None:
        port = 5432
    else:
        pass

    if return_con:
        con = psycopg2.connect(database=database, port=port)
        con.autocommit = True

        return con
    else:
        return database, port

def create_SSObject():
    with database_connect() as con:
        cur = con.cursor()
        query = """
                SELECT exists
                (select 1 from pg_type where typname = 'ssobject');
                """
        cur.execute(query)
        result = cur.fetchall()
        if not result[0][0]:
            query_ = open(os.path.join(os.path.dirname(__file__),
                                       'data', 'sso_query.sql'), 'r').read()
            query = query_.replace('\n', '')
            cur.execute(query)

def initialize_SolarSystem_db(force=False):
    """Add Solar System information to the database
    Currently the solar system data is in a hand-made table, but it would
    be great to get this information directly from the SPICE kernels

    **Parameters**

    database
        Name of the PostgeSQL database to use. Default is 'thesolarsystemmb'
        and there should be no reason to change this. This database is used
        for all nexoclom modules.

    force
        By default, the database tables are only created if they do not already
        exist. Set force to True to force the tables to be remade. This would
        be necessary if there are updates to the atomic data.

    **Output**
    No output."""
    
    if isinstance(sys.modules['psycopg2'], types.ModuleType):
        # Get database name and port
        database, port = database_connect(return_con=False)

        # Verify postgres is running
        status = os.popen('pg_ctl status').read()
        if 'no server running' in status:
            os.system(f'pg_ctl start -D $HOME/.postgres/main'
                      f'-l $HOME/.postgres/logfile -o "-p {port}"')
        else:
            pass
        
        # Create database if necessary
        with database_connect(database='postgres') as con:
            cur = con.cursor()
            cur.execute('select datname from pg_database')
            dbs = [r[0] for r in cur.fetchall()]

            if database not in dbs:
                print(f'Creating database {database}')
                cur.execute(f'create database {database}')
            else:
                pass

        # Populate the database tables
        with database_connect() as con:
            # Drop the old table (if necessary) and create a new one
            con.autocommit = True
            cur = con.cursor()
            cur.execute('select table_name from information_schema.tables')
            tables = [r[0] for r in cur.fetchall()]

            if ('solarsystem' in tables) and force:
                cur.execute('drop table solarsystem')
            else:
                pass

            if ('solarsystem' not in tables) or force:
                # Create SSObject datatype
                try:
                    cur.execute('''CREATE TYPE SSObject
                                   as ENUM (
                                        'Milky Way',
                                        'Sun',
                                        'Mercury',
                                        'Venus',
                                        'Earth',
                                        'Mars',
                                        'Jupiter',
                                        'Saturn',
                                        'Uranus',
                                        'Neptune',
                                        'Ceres',
                                        'Pluto',
                                        'Moon',
                                        'Phobos',
                                        'Deimos',
                                        'Io',
                                        'Europa',
                                        'Ganymede',
                                        'Callisto',
                                        'Mimas',
                                        'Enceladus',
                                        'Tethys',
                                        'Dione',
                                        'Rhea',
                                        'Titan',
                                        'Hyperion',
                                        'Iapetus',
                                        'Phoebe',
                                        'Charon',
                                        'Nix',
                                        'Hydra')''')
                except:
                    pass

                # Create the database table
                print('Creating solarsystem table')
                cur.execute('''CREATE TABLE SolarSystem (
                                 Object SSObject UNIQUE,
                                 orbits SSObject,
                                 radius float,
                                 mass float,
                                 a float,
                                 e float,
                                 tilt float,
                                 rotperiod float,
                                 orbperiod float)''')

                planfile = glob.glob(os.path.join(os.path.dirname(__file__),
                                                  'data',
                                                  'PlanetaryConstants.dat'))
                plantable = ascii.read(planfile[0], delimiter=':', comment='#')

                for row in plantable:
                    cur.execute('''INSERT into SolarSystem VALUES
                                       (%s, %s, %s, %s, %s, %s, %s, %s, %s)''',
                                       tuple(row))

            if ('naifids' in tables) and force:
                cur.execute('drop table naifids')
            else:
                pass

            if ('naifids' not in tables) or force:
                print('Creating naifids table')
                cur.execute('''CREATE table naifids (id int, object text)''')

                naifid_file = glob.glob(os.path.join(os.path.dirname(__file__),
                                                     'data', 'naif_ids.dat'))
                for line in open(naifid_file[0], 'r').readlines():
                    if ':' in line:
                        line2 = line.split(':')
                        id = int(line2[0].strip())
                        object = line2[1].strip()
                        cur.execute(f"""INSERT into naifids values
                                      ({id}, '{object}')""")
