# instagram_downloader.py
import instaloader
from dotenv import load_dotenv
import os
from datetime import date
from src.two_factor_auth_handler import TwoFactorAuthHandler
from src.download_helper import configure_loader, download_stories, download_content
from src.logger_config import logger


def main():
    load_dotenv()
    username = os.getenv("INSTA_USERNAME")
    password = os.getenv("INSTA_PASSWORD")
    target_account = os.getenv("TARGET_ACCOUNT")

    if not all([username, password, target_account]):
        logger.error("Missing .env credentials")
        print("Required credentials missing in .env file")
        return

    loader = configure_loader("downloads")
    auth_handler = TwoFactorAuthHandler(loader, username, password)
    
    if not auth_handler.login():
        logger.error("Authentication failed")
        return

    today = date.today().isoformat()
    
    try:
        profile = instaloader.Profile.from_username(loader.context, target_account)
        
        # Download stories first
        download_stories(loader, profile, today)
        
        # Download posts and reels
        download_content(loader, profile)
        
    except Exception as e:
        logger.error(f"Fatal error: {str(e)}")
        print(f"Operation failed: {str(e)}")

if __name__ == "__main__":
    main()