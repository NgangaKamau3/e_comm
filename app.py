from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
import pymysql
from werkzeug.utils import secure_filename
import os
from dotenv import load_dotenv
# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

# Configuration
UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', 'static/images')
MAX_CONTENT_LENGTH = int(os.getenv('MAX_CONTENT_LENGTH', 16 * 1024 * 1024))
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def get_db_connection():
    try:
        connection = pymysql.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME'),
            port=int(os.getenv('DB_PORT', 3306)),
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        return connection
    except pymysql.Error as e:
        print(f"Error connecting to database: {e}")
        return None

from flask import *
import pymysql
from werkzeug.utils import secure_filename
import os
from flask import session

app = Flask(__name__)
app.config['SESSION_TYPE'] = 'filesystem'
app.secret_key = 'your-secret-key-here'  # Change this to a secure key

@app.before_request
def initialize_session():
    if 'cart' not in session:
        session['cart'] = []

# Configuration
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'images')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def get_db_connection():
    try:
        connection = pymysql.connect(
            host='localhost',
            user='root',
            password='',  # default XAMPP MySQL password is blank
            database='grabit',
            port=3306,
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        return connection
    except pymysql.Error as e:
        print(f"Error connecting to database: {e}")
        return None

def handle_db_error(error):
    flash(f"Database error: {str(error)}", "error")
    # Return error page instead of redirecting
    return render_template("error.html", error=error), 500

# homepage  route 
@app.route("/")
def homepage():
    try:
        connection = get_db_connection()
        if not connection:
            return handle_db_error("Could not connect to database")
        
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        categories = ['shoes', 'clothes', 'electronics', 'accessories']
        products_by_category = {}
        
        for category in categories:
            cursor.execute("""
                SELECT * FROM products 
                WHERE product_category = %s 
                ORDER BY created_at DESC 
                LIMIT 4
            """, (category,))
            products_by_category[category] = cursor.fetchall()
        
        return render_template("home.html", products=products_by_category)
    except Exception as e:
        return handle_db_error(e)
    finally:
        if connection:
            connection.close()

@app.route("/product/<int:product_id>")
def product_detail(product_id):
    try:
        connection = get_db_connection()
        if not connection:
            return handle_db_error("Could not connect to database")
        
        cursor = connection.cursor()
        cursor.execute("""
            SELECT p.*, COUNT(r.id) as review_count, AVG(r.rating) as avg_rating 
            FROM products p 
            LEFT JOIN reviews r ON p.id = r.product_id 
            WHERE p.id = %s
            GROUP BY p.id
        """, (product_id,))
        
        product = cursor.fetchone()
        if not product:
            flash("Product not found", "error")
            return redirect(url_for('homepage'))
            
        return render_template("product_detail.html", product=product)
    except Exception as e:
        return handle_db_error(e)
    finally:
        if connection:
            connection.close()

# upload route
@app.route("/upload", methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        if not all(field in request.form for field in ['product_name', 'product_desc', 'product_cost', 'product_category']):
            flash("All fields are required", "error")
            return render_template("upload.html")
        
        product_image = request.files.get('product_image')
        if not product_image:
            flash("Image is required", "error")
            return render_template("upload.html")
            
        filename = secure_filename(product_image.filename)
        product_image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
        try:
            connection = get_db_connection()
            if not connection:
                return handle_db_error("Could not connect to database")
            
            cursor = connection.cursor()
            sql = """INSERT INTO products 
                    (product_name, product_desc, product_cost, product_category, product_image_name) 
                    VALUES (%s, %s, %s, %s, %s)"""
            
            data = (
                request.form['product_name'],
                request.form['product_desc'],
                request.form['product_cost'],
                request.form['product_category'],
                filename
            )
            
            cursor.execute(sql, data)
            connection.commit()
            flash("Product added successfully!", "success")
            return redirect(url_for('homepage'))
            
        except Exception as e:
            return handle_db_error(e)
        finally:
            if connection:
                connection.close()
    
    return render_template("upload.html")

@app.route("/cart", methods=['GET', 'POST'])
def view_cart():
    if 'cart' not in session:
        session['cart'] = []
    
    total = sum(item['price'] * item['quantity'] for item in session['cart'])
    return render_template("cart.html", cart=session['cart'], total=total)

@app.route("/checkout", methods=['GET', 'POST'])
def checkout():
    if 'cart' not in session or not session['cart']:
        flash("Your cart is empty", "warning")
        return redirect(url_for('homepage'))
    
    if request.method == 'POST':
        # Simulate order completion
        session['cart'] = []
        flash("Order placed successfully! (Demo only - no actual payment processed)", "success")
        return redirect(url_for('homepage'))
    
    total = sum(item['price'] * item['quantity'] for item in session['cart'])
    return render_template("checkout.html", cart=session['cart'], total=total)

@app.route("/add_to_cart/<int:product_id>", methods=['POST'])
def add_to_cart(product_id):
    try:
        quantity = int(request.form.get('quantity', 1))
        connection = get_db_connection()
        if not connection:
            return jsonify({'error': 'Database connection failed'}), 500
            
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM products WHERE id = %s", (product_id,))
        product = cursor.fetchone()
        
        if not product:
            return jsonify({'error': 'Product not found'}), 404
            
        if 'cart' not in session:
            session['cart'] = []
            
        cart_item = {
            'id': product['id'],
            'name': product['product_name'],
            'price': float(product['product_cost']),
            'quantity': quantity,
            'image': product['product_image_name']
        }
        
        session['cart'].append(cart_item)
        session.modified = True
        
        return jsonify({
            'success': True,
            'message': 'Product added to cart',
            'cart_count': len(session['cart'])
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if connection:
            connection.close()

@app.route("/category/<category>")
def category_view(category):
    try:
        connection = get_db_connection()
        if not connection:
            return handle_db_error("Could not connect to database")
        
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        
        # Get all subcategories for this category
        cursor.execute("""
            SELECT DISTINCT sub_category 
            FROM products 
            WHERE product_category = %s
        """, (category,))
        sub_categories = [row['sub_category'] for row in cursor.fetchall()]
        
        # Get all brands for this category
        cursor.execute("""
            SELECT DISTINCT brand 
            FROM products 
            WHERE product_category = %s
        """, (category,))
        brands = [row['brand'] for row in cursor.fetchall()]
        
        # Get products with filters
        sub_category = request.args.get('sub_category')
        brand = request.args.get('brand')
        sort = request.args.get('sort', 'newest')
        
        query = """
            SELECT * FROM products 
            WHERE product_category = %s 
        """
        params = [category]
        
        if sub_category:
            query += " AND sub_category = %s"
            params.append(sub_category)
        if brand:
            query += " AND brand = %s"
            params.append(brand)
            
        if sort == 'price_low':
            query += " ORDER BY product_cost ASC"
        elif sort == 'price_high':
            query += " ORDER BY product_cost DESC"
        else:  # newest
            query += " ORDER BY created_at DESC"
            
        cursor.execute(query, tuple(params))
        products = cursor.fetchall()
        
        return render_template(
            "category.html",
            category=category,
            products=products,
            sub_categories=sub_categories,
            brands=brands,
            selected_sub_category=sub_category,
            selected_brand=brand,
            selected_sort=sort
        )
        
    except Exception as e:
        return handle_db_error(e)
    finally:
        if connection:
            connection.close()

if __name__ == '__main__':
    app.run(debug=True)