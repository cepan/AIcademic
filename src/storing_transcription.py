import chromadb
import openai
from chromadb.utils.embedding_functions import OpenCLIPEmbeddingFunction
import os
import json

from chromadb.utils.data_loaders import ImageLoader

os.environ["OPENAI_API_KEY"] = "openai-api"
if os.getenv("OPENAI_API_KEY") is not None:
    openai.api_key = os.getenv("OPENAI_API_KEY")
else:
    print("OPENAI_API_KEY environment variable not found")

openai_ef = OpenCLIPEmbeddingFunction(
    # api_key=os.environ.get('OPENAI_API_KEY')
)
image_loader = ImageLoader()

# Replace with the actual path to your 'AIcademic' directory
root_dir = '../'
video_dir = os.path.join(root_dir, 'data', 'video',
                         'snapshot')  # sub directories
transcription_dir = os.path.join(
    root_dir, 'data', 'video', 'transcription')  # json files

# Lists to hold the unique ids for images, URIs for the images, and transcriptions
image_ids = []
image_uris = []
transcriptions = []
# video_inorder
video_link = ['xoA5v9AO7S0', 'G3S1fhCBRkY', 'uRjvVq1Jd-M', 'rUcBgSe6M4M', 'fL41WSVDunM', '1nLV8FEaZD0', '3_1h13PJkUs', 'VpiyOxiVmCg', 'ytjf6zYDd4s', 'UZePPh340sU', 'E9aoTVmQvok', 'ZsXIuJtjsWk', 'ZjdQD79Psi0', 'e8dA0tscrCM', 'QzXE8JDGxus', 'HjaRHQONwBE', 'lvtgro9ruJo', 'EmxxOyLcYrw', 'ONM5MB3_iOU', 'O9QnC5WJJ90', 'tY1JE6XFjCY', 'QIC3BuIQiNA', 'uYz84Hmi_ac', 'k0uxnVEuuz0', 'BQgglNWdqak', 'cuDDBfvK71g', 'Y78Kugdq24I', 'c0_vNfNZ4JM', 'zLuVrqlYKyg', 'FRZvgNvALJ4', 'RJtCR3h9mXQ', 'Cedjf9G0otE', 'siCPjpUtE0A', 'uxsDKhZHDcc', 'dScm-2uL-Fk', 'SRTSVxUnsNI', 'NDSAiEGJshM', 'qBTdukbzc78', '895jWrdNA5I', 'A5DOq-SGt5A', '1JRrCEgiyHM', '2uxXPzm-7FY', 'h9gpufJFF-0', '6BTLobS7AU8', 'VZKMyTaLI00', 'yLdOS6xyM_Q', 'P5mlg91as1c',
              'UyAfmAZU_WI', 'c7e-D2tmRE0', 'K38wVcdNuFc', 'SO1KTzuKTSI', 'WgK_D6IyDbM', 'qgsuly5nxIw', '4-f77HjB_CI', 'E8aMcwmqsTg', 'GGWBMg0i9d4', 'HY3Csl52PfE', 'DLfh8pv4-yQ', 'rg2cjfMsCk4', 'RD0nNK51Fp8', 'NP1Zk8MY08k', 'JrOJspZ1CUw', 'h0fBgE1tp3Y', 'vKz3EwibNAw', '9orfibrnIRk', 'c0e3S_4k6Eg', 'v7H5ks5iDEQ', 'ax8LxRZCORU', 'bS1avoD6g8s', '8xbnLHn4jjQ', 'rB-iRIpAPKo', '7eKCLOcten4', 'NsUqRe-9tb4', 'QjFHWUsoZBw', 'wNhnAogeHJQ', 'y8wQire7BuQ', 'Y6sON_3b1Bc', 'sCaKwQEF8Ao', 'TrSPBIwnlAA', 'Z0A9C2kabAM', 'SMGETXHYCyM', '_rWpSC-s4vU', 'n9S9wmMRCtw', 'b28Pqp--P6w', 'WJLE2rMrbqs', 'oxTYnvJYGDo', 'MYHEXXVe8Bw', 'qwUh8K3s03o', 'URaS1u-Murc', 'utqXi7BGSmQ', 'EREz63VQIEI', 'rQEDfQzfvSw', 'blvMKHJFkPo', 'c6GExahScyU']
meta_data = []


def generate_image_id(lecture_number, image_number):
    return f'lecture{lecture_number}_image{image_number}'


def get_image_uri(video_folder, image_file):
    return os.path.join(video_folder, image_file)


def read_transcription_file(json_path):
    with open(json_path, 'r') as file:
        return json.load(file)


# Iterating through the lecture folders to populate the lists
for lecture_folder in sorted(os.listdir(video_dir)):
    # Extracting lecture number from the folder name
    # print(lecture_folder)
    lecture_number = lecture_folder.split(' — ')[0].split()[1]
    # print(lecture_number)
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
    transcription_keys = list(transcription_data.keys())

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
        timestamp_key = transcription_keys[i]
        transcriptions.append(
            transcription_data[timestamp_key])
        meta_data.append(
            {"youtube_link": "https://www.youtube.com/watch?v="+video_link[int(lecture_number)-1]})

chroma_client = chromadb.PersistentClient(path="../chromadb/DSCI553")


collection = chroma_client.get_or_create_collection(
    name="openclip",
    embedding_function=openai_ef,
    data_loader=image_loader)

collection.add(ids=image_ids, uris=image_uris,
               metadatas=meta_data, documents=transcriptions)
print("Successfully stored photos and relevant information")
