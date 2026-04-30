from functools import wraps
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app, make_response, abort
from flask_login import login_user, logout_user, current_user, login_required
from datetime import datetime, date
from io import StringIO
import csv
from .models import Chemical, User
from . import db
from app import login_manager

bp = Blueprint('main', __name__)


def get_low_stock_threshold():
    return current_app.config.get('ALERT_THRESHOLD', 5)


def admin_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated:
            return login_manager.unauthorized()
        if current_user.role != 'admin':
            abort(403)
        return func(*args, **kwargs)
    return wrapper


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))

    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            login_user(user)
            flash('Logged in successfully.', 'success')
            next_page = request.args.get('next')
            return redirect(next_page or url_for('main.dashboard'))

        flash('Invalid username or password.', 'danger')

    return render_template('login.html')


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))

    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password']
        role = request.form.get('role', 'user')

        if User.query.filter_by(username=username).first():
            flash('Username already exists.', 'danger')
            return render_template('register.html')

        new_user = User(username=username, role=role)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        flash('Account created. Please log in.', 'success')
        return redirect(url_for('main.login'))

    return render_template('register.html')


@bp.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.login'))


@bp.route('/')
@login_required
def dashboard():
    total_chemicals = Chemical.query.count()
    low_stock_items = Chemical.query.filter(Chemical.quantity < get_low_stock_threshold()).all()
    expired_chemicals = Chemical.query.filter(Chemical.expiry_date < date.today()).all()
    alerts = []

    if low_stock_items:
        alerts.append(f"{len(low_stock_items)} chemical(s) are low in stock")
    if expired_chemicals:
        alerts.append(f"{len(expired_chemicals)} chemical(s) have expired")

    return render_template(
        'dashboard.html',
        total_chemicals=total_chemicals,
        low_stock_count=len(low_stock_items),
        expired_count=len(expired_chemicals),
        low_stock_items=low_stock_items,
        expired_chemicals=expired_chemicals,
        alerts=alerts,
        threshold=get_low_stock_threshold(),
        today=date.today()
    )


@bp.route('/chemicals')
@login_required
def chemicals():
    query = request.args.get('q', '').strip()
    chemicals_query = Chemical.query.order_by(Chemical.name)

    if query:
        chemicals_query = chemicals_query.filter(Chemical.name.ilike(f'%{query}%'))

    chemicals_list = chemicals_query.all()
    return render_template(
        'chemicals.html',
        chemicals=chemicals_list,
        query=query,
        threshold=get_low_stock_threshold(),
        today=date.today()
    )


@bp.route('/chemicals/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_chemical():
    if request.method == 'POST':
        name = request.form['name'].strip()
        quantity = float(request.form['quantity'])
        unit = request.form['unit'].strip()
        expiry_date = datetime.strptime(request.form['expiry_date'], '%Y-%m-%d').date()
        hazard_level = request.form['hazard_level'].strip()
        storage_location = request.form['storage_location'].strip()

        new_chemical = Chemical(
            name=name,
            quantity=quantity,
            unit=unit,
            expiry_date=expiry_date,
            hazard_level=hazard_level,
            storage_location=storage_location,
        )
        db.session.add(new_chemical)
        db.session.commit()
        flash('Chemical added successfully!', 'success')
        return redirect(url_for('main.chemicals'))

    return render_template('add_chemical.html')


@bp.route('/chemicals/<int:chemical_id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_chemical(chemical_id):
    chemical = Chemical.query.get_or_404(chemical_id)

    if request.method == 'POST':
        chemical.name = request.form['name'].strip()
        chemical.quantity = float(request.form['quantity'])
        chemical.unit = request.form['unit'].strip()
        chemical.expiry_date = datetime.strptime(request.form['expiry_date'], '%Y-%m-%d').date()
        chemical.hazard_level = request.form['hazard_level'].strip()
        chemical.storage_location = request.form['storage_location'].strip()

        db.session.commit()
        flash('Chemical updated successfully!', 'success')
        return redirect(url_for('main.chemicals'))

    return render_template('edit_chemical.html', chemical=chemical)


@bp.route('/chemicals/<int:chemical_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_chemical(chemical_id):
    chemical = Chemical.query.get_or_404(chemical_id)
    db.session.delete(chemical)
    db.session.commit()
    flash('Chemical deleted successfully!', 'success')
    return redirect(url_for('main.chemicals'))


@bp.route('/alerts')
@login_required
def alerts():
    low_stock_items = Chemical.query.filter(Chemical.quantity < get_low_stock_threshold()).all()
    expired_chemicals = Chemical.query.filter(Chemical.expiry_date < date.today()).all()
    return render_template(
        'alerts.html',
        low_stock=low_stock_items,
        expired_chemicals=expired_chemicals,
        threshold=get_low_stock_threshold(),
        today=date.today(),
    )


@bp.route('/export')
@login_required
@admin_required
def export_report():
    chemicals = Chemical.query.order_by(Chemical.name).all()
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow([
        'Name',
        'Quantity',
        'Unit',
        'Expiry Date',
        'Hazard Level',
        'Storage Location',
        'Status',
    ])

    for chemical in chemicals:
        status = 'Expired' if chemical.expiry_date < date.today() else 'OK'
        writer.writerow([
            chemical.name,
            chemical.quantity,
            chemical.unit,
            chemical.expiry_date.isoformat(),
            chemical.hazard_level,
            chemical.storage_location,
            status,
        ])

    response = make_response(output.getvalue())
    response.headers['Content-Disposition'] = 'attachment; filename=chemical_report.csv'
    response.headers['Content-Type'] = 'text/csv'
    return response


@bp.route('/chemicals/<int:chemical_id>/barcode')
@login_required
def barcode_page(chemical_id):
    chemical = Chemical.query.get_or_404(chemical_id)
    barcode_value = f"CHEM-{chemical.id:05d}"
    return render_template('barcode.html', chemical=chemical, barcode_value=barcode_value)


@bp.route('/scan', methods=['GET', 'POST'])
@login_required
def scan():
    chemical = None
    code = ''
    if request.method == 'POST':
        code = request.form.get('code', '').strip()
        wireless_code = code
        chemical_id = None

        if code.upper().startswith('CHEM-'):
            code = code.upper().replace('CHEM-', '')

        if code.isdigit():
            chemical_id = int(code)

        if chemical_id:
            chemical = Chemical.query.get(chemical_id)

        if not chemical and request.method == 'POST':
            flash('No chemical found for scanned code.', 'danger')

    return render_template('scan.html', chemical=chemical, code=wireless_code if 'wireless_code' in locals() else code)