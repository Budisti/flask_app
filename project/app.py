from flask import Flask, render_template
import sqlite3
from datetime import datetime, timedelta
import pandas as pd

app = Flask(__name__)

@app.route("/")
def index():
    # get last 7 days
    last_7_days = [(datetime.now() - timedelta(days=i)).strftime('%d') for i in range(6, -1, -1)]

    # get last 7 dates
    last_7_dates = [(datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(6, -1, -1)]

    # active users this week
    active_users = [0,0,0,0,0,0,0]

    # number of new users this week
    new_users = [0,0,0,0,0,0,0]

    # connect to database
    con = sqlite3.connect("database.db")

    # cursor
    cur = con.cursor()

    # get data of this week
    cur.execute('SELECT user_id, login_date FROM user_activity WHERE login_date BETWEEN (?) AND (?)', (last_7_dates[0], last_7_dates[-1]))

    rows = cur.fetchall()

    # for each date count how many active users there are
    data = pd.DataFrame.from_dict(rows)

    data.drop_duplicates(keep="first", inplace=True, ignore_index=True)

    for i in range(len(active_users)):
        for j in range(len(data)):
            if (data[1][j] == last_7_dates[i]):
                active_users[i] = active_users[i] + 1

    # new users

    # get data for this week
    cur.execute('SELECT id, created_at FROM users WHERE created_at BETWEEN (?) AND (?)', (last_7_dates[0], last_7_dates[-1]))

    rows = cur.fetchall()

    # for each date count how many new users there are
    data = pd.DataFrame.from_dict(rows)

    data.drop_duplicates(keep="first", inplace=True, ignore_index=True)

    for i in range(len(new_users)):
        for j in range(len(data)):
            if (data[1][j] == last_7_dates[i]):
                new_users[i] = new_users[i] + 1

    # close database
    con.commit()

    con.close()

    return render_template("index.html", last_7_days=last_7_days, active_users=active_users, new_users=new_users)

@app.route("/products")
def products():
    # connect to database
    con = sqlite3.connect("database.db")

    # cursor
    cur = con.cursor()

    rows = cur.fetchall()

    print(rows)

    # close database
    con.commit()

    con.close()

    return render_template("products.html")

@app.route("/overview")
def overview():
    # get last 7 days
    last_7_days = [(datetime.now() - timedelta(days=i)).strftime('%d') for i in range(6, -1, -1)]

    # get last 7 dates
    last_7_dates = [(datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(6, -1, -1)]

    # total revenue for each date
    total_revenue = [0,0,0,0,0,0,0]

    # connect to database
    con = sqlite3.connect("database.db")

    # cursor
    cur = con.cursor()

    cur.execute('SELECT total_price, purchase_date FROM purchases WHERE purchase_date BETWEEN (?) AND (?)', (last_7_dates[0], last_7_dates[-1]))

    rows = cur.fetchall()

    data = pd.DataFrame.from_dict(rows)

    for i in range(len(total_revenue)):
        for j in range(len(data)):
            if (data[1][j] == last_7_dates[i]):
                total_revenue[i] += data[0][j]

    # total purchasers for each date
    total_purchasers = [0,0,0,0,0,0,0]

    cur.execute('SELECT user_id, purchase_date FROM purchases WHERE purchase_date BETWEEN (?) AND (?)', (last_7_dates[0], last_7_dates[-1]))

    rows = cur.fetchall()

    data = pd.DataFrame.from_dict(rows)

    data.drop_duplicates(keep="first", inplace=True, ignore_index=True)

    for i in range(len(total_purchasers)):
        for j in range(len(data)):
            if (data[1][j] == last_7_dates[i]):
                total_purchasers[i] = total_purchasers[i] + 1

    # first time purchasers for each date
    first_purchasers = [0,0,0,0,0,0,0]

    # get id of all first time purchasers
    cur.execute('SELECT user_id, purchase_date FROM purchases WHERE user_id NOT IN (SELECT user_id FROM purchases GROUP BY user_id HAVING COUNT(user_id) > 1)')

    rows = cur.fetchall()

    data = pd.DataFrame.from_dict(rows)

    data.drop_duplicates(keep="first", inplace=True, ignore_index=True)

    for i in range(len(first_purchasers)):
        for j in range(len(data)):
            if (data[1][j] == last_7_dates[i]):
                first_purchasers[i] = first_purchasers[i] + 1

    # close database
    con.commit()

    con.close()

    return render_template('overview.html', last_7_days=last_7_days, total_revenue=total_revenue, total_purchasers=total_purchasers, first_purchasers=first_purchasers)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)