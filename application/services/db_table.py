from application.services.db_connection import DBConnection


# Create_database_table__start
def create_table():
    with DBConnection() as connection:
        with connection:
            connection.execute(
                """
            CREATE TABLE IF NOT EXISTS phones (
            phoneID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            contactName VARCHAR NOT NULL,
            phoneValue INTEGER NOT NULL
            )
            """
            )
