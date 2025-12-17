"""
TikTok Bot - FastAPI Backend
Main API endpoint handler with WebSocket support
"""

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, HttpUrl
from typing import Optional, Dict, List
import asyncio
import uuid
from datetime import datetime

from bot_manager import BotManager
from websocket_handler import ConnectionManager

app = FastAPI(
    title="TikTok Bot API",
    description="Backend API for TikTok automation bot",
    version="2.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your GitHub Pages domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Managers
bot_manager = BotManager()
ws_manager = ConnectionManager()

# Models
class BotConfig(BaseModel):
    video_url: HttpUrl
    bot_mode: int  # 1=Views, 2=Hearts, 4=Followers
    max_retries: Optional[int] = 3
    base_wait_time: Optional[int] = 10
    headless: Optional[bool] = True

class BotStatus(BaseModel):
    session_id: str
    status: str  # running, stopped, error
    mode: str
    stats: Dict
    start_time: str

class BotResponse(BaseModel):
    session_id: str
    message: str
    status: str


# Root endpoint
@app.get("/")
async def root():
    return {
        "name": "TikTok Bot API",
        "version": "2.0.0",
        "status": "running",
        "endpoints": {
            "start_bot": "/api/bot/start",
            "stop_bot": "/api/bot/stop/{session_id}",
            "status": "/api/bot/status/{session_id}",
            "websocket": "/ws/{session_id}"
        }
    }


# Health check
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "active_sessions": bot_manager.get_active_count(),
        "timestamp": datetime.now().isoformat()
    }


# Start bot
@app.post("/api/bot/start", response_model=BotResponse)
async def start_bot(config: BotConfig):
    """Start a new bot session"""
    try:
        # Generate unique session ID
        session_id = str(uuid.uuid4())
        
        # Validate bot mode
        if config.bot_mode not in [1, 2, 4]:
            raise HTTPException(status_code=400, detail="Invalid bot_mode. Must be 1, 2, or 4")
        
        # Start bot in background
        await bot_manager.start_bot(
            session_id=session_id,
            config=config.dict(),
            ws_manager=ws_manager
        )
        
        return BotResponse(
            session_id=session_id,
            message="Bot started successfully",
            status="running"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Stop bot
@app.post("/api/bot/stop/{session_id}")
async def stop_bot(session_id: str):
    """Stop a running bot session"""
    try:
        success = await bot_manager.stop_bot(session_id)
        
        if not success:
            raise HTTPException(status_code=404, detail="Session not found")
        
        return {
            "session_id": session_id,
            "message": "Bot stopped successfully",
            "status": "stopped"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Get bot status
@app.get("/api/bot/status/{session_id}", response_model=BotStatus)
async def get_bot_status(session_id: str):
    """Get status of a bot session"""
    status = bot_manager.get_status(session_id)
    
    if not status:
        raise HTTPException(status_code=404, detail="Session not found")
    
    return status


# List all sessions
@app.get("/api/bot/sessions")
async def list_sessions():
    """Get all active bot sessions"""
    return {
        "active_sessions": bot_manager.get_active_count(),
        "sessions": bot_manager.list_sessions()
    }


# WebSocket endpoint for real-time updates
@app.websocket("/ws/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str):
    """WebSocket connection for real-time bot updates"""
    await ws_manager.connect(session_id, websocket)
    
    try:
        while True:
            # Keep connection alive and receive client messages
            data = await websocket.receive_text()
            
            # Client can send commands through WebSocket
            if data == "ping":
                await websocket.send_json({"type": "pong"})
                
    except WebSocketDisconnect:
        ws_manager.disconnect(session_id)


# Cleanup endpoint (admin only - add authentication in production)
@app.post("/api/admin/cleanup")
async def cleanup_sessions():
    """Stop all running bots and cleanup"""
    count = await bot_manager.cleanup_all()
    return {
        "message": f"Cleaned up {count} sessions",
        "status": "success"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
