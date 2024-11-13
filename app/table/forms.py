from flask_wtf import FlaskForm
from wtforms import  StringField, IntegerField, FloatField, SelectField
from wtforms.validators import DataRequired, Length, ValidationError, Optional
from app.database.models import Bakery


class BakeryForm(FlaskForm):
    
    first_name = StringField(
        label='نام',
        validators=[
            # DataRequired(
            #     message="وارد کردن نام الزامیست!"
            # ),
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
            # DataRequired(),
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
            # DataRequired(),
            Length(
                min=10,
                max=10,
                message='10 رقم!'
            )
        ],
        render_kw={
            "placeholder": "0123456789"
        }
    )
    
    phone = StringField(
        label='تلفن همراه',
        validators=[
            # DataRequired(),
            Length(
                min=11,
                max=11,
                message='11 رقم!'
            )
        ],
        render_kw={
            "placeholder": "09151234567"
        }
    )
    
    bakery_id = StringField(
        label='شماره خبازی',
        validators=[
            # DataRequired(),
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
            # DataRequired(),
        ],
        choices=[
            ('', ''),
            ('مالک', 'مالک'),
            ('استیجاری', 'استیجاری'),
        ]
    )
    
    number_violations = IntegerField(
        label='تعداد تخلفات نانوایی',
        validators=[
            # DataRequired(),
        ],
        render_kw={
            "placeholder": "1"
        }
    )
    
    second_fuel = SelectField(
        label='سوخت دوم',
        validators=[
            # DataRequired(),
        ],
        choices=[
            ('', ''),
            ('ندارد', 'ندارد'),
            ('گازوئیل', 'گازوئیل'),
            ('نفت', 'نفت'),
        ]
    )
    
    city = SelectField(
        label='شهر',
        validators=[
            # DataRequired(),
        ],
        choices=[
            ('', ''),
            ('مشهد', 'مشهد'),
        ]
    )
    
    region = SelectField(
        label='منطقه',
        validators=[
            # DataRequired(),
        ],
        choices=[
            ('', ''),
            ('1', 'منطقه 1'),
            ('2', 'منطقه 2'),
            ('3', 'منطقه 3'),
            ('4', 'منطقه 4'),
            ('5', 'منطقه 5'),
            ('6', 'منطقه 6'),
            ('7', 'منطقه 7'),
            ('8', 'منطقه 8'),
            ('9', 'منطقه 9'),
            ('10', 'منطقه 10'),
            ('11', 'منطقه 11'),
            ('12', 'منطقه 12'),
            ('13', 'منطقه 13'),
        ]
    )
    
    district = SelectField(
        label='ناحیه',
        validators=[
            # DataRequired(),
        ],
        choices=[
            ('', ''),
            ('1', 'ناحیه 1'),
            ('2', 'ناحیه 2'),
            ('3', 'ناحیه 3'),
            ('4', 'ناحیه 4'),
            ('5', 'ناحیه 5'),
        ]
    )
    
    lat = FloatField(
        label='عرض جغرافیایی',
        validators=[
            Optional(),
            # DataRequired(),
        ],
        render_kw={
            "placeholder": "36.254687"
        }
    )
    
    lon = FloatField(
        label='طول جغرافیایی',
        validators=[
            Optional(),
            # DataRequired(),
        ],
        render_kw={
            "placeholder": "59.254687"
        }
    )
    
    household_risk = SelectField(
        label='ریسک خانوار',
        validators=[
            # DataRequired(),
        ],
        choices=[
            ('', ''),
            ('کم ریسک', 'کم ریسک'),
            ('ریسک متوسط', 'ریسک متوسط'),
            ('پرریسک', 'پرریسک'),
            ('خیلی پرریسک', 'خیلی پرریسک'),
        ]
    )
    
    bakers_risk = SelectField(
        label='ریسک نانوا',
        validators=[
            # DataRequired(),
        ],
        choices=[
            ('', ''),
            ('کم ریسک', 'کم ریسک'),
            ('ریسک متوسط', 'ریسک متوسط'),
            ('پرریسک', 'پرریسک'),
            ('خیلی پرریسک', 'خیلی پرریسک'),
        ]
    )

    
    type_bread = SelectField(
        label='نوع پخت',
        validators=[
            # DataRequired(),
        ],
        choices=[
            ('', ''),
            ('بربری', 'بربری'),
            ('سنگک', 'سنگک'),
            ('تافتون', 'تافتون'),
            ('لواش', 'لواش'),
        ]
    )
    
      
    type_flour = SelectField(
        label='نوع آرد',
        validators=[
            # DataRequired(),
        ],
        choices=[
            ('', ''),
            ('1', '1'),
            ('2', '2'),
            ('3', '3'),
            ('4', '4'),
            ('5', '5'),
            ('6', '6'),
        ]
    )
    
    bread_rations = IntegerField(
        label='سهمیه آرد',
        validators=[
            # DataRequired(),
        ],
        render_kw={
            "placeholder": "100"
        }
    )