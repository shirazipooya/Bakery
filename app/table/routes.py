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
    name='table',
    import_name=__name__,
)

# ==============================================================================
# Load Pages
# ==============================================================================
@blueprint.route(rule='/table', methods=['POST', 'GET'])
@login_required
def home():
    query = OwnershipStatus.query.with_entities(OwnershipStatus.name).distinct()
    items = query.all()
    ownership_status_options = sorted([item[0] for item in items])
    
    query = SecondFuel.query.with_entities(SecondFuel.name).distinct()
    items = query.all()
    second_fuel_options = sorted([item[0] for item in items])
    
    query = HouseholdRisk.query.with_entities(HouseholdRisk.name).distinct()
    items = query.all()
    household_risk_options = sorted([item[0] for item in items])
    
    query = BakersRisk.query.with_entities(BakersRisk.name).distinct()
    items = query.all()
    bakers_risk_options = sorted([item[0] for item in items])
    
    query = TypeFlour.query.with_entities(TypeFlour.name).distinct()
    items = query.all()
    type_flour_options = sorted([item[0] for item in items])
    
    query = TypeBread.query.with_entities(TypeBread.name).distinct()
    items = query.all()
    type_bread_options = sorted([item[0] for item in items])
    
    
    excluded_columns = {"id", "city", "created_at", "updated_at"}
    
    table_columns = {
        key: value for key, value in Bakery.verbose_names.items() if key not in excluded_columns
    }
    
    print(table_columns)
    
    data={
        "ownership_status_options": ownership_status_options,
        "second_fuel_options": second_fuel_options,
        "household_risk_options": household_risk_options,
        "bakers_risk_options": bakers_risk_options,
        "type_flour_options": type_flour_options,
        "type_bread_options": type_bread_options,
        "table_columns": table_columns
    }
    
    return render_template(
        template_name_or_list='table/home.html',
        data=data
    )


# ==============================================================================
# API
# ==============================================================================
@blueprint.route(rule='/api/table/headers', methods=['GET'])
@login_required
def get_table_headers():
    headers = [
        {"field": key, "label": value} for key, value in Bakery.verbose_names.items()
    ]
    return jsonify(headers)



@blueprint.route(rule='/api/table/data', methods=['GET'])
@login_required
def get_table_data():
    selected_column = request.args.get('column', 'all')
    search = request.args.get('search', '')
    search = search.split()
    sort_by = request.args.get('sort_by', 'id')
    sort_order = request.args.get('sort_order', 'asc')
    page = int(request.args.get('page', 1))
    per_page = 10
    offset = (page - 1) * per_page
    
    if selected_column == "all":
        columns = [column.name for column in Bakery.__table__.columns]
    else:
        columns = [selected_column]
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
    
    columns = [column.name for column in Bakery.__table__.columns]
    
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


@blueprint.route('/api/table/delete/<int:id>', methods=['DELETE'])
@login_required
def delete_record(id):
    record = Bakery.query.get(id)
    if record:
        db.session.delete(record)
        db.session.commit()
        return jsonify({"message": f"نانوایی با شماره ردیف {id} با موفقیت از پایگاه داده حذف شد!"}), 200
    else:
        return jsonify({"error": f"نانوایی با شماره ردیف {id} پیدا نشد"}), 404


@blueprint.route('/api/table/update/<int:id>', methods=['GET', 'POST'])
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
        bakery.household_risk = data.get('household_risk')
        bakery.bakers_risk = data.get('bakers_risk')
        bakery.flour_types = data.get('flour_types')
        bakery.bread_types = data.get('bread_types')
        bakery.bread_rations = data.get('bread_rations')
        db.session.commit()
        return jsonify({'message': 'Bakery Updated Successfully'})