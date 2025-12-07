import psycopg2

connection = psycopg2.connect(database="dbname", user="username", password="pass", host="hostname", port=5432)
cursor = connection.cursor()
cursor.execute("SELECT * from portal.portal_users;")