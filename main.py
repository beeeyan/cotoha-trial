# -*- coding:utf-8 -*-

import os
import json
import configparser
import datetime
import codecs
import cotoha_function as cotoha
from aozora_scraping import get_aocora_sentence
from respobj.coreference import Coreference
from json_to_obj import json_to_coreference



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
    max_call_api_count = 150
    max_elements_count = 20
    # 青空文庫のURL
    aozora_html = 'https://www.aozora.gr.jp/cards/000148/files/773_14560.html'
    # 現在時刻
    now_date = datetime.datetime.today().strftime("%Y%m%d%H%M%S")
    # 元のテキストを保存するファイルのパス（任意）
    origin_txt_path = './result/origin_' + now_date + '.txt'
    # 結果を保存するファイルのパス（任意）
    result_txt_path = './result/converted_' + now_date + '.txt'

    # COTOHA APIインスタンス生成
    cotoha_api = cotoha.CotohaApi(CLIENT_ID, CLIENT_SECRET, DEVELOPER_API_BASE_URL, ACCESS_TOKEN_PUBLISH_URL)

    # 青空文庫のテキストの取得
    sentences = get_aocora_sentence(aozora_html)
    with open(origin_txt_path, mode='a') as f:
        for sentence in sentences:
            f.write(sentence + '\n')

    # 初期値
    start_index = 0
    end_index = 0
    call_api_count = 1
    temp_sentences = sentences[start_index:end_index]
    elements_count = end_index - start_index
    result = []
    print("リクエストする配列の総数" + str(len(sentences)))
    while(end_index <= len(sentences) and call_api_count <= max_call_api_count):
        length_sentences = len(''.join(temp_sentences))
        if(length_sentences < max_word and elements_count < max_elements_count and end_index <= len(sentences)):
            end_index += 1
        else:
            input_sentences = sentences[start_index:end_index - 1]
            print('インデックス : ' + str(start_index) + 'から' + str(end_index) + 'まで')
            print(str(call_api_count) + '回目の通信')
            response = cotoha_api.coreference(input_sentences)
            result.append(json_to_coreference(response))
            call_api_count += 1
            start_index = end_index - 1
        temp_sentences = sentences[start_index:end_index]
        elements_count = end_index - start_index
    
    for obj in result:
        coreferences = obj.result.coreference
        tokens = obj.result.tokens
        for coreference in coreferences:
            anaphor = []
            # coreference内の最初の照応詞を元にする。
            anaphor.append(coreference.referents[0].form)
            for referent in coreference.referents:
                sentence_id = referent.sentence_id
                token_id_from = referent.token_id_from
                token_id_to = referent.token_id_to
                # 後続の処理のためにlistの要素数を変更しないように書き換える。
                anaphor_and_empty = anaphor + ['']*(token_id_to - token_id_from)
                tokens[sentence_id][token_id_from: (token_id_to + 1)] = anaphor_and_empty
        # 変更後の文章をファイルに保存する
        with open(result_txt_path, mode='a') as f:
            for token in tokens:
                line = ''.join(token)
                f.write(line + '\n')
