

from flask import Flask, render_template, request, redirect
import pandas as pd

app = Flask(__name__)

# Function to load dataset
def load_data():
    return pd.read_csv('Top Indian Places to Visit.csv')

# Load the dataset
df = load_data()

# Function to get all place names
def get_place_names():
    return df['Name'].tolist()

@app.route('/', methods=['GET', 'POST'])
def index():
    global df
    recommendations = []
    selected_place_details = {}

    if request.method == 'POST':
        selected_place = request.form.get('place_name')

        if selected_place:
            # Get the selected place details
            place_info = df[df['Name'] == selected_place].iloc[0]
            selected_city = place_info['City']
            selected_zone = place_info['Zone']
            selected_state = place_info['State']

            # Save the selected place details to display it alongside recommendations
            selected_place_details = place_info.to_dict()

            # First, recommend places in the same state, city, and zone
            recommendations = df[(df['State'] == selected_state) & 
                                 (df['City'] == selected_city) & 
                                 (df['Zone'] == selected_zone) & 
                                 (df['Name'] != selected_place)]
            
            # If no results, recommend places in the same state and city (ignore zone)
            if recommendations.empty:
                recommendations = df[(df['State'] == selected_state) & 
                                     (df['City'] == selected_city) & 
                                     (df['Name'] != selected_place)]
            
            # If still no results, recommend places in the same state and zone (ignore city)
            if recommendations.empty:
                recommendations = df[(df['State'] == selected_state) & 
                                     (df['Zone'] == selected_zone) & 
                                     (df['Name'] != selected_place)]
            
            # If still no results, recommend places in the same state (ignore city and zone)
            if recommendations.empty:
                recommendations = df[df['State'] == selected_state & (df['Name'] != selected_place)]
            
            # Convert recommendations to a dictionary for rendering
            recommendations = recommendations.to_dict(orient='records')

    return render_template('index.html', place_names=get_place_names(), selected_place_details=selected_place_details, recommendations=recommendations)

@app.route('/add_place_form', methods=['GET'])
def add_place_form():
    return render_template('add_place.html')

@app.route('/add_place', methods=['POST'])
def add_place():
    global df
    new_place = {
        'Name': request.form['name'],
        'City': request.form['city'],
        'Zone': request.form['zone'],
        'State': request.form['state'],
        'Type': request.form['type'],
        'Establishment Year': int(request.form['establishment_year']),
        'time needed to visit in hrs': (request.form['time_needed']),
        'Google review rating': float(request.form['google_review_rating']),
        'Entrance Fee in INR': int(request.form['entrance_fee']),
        'Weekly Off': request.form['weekly_off'],
        'Significance': request.form['significance'],
        'DSLR Allowed': request.form['dslr_allowed'],
        'Number of google review in lakhs': float(request.form['google_reviews']),
        'Best Time to visit': request.form['best_time_to_visit']
    }
    
    # Convert new place dictionary to DataFrame
    new_place_df = pd.DataFrame([new_place])
    
    # Concatenate the new place DataFrame with the existing DataFrame
    df = pd.concat([df, new_place_df], ignore_index=True)
    
    # Save the updated DataFrame to CSV
    df.to_csv('Top Indian Places to Visit.csv', index=False)

    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
