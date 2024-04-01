#!/bin/bash

# Define the path to the directory containing your video files
VIDEO_FOLDER="/Users/shawnpan/Downloads/4K Video Downloader+/Mining Massive Datasets - Stanford University [FULL COURSE]"
# Ensure there's no space around the '='
IMAGE_FOLDER="/Users/shawnpan/Github/AIcademic/data/video/snapshot"

# Iterate over each video file in the directory
for video_file in "$VIDEO_FOLDER"/*.mp4; do
  # Skip if directory (in case of no .mp4 files)
  [ -d "$video_file" ] && continue

  # Extract the filename without the extension
  base_name=$(basename "$video_file" .mp4)

  # Create a directory within IMAGE_FOLDER with the name of the video file
  mkdir -p "$IMAGE_FOLDER/$base_name"

  # Use ffmpeg to extract frames and save them in the created directory, specifying full paths
  ffmpeg -i "$video_file" -r 0.05 "$IMAGE_FOLDER/$base_name/output_%03d.jpeg"
done
