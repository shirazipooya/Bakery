from flask import Blueprint, render_template
from flask_login import current_user, login_required


blueprint = Blueprint(
    name='dashboard',
    import_name=__name__,
)


@blueprint.route('/')
@login_required
def home():
    return render_template(template_name_or_list='dashboard/home.html')