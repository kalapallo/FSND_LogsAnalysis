# FSND - Logs Analysis

This program creates a Python web server that connects to a "news" database to fetch information from it. The web site contains three buttons, each of them performing one query and printing the results under the buttons.

## How to set up the database

In a terminal running on a Linux virtual machine, get the file "newdata.sql" and run the command "psql -d news -f newsdata.sql". This will connect to the database server and execute the SQL commands in the file creating tables and populating them with data.

## How to run

Open a terminal in the directory where all the files are installed. Run "python logserver.py" in the directory where the files are located. The webserver is started on localhost and will listen to port 8000, so the website can be accessed at http://localhost:8000. Click on any of the query buttons to get the results printed.

## Prerequisites

Python3, Flask, psycopg2
