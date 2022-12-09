from flask import Blueprint, render_template, abort, flash
from flask_login import login_required
from flask_wtf import FlaskForm
from sqlalchemy import or_, and_
from wtforms import StringField
from wtforms.validators import InputRequired, Regexp

from models import SubAccount, Currency, User, InternalTransaction, CurrencyExchange, ExternalTransaction

bp = Blueprint('bp_account', __name__, template_folder='templates')


# Show account page
@bp.route('/account/<int:account_id>/<string:currency_name>', methods=['GET', 'POST'])
@login_required
def get(account_id, currency_name='pln'):

    currency = Currency.query.filter_by(name=currency_name).first()
    if not currency:
        abort(404)

    sub_account = SubAccount.query.filter_by(account_id=account_id, currency_id=currency.id).first()
    if not sub_account:
        abort(404)

    # currency names list
    sub_accounts = SubAccount.query.filter_by(account_id=account_id).all()
    currency_list = []
    for sa in sub_accounts:
        cur = Currency.query.filter_by(id=sa.currency_id).first()
        currency_list.append(cur.name)

    # transaction and exchange history
    user = User.query.filter_by(account_id=account_id).first()

    in_transactions = InternalTransaction.query.filter(or_(and_(InternalTransaction.transaction_from == user.id,
                                                                InternalTransaction.currency_id == currency.id),
                                                           and_(InternalTransaction.transaction_to == user.id,
                                                                InternalTransaction.currency_id == currency.id))).\
        order_by(InternalTransaction.transaction_date).all()

    ex_transactions = ExternalTransaction.query.filter(and_(ExternalTransaction.transaction_to == user.id,
                                                            ExternalTransaction.currency_id == currency.id))

    exchanges = CurrencyExchange.query.filter(or_(and_(CurrencyExchange.user_id == user.id,
                                                       CurrencyExchange.currency_from == currency.id),
                                                  and_(CurrencyExchange.user_id == user.id,
                                                       CurrencyExchange.currency_to == currency.id))).\
        order_by(CurrencyExchange.exchange_date).all()

    history = []
    history.extend(in_transactions)
    history.extend(ex_transactions)
    history.extend(exchanges)
    history.sort(key=lambda x: x.transaction_date if hasattr(x, 'transaction_date') else x.exchange_date, reverse=True)

    # External transaction - disabled
    class ExternalTransactionForm(FlaskForm):
        value = StringField('Kwota doładowania', validators=[InputRequired(), Regexp(r'^[0-9.]{1,}[.][0-9][0-9]$')])

    form = ExternalTransactionForm()

    if form.validate_on_submit():
        flash('Funkcjonalość została wyłączona.')

    elif form.is_submitted():
        for field_name, errors in form.errors.items():
            for err in errors:
                flash(f"{form._fields[field_name].label.text}: {err}", 'error')

    return render_template('account.html', currency=currency, sub_account=sub_account, currency_list=currency_list,
                           history=history, form=form)
