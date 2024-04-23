import chromadb
import openai
from chromadb.utils.embedding_functions import OpenCLIPEmbeddingFunction
import os
import json
import numpy as np
from PIL import Image

os.environ["OPENAI_API_KEY"] = "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"
if os.getenv("OPENAI_API_KEY") is not None:
    openai.api_key = os.getenv("OPENAI_API_KEY")
else:
    print("OPENAI_API_KEY environment variable not found")

openai_ef = OpenCLIPEmbeddingFunction(
    # api_key=os.environ.get('OPENAI_API_KEY')
)


# Replace with the actual path to your 'AIcademic' directory
root_dir = '/Users/shawnpan/Github/AIcademic'
video_dir = os.path.join(root_dir, 'data', 'video',
                         'snapshot')  # sub directories
transcription_dir = os.path.join(
    root_dir, 'data', 'video', 'transcription')  # json files

# Lists to hold the unique ids for images, URIs for the images, and transcriptions
image_ids = []
image_uris = []
transcriptions = []

# Function to generate unique image IDs


def generate_image_id(lecture_number, image_number):
    return f'lecture{lecture_number}_image{image_number}'

# Function to get the URI for an image


def get_image_uri(video_folder, image_file):
    return os.path.join(video_folder, image_file)

# Function to read the JSON transcription file


def read_transcription_file(json_path):
    with open(json_path, 'r') as file:
        return json.load(file)


# Iterating through the lecture folders to populate the lists
for lecture_folder in sorted(os.listdir(video_dir)):
    # Extracting lecture number from the folder name
    print(lecture_folder)
    lecture_number = lecture_folder.split(' — ')[1].split('   ')[0]

    # Constructing paths for the video folder and transcription JSON
    video_folder_path = os.path.join(
        video_dir, lecture_folder)  # full of images
    # navigate to lecture json
    transcription_file_name = f"{lecture_folder}.json"
    transcription_file_path = os.path.join(
        transcription_dir, transcription_file_name)

    # Reading transcription data from JSON
    transcription_data = read_transcription_file(
        transcription_file_path)  # JSON Object

    # Checking if the number of images matches the number of transcription entries
    image_files = sorted(os.listdir(video_folder_path))
    transcription_keys = sorted(transcription_data.keys())

    if len(image_files) != len(transcription_keys):
        print(
            f"Warning: The number of images in '{lecture_folder}' does not match the number of transcriptions.")
        continue

    # Populating the lists
    for i, image_file in enumerate(image_files):
        # Generating unique ID and URI for the image
        image_id = generate_image_id(lecture_number, i)
        image_ids.append(image_id)

        image_uri = get_image_uri(video_folder_path, image_file)
        image_uris.append(image_uri)

        # Extracting transcription for the corresponding image
        timestamp_key = transcription_keys[i]
        transcriptions.append(
            {timestamp_key: transcription_data[timestamp_key]})

# Output the lists
print(f"Image IDs: {image_ids}")
# print(f"Image URIs: {image_uris}")
# print(f"Transcriptions: {transcriptions})")


exit()


chroma_client = chromadb.PersistentClient(path="../chromadb/DSCI553")


collection = chroma_client.get_or_create_collection(
    name="openclip", embedding_function=openai_ef)
