from flask import Blueprint, render_template, redirect, url_for, flash, request
from app.users.forms import RegistrationForm, LoginForm
from app.users.models import User
from app.extensions import db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required
from functools import wraps


blueprint = Blueprint(
    name='users',
    import_name=__name__,
)


def role_required(required_role):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if current_user.role == required_role:
                # Redirect to a page that you want users with the given role to go
                return redirect(url_for('users.forbidden'))  # For example, a forbidden page
            return func(*args, **kwargs)
        return wrapper
    return decorator


@blueprint.route('/forbidden')
def forbidden():
    return render_template(template_name_or_list='exceptions/403.html')


@blueprint.route('/register', methods=['POST', 'GET'])
@login_required
@role_required('کاربر عادی')
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(
            first_name = form.first_name.data,
            last_name = form.last_name.data,
            username = form.username.data,
            password = hashed_password,
            phone = form.phone.data,
            role = form.role.data,
        )
        db.session.add(user)
        db.session.commit()
        flash(message='حساب کاربری شما با موفقیت ایجاد گردید.', category='success')
        return redirect(location=url_for(endpoint='users.login'))
    return render_template(template_name_or_list='users/register.html', form=form)
    

@blueprint.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(location=url_for('dashboard.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user=user, remember=form.remember.data)
            next_page = request.args.get('next')
            # flash(message='شما با موفقیت وارد شده‌اید!', category='success')
            return redirect(location=next_page if next_page else url_for(endpoint='dashboard.home'))
        else:
            flash(message='نام کاربری یا گذرواژه شما اشتباه می‌باشد!', category='danger')
            return redirect(location=url_for(endpoint='users.login'))           
            
        
    return render_template(template_name_or_list='users/login.html', form=form)


@blueprint.route('/logout')
@login_required
def logout():
	logout_user()
	flash('شما با موفقیت از حساب کاربری خود خارج شدید!', 'success')
	return redirect(url_for('users.login'))