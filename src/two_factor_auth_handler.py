from instaloader.exceptions import (TwoFactorAuthRequiredException,
                                  BadCredentialsException)

from src.logger_config import logger


class TwoFactorAuthHandler:
    def __init__(self, loader, username, password):
        self.loader = loader
        self.username = username
        self.password = password

    def login(self):
        max_attempts = 3
        for attempt in range(1, max_attempts + 1):
            try:
                self.loader.login(self.username, self.password)
                return True
            except TwoFactorAuthRequiredException:
                print("\nTwo-factor authentication required.")
                code = input("Enter 2FA code from trusted device: ")
                try:
                    self.loader.two_factor_login(code)
                    return True
                except BadCredentialsException:
                    print(f"Invalid code (Attempt {attempt}/{max_attempts})")
                    if attempt == max_attempts:
                        logger.error("2FA max attempts reached")
                        return False
            except Exception as e:
                logger.error(f"Login error: {str(e)}")
                print(f"Login failed: {str(e)}")
                return False
        return False