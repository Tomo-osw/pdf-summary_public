import sys
from pdfminer.high_level import extract_text
import openai
import os
from django.conf import settings

openai.organization = "***"
openai.api_key = "***"

def pdf_s(filename, summary_number):
    input_path = settings.MEDIA_ROOT + '/pdf/' + filename
    text = extract_text(input_path)
    response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo-16k",
    messages=[
        {"role": "system", "content": f"内容を{summary_number}文字に要約してください"},
        {"role": "user", "content": text}
        ],
    #max_tokens=500,  # 生成するトークンの最大数
    n=1,  # 生成するレスポンスの数
    stop=None,  # 停止トークンの設定
    temperature=0.7,  # 生成時のランダム性の制御
    top_p=1  # トークン選択時の確率閾値
    )
    return response.choices[0]["message"]["content"].strip()