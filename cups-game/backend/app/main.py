from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.game.engine import GameManager

app = FastAPI()
game = GameManager()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class StartRequest(BaseModel):
    player_name: str

@app.post("/api/start")
def start_game(req: StartRequest):
    return game.start_game(req.player_name)

@app.post("/api/turn")
def next_turn():
    return game.resolve_turn()

@app.post("/api/reset")
def reset_game():
    game.reset()
    return game.serialize_state()

@app.get("/api/state")
def get_state():
    return game.serialize_state()

@app.get("/api/winner")
def winner():
    return game.get_winner()
