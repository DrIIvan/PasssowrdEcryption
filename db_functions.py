import sqlite3


def get_account(sort_key: str, database_name: str):
    connection = sqlite3.connect(f"./data_base/{database_name}.db")
    cursor = connection.cursor()

    if sort_key == "NONE":
        request = """
            SELECT *
            FROM Passwords
            """
        res = cursor.execute(request).fetchall()
    else:
        request = """
        SELECT *
        FROM Passwords
        WHERE Service = ?
        """
        res = cursor.execute(request, (sort_key,)).fetchall()
    connection.close()
    return res


def add_account(service: str, password: bytes, database_name: str):
    connection = sqlite3.connect(f"./data_base/{database_name}.db")
    cursor = connection.cursor()

    request = """
    INSERT INTO Passwords
    VALUES (?, ?)
    """
    cursor.execute(request, (service, password,))

    connection.commit()
    connection.close()


def update_account(service: str, value: bytes, database_name: str):
    connection = sqlite3.connect(f"./data_base/{database_name}.db")
    cursor = connection.cursor()
    request = """
    UPDATE Passwords
    SET Password = ?
    WHERE Service = ?
    """
    cursor.execute(request, (value, service,))

    connection.commit()
    connection.close()


def delete_account(service: str, database_name: str):
    connection = sqlite3.connect(f"./data_base/{database_name}.db")
    cursor = connection.cursor()

    if service == "DELETE_ALL":
        request = """
        DELETE FROM Passwords
        """
        cursor.execute(request)
    else:
        request = """
        DELETE FROM Passwords
        WHERE Service = ?
        """
        cursor.execute(request, (service,))

    connection.commit()
    connection.close()
