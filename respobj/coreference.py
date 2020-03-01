# -*- coding: utf-8; -*-
from dataclasses import dataclass, field
from typing import List

@dataclass
class Referent:
    referent_id: int
    sentence_id: int
    token_id_from: int
    token_id_to: int
    form: str

@dataclass
class Representative:
    representative_id: int
    referents: List[Referent] = field(default_factory=list)

@dataclass
class Result:
    coreference: List[Representative] = field(default_factory=list)
    tokens: List[List[str]] = field(default_factory=list)

@dataclass
class Coreference:
    result: Result
    status: int
    message: str