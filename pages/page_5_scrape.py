import numpy as np
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import streamlit as st
from  selenium.webdriver.chrome.options import Options

with st.form(key='Library check'):
    st.header('Library check')
    # text box
    libIdList = st.multiselect(
        'Library ID',
        ['9027551499', '9027551502', '9027551510', ],
        ['9027551499', '9027551502', '9027551510', ]
    )
    libPw = st.text_input('Library password')

    # button
    submit_btn = st.form_submit_button('送信')
    cancel_btn = st.form_submit_button('キャンセル')
    if submit_btn:
        if len(libPw)==0:
            st.write('Input password')
        else:
            history1 = np.zeros((0,4))
            col1 = ['userID', 'byDate', 'bookName', 'author',]
            history2 = np.zeros((0,4))
            col2 = ['userID', 'status', 'bookName', 'author',]

            # driver = webdriver.Chrome(service=Service(), options=webdriver.ChromeOptions())
            chrome_options = Options()
            chrome_options.add_argument("--headless")
            driver = webdriver.Chrome(service=Service(), options=chrome_options)

            for libId in libIdList:
                st.write(f'{libId}の確認中')
                driver.get('https://opac.lib.city.yokohama.lg.jp/winj/opac/top.do')
                driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/ul/li/a').click()
                driver.find_element(By.XPATH, '/html/body/div[2]/div/div[1]/div/form/dl/dd[1]/input').send_keys(libId)
                driver.find_element(By.XPATH, '/html/body/div[2]/div/div[1]/div/form/dl/dd[2]/input').send_keys(libPw)
                driver.find_element(By.XPATH, '/html/body/div[2]/div/div[1]/div/form/input').click()
                # Myライブラリ
                driver.find_element(By.XPATH, '/html/body/div[1]/div/div[1]/ul/li[7]/a').click()
                # 貸出中の本
                driver.find_element(By.XPATH, '/html/body/div[2]/div[1]/ul/li[1]/a/dl/dt').click()
                if driver.find_element(By.XPATH, '/html/body/div[2]/div[1]').text != '貸出中の本\n該当するリストが存在しません。':
                    numBooks1 = int(driver.find_element(By.XPATH, '/html/body/div[2]/div[1]/form/div[6]/p').text.split('全')[1].split('件')[0])
                    for i in range(numBooks1):
                        item1 = np.array([
                            libId,
                            driver.find_element(By.XPATH, f'/html/body/div[2]/div[1]/form/ol/li[{str(i+1)}]/div/div[1]/div/p[2]').text.split(':')[2],
                            driver.find_element(By.XPATH, f'/html/body/div[2]/div[1]/form/ol/li[{str(i+1)}]/div/div[1]/h4/span/a/span').text,
                            driver.find_element(By.XPATH, f'/html/body/div[2]/div[1]/form/ol/li[{str(i+1)}]/div/div[1]/div/p[1]').text.split('--')[0].split('／')[0],
                        ])
                        history1 = np.vstack((history1, item1))
                # Myライブラリ
                driver.find_element(By.XPATH, '/html/body/div[1]/div/div[1]/ul/li[7]/a').click()
                # 予約中の本
                driver.find_element(By.XPATH, '/html/body/div[2]/div[1]/ul/li[2]/a/dl/dt').click()
                if driver.find_element(By.XPATH, '/html/body/div[2]/div[1]').text != '予約中の本\n有効予約一覧\n取消済予約一覧\n該当するリストが存在しません。':
                    numBooks2 = int(driver.find_element(By.XPATH, '/html/body/div[2]/div[1]/form/div[5]/p').text.split('全')[1].split('件')[0])
                    for i in range(numBooks2):
                        item2 = np.array([
                            libId,
                            driver.find_element(By.XPATH, f'/html/body/div[2]/div[1]/form/ol/li[{str(i+1)}]/div/div[1]/div/div/p').text.split('(')[-1].split('位')[0],
                            driver.find_element(By.XPATH, f'/html/body/div[2]/div[1]/form/ol/li[{str(i+1)}]/div/div[1]/h4/a/span').text,
                            driver.find_element(By.XPATH, f'/html/body/div[2]/div[1]/form/ol/li[{str(i+1)}]/div/div[1]/div/p[1]').text.split('--')[0].split('／')[0],
                        ])
                        history2 = np.vstack((history2, item2))

                # ログアウト
                driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/ul[1]/li[2]/a').click()
                # トップメニュー
                driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div/a').click()
            driver.close()
            df1 = pd.DataFrame(history1, columns=col1).drop_duplicates()
            # df2 = pd.read_excel(r"D:\OneDrive - yo\YO06_IT_Skill\01_Python\01_Scraping\20220122_libralyBooks\20240120_bookHistory.xlsx")
            # df3 = pd.concat([df1, df2]).drop_duplicates(ignore_index=True)
            # df3.to_excel(r"D:\OneDrive - yo\YO06_IT_Skill\01_Python\01_Scraping\20220122_libralyBooks\20240120_bookHistory.xlsx", index=False)
            df4 = pd.DataFrame(history2, columns=col2)
            for i in df4.index:
                if df4.loc[i, 'status']=='受取館へ回送中  ':
                    df4.loc[i, 'status']='0'
            df4['status'] = df4['status'].astype('int')
            st.subheader('借りている本')
            st.dataframe(df1.sort_values(['byDate', 'userID', 'bookName']))
            st.subheader('予約している本')
            st.dataframe(df4.sort_values(['status', 'bookName', ], ascending=True))

with st.form(key='Otenki check'):
    st.header('Otenki check')
    # button
    submit_btn = st.form_submit_button('送信')
    cancel_btn = st.form_submit_button('キャンセル')
