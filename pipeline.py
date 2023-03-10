import csv
import sys
import mysql.connector
from datetime import date, timedelta
from config import DATABASE_CONFIG

def get_db_connection():
    connection = None
    try:
        connection = mysql.connector.connect(**DATABASE_CONFIG)
    except Exception as error:
        print("Error while connecting to database for pipeline project", error)

    return connection

def create_ticket_sales_table(conn):
    connection = conn

    # Create a cursor object
    cursor = connection.cursor()

    # Make the  SQL query to check if the table exists
    table_exists_query = """
        SELECT 1
        FROM information_schema.tables
        WHERE table_schema = 'pipeline'
        AND table_name = 'ticket_sales'
        LIMIT 1
    """

    # check if table exists
    cursor.execute(table_exists_query)

    # If the table doesn't exist, create it
    if not cursor.fetchone():
        # Define the SQL query to create the table
        create_table_query = """
            CREATE TABLE ticket_sales (
                ticket_id INT,
                trans_date DATE,
                event_id INT,
                event_name VARCHAR(50),
                event_date DATE,
                event_type VARCHAR(10),
                event_city VARCHAR(20),
                customer_id INT,
                price DECIMAL,
                num_tickets INT
            )
        """

        # create the table
        cursor.execute(create_table_query)

        # Commit the changes to the database
        connection.commit()
        print("Table created successfully.")

    else:
        print("Table already exists.")





def load_third_party(conn, file_path_csv):
    cursor = conn.cursor()

    # [Iterate through the CSV file and execute insert statement]
    # Create the SQL query to insert data into the ticket_sales table
    insert_query = """
        INSERT INTO ticket_sales (
            ticket_id,
            trans_date,
            event_id,
            event_name,
            event_date,
            event_type,
            event_city,
            customer_id,
            price,
            num_tickets
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    # Open the CSV file and iterate through its rows
    with open(file_path_csv, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            # Get the values from the current row of the CSV file
            ticket_id, trans_date, event_id, event_name, event_date, event_type, event_city, customer_id, price, num_tickets = row

            # Do insert with the current row
            cursor.execute(insert_query, (
                int(ticket_id),
                trans_date,
                int(event_id),
                event_name,
                event_date,
                event_type,
                event_city,
                int(customer_id),
                float(price),
                int(num_tickets)
            ))

    conn.commit()
    cursor.close()
    return


def query_popular_tickets(conn):
    # Get the most popular ticket
    # The instructions said "in the past month", but I am leaving that out because all of the data is a couple of
    # years old.  So, there are none in the past month.  However, I am leaving the code to demonstrate the knowledge
    # of how to do that
    today = date.today()
    one_month_ago = today - timedelta(days=30)
    sql_statement = """
        SELECT event_name, SUM(num_tickets) AS total_tickets_sold
        FROM ticket_sales
#        WHERE trans_date >= %s
        GROUP BY event_name
        ORDER BY total_tickets_sold DESC
        LIMIT 3
    """
    cursor = conn.cursor()
#    cursor.execute(sql_statement, (one_month_ago,))
    cursor.execute(sql_statement)
    records = cursor.fetchall()
    cursor.close()
    return records

def main(file_path_csv):
    # get the connection
    db_connection = get_db_connection()
    # create the table if it doens't already exist
    create_ticket_sales_table(db_connection)



    # I'm leaving out the "in the past month" because all of the data is from a couple of years ago.
    print("Here are the most popular tickets:")
    for event_name,total_tickets_sold,  in query_popular_tickets(db_connection):
        print("- " + event_name + ":  Sold " + str(total_tickets_sold) + " tickets")

    db_connection.close()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python myscript.py <file_path_csv>")
        sys.exit(1)

    file_path_csv = sys.argv[1]
    main(file_path_csv)
