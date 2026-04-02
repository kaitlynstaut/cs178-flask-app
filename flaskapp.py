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

# Connect to DynamoDB
dynamodb = boto3.resource('dynamodb', region_name='us-east-2')
table = dynamodb.Table('Wishlist')

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/customer')
def customer():
    return render_template('customer.html')

##################
#MySQL Inventory##
##################

# Item query by category
@app.route("/browse/<category>")
def browse(category):
    """
    Returns all clothing items matching the given category.
    Can be called from the URL directly (/browse/tops)
    or from the POST form handler below.
    """
    rows = execute_query("""
        SELECT c.name, c.category, a.color, c.base_price, ca.sku
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
    categories  = ["tops", "bottoms", "outerwear", "other"]
    return render_template('textbox.html', fieldname="Category", categories = categories)

@app.route('/browsetextbox', methods=['POST'])
def browse_form_post():
    """
    POST handler: reads the category the user typed into the form,
    then calls browse() to run the query and return the table.
    """
    text = request.form['text']

    if text == 'all':
        rows = execute_query("""
            SELECT c.name, c.category, a.color, c.base_price, ca.sku
                FROM clothing_attributes ca
                JOIN clothing c ON ca.clothing_id = c.clothing_id
                JOIN attributes a ON ca.attribute_id = a.attribute_id
        """)
        return render_template('itemquery.html', items=rows, category="All")
    
    return browse(text)

# Add item (used AI to help me insert info entered here to ALL tables in the database)
@app.route('/add-item', methods=['GET', 'POST'])
def add_item():
    if request.method == 'POST':
        name = request.form['name']
        category = request.form['category']
        price = float(request.form['price'])
        color = request.form['color']
        sku = request.form['sku']
        stock_qty = request.form['stock_qty']

        # 1. Insert base item, get its new ID via lastrowid
        clothing_id = execute_insert(
            "INSERT INTO clothing (name, category, base_price) VALUES (%s, %s, %s)",
            (name, category, price)
        )

        # 2. Insert color if it doesn't exist, then fetch its ID
        execute_insert("INSERT IGNORE INTO attributes (color) VALUES (%s)", (color,))
        result = execute_query("SELECT attribute_id FROM attributes WHERE color = %s", (color,))
        attribute_id = result[0]['attribute_id']

        # 3. Insert the variant linking everything together
        execute_insert(
            "INSERT INTO clothing_attributes (sku, clothing_id, attribute_id, stock_qty) VALUES (%s, %s, %s, %s)",
            (sku, clothing_id, attribute_id, stock_qty)
        )

        flash('Item added successfully!', 'success')
        return redirect(url_for('admin'))
    else:
        categories = ["tops", "bottoms", "outerwear", "other"]
        return render_template('add_item.html', categories=categories)
    
# Delete item
@app.route('/delete-item',methods=['GET', 'POST'])
def delete_item():
    if request.method == 'POST':
        # Extract form data
        sku = request.form['sku']
        
        # Process the data (e.g., add it to a database)
        execute_insert(
            "DELETE FROM clothing_attributes WHERE sku = %s",
            (sku,)
        )
        
        flash('Item deleted successfully!', 'warning') 
        # Redirect to admin page upon successful submission
        return redirect(url_for('admin'))
    else:
        # Render the form page if the request method is GET
        return render_template('delete_item.html')
    
# Update price
@app.route('/update-price', methods=['GET', 'POST'])
def update_price():
    if request.method == 'POST':
        # Extract form data
        sku = request.form['sku']
        price = request.form['price']

        # Update MySQL
        execute_insert(
            """UPDATE clothing c
            JOIN clothing_attributes ca ON c.clothing_id = ca.clothing_id
            SET c.base_price = %s
            WHERE ca.sku = %s""",
            (float(price), sku)
        )

        flash('Price updated successfully!', 'info')
        return redirect(url_for('admin'))
    else:
        return render_template('update_price.html')
    

###################
#DynamoDB Wishlist#
###################

# View wishlist
@app.route('/view-wishlist')
def view_wishlist():
    # Read all items from DynamoDB
    response = table.scan()
    items = response['Items']
    return render_template('view_wishlist.html', items=items)

# Add to wishlist
@app.route('/add-to-wishlist', methods=['GET', 'POST'])
def add_to_wishlist():
    if request.method == 'POST':
        # Extract form data
        name = request.form['name']
        sku = request.form['sku']
        color = request.form['color']
        price = request.form['price']

        # Insert into DynamoDB
        table.put_item(Item={
            'wishlist_id': str(uuid.uuid4()),
            'name': name,
            'sku': sku,
            'color': color,
            'price': price
        })

        flash('Item added to wishlist!', 'success')
        return redirect(url_for('customer'))
    else:
        return render_template('add_to_wishlist.html')

# Update wishlist (Used AI to remember how to use the update_item function)
@app.route('/update-wishlist', methods=['GET', 'POST'])
def update_wishlist():
    if request.method == 'POST':
        # Extract form data
        wishlist_id = request.form['wishlist_id']
        name = request.form['name']
        sku = request.form['sku']
        color = request.form['color']
        price = request.form['price']

        # Update item in DynamoDB
        table.update_item(
            Key={'wishlist_id': wishlist_id},
            UpdateExpression='SET #n = :name, sku = :sku, color = :color, price = :price',
            ExpressionAttributeNames={'#n': 'name'},
            ExpressionAttributeValues={
                ':name': name,
                ':sku': sku,
                ':color': color,
                ':price': price
            }
        )

        flash('Wishlist item updated!', 'info')
        return redirect(url_for('view_wishlist'))
    else:
        return render_template('update_wishlist.html')

# Clear wishlist
@app.route('/clear-wishlist', methods=['GET', 'POST'])
def clear_wishlist():
    if request.method == 'POST':
        # Scan and delete all items from DynamoDB
        response = table.scan()
        items = response['Items']

        for item in items:
            table.delete_item(
                Key={'wishlist_id': item['wishlist_id']}
            )

        flash('Wishlist cleared!', 'warning')
        return redirect(url_for('customer'))
    else:
        return render_template('clear_wishlist.html')

# these two lines of code should always be the last in the file
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
