from flask import Flask, render_template, request
import sqlite3
from datetime import datetime, timedelta, date
import numpy
import pandas as pd
import json

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

    print(rows)

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

@app.route("/home")
def home():
    # get last 7 days
    last_7_days = [(datetime.now() - timedelta(days=i)).strftime('%d') for i in range(6, -1, -1)]

    # get last 7 dates
    last_7_dates = [(datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(6, -1, -1)]

    # connect to database
    con = sqlite3.connect("database.db")

    # cursor
    cur = con.cursor()

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

    # active users
    active_users = [0,0,0,0,0,0,0]

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

    # total active users
    total_active = 0

    for i in range(len(active_users)):
        total_active += active_users[i]

    # count events
    count_events = [0,0,0,0,0,0,0]

    # count checkout and purchases
    cur.execute('SELECT id, action_date FROM cart_actions')

    count_events_rows = cur.fetchall()

    for i in range(len(count_events)):
        for j in range(len(count_events_rows)):
            if (count_events_rows[j][1] == last_7_dates[i]):
                count_events[i] += 1

    # add purchases to events
    cur.execute('SELECT id, purchase_date FROM purchases')

    count_purchases_rows = cur.fetchall()

    for i in range(len(count_events)):
        for j in range(len(count_purchases_rows)):
            if (count_purchases_rows[j][1] == last_7_dates[i]):
                count_events[i] += 1

    # total event count
    total_count_events = 0

    for i in range(len(count_events)):
        total_count_events += count_events[i]

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

    total_purchasers1 = 0
        
    for i in range(len(total_purchasers)):
        total_purchasers1 += total_purchasers[i]

    # get top 10 most popular countries between users
    cur.execute('SELECT id, COUNT(countries), countries FROM users GROUP BY countries ORDER BY COUNT(countries) DESC LIMIT 10')

    top_countries = cur.fetchall()

    # seperate countries from count
    countries_count = []

    countries = []

    # count and countries
    for i in range(len(top_countries)):
        # count
        countries_count.append(top_countries[i][1])

        # countries
        countries.append(top_countries[i][2])

    # new users
    cur.execute('SELECT COUNT(countries), countries FROM users WHERE created_at BETWEEN (?) AND (?) GROUP BY countries ORDER BY COUNT(countries) DESC LIMIT 5', ("01-01-2024", last_7_dates[-1]))
    
    new_users = cur.fetchall()

    # seperate countries from count
    new_users_count = []

    new_users_countries = []

    # count and countries
    for i in range(len(new_users)):
        # count
        new_users_count.append(new_users[i][0])

        # countries
        new_users_countries.append(new_users[i][1])

    # active users
    cur.execute('SELECT COUNT(countries), countries FROM user_activity JOIN users ON user_activity.user_id = users.id WHERE login_date BETWEEN (?) AND (?) GROUP BY countries ORDER BY COUNT(countries) DESC LIMIT 5', ("01-01-2024", last_7_dates[-1]))

    active_users = cur.fetchall()

    # seperate countries from count
    active_users_count = []

    active_users_countries = []

    # count and countries
    for i in range(len(active_users)):
        # count
        active_users_count.append(active_users[i][0])

        # countries
        active_users_countries.append(active_users[i][1])

    # most viewed products last 7 days
    cur.execute('SELECT COUNT(product_id), name, view_date FROM product_views JOIN products ON product_views.product_id = products.id WHERE view_date BETWEEN (?) AND (?) GROUP BY product_id ORDER BY COUNT(product_id) DESC LIMIT 5', (last_7_dates[0], last_7_dates[-1]))

    most_viewed_products_data_last7 = cur.fetchall()

    # seperate countries from count
    most_viewed_products_count_last7 = []

    most_viewed_products_names_last7 = []

    # count and products
    for i in range(len(most_viewed_products_data_last7)):
        # count
        most_viewed_products_count_last7.append(most_viewed_products_data_last7[i][0])

        # products
        most_viewed_products_names_last7.append(most_viewed_products_data_last7[i][1])

    # most viewed products last 14 days
    
    # get last 14 dates
    last_14_dates = [(datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(13, -1, -1)]

    cur.execute('SELECT COUNT(product_id), name, view_date FROM product_views JOIN products ON product_views.product_id = products.id WHERE view_date BETWEEN (?) AND (?) GROUP BY product_id ORDER BY COUNT(product_id) DESC LIMIT 5', (last_14_dates[0], last_14_dates[-1]))

    most_viewed_products_data_last14 = cur.fetchall()

    # seperate countries from count
    most_viewed_products_count_last14 = []

    most_viewed_products_names_last14 = []

    # count and products
    for i in range(len(most_viewed_products_data_last14)):
        # count
        most_viewed_products_count_last14.append(most_viewed_products_data_last14[i][0])

        # products
        most_viewed_products_names_last14.append(most_viewed_products_data_last14[i][1])

    # most viewed products last 14 days
    
    # get last 28 dates
    last_28_dates = [(datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(27, -1, -1)]

    cur.execute('SELECT COUNT(product_id), name, view_date FROM product_views JOIN products ON product_views.product_id = products.id WHERE view_date BETWEEN (?) AND (?) GROUP BY product_id ORDER BY COUNT(product_id) DESC LIMIT 5', (last_28_dates[0], last_28_dates[-1]))

    most_viewed_products_data_last28 = cur.fetchall()

    # seperate countries from count
    most_viewed_products_count_last28 = []

    most_viewed_products_names_last28 = []

    # count and products
    for i in range(len(most_viewed_products_data_last28)):
        # count
        most_viewed_products_count_last28.append(most_viewed_products_data_last28[i][0])

        # products
        most_viewed_products_names_last28.append(most_viewed_products_data_last28[i][1])

    # close database
    con.commit()

    con.close()

    return render_template('home.html', average=average, last_7_days=last_7_days, average_total=average_total, active_users=active_users, total_active=total_active, count_events=count_events, total_count_events=total_count_events, total_purchasers1=total_purchasers1, total_purchasers=total_purchasers, countries_count=countries_count, countries=countries, new_users_countries=new_users_countries, new_users_count=new_users_count, active_users_count=active_users_count, active_users_countries=active_users_countries, most_viewed_products_count_last7=most_viewed_products_count_last7, most_viewed_products_names_last7=most_viewed_products_names_last7, most_viewed_products_count_last14=most_viewed_products_count_last14, most_viewed_products_names_last14=most_viewed_products_names_last14, most_viewed_products_count_last28=most_viewed_products_count_last28, most_viewed_products_names_last28=most_viewed_products_names_last28)

@app.route("/behavioralInsights")
def behavioralInsights():

    # connect to database
    con = sqlite3.connect("database.db")

    # cursor
    cur = con.cursor()

    # get all from user location join to get name
    cur.execute('SELECT name, latitude, longitude, street_address FROM user_location JOIN users ON user_location.user_id = users.id')

    # store data of user location
    user_location = cur.fetchall()

    # --- users for audience ---
    cur.execute('SELECT COUNT(id) FROM users')

    users_audience = cur.fetchall()

    users_audience = users_audience[0][0]

    # --- non-purchasers for audience ---

    # all user ids
    cur.execute('SELECT id FROM users')

    rows = cur.fetchall()

    user_ids = []

    for row in rows:
        user_ids.append(row[0])

    # purchasers id
    cur.execute('SELECT user_id FROM purchases GROUP BY user_id')

    rows = cur.fetchall()

    purchasers = []

    for row in rows:
        purchasers.append(row[0])

    # if user id not in purchasers add count to non_purchasers
    non_purchasers_audience = 0

    for element in user_ids:
        if (element not in purchasers):
            non_purchasers_audience += 1

    # --- recently active users for audience (users who have logged in the last 30 days) ---
    
    # get last 7 dates
    last_7_dates = [(datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(6, -1, -1)]

    cur.execute('SELECT COUNT(DISTINCT(user_id)) FROM user_activity WHERE login_date BETWEEN (?) AND (?)', (last_7_dates[0], last_7_dates[-1]))

    users_last7_audience = cur.fetchall()

    users_last7_audience = users_last7_audience[0][0]

    # --- 7 day purchasers for audience ---
    cur.execute('SELECT COUNT(DISTINCT(user_id)) FROM purchases WHERE purchase_date BETWEEN (?) AND (?)', (last_7_dates[0], last_7_dates[-1]))

    rows = cur.fetchall()

    day7_purchase_audience = rows[0][0]

    # --- rank pages by views ---
    cur.execute('SELECT page_title, COUNT(page_title) FROM page_views GROUP BY page_title ORDER BY COUNT(page_title) DESC LIMIT 10')

    rows = cur.fetchall()

    pages_title_views = []

    pages_count_views = []

    # for row in rows:
    for row in rows:
        pages_title_views.append(row[0])

        pages_count_views.append(row[1])

    # --- count events ---

    # count add and checkout
    cur.execute('SELECT action FROM cart_actions')

    rows = cur.fetchall()

    add = 0

    checkout = 0

    for row in rows:
        if (row[0] == "add"):
            add += 1
        
        elif (row[0] == "checkout"):
            checkout += 1

    # count purchase
    cur.execute('SELECT COUNT(*) FROM purchases')

    rows = cur.fetchall()

    purchases = rows[0][0]

    # --- users logged day of week total ---
    cur.execute('SELECT user_id, login_date FROM user_activity')

    rows = cur.fetchall()

    # Create DataFrame with proper column names
    rows_dict = pd.DataFrame(rows, columns=['user_id', 'login_date'])

    # remove duplicates (if the same user_id logged in multiple times a day)
    rows_dict.drop_duplicates(subset=['user_id', 'login_date'], keep="first", inplace=True)

    # Initialize weekday counts (Monday=0 to Sunday=6)
    weekdays = [0] * 7

    # Initialize month counts (January=0 to December=11)
    months = [0] * 12

    for date_str in rows_dict['login_date']:

        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        
        # Count weekdays - much simpler approach
        weekday = date_obj.weekday()
        
        weekdays[weekday] += 1
        
        # Count months - note: months are 1-12 in datetime
        month = date_obj.month - 1  # convert to 0-based index
        
        months[month] += 1

    # --- users logged yearly ---
    current_year = datetime.now().year
    
    years_list = [current_year - i for i in range(4, -1, -1)]  # creates [current_year-4, ..., current_year]
    
    years = [0] * 5

    for date_str in rows_dict['login_date']:
        
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        
        year = date_obj.year
        
        if year in years_list:
            
            index = years_list.index(year)
            
            years[index] += 1

    # --- location of users that logged in this week ---
    cur.execute('SELECT DISTINCT user_location.user_id, latitude, longitude FROM user_activity JOIN user_location ON user_activity.user_id = user_location.user_id WHERE login_date BETWEEN ? AND ?', (last_7_dates[0], last_7_dates[-1]))

    rows = cur.fetchall()

    recently_active_latitude = []

    recently_active_longitude = []

    recently_active_userIds = []

    for row in rows:

        recently_active_userIds.append(row[0])

        recently_active_latitude.append(row[1])

        recently_active_longitude.append(row[2])      

    # --- location of users that logged in the last 30 days and dont belong in the week array ---

    # last 30 dates
    last_30_dates = [(datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(29, -1, -1)]

    cur.execute('SELECT DISTINCT user_location.user_id, latitude, longitude FROM user_activity JOIN user_location ON user_activity.user_id = user_location.user_id WHERE login_date BETWEEN ? AND ?', (last_30_dates[0], last_30_dates[-1]))

    rows = cur.fetchall()

    month_active_latitude = []

    month_active_longitude = []

    month_active_userIds = []

    for row in rows:

        if (row[0] not in recently_active_userIds):

            month_active_userIds.append(row[0])

            month_active_latitude.append(row[1])

            month_active_longitude.append(row[2])

    # close database
    con.commit()

    con.close()

    return render_template("behavioralInsights.html", user_location=user_location, users_audience=users_audience, non_purchasers_audience=non_purchasers_audience, users_last7_audience=users_last7_audience, day7_purchase_audience=day7_purchase_audience, pages_title_views=pages_title_views, pages_count_views=pages_count_views, add=add, checkout=checkout, purchases=purchases, weekdays=weekdays, months=months, years=years, recently_active_latitude=recently_active_latitude, recently_active_longitude=recently_active_longitude, month_active_latitude=month_active_latitude, month_active_longitude=month_active_longitude)

@app.route("/purchaseJourney")
def purchaseJourney():

    # connect to database
    con = sqlite3.connect("database.db")

    # cursor
    cur = con.cursor()

    # count
    cur.execute('SELECT device_category, COUNT(DISTINCT CASE WHEN source = "user_activity" THEN user_id END) AS unique_users, COUNT(DISTINCT CASE WHEN source = "product_views" THEN user_id END) AS unique_product_viewers, COUNT(DISTINCT CASE WHEN source = "cart_actions_add" THEN user_id END) AS unique_cart_adds, COUNT(DISTINCT CASE WHEN source = "cart_actions_checkout" THEN user_id END) AS unique_checkouts, COUNT(DISTINCT CASE WHEN source = "purchases" THEN user_id END) AS unique_purchasers FROM (SELECT user_id, device_category, "user_activity" AS source FROM user_activity UNION SELECT user_id, device_category, "product_views" AS source FROM product_views UNION SELECT user_id, device_category, "cart_actions_add" AS source FROM cart_actions WHERE action = "add" UNION SELECT user_id, device_category, "cart_actions_checkout" AS source FROM cart_actions WHERE action = "checkout" UNION SELECT user_id, device_category, "purchases" AS source FROM purchases) GROUP BY device_category')

    data = cur.fetchall()

    # get total for each column
    total = [0,0,0,0,0]

    for i in range(1,6):
        for j in range(len(data)):
            total[i - 1] += data[j][i]

    # part of total for first column
    partTotal_visitors = [0,0,0,0]

    for i in range(len(data)):
        partTotal_visitors[i] = round(data[i][1] / total[0] * 100)

    # part of total for second column
    partTotal_views = [0,0,0,0]

    for i in range(len(data)):
        partTotal_views[i] = round(data[i][2] / total[1] * 100)

    # part of total for third column
    partTotal_cart = [0,0,0,0]

    for i in range(len(data)):
        partTotal_cart[i] = round(data[i][3] / total[2] * 100)

    # part of total for fourth column
    partTotal_checkout = [0,0,0,0]

    for i in range(len(data)):
        partTotal_checkout[i] = round(data[i][4] / total[3] * 100)

    # part of total for fifth column
    partTotal_purchase = [0,0,0,0]

    for i in range(len(data)):
        partTotal_purchase[i] = round(data[i][5] / total[4] * 100)

    # drop offs
    d1 = round ( ( (total[0] - total[1]) / total[0] ) * 100 )

    d2 = round ( ( (total[1] - total[2]) / total[1] ) * 100 )

    d3 = round ( ( (total[2] - total[3]) / total[2] ) * 100 )

    d4 = round ( ( (total[3] - total[4]) / total[3] ) * 100 )

    # close database
    con.commit()

    con.close()

    return render_template("purchaseJourney.html", data=data, total=total, partTotal_visitors=partTotal_visitors, partTotal_views=partTotal_views, partTotal_cart=partTotal_cart, partTotal_checkout=partTotal_checkout, partTotal_purchase=partTotal_purchase, d1=d1, d2=d2, d3=d3, d4=d4)

@app.route("/ecommercePurchases", methods=['GET','POST'])
def ecommercePurchases():
    if request.method == 'POST':
        # connect to database
        con = sqlite3.connect("database.db")

        # cursor
        cur = con.cursor()

        # get chosen days
        selected_days = request.form.get('days')

        days = []

        dates = []

        row_length = 0

        today = date.today()

        last_day = ""

        if (selected_days == "week"):
            # get last 7 days
            days = [(datetime.now() - timedelta(days=i)).strftime('%d') for i in range(6, -1, -1)]

            # get last 7 dates
            dates = [(datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(6, -1, -1)]

            row_length = 7

            last_day = date.today() - timedelta(days=6)

        if (selected_days == "month"):
            # get last 30 days
            days = [(datetime.now() - timedelta(days=i)).strftime('%d') for i in range(29, -1, -1)]

            # get last 30 dates
            dates = [(datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(29, -1, -1)]

            row_length = 30

            last_day = date.today() - timedelta(days=29)       

        # get selected filter
        selected_filter = request.form.get('filters')

        data = []

        # revenue
        if(selected_filter == "revenue"):
            # get top products with the most revenue
            cur.execute('SELECT p.name AS product_name, COUNT(DISTINCT pv.id) AS view_count, COUNT(DISTINCT CASE WHEN ca.action = "add" THEN ca.id END) AS add_to_cart_count, COALESCE(pu.purchase_count, 0) AS purchase_count, COALESCE(pu.total_revenue, 0) AS total_revenue FROM products p LEFT JOIN product_views pv ON p.id = pv.product_id LEFT JOIN cart_actions ca ON p.id = ca.product_id LEFT JOIN (SELECT product_id, COUNT(id) AS purchase_count, SUM(total_price) AS total_revenue FROM purchases GROUP BY product_id) pu ON p.id = pu.product_id GROUP BY p.id ORDER BY total_revenue DESC LIMIT 10')

            data = cur.fetchall()

            # get total_price and purchase_date of all items
            cur.execute('SELECT name, total_price, purchase_date FROM purchases JOIN products ON purchases.product_id = products.id')

            purchases = cur.fetchall()

            # get selected products
            products = request.form.getlist('products')

            # turn dictionary into dataframe
            purchases_dict = pd.DataFrame.from_dict(purchases)

            default = []

            # if user has selected products
            if (products):
                # assign revenue
                default = numpy.zeros((len(products),row_length))

                for i in range(len(products)):
                    for j in range(len(dates)):
                        for k in range(len(purchases_dict)):
                            if (purchases_dict[0][k] == products[i] and purchases_dict[2][k] == dates[j]):
                                default[i][j] += purchases_dict[1][k]

                # Convert the array to list
                default = default.tolist()
            else:
                default = []

            filter_header = "Item revenue"


        # purchase
        if(selected_filter == "purchased"):
            # get top products with the most purchases
            cur.execute('SELECT p.name AS product_name, COUNT(DISTINCT pv.id) AS view_count, COUNT(DISTINCT CASE WHEN ca.action = "add" THEN ca.id END) AS add_to_cart_count, COALESCE(pu.purchase_count, 0) AS purchase_count, COALESCE(pu.total_revenue, 0) AS total_revenue FROM products p LEFT JOIN product_views pv ON p.id = pv.product_id LEFT JOIN cart_actions ca ON p.id = ca.product_id LEFT JOIN (SELECT product_id, COUNT(id) AS purchase_count, SUM(total_price) AS total_revenue FROM purchases GROUP BY product_id) pu ON p.id = pu.product_id GROUP BY p.id ORDER BY purchase_count DESC LIMIT 10')

            data = cur.fetchall()

            # get total_price and purchase_date of all items
            cur.execute('SELECT name, total_price, purchase_date FROM purchases JOIN products ON purchases.product_id = products.id')

            purchases = cur.fetchall()

            # get selected products
            products = request.form.getlist('products')

            # turn dictionary into dataframe
            purchases_dict = pd.DataFrame.from_dict(purchases)

            default = []

            # if user has selected products
            if (products):
                
                # assign revenue
                default = numpy.zeros((len(products),row_length))

                for i in range(len(products)):
                    for j in range(len(dates)):
                        for k in range(len(purchases_dict)):
                            if (purchases_dict[0][k] == products[i] and purchases_dict[2][k] == dates[j]):
                                default[i][j] += 1

                # Convert the array to list
                default = default.tolist()

            filter_header = "Items purchased"

        # cart
        if(selected_filter == "cart"):
            # order rows by cart
            cur.execute('SELECT p.name AS product_name, COUNT(DISTINCT pv.id) AS view_count, COUNT(DISTINCT CASE WHEN ca.action = "add" THEN ca.id END) AS add_to_cart_count, COALESCE(pu.purchase_count, 0) AS purchase_count, COALESCE(pu.total_revenue, 0) AS total_revenue FROM products p LEFT JOIN product_views pv ON p.id = pv.product_id LEFT JOIN cart_actions ca ON p.id = ca.product_id LEFT JOIN (SELECT product_id, COUNT(id) AS purchase_count, SUM(total_price) AS total_revenue FROM purchases GROUP BY product_id) pu ON p.id = pu.product_id GROUP BY p.id ORDER BY add_to_cart_count DESC LIMIT 10')

            data = cur.fetchall()

            # get cart rows
            cur.execute('SELECT name, action_date FROM cart_actions JOIN products ON cart_actions.product_id = products.id WHERE action = "add"')

            cart = cur.fetchall()

            # get selected products
            products = request.form.getlist('products')

            # turn dictionary into dataframe
            cart_dict = pd.DataFrame.from_dict(cart)

            default = []

            # if user has selected products
            if (products):
                
                # assign revenue
                default = numpy.zeros((len(products),row_length))

                for i in range(len(products)):
                    for j in range(len(dates)):
                        for k in range(len(cart_dict)):
                            if (cart_dict[0][k] == products[i] and cart_dict[1][k] == dates[j]):
                                default[i][j] += 1

                # Convert the array to list
                default = default.tolist()

            filter_header = "Items added to cart"

        # views
        if(selected_filter == "views"):
            # order rows by cart
            cur.execute('SELECT p.name AS product_name, COUNT(DISTINCT pv.id) AS view_count, COUNT(DISTINCT CASE WHEN ca.action = "add" THEN ca.id END) AS add_to_cart_count, COALESCE(pu.purchase_count, 0) AS purchase_count, COALESCE(pu.total_revenue, 0) AS total_revenue FROM products p LEFT JOIN product_views pv ON p.id = pv.product_id LEFT JOIN cart_actions ca ON p.id = ca.product_id LEFT JOIN (SELECT product_id, COUNT(id) AS purchase_count, SUM(total_price) AS total_revenue FROM purchases GROUP BY product_id) pu ON p.id = pu.product_id GROUP BY p.id ORDER BY view_count DESC LIMIT 10')

            data = cur.fetchall()

            # get views rows
            cur.execute('SELECT name, view_date FROM product_views JOIN products ON product_views.product_id = products.id')

            views = cur.fetchall()

            # get selected products
            products = request.form.getlist('products')

            # turn dictionary into dataframe
            views_dict = pd.DataFrame.from_dict(views)

            default = []

            # if user has selected products
            if (products):
                
                # assign revenue
                default = numpy.zeros((len(products),row_length))

                for i in range(len(products)):
                    for j in range(len(dates)):
                        for k in range(len(views_dict)):
                            if (views_dict[0][k] == products[i] and views_dict[1][k] == dates[j]):
                                default[i][j] += 1

                # Convert the array to list
                default = default.tolist()

            filter_header = "Items viewed"

        # close database
        con.commit()

        con.close()

        return render_template("ecommercePurchases.html", data=data, days=days, default=default, products=products, filter_header=filter_header, today=today, last_day=last_day)
    
    if request.method == 'GET':
        # connect to database
        con = sqlite3.connect("database.db")

        # cursor
        cur = con.cursor()

        # get last 7 days
        days = [(datetime.now() - timedelta(days=i)).strftime('%d') for i in range(6, -1, -1)]

        # get last 7 dates
        dates = [(datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(6, -1, -1)]

        # get today
        today = date.today()

        # date seven days ago
        last_day = date.today() - timedelta(days=7)

        # get selected filter
        selected_filter = request.form.get('filters')

        data = []

        # order rows by cart
        cur.execute('SELECT p.name AS product_name, COUNT(DISTINCT pv.id) AS view_count, COUNT(DISTINCT CASE WHEN ca.action = "add" THEN ca.id END) AS add_to_cart_count, COALESCE(pu.purchase_count, 0) AS purchase_count, COALESCE(pu.total_revenue, 0) AS total_revenue FROM products p LEFT JOIN product_views pv ON p.id = pv.product_id LEFT JOIN cart_actions ca ON p.id = ca.product_id LEFT JOIN (SELECT product_id, COUNT(id) AS purchase_count, SUM(total_price) AS total_revenue FROM purchases GROUP BY product_id) pu ON p.id = pu.product_id GROUP BY p.id ORDER BY view_count DESC LIMIT 10')

        data = cur.fetchall()

        # get views rows
        cur.execute('SELECT name, view_date FROM product_views JOIN products ON product_views.product_id = products.id')

        views = cur.fetchall()

        # get selected products
        products = request.form.getlist('products')

        # turn dictionary into dataframe
        views_dict = pd.DataFrame.from_dict(views)

        default = []

        # if user has selected products
        if (products):
            
            # assign revenue
            default = numpy.zeros((len(products),7))

            for i in range(len(products)):
                for j in range(len(dates)):
                    for k in range(len(views_dict)):
                        if (views_dict[0][k] == products[i] and views_dict[1][k] == dates[j]):
                            default[i][j] += 1

            # Convert the array to list
            default = default.tolist()

        filter_header = "Items viewed"

        # close database
        con.commit()

        con.close()

        return render_template("ecommercePurchases.html", data=data, days=days, default=default, filter_header=filter_header, today=today, last_day=last_day)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)