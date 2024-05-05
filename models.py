
import joblib
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split, GridSearchCV
from itertools import product
import pandas as pd
import xgboost as xgb
import warnings
warnings.filterwarnings("ignore")

def RandomForest(Mad, Ad, Vdaf, Cin, Hin, Nin, Sin, Oin, Tin, Pin, Time, Addition, nS, Sc, Solvent_type, Catalyst, Atmosphere):  #
    # 加载模型——转化率、油产率
    # rf_1 = joblib.load('\\models\\random_forest_Conversion.pkl')
    rf_2 = joblib.load('./models/random_forest_Oil.pkl')
    rf_1 = joblib.load('./models/random_forest_Conversion.pkl')

    #选择某煤样的其它条件
    #神东煤，Fe2O3，催化剂添加量为3，'nS:nFe':[2]，四氢萘，'S:C':[3]，氢气气氛下，
    x1 = {'Mad':[Mad],'Ad':[Ad],'Vdaf':[Vdaf],'C':[Cin],'H':[Hin],'N':[Nin],'S':[Sin],'O':[Oin],
        'T':[int(Tin)],'P':[int(Pin)],'Time':[int(Time)],
        'Addition':[int(Addition)],'nS:nFe':[int(nS)],'S:C':[int(Sc)],
        'Solvent type':[int(Solvent_type)],'Catalyst':[int(Catalyst)],'Atmosphere':[int(Atmosphere)]}
    #print(type(x1["Mad"]))
    x1 = pd.DataFrame(x1)

    # 使用加载的模型进行预测
    Conversion_pred = rf_1.predict(x1)
    Oil_pred = rf_2.predict(x1)
    return (Conversion_pred, Oil_pred)


def lightgbm(Mad, Ad, Vdaf, Cin, Hin, Nin, Sin, Oin, Tin, Pin, Time, Addition, nS, Sc, Solvent_type, Catalyst, Atmosphere):
    # 加载模型——转化率、油产率
    rf_1 = joblib.load('models/LightGBM_Conversion.pkl')
    rf_2 = joblib.load('models/LightGBM_Oil.pkl')
    #选择某煤样的其它条件
    #神东煤，Fe2O3，催化剂添加量为3，'nS:nFe':[2]，四氢萘，'S:C':[3]，氢气气氛下，
    x1 = {'Mad':[Mad],'Ad':[Ad],'Vdaf':[Vdaf],'C':[Cin],'H':[Hin],'N':[Nin],'S':[Sin],'O':[Oin],
        'T':[int(Tin)],'P':[int(Pin)],'Time':[int(Time)],
        'Addition':[int(Addition)],'nS:nFe':[int(nS)],'S:C':[int(Sc)],
        'Solvent type':[int(Solvent_type)],'Catalyst':[int(Catalyst)],'Atmosphere':[int(Atmosphere)]}
    x1 = pd.DataFrame(x1)
    # 使用加载的模型进行预测
    Conversion_pred = rf_1.predict(x1)
    Oil_pred = rf_2.predict(x1)
    return (Conversion_pred, Oil_pred)


def xgboost(Mad, Ad, Vdaf, Cin, Hin, Nin, Sin, Oin, Tin, Pin, Time, Addition, nS, Sc, Solvent_type, Catalyst, Atmosphere):
    # 加载模型——转化率、油产率
    #xgb_model = xgb.XGBRegressor(objective='reg:squarederror')
    # 模型
    rf_1 = joblib.load('models/XGBoost_Conversion.pkl')
    rf_2 = joblib.load('models/XGBoost_Oil.pkl')
    #选择某煤样的其它条件
    #神东煤，Fe2O3，催化剂添加量为3，'nS:nFe':[2]，四氢萘，'S:C':[3]，氢气气氛下，
    x1 = {'Mad':[Mad],'Ad':[Ad],'Vdaf':[Vdaf],'C':[Cin],'H':[Hin],'N':[Nin],'S':[Sin],'O':[Oin],
        'T':[int(Tin)],'P':[int(Pin)],'Time':[int(Time)],
        'Addition':[int(Addition)],'nS:nFe':[int(nS)],'S:C':[int(Sc)],
        'Solvent type':[int(Solvent_type)],'Catalyst':[int(Catalyst)],'Atmosphere':[int(Atmosphere)]}
    x1 = pd.DataFrame(x1)
    # 使用加载的模型进行预测
    Conversion_pred = rf_1.predict(x1)
    Oil_pred = rf_2.predict(x1)
    return (Conversion_pred, Oil_pred)


#print(RandomForest())
#print(lightgbm())
# print(xgboost())


    # x1 = {'Mad':[5.48],'Ad':[5.65],'Vdaf':[36.52],'C':[77.94],'H':[4.74],'N':[0.98],'S':[0.36],'O':[14.49],
    #     'T':[450],'P':[6],'Time':[60],
    #     'Addition':[3],'nS:nFe':[2],'S:C':[3],'Solvent type':[6],'Catalyst':[35],'Atmosphere':[3]}
    

