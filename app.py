import json
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# File to store functions
DATA_FILE = 'functions.json'

# Function to read data from JSON file
def read_data():
    try:
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

# Function to write data to JSON file
def write_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

# Home route to list all functions
#@app.route('/')
#def home():
#    functions = read_data()
#    return render_template('home.html', functions=functions)

@app.route('/')
def home():
    search_query = request.args.get('search')
    functions = read_data()
    # Filter functions by the 'visible' flag
    functions = [f for f in functions if f['visible']]
    if search_query:
        functions = [f for f in functions if search_query.lower() in f['name'].lower()]
    return render_template('home.html', functions=functions)


# Add new function route
@app.route('/add', methods=['GET', 'POST'])
def add_function():
    if request.method == 'POST':
        name = request.form['name']
        definition = request.form['definition']
        example = request.form['example']
        external_link = request.form['external_link']

        functions = read_data()
        new_function = {
            "id": len(functions) + 1,
            "name": name,
            "definition": definition,
            "example": example,
            "external_link": external_link
        }
        functions.append(new_function)
        write_data(functions)

        return redirect(url_for('home'))
    
    return render_template('add_function.html')

# View individual function details
@app.route('/function/<int:id>')
def view_function(id):
    functions = read_data()
    function = next((f for f in functions if f['id'] == id), None)
    if function:
        return render_template('view_function.html', function=function)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)

