"""
TikTok Automation Bot - Enhanced Version
Author: Enhanced by Copilot based on NoNameoN-A's original work
Repository: https://github.com/Pausiar/tiktok_boost

WARNING: This bot is for educational purposes only.
Using automation to manipulate TikTok metrics violates TikTok's Terms of Service
and may result in permanent account suspension.
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import logging
import sys
import time
import json
from pathlib import Path
from datetime import datetime


class TikTokBot:
    """Enhanced TikTok automation bot with modern Selenium practices."""
    
    def __init__(self, config_path="config.json"):
        """Initialize the bot with configuration."""
        self.config = self.load_config(config_path)
        self.setup_logging()
        self.driver = None
        self.stats = {
            'views_delivered': 0,
            'hearts_delivered': 0,
            'followers_delivered': 0,
            'errors': 0,
            'start_time': datetime.now()
        }
        
    def load_config(self, config_path):
        """Load configuration from JSON file."""
        default_config = {
            "video_url": "https://www.tiktok.com/@username/video/1234567890",
            "bot_mode": 1,
            "chromedriver_path": "chromedriver",
            "headless": False,
            "max_retries": 3,
            "base_wait_time": 10,
            "target_site": "https://vipto.de/"
        }
        
        config_file = Path(config_path)
        if config_file.exists():
            with open(config_file, 'r') as f:
                user_config = json.load(f)
                default_config.update(user_config)
        else:
            # Create default config file
            with open(config_path, 'w') as f:
                json.dump(default_config, f, indent=4)
            self.logger.info(f"Created default config file: {config_path}")
        
        return default_config
    
    def setup_logging(self):
        """Configure logging system."""
        log_format = '%(asctime)s - %(levelname)s - %(message)s'
        logging.basicConfig(
            level=logging.INFO,
            format=log_format,
            handlers=[
                logging.FileHandler(f'tiktok_bot_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'),
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def setup_driver(self):
        """Initialize Chrome WebDriver with options."""
        try:
            chrome_options = webdriver.ChromeOptions()
            if self.config['headless']:
                chrome_options.add_argument('--headless')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-blink-features=AutomationControlled')
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            
            self.driver = webdriver.Chrome(
                executable_path=self.config['chromedriver_path'],
                options=chrome_options
            )
            self.driver.maximize_window()
            self.logger.info("WebDriver initialized successfully")
        except Exception as e:
            self.logger.error(f"Failed to initialize WebDriver: {e}")
            raise
    
    def wait_for_element(self, by, value, timeout=20):
        """Wait for an element to be clickable."""
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable((by, value))
            )
            return element
        except TimeoutException:
            self.logger.warning(f"Timeout waiting for element: {value}")
            return None
    
    def safe_click(self, by, value, timeout=20):
        """Safely click an element with wait."""
        element = self.wait_for_element(by, value, timeout)
        if element:
            element.click()
            return True
        return False
    
    def safe_send_keys(self, by, value, keys, timeout=20):
        """Safely send keys to an element."""
        element = self.wait_for_element(by, value, timeout)
        if element:
            element.clear()
            element.send_keys(keys)
            return True
        return False
    
    def handle_captcha(self):
        """Wait for user to solve captcha."""
        self.logger.info("⚠️ Please solve the CAPTCHA in the browser window...")
        self.logger.info("Waiting 60 seconds for captcha solution...")
        time.sleep(60)
    
    def views_loop(self, retry_count=0):
        """Automated views generation loop."""
        if retry_count >= self.config['max_retries']:
            self.logger.error("Max retries reached for views loop")
            return
        
        try:
            time.sleep(self.config['base_wait_time'])
            
            # Click views button
            if not self.safe_click(By.XPATH, "/html/body/div[4]/div[1]/div[3]/div/div[4]/div/button"):
                self.logger.warning("Captcha detected or button not found")
                self.handle_captcha()
                self.driver.refresh()
                return self.views_loop(retry_count + 1)
            
            # Enter video URL
            time.sleep(2)
            if not self.safe_send_keys(By.XPATH, "//*[@id=\"sid4\"]/div/div/div/form/div/input", 
                                      self.config['video_url']):
                raise Exception("Failed to enter video URL")
            
            # Click search
            time.sleep(1)
            self.safe_click(By.XPATH, "//*[@id=\"sid4\"]/div/div/div/form/div/div/button")
            
            # Submit for views
            time.sleep(2)
            self.safe_click(By.XPATH, "//*[@id=\"c2VuZC9mb2xsb3dlcnNfdGlrdG9V\"]/div[1]/div/form/button")
            
            self.stats['views_delivered'] += 1000
            self.logger.info(f"✅ Views delivered! Total: {self.stats['views_delivered']} views")
            
            # Wait before next iteration
            time.sleep(55)
            self.driver.refresh()
            self.views_loop(0)
            
        except Exception as e:
            self.stats['errors'] += 1
            self.logger.error(f"Error in views loop: {e}")
            self.driver.refresh()
            time.sleep(5)
            self.views_loop(retry_count + 1)
    
    def hearts_loop(self, retry_count=0):
        """Automated hearts/likes generation loop."""
        if retry_count >= self.config['max_retries']:
            self.logger.error("Max retries reached for hearts loop")
            return
        
        try:
            time.sleep(self.config['base_wait_time'])
            
            # Click hearts button
            if not self.safe_click(By.XPATH, "/html/body/div[4]/div[1]/div[3]/div/div[2]/div/button"):
                self.logger.warning("Captcha detected or button not found")
                self.handle_captcha()
                self.driver.refresh()
                return self.hearts_loop(retry_count + 1)
            
            # Enter video URL
            time.sleep(2)
            if not self.safe_send_keys(By.XPATH, "/html/body/div[4]/div[3]/div/div/div/form/div/input",
                                      self.config['video_url']):
                raise Exception("Failed to enter video URL")
            
            # Click search
            time.sleep(1)
            self.safe_click(By.XPATH, "/html/body/div[4]/div[3]/div/div/div/form/div/div/button")
            
            # Submit for hearts
            time.sleep(10)
            self.safe_click(By.XPATH, "/html/body/div[4]/div[3]/div/div/div/div/div[1]/div/form/button")
            
            # Get hearts count
            time.sleep(10)
            try:
                hearts_element = self.driver.find_element(By.XPATH, '//*[@id="c2VuZE9nb2xsb3dlcnNfdGlrdG9r"]/span')
                hearts_count = hearts_element.text
                self.logger.info(f"✅ {hearts_count} hearts delivered!")
            except:
                self.logger.info("✅ Hearts delivered!")
            
            self.stats['hearts_delivered'] += 1
            
            # Wait before next iteration
            time.sleep(155)
            self.driver.refresh()
            time.sleep(200)
            self.hearts_loop(0)
            
        except Exception as e:
            self.stats['errors'] += 1
            self.logger.error(f"Error in hearts loop: {e}")
            self.driver.refresh()
            time.sleep(355)
            self.hearts_loop(retry_count + 1)
    
    def followers_loop(self, retry_count=0):
        """Automated followers generation loop."""
        if retry_count >= self.config['max_retries']:
            self.logger.error("Max retries reached for followers loop")
            return
        
        wait_time = 660  # 11 minutes
        
        try:
            time.sleep(20)
            
            # Click followers button
            if not self.safe_click(By.XPATH, "/html/body/div[4]/div[1]/div[3]/div/div[1]/div/button"):
                self.logger.warning("Captcha detected or button not found")
                self.handle_captcha()
                self.driver.refresh()
                return self.followers_loop(retry_count + 1)
            
            # Enter video URL
            time.sleep(20)
            if not self.safe_send_keys(By.XPATH, "/html/body/div[4]/div[2]/div/div/div/form/div/input",
                                      self.config['video_url']):
                raise Exception("Failed to enter video URL")
            
            # Click search
            time.sleep(2)
            self.safe_click(By.XPATH, "//*[@id=\"sid\"]/div/div/div/form/div/div/button")
            
            # Add followers
            time.sleep(20)
            self.safe_click(By.XPATH, "//*[@id=\"c2VuZF9mb2xsb3dlcnNfdGlrdG9r\"]/div[1]/div/form/button")
            
            self.stats['followers_delivered'] += 1
            self.logger.info(f"✅ Followers delivered! Total: {self.stats['followers_delivered']}")
            
            # Wait before next iteration
            time.sleep(wait_time)
            self.driver.refresh()
            self.followers_loop(0)
            
        except Exception as e:
            self.stats['errors'] += 1
            self.logger.error(f"Error in followers loop: {e}")
            self.driver.refresh()
            time.sleep(wait_time)
            self.followers_loop(retry_count + 1)
    
    def print_banner(self):
        """Print startup banner."""
        banner = """
╔══════════════════════════════════════════════╗
║     TikTok Bot - Enhanced Version            ║
║     Educational Purposes Only                ║
║     ⚠️  Use at your own risk!                ║
╚══════════════════════════════════════════════╝
        """
        print(banner)
        self.logger.info("Bot started")
        self.logger.info(f"Mode: {self.get_mode_name()}")
        self.logger.info(f"Video URL: {self.config['video_url']}")
    
    def get_mode_name(self):
        """Get human-readable mode name."""
        modes = {
            1: "Views",
            2: "Hearts/Likes",
            3: "Views + Hearts (Not implemented)",
            4: "Followers"
        }
        return modes.get(self.config['bot_mode'], "Unknown")
    
    def print_stats(self):
        """Print bot statistics."""
        runtime = datetime.now() - self.stats['start_time']
        self.logger.info("=" * 50)
        self.logger.info("Bot Statistics:")
        self.logger.info(f"Runtime: {runtime}")
        self.logger.info(f"Views delivered: {self.stats['views_delivered']}")
        self.logger.info(f"Hearts delivered: {self.stats['hearts_delivered']}")
        self.logger.info(f"Followers delivered: {self.stats['followers_delivered']}")
        self.logger.info(f"Errors: {self.stats['errors']}")
        self.logger.info("=" * 50)
    
    def run(self):
        """Main bot execution."""
        try:
            self.print_banner()
            self.setup_driver()
            
            # Navigate to target site
            self.logger.info(f"Navigating to {self.config['target_site']}")
            self.driver.get(self.config['target_site'])
            
            # Execute based on mode
            mode = self.config['bot_mode']
            if mode == 1:
                self.views_loop()
            elif mode == 2:
                self.hearts_loop()
            elif mode == 3:
                self.logger.warning("Combined mode not yet implemented")
            elif mode == 4:
                self.followers_loop()
            else:
                self.logger.error(f"Invalid bot mode: {mode}")
                
        except KeyboardInterrupt:
            self.logger.info("Bot stopped by user")
        except Exception as e:
            self.logger.error(f"Fatal error: {e}")
        finally:
            self.cleanup()
    
    def cleanup(self):
        """Cleanup resources."""
        self.print_stats()
        if self.driver:
            self.driver.quit()
            self.logger.info("WebDriver closed")


if __name__ == "__main__":
    bot = TikTokBot()
    bot.run()
