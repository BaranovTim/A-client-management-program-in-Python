import psycopg2


def delete_table(cursor):
    cursor.execute("""
        DROP TABLE IF EXISTS phone;
        DROP TABLE IF EXISTS client;
    """)

def tables(cursor):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS client(
            client_id SERIAL PRIMARY KEY,
            client_name varchar(40),
            client_surname varchar(40),
            client_email varchar(40) UNIQUE
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS phone(
            phone_id SERIAL PRIMARY KEY,
            client_id INTEGER REFERENCES client(client_id) ON DELETE CASCADE,
            client_phone varchar(20) 
        );
    """)

def add_phone(cursor, client_id, phone):
    cursor.execute("""
        INSERT INTO phone (client_id, client_phone) VALUES (%s, %s)
        RETURNING phone_id;
    """, (client_id, phone))
    phone_id = cursor.fetchone()[0]
    return phone_id

def add_client(cursor, client_name, client_surname, client_email):
    cursor.execute("""
        
        INSERT INTO client(client_name, client_surname, client_email ) 
        VALUES (%s, %s, %s) 
        RETURNING client_id
        
    """, (client_name, client_surname, client_email,))
    client_id = cursor.fetchone()[0]
    return client_id

def update_client(cursor, client_id):
    question = input("Выберите из списка и напишите точное название что вы хотите поменять в своих данных : client_name , client_surname , client_email, client_phone ")
    question_2 = input("Напишите нужные вам данные: ")

    if question in ['client_name', 'client_surname', 'client_email']:
        cursor.execute(f"""
            UPDATE client SET {question} = %s WHERE client_id = %s;
        """, (question_2, client_id))

    elif question == 'client_phone':
        cursor.execute("""
            UPDATE phone SET client_phone = %s WHERE client_id = %s;
        """, (question_2, client_id))

    else:
        print("Некорректное название столбца")

def delete_phone(cursor,client_id, phone_id):
    cur.execute("""

    DELETE FROM phone 
    WHERE phone_id = %s and client_id = %s
                    
    """, (phone_id, client_id,))
    pass
 
def delete_client(cursor,client_id):
    cur.execute("""

    DELETE FROM client 
    WHERE client_id = %s
                    
    """, (client_id,))
    pass
        
        #Лучше бы тут наверное сделать через цикл for чтобы если бы было известно несколько своих данных было бы более точнее определить пользователя,
        # но в задании просят "или" и у меня есть еще недоделанные работы. 
def find_client(cursor):

    question1 = input("Выберите из списка и напишите точное название что вам известно в своих данных в своих данных (что то одно) : client_name , client_surname , client_email, client_phone ")
    question2 = input("Напишите информацию которая вам известна:   ")
    
    if question1 in ["client_name" , "client_surname" , "client_email"]:

            cursor.execute(f"""
                SELECT * FROM client WHERE {question1}= %s;
                """,(question2,))
    elif question1 == "client_phone" :
            cursor.execute("""
                SELECT c.* FROM client c 
                JOIN phone p ON c.client_id = p.client_id        
                WHERE p.client_phone = %s;
                """,(question2,))
    else:
         print("Неверно назван столбец")
         return None


    client_data = cursor.fetchall()
    return client_data
        

with psycopg2.connect(database="First_psycopg2", user="postgres", password="Tim597707") as conn:
    with conn.cursor() as cur:        
        
        delete_table(cur)
        tables(cur)

        # Добавление нового клиента и телефона
        client_id = add_client(cur, 'John', 'Doe', 'john.doe@example.com')
        phone_id = add_phone(cur, client_id, '123-456-7890')
        
        # Обновление данных клиента
        update_client(cur, client_id)
        
        # Поиск клиента
        clients = find_client(cur)
        print(clients)
        
        # Удаление телефона и клиента
        delete_phone(cur, client_id, phone_id)
        delete_client(cur, client_id)

        conn.commit()