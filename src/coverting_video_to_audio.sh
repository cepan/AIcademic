#!/bin/bash

# Directory containing MP4 files
SOURCE_DIR="/Users/shawnpan/Downloads/4K Video Downloader+/Mining Massive Datasets - Stanford University [FULL COURSE]"

# Directory to save MP3 files
DESTINATION_DIR="/Users/shawnpan/Downloads/audio/"

# Create destination directory if it doesn't exist
#mkdir -p "$DESTINATION_DIR"

# Convert each MP4 file to MP3
for file in "$SOURCE_DIR"/*.mp4; do
    # Extract filename without extension
    filename=$(basename -- "$file" .mp4)
    
    # Full path for the output MP3 file
    output_file="$DESTINATION_DIR/$filename.mp3"
    
    # Command to convert MP4 to MP3
    ffmpeg -i "$file" -q:a 0 -map a "$output_file"
    echo "Converted $file to $output_file"
done

echo "All conversions completed!"
