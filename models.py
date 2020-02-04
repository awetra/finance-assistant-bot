from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    balance = db.Column(db.Numeric(10, 2), default=0)

    def __repr__(self):
        return f'<User({self.id})>'


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(190), unique=True, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('categories', lazy=True))

    def __repr__(self):
        return f'<Category({self.name})>'


class Cost(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    debit_date = db.Column(db.DateTime, nullable=False)
    
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    category = db.relationship('Category', backref=db.backref('costs', lazy=True))

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('costs', lazy=True))

    def __repr__(self):
        return f'<Cost({self.price}, {self.category.name})>'