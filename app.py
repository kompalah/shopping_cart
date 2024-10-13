from flask import Flask, render_template, redirect, url_for, request, session, jsonify
import json

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Load product data
with open('data/products.json') as f:
    products = json.load(f)

@app.route('/')
def index():
    return render_template('index.html', products=products)

@app.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    if 'cart' not in session:
        session['cart'] = {}
    
    cart = session['cart']
    if str(product_id) in cart:
        cart[str(product_id)] += 2
    else:
        cart[str(product_id)] = 1
    
    session['cart'] = cart
    return redirect(url_for('cart'))

@app.route('/cart')
def cart():
    cart = session.get('cart', {})
    cart_items = []
    total = 0
    for product_id, quantity in cart.items():
        product = next((p for p in products if p['id'] == int(product_id)), None)
        if product:
            cart_items.append({
                'product': product,
                'quantity': quantity,
                'total_price': product['price'] * quantity
            })
            total += product['price'] * quantity
    
    return render_template('cart.html', cart_items=cart_items, total=total)

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if request.method == 'POST':
        # Process the payment and clear the cart
        session.pop('cart', None)
        return redirect(url_for('index'))
    
    return render_template('checkout.html')

if __name__ == '__main__':
    app.run(debug=True,port=8000)