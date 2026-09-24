import sqlite3

DB = "viral_saves.db"


def setup():
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS videos (
        id INTEGER PRIMARY KEY,
        title TEXT,
        url TEXT UNIQUE
    )
    """)
    conn.commit()
    conn.close()


def save_video(video):
    setup()
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute(
        "INSERT OR IGNORE INTO videos(title,url) VALUES(?,?)",
        (video.get("title"), video.get("url"))
    )
    conn.commit()
    conn.close()


def get_saved_videos():
    setup()
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute("SELECT title,url FROM videos ORDER BY id DESC")
    rows = cur.fetchall()
    conn.close()

    return [{"title": r[0], "url": r[1]} for r in rows]
