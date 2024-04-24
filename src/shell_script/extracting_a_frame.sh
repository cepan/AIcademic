#!/bin/bash

# Define the path to the specific video file
VIDEO_FILE="/Users/shawnpan/Downloads/4K Video Downloader+/video_Mining Massive Datasets - Stanford University [FULL COURSE]/Lecture 65 — The Balance Algorithm   Mining of Massive Datasets   Stanford University.mp4"
# Ensure there's no space around the '='
IMAGE_FOLDER="/Users/shawnpan/Github/AIcademic/data/video/snapshot"

# Check if the specified video file actually exists
if [ ! -f "$VIDEO_FILE" ]; then
  echo "Error: Video file does not exist."
  exit 1
fi

# Extract the filename without the extension
base_name=$(basename "$VIDEO_FILE" .mp4)

# Create a directory within IMAGE_FOLDER with the name of the video file
mkdir -p "$IMAGE_FOLDER/$base_name"

# Use ffmpeg to extract frames and save them in the created directory, specifying full paths
ffmpeg -i "$VIDEO_FILE" -r 0.05 "$IMAGE_FOLDER/$base_name/output_%03d.jpeg"
