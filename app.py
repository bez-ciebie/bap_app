#---PAKETLER---
import pandas as pd
import numpy as np
from pathlib import Path
import plotly.express as px
import streamlit as st
from PIL import Image
import streamlit_antd_components as sac
import sqlite3

#---KONUMLAR---
CUR_DIR = Path.cwd()
DATA_DIR = CUR_DIR / 'data'
CSS_DIR = CUR_DIR / 'css'
IMG_DIR = CUR_DIR / 'images'

#---SAYFA DÜZENİ---
st.set_page_config(page_title = 'BAP', page_icon = '🗺️', layout = "wide", initial_sidebar_state = "auto")

# #---DATA---
# @st.cache_data
# def fetch_data(path):
#     return pd.read_csv(DATA_DIR / path, low_memory = False)
# df = fetch_data('dashboard_data_1.csv')

# @st.cache_data
# def fetch_age():
#     return df.merge(fetch_data('tuik_cinsiyet.csv').groupby(['MAHALLE ADI', 'yıl', 'yaş'])['sıklık'].sum().reset_index(), how = 'left', left_on = 'Mahalle', right_on = 'MAHALLE ADI')
# yas_df = fetch_age()

# @st.cache_data
# def fetch_age_map():
#     idx = yas_df[yas_df['yaş'] != 'GENEL TOPLAM'].groupby(['lat', 'lon', 'yıl'])['sıklık'].idxmax()
#     result_df = yas_df.loc[idx]
#     return result_df
# result_df = fetch_age_map()

# @st.cache_data
# def fetch_egitim():
#     return df.merge(fetch_data('tuik_egitim.csv').groupby(['MAHALLEADI', 'YIL', 'EGITIM_DURUMU_ADI'])['NUFUS'].sum().reset_index(), how = 'left', left_on = 'Mahalle', right_on = 'MAHALLEADI')
# egitim_df = fetch_egitim()

# @st.cache_data
# def fetch_egitim_map():
#     idx = egitim_df[egitim_df['EGITIM_DURUMU_ADI'] != 'GENEL TOPLAM'].groupby(['lat', 'lon', 'YIL'])['NUFUS'].idxmax()
#     result_egitim_df = egitim_df.loc[idx]
#     return result_egitim_df
# result_egitim_df = fetch_egitim_map()

# @st.cache_data
# def fetch_medeni():
#     return df.merge(fetch_data('tuik_medeni_durum.csv').groupby(['MAHALLE ADI', 'yıl', 'MEDENİ DURUM'])['TOPLAM'].sum().reset_index(), how = 'left', left_on = 'Mahalle', right_on = 'MAHALLE ADI')
# medeni_df = fetch_medeni()

# @st.cache_data
# def fetch_medeni_map():
#     idx = medeni_df[medeni_df['MEDENİ DURUM'] != 'GENEL TOPLAM'].groupby(['lat', 'lon', 'yıl'])['TOPLAM'].idxmax()
#     result_medeni_df = medeni_df.loc[idx]
#     return result_medeni_df
# result_medeni_df = fetch_medeni_map()




#---CSS---
with open(CSS_DIR / 'introduction.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

#----------------------------------------------------------------------------------------------------------------------
#-MENU-
with st.sidebar:
    menu = sac.menu([
        sac.MenuItem('项目介绍', icon='house-fill'),
        sac.MenuItem('元数据', icon='bar-chart-line-fill', children = [
            sac.MenuItem('数据浏览', icon='buildings-fill'),
            sac.MenuItem('图表可视化', icon = 'building-fill-add'),
        ]),
        sac.MenuItem('模型预测', icon='bar-chart-line-fill'),
        sac.MenuItem('总结', icon='clipboard-check-fill'),], 
        format_func='title', open_all=True)
    
#-INTRODUCTION-
if menu == '项目介绍':


    st.title('欢迎来到煤直接液化可视化界面!')

    # About the project
    st.markdown("""<body>
    <div class="card">
    <h2 class="about-title">项目介绍</h2>
    <p class="about-text">&emsp;&emsp;神华煤直接液化项目是全世界第一套商业化示范工程；是国家十五重点项目之一，是涉及国家能源战略、产业战略以及神华集团自身发展战略的重大项目；是一种洁净的煤技术和国家煤炭清洁转化的示范工程；是解决我国石油供应的一条重要途径，同时也是神华集团迈向世界煤炭及深加工等一流能源企业的重要跨越。</p>
    </div>
    </body>""", unsafe_allow_html=True)
    
    site_1, site_2,site_3,site_4 = st.columns(4)
    with site_4:
        st.image("images/jituan.png", width=300)
    
    sac.divider(label='', icon='building', align='center')

    # About the sites

    st.markdown("""<body>
    <div class="sites">
    <p class="about-sites">&emsp;&emsp;神华鄂尔多斯煤制油分公司致力于发展中国的石油替代创新事业，按照“本质安全型、质量效益型、资源节约型、科技创新型、和谐发展型”的标准，全面加强和优化管理，不断创新提高，把公司逐步打造成为世界级煤制油样板公司。必将在更大范围、更广领域和更高层次上引领煤制油产业的发展，积极参与能源市场竞争，努力寻求与相关行业建立长期合作的战略伙伴关系。 </p>
    </div>
    </body>""", unsafe_allow_html=True)


#-Data Visualization-
# Table
elif menu == '数据浏览':
    # Title
    st.markdown("""
                <body>
                <style>
                h1 {
                color: #012d64;
                }
                </style>
                <h1>数据浏览</h1>
                </body>
                """, unsafe_allow_html=True)
    con = sqlite3.connect('data/data20240311.db',check_same_thread=False)
    cur = con.cursor()
    sql = 'select 煤种,Mad,Ad,Vdaf,Cdaf,Hdaf,Ndaf,Sdaf,Odaf,催化剂,助催化剂,供氢溶剂,气氛,转化率,油产率 from {0}'.format("Sheet1")
    cur.execute(sql)
    content = cur.fetchall()
    labels = [tuple[0] for tuple in cur.description]
    packs= pd.DataFrame(data = content, columns = labels)
    cur.close()
    con.close()

    st.table(packs)

#-Data Visualization-
# Graphics
elif menu == '图表可视化':
    # Title
    st.markdown("""
                <body>
                <style>
                h1 {
                color: #012d64;
                }
                </style>
                <h1>图表可视化</h1>
                </body>
                """, unsafe_allow_html=True)


    con = sqlite3.connect('./data/data20240311.db',check_same_thread=False)
    # 获取数据库热力表对转化率的内容
    cur = con.cursor()
    sql = 'select Mad,Ad,Vdaf,Cdaf,Hdaf,Ndaf,Sdaf,Odaf,T,P,Time,转化率 from {0}'.format("Sheet1")    
    cur.execute(sql)
    content = cur.fetchall()#只获得了数据

    # 获取数据库表的表头
    labels = [tuple[0] for tuple in cur.description]
    #print(labels)
    # 计算相关系数
    content = pd.read_sql_query(sql, con)
    data_float = [[float(value) if value.strip() else 0.00 for value in row] for row in content.values]
    raw_data = pd.DataFrame(data_float, columns=labels)
    raw_data_corr = raw_data.corr().to_dict(orient='records')

    data_values = []
    data_bigvalue = []
    for i in raw_data_corr:
        for j in list(i.values()):
            data_values.append(round(j,2))
        data_bigvalue.append(data_values)
        data_values=[]
    
    legend = list(raw_data_corr[0].keys())

    fig = px.imshow(data_bigvalue)

    fig = px.imshow(data_bigvalue,
                    labels=dict(),
                    x=legend,
                    y=legend,
                    text_auto=True
                   )
    fig.update_xaxes(side="top")


    tab1, tab2 = st.tabs(["Streamlit theme (default)", "Plotly native theme"])
    with tab1:
        st.plotly_chart(fig, theme="streamlit")
    with tab2:
        st.plotly_chart(fig, theme=None)

#-ModelPrediction
# RandomForest
elif menu == '模型预测':

    st.title("机器学习的煤直接液化预测")



    col1, col2, col3 = st.columns(3)
    with col1:
        Mad = st.text_input('Mad')
    with col2:
        Ad = st.text_input('Ad')
    with col3:
        Vdaf = st.text_input('Vdaf')
    with col1:
        C = st.text_input('C')
    with col2:
        H = st.text_input('H')
    with col3:
        N = st.text_input('N')
    with col1:
        S = st.text_input('S')
    with col2:
        O = st.text_input('O')
    with col3:
        T = st.text_input('T')
    with col1:
        P = st.text_input('P')
    with col2:
        Time = st.text_input('Time')
    with col3:
        Addition = st.text_input('Addition')
    with col1:
        nS = st.text_input('nS:nFe')
    with col2:
        SC = st.text_input('S:C')
    with col3:
        Solvent_type = st.text_input('Solvent_type')
    with col1:
        Catalyst = st.text_input('Catalyst')
    with col2:
        Atmosphere = st.text_input('Atmosphere')
    with col3:
        Coal = st.text_input('Coal')
 

    prediction = ''
    # About the sites
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("RF Prediction"):
            #RF_Conversion_prediction = RF_conversion_model.predict([[fo, fhi, flo, Jitter_percent, Jitter_Abs, RAP, PPQ,DDP,Shimmer,Shimmer_dB,APQ3,APQ5,APQ,DDA,NHR,HNR,RPDE,DFA,spread1,spread2,D2,PPE]])
            prediction = "RF模型预测下的转化率为：83.22%，油产率为57.98%"
    with col2:
        if st.button("Lightgbm Prediction"):
            #RF_Conversion_prediction = RF_conversion_model.predict([[fo, fhi, flo, Jitter_percent, Jitter_Abs, RAP, PPQ,DDP,Shimmer,Shimmer_dB,APQ3,APQ5,APQ,DDA,NHR,HNR,RPDE,DFA,spread1,spread2,D2,PPE]])
            prediction = "Lightgbm模型预测下的转化率为：83.22%，油产率为57.98%"
    with col3:
        if st.button("XGBoost Prediction"):
            #RF_Conversion_prediction = RF_conversion_model.predict([[fo, fhi, flo, Jitter_percent, Jitter_Abs, RAP, PPQ,DDP,Shimmer,Shimmer_dB,APQ3,APQ5,APQ,DDA,NHR,HNR,RPDE,DFA,spread1,spread2,D2,PPE]])
            prediction = "XGBoost模型预测下的转化率为：83.22%，油产率为57.98%"
    st.success(prediction)
else:
    st.title('总结')

    # About the project
    st.markdown("""<body>
    <div class="card">
    <p class="about-text">At vero eos et accusamus et iusto odio dignissimos ducimus qui blanditiis praesentium voluptatum deleniti atque corrupti quos dolores et quas molestias excepturi sint occaecati cupiditate non provident, similique sunt in culpa qui officia deserunt mollitia animi, id est laborum et dolorum fuga. Et harum quidem rerum facilis est et expedita distinctio. Nam libero tempore, cum soluta nobis est eligendi optio cumque nihil impedit quo minus id quod maxime placeat facere possimus, omnis voluptas assumenda est, omnis dolor repellendus. Temporibus autem quibusdam et aut officiis debitis aut rerum necessitatibus saepe eveniet ut et voluptates repudiandae sint et molestiae non recusandae. Itaque earum rerum hic tenetur a sapiente delectus, ut aut reiciendis voluptatibus maiores alias consequatur aut perferendis doloribus asperiores repellat.</p>
    </div>
    </body>""", unsafe_allow_html=True)
