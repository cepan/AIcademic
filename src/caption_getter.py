from googleapiclient.discovery import build
from youtube_transcript_api import YouTubeTranscriptApi

# Your API key
api_key = 'AIzaSyBl0258Fl6Bw5s9SzXTYzFbJS44LRKvmCM'

youtube = build('youtube', 'v3', developerKey=api_key)

# Function to get video IDs from a playlist


def get_video_ids_from_playlist(playlist_id):
    video_ids = []
    next_page_token = None

    while True:
        pl_request = youtube.playlistItems().list(
            part='contentDetails',
            playlistId=playlist_id,
            maxResults=50,
            pageToken=next_page_token
        )

        pl_response = pl_request.execute()

        video_ids += [item['contentDetails']['videoId']
                      for item in pl_response['items']]

        next_page_token = pl_response.get('nextPageToken')

        if not next_page_token:
            break

    return video_ids


playlist_id = 'PLLssT5z_DsK9JDLcT8T62VtzwyW9LNepV'
video_ids = get_video_ids_from_playlist(playlist_id)[:2]


def get_transcription(video_id):

    transcript = YouTubeTranscriptApi.get_transcript(video_id)

    accumulated_text = ""
    next_boundary = 20
    result = {}

    for entry in transcript:
        start = entry['start']
        text = entry['text']

        while start >= next_boundary:
            result[f"{next_boundary-20}-{next_boundary}"] = accumulated_text
            # result.appensd()
            accumulated_text = ""
            next_boundary += 20

        # Append the current text to the accumulated text
        accumulated_text += " " + text

    if accumulated_text:
        # print(next_boundary-20)
        # print(accumulated_text)
        result[f"{next_boundary-20}-{next_boundary}"] = accumulated_text
    print(result)


all_video_transcription = []
for video_id in video_ids:
    # print(video_id)
    all_video_transcription.append(get_transcription(video_id))
