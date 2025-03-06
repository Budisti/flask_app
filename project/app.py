from flask import Flask, render_template
import sqlite3
from datetime import datetime, timedelta
import numpy
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

    # total revenue
    total_revenue1 = 0

    for i in range(len(total_revenue)):
        total_revenue1 += total_revenue[i]

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

    total_purchasers1= 0
        
    for i in range(len(total_purchasers)):
        total_purchasers1 += total_purchasers[i]

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

    first_purchasers1 = 0

    for i in range(len(first_purchasers)):
        first_purchasers1 += first_purchasers[i]

    # average purchase revenue per date

    # get columns for the unique users that have purchased
    cur.execute('SELECT user_id, purchase_date FROM purchases WHERE purchase_date BETWEEN (?) AND (?)', (last_7_dates[0], last_7_dates[-1]))

    # fetch data
    rows = cur.fetchall()

    # count unique purchasers for each date

    # turn dictionary into dataframe
    data = pd.DataFrame.from_dict(rows)

    data.drop_duplicates(keep="first", inplace=True, ignore_index=True)

    # unique users that purchased
    unique_user_purchases = data

    # number of users
    total_users = [0,0,0,0,0,0,0]

    # get number of purchasers for everyday
    for i in range(len(total_users)):
        for j in range(len(unique_user_purchases)):
            if (unique_user_purchases[1][j] == last_7_dates[i]):
                total_users[i] = total_users[i] + 1

    # get data for purchases
    cur.execute('SELECT user_id, purchase_date, total_price FROM purchases WHERE purchase_date BETWEEN (?) AND (?)', (last_7_dates[0], last_7_dates[-1]))

    rows = cur.fetchall()

    # turn dictionary into dataframe
    data = pd.DataFrame.from_dict(rows)

    # total amount spent by users per day 
    total_day = [0,0,0,0,0,0,0]

    # get total for everyday
    for i in range(len(total_day)):
        for j in range(len(data)):
            if (data[1][j] == last_7_dates[i]):
                total_day[i] += round(data[2][j], 2)

    # round numbers
    for i in range(len(total_day)):
        total_day[i] = round(total_day[i], 2)

    # get average
    average = [0,0,0,0,0,0,0]

    for i in range(len(average)):
        if (total_users[i] != 0):
            average[i] = total_day[i] / total_users[i]

    # total average

    # total number of users
    total_users_number = 0

    for i in range(len(total_users)):
        total_users_number += total_users[i]

    # total number
    total = 0

    for i in range(len(total_day)):
        total += total_day[i]

    # get average
    average_total = 0

    if (total_users_number != 0):
        average_total = total / total_users_number

    # items that were purchased more
    cur.execute('SELECT p.name AS product_name, pu.product_id, SUM(pu.quantity) AS total_quantity, SUM(pu.total_price) AS total_price FROM purchases pu JOIN products p ON pu.product_id = p.id GROUP BY pu.product_id, p.name ORDER BY total_quantity DESC LIMIT 7')

    rows = cur.fetchall()

    # turn dictionary into dataframe
    data = pd.DataFrame.from_dict(rows)

    items = []

    quantity = []

    for i in range(len(data)):
        items.append(data[0][i])

    for i in range(len(data)):
        quantity.append(int(data[2][i]))

    # close database
    con.commit()

    con.close()

    return render_template('overview.html', last_7_days=last_7_days, total_revenue=total_revenue, total_revenue1=total_revenue1,total_purchasers=total_purchasers, total_purchasers1=total_purchasers1,first_purchasers=first_purchasers, first_purchasers1=first_purchasers1, average=average, average_total=average_total,items=items, quantity=quantity)

@app.route("/ecommercePurchases")
def ecommercePurchases():
    # get last 7 days
    last_7_days = [(datetime.now() - timedelta(days=i)).strftime('%d') for i in range(6, -1, -1)]

    # get last 7 dates
    last_7_dates = [(datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(6, -1, -1)]

    # connect to database
    con = sqlite3.connect("database.db")

    # cursor
    cur = con.cursor()

    # top 10 items by revenue
    cur.execute('SELECT p.name AS product_name, COUNT(DISTINCT pv.id) AS view_count, COUNT(DISTINCT CASE WHEN ca.action = "add" THEN ca.id END) AS add_to_cart_count, COALESCE(pu.purchase_count, 0) AS purchase_count, COALESCE(pu.total_revenue, 0) AS total_revenue FROM products p LEFT JOIN product_views pv ON p.id = pv.product_id LEFT JOIN cart_actions ca ON p.id = ca.product_id LEFT JOIN (SELECT product_id, COUNT(id) AS purchase_count, SUM(total_price) AS total_revenue FROM purchases GROUP BY product_id) pu ON p.id = pu.product_id GROUP BY p.id ORDER BY total_revenue DESC LIMIT 10')

    top_revenue = cur.fetchall()

    print(top_revenue)

    # purchases
    cur.execute('SELECT name, total_price, purchase_date FROM purchases JOIN products ON purchases.product_id = products.id')

    purchases = cur.fetchall()

    # revenue = numpy.zeros((5,7))

    # for every item in rows
    #for i in range(len(rows)):
        # for every date in the last 7 dates
     #   for j in range(len(last_7_dates)):
            # for every purchase made
      #      for k in range(len(purchases)):
                # if the row in purchases matches the name and the date
       #         if (purchases[k][0] == rows[i][0] and purchases[k][2] == last_7_dates[j]):
        #            revenue[i][j] = purchases[k][1]

    # close database
    con.commit()

    con.close()

    return render_template("ecommercePurchases.html", top_revenue=top_revenue, last_7_days=last_7_days)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)