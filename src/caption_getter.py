from googleapiclient.discovery import build
from youtube_transcript_api import YouTubeTranscriptApi

import openai
import os
import json
import re
# Your API key
api_key = 'google-api'
AUDIO_FOLDER = '/Users/shawnpan/Downloads/audio'


def get_video_details_from_playlist(youtube, playlist_id):
    video_details = []
    next_page_token = None

    while True:
        # Request to get playlist items
        pl_request = youtube.playlistItems().list(
            part='contentDetails',
            playlistId=playlist_id,
            maxResults=50,
            pageToken=next_page_token
        )

        pl_response = pl_request.execute()

        video_ids = [item['contentDetails']['videoId']
                     for item in pl_response['items']]

        if video_ids:
            # Request to get video details
            video_request = youtube.videos().list(
                part="id,snippet",
                id=','.join(video_ids)
            )
            video_response = video_request.execute()

            # Collect video ID and title
            video_details += [{'videoId': item['id'], 'title': item['snippet']['title']}
                              for item in video_response['items']]
            # video_details += [item['id'] for item in video_response['items']]

        next_page_token = pl_response.get('nextPageToken')

        if not next_page_token:
            break

    return video_details


def divide_transcript(transcript):
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

    return result


def srt_to_dict(srt):
    subtitles = srt.strip().split('\n\n')

    # Prepare a list to store subtitle dictionaries
    result = []

    # Define a regex pattern to find timecodes and text
    timecode_pattern = re.compile(
        r'(\d{2}):(\d{2}):(\d{2}),(\d{3}) --> \d{2}:\d{2}:\d{2},\d{3}')

    for subtitle in subtitles:
        # Split subtitle into lines
        lines = subtitle.split('\n')

        if len(lines) >= 3:
            # The first line is the subtitle number (ignored in output)
            # The second line contains the timecodes
            time_match = timecode_pattern.match(lines[1])

            if time_match:
                # Calculate start time in seconds
                hours, minutes, seconds, milliseconds = map(
                    int, time_match.groups())
                start_time = hours * 3600 + minutes * 60 + seconds + milliseconds / 1000.0

                # The rest is the subtitle text
                text = ' '.join(lines[2:])

                # Append to result list as a dictionary
                result.append({'text': text, 'start': start_time})
    return result


def transcibe_audio(lecture):
    missing_transcription = os.path.join(
        AUDIO_FOLDER, lecture + '.mp3')

    with open(missing_transcription, "rb") as audio_file:
        # exit()
        generated_transcript = client.audio.transcriptions.create(
            file=audio_file,
            model="whisper-1",
            response_format="srt"
        )

    text = srt_to_dict(generated_transcript)

    return text


def get_transcription(video_id, lecture):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)

    except:
        print(
            f"Error for {lecture} NO TRANSCRIPTION ID: {video_id}")

        transcript = transcibe_audio(lecture)
        if not transcript:
            return None

    transcript_divided = divide_transcript(transcript)

    output_fp = os.path.join("../data/video/transcription", lecture+".json")
    with open(output_fp, 'w') as file:
        json.dump(transcript_divided, file, indent=4)

    return transcript_divided


os.environ["OPENAI_API_KEY"] = "openai-api"
client = openai.OpenAI()


youtube = build('youtube', 'v3', developerKey=api_key)
playlist_id = 'PLLssT5z_DsK9JDLcT8T62VtzwyW9LNepV'
video_ids = get_video_details_from_playlist(youtube, playlist_id)
lectures = video_ids

all_video_transcription = []
for lecture in lectures:
    # print(lecture['videoId'], lecture['title'])
    get_transcription(lecture['videoId'], lecture['title'])

print("ALL TRANSCIPTIONS RETRIEVED")
