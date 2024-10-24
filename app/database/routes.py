import csv
import io
import os
from flask import Blueprint, render_template, flash, redirect, url_for, request, jsonify
from app.database.forms import BakeryForm
from app.database.models import Bakery
from app.extensions import db
from sqlalchemy import or_, asc, desc
import pandas as pd
import geopandas as gpd
from sqlalchemy.exc import IntegrityError
from flask_login import current_user, login_required


blueprint = Blueprint(
    name='database',
    import_name=__name__,
)


def clean_csv_file(df):
    gdf_regions = gpd.read_file('app/assets/data/geodatabase/Region.geojson')
    gdf_district = gpd.read_file('app/assets/data/geodatabase/District.geojson')
    
    COLs = ['first_name', 'last_name', 'ownership_status', 'second_fuel', 'city', 'household_risk', 'bakers_risk', 'type_bread', 'nid', 'phone', 'bakery_id']
    df[COLs] = df[COLs].astype(str)
    df[COLs] = df[COLs].apply(lambda x: x.str.rstrip())
    df[COLs] = df[COLs].apply(lambda x: x.str.lstrip())
    df[COLs] = df[COLs].apply(lambda x: x.str.replace(' +', ' '))
    df[COLs] = df[COLs].apply(lambda x: x.str.replace('ي','ی'))
    df[COLs] = df[COLs].apply(lambda x: x.str.replace('ئ','ی'))
    df[COLs] = df[COLs].apply(lambda x: x.str.replace('ك', 'ک'))

    COLs = ['number_violations', 'type_flour', 'bread_rations']
    df[COLs] = df[COLs].astype(int, errors='ignore')

    COLs = ['lat', 'lon']
    df[COLs] = df[COLs].astype(float)

    # Drop All NULL Value from Lat & Lon Columns
    df.dropna(subset=['lat', 'lon'], inplace=True)

    # Remove All Duplicates Row
    df.drop_duplicates(inplace=True)

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
        return 'No selected file'
    
    if file and file.filename.endswith('.csv'):
        file_path = os.path.join('uploads', file.filename)
        file.save(file_path)
        data = clean_csv_file(pd.read_csv(file_path, dtype=str))
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
    flash(message='فقط فایل با فرمت *.csv قابل قبول است!', category='danger')
    return redirect(location=url_for(endpoint='database.home'))



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