from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Place(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    city = db.Column(db.String(255), nullable=False)
    zone = db.Column(db.String(255), nullable=False)
    state = db.Column(db.String(255), nullable=False)
    type = db.Column(db.String(255), nullable=False)
    establishment_year = db.Column(db.String(255))
    time_needed_to_visit = db.Column(db.String(255))
    google_review_rating = db.Column(db.String(255))
    entrance_fee = db.Column(db.String(255))
    weekly_off = db.Column(db.String(255))
    significance = db.Column(db.String(255))
    dslr_allowed = db.Column(db.String(255))
    number_of_google_reviews = db.Column(db.String(255))
    best_time_to_visit = db.Column(db.String(255))

    def to_dict(self):
        return {
            'Name': self.name,
            'Type': self.type,
            'City': self.city,
            'State': self.state,
            'Zone': self.zone,
            'Establishment Year': self.establishment_year,
            'time needed to visit in hrs': self.time_needed_to_visit,
            'Google review rating': self.google_review_rating,
            'Entrance Fee in INR': self.entrance_fee,
            'Weekly Off': self.weekly_off,
            'Significance': self.significance,
            'DSLR Allowed': self.dslr_allowed,
            'Number of google review in lakhs': self.number_of_google_reviews,
            'Best Time to visit': self.best_time_to_visit
        }
