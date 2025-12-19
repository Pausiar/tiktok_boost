"""
TikTok Bot Enhanced - Modern Selenium 4 Implementation
Author: Enhanced version for educational purposes
Warning: Using this bot violates TikTok's Terms of Service
"""

import json
import logging
import sys
import time
from datetime import datetime
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException


class TikTokBot:
    def __init__(self, config_path='config.json'):
        """Initialize the TikTok bot with configuration"""
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
        """Load configuration from JSON file"""
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"❌ Config file '{config_path}' not found!")
            print("📝 Creating default config.json...")
            default_config = {
                "video_url": "https://www.tiktok.com/@username/video/1234567890",
                "bot_mode": 1,
                "chromedriver_path": "chromedriver",
                "headless": False,
                "max_retries": 3,
                "base_wait_time": 10,
                "target_site": "https://vipto.de/"
            }
            with open(config_path, 'w') as f:
                json.dump(default_config, f, indent=4)
            print("✅ Default config created. Please edit config.json and run again.")
            sys.exit(1)
    
    def setup_logging(self):
        """Configure logging to file and console"""
        log_format = '%(asctime)s - %(levelname)s - %(message)s'
        logging.basicConfig(
            level=logging.INFO,
            format=log_format,
            handlers=[
                logging.FileHandler('tiktok_bot.log'),
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def setup_driver(self):
        """Initialize Chrome WebDriver with options"""
        self.logger.info("🔧 Setting up Chrome WebDriver...")
        chrome_options = webdriver.ChromeOptions()
        
        if self.config.get('headless', False):
            chrome_options.add_argument('--headless')
            self.logger.warning("⚠️  Running in headless mode - captcha solving may fail")
        
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        try:
            driver_path = self.config.get('chromedriver_path', 'chromedriver')
            self.driver = webdriver.Chrome(driver_path, options=chrome_options)
            self.logger.info("✅ WebDriver initialized successfully")
        except WebDriverException as e:
            self.logger.error(f"❌ Failed to initialize WebDriver: {e}")
            self.logger.error("💡 Make sure ChromeDriver is installed and path is correct")
            sys.exit(1)
    
    def wait_for_element(self, by, value, timeout=20):
        """Wait for element to be present and return it"""
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by, value))
            )
            return element
        except TimeoutException:
            self.logger.warning(f"⏰ Timeout waiting for element: {value}")
            return None
    
    def safe_click(self, by, value, timeout=20):
        """Safely click an element with wait"""
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable((by, value))
            )
            element.click()
            return True
        except (TimeoutException, NoSuchElementException) as e:
            self.logger.warning(f"⚠️  Could not click element: {value}")
            return False
    
    def print_banner(self):
        """Print startup banner"""
        banner = """
╔════════════════════════════════════════╗
║     TikTok Bot Enhanced v2.0          ║
║     Modern Selenium Implementation     ║
╚════════════════════════════════════════╝
        """
        print(banner)
        print(f"⚠️  WARNING: This violates TikTok ToS!")
        print(f"🎯 Mode: {self.get_mode_name()}")
        print(f"🎬 Video: {self.config['video_url']}")
        print(f"🌐 Target: {self.config['target_site']}")
        print("=" * 50)
    
    def get_mode_name(self):
        """Get human-readable mode name"""
        modes = {1: "Views", 2: "Hearts", 3: "Views + Hearts", 4: "Followers"}
        return modes.get(self.config['bot_mode'], "Unknown")
    
    def print_stats(self):
        """Print current statistics"""
        runtime = datetime.now() - self.stats['start_time']
        print("\n" + "=" * 50)
        print("📊 STATISTICS")
        print(f"⏱️  Runtime: {runtime}")
        print(f"👁️  Views: {self.stats['views_delivered']}")
        print(f"❤️  Hearts: {self.stats['hearts_delivered']}")
        print(f"👥 Followers: {self.stats['followers_delivered']}")
        print(f"❌ Errors: {self.stats['errors']}")
        print("=" * 50 + "\n")
    
    def loop_views(self):
        """Main loop for views automation"""
        self.logger.info("🚀 Starting Views automation...")
        retry_count = 0
        max_retries = self.config.get('max_retries', 3)
        
        while True:
            try:
                time.sleep(self.config.get('base_wait_time', 10))
                
                # Click views button
                if not self.safe_click(By.XPATH, "/html/body/div[4]/div[1]/div[3]/div/div[4]/div/button"):
                    self.logger.warning("🔄 Captcha not solved or button not found. Refreshing...")
                    self.driver.refresh()
                    retry_count += 1
                    if retry_count >= max_retries:
                        self.logger.error("❌ Max retries reached. Exiting...")
                        break
                    continue
                
                retry_count = 0
                time.sleep(2)
                
                # Enter video URL
                url_input = self.driver.find_element(By.XPATH, "//*[@id='sid4']/div/div/div/form/div/input")
                url_input.clear()
                url_input.send_keys(self.config['video_url'])
                time.sleep(1)
                
                # Click search
                self.safe_click(By.XPATH, "//*[@id='sid4']/div/div/div/form/div/div/button")
                time.sleep(2)
                
                # Submit for views
                self.safe_click(By.XPATH, "//*[@id='c2VuZC9mb2xsb3dlcnNfdGlrdG9V']/div[1]/div/form/button")
                
                self.stats['views_delivered'] += 1000
                self.logger.info(f"✅ Views delivered! Total: {self.stats['views_delivered']}")
                
                self.driver.refresh()
                time.sleep(55)
                
                if self.stats['views_delivered'] % 5000 == 0:
                    self.print_stats()
                    
            except Exception as e:
                self.logger.error(f"❌ Error in views loop: {e}")
                self.stats['errors'] += 1
                self.driver.refresh()
                time.sleep(10)
    
    def loop_hearts(self):
        """Main loop for hearts automation"""
        self.logger.info("🚀 Starting Hearts automation...")
        
        while True:
            try:
                time.sleep(10)
                
                if not self.safe_click(By.XPATH, "/html/body/div[4]/div[1]/div[3]/div/div[2]/div/button"):
                    self.logger.warning("🔄 Refreshing page...")
                    self.driver.refresh()
                    continue
                
                time.sleep(2)
                
                url_input = self.driver.find_element(By.XPATH, "/html/body/div[4]/div[3]/div/div/div/form/div/input")
                url_input.clear()
                url_input.send_keys(self.config['video_url'])
                time.sleep(1)
                
                self.safe_click(By.XPATH, "/html/body/div[4]/div[3]/div/div/div/form/div/div/button")
                time.sleep(10)
                
                self.safe_click(By.XPATH, "/html/body/div[4]/div[3]/div/div/div/div/div[1]/div/form/button")
                time.sleep(10)
                
                try:
                    hearts_text = self.driver.find_element(By.XPATH, '//*[@id="c2VuZE9nb2xsb3dlcnNfdGlrdG9r"]/span').text
                    self.logger.info(f"❤️  {hearts_text} delivered!")
                    self.stats['hearts_delivered'] += 1
                except:
                    pass
                
                time.sleep(155)
                self.driver.refresh()
                time.sleep(200)
                
            except Exception as e:
                self.logger.error(f"❌ Error in hearts loop: {e}")
                self.stats['errors'] += 1
                self.driver.refresh()
                time.sleep(355)
    
    def loop_followers(self):
        """Main loop for followers automation"""
        self.logger.info("🚀 Starting Followers automation...")
        wait_time = 660  # 11 minutes
        
        while True:
            try:
                time.sleep(20)
                
                if not self.safe_click(By.XPATH, "/html/body/div[4]/div[1]/div[3]/div/div[1]/div/button"):
                    self.logger.warning("🔄 Refreshing page...")
                    self.driver.refresh()
                    continue
                
                time.sleep(20)
                
                url_input = self.driver.find_element(By.XPATH, "/html/body/div[4]/div[2]/div/div/div/form/div/input")
                url_input.clear()
                url_input.send_keys(self.config['video_url'])
                time.sleep(2)
                
                self.safe_click(By.XPATH, "//*[@id='sid']/div/div/div/form/div/div/button")
                time.sleep(20)
                
                self.safe_click(By.XPATH, "//*[@id='c2VuZF9mb2xsb3dlcnNfdGlrdG9r']/div[1]/div/form/button")
                
                self.stats['followers_delivered'] += 1
                self.logger.info(f"✅ Followers delivered! Total: {self.stats['followers_delivered']}")
                
                time.sleep(wait_time / 3)
                self.driver.refresh()
                time.sleep(wait_time / 3 * 2)
                
            except Exception as e:
                self.logger.error(f"❌ Error in followers loop: {e}")
                self.stats['errors'] += 1
                self.driver.refresh()
                time.sleep(wait_time)
    
    def run(self):
        """Main execution method"""
        self.print_banner()
        self.setup_driver()
        
        try:
            self.logger.info(f"🌐 Navigating to {self.config['target_site']}")
            self.driver.get(self.config['target_site'])
            
            mode = self.config['bot_mode']
            
            if mode == 1:
                self.loop_views()
            elif mode == 2:
                self.loop_hearts()
            elif mode == 4:
                self.loop_followers()
            else:
                self.logger.error(f"❌ Invalid bot mode: {mode}")
                
        except KeyboardInterrupt:
            self.logger.info("\n⏹️  Bot stopped by user")
            self.print_stats()
        except Exception as e:
            self.logger.error(f"❌ Fatal error: {e}")
        finally:
            if self.driver:
                self.driver.quit()
                self.logger.info("🔒 Browser closed")


if __name__ == "__main__":
    bot = TikTokBot()
    bot.run()
