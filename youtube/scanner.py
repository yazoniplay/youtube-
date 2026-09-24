from googleapiclient.discovery import build
from datetime import datetime, timezone, timedelta
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

        queries = [
            "viral shorts",
            "youtube shorts trending",
            "viral challenge",
            "minecraft shorts",
            "AI shorts",
            "funny shorts"
        ]

        candidates = []
        published_after = (datetime.now(timezone.utc) - timedelta(days=7)).isoformat().replace("+00:00", "Z")

        for query in queries:
            search = youtube.search().list(
                part="snippet",
                maxResults=25,
                order="relevance",
                publishedAfter=published_after,
                q=query,
                type="video"
            ).execute()

            ids = [
                item.get("id", {}).get("videoId")
                for item in search.get("items", [])
                if item.get("id", {}).get("videoId")
            ]

            if not ids:
                continue

            details_response = youtube.videos().list(
                part="statistics,snippet,contentDetails",
                id=",".join(ids)
            ).execute()

            for details in details_response.get("items", []):
                stats = details.get("statistics", {})
                snippet = details.get("snippet", {})
                video_id = details.get("id")

                published = snippet.get("publishedAt")
                if not published:
                    continue

                upload_time = datetime.fromisoformat(published.replace("Z", "+00:00"))
                hours_old = max((datetime.now(timezone.utc) - upload_time).total_seconds() / 3600, 1)

                video = {
                    "title": snippet.get("title", "Unknown"),
                    "url": f"https://youtube.com/watch?v={video_id}",
                    "views": int(stats.get("viewCount", 0)),
                    "likes": int(stats.get("likeCount", 0)),
                    "comments": int(stats.get("commentCount", 0)),
                    "hours_old": hours_old
                }

                # ignore dead videos
                if video["views"] < 1000:
                    continue

                video["viral_score"] = calculate_score(video)
                candidates.append(video)

        # fallback search without date filter if nothing found
        if not candidates:
            search = youtube.search().list(
                part="snippet",
                maxResults=10,
                order="viewCount",
                q="viral shorts",
                type="video"
            ).execute()

            for item in search.get("items", []):
                video_id = item.get("id", {}).get("videoId")
                if video_id:
                    candidates.append({
                        "title": item["snippet"].get("title", "Unknown"),
                        "url": f"https://youtube.com/watch?v={video_id}",
                        "views": 0,
                        "likes": 0,
                        "comments": 0,
                        "hours_old": 24,
                        "viral_score": 0
                    })

        return max(candidates, key=lambda x: x["viral_score"]) if candidates else None

    except Exception as e:
        print(f"YouTube scanner error: {e}")
        return None
