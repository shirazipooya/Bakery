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


@blueprint.route(rule='/table', methods=['POST', 'GET'])
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
        return redirect(location=url_for(endpoint='table.home'))
    return render_template(template_name_or_list='table/home.html', form=form)


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




