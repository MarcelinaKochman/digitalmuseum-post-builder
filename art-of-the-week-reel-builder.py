import os
from moviepy.editor import ImageClip, concatenate_videoclips, ColorClip
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip
from moviepy.video.fx.resize import resize


def build_reel(final_slide_prefix: str, folder: str = './digitalaiartmuseum_posts'):
    # Set video resolution and background
    width, height = 1080, 1920
    background_color = (255, 255, 255)  # White background

    # Collect all jpg files in the folder
    images = [os.path.join(folder, img) for img in os.listdir(folder) if img.endswith('.jpg')]

    # Separate final slides with the specified prefix
    final_slides = sorted([img for img in images if os.path.basename(img).startswith(final_slide_prefix)])

    # Non-final slides (before the final slide)
    other_slides = sorted([img for img in images if img not in final_slides])

    # Total number of other slides
    total_other_slides = len(other_slides)

    # Set duration rules for the slides
    durations = []
    for i in range(total_other_slides):
        if i >= total_other_slides - 3:  # Last 3 slides
            durations.append(0.35)  # 5 seconds
        elif i >= total_other_slides - 7:  # 4 second to last slides
            durations.append(0.3)  # 4 seconds
        elif i >= total_other_slides - 12:  # 5 third to last slides
            durations.append(0.2)  # 3 seconds
        elif i >= total_other_slides - 18:  # 6 fourth to last slides
            durations.append(0.15)  # 2 seconds
        else:
            durations.append(0.1)  # 1 second for all others at the beginning

    # Create the clips list
    clips = []

    # Create video clips from the other slides
    for img, duration in zip(other_slides, durations):
        # Create the image clip and set its duration
        image_clip = ImageClip(img).set_duration(duration)

        # Resize the image to 1080x1080
        image_clip = image_clip.resize(height=1080)

        # Create a white background and composite the image on it
        background = ColorClip(size=(width, height), color=background_color).set_duration(duration)

        # Center the image on the background
        image_centered = image_clip.set_position("center").set_duration(duration)

        # Overlay the image on the background
        composite_clip = CompositeVideoClip([background, image_centered])

        clips.append(composite_clip)

    # Add final slide(s) with a 2-second duration each
    for img in final_slides:
        final_clip = ImageClip(img).set_duration(3)
        final_clip = final_clip.resize(height=1080)  # Resize final slides to 1080x1080
        background = ColorClip(size=(width, height), color=background_color).set_duration(5)

        # Center the final image on the background
        final_centered = final_clip.set_position("center").set_duration(5)

        # Overlay the final image on the background
        composite_final = CompositeVideoClip([background, final_centered])

        clips.append(composite_final)

    # Concatenate all the clips into one final video
    final_video = concatenate_videoclips(clips)

    # Save the video
    final_video.write_videofile("reel_output.mp4", fps=24)


build_reel("2025-04-07_08-29-11_")