from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
import re
from datetime import datetime
from datetime import date
import mysql.connector
from mysql.connector import FieldType
import connect

app = Flask(__name__)

dbconn = None
connection = None

def getCursor():
    global dbconn
    global connection
    connection = mysql.connector.connect(user=connect.dbuser, \
    password=connect.dbpass, host=connect.dbhost, \
    database=connect.dbname, autocommit=True)
    dbconn = connection.cursor()
    return dbconn

@app.route("/")
def home():
    return render_template("home.html")

@app.route ("/search")
def search():
    return render_template ("search.html")

@app.route ("/searchresult", methods=["GET", "POST"])
def searchresult():
    author=request.args.get("author")
    title =request.args.get("title")
    connection = getCursor()
    connection.execute("SELECT books.bookid, books.booktitle, books.author, bookcopies.bookcopyid, bookcopies.format,\
       loans.returned, DATEDIFF(CURDATE(),loans.loandate) \
        FROM books inner join bookcopies on books.bookid = bookcopies.bookid inner join loans \
        on bookcopies.bookcopyid=loans.bookcopyid;")
    resultlist = connection.fetchall()
    result_list=[]

    
    if author is '':
        for result in resultlist:
            if title.lower() in result[1].lower():           
                result_list.append(result)
    
    elif title is '':
        for result in resultlist:
            if author.lower() in result[2].lower():           
                result_list.append(result)
    
    elif author is not '' and title is not '':
        for result in resultlist:
            if (author.lower() in result[2].lower()) and (title.lower() in result[1].lower()) :           
                result_list.append(result)
                print(result_list)
    
    if len(result_list) == 0:
        return render_template ("noresult.html", author=author, title=title)
    else:
        return render_template ("result.html", author=author, title=title, result_list = result_list)
                
    



@app.route("/listbooks")
def listbooks():
    connection = getCursor()
    connection.execute("SELECT bookid, booktitle, author, category, \
    yearofpublication FROM books;")
    bookList = connection.fetchall()
    print(bookList)
    return render_template("booklist.html", booklist = bookList)  


@app.route("/staff")
def staff():
    return render_template("staffhome.html") 

@app.route("/staff/search")
def staffsearch():
    return render_template("staffsearch.html") 


@app.route("/staff/borrowerlist")
def borrowerlist():
    return render_template("borrowerlist.html") 


@app.route("/staff/updateborrower")
def updateborrower():
    return render_template("updateborrower.html") 

@app.route("/staff/issuebooks")
def issuebooks():
    return render_template("issuebooks.html") 

@app.route("/staff/returnbooks")
def returnbooks():
    return render_template("returnbooks.html") 

@app.route("/staff/overduebooks")
def overduebooks():
    return render_template("overduebooks.html") 

@app.route("/staff/loansummary")
def loansummary():
    return render_template("loansummary.html") 

@app.route("/staff/borrowersummary")
def borrowersummary():
    return render_template("borrowersummary.html") 
           



    