import psycopg
from psycopg import sql
from configparser import ConfigParser

class DatabaseSetup:
    def config(self, filename='database.ini', section='postgresql'):
        # create a parser
        parser = ConfigParser()

        # read config file
        parser.read(filename)

        # get section, default to postgresql
        db = {}
        if parser.has_section(section):
            params = parser.items(section)
            for param in params:
                db[param[0]] = param[1]
        else:
            raise Exception('Section {0} not found in the {1} file'.format(section, filename))

        return db

    def connect(self):
        """ Connect to the PostgreSQL database server """
        conn = None
        try:
            # read connection parameters
            params = self.config()

            # connect to the PostgreSQL server
            print('Connecting to the PostgreSQL database...')
            conn = psycopg.connect(**params)
            
            # create a cursor
            cur = conn.cursor()
            
            #Look through tables in database to see if there is already a table created for this client
            SQL = "SELECT tablename FROM pg_catalog.pg_tables WHERE tablename = (%s)"
            SQLdata = ('banana', )
            cur.execute(SQL, SQLdata)
            tableinfo = cur.fetchone()
            dbName = 'players'
    
            #If a database isn't created in Supabase then create one. If it is, then don't worry about creating one.
            if tableinfo is None:
                print("Table for client doesnt exist. Creating now.")
                cur.execute(sql.SQL("CREATE TABLE {} ();").format(sql.Identifier(dbName)))
                cur.execute(sql.SQL("ALTER TABLE {} ADD COLUMN \"id\" int8 PRIMARY KEY;").format(sql.Identifier(dbName)))
                cur.execute(sql.SQL("ALTER TABLE {} ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY;").format(sql.Identifier(dbName)))
                cur.execute(sql.SQL("ALTER TABLE {} ADD COLUMN \"playerID\" int8;").format(sql.Identifier(dbName)))
                cur.execute(sql.SQL("ALTER TABLE {} ADD COLUMN \"playerName\" text;").format(sql.Identifier(dbName)))
                cur.execute(sql.SQL("ALTER TABLE {} ADD COLUMN \"playerStatus\" text;").format(sql.Identifier(dbName)))
                cur.execute(sql.SQL("ALTER TABLE {} ADD COLUMN \"playerAlliance\" int8;").format(sql.Identifier(dbName)))
                cur.execute(sql.SQL("ALTER TABLE {} ADD COLUMN \"fetchDate\" timestamptz;").format(sql.Identifier(dbName)))
                conn.commit()

            else:
                print("Table for client exists in database. Beginning XML parser.")

            # close the communication with the PostgreSQL
            cur.close()

        except (Exception, psycopg.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()
                print('Database connection closed.')
