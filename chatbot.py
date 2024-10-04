from flask import Flask, request, jsonify, session, render_template
import pandas as pd
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Generate a random secret key for session management

# Load account data
def load_account_data():
    return pd.read_csv('accounts.csv', dtype={'AccountID': str, 'CustomerID': str, 'Username': str, 'Password': str, 'Balance': float, 'AccountType': str})

# Function to get user info based on username and password
def get_user_info(username, password):
    account_data = load_account_data()
    user_account = account_data[account_data['Username'] == username]
    
    if not user_account.empty:
        stored_password = str(user_account['Password'].values[0]).strip()  # Use 'Password'
        
        if stored_password == password:
            return user_account.to_dict(orient='records')[0]  # Convert to dictionary
    return None  # No match found

@app.route('/')
def home():
    return render_template('index.html')  # Render the HTML template

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user_info = get_user_info(username, password)

    if user_info:
        session['username'] = username  # Store username in session
        return jsonify(success=True)  # Respond with success
    else:
        return jsonify(success=False, error='Invalid username or password')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    message = data.get('message')

    # Get username from session
    username = session.get('username')  

    if message.lower() == "what is my balance?":
        account_data = load_account_data()
        user_info = account_data[account_data['Username'] == username]

        if not user_info.empty:
            balance = user_info['Balance'].values[0]
            response = f"Your balance is ${balance:.2f}."  # Format balance to 2 decimal places
        else:
            response = "User not found."
    else:
        response = "I'm sorry, I didn't understand that."

    return jsonify(response=response)

if __name__ == '__main__':
    app.run(debug=True)
