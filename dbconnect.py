import os
import sys
import queue
import psycopg2
import random
import copy
import html


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

def escape_special_characters(string):
    return string.replace('_', '\\_').replace('%', '\\%')

    
# gets the set of flashcards corresponding to a given courseid
# and lessonid. Returns a boolean value indicating whether the query
# was successful and a list of flashcard dicts corresponding to each flashcard.
# These values are stored in a list
def get_flashcards(username, courseid, lessonid):
    connection = _get_connection()
    
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1 FROM pg_prepared_statements WHERE name = 'select_flashcards'")
            exists = cursor.fetchone()

            if exists:
                # Deallocate the existing prepared statement
                cursor.execute("DEALLOCATE select_flashcards")

            # Prepare the new statement
            cursor.execute("PREPARE select_flashcards (INT, INT) AS "
                        "SELECT cardid, videolink, translation, memorytip, speech, sentence, courseid, lessonid "
                        "FROM flashcards WHERE courseid = $1 AND lessonid = $2")
            
            # Execute the prepared statement
            cursor.execute("EXECUTE select_flashcards (%s, %s)", [courseid, lessonid])
            table = cursor.fetchall()

            starred_flashcards = get_starred_cards(username)

            return_list = []
            return_list.append(True)
            
            flashcard_list = []
            for row in table:
                
                flashcard = {"cardid": row[0], "videolink": row[1], "translation": row[2],
             "memorytip": row[3], "speech": row[4], "sentence": row[5], "courseid": row[6],
                            "lessonid": row[7]}
                flashcard["starred-class"] = "active"
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
        connection.rollback()
        print(sys.argv[0] + ":", ex, file=sys.stderr)

    finally:
        _put_connection(connection)
    
    return return_list
    
def get_terms(searchterm):
    connection = _get_connection()


    try: 
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1 FROM pg_prepared_statements WHERE name = 'select_flashcards_by_translation'")
            exists = cursor.fetchone()

            if exists:
                # Deallocate the existing prepared statement
                cursor.execute("DEALLOCATE select_flashcards_by_translation")

            # Prepare the new statement
            cursor.execute("PREPARE select_flashcards_by_translation (TEXT) AS "
                        "SELECT videolink, translation, memorytip, speech, sentence "
                        "FROM flashcards WHERE translation ILIKE $1")
            
            # Execute the prepared statement
            cursor.execute("EXECUTE select_flashcards_by_translation (%s)", [f"%{escape_special_characters(searchterm)}%"])
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
            connection.rollback()
            print(sys.argv[0] + ":", ex, file=sys.stderr)

    finally:
            _put_connection(connection)
    
    return return_list

def get_lessonterms(searchterm, lesson, course):
    connection = _get_connection()


    try: 
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1 FROM pg_prepared_statements WHERE name = 'select_flashcards_by_translation_and_lesson_course'")
            exists = cursor.fetchone()

            if exists:
                # Deallocate the existing prepared statement
                cursor.execute("DEALLOCATE select_flashcards_by_translation_and_lesson_course")

            # Prepare the new statement
            cursor.execute("PREPARE select_flashcards_by_translation_and_lesson_course (TEXT, INT, INT) AS "
                        "SELECT videolink, translation, memorytip, speech, sentence, cardid "
                        "FROM flashcards WHERE translation ILIKE $1 AND lessonid = $2 AND courseid = $3")
            
            # Execute the prepared statement
            cursor.execute("EXECUTE select_flashcards_by_translation_and_lesson_course (%s, %s, %s)", (f"%{escape_special_characters(searchterm)}%", lesson, course))
            table = cursor.fetchall()

            return_list = []
            return_list.append(True)
            
            flashcard_list = []
            for row in table:
                flashcard = {"videolink": row[0], "translation": row[1],
                             "memorytip": row[2], "speech": row[3], "sentence": row[4], "cardid": row[5] }
                flashcard_list.append(flashcard)
            return_list.append(flashcard_list)

    except Exception as ex:
            return_list = []
            return_list.append(False)
            return_list.append("A server error occurred. Please contact the system administrator.")
            connection.rollback()
            print(sys.argv[0] + ":", ex, file=sys.stderr)

    finally:
            _put_connection(connection)
    
    return return_list

def get_user(netid):
    connection = _get_connection()


    try: 
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1 FROM pg_prepared_statements WHERE name = 'select_student_user_by_netid'")
            exists = cursor.fetchone()

            if exists:
                # Deallocate the existing prepared statement
                cursor.execute("DEALLOCATE select_student_user_by_netid")

            # Prepare the new statement
            cursor.execute("PREPARE select_student_user_by_netid (TEXT) AS "
                        "SELECT netid, firstname, lastname "
                        "FROM studentusers WHERE netid = $1")
            
            # Execute the prepared statement
            cursor.execute("EXECUTE select_student_user_by_netid (%s)", [escape_special_characters(netid)])
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
            connection.rollback()
            print(sys.argv[0] + ":", ex, file=sys.stderr)

    finally:
            _put_connection(connection)
    
    return return_list

def add_user(username, firstname, lastname):
    connection = _get_connection()

    try: 
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1 FROM pg_prepared_statements WHERE name = 'insert_student_user'")
            exists = cursor.fetchone()

            if exists:
                # Deallocate the existing prepared statement
                cursor.execute("DEALLOCATE insert_student_user")

            # Prepare the new statement
            cursor.execute("PREPARE insert_student_user (TEXT, TEXT, TEXT) AS "
                        "INSERT INTO studentusers (netid, firstname, lastname) VALUES ($1, $2, $3)")
            
            # Execute the prepared statement
            cursor.execute("EXECUTE insert_student_user (%s, %s, %s)", (username, firstname, lastname))
            connection.commit()
            
            return True, "User added successfully."

    except Exception as ex:
        error_message = "A server error occurred. Please contact the system administrator."
        print(sys.argv[0] + ":", ex, file=sys.stderr)
        connection.rollback()
        return False, error_message

    finally:
        _put_connection(connection)
        
def get_admin(netid):
    connection = _get_connection()


    try: 
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1 FROM pg_prepared_statements WHERE name = 'select_admin_by_adminid'")
            exists = cursor.fetchone()

            if exists:
                # Deallocate the existing prepared statement
                cursor.execute("DEALLOCATE select_admin_by_adminid")

            # Prepare the new statement
            cursor.execute("PREPARE select_admin_by_adminid (TEXT) AS "
                        "SELECT adminid, firstname, lastname "
                        "FROM admin WHERE adminid = $1")
            
            # Execute the prepared statement
            cursor.execute("EXECUTE select_admin_by_adminid (%s)", [escape_special_characters(netid)])
            table = cursor.fetchall()
            
            return_list = []
            return_list.append(True)
         
            if table == []: 
                 return_list.append(False)
                 return_list.append("You do not have access to administrative features.")
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
            connection.rollback()
            print(sys.argv[0] + ":", ex, file=sys.stderr)

    finally:
            _put_connection(connection)
    
    return return_list

 
def get_starred_cards(netid):
    connection = _get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1 FROM pg_prepared_statements WHERE name = 'select_starred_flashcards_by_netid'")
            exists = cursor.fetchone()

            if exists:
                # Deallocate the existing prepared statement
                cursor.execute("DEALLOCATE select_starred_flashcards_by_netid")

            # Prepare the new statement
            cursor.execute("PREPARE select_starred_flashcards_by_netid (TEXT) AS "
                        "SELECT flashcards.cardid, videolink, translation, memorytip, speech, sentence, flashcards.courseid, flashcards.lessonid "
                        "FROM flashcards, starredflashcards "
                        "WHERE netid = $1 AND starredflashcards.cardid = flashcards.cardid")
            
            # Execute the prepared statement
            cursor.execute("EXECUTE select_starred_flashcards_by_netid (%s)", [escape_special_characters(netid)])
            table = cursor.fetchall()

            return_list = []
            return_list.append(True)
            
            flashcard_list = []
            for row in table:
                flashcard = {"cardid": row[0], "videolink": row[1], "translation": row[2],
                             "memorytip": row[3], "speech": row[4], "sentence": row[5], "courseid": row[6],
                            "lessonid": row[7]}
                flashcard["starred-class"] = "active"
                flashcard_list.append(flashcard)
            return_list.append(flashcard_list)
    
    except Exception as ex:
        return_list = []
        return_list.append(False)
        return_list.append("A server error occurred. Please contact the system administrator.")
        connection.rollback()
        print(sys.argv[0] + ":", ex, file=sys.stderr)

    finally:
        _put_connection(connection)
    
    return return_list

def add_starred_card(netid, cardid, courseid, lessonid):
    connection = _get_connection()

    try: 
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1 FROM pg_prepared_statements WHERE name = 'insert_starred_flashcard'")
            exists = cursor.fetchone()

            if exists:
                # Deallocate the existing prepared statement
                cursor.execute("DEALLOCATE insert_starred_flashcard")

            # Prepare the new statement
            cursor.execute("PREPARE insert_starred_flashcard (TEXT, INT, INT, INT) AS "
                        "INSERT INTO starredflashcards (netid, cardid, courseid, lessonid) VALUES ($1, $2, $3, $4)")
            
            # Execute the prepared statement
            cursor.execute("EXECUTE insert_starred_flashcard (%s, %s, %s, %s)", [netid, cardid, courseid, lessonid])
            connection.commit()
            
            return True, "Flashcard starred"

    except Exception as ex:
        error_message = "A server error occurred. Please contact the system administrator."
        print(sys.argv[0] + ":", ex, file=sys.stderr)
        connection.rollback()
        return False, error_message

    finally:
        _put_connection(connection)
         
     


def del_starred_card(netid, cardid):
    connection = _get_connection()

    try: 
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1 FROM pg_prepared_statements WHERE name = 'delete_starred_flashcard_by_netid_and_cardid'")
            exists = cursor.fetchone()

            if exists:
                # Deallocate the existing prepared statement
                cursor.execute("DEALLOCATE delete_starred_flashcard_by_netid_and_cardid")

            # Prepare the new statement
            cursor.execute("PREPARE delete_starred_flashcard_by_netid_and_cardid (TEXT, INT) AS "
                        "DELETE FROM starredflashcards WHERE netid = $1 AND cardid = $2")
            
            # Execute the prepared statement
            cursor.execute("EXECUTE delete_starred_flashcard_by_netid_and_cardid (%s, %s)", [escape_special_characters(netid), escape_special_characters(cardid)])
            connection.commit()
            
            return True, "Flashcard unstarred"

    except Exception as ex:
        error_message = "A server error occurred. Please contact the system administrator."
        print(sys.argv[0] + ":", ex, file=sys.stderr)
        connection.rollback()
        return False, error_message

    finally:
        _put_connection(connection)

def add_card(courseid, lessonid, videolink, translation, memorytip, speech, sentence):
    connection = _get_connection()

    try: 
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1 FROM pg_prepared_statements WHERE name = 'insert_flashcard'")
            exists = cursor.fetchone()

            if exists:
                # Deallocate the existing prepared statement
                cursor.execute("DEALLOCATE insert_flashcard")

            # Prepare the new statement
            cursor.execute("PREPARE insert_flashcard (INT, INT, TEXT, TEXT, TEXT, TEXT, TEXT) AS "
                        "INSERT INTO flashcards (courseid, lessonid, videolink, translation, memorytip, speech, sentence) "
                        "VALUES ($1, $2, $3, $4, $5, $6, $7)")

            # Sanitize and format the videolink properly
            videolink_url = 'https://www.youtube.com/embed/' + html.escape(videolink) + '?controls=0&showinfo=0&rel=0&loop=1&mute=1'

            # Execute the prepared statement
            cursor.execute("EXECUTE insert_flashcard (%s, %s, %s, %s, %s, %s, %s)",
                        (courseid, lessonid, videolink_url, translation, memorytip, speech, sentence))
            connection.commit()
            
            return True, "Flashcard added successfully."

    except Exception as ex:
        error_message = "A server error occurred. Please contact the system administrator."
        print(sys.argv[0] + ":", ex, file=sys.stderr)
        connection.rollback()
        return False, error_message

    finally:
        _put_connection(connection)
        

def get_lessonlength(course):
    connection = _get_connection()


    try: 
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1 FROM pg_prepared_statements WHERE name = 'select_lessonid_by_courseid'")
            exists = cursor.fetchone()

            if exists:
                # Deallocate the existing prepared statement
                cursor.execute("DEALLOCATE select_lessonid_by_courseid")

            # Prepare the new statement
            cursor.execute("PREPARE select_lessonid_by_courseid (INT) AS "
                        "SELECT lessonid FROM classes WHERE courseid = $1")
            
            # Execute the prepared statement
            cursor.execute("EXECUTE select_lessonid_by_courseid (%s)", [course])
            table = cursor.fetchall()

            return_list = []
            return_list.append(True)
            
            lesson_list = []
            for row in table:
                
                flashcard = {"lessonid": row[0]}

                lesson_list.append(flashcard)

           
            return_list.append(lesson_list)

    except Exception as ex:
            return_list = []
            return_list.append(False)
            return_list.append("A server error occurred. Please contact the system administrator.")
            connection.rollback()
            print(sys.argv[0] + ":", ex, file=sys.stderr)

    finally:
            _put_connection(connection)
    
    return return_list

def contains_flashcard(cardid):
    connection = _get_connection()


    try: 
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1 FROM pg_prepared_statements WHERE name = 'select_flashcard'")
            exists = cursor.fetchone()

            if exists:
                # Deallocate the existing prepared statement
                cursor.execute("DEALLOCATE select_flashcard")

            # Prepare the new statement
            cursor.execute("PREPARE select_flashcard (INT) AS "
                        "SELECT cardid FROM flashcards WHERE cardid = $1")
            
            # Execute the prepared statement
            cursor.execute("EXECUTE select_flashcard (%s)", [cardid])
            table = cursor.fetchall()

            return_list = []
            return_list.append(True)
            
            lesson_list = []
            for row in table:
                
                flashcard = {"lessonid": row[0]}

                lesson_list.append(flashcard)

           
            return_list.append(lesson_list)

    except Exception as ex:
            return_list = []
            return_list.append(False)
            return_list.append("A server error occurred. Please contact the system administrator.")
            connection.rollback()
            print(sys.argv[0] + ":", ex, file=sys.stderr)

    finally:
            _put_connection(connection)
    
    return return_list

def add_lesson(course, lesson):
    connection = _get_connection()


    try: 
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1 FROM pg_prepared_statements WHERE name = 'insert_class'")
            exists = cursor.fetchone()

            if exists:
                # Deallocate the existing prepared statement
                cursor.execute("DEALLOCATE insert_class")

            # Prepare the new statement
            cursor.execute("PREPARE insert_class (INT, INT) AS "
                        "INSERT INTO classes (courseid, lessonid) VALUES ($1, $2)")
            
            # Execute the prepared statement
            cursor.execute("EXECUTE insert_class (%s, %s)", [course, lesson])
            connection.commit()
            
            return True, "Lesson added successfully."

    except Exception as ex:
            return_list = []
            return_list.append(False)
            return_list.append("A server error occurred. Please contact the system administrator.")
            connection.rollback()
            print(sys.argv[0] + ":", ex, file=sys.stderr)

    finally:
            _put_connection(connection)
    
    return return_list

def update_flashcard(card_id, translation, memorytip, speech, sentence):
    connection = _get_connection()

    try: 
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1 FROM pg_prepared_statements WHERE name = 'update_flashcards'")
            exists = cursor.fetchone()

            if exists:
                # Deallocate the existing prepared statement
                cursor.execute("DEALLOCATE update_flashcards")

            # Prepare the new statement
            cursor.execute("PREPARE update_flashcards (TEXT, TEXT, TEXT, INT) AS "
                        "UPDATE flashcards SET memorytip = $1, speech = $2, sentence = $3 WHERE cardid = $4")
            
            # Execute the prepared statement
            cursor.execute("EXECUTE update_flashcards (%s, %s, %s, %s)", ( memorytip, speech, sentence, card_id))
            connection.commit()

            return True, "Flashcard updated successfully."

    except Exception as ex:
        error_message = "A server error occurred. Please contact the system administrator."
        print(sys.argv[0] + ":", ex, file=sys.stderr)
        connection.rollback()
        return False, error_message

    finally:
        _put_connection(connection)

        
def delete_flashcard(card_id):
    connection = _get_connection()

    try:
        with connection.cursor() as cursor:
            # Prepare the statement to delete flashcards
            cursor.execute("PREPARE delete_flashcards_by_cardid (INT) AS "
                           "DELETE FROM flashcards WHERE cardid = $1")
            # Execute the prepared statement to delete flashcards
            cursor.execute("EXECUTE delete_flashcards_by_cardid (%s)", (card_id,))
            # Deallocate the prepared statement
            cursor.execute("DEALLOCATE delete_flashcards_by_cardid")

            # Prepare the statement to delete class data associated with the lesson
            cursor.execute("PREPARE delete_classes_by_cardid (INT) AS "
                           "DELETE FROM starredflashcards WHERE cardid = $1")
            # Execute the prepared statement to delete class data
            cursor.execute("EXECUTE delete_classes_by_cardid (%s)", (card_id,))
            # Deallocate the prepared statement
            cursor.execute("DEALLOCATE delete_classes_by_cardid")

            connection.commit()
            return True, "Flashcard deleted successfully."

    except Exception as ex:
        error_message = "A server error occurred. Please contact the system administrator."
        print(sys.argv[0] + ":", ex, file=sys.stderr)
        connection.rollback()
        return False, error_message

    finally:
        _put_connection(connection)
        
def delete_lesson(lesson_id, course_id):
    connection = _get_connection()

    try:
        with connection.cursor() as cursor:
            # Prepare the statement to delete flashcards associated with the lesson
            cursor.execute("PREPARE delete_flashcards_by_lessonid (INT, INT) AS "
                           "DELETE FROM flashcards WHERE lessonid = $1 AND courseid = $2")
            # Execute the prepared statement to delete flashcards
            cursor.execute("EXECUTE delete_flashcards_by_lessonid (%s, %s)", (lesson_id, course_id))
            # Deallocate the prepared statement
            cursor.execute("DEALLOCATE delete_flashcards_by_lessonid")

            # Prepare the statement to delete class data associated with the lesson
            cursor.execute("PREPARE delete_classes_by_lessonid (INT, INT) AS "
                           "DELETE FROM classes WHERE lessonid = $1 AND courseid = $2")
            # Execute the prepared statement to delete class data
            cursor.execute("EXECUTE delete_classes_by_lessonid (%s, %s)", (lesson_id, course_id))
            # Deallocate the prepared statement
            cursor.execute("DEALLOCATE delete_classes_by_lessonid")
            
            cursor.execute("PREPARE delete_classes_by_lessonid (INT, INT) AS "
                           "DELETE FROM starredflashcards WHERE lessonid = $1 AND courseid = $2")
            # Execute the prepared statement to delete class data
            cursor.execute("EXECUTE delete_classes_by_lessonid (%s, %s)", (lesson_id, course_id))
            # Deallocate the prepared statement
            cursor.execute("DEALLOCATE delete_classes_by_lessonid")

            connection.commit()
            return True, "Lesson deleted successfully."

    except Exception as ex:
        error_message = "A server error occurred. Please contact the system administrator."
        print(sys.argv[0] + ":", ex, file=sys.stderr)
        connection.rollback()
        return False, error_message

    finally:
        _put_connection(connection)



def get_quiz_questions(courseid, lessonid):
    connection = _get_connection()
    
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1 FROM pg_prepared_statements WHERE name = 'select_flashcards_by_courseid_and_lessonid'")
            exists = cursor.fetchone()

            if exists:
                # Deallocate the existing prepared statement
                cursor.execute("DEALLOCATE select_flashcards_by_courseid_and_lessonid")

            # Prepare the new statement
            cursor.execute("PREPARE select_flashcards_by_courseid_and_lessonid (INT, INT) AS "
                        "SELECT cardid, videolink, translation, memorytip, speech, sentence "
                        "FROM flashcards WHERE courseid = $1 AND lessonid = $2")
            
            # Execute the prepared statement
            cursor.execute("EXECUTE select_flashcards_by_courseid_and_lessonid (%s, %s)", [escape_special_characters(courseid), escape_special_characters(lessonid)])
            table = cursor.fetchall()


            return_list = []

            if (len(table) < 4):
                return_list.append(False)
                return_list.append("This lesson does not have enough vocab words to support the quiz feature. Please contact the course administrator")
                return return_list        

            return_list.append(True)
            
            flashcard_list = []

            check_unique_translations = {}
            translations_list = []
          
            for row in table:
                
                if row[2] not in check_unique_translations:
                    check_unique_translations[row[2]] = None
                    translations_list.append(row[2])
            
            
           
                flashcard = {"cardid": row[0], "videolink": row[1], "translation": row[2],
                             "memorytip": row[3], "speech": row[4], "sentence": row[5]}
    
                
                flashcard_list.append(flashcard)

            

            for flashcard in flashcard_list:
                 options = []

                 # start random process, set correct option
     
                 allowed_values = copy.deepcopy(translations_list)
                 allowed_values.remove(flashcard["translation"])
                 options.append([flashcard["translation"], "correct"])
                

                 # set second option
            
                 temp = random.choice(allowed_values)
                 allowed_values.remove(temp)
                 options.append([temp, "incorrect"])
              


                  # set third option
                 temp = random.choice(allowed_values)
                 allowed_values.remove(temp)
                 options.append([temp, "incorrect"])
            
                 # set fourth option
                 temp = random.choice(allowed_values)
                 allowed_values.remove(temp)
                 options.append([temp, "incorrect"])
             

                 random.shuffle(options)

                 flashcard["options"] = options

            random.shuffle(flashcard_list)

            return_list.append(flashcard_list)
    
    except Exception as ex:
        
        return_list = []
        return_list.append(False)
        return_list.append("A server error occurred. Please contact the system administrator.")
        connection.rollback()
        print(sys.argv[0] + ":", ex, file=sys.stderr)

    finally:
        _put_connection(connection)
    
    return return_list
     















