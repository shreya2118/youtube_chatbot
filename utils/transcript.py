from youtube_transcript_api import YouTubeTranscriptApi

def get_transcript(video_id):

    ytt = YouTubeTranscriptApi()

    transcript = ytt.fetch(
        video_id,
        languages=["en"]
    )

    return " ".join(
        snippet.text
        for snippet in transcript
    )