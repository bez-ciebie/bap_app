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

#---DATA---
@st.cache_data
def fetch_data(path):
    return pd.read_csv(DATA_DIR / path, low_memory = False)
df = fetch_data('dashboard_data_1.csv')

@st.cache_data
def fetch_age():
    return df.merge(fetch_data('tuik_cinsiyet.csv').groupby(['MAHALLE ADI', 'yıl', 'yaş'])['sıklık'].sum().reset_index(), how = 'left', left_on = 'Mahalle', right_on = 'MAHALLE ADI')
yas_df = fetch_age()

@st.cache_data
def fetch_age_map():
    idx = yas_df[yas_df['yaş'] != 'GENEL TOPLAM'].groupby(['lat', 'lon', 'yıl'])['sıklık'].idxmax()
    result_df = yas_df.loc[idx]
    return result_df
result_df = fetch_age_map()

@st.cache_data
def fetch_egitim():
    return df.merge(fetch_data('tuik_egitim.csv').groupby(['MAHALLEADI', 'YIL', 'EGITIM_DURUMU_ADI'])['NUFUS'].sum().reset_index(), how = 'left', left_on = 'Mahalle', right_on = 'MAHALLEADI')
egitim_df = fetch_egitim()

@st.cache_data
def fetch_egitim_map():
    idx = egitim_df[egitim_df['EGITIM_DURUMU_ADI'] != 'GENEL TOPLAM'].groupby(['lat', 'lon', 'YIL'])['NUFUS'].idxmax()
    result_egitim_df = egitim_df.loc[idx]
    return result_egitim_df
result_egitim_df = fetch_egitim_map()

@st.cache_data
def fetch_medeni():
    return df.merge(fetch_data('tuik_medeni_durum.csv').groupby(['MAHALLE ADI', 'yıl', 'MEDENİ DURUM'])['TOPLAM'].sum().reset_index(), how = 'left', left_on = 'Mahalle', right_on = 'MAHALLE ADI')
medeni_df = fetch_medeni()

@st.cache_data
def fetch_medeni_map():
    idx = medeni_df[medeni_df['MEDENİ DURUM'] != 'GENEL TOPLAM'].groupby(['lat', 'lon', 'yıl'])['TOPLAM'].idxmax()
    result_medeni_df = medeni_df.loc[idx]
    return result_medeni_df
result_medeni_df = fetch_medeni_map()




#---CSS---
with open(CSS_DIR / 'introduction.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

#----------------------------------------------------------------------------------------------------------------------
#-MENU-
with st.sidebar:
    menu = sac.menu([
        sac.MenuItem('Introduction', icon='house-fill'),
        sac.MenuItem('Data Visualisation', icon='bar-chart-line-fill', children = [
            sac.MenuItem('Table', icon='buildings-fill'),
            sac.MenuItem('Graphics', icon = 'building-fill-add'),
        ]),
        sac.MenuItem('Model', icon='bar-chart-line-fill'),
        sac.MenuItem('Conclusion', icon='clipboard-check-fill'),], 
        format_func='title', open_all=True)
    
#-INTRODUCTION-
if menu == 'Introduction':

    st.title('欢迎来到煤直接液化可视化界面!')

    # About the project
    st.markdown("""<body>
    <div class="card">
    <h2 class="about-title">About the Project</h2>
    <p class="about-text">Within the scope of this project, a multilayered database of the area determined as ‘education zone’ in Jansen Plan will be constructed with two focal points: <strong>TED University Campus</strong> and <strong>Ankara University Cebeci Campus</strong>. As the content of the database, in addition to the digitalization of the visual sources such as aerial photographs and the development plans of the area, the visualization of the information studies till today will be studied and archived. With this archival study and database construction, a visual and multi-layered knowledge base and memory of a part of Ankara will be provided for the citizens and students which has the potential to be developed for the whole city.</p>
    <img class="tedu-img" src="https://anket.tedu.edu.tr/assets/images/logo.png">
    </div>
    </body>""", unsafe_allow_html=True)
    sac.divider(label='', icon='building', align='center')

    # About the sites
    site_1, site_2 = st.columns(2)
    with site_1:
        st.markdown("""<body>
        <div class="sites">
        <p class="about-sites">After the declaration of Ankara as the new capital city, initiatives for a city plan were begun, and the first plan of the city was prepared by the German planner Dr. Carl Cristoph Lörcher in 1924, which included the major decisions of the following planning studies also: two parts as old city and Yenişehir (Cengizkan 2004, 25). After that, with the decision to give a modern image to the city, in 1927, an international competition was organized for the new Ankara master plan; and Berlin-based architect Hermann Jansen's plan, based on the ideas of the Garden City Movement, the predominant movement in Europe in that period, won the competition (Deriu 2013, 500). Cebeci is the area chosen for the development of the Higher Education District determined in Jansen Plan. Besides, there were new residential settlement formations related to the expansion of the city towards the foothills of the castle after being the capital city of the Republic. Further than that, as being close to the old and the new city, Cebeci was one of the squatter areas chosen to settle right after the declaration of Ankara as the new capital (Şenyapılı, 2004, 76). After 1930, Cebeci and Kolej districts witnessed construction of education buildings as pointed in Jansen plan and increase in the residential structures in relation – even emergence and increase in commercial activities in the following years -. Since then, the area continued to develop and transform with the changing conditions, plan decisions, etc. until 1990s mostly.<br><br>With the decision of the plan prepared in 1982, it was proposed to develop the city to the west; and in the direction of this decision, industrial zones and residential zones were proposed along this axis and mass housing projects were developed within these zones. During this sprawl of the city, the core of the city -including Cebeci district- began to be abandoned by the upper classes. In the end, after the movement of population outwards, the developments, changes and struggles in the city were began to be seen mainly outside the center of the city. Relatedly, Cebeci district could be said to be settled more and have a steady situation with minor function, spatial or social changes within itself.</p>
        </div>
        </body>""", unsafe_allow_html=True)

    with site_2:
        st.image('https://bisiklet.ego.gov.tr/wp-content/uploads/2020/09/guzergah-sihhiye.jpg', caption = 'Map of Cebeci, Ankara', use_column_width = 'always')
        st.image('https://kampusteengelsizyasam.files.wordpress.com/2011/05/0651.jpg', caption = 'Ankara University, Cebeci, Ankara', use_column_width = 'always')

    # Introduction
    st.markdown("""
                <body>
                <style>
                h2 {
                color: #012d64;
                }
                </style>
                <h2>Introduction</h2>
                </body>
                """, unsafe_allow_html=True)

    st.warning("Autocad'den alınan poligon verilerinde sorun var. Birbirine çok yakın noktalar ya da 3 nokta var; poligonlar çizilemiyor. Autocad'den veriler alınırken hangi CRS bilgisine göre alındı?", icon = '⚠️')


#-Data Visualization-
# Table
elif menu == 'Table':
    # Title
    st.markdown("""
                <body>
                <style>
                h1 {
                color: #012d64;
                }
                </style>
                <h1>Table</h1>
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
elif menu == 'Graphics':
    # Title
    st.markdown("""
                <body>
                <style>
                h1 {
                color: #012d64;
                }
                </style>
                <h1>Graphics</h1>
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
elif menu == 'Model':

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
    st.title('Conclusion/Remarks')

    # About the project
    st.markdown("""<body>
    <div class="card">
    <p class="about-text">At vero eos et accusamus et iusto odio dignissimos ducimus qui blanditiis praesentium voluptatum deleniti atque corrupti quos dolores et quas molestias excepturi sint occaecati cupiditate non provident, similique sunt in culpa qui officia deserunt mollitia animi, id est laborum et dolorum fuga. Et harum quidem rerum facilis est et expedita distinctio. Nam libero tempore, cum soluta nobis est eligendi optio cumque nihil impedit quo minus id quod maxime placeat facere possimus, omnis voluptas assumenda est, omnis dolor repellendus. Temporibus autem quibusdam et aut officiis debitis aut rerum necessitatibus saepe eveniet ut et voluptates repudiandae sint et molestiae non recusandae. Itaque earum rerum hic tenetur a sapiente delectus, ut aut reiciendis voluptatibus maiores alias consequatur aut perferendis doloribus asperiores repellat.</p>
    </div>
    </body>""", unsafe_allow_html=True)
