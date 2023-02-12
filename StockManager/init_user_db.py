import sqlite3


if __name__ == '__main__':

    conn = sqlite3.connect('user.db')

    c = conn.cursor()


    # c.execute("""CREATE TABLE user (
    #             USERNAME text,
    #             PASSWORD text
    #             ) """)

    c.execute("""INSERT INTO user (
                    USERNAME,
                    PASSWORD
                    ) 
                    VALUES 
                    ("ADMIN", "1234"),
                    ("READONLY", "9876")""")

    conn.commit()
