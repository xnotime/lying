from dataclasses import dataclass
from random import randrange
import time
import typing as t

@dataclass
class Player:
    ne: str
    role: Speaker | Judge
    time_to_submit: int = 15

@dataclass
class Speaker:
    wlink: str
    desc: str | None = None

@dataclass
class Judge:
    pass

class Game:
    code: str
    players: t.List[Player]
    chosen: int | None # None if game hasn't started yet
    start_time: float
    live: bool

    def __init__(self, code: str, judge_nick_enc: str):
        self.code = code
        self.players = [
            Player(judge_nick_enc, Judge()),
        ]
        self.chosen = None
        self.live = False
    
    def add_player(self, new_player: Player):
        self.players.append(new_player)
    
    def start_game(self):
        # Choose a speaker who will tell the truth
        choose = lambda: randrange(0, len(self.players))
        self.chosen = choose()
        while not isinstance(self.players[self.chosen].role, Speaker):
            self.chosen = choose()
        self.start_time = time.time()
    
    def chosen_article(self):
        if self.chosen is None:
            return None
        return self.players[self.chosen].role.wlink
    
    def status(self, ne: str):
        if self.chosen is None:
            return '@not-started'
        if self.live:
            return '@live'
        now = time.time()
        time_left = self.get_time() - int(now - self.start_time)
        if time_left <= 0:
            self.live = True
        return f'{time_left}s left'
    
    def attach_desc(self, ne: str, desc: str):
        idx = [
            i for i, spkr in enumerate(self.players) if spkr.ne == ne
        ][0]
        self.speakers[idx].desc = desc
        print(desc)
    
    def speakers_json(self):
        return {
            'list': [
                {
                    'ne': spkr.ne,
                    'desc': spkr.desc,
                } for spkr in self.players
                if isinstance(spkr, Speaker)
            ]
        }
    
    def guess(self, ne: str):
        return self.players[self.chosen].ne == ne
    
    def get_time(self, ne: str):
        return [
            spkr.time_to_submit
            for spkr in self.players
            if isinstance(spkr.role, Speaker)
        ][0]
