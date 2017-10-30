#!/usr/bin/env python3

import psycopg2

DB_NAME = "news"


# query 1
def get_top_articles():
    query = "SELECT title, count(*) AS views FROM articles LEFT JOIN log " + \
        "ON log.path = '/article/' || articles.slug " + \
        "GROUP BY articles.title ORDER BY views DESC LIMIT 3"

    return get_results(query)


# query 2
def get_most_popular_authors():
    query = "SELECT authors.name, count(*) AS views " + \
        "FROM authors, articles, log " + \
        "WHERE log.path = '/article/' || articles.slug " + \
        "AND articles.author = " + \
        "authors.id GROUP BY authors.name ORDER BY views DESC"

    return get_results(query)


# query 3
def get_days_with_error():
    # inner queries
    error_stats = "SELECT date_trunc('day', time) AS day, count(*) " + \
        "AS num " + \
        "FROM log WHERE status LIKE '4%' OR status LIKE '5%' GROUP BY day"

    all_stats = "SELECT date_trunc('day', time) AS day, count(*) " + \
        "AS num " + \
        "FROM log GROUP BY day"

    q = "SELECT errors.day AS day, " + \
        "(CAST (errors.num AS FLOAT)) / (CAST (total.num AS FLOAT)) " + \
        "AS ratio " + \
        "FROM (" + all_stats + ") AS total JOIN (" + error_stats + ") " + \
        "AS errors " + \
        "ON total.day = errors.day "

    qq = "SELECT day, 100 * ratio || '%' " + \
        "FROM (" + q + ") AS q WHERE ratio > 0.01"

    return get_results(qq)


# general query function
def get_results(query):
    db = psycopg2.connect("dbname=" + DB_NAME)
    cur = db.cursor()

    cur.execute(query)
    rows = cur.fetchall()
    print(rows)
    db.close()

    return rows
