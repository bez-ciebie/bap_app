#---PAKETLER---
import pandas as pd
from pathlib import Path
import plotly.express as px
import streamlit as st
from PIL import Image
import streamlit_antd_components as sac

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
df = fetch_data('dashboard_data.csv')

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
        sac.MenuItem('Analysis', icon='bar-chart-line-fill', children = [
            sac.MenuItem('Architectural', icon='buildings-fill'),
            sac.MenuItem('Functional Transformation', icon = 'building-fill-add'),
            sac.MenuItem('Demographics', icon = 'people-fill'),
            sac.MenuItem('Physical Status', icon = 'house-exclamation-fill')
        ]),
        sac.MenuItem('Conclusion', icon='clipboard-check-fill'),], 
        format_func='title', open_all=True)
    
#-INTRODUCTION-
if menu == 'Introduction':

    st.title('Welcome to BAP App!')

    # About the project
    st.markdown("""<body>
    <div class="card">
    <h2 class="about-title">About the Project</h2>
    <p class="about-text">Within the scope of this project, a multilayered database of the area determined as ‘education zone’ in Jansen Plan will be constructed with two focal points: <strong>TED University Campus</strong> and <strong>Ankara University Cebeci Campus</strong>. As the content of the database, in addition to the digitalization of the visual sources such as aerial photographs and the development plans of the area, the visualization of the information studies till today will be studied and archived. With this archival study and database construction, a visual and multi-layered knowledge base and memory of a part of Ankara will be provided for the citizens and students which has the potential to be developed for the whole city.</p>
    <img class="tedu-img" src="https://anket.tedu.edu.tr/assets/images/logo.png">
    </div>
    </body>""", unsafe_allow_html=True)

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
    sac.divider(label='', icon='building', align='center')
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


#-ANALYSIS-
# Architectural
elif menu == 'Architectural':
    # Title
    st.markdown("""
                <body>
                <style>
                h1 {
                color: #012d64;
                }
                </style>
                <h1>Architectural Analysis</h1>
                </body>
                """, unsafe_allow_html=True)
    # Map
    # Filters
    arch_1, arch_2, arch_3, arch_4, arch_5 = st.columns(5)
    with arch_1:
        arch_reg = sac.checkbox(items=[
            'Registered',
            'Not Registered'
        ],label = 'Select Registration', index = [0, 1], format_func='title', check_all='Select all', align='center')
        if arch_reg == ['Registered']:
            arch_reg = ['Tescilli']
        elif arch_reg == ['Not Registered']:
            arch_reg = ['Değil']
        else:
            arch_reg[0] = 'Tescilli'
            arch_reg[1] = 'Değil'
    with arch_2:
        arch_neigh = st.multiselect('Select Neighborhood', options = df['Mahalle'].dropna().unique())
        if arch_neigh == []:
            arch_neigh = df['Mahalle'].dropna().unique()
    with arch_3:
        arch_func = st.multiselect('Select Function', options = df['İşlev'].dropna().unique())
        if arch_func == []:
            arch_func = df['İşlev'].dropna().unique()
    with arch_4:
        arch_kat = st.multiselect('Select Number of Storeys', options = df['Kat Sayısı'].drop_duplicates().dropna().sort_values().astype(int))
        if arch_kat == []:
            arch_kat = df['Kat Sayısı'].dropna().unique()
    with arch_5:
        arch_area = sac.checkbox(items=[
            '2',
            '3',
            '4',
            '5',
            '6'
        ],label = 'Select Area', index = [0, 1, 2, 3, 4], format_func='title', check_all='Select all', align='center')
        arch_area = [int(area) for area in arch_area]
    # Scatter Map
    arch_fig = px.scatter_mapbox(data_frame = df.replace(['Tescilli', 'Değil'], ['Registered', 'Not Registered'])\
                                 .loc[df['Mahalle'].isin(arch_neigh)\
                                      &df['İşlev'].isin(arch_func)\
                                      &df['Kat Sayısı'].isin(arch_kat)\
                                      &df['Tescil Bilgisi'].isin(arch_reg)\
                                      &df['bölge'].isin(arch_area),:],
                        lat = 'lat',
                        lon = 'lon',
                        color = 'Tescil Bilgisi',
                        zoom = 14,
                        mapbox_style="open-street-map",
                        color_discrete_map={'Registered':'#2B3499', 'Not Registered':'#ED7D31'},
                        hover_data = ['Yapı', 'İşlev', 'No', 'Kat Sayısı', 'Mimarı', 'Mahalle', 'bölge'],
                        labels = {'Tescil Bilgisi':'Registration',
                                  'Yapı':'Structure',
                                  'No':'Detailed Area Number',
                                  'Kat Sayısı':'Number of Floors',
                                  'Mimarı':'Architect',
                                  'Mahalle':'Neighborhood',
                                  'bölge':'Area',
                                  'İşlev':'Function'}
                        )
    arch_fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0},
                           legend=dict(
                            orientation="h",
                            xanchor="center",
                            x = 0.5),
                            font=dict(
                            size=14
                         
    ))
    st.plotly_chart(arch_fig, use_container_width = True, theme = None)

# Functional Transformation
elif menu == 'Functional Transformation':
    # Title
    st.markdown("""
                <body>
                <style>
                h1 {
                color: #012d64;
                }
                </style>
                <h1>Functional Transformation</h1>
                </body>
                """, unsafe_allow_html=True)
    # Text
    st.markdown("""<body>
        <div class="card">
        <p class="about-text">Analyses conducted in different periods prove that educational buildings in the Cebeci area are at the forefront in shaping the character of the region. To observe the change in the distribution of functions, studies produced in different periods within the scope of the project were taken as major resources in addition to the comprehensive analysis carried out within the scope of the project. Two of the sources used to observe the change of functions in the declared project area and to make comparisons with today’s condition are Municipal plans dating before 2000 and an urban analysis on the are dating 2018-2019, before the pandemic period and the demolition of Cebeci Stadium in 2022. Since this data comparison is provided through a visual interface, it does not actually provide measurable values as a product, but it does provide instrumental information that provide a general framework for the functional transformation of the region.</p>
        </div>
        </body>""", unsafe_allow_html=True)
    function_1, function_2 = st.columns([1, 1])
    with function_1:
        st.image(Image.open(IMG_DIR / 'func_1.jpg'), use_column_width=True)
    with function_2:
        st.image(Image.open(IMG_DIR / 'func_2.jpg'), use_column_width=True)
    sac.divider(label='', icon='building', align='center')
    # Filters
    func_1, func_2, func_3, func_4, func_5 = st.columns(5)
    with func_1:
        func_reg = sac.checkbox(items=[
            'Registered',
            'Not Registered'
        ],label = 'Select Registration', index = [0, 1], format_func='title', check_all='Select all', align='center')
        if func_reg == ['Registered']:
            func_reg = ['Tescilli']
        elif func_reg == ['Not Registered']:
            func_reg = ['Değil']
        else:
            func_reg[0] = 'Tescilli'
            func_reg[1] = 'Değil'
    with func_2:
        func_neigh = st.multiselect('Select Neighborhood', options = df['Mahalle'].dropna().unique())
        if func_neigh == []:
            func_neigh = df['Mahalle'].dropna().unique()
    with func_3:
        func_func = st.multiselect('Select Function', options = df['İşlev'].dropna().unique(), default = ['Konut', 'Konut + Ticaret', 'Sağlık', 'Yurt', 'Eğitim'])
        if func_func == []:
            func_func = df['İşlev'].dropna().unique()
    with func_4:
        func_kat = st.multiselect('Select Number of Storeys', options = df['Kat Sayısı'].drop_duplicates().dropna().sort_values().astype(int))
        if func_kat == []:
            func_kat = df['Kat Sayısı'].dropna().unique()
    with func_5:
        func_area = sac.checkbox(items=[
            '2',
            '3',
            '4',
            '5',
            '6'
        ],label = 'Select Area', index = [0, 1, 2, 3, 4], format_func='title', check_all='Select all', align='center')
        func_area = [int(area) for area in func_area]

    # Scatter Map
    func_fig = px.scatter_mapbox(data_frame = df.replace(['Tescilli', 'Değil'], ['Registered', 'Not Registered'])\
                                 .loc[df['Mahalle'].isin(func_neigh)\
                                      &df['İşlev'].isin(func_func)\
                                      &df['Kat Sayısı'].isin(func_kat)\
                                      &df['Tescil Bilgisi'].isin(func_reg)\
                                      &df['bölge'].isin(func_area),:],
                        lat = 'lat',
                        lon = 'lon',
                        color = 'İşlev',
                        zoom = 14,
                        mapbox_style="open-street-map",
                        hover_data = ['Yapı', 'İşlev', 'No', 'Kat Sayısı', 'Mimarı', 'Mahalle', 'bölge'],
                        labels = {'Tescil Bilgisi':'Registration',
                                  'Yapı':'Structure',
                                  'No':'Detailed Area Number',
                                  'Kat Sayısı':'Number of Floors',
                                  'Mimarı':'Architect',
                                  'Mahalle':'Neighborhood',
                                  'bölge':'Area',
                                  'İşlev':'Function'})
    
    func_fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0},
                           legend=dict(
                            orientation="h",
                            xanchor="center",
                            x = 0.5),
                            font=dict(
                            size=14
                         
    ))
    st.plotly_chart(func_fig, use_container_width = True, theme = None)

    # Comparion Text
    st.info('Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.', icon="📍")
        
# Demographics
elif menu == 'Demographics':
    # Title
    st.markdown("""
                <body>
                <style>
                h1 {
                color: #012d64;
                }
                </style>
                <h1>Demographics</h1>
                </body>
                """, unsafe_allow_html=True)
    sac.divider(label='Age Analytics', icon='building', align='center')
  
    # AGE
    # Map and Bar
    age_1, age_2 = st.columns([1, 1])
    # Map
    with age_1:
        # Filters
        yas_map_col_1, yas_map_col_2 = st.columns(2)
        with yas_map_col_1:
            yas_map_neigh = st.multiselect('Select Neighborhood', options = yas_df['Mahalle'].dropna().unique())
            if yas_map_neigh == []:
                yas_map_neigh = yas_df['Mahalle'].dropna().unique()
        with yas_map_col_2:
                yas_map_yil = st.slider('Select Year', min_value = yas_df['yıl'].dropna().astype(int).min(), max_value = yas_df['yıl'].dropna().astype(int).max(), value = 2022, key = 'map_slider')
        # Data Manipulation
        age_map = px.scatter_mapbox(data_frame = result_df[(result_df['yıl'] == yas_map_yil) & (result_df['Mahalle'].isin(yas_map_neigh))],
                        lat = 'lat',
                        lon = 'lon',
                        color = 'yaş',
                        zoom = 14,
                        mapbox_style="open-street-map")
        age_map.update_layout(margin={"r":0,"t":0,"l":0,"b":0},
                              legend=dict(
                                orientation="h",
                                xanchor="center",
                                x = 0.5),
                                font=dict(
                            size=14))
        st.plotly_chart(age_map, use_container_width = True, theme = None)

    # Bar
    with age_2:
        # Filters
        yas_bar_col_1, yas_bar_col_2 = st.columns(2)
        with yas_bar_col_1:
            yas_bar_mah = st.selectbox('Select Neighborhood', options = yas_df['Mahalle'].dropna().unique())
        with yas_bar_col_2:
            yas_bar_yil = st.slider('Select Year', min_value = yas_df['yıl'].dropna().astype(int).min(), max_value = yas_df['yıl'].dropna().astype(int).max(), value = 2022)
        # Data Manipulation    
        yas_bar_df = yas_df[(yas_df['Mahalle'].isin([yas_bar_mah])) & (yas_df['yıl'] == yas_bar_yil) & (yas_df['yaş'] != 'GENEL TOPLAM')][['Mahalle','yaş', 'sıklık']].drop_duplicates()
        yas_bar_df = yas_bar_df.groupby(['Mahalle','yaş'])['sıklık'].sum().reset_index()
        yas_bar_df = yas_bar_df[yas_bar_df['sıklık'] != 0]
        yas_bar_df['color'] = yas_bar_df['sıklık'].apply(lambda x: '#012d64' if x in yas_bar_df.sort_values(by = 'sıklık').tail(3).sıklık.values else '#7D7C7C')
        yas_bar_mah = yas_bar_df['Mahalle'].unique()[0]
        yas_bar_1 = yas_bar_df.sort_values(by = 'sıklık').tail(3).sort_values(by = 'sıklık', ascending = False)['yaş'].values[0]
        yas_bar_2 = yas_bar_df.sort_values(by = 'sıklık').tail(3).sort_values(by = 'sıklık', ascending = False)['yaş'].values[1]
        yas_bar_3 = yas_bar_df.sort_values(by = 'sıklık').tail(3).sort_values(by = 'sıklık', ascending = False)['yaş'].values[2]
        # Bar Chart
        age_bar = px.bar(yas_bar_df,
                    y = 'yaş', 
                    x = 'sıklık',
                    color = 'yaş',
                    category_orders = {'yaş':['0-4' ,'5-9', '10-14', 
                                            '15-19', '20-24', '25-29',
                                            '30-34', '35-39', '40-44',
                                            '45-49', '50-54', '55-59',
                                            '60-64', '65 +']},
                    labels = {'yaş': 'Age Groups',
                            'sıklık':'Count'},
                    color_discrete_map = dict(zip(yas_bar_df['yaş'], yas_bar_df['color'])),
                    text_auto = True,
                    title=f'<b style="color:#7D7C7C;">Top 3 Densed Age Groups in <b style="color:#012d64;">{yas_bar_mah}</b> Are:</b><b style="color:#012d64;"> {yas_bar_1}, {yas_bar_2} and {yas_bar_3}</b>')
        age_bar.update_layout({
            'plot_bgcolor': 'rgba(0, 0, 0, 0)',
        },
        showlegend=False)
        st.plotly_chart(age_bar, use_container_width = True, theme = None)
        # Info
    st.info('Age Distribution of the Residents: The data, taken from Turkish Statistical Institute (TSI) and transformed into visual representation, shows that the young population concentrated around the campuses. In line with the increasing distance around the campuses the age of the residents increases. This is most probably related with the students living in the rented apartments in the close vicinity of the campuses. ', icon="📍")
    sac.divider(label='Educational Status Analytics', icon='building', align='center')

    # EDUCATIONAL STATUS
    # Map and Bar
    edu_1, edu_2 = st.columns([1, 1])
    # Map
    with edu_1:
        # Filters
        edu_map_col_1, edu_map_col_2 = st.columns(2)
        with edu_map_col_1:
            edu_map_neigh = st.multiselect('Select Neighborhood', options = egitim_df['MAHALLEADI'].dropna().unique(), key = 'edu_neigh_key')
            if edu_map_neigh == []:
                edu_map_neigh = egitim_df['MAHALLEADI'].dropna().unique()
        with edu_map_col_2:
                edu_map_yil = st.slider('Select Year', min_value = egitim_df['YIL'].dropna().astype(int).min(), max_value = egitim_df['YIL'].dropna().astype(int).max(), value = 2021, key = 'edu_slider')
        # Data Manipulation
        edu_map = px.scatter_mapbox(data_frame = result_egitim_df[(result_egitim_df['YIL'] == edu_map_yil) & (result_egitim_df['MAHALLEADI'].isin(edu_map_neigh))],
                        lat = 'lat',
                        lon = 'lon',
                        color = 'EGITIM_DURUMU_ADI',
                        zoom = 14,
                        mapbox_style="open-street-map")
        edu_map.update_layout(margin={"r":0,"t":0,"l":0,"b":0},
                              legend=dict(
                                orientation="h",
                                xanchor="center",
                                x = 0.5),
                                font=dict(
                            size=14))
        st.plotly_chart(edu_map, use_container_width = True, theme = None)

    # Bar
    with edu_2:
        # Filters
        edu_bar_col_1, edu_bar_col_2 = st.columns(2)
        with edu_bar_col_1:
            edu_bar_mah = st.selectbox('Select Neighborhood', options = egitim_df['MAHALLEADI'].dropna().unique(), key = 'edu_neigh_bar_key')
        with edu_bar_col_2:
            edu_bar_yil = st.slider('Select Year', min_value = egitim_df['YIL'].dropna().astype(int).min(), max_value = egitim_df['YIL'].dropna().astype(int).max(), value = 2021, key = 'edu_yil_bar_key')
        # Data Manipulation
        egitim_bar_df = egitim_df[(egitim_df['MAHALLEADI'].isin([edu_bar_mah])) & (egitim_df['YIL'] == edu_bar_yil) & (egitim_df['EGITIM_DURUMU_ADI'] != 'GENEL TOPLAM')][['MAHALLEADI','EGITIM_DURUMU_ADI', 'NUFUS']].drop_duplicates()
        egitim_bar_df = egitim_bar_df.groupby(['MAHALLEADI','EGITIM_DURUMU_ADI'])['NUFUS'].sum().reset_index()
        egitim_bar_df = egitim_bar_df[egitim_bar_df['NUFUS'] != 0]
        egitim_bar_df['color'] = egitim_bar_df['NUFUS'].apply(lambda x: '#012d64' if x in egitim_bar_df.sort_values(by = 'NUFUS').tail(3).NUFUS.values else '#7D7C7C')
        egitim_bar_mah = egitim_bar_df['MAHALLEADI'].unique()[0]
        egitim_bar_1 = egitim_bar_df.sort_values(by = 'NUFUS').tail(3).sort_values(by = 'NUFUS', ascending = False)['EGITIM_DURUMU_ADI'].values[0]
        egitim_bar_2 = egitim_bar_df.sort_values(by = 'NUFUS').tail(3).sort_values(by = 'NUFUS', ascending = False)['EGITIM_DURUMU_ADI'].values[1]
        egitim_bar_3 = egitim_bar_df.sort_values(by = 'NUFUS').tail(3).sort_values(by = 'NUFUS', ascending = False)['EGITIM_DURUMU_ADI'].values[2]
        # Bar Chart
        edu_bar = px.bar(egitim_bar_df,
                        y = 'EGITIM_DURUMU_ADI', 
                        x = 'NUFUS',
                        color = 'EGITIM_DURUMU_ADI',
                        category_orders = {'EGITIM_DURUMU_ADI':['BILINMEYEN' ,'OKUR-YAZAR DEĞIL', 'OKUR-YAZAR FAKAT BIR OKUL BITIRMEDI', 
                                                'İLKOKUL MEZUNU', 'İLKÖĞRETIM MEZUNU', 'ORTAOKUL VEYA DENGI MEZUNU',
                                                'LISE VEYA DENGI MEZUNU', 'YÜKSEKOKUL VEYA FAKÜLTE MEZUNU', 'YÜKSEK LISANS',
                                                'DOKTORA']},
                        labels = {'EGITIM_DURUMU_ADI': 'Educational Status',
                                'NUFUS':'Count'},
                        color_discrete_map = dict(zip(egitim_bar_df['EGITIM_DURUMU_ADI'], egitim_bar_df['color'])),
                        text_auto = True,
                        title=f'<b style="color:#7D7C7C;">Top 3 Densed Educational Status in <b style="color:#012d64;">{egitim_bar_mah}</b> Are:</b><br><b style="color:#012d64;"> {egitim_bar_1}, {egitim_bar_2} and {egitim_bar_3}</b>')
        edu_bar.update_layout({
                    'plot_bgcolor': 'rgba(0, 0, 0, 0)',
                    
                },
                title_font_size=14,
                showlegend=False,
                yaxis = dict(
                    tickfont = dict(size=9)))
        edu_bar.update_yaxes(title='', visible=True)
        st.plotly_chart(edu_bar, use_container_width = True, theme = None)
    st.info('Educational Status of the Residents: The data, taken from Turkish Statistical Institute (TSI) and transformed into visual representation, shows that the educational level of the population in the close environment of the campuses is mostly around and/or over undergraduate level. This is closely related to the young population living in the apartments around the campuses as seen in age distribution analysis.', icon="📍")
    sac.divider(label='Marital Status Analytics', icon='building', align='center')
    
    # MARITAL STATUS
    # Map and Bar
    mari_1, mari_2 = st.columns([1, 1])
    # Map
    with mari_1:
        # Filters
        mari_map_col_1, mari_map_col_2 = st.columns(2)
        with mari_map_col_1:
            mari_map_neigh = st.multiselect('Select Neighborhood', options = medeni_df['MAHALLE ADI'].dropna().unique(), key = 'mari_neigh_key')
            if mari_map_neigh == []:
                mari_map_neigh = medeni_df['MAHALLE ADI'].dropna().unique()
        with mari_map_col_2:
                mari_map_yil = st.slider('Select Year', min_value = medeni_df['yıl'].dropna().astype(int).min(), max_value = medeni_df['yıl'].dropna().astype(int).max(), value = 2022, key = 'mari_slider')
        # Data Manipulation
        mari_map = px.scatter_mapbox(data_frame = result_medeni_df[(result_medeni_df['yıl'] == mari_map_yil) & (result_medeni_df['MAHALLE ADI'].isin(mari_map_neigh))],
                        lat = 'lat',
                        lon = 'lon',
                        color = 'MEDENİ DURUM',
                        zoom = 14,
                        mapbox_style="open-street-map")
        mari_map.update_layout(margin={"r":0,"t":0,"l":0,"b":0},
                              legend=dict(
                                orientation="h",
                                xanchor="center",
                                x = 0.5),
                                font=dict(
                            size=14))
        st.plotly_chart(mari_map, use_container_width = True, theme = None)

    # Bar
    with mari_2:
        # Filters
        mari_bar_col_1, mari_bar_col_2 = st.columns(2)
        with mari_bar_col_1:
            mari_bar_mah = st.selectbox('Select Neighborhood', options = medeni_df['MAHALLE ADI'].dropna().unique(), key = 'mari_neigh_bar_key')
        with mari_bar_col_2:
            mari_bar_yil = st.slider('Select Year', min_value = medeni_df['yıl'].dropna().astype(int).min(), max_value = medeni_df['yıl'].dropna().astype(int).max(), value = 2022, key = 'mari_yil_bar_key')
        # Data Manipulation
        medeni_bar_df = medeni_df[(medeni_df['MAHALLE ADI'].isin([mari_bar_mah])) & (medeni_df['yıl'] == mari_bar_yil) & (medeni_df['MEDENİ DURUM'] != 'GENEL TOPLAM')][['MAHALLE ADI','MEDENİ DURUM', 'TOPLAM']].drop_duplicates()
        medeni_bar_df = medeni_bar_df.groupby(['MAHALLE ADI','MEDENİ DURUM'])['TOPLAM'].sum().reset_index()
        medeni_bar_df = medeni_bar_df[medeni_bar_df['TOPLAM'] != 0]
        medeni_bar_df['color'] = medeni_bar_df['TOPLAM'].apply(lambda x: '#012d64' if x in medeni_bar_df.sort_values(by = 'TOPLAM').tail(1).TOPLAM.values else '#7D7C7C')
        medeni_bar_mah = medeni_bar_df['MAHALLE ADI'].unique()[0]
        medeni_bar_1 = medeni_bar_df.sort_values(by = 'TOPLAM').tail(3).sort_values(by = 'TOPLAM', ascending = False)['MEDENİ DURUM'].values[0]
        # Bar Chart
        mari_bar = px.bar(medeni_bar_df,
             y = 'MEDENİ DURUM', 
             x = 'TOPLAM',
             color = 'MEDENİ DURUM',
             category_orders = {'MEDENİ DURUM':medeni_bar_df.sort_values(by = 'TOPLAM', ascending = False)['MEDENİ DURUM'].to_list()},
            labels = {'MEDENİ DURUM': 'MEDENİ DURUM',
                      'TOPLAM':'Count'},
            color_discrete_map = dict(zip(medeni_bar_df['MEDENİ DURUM'], medeni_bar_df['color'])),
            text_auto = True,
            title=f'<b style="color:#7D7C7C;">Top Densed Marital Status in <b style="color:#012d64;">{medeni_bar_mah}</b> is:</b><b style="color:#012d64;"> {medeni_bar_1}</b>')
        
        mari_bar.update_layout({
                    'plot_bgcolor': 'rgba(0, 0, 0, 0)',
                },
                title_font_size=14,
                showlegend=False,
                yaxis = dict(
                    tickfont = dict(size=9)))
        mari_bar.update_yaxes(title='', visible=True)
        st.plotly_chart(mari_bar, use_container_width = True, theme = None)
    st.info('Marital Status of the Residents: The data, taken from Turkish Statistical Institute (TSI) and transformed into visual representation, shows that a remarkable amount of the population in the close environment of the campuses is single residents. This concentration is most probably related to the students – young population - living in the apartments around the campuses as in the other two demographic analysis.', icon="📍")
elif menu == 'Physical Status':
    # Title
    st.markdown("""
                <body>
                <style>
                h1 {
                color: #012d64;
                }
                </style>
                <h1>Physical Status</h1>
                </body>
                """, unsafe_allow_html=True)
    
    # Kentsel Dönüşüm
    sac.divider(label='Urban Transformation', icon='building', align='center')
    st.warning("Kentsel dönüşümle ilgili yeterli veri bulunmamaktadır.", icon="⚠️")
    st.info('Urban Transformation: As a residential urban fabric, Cebeci has witnessed many changes and transformations since Ankara was declared as the capital city. Following the urban transformation boom affecting many early-settled neighborhoods, Cebeci area also became one of these. The districts located on the south of Ankara University Cebeci Campus houses many examples of such urban transformation activities scattered around. Cebeci Stadium demolished to implement a millet bahçesi project is the most remarkable example of urban transformation implementations in the area.', icon="📍")

    # Kat Yüksekliği
    sac.divider(label='Number of Storey', icon='building', align='center')

    # Map
    # Filters
    storey_1, storey_2, storey_3, storey_4, storey_5 = st.columns(5)
    with storey_1:
        storey_reg = sac.checkbox(items=[
            'Registered',
            'Not Registered'
        ],label = 'Select Registration', index = [0, 1], format_func='title', check_all='Select all', align='center')
        if storey_reg == ['Registered']:
            storey_reg = ['Tescilli']
        elif storey_reg == ['Not Registered']:
            storey_reg = ['Değil']
        else:
            storey_reg[0] = 'Tescilli'
            storey_reg[1] = 'Değil'
    with storey_2:
        storey_neigh = st.multiselect('Select Neighborhood', options = df['Mahalle'].dropna().unique())
        if storey_neigh == []:
            storey_neigh = df['Mahalle'].dropna().unique()
    with storey_3:
        storey_func = st.multiselect('Select Function', options = df['İşlev'].dropna().unique())
        if storey_func == []:
            storey_func = df['İşlev'].dropna().unique()
    with storey_4:
        storey_kat = st.multiselect('Select Number of Storeys', options = df['Kat Sayısı'].drop_duplicates().dropna().sort_values().astype(int))
        if storey_kat == []:
            storey_kat = df['Kat Sayısı'].dropna().unique()
    with storey_5:
        storey_area = sac.checkbox(items=[
            '2',
            '3',
            '4',
            '5',
            '6'
        ],label = 'Select Area', index = [0, 1, 2, 3, 4], format_func='title', check_all='Select all', align='center')
        storey_area = [int(area) for area in storey_area]
    # Scatter Map
    storey_fig = px.scatter_mapbox(data_frame = df.replace(['Tescilli', 'Değil'], ['Registered', 'Not Registered'])\
                                 .loc[df['Mahalle'].isin(storey_neigh)\
                                      &df['İşlev'].isin(storey_func)\
                                      &df['Kat Sayısı'].isin(storey_kat)\
                                      &df['Tescil Bilgisi'].isin(storey_reg)\
                                      &df['bölge'].isin(storey_area),:],
                        lat = 'lat',
                        lon = 'lon',
                        color = 'Kat Sayısı',
                        zoom = 14,
                        mapbox_style="carto-darkmatter",
                        hover_data = ['Yapı', 'İşlev', 'No', 'Kat Sayısı', 'Mimarı', 'Mahalle', 'bölge'],
                        labels = {'Tescil Bilgisi':'Registration',
                                  'Yapı':'Structure',
                                  'No':'Detailed Area Number',
                                  'Kat Sayısı':'Number of Storey',
                                  'Mimarı':'Architect',
                                  'Mahalle':'Neighborhood',
                                  'bölge':'Area',
                                  'İşlev':'Function'},
                        color_continuous_scale = px.colors.sequential.YlOrRd
                                  
                        )
    storey_fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0},
                           legend=dict(
                            orientation="h",
                            xanchor="center",
                            x = 0.5),
                            font=dict(
                            size=14
                         
    ))
    st.plotly_chart(storey_fig, use_container_width = True, theme = None)
else:
    st.title('Conclusion/Remarks')

    # About the project
    st.markdown("""<body>
    <div class="card">
    <p class="about-text">At vero eos et accusamus et iusto odio dignissimos ducimus qui blanditiis praesentium voluptatum deleniti atque corrupti quos dolores et quas molestias excepturi sint occaecati cupiditate non provident, similique sunt in culpa qui officia deserunt mollitia animi, id est laborum et dolorum fuga. Et harum quidem rerum facilis est et expedita distinctio. Nam libero tempore, cum soluta nobis est eligendi optio cumque nihil impedit quo minus id quod maxime placeat facere possimus, omnis voluptas assumenda est, omnis dolor repellendus. Temporibus autem quibusdam et aut officiis debitis aut rerum necessitatibus saepe eveniet ut et voluptates repudiandae sint et molestiae non recusandae. Itaque earum rerum hic tenetur a sapiente delectus, ut aut reiciendis voluptatibus maiores alias consequatur aut perferendis doloribus asperiores repellat.</p>
    </div>
    </body>""", unsafe_allow_html=True)
