import csv
import io
import os
from flask import Blueprint, render_template, flash, redirect, url_for, request, jsonify, Response
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
from sqlalchemy import distinct


from app.users.routes import role_required


blueprint = Blueprint(
    name='settings',
    import_name=__name__,
)


@blueprint.route('/settings', methods=['GET', 'POST'])
@login_required
@role_required('کاربر عادی')
def home():
    return render_template(template_name_or_list='settings/home.html')



@blueprint.route('/api/settings/download', methods=['GET'])
@login_required
@role_required('کاربر عادی')
def download_data():
    query = db.session.query(Bakery)
    df = pd.read_sql(str(query.statement), db.engine)
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Data')
    output.seek(0)

    # Return the Excel file as a response
    return Response(
        output,
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={
            "Content-Disposition": "attachment; filename=data.xlsx",
        },
    )
    # csv_data = df.to_csv(index=False, encoding='utf-8')
    # response = Response(
    #     csv_data,
    #     mimetype='text/csv',
    #     headers={
    #         'Content-Disposition': 'attachment;filename=data.csv',
    #         'Content-Type': 'text/csv; charset=utf-8'
    #     }
    # )
    # return response
    

@blueprint.route('/api/settings/all_items', methods=['GET', 'POST'])
@login_required
@role_required('کاربر عادی')
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
@role_required('کاربر عادی')
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


@blueprint.route('/api/settings/delete/<column>/<item>', methods=['DELETE'])
@login_required
@role_required('کاربر عادی')
def delete_item(column, item):
    
    if column == "ownership_status":
        items = Bakery.query.with_entities(distinct(Bakery.ownership_status)).all()
        items_list = [i[0] for i in items]
        if item in items_list:
            return jsonify({'message': 'آیتم مورد نظر در دیتابیس وجود دارد و شما قادر به حذف آن نیستید!', 'type': 'danger'})
        else:
            record = OwnershipStatus.query.filter_by(name=item).first()
            db.session.delete(record)
            db.session.commit()
            return jsonify({'message': 'آیتم با موفقیت حذف شد!', 'type': 'success'})
    
    if column == "second_fuel":
        items = Bakery.query.with_entities(distinct(Bakery.second_fuel)).all()
        items_list = [i[0] for i in items]
        if item in items_list:
            return jsonify({'message': 'آیتم مورد نظر در دیتابیس وجود دارد و شما قادر به حذف آن نیستید!', 'type': 'danger'})
        else:
            record = SecondFuel.query.filter_by(name=item).first()
            db.session.delete(record)
            db.session.commit()
            return jsonify({'message': 'آیتم با موفقیت حذف شد!', 'type': 'success'})
    
    if column == "household_risk":
        items = Bakery.query.with_entities(distinct(Bakery.household_risk)).all()
        items_list = [i[0] for i in items]
        if item in items_list:
            return jsonify({'message': 'آیتم مورد نظر در دیتابیس وجود دارد و شما قادر به حذف آن نیستید!', 'type': 'danger'})
        else:
            record = HouseholdRisk.query.filter_by(name=item).first()
            db.session.delete(record)
            db.session.commit()
            return jsonify({'message': 'آیتم با موفقیت حذف شد!', 'type': 'success'})
    
    if column == "bakers_risk":
        items = Bakery.query.with_entities(distinct(Bakery.bakers_risk)).all()
        items_list = [i[0] for i in items]
        if item in items_list:
            return jsonify({'message': 'آیتم مورد نظر در دیتابیس وجود دارد و شما قادر به حذف آن نیستید!', 'type': 'danger'})
        else:
            record = BakersRisk.query.filter_by(name=item).first()
            db.session.delete(record)
            db.session.commit()
            return jsonify({'message': 'آیتم با موفقیت حذف شد!', 'type': 'success'})
    
    if column == "flour_types":
        items = Bakery.query.with_entities(distinct(Bakery.flour_types)).all()
        items_list = [i[0] for i in items]
        if item in items_list:
            return jsonify({'message': 'آیتم مورد نظر در دیتابیس وجود دارد و شما قادر به حذف آن نیستید!', 'type': 'danger'})
        else:
            record = TypeFlour.query.filter_by(name=item).first()
            db.session.delete(record)
            db.session.commit()
            return jsonify({'message': 'آیتم با موفقیت حذف شد!', 'type': 'success'})
    
    if column == "bread_types":
        items = Bakery.query.with_entities(distinct(Bakery.bread_types)).all()
        items_list = [i[0] for i in items]
        if item in items_list:
            return jsonify({'message': 'آیتم مورد نظر در دیتابیس وجود دارد و شما قادر به حذف آن نیستید!', 'type': 'danger'})
        else:
            record = TypeBread.query.filter_by(name=item).first()
            db.session.delete(record)
            db.session.commit()
            return jsonify({'message': 'آیتم با موفقیت حذف شد!', 'type': 'success'})
    
    
    
    
    jsonify({'message': 'آیتم موجود نمی‌باشد!', 'type': 'danger'})