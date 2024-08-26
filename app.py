from flask import Flask, render_template, request, redirect, url_for
from config import Config
from model import db, Place

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

@app.before_first_request
def create_tables():
    with app.app_context():
        db.create_all()

@app.route('/', methods=['GET', 'POST'])
def index():
    recommendations = []
    selected_place_details = {}

    if request.method == 'POST':
        selected_place = request.form.get('place_name')
        place_info = Place.query.filter_by(name=selected_place).first()

        if place_info:
            selected_city = place_info.City
            selected_zone = place_info.Zone
            selected_state = place_info.State

            selected_place_details = place_info.to_dict()

            recommendations = Place.query.filter(
                (Place.state == selected_state) & 
                (Place.city == selected_city) & 
                (Place.zone == selected_zone) & 
                (Place.name != selected_place)
            ).all()

            if not recommendations:
                recommendations = Place.query.filter(
                    (Place.state == selected_state) & 
                    (Place.city == selected_city) & 
                    (Place.name != selected_place)
                ).all()

            if not recommendations:
                recommendations = Place.query.filter(
                    (Place.state == selected_state) & 
                    (Place.zone == selected_zone) & 
                    (Place.name != selected_place)
                ).all()

            recommendations = [place.to_dict() for place in recommendations]

    place_names = [place.name for place in Place.query.all()]
    return render_template('index.html', place_names=place_names, selected_place_details=selected_place_details, recommendations=recommendations)

@app.route('/add_place', methods=['GET', 'POST'])
def add_place():
    if request.method == 'POST':
        new_place = Place(
            name=request.form.get('name'),
            city=request.form.get('city'),
            zone=request.form.get('zone'),
            state=request.form.get('state'),
            type=request.form.get('type'),
            establishment_year=request.form.get('establishment_year'),
            time_needed_to_visit=request.form.get('time_needed_to_visit'),
            google_review_rating=request.form.get('google_review_rating'),
            entrance_fee=request.form.get('entrance_fee'),
            weekly_off=request.form.get('weekly_off'),
            significance=request.form.get('significance'),
            dslr_allowed=request.form.get('dslr_allowed'),
            number_of_google_reviews=request.form.get('number_of_google_reviews'),
            best_time_to_visit=request.form.get('best_time_to_visit')
        )
        
        db.session.add(new_place)
        db.session.commit()
        
        return redirect(url_for('index'))

    return render_template('add_place.html')

if __name__ == '__main__':
    app.run(debug=True)
