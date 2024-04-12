import os
import contextlib
import sys
import queue
import psycopg2


#-----------------------------------------------------------------------
# URL for database file
_DATABASE_URL = os.environ['DATABASE_URL']

_connection_pool = queue.Queue()


def _get_connection():
    try:
        conn = _connection_pool.get(block=False) 
    except queue.Empty:
        conn = psycopg2.connect(_DATABASE_URL)
    return conn

def _put_connection(conn):
    _connection_pool.put(conn)


    
# gets the set of flashcards corresponding to a given courseid
# and lessonid. Returns a boolean value indicating whether the query
# was successful and a list of flashcard dicts corresponding to each flashcard.
# These values are stored in a list
def get_flashcards(username, courseid, lessonid):
    connection = _get_connection()
    
    try:
        with connection.cursor() as cursor:
            query_str = "SELECT cardid, videolink, translation, memorytip, speech, sentence "
            query_str += "FROM flashcards WHERE courseid = %s AND lessonid = %s "
            cursor.execute(query_str, [courseid, lessonid])
            table = cursor.fetchall()

            starred_flashcards = get_starred_cards(username)

            return_list = []
            return_list.append(True)
            
            flashcard_list = []
            for row in table:
                
                flashcard = {"cardid": row[0], "videolink": row[1], "translation": row[2],
                             "memorytip": row[3], "speech": row[4], "sentence": row[5]}
                if (flashcard in starred_flashcards[1]):
                   
                    flashcard["starred-class"] = "active"
                else:
    
                    flashcard["starred-class"] = ""

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
    
def get_terms(searchterm):
    connection = _get_connection()


    try: 
        with connection.cursor() as cursor:
            query_str = "SELECT videolink, translation, memorytip, speech, sentence "
            query_str += "FROM flashcards WHERE translation ILIKE %s "
            cursor.execute(query_str, [f"%{searchterm}%"])
            table = cursor.fetchall()

            return_list = []
            return_list.append(True)
            
            flashcard_list = []
            for row in table:
                flashcard = {"videolink": row[0], "translation": row[1],
                             "memorytip": row[2], "speech": row[3], "sentence": row[4] }
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

def get_user(netid):
    connection = _get_connection()


    try: 
        with connection.cursor() as cursor:
            query_str = "SELECT netid, firstname, lastname "
            query_str += "FROM studentusers WHERE netid = %s"
            cursor.execute(query_str, [netid])
            table = cursor.fetchall()
            
            return_list = []
            return_list.append(True)
         
            if table == []: 
                 return_list.append(False)
            else:
                return_list.append(True)
                row = table[0]
                user = {"netid": row[0], "firstname": row[1],
                             "lastname": row[2] }
                return_list.append(user)


    except Exception as ex:
            return_list = []
            return_list.append(False)
            return_list.append("A server error occurred. Please contact the system administrator.")
            print(sys.argv[0] + ":", ex, file=sys.stderr)

    finally:
            _put_connection(connection)
    
    return return_list

def add_user(username, firstname, lastname):
    connection = _get_connection()

    try: 
        with connection.cursor() as cursor:
            query_str = "INSERT INTO studentusers (netid, firstname, lastname) VALUES (%s, %s, %s)"
            cursor.execute(query_str, (username, firstname, lastname))
            connection.commit()
            
            return True, "User added successfully."

    except Exception as ex:
        error_message = "A server error occurred. Please contact the system administrator."
        print(sys.argv[0] + ":", ex, file=sys.stderr)
        return False, error_message

    finally:
        _put_connection(connection)
        
def get_admin(netid):
    connection = _get_connection()


    try: 
        with connection.cursor() as cursor:
            query_str = "SELECT adminid, firstname, lastname "
            query_str += "FROM admin WHERE adminid = %s"
            cursor.execute(query_str, [netid])
            table = cursor.fetchall()
            
            return_list = []
            return_list.append(True)
         
            if table == []: 
                 return_list.append(False)
            else:
                return_list.append(True)
                row = table[0]
                user = {"adminid": row[0], "firstname": row[1],
                             "lastname": row[2] }
                return_list.append(user)


    except Exception as ex:
            return_list = []
            return_list.append(False)
            return_list.append("A server error occurred. Please contact the system administrator.")
            print(sys.argv[0] + ":", ex, file=sys.stderr)

    finally:
            _put_connection(connection)
    
    return return_list

 
def get_starred_cards(netid):
    connection = _get_connection()

    try:
        with connection.cursor() as cursor:
            query_str = "SELECT flashcards.cardid, videolink, translation, memorytip, speech, sentence "
            query_str += "FROM flashcards, starredflashcards WHERE netid = %s AND starredflashcards.cardid = flashcards.cardid"
            cursor.execute(query_str, [netid])
            table = cursor.fetchall()

            return_list = []
            return_list.append(True)
            
            flashcard_list = []
            for row in table:
                flashcard = {"cardid": row[0], "videolink": row[1], "translation": row[2],
                             "memorytip": row[3], "speech": row[4], "sentence": row[5]}
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

def add_starred_card(netid, cardid):
    connection = _get_connection()

    try: 
        with connection.cursor() as cursor:
            query_str = "INSERT INTO starredflashcards (netid, cardid) VALUES (%s, %s)"
            cursor.execute(query_str, [netid, cardid])
            connection.commit()
            
            return True, "Flashcard starred"

    except Exception as ex:
        error_message = "A server error occurred. Please contact the system administrator."
        print(sys.argv[0] + ":", ex, file=sys.stderr)
        return False, error_message

    finally:
        _put_connection(connection)
         
     


def del_starred_card(netid, cardid):
    connection = _get_connection()

    try: 
        with connection.cursor() as cursor:
            query_str = "DELETE FROM starredflashcards WHERE netid = %s AND cardid = %s"
            cursor.execute(query_str, [netid, cardid])
            connection.commit()
            
            return True, "Flashcard unstarred"

    except Exception as ex:
        error_message = "A server error occurred. Please contact the system administrator."
        print(sys.argv[0] + ":", ex, file=sys.stderr)
        return False, error_message

    finally:
        _put_connection(connection)

def add_card(courseid, lessonid, videolink, translation, memorytip, speech, sentence):
    connection = _get_connection()
    
    print("hi")

    try: 
        with connection.cursor() as cursor:
            query_str = "INSERT INTO flashcards (courseid, lessonid, videolink, translation, memorytip, speech, sentence) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(query_str, (courseid, lessonid, videolink, translation, memorytip, speech, sentence))
            connection.commit()
            
            return True, "Flashcard added successfully."

    except Exception as ex:
        error_message = "A server error occurred. Please contact the system administrator."
        print(sys.argv[0] + ":", ex, file=sys.stderr)
        return False, error_message

    finally:
        _put_connection(connection)


















