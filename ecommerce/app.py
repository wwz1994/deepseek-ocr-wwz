from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import db, User, Product, Order, OrderItem, CartItem
from werkzeug.utils import secure_filename
import os
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-change-in-production'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Home page
@app.route('/')
def index():
    category = request.args.get('category')
    search = request.args.get('search')
    
    query = Product.query
    
    if category:
        query = query.filter_by(category=category)
    
    if search:
        query = query.filter(Product.name.contains(search) | Product.description.contains(search))
    
    products = query.all()
    categories = db.session.query(Product.category).distinct().all()
    categories = [c[0] for c in categories]
    
    return render_template('index.html', products=products, categories=categories, 
                         selected_category=category, search=search)

# Product detail
@app.route('/product/<int:product_id>')
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template('product_detail.html', product=product)

# Authentication routes
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists', 'error')
            return redirect(url_for('register'))
        
        if User.query.filter_by(email=email).first():
            flash('Email already registered', 'error')
            return redirect(url_for('register'))
        
        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            next_page = request.args.get('next')
            flash('Login successful!', 'success')
            return redirect(next_page if next_page else url_for('index'))
        else:
            flash('Invalid username or password', 'error')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('index'))

# Cart routes
@app.route('/cart')
@login_required
def cart():
    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
    total = sum(item.product.price * item.quantity for item in cart_items)
    return render_template('cart.html', cart_items=cart_items, total=total)

@app.route('/cart/add/<int:product_id>', methods=['POST'])
@login_required
def add_to_cart(product_id):
    product = Product.query.get_or_404(product_id)
    quantity = int(request.form.get('quantity', 1))
    
    if product.stock < quantity:
        flash('Not enough stock available', 'error')
        return redirect(url_for('product_detail', product_id=product_id))
    
    cart_item = CartItem.query.filter_by(user_id=current_user.id, product_id=product_id).first()
    
    if cart_item:
        cart_item.quantity += quantity
    else:
        cart_item = CartItem(user_id=current_user.id, product_id=product_id, quantity=quantity)
        db.session.add(cart_item)
    
    db.session.commit()
    flash('Product added to cart!', 'success')
    return redirect(url_for('cart'))

@app.route('/cart/update/<int:item_id>', methods=['POST'])
@login_required
def update_cart(item_id):
    cart_item = CartItem.query.get_or_404(item_id)
    
    if cart_item.user_id != current_user.id:
        flash('Unauthorized', 'error')
        return redirect(url_for('cart'))
    
    quantity = int(request.form.get('quantity', 1))
    
    if quantity <= 0:
        db.session.delete(cart_item)
    else:
        if cart_item.product.stock < quantity:
            flash('Not enough stock available', 'error')
            return redirect(url_for('cart'))
        cart_item.quantity = quantity
    
    db.session.commit()
    return redirect(url_for('cart'))

@app.route('/cart/remove/<int:item_id>')
@login_required
def remove_from_cart(item_id):
    cart_item = CartItem.query.get_or_404(item_id)
    
    if cart_item.user_id != current_user.id:
        flash('Unauthorized', 'error')
        return redirect(url_for('cart'))
    
    db.session.delete(cart_item)
    db.session.commit()
    flash('Item removed from cart', 'success')
    return redirect(url_for('cart'))

# Checkout
@app.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
    
    if not cart_items:
        flash('Your cart is empty', 'error')
        return redirect(url_for('cart'))
    
    if request.method == 'POST':
        shipping_address = request.form.get('shipping_address')
        
        if not shipping_address:
            flash('Please provide shipping address', 'error')
            return redirect(url_for('checkout'))
        
        total = sum(item.product.price * item.quantity for item in cart_items)
        
        order = Order(user_id=current_user.id, total=total, shipping_address=shipping_address)
        db.session.add(order)
        db.session.flush()
        
        for cart_item in cart_items:
            order_item = OrderItem(
                order_id=order.id,
                product_id=cart_item.product_id,
                quantity=cart_item.quantity,
                price=cart_item.product.price
            )
            db.session.add(order_item)
            
            # Update stock
            cart_item.product.stock -= cart_item.quantity
            
            # Remove from cart
            db.session.delete(cart_item)
        
        db.session.commit()
        flash('Order placed successfully!', 'success')
        return redirect(url_for('orders'))
    
    total = sum(item.product.price * item.quantity for item in cart_items)
    return render_template('checkout.html', cart_items=cart_items, total=total)

# Orders
@app.route('/orders')
@login_required
def orders():
    user_orders = Order.query.filter_by(user_id=current_user.id).order_by(Order.created_at.desc()).all()
    return render_template('orders.html', orders=user_orders)

# Admin routes
@app.route('/admin')
@login_required
def admin_dashboard():
    if not current_user.is_admin:
        flash('Unauthorized access', 'error')
        return redirect(url_for('index'))
    
    total_products = Product.query.count()
    total_orders = Order.query.count()
    total_users = User.query.count()
    recent_orders = Order.query.order_by(Order.created_at.desc()).limit(5).all()
    
    return render_template('admin/dashboard.html', 
                         total_products=total_products,
                         total_orders=total_orders,
                         total_users=total_users,
                         recent_orders=recent_orders)

@app.route('/admin/products')
@login_required
def admin_products():
    if not current_user.is_admin:
        flash('Unauthorized access', 'error')
        return redirect(url_for('index'))
    
    products = Product.query.all()
    return render_template('admin/products.html', products=products)

@app.route('/admin/products/add', methods=['POST'])
@login_required
def admin_add_product():
    if not current_user.is_admin:
        return jsonify({'error': 'Unauthorized'}), 403
    
    name = request.form.get('name')
    description = request.form.get('description')
    price = float(request.form.get('price'))
    category = request.form.get('category')
    stock = int(request.form.get('stock'))
    image = request.form.get('image', 'https://via.placeholder.com/400x300')
    
    product = Product(name=name, description=description, price=price, 
                     category=category, stock=stock, image=image)
    db.session.add(product)
    db.session.commit()
    
    flash('Product added successfully!', 'success')
    return redirect(url_for('admin_products'))

@app.route('/admin/products/edit/<int:product_id>', methods=['POST'])
@login_required
def admin_edit_product(product_id):
    if not current_user.is_admin:
        return jsonify({'error': 'Unauthorized'}), 403
    
    product = Product.query.get_or_404(product_id)
    
    product.name = request.form.get('name')
    product.description = request.form.get('description')
    product.price = float(request.form.get('price'))
    product.category = request.form.get('category')
    product.stock = int(request.form.get('stock'))
    
    if request.form.get('image'):
        product.image = request.form.get('image')
    
    db.session.commit()
    
    flash('Product updated successfully!', 'success')
    return redirect(url_for('admin_products'))

@app.route('/admin/products/delete/<int:product_id>')
@login_required
def admin_delete_product(product_id):
    if not current_user.is_admin:
        flash('Unauthorized access', 'error')
        return redirect(url_for('index'))
    
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    
    flash('Product deleted successfully!', 'success')
    return redirect(url_for('admin_products'))

@app.route('/admin/orders')
@login_required
def admin_orders():
    if not current_user.is_admin:
        flash('Unauthorized access', 'error')
        return redirect(url_for('index'))
    
    all_orders = Order.query.order_by(Order.created_at.desc()).all()
    return render_template('admin/orders.html', orders=all_orders)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000)
