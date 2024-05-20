from flask import Flask, render_template, request, jsonify, session, redirect, url_for, make_response
import sys, json
from models import Users,Orders,Payments,Addresses, db
from flask_login import LoginManager, current_user, login_user, logout_user
from datetime import datetime
from peewee import IntegrityError

app = Flask(__name__)
app.secret_key = #secret key

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    try:
        return Users.get(Users.user_id == user_id)
    except Users.DoesNotExist:
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']
    user = Users.select().where(Users.email == email).first()
    if user and user.password == password:
        login_user(user)
        return jsonify({'success': True})
    else:
        return jsonify({'success': False, 'message': 'Invalid email or password'})
    
@app.route('/signup', methods=['GET'])
def show_signup_form():
    return render_template('signup.html')


@app.route('/signup', methods=['POST'])
def signup():

    email = request.form.get('email')
    password = request.form.get('password')
    first_name = request.form.get('firstName')
    last_name = request.form.get('lastName')
    username = request.form.get('username')


   
    new_user = Users(
        email=email,
        password=password, 
        first_name=first_name,
        last_name=last_name,
        username=username,
        is_active=True  
    )

    try:
        
        new_user.save()
        return redirect(url_for('login')) 
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/dashboard')
def dashboard():
    return render_template('main.html')

@app.route('/cart')
def cart():
    return render_template('cart.html')

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    item_data = request.get_json()
    if 'cart' not in session:
        session['cart'] = []
    else:
        session.modified = True  

    session['cart'].append({
        'foodItem': item_data.get('foodItem'),
        'foodPrice': item_data.get('foodPrice'),
        'foodImage': item_data.get('foodImage')
    })

    return jsonify({'message': 'Item added to cart successfully'}), 200

@app.route('/get_cart')
def get_cart():
    cart_data = session.get('cart', [])
    print('Sending Cart Data:', cart_data)
    return jsonify(cart_data)

@app.route('/delete_from_cart', methods=['POST'])
def delete_from_cart():
    if 'cart' in session:
        data = request.get_json()
        item_to_delete = data['item']
        session['cart'] = [item for item in session['cart'] if item['foodItem'] != item_to_delete]
        
        
        total_price = sum(float(item['foodPrice']) for item in session['cart'])
        
        return jsonify({'message': 'Item deleted successfully', 'totalPrice': total_price})
    else:
        return jsonify({'error': 'Cart is empty'}), 400



# Route for The Stag Snack Bar
@app.route('/diner')
def diner():
    return render_template('diner.html')

# Route for Food Truck
@app.route('/foodTruck')
def foodTruck():
    return render_template('foodTruck.html')

# Route for The Levee
@app.route('/levee')
def levee():
    return render_template('levee.html')

# Route for Dunkin Donuts
@app.route('/dunkin')
def dunkin():
    return render_template('dunkin.html')

# Route for Starbucks
@app.route('/starbucks')
def starbucks():
    return render_template('starbucks.html')

# Route for Sushi
@app.route('/sushi')
def sushi():
    return render_template('sushi.html')

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    print("before entering info")
    if request.method == 'POST':
        return process_checkout()
    return render_template('checkout.html')


def process_checkout():
    app.logger.debug("Checkout process started")
    if not current_user.is_authenticated:
        return jsonify({'error': 'User not logged in'}), 401

    user_id = current_user.get_id()
    first_name = request.form.get('field-1', '')
    last_name = request.form.get('field-2', '')
    dorm_townhouse = request.form.get('field-3', '')
    room_number = request.form.get('field-4', '')
    stag_ID = request.form.get('field-5', '')
    selected_payment_method = request.form.get('payment', 'Unknown')
    total_price = request.form.get('total_price', default=0.0, type=float)



    try:
        with db.atomic():
            order = Orders.create(
                user_id=user_id,
                stagID = stag_ID,
                quantity=int(request.form.get('quantity', 1)),
                order_date=datetime.now(),
                firstName=first_name,
                lastName=last_name
            )
            Addresses.create(
                user_id=user_id,
                order_id=order.order_id,
                dorm_name=dorm_townhouse,
                room_number=room_number
            )
            Payments.create(

                order_id=order.order_id,
                payment_method=selected_payment_method,
                amount=total_price,
                payment_date=datetime.now()

            )
            session['receipt_data'] = {
                'firstName': first_name,
                'lastName': last_name,
                'totalPrice': total_price,
                'paymentMethod': selected_payment_method,
                'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        session.pop('cart', None)
    except IntegrityError as e:
        return jsonify({'success': False, 'message': 'Database error: ' + str(e)}), 500

    return redirect(url_for('thank_you'))
@app.route('/thank-you')
def thank_you():
    return render_template('thanks.html')

@app.route('/download-receipt')
def download_receipt():
    
    receipt_data = session.get('receipt_data', {})
    if not receipt_data:
        return "Receipt not available", 404
    
    receipt_json = json.dumps(receipt_data, indent=4)
    response = make_response(receipt_json)
    response.headers['Content-Disposition'] = 'attachment; filename=receipt.json'
    response.mimetype = 'application/json'
    return response

@app.route('/clear_session')
def clear_session():
    session.clear()
    return "Session cleared!"

@app.route('/logout')
def logout():
    logout_user()  
    session.clear()  
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
