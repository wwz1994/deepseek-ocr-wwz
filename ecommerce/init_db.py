from app import app, db
from models import User, Product

def init_database():
    with app.app_context():
        # Create all tables
        db.create_all()
        
        # Check if admin user exists
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin = User(username='admin', email='admin@ecommerce.com', is_admin=True)
            admin.set_password('admin123')
            db.session.add(admin)
        
        # Check if products exist
        if Product.query.count() == 0:
            # Sample products
            products = [
                # Electronics
                Product(
                    name='Wireless Headphones',
                    description='High-quality wireless headphones with noise cancellation and 30-hour battery life. Perfect for music lovers and professionals.',
                    price=149.99,
                    category='Electronics',
                    stock=50,
                    image='https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400&h=300&fit=crop'
                ),
                Product(
                    name='Smart Watch',
                    description='Feature-rich smartwatch with fitness tracking, heart rate monitor, and smartphone notifications. Water-resistant design.',
                    price=299.99,
                    category='Electronics',
                    stock=30,
                    image='https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=400&h=300&fit=crop'
                ),
                Product(
                    name='Laptop Stand',
                    description='Ergonomic aluminum laptop stand with adjustable height. Improves posture and cooling for your laptop.',
                    price=49.99,
                    category='Electronics',
                    stock=100,
                    image='https://images.unsplash.com/photo-1527864550417-7fd91fc51a46?w=400&h=300&fit=crop'
                ),
                Product(
                    name='Wireless Mouse',
                    description='Precision wireless mouse with ergonomic design. Long battery life and smooth tracking on any surface.',
                    price=29.99,
                    category='Electronics',
                    stock=75,
                    image='https://images.unsplash.com/photo-1527814050087-3793815479db?w=400&h=300&fit=crop'
                ),
                
                # Fashion
                Product(
                    name='Classic Leather Jacket',
                    description='Premium genuine leather jacket with timeless design. Perfect for any season and occasion.',
                    price=199.99,
                    category='Fashion',
                    stock=25,
                    image='https://images.unsplash.com/photo-1551028719-00167b16eac5?w=400&h=300&fit=crop'
                ),
                Product(
                    name='Designer Sunglasses',
                    description='Stylish polarized sunglasses with UV protection. Comes with protective case and cleaning cloth.',
                    price=89.99,
                    category='Fashion',
                    stock=60,
                    image='https://images.unsplash.com/photo-1572635196237-14b3f281503f?w=400&h=300&fit=crop'
                ),
                Product(
                    name='Canvas Backpack',
                    description='Durable canvas backpack with multiple compartments. Perfect for daily commute or travel.',
                    price=59.99,
                    category='Fashion',
                    stock=40,
                    image='https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=400&h=300&fit=crop'
                ),
                Product(
                    name='Running Shoes',
                    description='Lightweight running shoes with excellent cushioning and breathable mesh upper. Ideal for athletes.',
                    price=119.99,
                    category='Fashion',
                    stock=45,
                    image='https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=400&h=300&fit=crop'
                ),
                
                # Home & Garden
                Product(
                    name='Ceramic Plant Pot Set',
                    description='Set of 3 modern ceramic plant pots with drainage holes. Perfect for indoor plants and succulents.',
                    price=34.99,
                    category='Home & Garden',
                    stock=80,
                    image='https://images.unsplash.com/photo-1485955900006-10f4d324d411?w=400&h=300&fit=crop'
                ),
                Product(
                    name='LED Desk Lamp',
                    description='Adjustable LED desk lamp with touch control and multiple brightness levels. Energy-efficient and eye-friendly.',
                    price=39.99,
                    category='Home & Garden',
                    stock=55,
                    image='https://images.unsplash.com/photo-1507473885765-e6ed057f782c?w=400&h=300&fit=crop'
                ),
                Product(
                    name='Throw Pillow Set',
                    description='Set of 2 decorative throw pillows with soft velvet covers. Adds comfort and style to any room.',
                    price=44.99,
                    category='Home & Garden',
                    stock=70,
                    image='https://images.unsplash.com/photo-1584100936595-c0654b55a2e2?w=400&h=300&fit=crop'
                ),
                Product(
                    name='Wall Clock',
                    description='Modern minimalist wall clock with silent movement. Perfect for living room, bedroom, or office.',
                    price=24.99,
                    category='Home & Garden',
                    stock=90,
                    image='https://images.unsplash.com/photo-1563861826100-9cb868fdbe1c?w=400&h=300&fit=crop'
                ),
                
                # Sports
                Product(
                    name='Yoga Mat',
                    description='Premium non-slip yoga mat with extra cushioning. Includes carrying strap for easy transport.',
                    price=39.99,
                    category='Sports',
                    stock=65,
                    image='https://images.unsplash.com/photo-1601925260368-ae2f83cf8b7f?w=400&h=300&fit=crop'
                ),
                Product(
                    name='Dumbbell Set',
                    description='Adjustable dumbbell set with multiple weight options. Perfect for home workouts and strength training.',
                    price=89.99,
                    category='Sports',
                    stock=35,
                    image='https://images.unsplash.com/photo-1517836357463-d25dfeac3438?w=400&h=300&fit=crop'
                ),
                Product(
                    name='Water Bottle',
                    description='Insulated stainless steel water bottle keeps drinks cold for 24 hours. BPA-free and leak-proof.',
                    price=24.99,
                    category='Sports',
                    stock=100,
                    image='https://images.unsplash.com/photo-1602143407151-7111542de6e8?w=400&h=300&fit=crop'
                ),
                Product(
                    name='Resistance Bands Set',
                    description='Set of 5 resistance bands with different strength levels. Includes door anchor and carrying bag.',
                    price=29.99,
                    category='Sports',
                    stock=85,
                    image='https://images.unsplash.com/photo-1598289431512-b97b0917affc?w=400&h=300&fit=crop'
                ),
            ]
            
            for product in products:
                db.session.add(product)
        
        db.session.commit()
        print("Database initialized successfully!")
        print("Admin credentials: username='admin', password='admin123'")

if __name__ == '__main__':
    init_database()
