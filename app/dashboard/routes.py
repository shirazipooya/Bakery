from flask import Blueprint, render_template, jsonify
from flask_login import current_user, login_required
import pandas as pd
from app.database.models import Bakery, Amarnameh
from app.extensions import db, cache
from sqlalchemy import distinct
from sqlalchemy import func
from sqlalchemy.orm import aliased


blueprint = Blueprint(
    name='dashboard',
    import_name=__name__,
)

# ==============================================================================
# Load Page
# ==============================================================================

# ------------------------------------------------------------------------------
# Home Page
# ------------------------------------------------------------------------------
@blueprint.route('/')
@login_required
def home():
    return render_template(template_name_or_list='dashboard/home.html')


# ==============================================================================
# API
# ==============================================================================

# ------------------------------------------------------------------------------
# Get Ostan Options
# ------------------------------------------------------------------------------
@blueprint.route(rule='/api/dashboard/ostan', methods=['GET'])
@login_required
def get_ostan_options():
    query = Bakery.query.with_entities(Bakery.ostan).distinct()
    items = query.all()
    data = sorted([item[0] for item in items])
    return jsonify(data)

# ------------------------------------------------------------------------------
# Get Shahrestan Options
# ------------------------------------------------------------------------------
@blueprint.route('/api/dashboard/shahrestan/<ostan>', methods=["GET"])
@login_required
def get_shahrestan_options(ostan):
    query = Bakery.query.with_entities(distinct(Bakery.shahrestan)).filter(Bakery.ostan == ostan)
    items = query.all()
    data = sorted([item[0] for item in items])
    return jsonify(data)

# ------------------------------------------------------------------------------
# Get Bakhsh Options
# ------------------------------------------------------------------------------
@blueprint.route('/api/dashboard/bakhsh/<shahrestan>/<ostan>', methods=["GET"])
@login_required
def get_bakhsh_options(shahrestan, ostan):
    query = Bakery.query.with_entities(distinct(Bakery.bakhsh)).filter(Bakery.ostan == ostan, Bakery.shahrestan == shahrestan)
    items = query.all()
    data = sorted([item[0] for item in items])
    return jsonify(data)

# ------------------------------------------------------------------------------
# Get Shahr/Rosta Options
# ------------------------------------------------------------------------------
@blueprint.route('/api/dashboard/shahrrosta/<bakhsh>/<shahrestan>/<ostan>', methods=["GET"])
@login_required
def get_shahr_rosta_options(bakhsh, shahrestan, ostan):
    query = Bakery.query.with_entities(distinct(Bakery.shahr)).filter(Bakery.ostan == ostan, Bakery.shahrestan == shahrestan, Bakery.bakhsh == bakhsh)
    items = query.all()
    data = sorted([item[0] for item in items])
    return jsonify(data)

# ------------------------------------------------------------------------------
# Get Mantagheh Options
# ------------------------------------------------------------------------------
@blueprint.route('/api/dashboard/mantagheh/<shahrrosta>/<bakhsh>/<shahrestan>/<ostan>', methods=["GET"])
@login_required
def get_mantagheh_options(shahrrosta, bakhsh, shahrestan, ostan):
    query = Bakery.query.with_entities(distinct(Bakery.region)).filter(Bakery.ostan == ostan, Bakery.shahrestan == shahrestan, Bakery.bakhsh == bakhsh, Bakery.shahr == shahrrosta)
    items = query.all()
    data = sorted([item[0] for item in items])
    return jsonify(data)

# ------------------------------------------------------------------------------
# Get Nahyeh Options
# ------------------------------------------------------------------------------
@blueprint.route('/api/dashboard/nahyeh/<mantagheh>/<shahrrosta>/<bakhsh>/<shahrestan>/<ostan>', methods=["GET"])
@login_required
def get_nahyeh_options(mantagheh, shahrrosta, bakhsh, shahrestan, ostan):
    query = Bakery.query.with_entities(distinct(Bakery.district)).filter(Bakery.ostan == ostan, Bakery.shahrestan == shahrestan, Bakery.bakhsh == bakhsh, Bakery.shahr == shahrrosta, Bakery.region == mantagheh)
    items = query.all()
    data = sorted([item[0] for item in items])
    return jsonify(data)

# ------------------------------------------------------------------------------
# Load Dashboard Data
# ------------------------------------------------------------------------------
@blueprint.route(rule='/api/dashboard/data/<ostan>/<shahrestan>/<bakhsh>/<shahrRosta>/<mantagheh>/<nahyeh>', methods=["GET"])
@login_required
def load_dashboard_data(ostan, shahrestan, bakhsh, shahrRosta, mantagheh, nahyeh):
    
    # --------------------------------------------------------------------------
    # Filter Database
    # --------------------------------------------------------------------------
    query_bakery = Bakery.query
    
    filters_bakery = []    
    if ostan != "999":
        filters_bakery.append(Bakery.ostan == ostan)
    if shahrestan != "999":
        filters_bakery.append(Bakery.shahrestan == shahrestan)
    if bakhsh != "999":
        filters_bakery.append(Bakery.bakhsh == bakhsh)
    if shahrRosta != "999":
        filters_bakery.append(Bakery.shahr == shahrRosta)
    if mantagheh != "999":
        filters_bakery.append(Bakery.region == mantagheh)
    if nahyeh != "999":
        filters_bakery.append(Bakery.district == nahyeh)    
    if filters_bakery:
        query_bakery = query_bakery.filter(*filters_bakery)
    
    unique_bakery_combinations = query_bakery.with_entities(
        Bakery.ostan,
        Bakery.shahrestan,
        Bakery.bakhsh,
        Bakery.shahr,
        Bakery.region,
        Bakery.district
    ).distinct().subquery()
    
    unique_alias = aliased(unique_bakery_combinations)
    
    query_amarnameh = Amarnameh.query.filter(
        Amarnameh.ostan == unique_alias.c.ostan,
        Amarnameh.shahrestan == unique_alias.c.shahrestan,
        Amarnameh.bakhsh == unique_alias.c.bakhsh,
        Amarnameh.shahr == unique_alias.c.shahr,
        Amarnameh.region == unique_alias.c.region,
        Amarnameh.district == unique_alias.c.district
    )
    
    # --------------------------------------------------------------------------
    # 
    # --------------------------------------------------------------------------
    number_of_bakeries = query_bakery.count()
    number_of_households = query_amarnameh.with_entities(func.sum(Amarnameh.n_households)).scalar() or 0
    area = query_amarnameh.with_entities(func.sum(Amarnameh.area)).scalar() or 0
    population = query_amarnameh.with_entities(func.sum(Amarnameh.population)).scalar() or 0
    population_male = query_amarnameh.with_entities(func.sum(Amarnameh.population_male)).scalar() or 0
    population_female = query_amarnameh.with_entities(func.sum(Amarnameh.population_female)).scalar() or 0
    population_number_of_bakeries = round(number=population / number_of_bakeries, ndigits=0) if number_of_bakeries > 0 else "-"
    households_number_of_bakeries = round(number=number_of_households / number_of_bakeries, ndigits=0) if number_of_bakeries > 0 else "-"
    area_number_of_bakeries = round(number=area / number_of_bakeries, ndigits=0) if number_of_bakeries > 0 and area != 0 else "-"
    population_bread_rations = round(number=(query_bakery.with_entities(func.sum(Bakery.bread_rations)).scalar() * 100) / population, ndigits=0) or 0
    response = {
        'number_of_bakeries': number_of_bakeries,
        'number_of_households': number_of_households ,
        'area': area if area != 0 else "-" ,
        'population': population ,
        'population_male': population_male ,
        'population_female': population_female ,
        'population_number_of_bakeries': population_number_of_bakeries,
        'households_number_of_bakeries': households_number_of_bakeries,
        'area_number_of_bakeries': area_number_of_bakeries,
        'population_bread_rations': population_bread_rations,
    }
    
    return jsonify(response)













# @blueprint.route('/api/dashboard/data/<option>', methods=["GET"])
# @login_required
# def load_data(option):
    
#     try: 
#         if option == "0":
#             query = Bakery.query.all()
#             region_bread_rations = db.session.query(
#                 func.sum(Bakery.bread_rations)
#             ).scalar()
#         else:
#             query = Bakery.query.filter_by(region=int(option))
#             region_bread_rations = db.session.query(
#                 func.sum(Bakery.bread_rations)
#             ).filter_by(region=int(option)).scalar()
        
#         data = [
#             {
#                 column: getattr(record, column) for column in record.__table__.columns.keys()
#             } for record in query
#         ]
        
#         df = pd.DataFrame(data)
        
#         type_bread_cat = df.groupby("type_bread")["type_bread"].count().to_dict()
#         type_bread_cat = {k: int(v) for k, v in type_bread_cat.items()}
        
#         type_flour_cat = df.groupby("type_flour")["type_flour"].count().to_dict()
#         type_flour_cat = {k: int(v) for k, v in type_flour_cat.items()}
        
#         bakers_risk_cat = df.groupby("bakers_risk")["bakers_risk"].count().to_dict()
#         bakers_risk_cat = {k: int(v) for k, v in bakers_risk_cat.items()}
            
#         household_risk_cat = df.groupby("household_risk")["household_risk"].count().to_dict()
#         household_risk_cat = {k: int(v) for k, v in household_risk_cat.items()}
        
#         bins = list(range(0, 700, 100))
#         df['category'] = pd.cut(df['bread_rations'], bins=bins, right=False)
#         category_counts = df['category'].value_counts().sort_index()   
#         bread_rations_cat = pd.DataFrame(category_counts).reset_index(drop=False).to_dict()['count']
#         bread_rations_cat = {k: int(v) for k, v in bread_rations_cat.items()}
        
        
#         # Second Database
        
#         query = Amarnameh.query.filter_by(region=int(option))
#         region_info = [
#             {
#                 column: getattr(record, column) for column in record.__table__.columns.keys()
#             } for record in query
#         ]
        
        
#         response = {
#             'data': data,
#             'number_of_row': len(data),
#             'type_bread_cat': type_bread_cat,
#             'type_flour_cat': type_flour_cat,
#             'bakers_risk_cat': bakers_risk_cat,
#             'household_risk_cat': household_risk_cat,
#             'bread_rations_cat': bread_rations_cat,
#             'region_info': region_info,
#             'region_bread_rations': region_bread_rations
#         }
        
#         return jsonify(response)
#     except Exception as e:
#         return jsonify({"error": str(e)})



# @blueprint.route(rule='/api/dashboard/cities', methods=['GET'])
# @login_required
# def cities_data():
#     query = Bakery.query.with_entities(Bakery.city).distinct()
#     cities = query.all()
#     data = sorted([city[0] for city in cities])
#     return jsonify(data)


# @blueprint.route('/api/dashboard/regions/<city>', methods=["GET"])
# @login_required
# def regions_data(city):
#     query = Bakery.query.with_entities(distinct(Bakery.region)).filter(Bakery.city == city)
#     regions = query.all()
#     data = sorted([region[0] for region in regions])
#     return jsonify(data)

# @blueprint.route('/api/dashboard/districts/<city>/<region>', methods=["GET"])
# @login_required
# def districts_data(city, region):
#     query = Bakery.query.with_entities(distinct(Bakery.district)).filter(Bakery.city == city, Bakery.region == region)
#     districts = query.all()
#     data = sorted([district[0] for district in districts])
#     return jsonify(data)


# @blueprint.route('/api/dashboard/map/data/', methods=["GET"])
# @login_required
# def load_map_data():
    
#     query = Bakery.query.all()
    
#     data = [
#         {
#             column: getattr(record, column) for column in record.__table__.columns.keys()
#         } for record in query
#     ]
    
#     response = {
#         'data': data,
#     }
    
#     return jsonify(response)


# @blueprint.route(rule='/api/dashboard/map/filter/<city>/<region>/<district>/<typebread>/<typeflour>/<secondfuel>', methods=['GET'])
# @login_required
# def get_filtered_data(city, region, district, typebread, typeflour, secondfuel):
#     query = Bakery.query
    
#     filters = []
    
#     if city != "999":
#         filters.append(Bakery.city == city)

#     if region != "999":
#         filters.append(Bakery.region == region)

#     if district != "999":
#         filters.append(Bakery.district == district)

#     if typebread != "999":
#         filters.append(Bakery.type_bread == typebread)

#     if typeflour != "999":
#         filters.append(Bakery.type_flour == typeflour)

#     if secondfuel != "999":
#         filters.append(Bakery.second_fuel == secondfuel)
        
    

#     if filters:
#         query = query.filter(*filters)

#     query = query.all()
    
#     data = [
#         {column: getattr(record, column) for column in record.__table__.columns.keys()}
#         for record in query
#     ]
        
#     response = {
#         'data': data,
#     }
    
#     return jsonify(response)


# @blueprint.route(rule='/api/dashboard/type_bread', methods=['GET'])
# @login_required
# def type_bread_data():
#     query = Bakery.query.with_entities(Bakery.type_bread).distinct()
#     type_bread = query.all()
#     data = sorted([tb[0] for tb in type_bread])
#     return jsonify(data)

# @blueprint.route(rule='/api/dashboard/type_flour', methods=['GET'])
# @login_required
# def type_flour_data():
#     query = Bakery.query.with_entities(Bakery.type_flour).distinct()
#     type_flour = query.all()
#     data = sorted([tb[0] for tb in type_flour])
#     return jsonify(data)

# @blueprint.route(rule='/api/dashboard/second_fuel', methods=['GET'])
# @login_required
# def second_fuel_data():
#     query = Bakery.query.with_entities(Bakery.second_fuel).distinct()
#     second_fuel = query.all()
#     data = sorted([sf[0] for sf in second_fuel])
#     return jsonify(data)


# population_data_region = pd.read_csv('./app/assets/data/mashhad_amarnameh_region.csv', dtype=float)
# population_data_district = pd.read_csv('./app/assets/data/mashhad_amarnameh_district.csv', dtype=float)

# def region_ratio_query():
    
#     data = db.session.query(
#         Bakery.region,
#         func.count(Bakery.id)
#     ).group_by(Bakery.region).all()
    
#     region_bakery_counts = pd.DataFrame(data, columns=['region', 'bakery_count'])
    
#     data = db.session.query(
#         Bakery.region,
#         func.sum(Bakery.bread_rations)
#     ).group_by(Bakery.region).all()
    
#     region_bread_rations = pd.DataFrame(data, columns=['region', 'bread_rations'])
    
#     return {
#         "region_bakery_counts": region_bakery_counts,
#         "region_bread_rations": region_bread_rations
#     }  


# @blueprint.route('/api/dashboard/map/region_ratio', methods=['GET'])
# @login_required
# def region_ratio():
#     region_bakery_counts = region_ratio_query().get("region_bakery_counts")
#     region_bread_rations = region_ratio_query().get("region_bread_rations")
#     data = pd.merge(population_data_region, region_bakery_counts, on='region', how='left').fillna(0)
#     data = pd.merge(data, region_bread_rations, on='region', how='left').fillna(0)
#     data['ratio'] = data['population'] / data['bakery_count']
#     data['ration'] = (data['bread_rations'] * 100) / data['population']
    
#     # Return the ratio data as JSON
#     return data[['region', 'ratio', 'ration']].to_json(orient='records')



# def district_ratio_query():
    
#     data = db.session.query(
#         Bakery.region,
#         Bakery.district,
#         func.count(Bakery.id)
#     ).group_by(Bakery.region, Bakery.district).all()
    
#     district_bakery_counts = pd.DataFrame(data, columns=['region', 'district', 'bakery_count'])
    
#     data = db.session.query(
#         Bakery.region,
#         Bakery.district,
#         func.sum(Bakery.bread_rations)
#     ).group_by(Bakery.region, Bakery.district).all()
    
#     district_bread_rations = pd.DataFrame(data, columns=['region', 'district', 'bread_rations'])
    
#     return {
#         "district_bakery_counts": district_bakery_counts,
#         "district_bread_rations": district_bread_rations
#     }
    
# @blueprint.route('/api/dashboard/map/district_ratio', methods=['GET'])
# @login_required
# def district_ratio():
#     district_bakery_counts = district_ratio_query().get("district_bakery_counts")
#     district_bread_rations = district_ratio_query().get("district_bread_rations")
#     data = pd.merge(population_data_district, district_bakery_counts, on=['region', 'district'], how='left').fillna(0)
#     data = pd.merge(data, district_bread_rations, on=['region', 'district'], how='left').fillna(0)
#     data['ratio'] = data['population'] / data['bakery_count']
#     data['ration'] = (data['bread_rations'] * 100) / data['population']
    
#     # Return the ratio data as JSON
    return data[['region', 'district', 'ratio', 'ration']].to_json(orient='records')