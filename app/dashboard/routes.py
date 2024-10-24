from flask import Blueprint, render_template, jsonify
from flask_login import current_user, login_required
import pandas as pd
from app.database.models import Bakery
from sqlalchemy import distinct


blueprint = Blueprint(
    name='dashboard',
    import_name=__name__,
)


@blueprint.route('/')
@login_required
def home():
    return render_template(template_name_or_list='dashboard/home.html')


@blueprint.route('/api/dashboard/data/<option>', methods=["GET"])
@login_required
def load_data(option):
       
    if option == "0":
        query = Bakery.query.all()
    else:
        query = Bakery.query.filter_by(region=int(option))
    
    data = [
        {
            column: getattr(record, column) for column in record.__table__.columns.keys()
        } for record in query
    ]
    
    df = pd.DataFrame(data)
    
    type_bread_cat = df.groupby("type_bread")["type_bread"].count().to_dict()
    type_bread_cat = {k: int(v) for k, v in type_bread_cat.items()}
    
    type_flour_cat = df.groupby("type_flour")["type_flour"].count().to_dict()
    type_flour_cat = {k: int(v) for k, v in type_flour_cat.items()}
    
    bakers_risk_cat = df.groupby("bakers_risk")["bakers_risk"].count().to_dict()
    bakers_risk_cat = {k: int(v) for k, v in bakers_risk_cat.items()}
        
    household_risk_cat = df.groupby("household_risk")["household_risk"].count().to_dict()
    household_risk_cat = {k: int(v) for k, v in household_risk_cat.items()}
    
    bins = list(range(0, 700, 100))
    df['category'] = pd.cut(df['bread_rations'], bins=bins, right=False)
    category_counts = df['category'].value_counts().sort_index()   
    bread_rations_cat = pd.DataFrame(category_counts).reset_index(drop=False).to_dict()['count']
    bread_rations_cat = {k: int(v) for k, v in bread_rations_cat.items()}
    
    
    response = {
        'data': data,
        'number_of_row': len(data),
        'type_bread_cat': type_bread_cat,
        'type_flour_cat': type_flour_cat,
        'bakers_risk_cat': bakers_risk_cat,
        'household_risk_cat': household_risk_cat,
        'bread_rations_cat': bread_rations_cat
    }
    
    return jsonify(response)


@blueprint.route('/api/dashboard/sunburst/<option>', methods=["GET"])
@login_required
def sunburst_data(option):
    selected_column = option
    query = Bakery.query.all()
    data = [
        {
            column: getattr(record, column) for column in record.__table__.columns.keys()
        } for record in query
    ]    
    data = pd.DataFrame(data)[['city', 'region', 'district', selected_column]]

    def build_hierarchy(data, keys):
        if not keys:
            return {'size': len(data)}
        result = []
        for key, group in data.groupby(keys[0]):
            
            if key in list(data[selected_column].unique()):
                result.append({
                    'name': key,
                    'size': len(group[selected_column])
                })
            else:
                result.append({
                    'name': key,
                    'children': build_hierarchy(group, keys[1:]) if len(keys) > 1 else len(group[selected_column])
                })                
        return result

    hierarchy = build_hierarchy(data, ['city', 'region', 'district', selected_column])

    hierarchical_json = {'name': 'Root', 'children': hierarchy}
    
    return jsonify(hierarchical_json)


@blueprint.route(rule='/api/dashboard/cities', methods=['GET'])
@login_required
def cities_data():
    query = Bakery.query.with_entities(Bakery.city).distinct()
    cities = query.all()
    data = sorted([city[0] for city in cities])
    return jsonify(data)


@blueprint.route('/api/dashboard/regions/<city>', methods=["GET"])
@login_required
def regions_data(city):
    query = Bakery.query.with_entities(distinct(Bakery.region)).filter(Bakery.city == city)
    regions = query.all()
    data = sorted([region[0] for region in regions])
    return jsonify(data)

@blueprint.route('/api/dashboard/districts/<city>/<region>', methods=["GET"])
@login_required
def districts_data(city, region):
    query = Bakery.query.with_entities(distinct(Bakery.district)).filter(Bakery.city == city, Bakery.region == region)
    districts = query.all()
    data = sorted([district[0] for district in districts])
    return jsonify(data)


@blueprint.route('/api/dashboard/map/data/', methods=["GET"])
@login_required
def load_map_data():
    
    query = Bakery.query.all()
    
    data = [
        {
            column: getattr(record, column) for column in record.__table__.columns.keys()
        } for record in query
    ]
    
    response = {
        'data': data,
    }
    
    return jsonify(response)


@blueprint.route(rule='/api/dashboard/map/filter/<city>/<region>/<district>/<typebread>/<typeflour>/<secondfuel>', methods=['GET'])
@login_required
def get_filtered_data(city, region, district, typebread, typeflour, secondfuel):
    query = Bakery.query
    
    filters = []
    
    if city != "999":
        filters.append(Bakery.city == city)

    if region != "999":
        filters.append(Bakery.region == region)

    if district != "999":
        filters.append(Bakery.district == district)

    if typebread != "999":
        filters.append(Bakery.type_bread == typebread)

    if typeflour != "999":
        filters.append(Bakery.type_flour == typeflour)

    if secondfuel != "999":
        filters.append(Bakery.second_fuel == secondfuel)
        
    

    if filters:
        query = query.filter(*filters)

    query = query.all()
    
    data = [
        {column: getattr(record, column) for column in record.__table__.columns.keys()}
        for record in query
    ]
        
    response = {
        'data': data,
    }
    
    return jsonify(response)


@blueprint.route(rule='/api/dashboard/type_bread', methods=['GET'])
@login_required
def type_bread_data():
    query = Bakery.query.with_entities(Bakery.type_bread).distinct()
    type_bread = query.all()
    data = sorted([tb[0] for tb in type_bread])
    return jsonify(data)

@blueprint.route(rule='/api/dashboard/type_flour', methods=['GET'])
@login_required
def type_flour_data():
    query = Bakery.query.with_entities(Bakery.type_flour).distinct()
    type_flour = query.all()
    data = sorted([tb[0] for tb in type_flour])
    return jsonify(data)

@blueprint.route(rule='/api/dashboard/second_fuel', methods=['GET'])
@login_required
def second_fuel_data():
    query = Bakery.query.with_entities(Bakery.second_fuel).distinct()
    second_fuel = query.all()
    data = sorted([sf[0] for sf in second_fuel])
    return jsonify(data)
