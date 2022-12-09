from flask import url_for
from flask_admin.contrib.sqla import ModelView
from flask_admin.menu import MenuLink
from flask_login import current_user

import models


class UserModelView(ModelView):
    can_view_details = True
    can_create = False
    can_edit = True
    can_delete = True
    column_list = [
        'email', 'roles'
    ]
    column_details_list = [
        'email', 'roles'
    ]
    form_columns = [
        'email', 'roles'
    ]
    column_labels = {
        'roles': 'Role'
    }


def admin_panel_init(admin, db):

    class LogoutLink(MenuLink):
        def get_url(self):
            return url_for("bp_auth.logout")

    class HomePageLink(MenuLink):
        def get_url(self):
            user = models.User.query.filter_by(id=current_user.id).one_or_none()
            return url_for("bp_account.get", account_id=user.account_id, currency_name='pln')

    admin.add_link(LogoutLink(name="Wyloguj się"))
    admin.add_link(HomePageLink(name="Konto"))

    admin.add_view(UserModelView(models.User, db.session, name='Użytkownicy'))

