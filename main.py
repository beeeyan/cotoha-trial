# -*- coding:utf-8 -*-

import os
import json
import configparser
import codecs
import marshmallow_dataclass
import cotoha_function as cotoha
from aozora_scraping import get_aocora_sentence
from respobj.coreference import Coreference
from respobj.test import LogItem, Referent
import time



if __name__ == '__main__':
    # ソースファイルの場所取得
    APP_ROOT = os.path.dirname(os.path.abspath( __file__)) + "/"

    # 設定値取得
    config = configparser.ConfigParser()
    config.read(APP_ROOT + "config.ini")
    CLIENT_ID = config.get("COTOHA API", "Developer Client id")
    CLIENT_SECRET = config.get("COTOHA API", "Developer Client secret")
    DEVELOPER_API_BASE_URL = config.get("COTOHA API", "Developer API Base URL")
    ACCESS_TOKEN_PUBLISH_URL = config.get("COTOHA API", "Access Token Publish URL")

    # 定数
    max_word = 1800
    max_call_api_count = 6
    max_elements_count = 20

    # COTOHA APIインスタンス生成
    cotoha_api = cotoha.CotohaApi(CLIENT_ID, CLIENT_SECRET, DEVELOPER_API_BASE_URL, ACCESS_TOKEN_PUBLISH_URL)

    # 例文
    sentence = "太郎は友人です。彼は焼き肉を食べた。"
    # 夏目漱石「心」
    sentences = get_aocora_sentence('https://www.aozora.gr.jp/cards/000148/files/773_14560.html')

    # 構文解析API実行
    #result = cotoha_api.userAttribute(sentence)

    # start_index = 1
    # end_index = 1
    # call_api_count = 1
    # temp_sentences = sentences[start_index:end_index]
    # elements_count = end_index - start_index
    # while(end_index < len(sentences) and call_api_count <= max_call_api_count):
    #     length_sentences = len(''.join(temp_sentences))
    #     print(length_sentences)
    #     if(length_sentences < max_word and elements_count < max_elements_count and end_index < len(sentences)):
    #         end_index += 1
    #     else:
    #         input_sentences = sentences[start_index:end_index-1]
    #         print(str(call_api_count) + '回目の通信')
    #         result = cotoha_api.coreference(input_sentences)
    #         print(result)
    #         call_api_count += 1
    #         start_index = end_index
    #     temp_sentences = sentences[start_index:end_index]
    #     elements_count = end_index - start_index

    #バインドのテスト部
    input_sentences = sentences[1:3]
    result = cotoha_api.coreference(input_sentences)
    result_formated = codecs.decode(json.dumps(result),'unicode-escape')
    print(result_formated)
    test = marshmallow_dataclass.class_schema( Coreference )().loads(result_formated)
    print(test)
    

    # 出力結果を見やすく整形
    # result_formated = json.dumps(result, indent=4, separators=(',', ': '))
    # print (codecs.decode(result_formated, 'unicode-escape'))