from moviepy.editor import VideoFileClip, clips_array, vfx

def convert_to_black_and_white(input_video_path, output_video_path):
    # Load the video file
    clip = VideoFileClip(input_video_path)
    
    # Convert the video to grayscale
    grayscale_clip = clip.fx(vfx.blackwhite)
    
    # Write the result to the output file
    grayscale_clip.write_videofile(output_video_path, codec="libx264", audio_codec="aac")

# Example usage
input_video_path = '/Users/shayneskrtic/Desktop/WormWatcher/cropped_video.mp4'
output_video_path = '/Users/shayneskrtic/Desktop/WormWatcher/cropped_video.mp4'
convert_to_black_and_white(input_video_path, output_video_path)
