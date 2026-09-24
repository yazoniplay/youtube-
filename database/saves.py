import sqlite3

DB = "viral_saves.db"


def setup():
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS videos (
        id INTEGER PRIMARY KEY,
        title TEXT,
        url TEXT UNIQUE,
        result TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    conn.commit()
    conn.close()


def save_video(video, result=""):
    setup()
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute(
        "INSERT OR IGNORE INTO videos(title,url,result) VALUES(?,?,?)",
        (video.get("title"), video.get("url"), result)
    )
    conn.commit()
    conn.close()


def get_saved_videos():
    setup()
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute("SELECT id,title,url,created_at FROM videos ORDER BY id DESC")
    rows = cur.fetchall()
    conn.close()

    return [
        {
            "id": r[0],
            "title": r[1],
            "url": r[2],
            "created_at": r[3]
        }
        for r in rows
    ]


def get_video(video_id):
    setup()
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute("SELECT id,title,url,result,created_at FROM videos WHERE id=?", (video_id,))
    row = cur.fetchone()
    conn.close()

    if not row:
        return None

    return {
        "id": row[0],
        "title": row[1],
        "url": row[2],
        "result": row[3],
        "created_at": row[4]
    }


def delete_video(video_id):
    setup()
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute("DELETE FROM videos WHERE id=?", (video_id,))
    conn.commit()
    conn.close()
