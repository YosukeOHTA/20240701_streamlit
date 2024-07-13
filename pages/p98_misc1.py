# https://qiita.com/tamura__246/items/366b5581c03dd74f4508

import streamlit as st
import pandas as pd

st.set_page_config(page_title="メインページ", page_icon='../data/P_20160712_093622.jpg')
st.title("Multiple OSS Access Log Analyzer")

uploaded_file = st.file_uploader("アクセスログをアップロードしてください。")
if uploaded_file is not None:
    df = pd.read_csv(
        uploaded_file,
        sep=r'\s(?=(?:[^"]*"[^"]*")*[^"]*$)(?![^\[]*\])',
        engine='python',
        na_values='-',
        header=None)
    st.markdown('### アクセスログ（先頭5件）')
    st.write(df.head(5))


usecols = st.multiselect(
    '何番目の列を解析の対象にしますか？',
    [0, 3, 4, 5, 6],
    [0, 3, 4, 5, 6])
if len(usecols) == 0:
    st.error('解析対象の列が指定されていません。')


help_txt = '''
    以下のフォーマット文字列を解析可能です。詳細については、[公式ページ](https://httpd.apache.org/docs/2.4/ja/mod/mod_log_config.html)を参照して下さい。

    | 列名 | フォーマット文字列 | 説明 | 
    |:-----|:-----:|:-----|
    | Remote Host | `%h` | リモートホスト |
    | Time | `%t` | リクエストを受付けた時刻 | 
    | Request | `\"%r\"` | リクエストの最初の行 | 
    | Status | `%>s` | ステータス | 
    | Size | `%b` | レスポンスのバイト数 | 
    | User Agent | `\"%{User-agent}i\"` | リクエストのUser-agentヘッダの内容 | 
    | Response Time | `%D` または `%T` | リクエストを処理するのにかかった時間 |         
    '''

names = st.multiselect(
    'これらの列を何を意味しますか？',
    ['Remote Host', 'Time', 'Request', 'Status', 'Size', 'User Agent', 'Response Time'],
    'Remote Host', help=help_txt)

my_bar = st.progress(0)
# 　・・・何らかの処理
my_bar.progress(10)
#　・・・何らかの処理
my_bar.progress(20)
#　・・・何らかの処理
#　・・・
my_bar.progress(100)