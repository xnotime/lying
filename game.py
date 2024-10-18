from dataclasses import dataclass
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

    def __init__(self, code: str, judge_nick_enc: str):
        self.code = code
        self.judge = judge_nick_enc
        self.speakers = []
    
    def add_speaker(self, new_speaker: Speaker):
        self.speakers.append(new_speaker)
