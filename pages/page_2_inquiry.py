import streamlit as st
import datetime

with st.form(key='profile_form'):
    # text box
    name = st.text_input('名前')
    address = st.text_input('住所')
    password = st.text_input('password', type='password')

    # select box
    age_category = st.selectbox(
        '年齢層',
        ('子供(18歳未満)', '大人(18歳以上)')
    )

    # select radio button
    sex = st.radio(
        '性別',
        ('男', '女')
    )

    # multi select radio button
    hobby = st.multiselect(
        '趣味',
        ('スポーツ', '読書', 'プログラミング', '料理', 'マイクラ', 'パパ')
    )

    # check box
    mail_subscribe = st.checkbox('パパの腰を心配する？')

    # slider
    height = st.slider('身長', min_value=110, max_value=210)

    # data
    start_data = st.date_input(
        '開始日', 
        datetime.date(2020, 7, 1)
    )

    # color picker
    color = st.color_picker('テーマカラー', '#00f900')

    # button
    submit_btn = st.form_submit_button('送信')
    cancel_btn = st.form_submit_button('キャンセル')


    if submit_btn:
        st.text(f'ようこそ{name}さん、{age_category}/{sex}を確認できたので、{address}に送りました')
        st.text(f'{",".join(hobby)}はいい趣味ですね！')
