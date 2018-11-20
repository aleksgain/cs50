import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached


@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.route("/")
@login_required
def index():
    user_money = db.execute("SELECT cash FROM users WHERE id = :id", id=session["user_id"])[0]["cash"]
    total = user_money
    user_shares = db.execute("SELECT * FROM portfolio WHERE username = :username", username=session["user_id"])
    stocks = []
    for stock in user_shares:
        ticker = lookup(stock["ticker"])
        stock["price"] = usd(ticker["price"])
        stock["name"] = ticker["name"]
        stock["symbol"] = ticker["symbol"]
        stock["value"] = usd(ticker["price"] * stock["amount"])
        total = total + (ticker["price"] * stock["amount"])
        del stock["username"]
        stocks.append(stock)
    return render_template("index.html", stocks=stocks, money=usd(user_money), total=usd(total))


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():

    if request.method == "POST":

        if not request.form.get("symbol"):
            return apology("provide symbol", 400)

        if not request.form.get("shares"):
            return apology("please provide a correct number of shares desired", 400)
        try:
            val = int(request.form.get("shares"))
        except ValueError:
            return apology("please provide a correct number of shares desired", 400)
        if int(request.form.get("shares")) < 1:
            return apology("please provide a correct number of shares desired", 400)

        shares = int(request.form.get("shares"))

        ticker = lookup(request.form.get("symbol"))

        if not ticker:
            return apology("Incorrect symbol", 400)

        user_money = db.execute("SELECT cash FROM users WHERE id = :id", id=session["user_id"])

        if ticker["price"] * shares > user_money[0]["cash"]:
            return apology("not enough funds to complete transaction", 400)

       # the buying part goes here
        else:
            user_money = user_money[0]["cash"] - ticker["price"] * shares
            portfolio = db.execute("SELECT * FROM portfolio WHERE username = :username AND ticker= :ticker",
                                   username=session["user_id"], ticker=ticker["symbol"])
            if portfolio:
                amount = portfolio[0]["amount"] + shares
                db.execute("UPDATE portfolio SET amount = :amount WHERE username= :username AND ticker= :ticker",
                           username=session["user_id"], ticker=ticker["symbol"], amount=portfolio[0]["amount"] + shares)
            else:
                db.execute("INSERT INTO portfolio (username, ticker, amount) VALUES(:username, :ticker, :amount)",
                           username=session["user_id"], ticker=ticker["symbol"], amount=shares)
            db.execute("UPDATE users SET cash = :cash WHERE id= :id", cash=user_money, id=session["user_id"])
            db.execute("INSERT INTO history (username, type, price, ticker, amount) VALUES(:username, :type, :price, :ticker, :amount)",
                       username=session["user_id"], type="BUY", price=ticker["price"], ticker=ticker["symbol"], amount=shares)
            return redirect("/")
    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    user_history = db.execute("SELECT * FROM history WHERE username = :username", username=session["user_id"])
    if user_history:
        return render_template("history.html", stocks=user_history)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 400)

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

    if request.method == "POST":

        if not request.form.get("symbol"):
            return apology("provide symbol", 400)

        ticker = lookup(request.form.get("symbol"))

        if not ticker:
            return apology("Incorrect symbol", 400)
        else:
            return render_template("quoted.html", name=ticker["name"], price=usd(ticker["price"]), symbol=ticker["symbol"])

    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Ensure password matches the confirmation field
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("password mismatch", 400)

        # Query database for username
        result = db.execute("INSERT INTO users (username, hash) VALUES(:username, :hash)", username=request.form.get(
                            "username"), hash=generate_password_hash(request.form.get("password")))

        if not result:
            return apology("username already exists", 400)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


@app.route("/change_pwd", methods=["GET", "POST"])
def change_pwd():
    """Register user"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        if not request.form.get("password"):
            return apology("must provide password", 400)

        elif request.form.get("password") != request.form.get("confirm_password"):
            return apology("password mismatch", 400)

        db.execute("UPDATE users SET hash = :hash WHERE id= :id", hash=generate_password_hash(
            request.form.get("password")), id=session["user_id"])

        return render_template("changed.html")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("change_pwd.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    if request.method == "POST":

        if not request.form.get("symbol"):
            return apology("provide symbol", 400)

        if not request.form.get("shares"):
            return apology("please provide a correct number of shares desired", 400)
        elif int(request.form.get("shares")) < 1:
            return apology("please provide a correct number of shares desired", 400)

        shares = int(request.form.get("shares"))

        ticker = lookup(request.form.get("symbol"))

        if not ticker:
            return apology("Incorrect symbol", 400)

        user_shares = db.execute("SELECT amount FROM portfolio WHERE username = :username AND ticker= :ticker",
                                 username=session["user_id"], ticker=ticker["symbol"])

        if not user_shares:
            return apology("Incorrect symbol", 400)

        if shares > user_shares[0]["amount"]:
            return apology("not enough shares owned", 400)

        else:
            # the selling part goes here
            user_money = db.execute("SELECT cash FROM users WHERE id = :id", id=session["user_id"])[
                0]["cash"] + ticker["price"] * shares
            portfolio = db.execute("SELECT * FROM portfolio WHERE username = :username AND ticker= :ticker",
                                   username=session["user_id"], ticker=ticker["symbol"])
            amount = portfolio[0]["amount"] - shares
            if amount > 0:
                db.execute("UPDATE portfolio SET amount = :amount WHERE username= :username AND ticker= :ticker",
                           username=session["user_id"], ticker=ticker["symbol"], amount=amount)
            else:
                db.execute("DELETE FROM portfolio WHERE username= :username AND ticker= :ticker",
                           username=session["user_id"], ticker=ticker["symbol"])
            db.execute("UPDATE users SET cash = :cash WHERE id= :id", cash=user_money, id=session["user_id"])
            db.execute("INSERT INTO history (username, type, price, ticker, amount) VALUES(:username, :type, :price, :ticker, :amount)",
                       username=session["user_id"], type="SELL", price=ticker["price"], ticker=ticker["symbol"], amount=shares)
        return redirect("/")
    else:
        stocks = db.execute("SELECT * FROM portfolio WHERE username = :username", username=session["user_id"])
        return render_template("sell.html", stocks=stocks)


def errorhandler(e):
    """Handle error"""
    return apology(e.name, e.code)


# listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
