# author: T. Urness and M. Moore
# description: Flask example using redirect, url_for, and flash
# credit: the template html files were constructed with the help of ChatGPT

from flask import Flask
from flask import render_template
from flask import Flask, render_template, request, redirect, url_for, flash
from dbCode import *

app = Flask(__name__)
app.secret_key = 'your_secret_key' # this is an artifact for using flash displays; 
                                   # it is required, but you can leave this alone

@app.route('/')
def home():
    return render_template('home.html')

##################
#MySQL Inventory##
##################

@app.route('/viewdb')
def view_all():
    """
    Fetches all items from the clothing_store database
    and returns them as an HTML table.
    Route: /viewdb
    """
    rows = execute_query("""
        SELECT
            c.name,
            c.category,
            a.color,
            a.material,
            ca.stock_qty,
            c.base_price
        FROM clothing_attributes ca
        JOIN clothing c ON ca.clothing_id  = c.clothing_id
        JOIN attributes a ON ca.attribute_id = a.attribute_id
        ORDER BY c.clothing_id, a.color
    """)
    return render_template('viewdb.html', items=rows)

# Item query by category
@app.route("/browse/<category>")
def browse(category):
    """
    Returns all clothing items matching the given category.
    Can be called from the URL directly (/browse/tops)
    or from the POST form handler below.
    """
    rows = execute_query("""
        SELECT c.name, c.category, a.color, c.base_price
            FROM clothing_attributes ca
            JOIN clothing c ON ca.clothing_id = c.clothing_id
            JOIN attributes a ON ca.attribute_id = a.attribute_id
            WHERE c.category = %s """, 
            (category,)
        )

    return render_template('itemquery.html', items=rows, category=category)

@app.route('/browsetextbox', methods=['GET'])
def browse_form():
    """
    GET handler: renders the empty search form.
    The 'fieldname' variable fills in the label text in textbox.html.
    """
    return render_template('textbox.html', fieldname="Category")

@app.route('/browsetextbox', methods=['POST'])
def browse_form_post():
    """
    POST handler: reads the category the user typed into the form,
    then calls browse() to run the query and return the table.
    """
    text = request.form['text']
    return browse(text)


###################
#DynamoDB Wishlist#
###################
@app.route('/add-item', methods=['GET', 'POST'])
def add_item():
    if request.method == 'POST':
        # Extract form data
        name = request.form['name']
        category = request.form['category']
        price = request.form['price']

        # Process the data (e.g., add it to a database)
        execute_query(
            "INSERT INTO clothing (name, category, base_price) VALUES (%s, %s, %s)",
            (name, category, price)
        )
        
        flash('Item added successfully!', 'success')  # 'success' is a category; makes a green banner at the top
        # Redirect to home page or another page upon successful submission
        return redirect(url_for('home'))
    else:
        # Render the form page if the request method is GET
        return render_template('add_item.html')

@app.route('/delete-item',methods=['GET', 'POST'])
def delete_item():
    if request.method == 'POST':
        # Extract form data
        name = request.form['name']
        
        # Process the data (e.g., add it to a database)
        execute_query(
            "DELETE FROM clothing WHERE name = %s",
            (name,)
        )
        
        flash('Item deleted successfully! Hoorah!', 'warning') 
        # Redirect to home page or another page upon successful submission
        return redirect(url_for('home'))
    else:
        # Render the form page if the request method is GET
        return render_template('delete_item.html')


@app.route('/display-users')
def display_users():
    # hard code a value to the users_list;
    # note that this could have been a result from an SQL query :) 
    users_list = (('John','Doe','Comedy'),('Jane', 'Doe','Drama'))
    return render_template('display_users.html', users = users_list)


# these two lines of code should always be the last in the file
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
