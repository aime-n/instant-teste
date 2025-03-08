import time
import instaloader
import os
from src.logger_config import logger


def configure_loader(target_dir):
    loader = instaloader.Instaloader(
        quiet=True,
        download_video_thumbnails=False,
        compress_json=False
    )
    loader.download_geotags = False
    loader.save_metadata = True
    loader.dirname_pattern = target_dir
    return loader

def download_stories(loader, profile, date_folder):
    try:
        story_dir = os.path.join("downloads", "stories", date_folder)
        os.makedirs(story_dir, exist_ok=True)
        loader.dirname_pattern = story_dir
        loader.download_stories(userids=[profile.userid])
        logger.info(f"Downloaded stories for {profile.username} on {date_folder}")

        time.sleep(2)  # Rate limiting between story requests
    except Exception as e:
        logger.error(f"Story download failed: {str(e)}")
        raise

def download_content(loader, profile):
    consecutive_errors = 0
    posts = profile.get_posts()
    for post in posts:
        try:
            content_type = "reels" if post.is_video else "posts"
            target_dir = os.path.join("downloads", content_type)
            
            os.makedirs(target_dir, exist_ok=True)
            date = post.date_local.date().isoformat()
            post_dir = os.path.join(target_dir, f"{date}_{post.shortcode}")
            if not os.path.exists(post_dir):
                loader.dirname_pattern = post_dir
                loader.download_post(post, target=target_dir)
                logger.info(f"Downloaded {content_type} for {profile.username} on {date}")
                consecutive_errors = 0
                
                time.sleep(2)  # Rate limiting
        except Exception as e:
            consecutive_errors += 1
            logger.error(f"Download error ({post.shortcode}): {str(e)}")
            if consecutive_errors >= 5:
                logger.error("Max consecutive errors reached - aborting")
                break