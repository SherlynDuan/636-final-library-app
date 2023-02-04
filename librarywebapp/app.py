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

@app.route ("/searchresult", methods=["POST"])
def searchresult():
    author=request.form.get("author")
    authorsearch = "%" + author + "%"
    title =request.form.get("title")
    titlesearch = "%" + title + "%"
    connection = getCursor()
    
    if author is '':
        connection.execute("SELECT books.bookid, books.booktitle, books.author, bookcopies.bookcopyid, bookcopies.format,\
       loans.returned, DATEDIFF(CURDATE(),loans.loandate) \
        FROM books inner join bookcopies on books.bookid = bookcopies.bookid inner join loans \
        on bookcopies.bookcopyid=loans.bookcopyid WHERE booktitle LIKE %s;",(titlesearch,)) 
        result_list = connection.fetchall()
    
    elif title is '':
        connection.execute("SELECT books.bookid, books.booktitle, books.author, bookcopies.bookcopyid, bookcopies.format,\
       loans.returned, DATEDIFF(CURDATE(),loans.loandate) \
        FROM books inner join bookcopies on books.bookid = bookcopies.bookid inner join loans \
        on bookcopies.bookcopyid=loans.bookcopyid WHERE author LIKE %s;",(authorsearch,)) 
        result_list= connection.fetchall()

    else:
        connection.execute("SELECT books.bookid, books.booktitle, books.author, bookcopies.bookcopyid, bookcopies.format,\
       loans.returned, DATEDIFF(CURDATE(),loans.loandate) \
        FROM books inner join bookcopies on books.bookid = bookcopies.bookid inner join loans \
        on bookcopies.bookcopyid=loans.bookcopyid WHERE author LIKE %s And booktitle LIKE %s;",(authorsearch,titlesearch,)) 
        result_list= connection.fetchall()
    
    print (result_list)

    return render_template ("result.html", author=author, title=title, result_list = result_list )
    
                
    



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


@app.route("/staff/borrowersearch")
def borrowersearch():
    return render_template("borrowersearch.html") 

@app.route("/staff/borrowersearchresult", methods=["GET", "POST"])
def borrowersearchresult():
    name=request.form.get("name")
    namesearch = "%" + name + "%"
    borrowerid =request.form.get("borrowerid")
    borroweridsearch= "%" + borrowerid + "%"
    connection = getCursor()
    
    
    if borrowerid == '':
        connection.execute("SELECT * from borrowers WHERE firstname LIKE %s OR familyname LIKE %s;", (namesearch, namesearch, ))
        result_list = connection.fetchall()

    elif name == '':
        connection.execute("SELECT * from borrowers WHERE borrowerid LIKE %s;", (borroweridsearch, ))
        result_list = connection.fetchall()       

    else:
        connection.execute ("SELECT * from borrowers WHERE borrowerid LIKE %s AND (familyname LIKE %s OR firstname LIKE %s);", (borroweridsearch,namesearch, namesearch,)) 
        result_list = connection.fetchall()
    
    
    return render_template ("borrowerresult.html", name=name, borrowerid=borrowerid, result_list = result_list)
                


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