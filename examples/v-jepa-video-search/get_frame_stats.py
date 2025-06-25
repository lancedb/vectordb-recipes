import os
import cv2
import statistics
from pathlib import Path

def get_video_frame_count(video_path):
    """
    Get the total number of frames in a video file.
    
    Args:
        video_path (str): Path to the video file
        
    Returns:
        int: Number of frames, or None if error
    """
    try:
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            print(f"Error: Could not open video {video_path}")
            return None
        
        # Get total frame count
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        cap.release()
        
        return frame_count
    except Exception as e:
        print(f"Error processing {video_path}: {str(e)}")
        return None

def scan_video_folder(folder_path, verbose=False):
    """
    Scan a folder for video files and analyze frame counts.
    
    Args:
        folder_path (str): Path to the folder containing videos
        verbose (bool): Whether to show detailed processing info
        
    Returns:
        dict: Statistics about video frame counts
    """
    # Common video file extensions
    video_extensions = {'.mp4', '.avi', '.mov', '.mkv', '.wmv', '.flv', '.webm', '.m4v', '.3gp'}
    
    folder = Path(folder_path)
    if not folder.exists():
        print(f"Error: Folder '{folder_path}' does not exist")
        return None
    
    frame_counts = []
    video_info = []
    
    print(f"Scanning folder: {folder_path}")
    
    # Find all video files in the folder
    video_files = []
    for file_path in folder.rglob('*'):
        if file_path.is_file() and file_path.suffix.lower() in video_extensions:
            video_files.append(file_path)
    
    if not video_files:
        print("No video files found in the specified folder")
        return None
    
    print(f"Processing {len(video_files)} video files...")
    
    # Process each video file
    processed_count = 0
    for i, video_file in enumerate(video_files, 1):
        if verbose:
            print(f"Processing ({i}/{len(video_files)}): {video_file.name}")
        
        frame_count = get_video_frame_count(str(video_file))
        
        if frame_count is not None:
            frame_counts.append(frame_count)
            video_info.append({
                'filename': video_file.name,
                'path': str(video_file),
                'frames': frame_count
            })
            processed_count += 1
            if verbose:
                print(f"  Frames: {frame_count}")
        else:
            if verbose:
                print(f"  Failed to process")
        
        # Show progress every 100 files
        if not verbose and i % 100 == 0:
            print(f"  Processed {i}/{len(video_files)} files...")
    
    print(f"Successfully processed {processed_count}/{len(video_files)} videos")
    
    if not frame_counts:
        print("No videos could be processed successfully")
        return None
    
    # Calculate statistics
    stats = {
        'total_videos': len(frame_counts),
        'mean_frames': statistics.mean(frame_counts),
        'min_frames': min(frame_counts),
        'max_frames': max(frame_counts),
        'median_frames': statistics.median(frame_counts),
        'total_frames': sum(frame_counts),
        'video_details': video_info
    }
    
    return stats

def print_statistics(stats, show_all_videos=False):
    """Print the video frame statistics in a formatted way."""
    if not stats:
        return
    
    print("\n" + "=" * 50)
    print("VIDEO FRAME ANALYSIS RESULTS")
    print("=" * 50)
    print(f"Total videos processed: {stats['total_videos']}")
    print(f"Total frames across all videos: {stats['total_frames']:,}")
    print()
    print("FRAME COUNT STATISTICS:")
    print(f"  Mean (Average): {stats['mean_frames']:.2f} frames")
    print(f"  Minimum:        {stats['min_frames']} frames")
    print(f"  Maximum:        {stats['max_frames']} frames")
    print(f"  Median:         {stats['median_frames']:.2f} frames")
    print()
    
    # Find videos with min and max frames
    min_videos = [v for v in stats['video_details'] if v['frames'] == stats['min_frames']]
    max_videos = [v for v in stats['video_details'] if v['frames'] == stats['max_frames']]
    
    print("VIDEOS WITH MINIMUM FRAMES:")
    for video in min_videos[:3]:  # Show only first 3
        print(f"  {video['filename']}: {video['frames']} frames")
    if len(min_videos) > 3:
        print(f"  ... and {len(min_videos) - 3} more")
    
    print("\nVIDEOS WITH MAXIMUM FRAMES:")
    for video in max_videos[:3]:  # Show only first 3
        print(f"  {video['filename']}: {video['frames']} frames")
    if len(max_videos) > 3:
        print(f"  ... and {len(max_videos) - 3} more")
    
    if show_all_videos:
        print("\nALL VIDEO DETAILS:")
        print("-" * 50)
        for video in sorted(stats['video_details'], key=lambda x: x['frames']):
            print(f"{video['filename']}: {video['frames']} frames")

def main():
    """Main function to run the video frame analysis."""
    folder_path = "UCF-101"
    
    # Ask for verbosity preference
    #verbose_input = input("Show detailed processing (y/n, default=n): ").strip().lower()
    verbose = False
    
    # Ask if user wants to see all video details
    #show_all_input = input("Show all video details in results (y/n, default=n): ").strip().lower()
    show_all = False
    
    # Scan the folder and get statistics
    stats = scan_video_folder(folder_path, verbose=verbose)
    
    # Print results
    print_statistics(stats, show_all_videos=show_all)

if __name__ == "__main__":
    main()