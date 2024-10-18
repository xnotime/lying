from dataclasses import dataclass
from random import randrange
import time
import typing as t

@dataclass
class Speaker:
    ne: str
    wlink: str
    desc: str | None = None

class Game:
    code: str
    judge: str
    speakers: t.List[Speaker]
    chosen: int | None # None if game hasn't started yet
    start_time: float
    live: bool

    def __init__(self, code: str, judge_nick_enc: str):
        self.code = code
        self.judge = judge_nick_enc
        self.speakers = []
        self.chosen = None
        self.time_left = 10
        self.live = False
    
    def add_speaker(self, new_speaker: Speaker):
        self.speakers.append(new_speaker)
    
    def start_game(self):
        # Choose a speaker who will tell the truth
        self.chosen = randrange(0, len(self.speakers))
        self.start_time = time.time()
    
    def chosen_article(self):
        if self.chosen is None:
            return None
        return self.speakers[self.chosen].wlink
    
    def status(self):
        if self.chosen is None:
            return '@not-started'
        if self.live:
            return '@live'
        now = time.time()
        time_left = 10 - int(now - self.start_time)
        if time_left <= 0:
            self.live = True
        return f'{time_left}s left'
    
    def attach_desc(self, ne: str, desc: str):
        idx = [
            i for i, spkr in enumerate(self.speakers) if spkr.ne == ne
        ][0]
        self.speakers[idx].desc = desc
        print(desc)
