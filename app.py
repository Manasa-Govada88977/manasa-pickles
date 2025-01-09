from flask import Flask, render_template, request, redirect, url_for, session
import json

app = Flask(__name__)
app.secret_key = "your_secret_key"  # To use sessions

# Load pickle data from the JSON file
def load_pickles():
    with open('data/pickles.json') as f:
        return json.load(f)

# Home route that displays the list of available pickles
@app.route('/')
def home():
    pickles = load_pickles()
    return render_template('index.html', pickles=pickles)

# Route to add pickles to the cart
@app.route('/add_to_cart/<int:pickle_id>', methods=['GET', 'POST'])
def add_to_cart(pickle_id):
    pickles = load_pickles()
    pickle = next((p for p in pickles if p['id'] == pickle_id), None)
    
    if pickle:
        cart = session.get('cart', [])
        cart.append(pickle)
        session['cart'] = cart
    return redirect(url_for('cart'))

# Route to view the cart
@app.route('/cart')
def cart():
    cart = session.get('cart', [])
    total_price = sum(pickle['price'] for pickle in cart)
    return render_template('cart.html', cart=cart, total_price=total_price)

# Route to place the order (could be extended with a form)
@app.route('/place_order', methods=['POST'])
def place_order():
    cart = session.get('cart', [])
    if not cart:
        return redirect(url_for('home'))
    
    # You can add order saving logic here (e.g., database or email confirmation)
    session.pop('cart', None)  # Clear the cart after placing the order
    return render_template('order_confirmation.html')

if __name__ == "__main__":
    app.run(debug=True)
