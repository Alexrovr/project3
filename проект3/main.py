from flask import Flask, render_template, redirect, request
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

from data import db_session
from data.add_book import AddBookForm
from data.book import LBookForm
from data.login_form import LoginForm
from data.users import User
from data.books import Books
from data.reviews import Reviews
from data.register import RegisterForm
from data.index import IndexForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html', message="Wrong login or password", form=form)
    return render_template('login.html', title='Authorization', form=form)


@app.route("/",  methods=['GET', 'POST'])
def index():
    form = IndexForm()
    db_sess = db_session.create_session()
    books = db_sess.query(Books).all()
    users = db_sess.query(User).all()
    reviews = db_sess.query(Reviews).all()
    names = {name.id: (name.surname, name.name) for name in users}
    if form.validate_on_submit():
        return render_template("index.html", books=books, names=names, fb=form.fbook.data, title='Bookshelf', form=form)
    return render_template("index.html", books=books, names=names, fb="", title='Bookshelf', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Register', form=form,
                                   message="Passwords don't match")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Register', form=form,
                                   message="This user already exists")
        user = User(
            name=form.name.data,
            surname=form.surname.data,
            age=form.age.data,
            email=form.email.data,
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)



@app.route('/addbook', methods=['GET', 'POST'])
def addbook():
    add_form = AddBookForm()
    if add_form.validate_on_submit():
        db_sess = db_session.create_session()
        books = Books(
            name=add_form.name.data,
            author=add_form.author.data
        )
        db_sess.add(books)
        db_sess.commit()
        return redirect('/')
    return render_template('addbook.html', title='Adding a book', form=add_form)


def main():
    db_session.global_init("db/mars_explorer.sqlite")

    app.run()


@app.route('/books/<int:id>', methods=['GET', 'POST'])
def lbook(id):
    add_form = LBookForm()
    db_sess = db_session.create_session()
    books = db_sess.query(Books).all()
    users = db_sess.query(User).all()
    reviews = db_sess.query(Reviews).all()
    if add_form.validate_on_submit():
        review = Reviews(
            text=add_form.text.data,
            user=current_user.id,
            book=id)
        db_sess.add(review)
        db_sess.commit()
        return redirect(f'/books/{id}')
    if current_user.is_authenticated:
        sid = current_user.id
    else:
        sid = -1
    return render_template("book.html", books=books, users=users, reviews=reviews, id=id, sid=sid, form=add_form)

    

@app.route('/books/editbook/<int:id>', methods=['GET', 'POST'])
@login_required
def job_edit(id):
    form = AddBookForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        books = db_sess.query(Books).filter(Books.id == id).first()
        if books:
            form.name.data = books.name
            form.author.data = books.author
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        books = db_sess.query(Books).filter(Books.id == id).first()
        if books:
            books.name = form.name.data
            books.author = form.author.data
            db_sess.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template('addbook.html', title='Book Edit', form=form)


if __name__ == '__main__':
    main()