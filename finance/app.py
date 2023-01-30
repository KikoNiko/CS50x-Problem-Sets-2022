import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
import datetime

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Custom filter
app.jinja_env.filters["usd"] = usd
app.jinja_env.globals.update(usd=usd)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    user_id = session["user_id"]
    # Get from transactions the info about purchased stocks for our current user
    transactions_info = db.execute("SELECT symbol, name, SUM(shares) as shares, price FROM transactions WHERE user_id = ? GROUP BY symbol", user_id)
    # Get cash info from users
    cash_info = db.execute("SELECT cash FROM users WHERE id = ?", user_id)

    # Go to index.html, display current info about stocks owned and available funds
    return render_template("index.html", stocks_owned=transactions_info, cash_info=cash_info[0]["cash"])


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "GET":
        return render_template("buy.html")
    else:
        # Here similar to quote we need to request for stock symbol but also ask for number of shares to buy
        symbol = request.form.get("symbol")
        shares = int(request.form.get("shares"))

        # Run some checks
        if not symbol:
            return apology("Please Enter Stock Symbol")

        stock = lookup(symbol)

        if stock == None:
            return apology("Not A Valid Stock Symbol")

        if shares < 0:
            return apology("Enter A Positive Number")

        # Check if user has enough money to make the purchase
        purchase_value = shares * stock["price"]
        user_id = session["user_id"]
        user_cash = db.execute("SELECT cash FROM users WHERE id = ?", user_id)
        user_cash_value = user_cash[0]["cash"]
        if user_cash_value < purchase_value:
            return apology("Not Enough Money :(")

        # After transaction update users table subtracting from cash the value of the purchase
        updated_cash = user_cash_value - purchase_value
        db.execute("UPDATE users SET cash = ? WHERE id = ?", updated_cash, user_id)
        # Save current time of purchase
        date = datetime.datetime.now()
        # Update transactions table
        db.execute("INSERT INTO transactions (user_id, symbol, name, shares, price, date) VALUES (?, ?, ?, ?, ?, ?)", user_id, stock["symbol"], stock["name"], shares, stock["price"], date)
        # Display a flash message and after purchase is successful return to main route
        flash("Purchase Successful!")
        return redirect("/")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    # Here there is only GET method
    # Get user id from sessions
    user_id = session["user_id"]
    # Get information from transaction table and display it in history.html template
    transactions_info = db.execute("SELECT * FROM transactions WHERE user_id = ?", user_id)
    return render_template("history.html", transactions = transactions_info)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "GET":
        return render_template("quote.html")
    else:
        # via POST take the stock symbol. I ensured it is sent as all uppercase string.
        symbol = request.form.get("symbol").upper()
        if not symbol:
            return apology("Please Enter Stock Symbol")

    # Contacting API get the info about that stock from IEX via lookup (function defined in helpers.py)
    # and return data in new template "quoted.html" returning stock's name, price and symbol
    stock = lookup(symbol)
    if stock == None:
        return apology("Not A Valid Stock Symbol")
    else:
        return render_template("quoted.html", name=stock["name"], price=stock["price"], symbol=stock["symbol"])


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "GET":
        return render_template("register.html")
    else:
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

    # Check if all the fields are filled and if password matches confirmation
        if not username:
            return apology("Please Enter Username")
        if not password:
            return apology("Please Enter Password")
        if not confirmation:
            return apology("Please Confirm Password")
        if password != confirmation:
            return apology("Passwords Do Not Match!")

    # Use hash function to "hash" the password making it more secure (not visible) and this way store it later into our database table
        hash_pass = generate_password_hash(password)

    # Use SQL query to save user data into our database
        try:
            new_user = db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, hash_pass)
        except:
            return apology("Username already exists!")

        # Remember user when they register. (This is a small addition to the code)
        # storing the user's data in session
        session["user_id"] = new_user
        return redirect("/")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "GET":
        user_id = session["user_id"]
        symbols_info = db.execute("SELECT symbol FROM transactions WHERE user_id = ? GROUP BY symbol HAVING SUM(shares) > 0", user_id)
        return render_template("sell.html", symbols=[row["symbol"] for row in symbols_info])

    else:
        # Here code is similar to buy function
        symbol = request.form.get("symbol")
        shares = int(request.form.get("shares"))

        # Run some checks
        if not symbol:
            return apology("Please Enter Stock Symbol")

        stock = lookup(symbol)

        if stock == None:
            return apology("Not A Valid Stock Symbol")

        if shares < 0:
            return apology("Enter A Positive Number")

        sell_value = shares * stock["price"]
        user_id = session["user_id"]
        user_cash = db.execute("SELECT cash FROM users WHERE id = ?", user_id)
        user_cash_value = user_cash[0]["cash"]

        user_shares = db.execute("SELECT shares FROM transactions WHERE user_id = ? AND symbol = ? GROUP BY symbol", user_id, symbol)
        user_shares_owned = user_shares[0]["shares"]
        if shares > user_shares_owned:
            return apology("Not Enough Shares")

        # Difference here is we add the price of the stock we sell back to our funds
        updated_cash = user_cash_value + sell_value
        db.execute("UPDATE users SET cash = ? WHERE id = ?", updated_cash, user_id)
        # Save current time of transaction
        date = datetime.datetime.now()
        # Update transactions table
        db.execute("INSERT INTO transactions (user_id, symbol, name, shares, price, date) VALUES (?, ?, ?, ?, ?, ?)", user_id, stock["symbol"], stock["name"], (-1)*shares, stock["price"], date)

        flash("Transaction Successful!")
        return redirect("/")

