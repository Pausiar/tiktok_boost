"""
Bot Manager - Handles bot lifecycle and execution
"""

import asyncio
from typing import Dict, Optional
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BotSession:
    """Represents a single bot session"""
    
    def __init__(self, session_id: str, config: dict, ws_manager):
        self.session_id = session_id
        self.config = config
        self.ws_manager = ws_manager
        self.driver = None
        self.status = "initializing"
        self.stats = {
            'views_delivered': 0,
            'hearts_delivered': 0,
            'followers_delivered': 0,
            'errors': 0,
            'cycles_completed': 0
        }
        self.start_time = datetime.now()
        self.task = None
        self.should_stop = False
        
    async def send_update(self, message: str, level: str = "info"):
        """Send update through WebSocket"""
        await self.ws_manager.send_message(self.session_id, {
            "type": "log",
            "level": level,
            "message": message,
            "timestamp": datetime.now().isoformat(),
            "stats": self.stats
        })
    
    def setup_driver(self):
        """Initialize Chrome WebDriver"""
        try:
            chrome_options = webdriver.ChromeOptions()
            
            # Essential options for running in server environment
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--disable-blink-features=AutomationControlled')
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            
            self.driver = webdriver.Chrome(options=chrome_options)
            self.driver.maximize_window()
            logger.info(f"Session {self.session_id}: WebDriver initialized")
            
        except Exception as e:
            logger.error(f"Session {self.session_id}: Failed to initialize WebDriver: {e}")
            raise
    
    async def run(self):
        """Main bot execution loop"""
        try:
            self.status = "running"
            await self.send_update("🚀 Bot iniciado", "info")
            
            self.setup_driver()
            await self.send_update("✅ Navegador inicializado", "success")
            
            # Navigate to target site
            self.driver.get("https://vipto.de/")
            await self.send_update(f"🌐 Conectado a vipto.de", "info")
            
            mode = self.config['bot_mode']
            
            if mode == 1:
                await self.views_loop()
            elif mode == 2:
                await self.hearts_loop()
            elif mode == 4:
                await self.followers_loop()
            else:
                raise ValueError(f"Invalid bot mode: {mode}")
                
        except Exception as e:
            self.status = "error"
            logger.error(f"Session {self.session_id}: Error in bot execution: {e}")
            await self.send_update(f"❌ Error: {str(e)}", "error")
            self.stats['errors'] += 1
            
        finally:
            self.cleanup()
    
    async def views_loop(self):
        """Views automation loop"""
        retry_count = 0
        max_retries = self.config.get('max_retries', 3)
        
        while not self.should_stop and retry_count < max_retries:
            try:
                await asyncio.sleep(self.config.get('base_wait_time', 10))
                
                # Click views button
                await self.send_update("👁️ Iniciando proceso de views...", "info")
                
                views_btn = WebDriverWait(self.driver, 20).until(
                    EC.element_to_be_clickable((By.XPATH, "/html/body/div[4]/div[1]/div[3]/div/div[4]/div/button"))
                )
                views_btn.click()
                
                # Enter video URL
                await asyncio.sleep(2)
                url_input = WebDriverWait(self.driver, 20).until(
                    EC.element_to_be_clickable((By.XPATH, "//*[@id='sid4']/div/div/div/form/div/input"))
                )
                url_input.clear()
                url_input.send_keys(self.config['video_url'])
                
                # Submit
                await asyncio.sleep(1)
                search_btn = self.driver.find_element(By.XPATH, "//*[@id='sid4']/div/div/div/form/div/div/button")
                search_btn.click()
                
                await asyncio.sleep(2)
                submit_btn = self.driver.find_element(By.XPATH, "//*[@id='c2VuZC9mb2xsb3dlcnNfdGlrdG9V']/div[1]/div/form/button")
                submit_btn.click()
                
                self.stats['views_delivered'] += 1000
                self.stats['cycles_completed'] += 1
                await self.send_update(f"✅ 1000 views entregados! Total: {self.stats['views_delivered']}", "success")
                
                # Wait before next cycle
                await asyncio.sleep(55)
                self.driver.refresh()
                retry_count = 0
                
            except Exception as e:
                retry_count += 1
                self.stats['errors'] += 1
                await self.send_update(f"⚠️ Error en cycle de views (intento {retry_count}/{max_retries})", "warning")
                logger.error(f"Views loop error: {e}")
                await asyncio.sleep(5)
                self.driver.refresh()
    
    async def hearts_loop(self):
        """Hearts automation loop"""
        retry_count = 0
        max_retries = self.config.get('max_retries', 3)
        
        while not self.should_stop and retry_count < max_retries:
            try:
                await asyncio.sleep(self.config.get('base_wait_time', 10))
                
                await self.send_update("❤️ Iniciando proceso de hearts...", "info")
                
                # Click hearts button
                hearts_btn = WebDriverWait(self.driver, 20).until(
                    EC.element_to_be_clickable((By.XPATH, "/html/body/div[4]/div[1]/div[3]/div/div[2]/div/button"))
                )
                hearts_btn.click()
                
                # Enter video URL
                await asyncio.sleep(2)
                url_input = WebDriverWait(self.driver, 20).until(
                    EC.element_to_be_clickable((By.XPATH, "/html/body/div[4]/div[3]/div/div/div/form/div/input"))
                )
                url_input.clear()
                url_input.send_keys(self.config['video_url'])
                
                # Submit
                await asyncio.sleep(1)
                search_btn = self.driver.find_element(By.XPATH, "/html/body/div[4]/div[3]/div/div/div/form/div/div/button")
                search_btn.click()
                
                await asyncio.sleep(10)
                submit_btn = self.driver.find_element(By.XPATH, "/html/body/div[4]/div[3]/div/div/div/div/div[1]/div/form/button")
                submit_btn.click()
                
                self.stats['hearts_delivered'] += 1
                self.stats['cycles_completed'] += 1
                await self.send_update(f"✅ Hearts entregados! Total: {self.stats['hearts_delivered']}", "success")
                
                # Wait before next cycle
                await asyncio.sleep(155)
                self.driver.refresh()
                await asyncio.sleep(200)
                retry_count = 0
                
            except Exception as e:
                retry_count += 1
                self.stats['errors'] += 1
                await self.send_update(f"⚠️ Error en cycle de hearts (intento {retry_count}/{max_retries})", "warning")
                logger.error(f"Hearts loop error: {e}")
                await asyncio.sleep(355)
                self.driver.refresh()
    
    async def followers_loop(self):
        """Followers automation loop"""
        retry_count = 0
        max_retries = self.config.get('max_retries', 3)
        
        while not self.should_stop and retry_count < max_retries:
            try:
                await asyncio.sleep(20)
                
                await self.send_update("👥 Iniciando proceso de followers...", "info")
                
                # Click followers button
                followers_btn = WebDriverWait(self.driver, 20).until(
                    EC.element_to_be_clickable((By.XPATH, "/html/body/div[4]/div[1]/div[3]/div/div[1]/div/button"))
                )
                followers_btn.click()
                
                # Enter video URL
                await asyncio.sleep(20)
                url_input = WebDriverWait(self.driver, 20).until(
                    EC.element_to_be_clickable((By.XPATH, "/html/body/div[4]/div[2]/div/div/div/form/div/input"))
                )
                url_input.clear()
                url_input.send_keys(self.config['video_url'])
                
                # Submit
                await asyncio.sleep(2)
                search_btn = self.driver.find_element(By.XPATH, "//*[@id='sid']/div/div/div/form/div/div/button")
                search_btn.click()
                
                await asyncio.sleep(20)
                submit_btn = self.driver.find_element(By.XPATH, "//*[@id='c2VuZF9mb2xsb3dlcnNfdGlrdG9r']/div[1]/div/form/button")
                submit_btn.click()
                
                self.stats['followers_delivered'] += 1
                self.stats['cycles_completed'] += 1
                await self.send_update(f"✅ Followers entregados! Total: {self.stats['followers_delivered']}", "success")
                
                # Wait before next cycle (11 minutes)
                await asyncio.sleep(660)
                self.driver.refresh()
                retry_count = 0
                
            except Exception as e:
                retry_count += 1
                self.stats['errors'] += 1
                await self.send_update(f"⚠️ Error en cycle de followers (intento {retry_count}/{max_retries})", "warning")
                logger.error(f"Followers loop error: {e}")
                await asyncio.sleep(660)
                self.driver.refresh()
    
    def stop(self):
        """Stop the bot session"""
        self.should_stop = True
        self.status = "stopping"
    
    def cleanup(self):
        """Cleanup resources"""
        if self.driver:
            try:
                self.driver.quit()
                logger.info(f"Session {self.session_id}: WebDriver closed")
            except:
                pass
        self.status = "stopped"


class BotManager:
    """Manages multiple bot sessions"""
    
    def __init__(self):
        self.sessions: Dict[str, BotSession] = {}
    
    async def start_bot(self, session_id: str, config: dict, ws_manager):
        """Start a new bot session"""
        if session_id in self.sessions:
            raise ValueError(f"Session {session_id} already exists")
        
        session = BotSession(session_id, config, ws_manager)
        self.sessions[session_id] = session
        
        # Run bot in background task
        session.task = asyncio.create_task(session.run())
        
        logger.info(f"Started bot session: {session_id}")
        return session
    
    async def stop_bot(self, session_id: str) -> bool:
        """Stop a bot session"""
        session = self.sessions.get(session_id)
        if not session:
            return False
        
        session.stop()
        
        if session.task:
            session.task.cancel()
        
        logger.info(f"Stopped bot session: {session_id}")
        return True
    
    def get_status(self, session_id: str) -> Optional[dict]:
        """Get session status"""
        session = self.sessions.get(session_id)
        if not session:
            return None
        
        mode_names = {1: "Views", 2: "Hearts", 4: "Followers"}
        
        return {
            "session_id": session_id,
            "status": session.status,
            "mode": mode_names.get(session.config['bot_mode'], "Unknown"),
            "stats": session.stats,
            "start_time": session.start_time.isoformat()
        }
    
    def list_sessions(self) -> list:
        """List all sessions"""
        return [
            {
                "session_id": sid,
                "status": session.status,
                "start_time": session.start_time.isoformat()
            }
            for sid, session in self.sessions.items()
        ]
    
    def get_active_count(self) -> int:
        """Get count of active sessions"""
        return len([s for s in self.sessions.values() if s.status == "running"])
    
    async def cleanup_all(self) -> int:
        """Stop all sessions and cleanup"""
        count = 0
        for session_id in list(self.sessions.keys()):
            if await self.stop_bot(session_id):
                count += 1
        self.sessions.clear()
        return count
