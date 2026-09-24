from googleapiclient.discovery import build
from datetime import datetime, timezone
from config import YOUTUBE_API_KEY


def calculate_score(video):
    views = video.get("views", 0)
    hours = max(video.get("hours_old", 1), 1)
    likes = video.get("likes", 0)
    comments = video.get("comments", 0)

    views_per_hour = views / hours
    engagement = ((likes + comments) / max(views, 1)) * 100

    return round((views_per_hour / 1000) + (engagement * 50), 2)


def find_viral_video():
    try:
        youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)

        search = youtube.search().list(
            part="snippet",
            maxResults=10,
            order="date",
            type="video"
        ).execute()

        candidates = []

        for item in search.get("items", []):
            video_id = item.get("id", {}).get("videoId")

            if not video_id:
                continue

            details_response = youtube.videos().list(
                part="statistics,snippet",
                id=video_id
            ).execute()

            if not details_response.get("items"):
                continue

            details = details_response["items"][0]
            stats = details.get("statistics", {})
            published = details.get("snippet", {}).get("publishedAt")

            if not published:
                continue

            upload_time = datetime.fromisoformat(published.replace("Z", "+00:00"))
            hours_old = max((datetime.now(timezone.utc) - upload_time).total_seconds() / 3600, 1)

            video = {
                "title": details["snippet"].get("title", "Unknown"),
                "url": f"https://youtube.com/watch?v={video_id}",
                "views": int(stats.get("viewCount", 0)),
                "likes": int(stats.get("likeCount", 0)),
                "comments": int(stats.get("commentCount", 0)),
                "hours_old": hours_old
            }

            video["viral_score"] = calculate_score(video)
            candidates.append(video)

        if not candidates:
            return None

        return max(candidates, key=lambda x: x["viral_score"])

    except Exception as e:
        print(f"YouTube scanner error: {e}")
        return None
