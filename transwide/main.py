import datetime
import boto3
from flask import *
from flask_login import login_required, current_user, logout_user
import random
from . import db as debe
from .models import *

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/dashboard')
@login_required
def dashboard():
    return render_template('dash.html', name=current_user.name)

@main.route('/rquotation')
@login_required
def rquotation():
    quotation_id = random.randint(111, 999)
    today = datetime.datetime.now()
    d = today.strftime("%m/%d/%Y")
    return render_template('rquo.html', quotation_id=quotation_id, name=current_user.name, d = d)

@main.route('/rquotation', methods=['POST'])
@login_required
def rquotation_post():
    quotation_id = request.form.get('quotation_id')
    creator = request.form.get('creator')
    date_created = request.form.get('date_created')

    item_name = request.form.getlist('item_name[]')
    item_quantity = request.form.getlist('item_quantity[]')





    items = list(zip(item_name, item_quantity))

    ####################################################################
    import psycopg2
    import pandas as pd
    from sqlalchemy import create_engine

    conn_string = "postgresql://postgres:123456@localhost:5432/transwide"
    db = create_engine(conn_string)
    conn = db.connect()

    data = {'creator': creator, 'quotation_id' : pd.to_numeric(quotation_id), 'date': date_created,  'item_name' : item_name, 'item_quantity':item_quantity}

    #create dataframe
    df = pd.DataFrame(data)
    df.to_sql('quotations', con=conn, if_exists='append', index=False)
    connn = psycopg2.connect(conn_string)
    connn.autocommit = True
    connn.commit()
    connn.close()

    ######################################################################

    allq = AllQ(creator=creator, quotation_id=quotation_id, date=date_created)

    debe.session.add(allq)
    debe.session.commit()

    return redirect(url_for('main.quotations'))


@main.route('/quotations')
@login_required
def quotations():
    data = AllQ.query.filter_by(creator=current_user.name).all()
    items = Quotations.query.filter_by(creator=current_user.name).all()
    return render_template('quotations.html', data=data, items=items)

@main.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))



@main.route('/admin')
def console():
    return render_template('admin.html')

@main.route('/recieved')
def recieved():
    items = Quotations.query.all()
    return render_template('admin_quotations.html', items=items)


