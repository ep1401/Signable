import os
import contextlib
import sys
import queue
import psycopg2


#-----------------------------------------------------------------------
# URL for database file
_DATABASE_URL = os.environ['DATABASE_URL']

_connection_pool = queue.Queue()

# gets the set of flashcards corresponding to a given courseid
# and lessonid. Returns a boolean value indicating whether the query
# was successful and a list of flashcard dicts corresponding to each flashcard.
# These values are stored in a list
def _get_connection():
    try:
        conn = _connection_pool.get(block=False) 
    except queue.Empty:
        conn = psycopg2.connect(_DATABASE_URL)
    return conn

def _put_connection(conn):
    _connection_pool.put(conn)


    

def get_flashcards(courseid, lessonid):
    connection = _get_connection()
    
    try:
        with connection.cursor() as cursor:
            query_str = "SELECT cardid, videolink, translation, memorytip, speech, sentence "
            query_str += "FROM flashcards WHERE courseid = %d AND lessonid = %d "
            cursor.execute(query_str, [courseid, lessonid])
            table = cursor.fetchall()

            return_list = []
            return_list.append(True)
            
            flashcard_list = []
            for row in table:
                flashcard = {"cardid": row[0], "videolink": row[1], "translation": row[2],
                             "memorytip": row[3], "speech": row[4], "sentence": row[5] }
                flashcard_list.append(flashcard)
            return_list.append(flashcard_list)
    
    except Exception as ex:
        return_list = []
        return_list.append(False)
        return_list.append("A server error occurred. Please contact the system administrator.")
        print(sys.argv[0] + ":", ex, file=sys.stderr)

    finally:
        _put_connection(connection)
    
    return return_list
    
    
    




