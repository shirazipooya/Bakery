from flask_wtf import FlaskForm
from wtforms import  StringField, IntegerField, FloatField, SelectField
from wtforms.validators import DataRequired, Length, ValidationError, Optional
# from app.database.models import Bakery, OwnershipStatus, SecondFuel, HouseholdRisk, BakersRisk, TypeFlour, TypeBread
from shapely.geometry import Point
import geopandas as gpd

def validate_phone_start(form, field):
    if not field.data.startswith('09'):
        raise ValidationError('شماره تلفن باید با 09 شروع شود!')


def validate_iranian_national_code(form, field):
    code = field.data
    code_len = len(code)
    
    if code_len > 10 or code_len < 8:
        raise ValidationError('کد ملی میتواند 8 تا 10 رقم باشد!')

    if len(set(code)) == 1:
        raise ValidationError('همه ارقام کدملی نمیتواند یکسان باشد!')

    if len(code) < 10:
        code = code.zfill(10)

    factors = [10, 9, 8, 7, 6, 5, 4, 3, 2]
    checksum = sum(int(code[i]) * factors[i] for i in range(len(code) - 1))
    remainder = checksum % 11
    last_digit = int(code[-1])

    if remainder < 2:
        if remainder != last_digit:
            raise ValidationError('کدملی اشتباه وارد شده است!')  
    else:
        if 11 - remainder != last_digit:
            raise ValidationError('کدملی اشتباه وارد شده است!') 


def validate_lat_lon(form, field):
    gdf_bakhsh = gpd.read_file('app/assets/data/geodatabase/Bakhsh.geojson')
    point = Point(float(form.lon.data), float(form.lat.data))
    containing_feature = gdf_bakhsh[gdf_bakhsh.geometry.apply(lambda geom: geom.contains(point))]
    if containing_feature.empty:
        raise ValidationError('طول و عرض جغرافیایی وارد شده در محدوده استان، شهرستان و بخش دیتابیس موجود نمی باشد!') 

          
class BakeryForm(FlaskForm):
    
    first_name = StringField(
        label='نام',
        validators=[
            DataRequired(
                message="وارد کردن نام الزامیست!"
            ),
            Length(
                # min=2,
                max=30,
                message='حداکثر 30 کاراکتر!'
            )
        ],
        render_kw={
            "placeholder": "پویا"
        }
    )
    
    last_name = StringField(
        label='نام خانوادگی',
        validators=[
            DataRequired(
                message="وارد کردن نام خانوادگی الزامیست!"
            ),
            Length(
                # min=2,
                max=30,
                message='حداکثر 30 کاراکتر!'
            )
        ],
        render_kw={
            "placeholder": "شیرازی"
        }
    )
    
    nid = StringField(
        label='کدملی',
        validators=[
            DataRequired(
                message="وارد کردن کدملی الزامیست!"
            ),
            validate_iranian_national_code
        ],
        render_kw={
            "placeholder": "0123456789"
        }
    )
    
    phone = StringField(
        label='تلفن همراه',
        validators=[
            DataRequired(
                message="وارد کردن تلفن همراه الزامیست!"    
            ),
            Length(
                min=11,
                max=11,
                message='11 رقم!'
            ),
            validate_phone_start
        ],
        render_kw={
            "placeholder": "09151234567"
        }
    )
    
    bakery_id = StringField(
        label='شماره خبازی',
        validators=[
            DataRequired(
                message="وارد کردن شماره خبازی الزامیست!"
            ),
            Length(
                # min=11,
                max=30,
                message='حداکثر 30 کاراکتر!'
            )
        ],
        render_kw={
            "placeholder": "1122334455"
        }
    )
    
    ownership_status = SelectField(
        label='نوع ملک نانوایی',
        validators=[
            DataRequired(),
        ],
    )
    
    number_violations = IntegerField(
        label='تعداد تخلفات نانوایی',
        validators=[
            DataRequired(
                message="وارد کردن تعداد تخلفات نانوایی الزامیست!"
            ),
        ],
        render_kw={
            "placeholder": "1"
        }
    )
    
    second_fuel = SelectField(
        label='سوخت دوم',
        validators=[
            DataRequired(),
        ],
    )

    
    lat = FloatField(
        label='عرض جغرافیایی',
        validators=[
            # Optional(),
            DataRequired(
                message="وارد کردن عرض جغرافیایی الزامیست!"
            ),
            validate_lat_lon
        ],
        render_kw={
            "placeholder": "36.254687"
        }
    )
    
    lon = FloatField(
        label='طول جغرافیایی',
        validators=[
            # Optional(),
            DataRequired(
                message="وارد کردن طول جغرافیایی الزامیست!"
            ),
            validate_lat_lon
        ],
        render_kw={
            "placeholder": "59.254687"
        }
    )
    
    household_risk = SelectField(
        label='ریسک خانوار',
        validators=[
            DataRequired(),
        ],
    )
    
    bakers_risk = SelectField(
        label='ریسک نانوا',
        validators=[
            DataRequired(),
        ],
    )

    
    bread_types = SelectField(
        label='نوع پخت',
        validators=[
            DataRequired(),
        ],
    )
    
      
    flour_types = SelectField(
        label='نوع آرد',
        validators=[
            DataRequired(),
        ],
    )
    
    bread_rations = IntegerField(
        label='سهمیه آرد',
        validators=[
            DataRequired(
                message="وارد کردن سهمیه آرد الزامیست!"
            ),
        ],
        render_kw={
            "placeholder": "100"
        }
    )