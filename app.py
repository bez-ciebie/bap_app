#---PAKETLER---
import pandas as pd
import numpy as np
from pathlib import Path
import plotly.express as px
import streamlit as st
from PIL import Image
import streamlit_antd_components as sac
import sqlite3
from models import RandomForest, lightgbm, xgboost
import input_check


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
    <p class="about-text">&emsp;&emsp;中国神华煤制油化工有限公司鄂尔多斯煤制油分公司隶属于中国神华煤制油化工有限公司，位于内蒙古鄂尔多斯伊金霍洛旗乌兰木伦镇，公司采用具有自主知识产权的神华煤直接液化工艺，以煤炭为原料，通过化学加工过程生产石油、石化产品，是世界上居领先地位的现代化大型煤炭直接液化工业化生产企业。拥有标准化的质量检测中心，配备一流的检测设备。公司拥有的煤直接液化试生产线是全世界第一套商业化运行生产线，是国家十五重点项目之一，是涉及国家能源战略、产业战略以及神华集团自身发展战略的重大项目，是一种先进的洁净煤技术和国家煤炭清洁转化的示范工程，是解决我国石油供应的一条重要途径。同时也是神华集团迈向世界煤炭及深加工等一流能源企业的重要跨越。</p>
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
    col1, col2 = st.columns(2)
    with col1:
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

    with col2:
        con = sqlite3.connect('./data/data20240311.db',check_same_thread=False)
        # 获取数据库热力表对转化率的内容
        cur = con.cursor()
        sql = 'select Mad,Ad,Vdaf,Cdaf,Hdaf,Ndaf,Sdaf,Odaf,T,P,Time,油产率 from {0}'.format("Sheet1")    
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

    #工业分析
    col1, col2, col3, col4, col5, col6, col7, col8 = st.columns(8)
    with col1:
        st.write("")
        st.write("")
        st.write("工业分析")
    with col2:
        Mad = st.number_input('Mad/%', min_value=0.00, max_value=100.00, step=0.01)
    with col3:
        Ad = st.number_input('Ad/%', min_value=0.00, max_value=100.00, step=0.01)
    with col4:
        Vdaf = st.number_input('Vdaf/%', min_value=0.00, max_value=100.00, step=0.01)

    #元素分析
    col1, col2, col3, col4, col5, col6, col7, col8 = st.columns(8)
    with col1:
        st.write("")
        st.write("")
        st.write("元素分析")
    with col2:
        Cin = st.number_input('C/%', min_value=0.00, max_value=100.00, step=0.01)
    with col3:
        Hin = st.number_input('H/%', min_value=0.00, max_value=100.00, step=0.01)
    with col4:
        Nin = st.number_input('N/%', min_value=0.00, max_value=100.00, step=0.01)
    with col5:
        Sin = st.number_input('S/%', min_value=0.00, max_value=100.00, step=0.01)
    with col6:
        Oin = st.number_input('O/%', min_value=0.00, max_value=100.00, step=0.01)

    #反应条件
    col1, col2, col3, col4, col5, col6, col7, col8 = st.columns(8)
    with col1:
        st.write("")
        st.write("")
        st.write("反应条件")
    with col2:
        Tin = st.number_input('反应温度/℃', min_value=350, max_value=500, step=1) #摄氏度，预测时也是摄氏度   整数   350-500
    with col3:
        Pin = st.number_input('反应压力/MPa', min_value=0.00, max_value=30.00, step=0.01) # P  0-30  小数
    with col4:
        Time = st.number_input('恒温时间/min', min_value=0.00, max_value=120.00, step=0.01) #0-120  小数
    with col5:
        Atmosphere = st.text_input('气氛', value="氢气")
        #省略查询编码
        Atmosphere = 3


    #催化条件
    col1, col2, col3, col4, col5, col6, col7, col8 = st.columns(8)
    with col1:
        st.write("")
        st.write("")
        st.write("催化条件")    
    with col2:
        Catalyst = st.text_input('催化剂', value="Fe2O3") 
        #省略查询编码
        Catalyst = 35
    with col3:
        nS = st.number_input('nS\:nFe', min_value=0.00, max_value=4.00, step=0.01)#小数
    with col4:
        Addition = st.number_input('催化剂添加量/%', min_value=0.00, max_value=10.00, step=0.01)



    #溶剂条件
    col1, col2, col3, col4, col5, col6, col7, col8 = st.columns(8)
    with col1:
        st.write("")
        st.write("")
        st.write("溶剂条件")    
    with col2:
        Solvent_type = st.text_input('供氢溶剂', value="四氢萘")
        #省略查询编码
        Solvent_type = 6
    with col3:
        Sc = st.number_input('溶煤比', min_value=0.00, max_value=3.00, step=0.01)#小数
 


    #输入格式处理  遍历一遍 判断类型 前面是float:.2f  后面是int
    myshow = ''
    
    ret_li = input_check.input_check_all(Mad, Ad, Vdaf, Cin, Hin, Nin, Sin, Oin, Tin, Pin, Time, Addition, nS, Sc, Solvent_type, Catalyst, Atmosphere)
    if ret_li==None:
        my_show = "请检查，所有项都需要设置且不能为零！"
    else:
        my_show = f"输入数据：{ret_li}，请点击使用模型进行预测。"

    col1, col2, col3 = st.columns(3)
    with col1:
        st.success(my_show)
    # col1, col2, col3 = st.columns(3)  #Mad, Ad, Vdaf, C, H, N, S, O,T,P, Time, Addition, nS, Sc, Solvent_type, Catalyst, Atmosphere, Coal
    
    myshow_rf = ""
    myshow_li = ""
    myshow_xgb = ""
    # About the sites
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("随机森林预测"):
            if ret_li==None:
                myshow_rf = "请继续输入数据！"
            else:
                pair = RandomForest(Mad, Ad, Vdaf, Cin, Hin, Nin, Sin, Oin, Tin, Pin, Time, Addition, nS, Sc, Solvent_type, Catalyst, Atmosphere)
                myshow_rf = f"建议在反应温度为{Tin}℃、反应压力为{Pin}MPa、恒温时间为{Time}min的条件下进行反应。预估转化率为{pair[0][0]:.2f}%，油产率为{pair[1][0]:.2f}%"
        st.success(myshow_rf)
    with col2:
        if st.button("Lightgbm预测"):
            if ret_li==None:
                myshow_li = "请继续输入数据！"
            else:
                pair = lightgbm(Mad, Ad, Vdaf, Cin, Hin, Nin, Sin, Oin, Tin, Pin, Time, Addition, nS, Sc, Solvent_type, Catalyst, Atmosphere)
                myshow_li = f"建议在反应温度为{Tin}℃、反应压力为{Pin}MPa、恒温时间为{Time}min的条件下进行反应。预估转化率为{pair[0][0]:.2f}%，油产率为{pair[1][0]:.2f}%"
        st.success(myshow_li)
    with col3:
        if st.button("XGBoost预测"):
            if ret_li==None:
                myshow_xgb = "请继续输入数据！"
            else:
                pair = xgboost(Mad, Ad, Vdaf, Cin, Hin, Nin, Sin, Oin, Tin, Pin, Time, Addition, nS, Sc, Solvent_type, Catalyst, Atmosphere)           
                myshow_xgb = f"建议在反应温度为{Tin}℃、反应压力为{Pin}MPa、恒温时间为{Time}min的条件下进行反应。预估转化率为{pair[0][0]:.2f}%，油产率为{pair[1][0]:.2f}%"
        st.success(myshow_xgb)
else:
    st.title('总结')

    # About the project
    st.markdown("""<body>
    <div class="card">
    <p class="about-text">At vero eos et accusamus et iusto odio dignissimos ducimus qui blanditiis praesentium voluptatum deleniti atque corrupti quos dolores et quas molestias excepturi sint occaecati cupiditate non provident, similique sunt in culpa qui officia deserunt mollitia animi, id est laborum et dolorum fuga. Et harum quidem rerum facilis est et expedita distinctio. Nam libero tempore, cum soluta nobis est eligendi optio cumque nihil impedit quo minus id quod maxime placeat facere possimus, omnis voluptas assumenda est, omnis dolor repellendus. Temporibus autem quibusdam et aut officiis debitis aut rerum necessitatibus saepe eveniet ut et voluptates repudiandae sint et molestiae non recusandae. Itaque earum rerum hic tenetur a sapiente delectus, ut aut reiciendis voluptatibus maiores alias consequatur aut perferendis doloribus asperiores repellat.</p>
    </div>
    </body>""", unsafe_allow_html=True)
