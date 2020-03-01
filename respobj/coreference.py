# -*- coding: utf-8; -*-
from dataclasses import dataclass, field
from typing import List

# エンティティオブジェクト
@dataclass
class Referent:
    # エンティティのID
    referent_id: int
    # エンティティが含まれる文の番号
    sentence_id: int
    # エンティティの開始形態素番号
    token_id_from: int
    # エンティティの終了形態素番号
    token_id_to: int
    # 対象の照応詞
    form: str

# 照応解析情報オブジェクト
@dataclass
class Representative:
    # 照応解析情報ID
    representative_id: int
    # エンティティオブジェクトの配列
    referents: List[Referent] = field(default_factory=list)

# 照応解析結果オブジェクト
@dataclass
class Result:
    # 照応解析情報オブジェクトの配列
    coreference: List[Representative] = field(default_factory=list)
    # 解析対象文の各文を形態素解析して得られた表記の配列
    tokens: List[List[str]] = field(default_factory=list)

# レスポンス
@dataclass
class Coreference:
    # 照応解析結果オブジェクト
    result: Result
    # ステータスコード 0:OK, >0:エラー
    status: int
    # エラーメッセージ
    message: str