from flask import render_template


def page_not_found(e):
    return render_template(template_name_or_list='exceptions/404.html'), 404


def server_error(e):
    return render_template(template_name_or_list='exceptions/500.html'), 500


def unauthorized(e):
    return render_template(template_name_or_list='exceptions/401.html'), 401