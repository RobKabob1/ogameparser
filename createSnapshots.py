import psycopg2
from psycopg2 import sql
from configparser import ConfigParser
from databasesetup import DatabaseSetup

class CreateSnapshots: 
    def startSnapshots(self):
        # Create database connection 
        dbConnection = DatabaseSetup()

        """ Connect to the PostgreSQL database server """
        conn = None
        try:
            # read connection parameters & connect to PostgreSQL server
            params = dbConnection.config()
            print('Connecting to the PostgreSQL database...')
            conn = psycopg2.connect(**params)
            
            # create a cursor
            cur = conn.cursor()
            
            #Copy data from the players table into the playersDaily table
            SQL = "DELETE FROM public.\"playersDaily\""
            cur.execute(SQL)
            conn.commit()

            SQL = "INSERT INTO public.\"playersDaily\" SELECT * FROM players WHERE players.\"fetchDate\" >= CURRENT_DATE"
            cur.execute(SQL)
            conn.commit()

            #Copy data from the alliances table into the alliancesDaily table
            SQL = "DELETE FROM public.\"alliancesDaily\""
            cur.execute(SQL)
            conn.commit()

            SQL = "INSERT INTO public.\"alliancesDaily\" SELECT * FROM alliances WHERE alliances.\"fetchDate\" >= CURRENT_DATE"
            cur.execute(SQL)
            conn.commit()

            #Copy data from the planets table into the planetsWeekly table
            SQL = "DELETE FROM public.\"planetsWeekly\""
            cur.execute(SQL)
            conn.commit()

            SQL = "INSERT INTO public.\"planetsWeekly\" SELECT * FROM planets WHERE planets.\"fetchDate\" >= CURRENT_DATE"
            cur.execute(SQL)
            conn.commit()

            # close the communication with the PostgreSQL
            cur.close()

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()
                print('Database connection closed.')
        