import sqlite3

DB = "slovicka.db"


def vytvor_db():

    conn = sqlite3.connect(DB)

    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS slovicka(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            english TEXT NOT NULL,
            czech TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


def pridej_slovicko(english, czech):

    conn = sqlite3.connect(DB)

    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO slovicka
        (english, czech)
        VALUES (?, ?)
        """,
        (english, czech)
    )

    conn.commit()
    conn.close()


def nacti_slovicka():

    conn = sqlite3.connect(DB)

    cur = conn.cursor()

    cur.execute(
        """
        SELECT id, english, czech
        FROM slovicka
        """
    )

    data = cur.fetchall()

    conn.close()

    return data


def smaz_slovicko(id_slova):

    conn = sqlite3.connect(DB)

    cur = conn.cursor()

    cur.execute(
        """
        DELETE FROM slovicka
        WHERE id = ?
        """,
        (id_slova,)
    )

    conn.commit()
    conn.close()


def uprav_slovicko(
    id_slova,
    english,
    czech
):

    conn = sqlite3.connect(DB)

    cur = conn.cursor()

    cur.execute(
        """
        UPDATE slovicka
        SET english=?,
            czech=?
        WHERE id=?
        """,
        (
            english,
            czech,
            id_slova
        )
    )

    conn.commit()
    conn.close()