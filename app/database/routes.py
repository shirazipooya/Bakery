import logging
import csv
import io
import os
from flask import Blueprint, render_template, flash, redirect, url_for, request, jsonify
from app.database.forms import BakeryForm
from app.database.models import Bakery, OwnershipStatus, SecondFuel, HouseholdRisk, BakersRisk, TypeFlour, TypeBread
from app.extensions import db, socketio
from sqlalchemy import or_, asc, desc
import numpy as np
import pandas as pd
import geopandas as gpd
from sqlalchemy.exc import IntegrityError
from flask_login import current_user, login_required
# from flask_socketio import emit
from shapely.geometry import Point

from app.users.routes import role_required


blueprint = Blueprint(
    name='database',
    import_name=__name__,
)


def virastar(df, columns):
    df[columns] = df[columns].astype(str)
    df[columns] = df[columns].apply(lambda x: x.str.rstrip())
    df[columns] = df[columns].apply(lambda x: x.str.lstrip())
    df[columns] = df[columns].apply(lambda x: x.str.replace(' +', ' '))
    df[columns] = df[columns].apply(lambda x: x.str.replace('ي','ی'))
    # df[columns] = df[columns].apply(lambda x: x.str.replace('ئ','ی'))
    df[columns] = df[columns].apply(lambda x: x.str.replace('ك', 'ک'))
    return df

def virastarNoSpace(df, columns):
    df[columns] = df[columns].astype(str)
    df[columns] = df[columns].apply(lambda x: x.str.rstrip())
    df[columns] = df[columns].apply(lambda x: x.str.lstrip())
    df[columns] = df[columns].apply(lambda x: x.str.replace(' ', ''))
    df[columns] = df[columns].apply(lambda x: x.str.replace('ي','ی'))
    # df[columns] = df[columns].apply(lambda x: x.str.replace('ئ','ی'))
    df[columns] = df[columns].apply(lambda x: x.str.replace('ك', 'ک'))
    return df

def virastarStr(x):
    x = str(x)
    x = x.rstrip()
    x = x.lstrip()
    x = x.replace(' +', ' ')
    x = x.replace('ي','ی')
    # x = x.replace('ئ','ی')
    x = x.replace('ك', 'ک')
    return x

warnings = []

def emit(warnings, message):
    ms = message
    warnings.append(ms)
    socketio.emit('validation_message', ms)
    return None


def validate_bakery_id(bid):
    if len(bid) != 6:
        return False    
    elif bid == "000000":
        return False
    else:
        return True

def validate_phone_number(phone):    
    if len(phone) != 11:
        return False    
    elif phone == "00000000000":
        return False
    else:
        return True
    

def validate_iranian_national_code(code):
    code_len = len(code)
    if code_len > 10 or code_len < 8:
        return False

    if len(set(code)) == 1:
        return False

    if len(code) < 10:
        code = code.zfill(10)

    factors = [10, 9, 8, 7, 6, 5, 4, 3, 2]
    checksum = sum(int(code[i]) * factors[i] for i in range(len(code) - 1))
    remainder = checksum % 11
    last_digit = int(code[-1])

    if remainder < 2:
        return remainder == last_digit
    else:
        return 11 - remainder == last_digit




def extract_location(lat, lon):
    gdf_bakhsh = gpd.read_file('app/assets/data/geodatabase/Bakhsh.geojson')
    gdf_shahr = gpd.read_file('app/assets/data/geodatabase/Shahr.geojson')
    gdf_district = gpd.read_file('app/assets/data/geodatabase/District.geojson')
    point = Point(lon, lat)
    
    containing_feature = gdf_bakhsh[gdf_bakhsh.geometry.apply(lambda geom: geom.contains(point))]
    ostan = containing_feature.iloc[0]['ostan']
    shahrestan = containing_feature.iloc[0]['shahrestan']
    bakhsh = containing_feature.iloc[0]['bakhsh']
    
    containing_feature = gdf_shahr[gdf_shahr.geometry.apply(lambda geom: geom.contains(point))]
    if not containing_feature.empty:
        shahr = containing_feature.iloc[0]['shahr']
        
        containing_feature = gdf_district[gdf_district.geometry.apply(lambda geom: geom.contains(point))]
        if not containing_feature.empty:
            region = containing_feature.iloc[0]['region']
            district = containing_feature.iloc[0]['district']
        else:
            region = 1
            district = 1  
    else:
        shahr = "روستایی"
        region = 1
        district = 1
    
    return ostan, shahrestan, bakhsh, shahr, region, district


def clean_csv_file(df):
        
    gdf_bakhsh = gpd.read_file('app/assets/data/geodatabase/Bakhsh.geojson')
    gdf_shahr = gpd.read_file('app/assets/data/geodatabase/Shahr.geojson')
    gdf_regions = gpd.read_file('app/assets/data/geodatabase/Region.geojson')
    gdf_district = gpd.read_file('app/assets/data/geodatabase/District.geojson')
    
    originalCols = [
        'first_name', #Done
        'last_name', #Done
        'nid', #Done
        'phone', #Done
        'bakery_id', #Done
        'ownership_status', #Done
        'second_fuel', #Done
        'city', #Done
        'lat', #Done
        'lon', #Done
        'household_risk', #Done
        'bakers_risk', #Done
        'flour_types', #Done
        'bread_types', #Done
        'number_violations', #Done
        'bread_rations' #Done
    ]
    
    # ⚠️: ⚠️
    # ❌: \u274C
    # ✅: \u2705
    
    # Check Columns Count
    if df.columns.__len__() != originalCols.__len__():
        emit(warnings=warnings, message=f"\u274C خطایی رخ داده است:\n ستون‌های فایل *.csv شما باید فقط شامل این موارد باشد:\n {', '.join(originalCols)}")
        logging.info(f"\u274C خطایی رخ داده است:\n ستون‌های فایل *.csv شما باید فقط شامل این موارد باشد:\n {', '.join(originalCols)}")
        return None
    
    # Check Columns Name
    if set(originalCols) != set(df.columns):
        emit(warnings=warnings, message=f"\u274C خطایی رخ داده است:\n ستون‌های فایل *.csv شما باید فقط شامل این موارد باشد:\n {', '.join(originalCols)}")
        logging.info(f"\u274C خطایی رخ داده است:\n ستون‌های فایل *.csv شما باید فقط شامل این موارد باشد:\n {', '.join(originalCols)}")
        return None
    
    if df.shape[0] == 0:
        emit(warnings=warnings, message=f"\u274C خطایی رخ داده است:\n فایل ورودی هیچگونه رکوردی ندارد!")
        logging.info(f"\u274C خطایی رخ داده است:\n فایل ورودی هیچگونه رکوردی ندارد!")
        return None
    
    # Remove Duplicate Rows
    if df.duplicated().sum() > 0:
        emit(warnings=warnings, message=f"⚠️ در فایل ورودی شما {df.duplicated().sum()} ردیف تکراری وجود داشت که حذف گردید!")
        logging.info(f"⚠️ در فایل ورودی شما {df.duplicated().sum()} ردیف تکراری وجود داشت که حذف گردید!")
        df.drop_duplicates(inplace=True)
    
    # Remove None lat and lon
    df['lat'] = pd.to_numeric(df['lat'], errors='coerce')
    df['lon'] = pd.to_numeric(df['lon'], errors='coerce')
    df[['lat', 'lon']] = df[['lat', 'lon']].astype(float)
    missing_lat_lon = df[(df['lat'].isna()) | (df['lon'].isna())]
    if missing_lat_lon.shape[0] == df.shape[0]:
        emit(warnings=warnings, message=f"\u274C دو ستون «طول جغرافیایی» و «عرض جغرافیایی» حتما باید دارای مقدار باشند!")
        logging.info(f"\u274C دو ستون «طول جغرافیایی» و «عرض جغرافیایی» حتما باید دارای مقدار باشند!")
        emit(warnings=warnings, message=f"\u274C خطایی رخ داده است:\n تمام ردیف‌های این فایل فاقد مقدار برای دو ستون «طول جغرافیایی» و «عرض جغرافیایی» می‌باشند!")
        logging.info(f"\u274C خطایی رخ داده است:\n تمام ردیف‌های این فایل فاقد مقدار برای دو ستون «طول جغرافیایی» و «عرض جغرافیایی» می‌باشند!")
        return None
    if missing_lat_lon.shape[0] != 0:
        emit(warnings=warnings, message=f"⚠️ دو ستون «طول جغرافیایی» و «عرض جغرافیایی» حتما باید دارای مقدار عددی باشند!")
        logging.info(f"⚠️ دو ستون «طول جغرافیایی» و «عرض جغرافیایی» حتما باید دارای مقدار عددی باشند!")
        emit(warnings=warnings, message=f"\u2705 تعداد {missing_lat_lon.shape[0]} ردیف، بدون طول و عرض جغرافیایی، از فایل ورودی حذف شدند!")
        logging.info(f"\u2705 تعداد {missing_lat_lon.shape[0]} ردیف، بدون طول و عرض جغرافیایی، از فایل ورودی حذف شدند!")
        df.dropna(subset=['lat', 'lon'], inplace=True)
        
    # Reset Index
    df.reset_index(drop=True, inplace=True)
    
    # first_name:
    df['first_name'] = df['first_name'].fillna('نامشخص')
    df['first_name'] = df['first_name'].replace(0, 'نامشخص')
    df['first_name'] = df['first_name'].replace("0", 'نامشخص')
    df = virastar(df=df, columns=['first_name'])
    df['first_name'] = df['first_name'].astype(str)
    
    # last_name:
    df['last_name'] = df['last_name'].fillna('نامشخص')
    df['last_name'] = df['last_name'].replace(0, 'نامشخص')
    df['last_name'] = df['last_name'].replace("0", 'نامشخص')
    df = virastar(df=df, columns=['last_name'])
    df['last_name'] = df['last_name'].astype(str)
    
    # nid:
    df['nid'] = df['nid'].astype(str)
    df = virastarNoSpace(df=df, columns=['nid'])
    df['nid'] = df['nid'].apply(lambda x: x.replace("-", ""))
    df['nid'] = pd.to_numeric(df['nid'], errors='coerce')
    df['nid'] = df['nid'].astype('Int64')
    df['nid'] = df['nid'].fillna(0)
    df['nid'] = df['nid'].apply(lambda x: str(x).zfill(10))
    number_wrong_nid = df['nid'].apply(lambda x: not validate_iranian_national_code(x)).sum()
    df['nid'] = df['nid'].apply(lambda x: x if validate_iranian_national_code(x) else 'نامشخص')
    if number_wrong_nid != 0:
        emit(warnings=warnings, message=f"⚠️ ستون «کد ملی» دارای {number_wrong_nid} ردیف با مقدار «نامشخص» می‌باشد!")
        logging.info(f"⚠️ ستون «کد ملی» دارای {number_wrong_nid} ردیف با مقدار «نامشخص» می‌باشد!")
    
    # phone:
    df['phone'] = df['phone'].astype(str)
    df = virastarNoSpace(df=df, columns=['phone'])
    df['phone'] = pd.to_numeric(df['phone'], errors='coerce')
    df['phone'] = df['phone'].astype('Int64')
    df['phone'] = df['phone'].fillna(0)
    df['phone'] = df['phone'].apply(lambda x: str(x).zfill(11))    
    number_wrong_phone = df['phone'].apply(lambda x: not validate_phone_number(x)).sum()
    df['phone'] = df['phone'].apply(lambda x: x if validate_phone_number(x) else 'نامشخص')
    if number_wrong_phone != 0:
        emit(warnings=warnings, message=f"⚠️ ستون «تلفن همراه» دارای {number_wrong_phone} ردیف با مقدار «نامشخص» می‌باشد!")
        logging.info(f"⚠️ ستون «تلفن همراه» دارای {number_wrong_phone} ردیف با مقدار «نامشخص» می‌باشد!")
    
    # bakery_id:
    df['bakery_id'] = df['bakery_id'].astype(str)
    df = virastarNoSpace(df=df, columns=['bakery_id'])
    df['bakery_id'] = pd.to_numeric(df['bakery_id'], errors='coerce')
    df['bakery_id'] = df['bakery_id'].astype('Int64')
    df['bakery_id'] = df['bakery_id'].fillna(0)
    df['bakery_id'] = df['bakery_id'].apply(lambda x: str(x).zfill(6))    
    number_wrong_bakery_id = df['bakery_id'].apply(lambda x: not validate_bakery_id(x)).sum()
    df['bakery_id'] = df['bakery_id'].apply(lambda x: x if validate_bakery_id(x) else 'نامشخص')
    if number_wrong_bakery_id != 0:
        emit(warnings=warnings, message=f"⚠️ ستون «شماره خبازی» دارای {number_wrong_bakery_id} ردیف با مقدار «نامشخص» می‌باشد!")
        logging.info(f"⚠️ ستون «شماره خبازی» دارای {number_wrong_bakery_id} ردیف با مقدار «نامشخص» می‌باشد!")
    
    # ownership_status:
    df['ownership_status'] = df['ownership_status'].fillna('نامشخص')
    df['ownership_status'] = df['ownership_status'].replace("0", 'نامشخص')
    df['ownership_status'] = df['ownership_status'].astype(str)
    df = virastar(df=df, columns=['ownership_status'])
    
    os_df_unique = df['ownership_status'].unique()   
    os_items = [x[0] for x in db.session.query(OwnershipStatus.name).all()]
    
    if not set(os_df_unique).issubset(set(os_items)):
        emit(
            warnings=warnings,
            message=f"\u274C خطایی رخ داده است:\n- در ستون «نوع ملک» داده‌های شما، مقادیر زیر وجود دارد: {', '.join(os_df_unique)}\n- در حالیکه در مدیریت مشخصه‌ها برای ستون «نوع ملک» مقادیر زیر وجود دارد: {', '.join(os_items)}"
        )
        logging.info(f"\u274C خطایی رخ داده است:\n- در ستون «نوع ملک» داده‌های شما، مقادیر زیر وجود دارد: {', '.join(os_df_unique)}\n- در حالیکه در مدیریت مشخصه‌ها برای ستون «نوع ملک» مقادیر زیر وجود دارد: {', '.join(os_items)}")
        return None
    
    if df['ownership_status'].value_counts().get('نامشخص', 0) != 0:
        emit(warnings=warnings, message=f"⚠️ ستون «نوع ملک» دارای {df['ownership_status'].value_counts().get('نامشخص', 0)} ردیف با مقدار «نامشخص» می‌باشد!")
        logging.info(f"⚠️ ستون «نوع ملک» دارای {df['ownership_status'].value_counts().get('نامشخص', 0)} ردیف با مقدار «نامشخص» می‌باشد!")
    
    # second_fuel:
    df['second_fuel'] = df['second_fuel'].fillna('نامشخص')
    df['second_fuel'] = df['second_fuel'].replace("0", 'نامشخص')
    df['second_fuel'] = df['second_fuel'].astype(str)
    df = virastar(df=df, columns=['second_fuel'])
    
    sf_df_unique = df['second_fuel'].unique()   
    sf_items = [x[0] for x in db.session.query(SecondFuel.name).all()]
    
    if not set(sf_df_unique).issubset(set(sf_items)):
        emit(
            warnings=warnings,
            message=f"\u274C خطایی رخ داده است:\n- در ستون «سوخت دوم» داده‌های شما، مقادیر زیر وجود دارد: {', '.join(sf_df_unique)}\n- در حالیکه در مدیریت مشخصه‌ها برای ستون «سوخت دوم» مقادیر زیر وجود دارد: {', '.join(sf_items)}"
        )
        logging.info(f"\u274C خطایی رخ داده است:\n- در ستون «سوخت دوم» داده‌های شما، مقادیر زیر وجود دارد: {', '.join(sf_df_unique)}\n- در حالیکه در مدیریت مشخصه‌ها برای ستون «سوخت دوم» مقادیر زیر وجود دارد: {', '.join(sf_items)}")
        return None
    
    if df['second_fuel'].value_counts().get('نامشخص', 0) != 0:
        emit(warnings=warnings, message=f"⚠️ ستون «سوخت دوم» دارای {df['second_fuel'].value_counts().get('نامشخص', 0)} ردیف با مقدار «نامشخص» می‌باشد!")
        logging.info(f"⚠️ ستون «سوخت دوم» دارای {df['second_fuel'].value_counts().get('نامشخص', 0)} ردیف با مقدار «نامشخص» می‌باشد!")

    
    # household_risk:
    df['household_risk'] = df['household_risk'].fillna('نامشخص')
    df['household_risk'] = df['household_risk'].replace("0", 'نامشخص')
    df['household_risk'] = df['household_risk'].astype(str)
    df = virastar(df=df, columns=['household_risk'])
    
    hr_df_unique = df['household_risk'].unique()   
    hr_items = [x[0] for x in db.session.query(HouseholdRisk.name).all()]
    
    if not set(hr_df_unique).issubset(set(hr_items)):
        emit(
            warnings=warnings,
            message=f"\u274C خطایی رخ داده است:\n- در ستون «ریسک خانوار» داده‌های شما، مقادیر زیر وجود دارد: {', '.join(hr_df_unique)}\n- در حالیکه در مدیریت مشخصه‌ها برای ستون «ریسک خانوار» مقادیر زیر وجود دارد: {', '.join(hr_items)}"
        )
        logging.info(f"\u274C خطایی رخ داده است:\n- در ستون «ریسک خانوار» داده‌های شما، مقادیر زیر وجود دارد: {', '.join(hr_df_unique)}\n- در حالیکه در مدیریت مشخصه‌ها برای ستون «ریسک خانوار» مقادیر زیر وجود دارد: {', '.join(hr_items)}")
        return None
    
    if df['household_risk'].value_counts().get('نامشخص', 0) != 0:
        emit(warnings=warnings, message=f"⚠️ ستون «ریسک خانوار» دارای {df['household_risk'].value_counts().get('نامشخص', 0)} ردیف با مقدار «نامشخص» می‌باشد!")
        logging.info(f"⚠️ ستون «ریسک خانوار» دارای {df['household_risk'].value_counts().get('نامشخص', 0)} ردیف با مقدار «نامشخص» می‌باشد!")
        
    # bakers_risk:
    df['bakers_risk'] = df['bakers_risk'].fillna('نامشخص')
    df['bakers_risk'] = df['bakers_risk'].replace("0", 'نامشخص')
    df['bakers_risk'] = df['bakers_risk'].astype(str)
    df = virastar(df=df, columns=['bakers_risk'])
    
    br_df_unique = df['bakers_risk'].unique()   
    br_items = [x[0] for x in db.session.query(BakersRisk.name).all()]
    
    if not set(br_df_unique).issubset(set(br_items)):
        emit(
            warnings=warnings,
            message=f"\u274C خطایی رخ داده است:\n- در ستون «ریسک نانوا» داده‌های شما، مقادیر زیر وجود دارد: {', '.join(br_df_unique)}\n- در حالیکه در مدیریت مشخصه‌ها برای ستون «ریسک نانوا» مقادیر زیر وجود دارد: {', '.join(br_items)}"
        )
        logging.info(f"\u274C خطایی رخ داده است:\n- در ستون «ریسک نانوا» داده‌های شما، مقادیر زیر وجود دارد: {', '.join(br_df_unique)}\n- در حالیکه در مدیریت مشخصه‌ها برای ستون «ریسک نانوا» مقادیر زیر وجود دارد: {', '.join(br_items)}")
        return None
    
    if df['bakers_risk'].value_counts().get('نامشخص', 0) != 0:
        emit(warnings=warnings, message=f"⚠️ ستون «ریسک نانوا» دارای {df['bakers_risk'].value_counts().get('نامشخص', 0)} ردیف با مقدار «نامشخص» می‌باشد!")
        logging.info(f"⚠️ ستون «ریسک نانوا» دارای {df['bakers_risk'].value_counts().get('نامشخص', 0)} ردیف با مقدار «نامشخص» می‌باشد!")
    
    
    # flour_types:
    df['flour_types'] = df['flour_types'].fillna('نامشخص')
    df['flour_types'] = df['flour_types'].replace("0", 'نامشخص')
    df['flour_types'] = df['flour_types'].astype(str)
    df = virastar(df=df, columns=['flour_types'])
    
    tf_df_unique = df['flour_types'].unique()   
    tf_items = [x[0] for x in db.session.query(TypeFlour.name).all()]
    
    if not set(tf_df_unique).issubset(set(tf_items)):
        emit(
            warnings=warnings,
            message=f"\u274C خطایی رخ داده است:\n- در ستون «نوع آرد» داده‌های شما، مقادیر زیر وجود دارد: {', '.join(tf_df_unique)}\n- در حالیکه در مدیریت مشخصه‌ها برای ستون «نوع آرد» مقادیر زیر وجود دارد: {', '.join(tf_items)}"
        )
        logging.info(f"\u274C خطایی رخ داده است:\n- در ستون «نوع آرد» داده‌های شما، مقادیر زیر وجود دارد: {', '.join(tf_df_unique)}\n- در حالیکه در مدیریت مشخصه‌ها برای ستون «نوع آرد» مقادیر زیر وجود دارد: {', '.join(tf_items)}")
        return None
    
    if df['flour_types'].value_counts().get('نامشخص', 0) != 0:
        emit(warnings=warnings, message=f"⚠️ ستون «نوع آرد» دارای {df['flour_types'].value_counts().get('نامشخص', 0)} ردیف با مقدار «نامشخص» می‌باشد!")
        logging.info(f"⚠️ ستون «نوع آرد» دارای {df['flour_types'].value_counts().get('نامشخص', 0)} ردیف با مقدار «نامشخص» می‌باشد!")
    
    
    # bread_types:
    df['bread_types'] = df['bread_types'].fillna('نامشخص')
    df['bread_types'] = df['bread_types'].replace("0", 'نامشخص')
    df['bread_types'] = df['bread_types'].astype(str)
    df = virastar(df=df, columns=['bread_types'])
    
    tb_df_unique = df['bread_types'].unique()   
    tb_items = [x[0] for x in db.session.query(TypeBread.name).all()]
    
    if not set(tb_df_unique).issubset(set(tb_items)):
        emit(
            warnings=warnings,
            message=f"\u274C خطایی رخ داده است:\n- در ستون «نوع پخت» داده‌های شما، مقادیر زیر وجود دارد: {', '.join(tb_df_unique)}\n- در حالیکه در مدیریت مشخصه‌ها برای ستون «نوع پخت» مقادیر زیر وجود دارد: {', '.join(tb_items)}"
        )
        logging.info(f"\u274C خطایی رخ داده است:\n- در ستون «نوع پخت» داده‌های شما، مقادیر زیر وجود دارد: {', '.join(tb_df_unique)}\n- در حالیکه در مدیریت مشخصه‌ها برای ستون «نوع پخت» مقادیر زیر وجود دارد: {', '.join(tb_items)}")
        return None
    
    if df['bread_types'].value_counts().get('نامشخص', 0) != 0:
        emit(warnings=warnings, message=f"⚠️ ستون «نوع پخت» دارای {df['bread_types'].value_counts().get('نامشخص', 0)} ردیف با مقدار «نامشخص» می‌باشد!")
        logging.info(f"⚠️ ستون «نوع پخت» دارای {df['bread_types'].value_counts().get('نامشخص', 0)} ردیف با مقدار «نامشخص» می‌باشد!")
    
    # city:
    df['city'] = df['city'].fillna('نامشخص')
    df['city'] = df['city'].replace("0", 'نامشخص')
    df['city'] = df['city'].astype(str)
    df = virastar(df=df, columns=['city'])
    
    if df['city'].value_counts().get('نامشخص', 0) != 0:
        emit(warnings=warnings, message=f"⚠️ ستون «شهر» دارای {df['city'].value_counts().get('نامشخص', 0)} ردیف با مقدار «نامشخص» می‌باشد!")
        logging.info(f"⚠️ ستون «شهر» دارای {df['city'].value_counts().get('نامشخص', 0)} ردیف با مقدار «نامشخص» می‌باشد!")
    
    # number_violations:
    df['number_violations'] = df['number_violations'].astype(str)
    df = virastarNoSpace(df=df, columns=['number_violations'])
    df['number_violations'] = pd.to_numeric(df['number_violations'], errors='coerce')
    df['number_violations'] = df['number_violations'].astype('Int64')
    number_na_nv = df['number_violations'].isna().sum()
    df['number_violations'] = df['number_violations'].fillna(0)

    if number_na_nv != 0:
        emit(warnings=warnings, message=f"⚠️ ستون «تعداد تخلفات نانوایی» دارای {number_na_nv} ردیف با مقدار «نامشخص» می‌باشد که با مقدار صفر جایگزین شد!")
        logging.info(f"⚠️ ستون «تعداد تخلفات نانوایی» دارای {number_na_nv} ردیف با مقدار «نامشخص» می‌باشد که با مقدار صفر جایگزین شد!")
        
    
    # bread_rations:
    df['bread_rations'] = df['bread_rations'].astype(str)
    df = virastarNoSpace(df=df, columns=['bread_rations'])
    df['bread_rations'] = pd.to_numeric(df['bread_rations'], errors='coerce')
    df['bread_rations'] = df['bread_rations'].apply(lambda x: int(round(x, 0)))
    df['bread_rations'] = df['bread_rations'].astype('Int64')
    number_na_br = df['bread_rations'].isna().sum()
    df['bread_rations'] = df['bread_rations'].fillna(0)

    if number_na_br != 0:
        emit(warnings=warnings, message=f"⚠️ ستون «سهمیه» دارای {number_na_br} ردیف با مقدار «نامشخص» می‌باشد که با مقدار صفر جایگزین شد!")
        logging.info(f"⚠️ ستون «سهمیه» دارای {number_na_br} ردیف با مقدار «نامشخص» می‌باشد که با مقدار صفر جایگزین شد!")
    
    
    gdf = gpd.GeoDataFrame(
        df,
        geometry=gpd.points_from_xy(df['lon'], df['lat'])
    )

    gdf = gdf.set_crs('EPSG:4326')
    gdf_bakhsh = gdf_bakhsh.to_crs('EPSG:4326')
    gdf_shahr = gdf_shahr.to_crs('EPSG:4326')
    gdf_regions = gdf_regions.to_crs('EPSG:4326')
    gdf_district = gdf_district.to_crs('EPSG:4326')
    
    
    gdf_joined_gdf_bakhsh = gpd.sjoin(gdf, gdf_bakhsh, how='left', predicate='within')
    gdf_joined_gdf_bakhsh.drop_duplicates(subset=originalCols, inplace=True)
    
    gdf_joined_gdf_shahr = gpd.sjoin(gdf, gdf_shahr, how='left', predicate='within')
    gdf_joined_gdf_shahr.drop_duplicates(subset=originalCols, inplace=True)
       
    gdf_joined_gdf_regions = gpd.sjoin(gdf, gdf_regions, how='left', predicate='within')
    gdf_joined_gdf_regions.drop_duplicates(subset=originalCols, inplace=True)
    
    gdf_joined_gdf_district = gpd.sjoin(gdf, gdf_district, how='left', predicate='within')
    gdf_joined_gdf_district.drop_duplicates(subset=originalCols, inplace=True)

    df[['ostan', 'shahrestan', 'bakhsh']] = gdf_joined_gdf_bakhsh[['ostan', 'shahrestan', 'bakhsh']]
    df['shahr'] = gdf_joined_gdf_shahr['shahr']
    df['region'] = gdf_joined_gdf_district['region']
    df['district'] = gdf_joined_gdf_district['district']
    
    df['region'] = pd.to_numeric(df['region'], errors='coerce')
    df['region'] = df['region'].astype('Int64')
    df['district'] = pd.to_numeric(df['district'], errors='coerce')
    df['district'] = df['district'].astype('Int64')
    
    # Drop All NULL Value from ostan, shahrestan, bakhsh
    n = df[['ostan', 'shahrestan', 'bakhsh']].isna().all(axis=1).sum()
    if n != 0:
        df.dropna(subset=['ostan', 'shahrestan', 'bakhsh'], inplace=True)
        emit(warnings=warnings, message=f"⚠️ {n} ردیف به علت نبودن در محدوده شهرستان از فایل ورودی حذف شدند!")
        logging.info(f"⚠️ {n} ردیف به علت نبودن در محدوده شهرستان از فایل ورودی حذف شدند!")
    
    
    df['shahr'] = df['shahr'].apply(lambda x: x if pd.notna(x) else "روستایی")
    df['region'] = df['region'].apply(lambda x: x if pd.notna(x) else 1)
    df['district'] = df['district'].apply(lambda x: x if pd.notna(x) else 1)
    
    
    # Reset Index
    df.reset_index(drop=True, inplace=True)

    return df
    



@blueprint.route(rule='/database', methods=['GET', 'POST'])
@login_required
@role_required('کاربر عادی')
def home():
    form = BakeryForm()
    
    items = OwnershipStatus.query.with_entities(OwnershipStatus.name).distinct().all()
    form.ownership_status.choices = [(item[0], item[0]) for item in items]
    
    items = SecondFuel.query.with_entities(SecondFuel.name).distinct().all()
    form.second_fuel.choices = [(item[0], item[0]) for item in items]
    
    items = HouseholdRisk.query.with_entities(HouseholdRisk.name).distinct().all()
    form.household_risk.choices = [(item[0], item[0]) for item in items]
    
    items = BakersRisk.query.with_entities(BakersRisk.name).distinct().all()
    form.bakers_risk.choices = [(item[0], item[0]) for item in items]
    
    items = TypeFlour.query.with_entities(TypeFlour.name).distinct().all()
    form.flour_types.choices = [(item[0], item[0]) for item in items]
    
    items = TypeBread.query.with_entities(TypeBread.name).distinct().all()
    form.bread_types.choices = [(item[0], item[0]) for item in items]
    
    if form.validate_on_submit():
        
        first_name = virastarStr(form.first_name.data)
        last_name = virastarStr(form.last_name.data)
        ostan, shahrestan, bakhsh, shahr, region, district = extract_location(lat=float(form.lat.data), lon=float(form.lon.data))
                
        bakery = Bakery(
            first_name = first_name,
            last_name = last_name,
            nid = form.nid.data,
            phone = form.phone.data,
            bakery_id = form.bakery_id.data,
            ownership_status = form.ownership_status.data,
            number_violations = int(form.number_violations.data),
            second_fuel = form.second_fuel.data,
            ostan = ostan,
            shahrestan = shahrestan,
            bakhsh = bakhsh,
            shahr = shahr,
            city = shahr,
            region = int(region),
            district = int(district),
            lat = float(form.lat.data),
            lon = float(form.lon.data),
            household_risk = form.household_risk.data,
            bakers_risk = form.bakers_risk.data,
            flour_types = form.flour_types.data,
            bread_types = form.bread_types.data,
            bread_rations = int(form.bread_rations.data),
        )
        db.session.add(bakery)
        db.session.commit()
        flash(message='رکورد جدید ایجاد گردید.', category='success')
        return redirect(location=url_for(endpoint='database.home'))
    return render_template(template_name_or_list='database/home.html', form=form)
    
      
@blueprint.route(rule='/api/database/upload', methods=['POST'])
@login_required
@role_required('کاربر عادی')
def upload_csv():    
    
    if 'file' not in request.files:
        return 'No file part'
    
    file = request.files['file']
        
    if file.filename == '':
        emit(warnings=warnings, message="\u274C فایلی انتخاب نشده است!") 
        return '', 204 
    
    if file and file.filename.endswith('.csv'):
        file_path = os.path.join('uploads', file.filename)
        file.save(file_path)
        data = clean_csv_file(pd.read_csv(file_path, dtype=str))
        if data is None:
            return '', 204       
        records_to_insert = []
        for _, row in data.iterrows():
            existing_record = Bakery.query.filter_by(
                first_name=row['first_name'],
                last_name=row['last_name'],
                nid=row['nid'],
                phone=row['phone'],
                bakery_id=row['bakery_id'],
                ownership_status=row['ownership_status'],
                number_violations=row['number_violations'],
                second_fuel=row['second_fuel'],
                ostan=row['ostan'],
                shahrestan=row['shahrestan'],
                bakhsh=row['bakhsh'],
                shahr=row['shahr'],
                city=row['city'],
                region=row['region'],
                district=row['district'],
                lat=row['lat'],
                lon=row['lon'],
                household_risk=row['household_risk'],
                bakers_risk=row['bakers_risk'],
                flour_types=row['flour_types'],
                bread_types=row['bread_types'],
                bread_rations=row['bread_rations'],
            ).first()
            
            if not existing_record:
                record = Bakery(
                    first_name=row['first_name'],
                    last_name=row['last_name'],
                    nid=row['nid'],
                    phone=row['phone'],
                    bakery_id=row['bakery_id'],
                    ownership_status=row['ownership_status'],
                    number_violations=row['number_violations'],
                    second_fuel=row['second_fuel'],
                    ostan=row['ostan'],
                    shahrestan=row['shahrestan'],
                    bakhsh=row['bakhsh'],
                    shahr=row['shahr'],
                    city=row['city'],
                    region=row['region'],
                    district=row['district'],
                    lat=row['lat'],
                    lon=row['lon'],
                    household_risk=row['household_risk'],
                    bakers_risk=row['bakers_risk'],
                    flour_types=row['flour_types'],
                    bread_types=row['bread_types'],
                    bread_rations=row['bread_rations'],
                )
                records_to_insert.append(record)
                # db.session.add(record)
        if records_to_insert:
            try:
                db.session.bulk_save_objects(records_to_insert)
                db.session.commit()
            except IntegrityError as e:
                db.session.rollback()  # Roll back the session if there's an error
                print(f"Error occurred: {e}")
        os.remove(file_path)        
        db.session.commit()
        flash(message='پایگاه داده با موفقیت ایجاد گردید!', category='success')
        return redirect(location=url_for(endpoint='table.home'))
    else:
        emit(warnings=warnings, message="\u274C فرمت فایل انتخابی حتما باید csv و نویسه کدگذاری آن utf-8 باشد!")
        return '', 204 
        # return redirect(location=url_for(endpoint='database.home'))



@blueprint.route('/api/database/delete/<int:id>', methods=['DELETE'])
@login_required
@role_required('کاربر عادی')
def delete_record(id):
    record = Bakery.query.get(id)
    if record:
        db.session.delete(record)
        db.session.commit()
        return jsonify({"message": f"نانوایی با شماره ردیف {id} با موفقیت از پایگاه داده حذف شد!"}), 200
    else:
        return jsonify({"error": f"نانوایی با شماره ردیف {id} پیدا نشد"}), 404

@blueprint.route('/api/database/delete/', methods=['DELETE'])
@login_required
@role_required('کاربر عادی')
def delete_table():
    try:
        db.session.query(Bakery).delete()
        db.session.commit()
        return jsonify({"message": f"همه ردیف های جدول حذف گردید!"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@blueprint.route('/api/database/update/<int:id>', methods=['GET', 'POST'])
@login_required
@role_required('کاربر عادی')
def update_record(id):
    data = request.json
    bakery = Bakery.query.filter_by(id=id).first()
    if bakery:
        bakery.first_name = data.get('first_name')
        bakery.last_name = data.get('last_name')
        bakery.nid = data.get('nid')
        bakery.phone = data.get('phone')
        bakery.bakery_id = data.get('bakery_id')
        bakery.ownership_status = data.get('ownership_status')
        bakery.number_violations = data.get('number_violations')
        bakery.second_fuel = data.get('second_fuel')
        bakery.city = data.get('city')
        bakery.region = data.get('region')
        bakery.district = data.get('district')
        bakery.lat = data.get('lat')
        bakery.lon = data.get('lon')
        bakery.household_risk = data.get('household_risk')
        bakery.bakers_risk = data.get('bakers_risk')
        bakery.flour_types = data.get('flour_types')
        bakery.bread_types = data.get('bread_types')
        bakery.bread_rations = data.get('bread_rations')
        db.session.commit()
        return jsonify({'message': 'Bakery Updated Successfully'})