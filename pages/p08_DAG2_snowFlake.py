# https://qiita.com/kanazawayuto/items/f7c8f4657ae004b89694

import json

import pandas as pd

from snowflake.snowpark import Session
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.exceptions import SnowparkSessionException
import streamlit as st


# Sessionの取得
try:
    # Streamlit in Snowflakeで実行する場合
    session = get_active_session()
except SnowparkSessionException:
    # ローカル環境で実行する場合
    with open('./snowflake_connection_parameters.json') as f:
        connection_parameters = json.load(f)
    session = Session.builder.configs(connection_parameters).create() 

def query_dependencies_parent_df(session, object_domain, start_object):
    # Snowflakeから参照元方向へオブジェクトの依存関係を取得
    query_text = f'''
with od as (
    select
        referenced_object_domain,
        referenced_database ||'.'|| referenced_schema ||'.'|| referenced_object_name as referenced_object_fullname,
        referencing_object_domain,
        referencing_database ||'.'|| referencing_schema ||'.'|| referencing_object_name as referencing_object_fullname
    from
        snowflake.account_usage.object_dependencies
    where
        referenced_object_domain in ('{object_domain}')
        and referencing_object_domain in ('{object_domain}')
)
select
    *
from od
    start with referenced_object_fullname = '{start_object}'
    connect by referenced_object_fullname = prior referencing_object_fullname
;
'''
    return session.sql(query_text).to_pandas()

def query_dependencies_child_df(session, object_domain, start_object):
    # Snowflakeから参照先方向へオブジェクトの依存関係を取得
    query_text = f'''
with od as (
    select
        referenced_object_domain,
        referenced_database ||'.'|| referenced_schema ||'.'|| referenced_object_name as referenced_object_fullname,
        referencing_object_domain,
        referencing_database ||'.'|| referencing_schema ||'.'|| referencing_object_name as referencing_object_fullname
    from
        snowflake.account_usage.object_dependencies
    where
        referenced_object_domain in ('{object_domain}')
        and referencing_object_domain in ('{object_domain}')
)
select
    *
from od
    start with referencing_object_fullname = '{start_object}'
    connect by referencing_object_fullname = prior referenced_object_fullname
;
'''
    return session.sql(query_text).to_pandas()

def genetate_node(from_object_names, to_object_names):
    # Graphvizのノード情報をテキスト出力
    result = ''
    for from_object_name, to_object_name in zip(from_object_names, to_object_names):
        result += f'''"{from_object_name}" -> "{to_object_name}";\n'''
    return result

def generate_graph(graph_parts):
    # Graphvizのグラフを出力
    return f'''digraph {{
{graph_parts}
}}'''

# Streamlitの画面表示
st.title("Object Dependencies Generator")

object_domain = st.selectbox(label='Select Object Domain', options = ['VIEW', 'TASK'])
if object_domain == 'VIEW': object_domain = "VIEW','TABLE"
start_object = st.text_input('Input Object Name', 'DATABASE.SCHEMA.OBJECT')

# Snowflakeからデータの取得
dependencies_child_df = query_dependencies_child_df(session, object_domain, start_object) 
dependencies_parent_df = query_dependencies_parent_df(session, object_domain, start_object)

# Graphvizで表示するためにdot言語の文を生成
graph_parts = ''
graph_parts += genetate_node(dependencies_child_df['REFERENCING_OBJECT_FULLNAME'], dependencies_child_df['REFERENCED_OBJECT_FULLNAME'])
graph_parts += genetate_node(dependencies_parent_df['REFERENCING_OBJECT_FULLNAME'], dependencies_parent_df['REFERENCED_OBJECT_FULLNAME'])
graph = generate_graph(graph_parts)

# Graphvizのグラフを表示
st.graphviz_chart(graph)
