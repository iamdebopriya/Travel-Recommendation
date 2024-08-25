from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

# Load the dataset
df = pd.read_csv('Top Indian Places to Visit.csv')

# Get all place names for the dropdown
place_names = df['Name'].tolist()

@app.route('/', methods=['GET', 'POST'])
def index():
    recommendations = []
    selected_place_details = {}
    
    if request.method == 'POST':
        selected_place = request.form.get('place_name')
        
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
        
        # Convert recommendations to a dictionary for rendering
        recommendations = recommendations.to_dict(orient='records')

    return render_template('index.html', place_names=place_names, selected_place_details=selected_place_details, recommendations=recommendations)

if __name__ == '__main__':
    app.run(debug=True)
