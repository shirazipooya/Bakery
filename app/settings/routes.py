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
    name='settings',
    import_name=__name__,
)


@blueprint.route('/settings', methods=['GET', 'POST'])
@login_required
def home():
    return render_template(template_name_or_list='settings/home.html')
    

@blueprint.route('/api/settings/all_items', methods=['GET', 'POST'])
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
    if column == "flour_types":
        items = sorted([x[0] for x in db.session.query(TypeFlour.name).all()])
        return jsonify(items)
    if column == "bread_types":
        items = sorted([x[0] for x in db.session.query(TypeBread.name).all()])
        return jsonify(items)


@blueprint.route('/api/settings/add_category', methods=['GET', 'POST'])
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
    
    if column == "flour_types":
        items = [x[0] for x in db.session.query(TypeFlour.name).all()]
        if new_category not in items:               
            item = TypeFlour(name=new_category)
            db.session.add(item)
            db.session.commit()
            return jsonify({'message': 'آیتم با موفقیت اضافه شد!', 'type': 'success'})
        else:
            return jsonify({'message': 'آیتم تکراری می‌باشد!', 'type': 'danger'})
    
    if column == "bread_types":
        items = [x[0] for x in db.session.query(TypeBread.name).all()]
        if new_category not in items:               
            item = TypeBread(name=new_category)
            db.session.add(item)
            db.session.commit()
            return jsonify({'message': 'آیتم با موفقیت اضافه شد!', 'type': 'success'})
        else:
            return jsonify({'message': 'آیتم تکراری می‌باشد!', 'type': 'danger'})
    
    jsonify({'message': 'مشخصه موجود نمی‌باشد!', 'type': 'danger'})