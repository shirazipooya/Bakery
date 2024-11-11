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
from flask_socketio import emit


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
    df[columns] = df[columns].apply(lambda x: x.str.replace('ئ','ی'))
    df[columns] = df[columns].apply(lambda x: x.str.replace('ك', 'ک'))
    return df

def virastarNoSpace(df, columns):
    df[columns] = df[columns].astype(str)
    df[columns] = df[columns].apply(lambda x: x.str.rstrip())
    df[columns] = df[columns].apply(lambda x: x.str.lstrip())
    df[columns] = df[columns].apply(lambda x: x.str.replace(' ', ''))
    df[columns] = df[columns].apply(lambda x: x.str.replace('ي','ی'))
    df[columns] = df[columns].apply(lambda x: x.str.replace('ئ','ی'))
    df[columns] = df[columns].apply(lambda x: x.str.replace('ك', 'ک'))
    return df

def virastarStr(x):
    x = str(x)
    x = x.rstrip()
    x = x.lstrip()
    x = x.replace(' +', ' ')
    x = x.replace('ي','ی')
    x = x.replace('ئ','ی')
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
    

def clean_csv_file(df):
        
    gdf_regions = gpd.read_file('app/assets/data/geodatabase/Region.geojson')
    emit(warnings=warnings, message="\u2705 فایل Region.geojson با موفقیت بارگزاری شد!")   
    
    gdf_district = gpd.read_file('app/assets/data/geodatabase/District.geojson')
    emit(warnings=warnings, message="\u2705 فایل District.geojson با موفقیت بارگزاری شد!")   
    
    originalCols = [
        'first_name',
        'last_name',
        'nid',
        'phone',
        'bakery_id',
        'ownership_status',
        'number_violations',
        'second_fuel',
        'city',
        'lat',
        'lon',
        'household_risk',
        'bakers_risk',
        'type_flour',
        'type_bread',
        'bread_rations'
    ]
    
    # ⚠️: ⚠️
    # ❌: \u274C
    # ✅: \u2705
    
    # Check Columns Count
    if df.columns.__len__() != originalCols.__len__():
        emit(warnings=warnings, message=f"\u274C ستون‌های فایل *.csv شما باید فقط شامل این موارد باشد:\n {', '.join(originalCols)}")
        return None
    
    # Check Columns Name
    if set(originalCols) != set(df.columns):
        emit(warnings=warnings, message=f"\u274C ستون‌های فایل *.csv شما باید فقط شامل این موارد باشد:\n {', '.join(originalCols)}")
        return None
    
    if df.shape[0] == 0:
        emit(warnings=warnings, message=f"\u274C فایل ورودی هیچگونه رکوردی ندارد!")
        return None
    
    # Remove Duplicate Rows
    if df.duplicated().sum() > 0:
        emit(warnings=warnings, message=f"⚠️ در فایل ورودی شما {df.duplicated().sum()} ردیف تکراری وجود داشت که حذف گردید!")
        df.drop_duplicates(inplace=True)
    
    # Remove None lat and lon
    df['lat'] = pd.to_numeric(df['lat'], errors='coerce')
    df['lon'] = pd.to_numeric(df['lon'], errors='coerce')
    df[['lat', 'lon']] = df[['lat', 'lon']].astype(float)
    missing_lat_lon = df[(df['lat'].isna()) | (df['lon'].isna())]
    if missing_lat_lon.shape[0] == df.shape[0]:
        emit(warnings=warnings, message=f"\u274C دو ستون lat و lon حتما باید دارای مقدار باشند!")
        emit(warnings=warnings, message=f"\u274C تمام ردیف‌های این فایل فاقد مقدار برای دو ستون lat و lon می‌باشند!")
        return None
    if missing_lat_lon.shape[0] != 0:
        emit(warnings=warnings, message=f"⚠️ دو ستون lat و lon حتما باید دارای مقدار عددی باشند!")
        emit(warnings=warnings, message=f"\u2705 تعداد {missing_lat_lon.shape[0]} ردیف، بدون طول و عرض جغرافیایی، از فایل ورودی حذف شدند!")
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
    df['nid'] = pd.to_numeric(df['nid'], errors='coerce')
    df['nid'] = df['nid'].astype('Int64')
    df['nid'] = df['nid'].fillna(0)
    df['nid'] = df['nid'].apply(lambda x: str(x).zfill(10))
    number_wrong_nid = df['nid'].apply(lambda x: not validate_iranian_national_code(x)).sum()
    df['nid'] = df['nid'].apply(lambda x: x if validate_iranian_national_code(x) else 'نامشخص')
    emit(warnings=warnings, message=f"⚠️ {number_wrong_nid} ردیف دارای کد ملی اشتباه می‌باشند!")
    
    # phone:
    df['phone'] = df['phone'].astype(str)
    df = virastarNoSpace(df=df, columns=['phone'])
    df['phone'] = pd.to_numeric(df['phone'], errors='coerce')
    df['phone'] = df['phone'].astype('Int64')
    df['phone'] = df['phone'].fillna(0)
    df['phone'] = df['phone'].apply(lambda x: str(x).zfill(11))    
    number_wrong_phone = df['phone'].apply(lambda x: not validate_phone_number(x)).sum()
    df['phone'] = df['phone'].apply(lambda x: x if validate_phone_number(x) else 'نامشخص')
    emit(warnings=warnings, message=f"⚠️ {number_wrong_phone} ردیف دارای تلفن اشتباه می‌باشند!")
    
    # bakery_id:
    df['bakery_id'] = df['bakery_id'].astype(str)
    df = virastarNoSpace(df=df, columns=['bakery_id'])
    df['bakery_id'] = pd.to_numeric(df['bakery_id'], errors='coerce')
    df['bakery_id'] = df['bakery_id'].astype('Int64')
    df['bakery_id'] = df['bakery_id'].fillna(0)
    df['bakery_id'] = df['bakery_id'].apply(lambda x: str(x).zfill(6))    
    number_wrong_bakery_id = df['bakery_id'].apply(lambda x: not validate_bakery_id(x)).sum()
    df['bakery_id'] = df['bakery_id'].apply(lambda x: x if validate_bakery_id(x) else 'نامشخص')
    emit(warnings=warnings, message=f"⚠️ {number_wrong_bakery_id} ردیف دارای شماره خبازی اشتباه می‌باشند!")
    
    
    
    
    
    
    print(df['bakery_id'].head(30))
    

    return None

    COLs = ['first_name', 'last_name', 'ownership_status', 'second_fuel', 'city', 'household_risk', 'bakers_risk', 'type_bread', 'nid', 'phone', 'bakery_id']
    df = virastar(df=df, columns=COLs)

    COLs = ['number_violations', 'type_flour', 'bread_rations']
    df[COLs] = df[COLs].astype(int, errors='ignore')
     
   

    # Convert nid and phone to `str`
    df['nid'] = df['nid'].apply(lambda x: str(x).zfill(10))
    df['phone'] = df['phone'].apply(lambda x: str(x).zfill(11))

    df.reset_index(drop=True, inplace=True)

    gdf = gpd.GeoDataFrame(
        df,
        geometry=gpd.points_from_xy(df['lon'], df['lat'])
    )

    gdf = gdf.set_crs('EPSG:4326')
    gdf_regions = gdf_regions.to_crs('EPSG:4326')
    gdf_district = gdf_district.to_crs('EPSG:4326')

    COLs = ['first_name', 'last_name', 'nid', 'phone', 'bakery_id',
        'ownership_status', 'number_violations', 'second_fuel', 'city', 'lat',
        'lon', 'household_risk', 'bakers_risk', 'type_flour', 'type_bread',
        'bread_rations']
    gdf_joined_gdf_regions = gpd.sjoin(gdf, gdf_regions, how='left', predicate='within')
    gdf_joined_gdf_regions.drop_duplicates(subset=COLs, inplace=True)
    gdf_joined_gdf_district = gpd.sjoin(gdf, gdf_district, how='left', predicate='within')
    gdf_joined_gdf_district.drop_duplicates(subset=COLs, inplace=True)

    df['region'] = gdf_joined_gdf_district['region']
    df['district'] = gdf_joined_gdf_district['district']

    # Drop All NULL Value from Region & Lon District
    df.dropna(subset=['region', 'district'], inplace=True)
    
    # df['number_violations'] = df['number_violations'].fillna(0)

    COLs = ['first_name', 'last_name', 'ownership_status', 'second_fuel', 'city', 'household_risk', 'bakers_risk', 'type_bread', 'nid', 'phone', 'bakery_id']
    df[COLs] = df[COLs].astype(str)
    
    # Convert nid and phone to `str`
    df['nid'] = df['nid'].apply(lambda x: str(x).zfill(10))
    df['phone'] = df['phone'].apply(lambda x: str(x).zfill(11))

    COLs = ['number_violations', 'type_flour', 'bread_rations', 'region', 'district']
    df[COLs] = df[COLs].astype(int, errors='ignore')

    COLs = ['lat', 'lon']
    df[COLs] = df[COLs].astype(float)

    # Reset Index
    df.reset_index(drop=True, inplace=True)
    
    return df
    


@blueprint.route(rule='/database', methods=['POST', 'GET'])
@login_required
def home():
    form = BakeryForm()
    if form.validate_on_submit():
        bakery = Bakery(
            first_name = form.first_name.data,
            last_name = form.last_name.data,
            nid = form.nid.data,
            phone = form.phone.data,
            bakery_id = form.bakery_id.data,
            ownership_status = form.ownership_status.data,
            number_violations = form.number_violations.data,
            second_fuel = form.second_fuel.data,
            city = form.city.data,
            region = int(form.region.data),
            district = int(form.district.data),
            lat = form.lat.data,
            lon = form.lon.data,
            household_risk = form.household_risk.data,
            bakers_risk = form.bakers_risk.data,
            type_flour = int(form.type_flour.data),
            type_bread = form.type_bread.data,
            bread_rations = form.bread_rations.data,
        )
        db.session.add(bakery)
        db.session.commit()
        flash(message='رکورد جدید ایجاد گردید.', category='success')
        return redirect(location=url_for(endpoint='database.home'))
    return render_template(template_name_or_list='database/home.html', form=form)


@blueprint.route(rule='/api/database/table', methods=['GET'])
@login_required
def show_table():
    search = request.args.get('search', '')
    search = search.split()
    sort_by = request.args.get('sort_by', 'id')
    sort_order = request.args.get('sort_order', 'asc')
    page = int(request.args.get('page', 1))
    per_page = 10
    offset = (page - 1) * per_page
    
    columns = [column.name for column in Bakery.__table__.columns]
    filters = []
    for term in search:
        term_filter = or_(
            *[getattr(Bakery, column).ilike(f"%{term}%") for column in columns]
        )
        filters.append(term_filter)
        
    query = Bakery.query.filter(or_(*filters))
    
    if sort_by in Bakery.__table__.columns:
        if sort_order == 'desc':
            query = query.order_by(desc(getattr(Bakery, sort_by)))
        else:
            query = query.order_by(asc(getattr(Bakery, sort_by)))
    
    total_results = query.count()
    
    query = query.limit(per_page).offset(offset)
    
    results = query.all()
    
    result_list = [
        {column: getattr(result, column) for column in columns}
        for result in results
    ]
    
    return jsonify(
        {
            'data': result_list,
            'total_count': total_results,
            'per_page': per_page,
            'page': page
        }
    )


@blueprint.route(rule='/api/database/upload', methods=['POST'])
@login_required
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
                city=row['city'],
                region=row['region'],
                district=row['district'],
                lat=row['lat'],
                lon=row['lon'],
                household_risk=row['household_risk'],
                bakers_risk=row['bakers_risk'],
                type_flour=row['type_flour'],
                type_bread=row['type_bread'],
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
                    city=row['city'],
                    region=row['region'],
                    district=row['district'],
                    lat=row['lat'],
                    lon=row['lon'],
                    household_risk=row['household_risk'],
                    bakers_risk=row['bakers_risk'],
                    type_flour=row['type_flour'],
                    type_bread=row['type_bread'],
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
        return redirect(location=url_for(endpoint='database.home'))
    else:
        emit(warnings=warnings, message="\u274C فرمت فایل انتخابی حتما باید csv و نویسه کدگذاری آن utf-8 باشد!")
        return '', 204 
        # return redirect(location=url_for(endpoint='database.home'))



@blueprint.route('/api/database/delete/<int:id>', methods=['DELETE'])
@login_required
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
        bakery.type_flour = data.get('type_flour')
        bakery.type_bread = data.get('type_bread')
        bakery.bread_rations = data.get('bread_rations')
        db.session.commit()
        return jsonify({'message': 'Bakery Updated Successfully'})


@blueprint.route('/api/database/all_items', methods=['GET', 'POST'])
@login_required
def all_items():
    column = request.json.get('column')
    if column == "ownership_status":
        items = sorted([x[0] for x in db.session.query(OwnershipStatus.name).all()])
        return jsonify(items)
    if column == "second_fuel":
        items = sorted([x[0] for x in db.session.query(SecondFuel.name).all()])
        return jsonify(items)
    if column == "household_risk":
        items = sorted([x[0] for x in db.session.query(HouseholdRisk.name).all()])
        return jsonify(items)
    if column == "bakers_risk":
        items = sorted([x[0] for x in db.session.query(BakersRisk.name).all()])
        return jsonify(items)
    if column == "type_flour":
        items = sorted([x[0] for x in db.session.query(TypeFlour.name).all()])
        return jsonify(items)
    if column == "type_bread":
        items = sorted([x[0] for x in db.session.query(TypeBread.name).all()])
        return jsonify(items)


@blueprint.route('/api/database/add_category', methods=['GET', 'POST'])
@login_required
def add_category():
    column = request.json.get('column')
    new_category = request.json.get('new_category')
    
   
    if column == "ownership_status":
        items = [x[0] for x in db.session.query(OwnershipStatus.name).all()]
        if new_category not in items:               
            item = OwnershipStatus(name=new_category)
            db.session.add(item)
            db.session.commit()
            return jsonify({'message': 'آیتم با موفقیت اضافه شد!', 'type': 'success'})
        else:
            return jsonify({'message': 'آیتم تکراری می‌باشد!', 'type': 'danger'})
    
    if column == "second_fuel":
        items = [x[0] for x in db.session.query(SecondFuel.name).all()]
        if new_category not in items:               
            item = SecondFuel(name=new_category)
            db.session.add(item)
            db.session.commit()
            return jsonify({'message': 'آیتم با موفقیت اضافه شد!', 'type': 'success'})
        else:
            return jsonify({'message': 'آیتم تکراری می‌باشد!', 'type': 'danger'})
    
    if column == "household_risk":
        items = [x[0] for x in db.session.query(HouseholdRisk.name).all()]
        if new_category not in items:               
            item = HouseholdRisk(name=new_category)
            db.session.add(item)
            db.session.commit()
            return jsonify({'message': 'آیتم با موفقیت اضافه شد!', 'type': 'success'})
        else:
            return jsonify({'message': 'آیتم تکراری می‌باشد!', 'type': 'danger'})
    
    if column == "bakers_risk":
        items = [x[0] for x in db.session.query(BakersRisk.name).all()]
        if new_category not in items:               
            item = BakersRisk(name=new_category)
            db.session.add(item)
            db.session.commit()
            return jsonify({'message': 'آیتم با موفقیت اضافه شد!', 'type': 'success'})
        else:
            return jsonify({'message': 'آیتم تکراری می‌باشد!', 'type': 'danger'})
    
    if column == "type_flour":
        items = [x[0] for x in db.session.query(TypeFlour.name).all()]
        if new_category not in items:               
            item = TypeFlour(name=new_category)
            db.session.add(item)
            db.session.commit()
            return jsonify({'message': 'آیتم با موفقیت اضافه شد!', 'type': 'success'})
        else:
            return jsonify({'message': 'آیتم تکراری می‌باشد!', 'type': 'danger'})
    
    if column == "type_bread":
        items = [x[0] for x in db.session.query(TypeBread.name).all()]
        if new_category not in items:               
            item = TypeBread(name=new_category)
            db.session.add(item)
            db.session.commit()
            return jsonify({'message': 'آیتم با موفقیت اضافه شد!', 'type': 'success'})
        else:
            return jsonify({'message': 'آیتم تکراری می‌باشد!', 'type': 'danger'})
    
    jsonify({'message': 'مشخصه موجود نمی‌باشد!', 'type': 'danger'})