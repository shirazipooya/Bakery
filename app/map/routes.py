from flask import Blueprint, render_template, jsonify
from flask_login import current_user, login_required
import pandas as pd
from app.database.models import Bakery, Amarnameh, TypeBread, TypeFlour, SecondFuel, BakersRisk, HouseholdRisk, OwnershipStatus
from app.extensions import db, cache
from sqlalchemy import distinct
from sqlalchemy import func
from sqlalchemy.orm import aliased


blueprint = Blueprint(
    name='map',
    import_name=__name__,
)


# ==============================================================================
# Load Page
# ==============================================================================

# ------------------------------------------------------------------------------
# Home Page
# ------------------------------------------------------------------------------
@blueprint.route('/home')
@login_required
def home():
    return render_template(template_name_or_list='map/home.html')



# ==============================================================================
# API
# ==============================================================================

# ------------------------------------------------------------------------------
# Get Ostan Options
# ------------------------------------------------------------------------------
@blueprint.route(rule='/api/map/ostan', methods=['GET'])
@login_required
def get_ostan_options():
    query = Bakery.query.with_entities(Bakery.ostan).distinct()
    items = query.all()
    data = sorted([item[0] for item in items])
    return jsonify(data)

# ------------------------------------------------------------------------------
# Get Shahrestan Options
# ------------------------------------------------------------------------------
@blueprint.route('/api/map/shahrestan/<ostan>', methods=["GET"])
@login_required
def get_shahrestan_options(ostan):
    query = Bakery.query.with_entities(distinct(Bakery.shahrestan)).filter(Bakery.ostan == ostan)
    items = query.all()
    data = sorted([item[0] for item in items])
    return jsonify(data)

# ------------------------------------------------------------------------------
# Get Bakhsh Options
# ------------------------------------------------------------------------------
@blueprint.route('/api/map/bakhsh/<shahrestan>/<ostan>', methods=["GET"])
@login_required
def get_bakhsh_options(shahrestan, ostan):
    query = Bakery.query.with_entities(distinct(Bakery.bakhsh)).filter(Bakery.ostan == ostan, Bakery.shahrestan == shahrestan)
    items = query.all()
    data = sorted([item[0] for item in items])
    return jsonify(data)

# ------------------------------------------------------------------------------
# Get Shahr Options
# ------------------------------------------------------------------------------
@blueprint.route('/api/map/shahr/<bakhsh>/<shahrestan>/<ostan>', methods=["GET"])
@login_required
def get_shahr_options(bakhsh, shahrestan, ostan):
    query = Bakery.query.with_entities(distinct(Bakery.shahr)).filter(Bakery.ostan == ostan, Bakery.shahrestan == shahrestan, Bakery.bakhsh == bakhsh)
    items = query.all()
    data = sorted([item[0] for item in items])
    return jsonify(data)

# ------------------------------------------------------------------------------
# Get Region Options
# ------------------------------------------------------------------------------
@blueprint.route('/api/map/region/<shahr>/<bakhsh>/<shahrestan>/<ostan>', methods=["GET"])
@login_required
def get_region_options(shahr, bakhsh, shahrestan, ostan):
    query = Bakery.query.with_entities(distinct(Bakery.region)).filter(Bakery.ostan == ostan, Bakery.shahrestan == shahrestan, Bakery.bakhsh == bakhsh, Bakery.shahr == shahr)
    items = query.all()
    data = sorted([item[0] for item in items])
    return jsonify(data)

# ------------------------------------------------------------------------------
# Get District Options
# ------------------------------------------------------------------------------
@blueprint.route('/api/map/district/<region>/<shahr>/<bakhsh>/<shahrestan>/<ostan>', methods=["GET"])
@login_required
def get_district_options(region, shahr, bakhsh, shahrestan, ostan):
    query = Bakery.query.with_entities(distinct(Bakery.district)).filter(Bakery.ostan == ostan, Bakery.shahrestan == shahrestan, Bakery.bakhsh == bakhsh, Bakery.shahr == shahr, Bakery.region == region)
    items = query.all()
    data = sorted([item[0] for item in items])
    return jsonify(data)

# ------------------------------------------------------------------------------
# Get Bread Types Options
# ------------------------------------------------------------------------------
@blueprint.route(rule='/api/map/bread_types', methods=['GET'])
@login_required
def get_bread_types_options():
    query = TypeBread.query.with_entities(TypeBread.name).distinct()
    items = query.all()
    data = sorted([item[0] for item in items])
    return jsonify(data)

# ------------------------------------------------------------------------------
# Get Flour Types Options
# ------------------------------------------------------------------------------
@blueprint.route(rule='/api/map/flour_types', methods=['GET'])
@login_required
def get_flour_types_options():
    query = TypeFlour.query.with_entities(TypeFlour.name).distinct()
    items = query.all()
    data = sorted([item[0] for item in items])
    return jsonify(data)

# ------------------------------------------------------------------------------
# Get Second Fuel Options
# ------------------------------------------------------------------------------
@blueprint.route(rule='/api/map/second_fuel', methods=['GET'])
@login_required
def get_second_fuel_options():
    query = SecondFuel.query.with_entities(SecondFuel.name).distinct()
    items = query.all()
    data = sorted([item[0] for item in items])
    return jsonify(data)

# ------------------------------------------------------------------------------
# Get Bakers Risk Options
# ------------------------------------------------------------------------------
@blueprint.route(rule='/api/map/bakers_risk', methods=['GET'])
@login_required
def get_bakers_risk_options():
    query = BakersRisk.query.with_entities(BakersRisk.name).distinct()
    items = query.all()
    data = sorted([item[0] for item in items])
    return jsonify(data)

# ------------------------------------------------------------------------------
# Get Household Risk Options
# ------------------------------------------------------------------------------
@blueprint.route(rule='/api/map/household_risk', methods=['GET'])
@login_required
def get_household_risk_options():
    query = HouseholdRisk.query.with_entities(HouseholdRisk.name).distinct()
    items = query.all()
    data = sorted([item[0] for item in items])
    return jsonify(data)

# ------------------------------------------------------------------------------
# Get Ownership Status Options
# ------------------------------------------------------------------------------
@blueprint.route(rule='/api/map/ownership_status', methods=['GET'])
@login_required
def get_ownership_status_options():
    query = OwnershipStatus.query.with_entities(OwnershipStatus.name).distinct()
    items = query.all()
    data = sorted([item[0] for item in items])
    return jsonify(data)

# ------------------------------------------------------------------------------
# Load Map Data
# ------------------------------------------------------------------------------
@blueprint.route(rule='/api/map/data/<ostan>/<shahrestan>/<bakhsh>/<shahr>/<region>/<district>/<bread_types>/<flour_types>/<second_fuel>/<bakers_risk>/<household_risk>/<ownership_status>', methods=["GET"])
@login_required
def load_map_data(ostan, shahrestan, bakhsh, shahr, region, district, bread_types, flour_types, second_fuel, bakers_risk, household_risk, ownership_status):
    
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
    if shahr != "999":
        filters_bakery.append(Bakery.shahr == shahr)
    if region != "999":
        filters_bakery.append(Bakery.region == region)
    if district != "999":
        filters_bakery.append(Bakery.district == district)    
    if bread_types != "999":
        filters_bakery.append(Bakery.bread_types == bread_types)
    if flour_types != "999":
        filters_bakery.append(Bakery.flour_types == flour_types)
    if second_fuel != "999":
        filters_bakery.append(Bakery.second_fuel == second_fuel)
    if bakers_risk != "999":
        filters_bakery.append(Bakery.bakers_risk == bakers_risk)
    if household_risk != "999":
        filters_bakery.append(Bakery.household_risk == household_risk)
    if ownership_status != "999":
        filters_bakery.append(Bakery.ownership_status == ownership_status)
           
    if filters_bakery:
        query_bakery = query_bakery.filter(*filters_bakery)
    
    # --------------------------------------------------------------------------
    # Filter Amarnameh
    # --------------------------------------------------------------------------
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
    # Return
    # --------------------------------------------------------------------------  
    data = [
        {column: getattr(record, column) for column in record.__table__.columns.keys()}
        for record in query_bakery.all()
    ]
    
    number_of_bakeries = query_bakery.count()    
    
    response = {
        'data': data,
        'number_of_bakeries': number_of_bakeries,
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
        
#         bread_types_cat = df.groupby("bread_types")["bread_types"].count().to_dict()
#         bread_types_cat = {k: int(v) for k, v in bread_types_cat.items()}
        
#         flour_types_cat = df.groupby("flour_types")["flour_types"].count().to_dict()
#         flour_types_cat = {k: int(v) for k, v in flour_types_cat.items()}
        
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
#             'bread_types_cat': bread_types_cat,
#             'flour_types_cat': flour_types_cat,
#             'bakers_risk_cat': bakers_risk_cat,
#             'household_risk_cat': household_risk_cat,
#             'bread_rations_cat': bread_rations_cat,
#             'region_info': region_info,
#             'region_bread_rations': region_bread_rations
#         }
        
#         return jsonify(response)
#     except Exception as e:
#         return jsonify({"error": str(e)})


# @blueprint.route('/api/dashboard/sunburst/<option>', methods=["GET"])
# @login_required
# def sunburst_data(option):
#     try:
#         selected_column = option
#         query = Bakery.query.all()
#         data = [
#             {
#                 column: getattr(record, column) for column in record.__table__.columns.keys()
#             } for record in query
#         ]    
#         data = pd.DataFrame(data)[['city', 'region', 'district', selected_column]]

#         def build_hierarchy(data, keys):
#             if not keys:
#                 return {'size': len(data)}
#             result = []
#             for key, group in data.groupby(keys[0]):
                
#                 if key in list(data[selected_column].unique()):
#                     result.append({
#                         'name': key,
#                         'size': len(group[selected_column])
#                     })
#                 else:
#                     result.append({
#                         'name': key,
#                         'children': build_hierarchy(group, keys[1:]) if len(keys) > 1 else len(group[selected_column])
#                     })                
#             return result

#         hierarchy = build_hierarchy(data, ['city', 'region', 'district', selected_column])

#         hierarchical_json = {'name': 'Root', 'children': hierarchy}
        
#         return jsonify(hierarchical_json)
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
#         filters.append(Bakery.bread_types == typebread)

#     if typeflour != "999":
#         filters.append(Bakery.flour_types == typeflour)

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


# @blueprint.route(rule='/api/dashboard/bread_types', methods=['GET'])
# @login_required
# def bread_types_data():
#     query = Bakery.query.with_entities(Bakery.bread_types).distinct()
#     bread_types = query.all()
#     data = sorted([tb[0] for tb in bread_types])
#     return jsonify(data)

# @blueprint.route(rule='/api/dashboard/flour_types', methods=['GET'])
# @login_required
# def flour_types_data():
#     query = Bakery.query.with_entities(Bakery.flour_types).distinct()
#     flour_types = query.all()
#     data = sorted([tb[0] for tb in flour_types])
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
#     return data[['region', 'district', 'ratio', 'ration']].to_json(orient='records')