from dataclasses import dataclass
from random import randrange
import typing as t

@dataclass
class Speaker:
    ne: str
    wlink: str
    desc: str = None

class Game:
    code: str
    judge: str
    speakers: t.List[Speaker]
    chosen: int | None # None if game hasn't started yet

    def __init__(self, code: str, judge_nick_enc: str):
        self.code = code
        self.judge = judge_nick_enc
        self.speakers = []
        self.article = None
    
    def add_speaker(self, new_speaker: Speaker):
        self.speakers.append(new_speaker)
    
    def start_game(self):
        # Choose a speaker who will tell the truth
        self.chosen = randrange(0, len(self.speakers))
        # Only tell the judge the chosen article
        return self.chosen_article()
    
    def chosen_article(self):
        if self.chosen is None:
            return None
        return self.speakers[self.chosen].wlink
