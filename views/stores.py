import json
from flask import Blueprint, render_template, request, redirect, url_for
from models.store import Store
from models.user import requires_login, requires_admin

store_bluprint = Blueprint('stores', __name__)


@store_bluprint.route('/')
@requires_login
def index():
    stores = Store.all()
    return render_template('stores/index.html', stores=stores)


@store_bluprint.route('/new', methods=['GET', 'POST'])
@requires_admin
def new_store():
    if request.method == 'POST':
        name = request.form['name']
        url_prefix = request.form['url_prefix']
        tag_name = request.form['tag_name']
        query = json.loads(request.form['query'])

        Store(name, url_prefix, tag_name, query).save_to_mongo()

    return render_template('stores/new_store.html')


@store_bluprint.route('/edit/<string:store_id>', methods=['GET', 'POST'])
@requires_admin
def edit_store(store_id):
    store = Store.get_by_id(store_id)

    if request.method == 'POST':
        store.url_prefix = request.form['url_prefix']
        store.tag_name = request.form['tag_name']
        store.query = json.loads(request.form['query'])
        store.save_to_mongo()

        return redirect(url_for('.index'))

    return render_template('stores/edit_store.html', store=store)


@store_bluprint.route('/delete/<string:store_id>')
@requires_admin
def delete_store(store_id):
    Store.get_by_id(store_id).remove_from_mongo()
    return redirect(url_for('.index'))
