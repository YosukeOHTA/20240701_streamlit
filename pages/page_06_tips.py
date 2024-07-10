
# https://qiita.com/tamura__246/items/366b5581c03dd74f4508
# https://zenn.dev/dataheroes/articles/2eae5a5ad92534

import pandas as pd
import streamlit as st

data_df = pd.DataFrame(
    {
        # サンプルデータ（URL）
        "apps": [
            "https://roadmap.streamlit.app",
            "https://extras.streamlit.app",
            "https://issues.streamlit.app",
            "https://30days.streamlit.app",
        ],
    }
)

st.dataframe(
    data_df,
    column_config={
        "apps": st.column_config.LinkColumn(
            # 表示するカラム名
            "アプリ",
            # 表示データのテキスト
             display_text="https://(.*?)\.streamlit\.app"
        )
    },
)

