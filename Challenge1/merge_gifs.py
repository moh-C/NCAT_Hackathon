#!/usr/bin/env python3
"""
Script to merge multiple GIF files side by side with their names as titles.
"""

import imageio
from PIL import Image, ImageDraw, ImageFont
import os
import sys


def get_font(size=20):
    """Try to load a font, fallback to default if not available."""
    try:
        # Try to use a default system font
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", size)
    except:
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf", size)
        except:
            # Fallback to default font
            font = ImageFont.load_default()
    return font


def add_title_to_image(img, title, font_size=30):
    """
    Add a title to the top of an image.
    
    Args:
        img: PIL Image object
        title: String to display as title
        font_size: Size of the font
    
    Returns:
        PIL Image with title added
    """
    # Create a copy of the image
    img_with_title = img.copy()
    
    # Get font
    font = get_font(font_size)
    
    # Calculate title height
    draw = ImageDraw.Draw(img_with_title)
    bbox = draw.textbbox((0, 0), title, font=font)
    title_height = bbox[3] - bbox[1] + 20  # Add padding
    
    # Create new image with space for title
    new_img = Image.new('RGB', (img.width, img.height + title_height), color='white')
    
    # Paste title area
    draw = ImageDraw.Draw(new_img)
    text_x = (img.width - (bbox[2] - bbox[0])) // 2
    text_y = 10
    draw.text((text_x, text_y), title, fill='black', font=font)
    
    # Paste original image below title
    new_img.paste(img, (0, title_height))
    
    return new_img


def merge_gifs_side_by_side(gif_paths, output_path, titles=None):
    """
    Merge multiple GIF files side by side with titles.
    
    Args:
        gif_paths: List of paths to GIF files
        output_path: Path to save the merged GIF
        titles: List of titles for each GIF (if None, uses filename without extension)
    """
    if titles is None:
        titles = [os.path.splitext(os.path.basename(path))[0] for path in gif_paths]
    
    # Read all GIFs
    gifs = []
    max_frames = 0
    durations = []
    
    print("Loading GIFs...")
    for i, gif_path in enumerate(gif_paths):
        if not os.path.exists(gif_path):
            print(f"Error: {gif_path} not found!")
            sys.exit(1)
        
        reader = imageio.get_reader(gif_path)
        frames = []
        frame_durations = []
        
        for frame in reader:
            frames.append(Image.fromarray(frame))
            # Get duration if available
            if hasattr(reader, 'get_meta_data'):
                try:
                    meta = reader.get_meta_data()
                    duration = meta.get('duration', 0.1)
                    frame_durations.append(duration)
                except:
                    frame_durations.append(0.1)
            else:
                frame_durations.append(0.1)
        
        gifs.append(frames)
        durations.append(frame_durations)
        max_frames = max(max_frames, len(frames))
        print(f"  Loaded {gif_path}: {len(frames)} frames")
        reader.close()
    
    # Process each frame
    print(f"\nProcessing {max_frames} frames...")
    merged_frames = []
    merged_durations = []
    
    for frame_idx in range(max_frames):
        frame_images = []
        frame_widths = []
        frame_heights = []
        
        # Get or duplicate frame for each GIF
        for gif_idx, gif_frames in enumerate(gifs):
            if frame_idx < len(gif_frames):
                frame = gif_frames[frame_idx]
            else:
                # Use last frame if this GIF has fewer frames
                frame = gif_frames[-1]
            
            # Add title to frame
            title = titles[gif_idx]
            frame_with_title = add_title_to_image(frame, title)
            frame_images.append(frame_with_title)
            frame_widths.append(frame_with_title.width)
            frame_heights.append(frame_with_title.height)
        
        # Create merged frame
        total_width = sum(frame_widths)
        max_height = max(frame_heights)
        merged_frame = Image.new('RGB', (total_width, max_height), color='white')
        
        x_offset = 0
        for frame_img in frame_images:
            # Center vertically if heights differ
            y_offset = (max_height - frame_img.height) // 2
            merged_frame.paste(frame_img, (x_offset, y_offset))
            x_offset += frame_img.width
        
        merged_frames.append(merged_frame)
        
        # Use average duration from all GIFs for this frame
        frame_duration = 0.1
        valid_durations = [durations[i][min(frame_idx, len(durations[i])-1)] 
                          for i in range(len(durations))]
        if valid_durations:
            frame_duration = sum(valid_durations) / len(valid_durations)
        merged_durations.append(frame_duration)
        
        if (frame_idx + 1) % 10 == 0:
            print(f"  Processed {frame_idx + 1}/{max_frames} frames...")
    
    # Save merged GIF
    print(f"\nSaving merged GIF to {output_path}...")
    merged_frames_pil = [frame for frame in merged_frames]
    
    # Convert durations to milliseconds for imageio
    durations_ms = [int(d * 1000) for d in merged_durations]
    
    # Save using imageio
    writer = imageio.get_writer(output_path, mode='I', duration=durations_ms[0]/1000.0, loop=0)
    for frame, duration in zip(merged_frames, durations_ms):
        writer.append_data(frame)
    writer.close()
    
    print(f"Successfully created merged GIF: {output_path}")


def main():
    """Main function to merge GIFs."""
    # Define the 3 GIF files
    gif_files = [
        "Challenge1/raw_animation.gif",
        "Challenge1/single-stage.gif",
        "Challenge1/two-stage.gif"
    ]
    
    # Output path
    output_file = "merged_gifs.gif"
    
    # Merge the GIFs
    merge_gifs_side_by_side(gif_files, output_file)
    
    print("\nDone!")


if __name__ == "__main__":
    main()

