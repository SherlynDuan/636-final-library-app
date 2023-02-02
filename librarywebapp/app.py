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
    connection.execute("SELECT * FROM books;")
    bookList = connection.fetchall()
    print(bookList)
    return render_template("booklist.html", booklist = bookList)    

@app.route("/loanbook")
def loanbook():
    todaydate = datetime.now().date()
    connection = getCursor()
    connection.execute("SELECT * FROM borrowers;")
    borrowerList = connection.fetchall()
    sql = """SELECT * FROM bookcopies
inner join books on books.bookid = bookcopies.bookid
 WHERE bookcopyid not in (SELECT bookcopyid from loans where returned <> 1 or returned is NULL);"""
    connection.execute(sql)
    bookList = connection.fetchall()
    return render_template("addloan.html", loandate = todaydate,borrowers = borrowerList, books= bookList)

@app.route("/loan/add", methods=["POST"])
def addloan():
    borrowerid = request.form.get('borrower')
    bookid = request.form.get('book')
    loandate = request.form.get('loandate')
    cur = getCursor()
    cur.execute("INSERT INTO loans (borrowerid, bookcopyid, loandate, returned) VALUES(%s,%s,%s,0);",(borrowerid, bookid, str(loandate),))
    return redirect("/currentloans")

@app.route("/listborrowers")
def listborrowers():
    connection = getCursor()
    connection.execute("SELECT * FROM borrowers;")
    borrowerList = connection.fetchall()
    return render_template("borrowerlist.html", borrowerlist = borrowerList)

@app.route("/currentloans")
def currentloans():
    connection = getCursor()
    sql=""" select br.borrowerid, br.firstname, br.familyname,  
                l.borrowerid, l.bookcopyid, l.loandate, l.returned, b.bookid, b.booktitle, b.author, 
                b.category, b.yearofpublication, bc.format 
            from books b
                inner join bookcopies bc on b.bookid = bc.bookid
                    inner join loans l on bc.bookcopyid = l.bookcopyid
                        inner join borrowers br on l.borrowerid = br.borrowerid
            order by br.familyname, br.firstname, l.loandate;"""
    connection.execute(sql)
    loanList = connection.fetchall()
    return render_template("currentloans.html", loanlist = loanList)