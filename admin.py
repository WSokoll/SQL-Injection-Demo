from flask import url_for, abort, redirect, request
from flask_admin.contrib.sqla import ModelView
from flask_admin.menu import MenuLink
from flask_login import current_user

import models


class UserModelView(ModelView):
    def is_accessible(self):
        if not current_user.is_active and not current_user.is_authenticated:
            return False

        roles_users = models.RolesUsers.query.filter_by(user_id=current_user.id).one_or_none()
        return roles_users is not None and models.Role.query.filter_by(id=roles_users.role_id).one_or_none() == 'Admin'

    def _handle_view(self, name, **kwargs):
        if not self.is_accessible():
            if current_user.is_authenticated:
                abort(403)
            else:
                return redirect(url_for('bp_auth.login'))

    can_view_details = True
    can_create = False
    can_edit = True
    can_delete = True
    column_list = [
        'email', 'active', 'create_datetime'
    ]
    column_details_list = [
        'email', 'active', 'current_login_at', 'current_login_ip', 'create_datetime', 'confirmed_at'
    ]
    form_columns = [
        'email', 'roles', 'active'
    ]
    column_labels = {
        'active': 'Aktywny',
        'current_login_at': 'Ostatnie logowanie',
        'current_login_ip': 'Ostatni adres IP',
        'create_datetime': 'Rejestracja',
        'confirmed_at': 'Aktywacja linkiem',
        'roles': 'Role'
    }


def admin_panel_init(admin, db):

    class LogoutLink(MenuLink):
        def get_url(self):
            return url_for("bp_auth.logout")

    class HomePageLink(MenuLink):
        def get_url(self):
            if not current_user.is_active and not current_user.is_authenticated:
                return url_for("bp_home.get")
            user = models.User.query.filter_by(id=current_user.id).one_or_none()
            return url_for("bp_account.get", account_id=user.account_id, currency_name='pln')

    admin.add_link(LogoutLink(name="Wyloguj się"))
    admin.add_link(HomePageLink(name="Konto"))

    admin.add_view(UserModelView(models.User, db.session, name='Użytkownicy'))

