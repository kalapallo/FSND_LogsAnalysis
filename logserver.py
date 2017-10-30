#!/usr/bin/env python3

from flask import Flask, request, redirect, url_for
from logs import get_top_articles, get_most_popular_authors,\
get_days_with_error

app = Flask(__name__)

# HTML template for the query page
HTML_WRAP = '''\
<!DOCTYPE html>
<html>
  <head>
    <title>Logs Analysis</title>
  </head>
  <body>
    <h1>Log queries</h1>
    <form method=post>
      <div><button name="q" value="q1" type="submit">Query 1</button></div>
      <div><button name="q" value="q2" type="submit">Query 2</button></div>
      <div><button name="q" value="q3" type="submit">Query 3</button></div>
    </form>
    <!-- query results will go here -->
%s
  </body>
</html>
'''

# HTML template for a query
LOG_RESULT = '''\
    <table>
      <tr>
        <th>%s</th>
        <th>%s</th>
      </tr>
    %s
    </table>
'''

ROW = '''\
    <tr>
      <td>%s</td>
      <td>%s</td>
    </tr>
'''

# The results will be saved to this global variable.
# I know global variables are evil, but I am doing it for simplicity's sake.
# I have no idea why this doesn't work as a string, but somehow works
# as a tuple. It's a terrible way to do this as the tuple grows on each
# query, and also clearing it at any point in the code empties and breaks it.
# In addition, the previous results will be shown on the web form whenever a
# GET operation is performed. Normally I'd write a class and the object could
# hold this data, but since this is just procedural code I don't know any
# better way to keep the data after a POST. Maybe the fetching part should be
# done on GET instead.
# Hopefully the person reading this comment can enlighten me...
query_result = [""]


@app.route('/', methods=['GET'])
def main():
    html = HTML_WRAP % query_result[-1]
    return html


@app.route('/', methods=['POST'])
def post():
    '''Send a command to database and parse the results'''
    button = request.form['q']

    if button == "q1":
        rows = get_top_articles()
        generate_table(rows, 'Article', 'Views')

    elif button == "q2":
        rows = get_most_popular_authors()
        generate_table(rows, 'Author', 'Views')

    elif button == "q3":
        rows = get_days_with_error()
        print(rows)
        generate_table(rows, 'Date', 'Errors')

    return redirect(url_for('main'))


def generate_table(rows, col1, col2):
    '''Generate a HTML table with two columns'''
    html_rows = ""
    for r in rows:
        html_rows += ROW % (r[0], r[1])

    query_result.append(LOG_RESULT % (col1, col2, html_rows))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
