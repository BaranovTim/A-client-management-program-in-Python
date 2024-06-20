import psycopg2


def delete_table(cursor):
    cursor.execute("""
        DROP TABLE IF EXISTS phone;
        DROP TABLE IF EXISTS client;
    """)
#A function that creates a database structure (tables).
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

#A function that allows you to add a new client.
def add_client(cursor, client_name, client_surname, client_email):
    cursor.execute("""
        
        INSERT INTO client(client_name, client_surname, client_email ) 
        VALUES (%s, %s, %s) 
        RETURNING client_id
        
    """, (client_name, client_surname, client_email,))
    client_id = cursor.fetchone()[0]
    return client_id

#A feature that allows you to add a phone for an existing customer.
def add_phone(cursor, client_id, phone):
    cursor.execute("""
        INSERT INTO phone (client_id, client_phone) VALUES (%s, %s)
        RETURNING phone_id;
    """, (client_id, phone))
    phone_id = cursor.fetchone()[0]
    return phone_id

#A function that allows you to change customer data.
def update_client(cursor, client_id):
    question_1 = input("Select from the list and write the exact name that you want to change in your data : client_name , client_surname , client_email, client_phone ")
    question_2 = input("Write the data you need: ")

    if question_1 in ['client_name', 'client_surname', 'client_email']:
        cursor.execute(f"""
            UPDATE client SET {question_1} = %s WHERE client_id = %s;
        """, (question_2, client_id))
        return f"{question_1} has been succesfully updated"

    elif question_1 == 'client_phone':
        cursor.execute("""
            UPDATE phone SET client_phone = %s WHERE client_id = %s;
        """, (question_2, client_id))
        return "Client's phone number has been succesfully updated"

    else:
        return"Incorrect input!"

#A feature that allows you to delete a phone for an existing customer.
def delete_phone(cursor, client_id, phone_id):
    cursor.execute("""

    DELETE FROM phone 
    WHERE phone_id = %s and client_id = %s
                    
    """, (phone_id, client_id,))
    return "Client's phone number has been succesfully deleted"

#A function that allows you to delete an existing client. 
def delete_client(cursor,client_id):
    cursor.execute("""

    DELETE FROM client 
    WHERE client_id = %s
                    
    """, (client_id,))
    return "Client has been succesfully deleted"

#A function that allows you to find a client by his data: first name, last name, email or phone number.
def find_client(cursor):

    question1 = input("Select from the list and write the exact name that you know in your data in your data (one thing) : client_name , client_surname , client_email, client_phone ")
    question2 = input("Write down the data that you know:   ")
    
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
         print("Incorrect input!")
         return None


    client_data = cursor.fetchall()
    return f"Your info: {client_data}"
        

with psycopg2.connect(database="First_psycopg2", user="postgres", password="Tim597707") as conn:
    with conn.cursor() as cur:        
        
        delete_table(cur)
        tables(cur)

        # Adds new client and phone
        client_id = add_client(cur, 'John', 'Doe', 'john.doe@example.com')
        phone_id = add_phone(cur, client_id, '123-456-7890')
        
        # Update client's data
        update_client(cur, client_id)
        
        # Find a client
        clients = find_client(cur)
        print(clients)
        
        # delete phone and a client
        delete_phone(cur, client_id, phone_id)
        delete_client(cur, client_id)

        conn.commit()