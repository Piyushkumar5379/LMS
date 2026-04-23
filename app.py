from flask import Flask, render_template, url_for, flash, redirect, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, Book, BorrowRecord
from forms import RegistrationForm, LoginForm, BookForm
from datetime import datetime
from pyngrok import ngrok

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here_change_in_production'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def home():
    books = Book.query.all()
    return render_template('index.html', books=books)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        is_admin = form.email.data == 'admin@library.com'  # Simple admin check
        user = User(username=form.username.data, email=form.email.data, password_hash=hashed_password, is_admin=is_admin)
        db.session.add(user)
        db.session.commit()
        flash('Account created successfully!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password_hash, form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/add_book', methods=['GET', 'POST'])
@login_required
def add_book():
    if not current_user.is_admin:
        flash('Access denied.', 'danger')
        return redirect(url_for('home'))
    form = BookForm()
    if form.validate_on_submit():
        book = Book(title=form.title.data, author=form.author.data, isbn=form.isbn.data, quantity=form.quantity.data, available_quantity=form.quantity.data)
        db.session.add(book)
        db.session.commit()
        flash('Book added successfully!', 'success')
        return redirect(url_for('home'))
    return render_template('add_book.html', form=form)

@app.route('/borrow/<int:book_id>', methods=['POST'])
@login_required
def borrow_book(book_id):
    book = Book.query.get_or_404(book_id)
    if book.available_quantity > 0:
        borrow_record = BorrowRecord(user_id=current_user.id, book_id=book_id)
        book.available_quantity -= 1
        db.session.add(borrow_record)
        db.session.commit()
        flash('Book borrowed successfully!', 'success')
    else:
        flash('Book not available.', 'danger')
    return redirect(url_for('home'))

@app.route('/return/<int:record_id>', methods=['POST'])
@login_required
def return_book(record_id):
    record = BorrowRecord.query.get_or_404(record_id)
    if record.user_id == current_user.id and not record.is_returned:
        record.return_date = datetime.utcnow()
        record.is_returned = True
        record.book.available_quantity += 1
        db.session.commit()
        flash('Book returned successfully!', 'success')
    else:
        flash('Invalid return request.', 'danger')
    return redirect(url_for('profile'))

@app.route('/profile')
@login_required
def profile():
    borrow_records = BorrowRecord.query.filter_by(user_id=current_user.id).all()
    return render_template('profile.html', borrow_records=borrow_records)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    # Create ngrok tunnel
    public_url = ngrok.connect(5000)
    print(f"Public URL: {public_url}")
    print("Share this URL with others to access your website!")
    app.run(host='127.0.0.1', port=5000, debug=True)