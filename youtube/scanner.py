from googleapiclient.discovery import build
from config import YOUTUBE_API_KEY


def find_viral_video():
    youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)

    response = youtube.search().list(
        part="snippet",
        maxResults=1,
        order="viewCount",
        type="video"
    ).execute()

    item = response["items"][0]

    return {
        "title": item["snippet"]["title"],
        "url": "https://youtube.com/watch?v=" + item["id"]["videoId"]
    }
