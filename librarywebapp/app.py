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

#  The public interface
@app.route("/")
def home():
    return render_template("home.html")

#Search the available books by title and/or author, See the availability of all copies of a book, whether a copy is on loan and, if so, the due date.
@app.route ("/search")
def search():
    return render_template ("search.html")

# show results of the book search, get input value from forms, allow for partial text searches
@app.route ("/searchresult", methods=["POST"])
def searchresult():
    author=request.form.get("author")
    authorsearch = "%" + author + "%"
    title =request.form.get("title")
    titlesearch = "%" + title + "%"
    connection = getCursor()

# an if condition to test which input is empty
# if the author input is empty   
    if author == '':
        connection.execute("SELECT books.bookid, books.booktitle, books.author, bookcopies.bookcopyid, bookcopies.format,\
       loans.returned, DATEDIFF(CURDATE(),loans.loandate) \
        FROM bookcopies LEFT JOIN books on books.bookid = bookcopies.bookid LEFT JOIN loans \
        on bookcopies.bookcopyid=loans.bookcopyid WHERE booktitle LIKE %s;",(titlesearch,)) 
        result_list = connection.fetchall()
# if the title input is empty      
    elif title == '':
        connection.execute("SELECT books.bookid, books.booktitle, books.author, bookcopies.bookcopyid, bookcopies.format,\
       loans.returned, DATEDIFF(CURDATE(),loans.loandate) \
        FROM bookcopies LEFT JOIN books on books.bookid = bookcopies.bookid LEFT JOIN loans \
        on bookcopies.bookcopyid=loans.bookcopyid WHERE booktitle LIKE %s;",(authorsearch,)) 
        result_list= connection.fetchall()

    else:
        connection.execute("SELECT books.bookid, books.booktitle, books.author, bookcopies.bookcopyid, bookcopies.format,\
       loans.returned, DATEDIFF(CURDATE(),loans.loandate) \
        FROM bookcopies LEFT JOIN books on books.bookid = bookcopies.bookid LEFT JOIN loans \
        on bookcopies.bookcopyid=loans.bookcopyid WHERE author LIKE %s And booktitle LIKE %s;",(authorsearch,titlesearch,)) 
        result_list= connection.fetchall()
    
    print (result_list)

    return render_template ("result.html", author=author, title=title, result_list = result_list )
    
# List all books available in the library at the /booklist route Include book title, author,category and year of publication.                
@app.route("/listbooks")
def listbooks():
    connection = getCursor()
    connection.execute("SELECT bookid, booktitle, author, category, \
    yearofpublication FROM books ;")
    bookList = connection.fetchall()
    print(bookList)
    return render_template("booklist.html", booklist = bookList)  

# homepage of the staff interface
@app.route("/staff")
def staff():
    return render_template("staffhome.html") 

#Search the available books by title and/or author, See the availability of all copies of a book, whether a copy is on loan and, if so, the due date.
@app.route ("/search")
@app.route("/staff/search")
def staffsearch():
    return render_template("staffsearch.html")

## show results of the book search, get input value from forms, allow for partial text searches. 
@app.route ("/staffsearchresult", methods=["POST"])
def staffsearchresult():
    author=request.form.get("author")
    authorsearch = "%" + author + "%"
    title =request.form.get("title")
    titlesearch = "%" + title + "%"
    connection = getCursor()
    
    if author  == '':
        connection.execute("SELECT books.bookid, books.booktitle, books.author, bookcopies.bookcopyid, bookcopies.format,\
       loans.returned,  DATEDIFF(CURDATE(),loans.loandate) \
        FROM bookcopies LEFT JOIN books on books.bookid = bookcopies.bookid LEFT JOIN loans \
        on bookcopies.bookcopyid=loans.bookcopyid WHERE booktitle LIKE %s;",(titlesearch,)) 
        result_list = connection.fetchall()

    
    elif title  == '':
        connection.execute("SELECT books.bookid, books.booktitle, books.author, bookcopies.bookcopyid, bookcopies.format,\
       loans.returned, DATEDIFF(CURDATE(),loans.loandate) \
        FROM bookcopies LEFT JOIN books on books.bookid = bookcopies.bookid LEFT JOIN loans \
        on bookcopies.bookcopyid=loans.bookcopyid WHERE booktitle LIKE %s;",(titlesearch,)) 
        result_list= connection.fetchall()

    else:
        connection.execute("SELECT books.bookid, books.booktitle, books.author, bookcopies.bookcopyid, bookcopies.format,\
       loans.returned, DATEDIFF(CURDATE(),loans.loandate) \
        FROM bookcopies LEFT JOIN books ON books.bookid = bookcopies.bookid LEFT JOIN loans \
        on bookcopies.bookcopyid=loans.bookcopyid WHERE author LIKE %s And booktitle LIKE %s;",(authorsearch,titlesearch,)) 
        result_list= connection.fetchall()
    
    print (result_list)

    return render_template ("staffsearch_result.html", author=author, title=title, result_list = result_list )

 

# View the details of a borrower, searching by name or by borrower id.
@app.route("/staff/borrowersearch")
def borrowersearch():
    return render_template("borrowersearch.html") 

#show borrowe rsearch results

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
                

# Update the details of a borrower
@app.route("/staff/updateborrower")
def updateborrower():
    return render_template("updateborrower.html") 


# get the borrower id that the staff wants to update
@app.route("/staff/borrowerid",  methods=["GET", "POST"])
def staffborrowerid():
    id=request.form.get("id")
    connection = getCursor()
    connection.execute ("SELECT * from borrowers WHERE borrowerid = %s;", (id,) )
    results= connection.fetchall()
    print (results)

    return render_template("iddetails.html", id=id, results=results) 

#upda information to the database
@app.route("/staff/updateinfo",  methods=["GET", "POST"])
def staffupdateinfo():
    ID=request.form.get("id")
    Firstname=request.form.get("firstname")
    Familyname=request.form.get("familyname")
    Dateofbirth=request.form.get("dateofbirth")
    Housenumbername=request.form.get("housenumbername")
    Street=request.form.get("street")
    Town=request.form.get("town")
    City=request.form.get("city")
    Postalcode=request.form.get("postalcode")
    connection = getCursor()
    connection.execute ( "UPDATE borrowers SET firstname=%s, familyname=%s,\
        dateofbirth=%s,  housenumbername=%s, street=%s, town=%s, \
            city=%s, postalcode=%s  WHERE borrowerid= %s;" , (Firstname, Familyname, Dateofbirth,\
                Housenumbername, Street, Town, City, Postalcode, ID,  ))
    connection.execute ( "SELECT * FROM borrowers WHERE borrowerid= %s;" , (ID, ) )
    results_list = connection.fetchall()
    print (results_list)
    return render_template ("updateconfirm.html", ID=ID, results_list= results_list)


 
#Add a new borrower
@app.route("/staff/addborrower")
def addborrower():
    return render_template("addborrower.html")


#get all input value from users and insert into database
@app.route("/staff/addborrowerinfo",  methods=["GET", "POST"])
def addborrowerinfo():
    Firstname=request.form.get("firstname")
    Familyname=request.form.get("familyname")
    Dateofbirth=request.form.get("dateofbirth")
    Housenumbername=request.form.get("housenumbername")
    Street=request.form.get("street")
    Town=request.form.get("town")
    City=request.form.get("city")
    Postalcode=request.form.get("postalcode")
    connection = getCursor()
    connection.execute ( "INSERT INTO borrowers (firstname, familyname, dateofbirth,  housenumbername, street, town, \
            city, postalcode ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s );", (Firstname, Familyname, Dateofbirth,\
                Housenumbername, Street, Town, City, Postalcode, ))
    connection.execute ( "SELECT * from borrowers ORDER BY borrowerid DESC LIMIT 1;")
    results_list = connection.fetchall()

    print (results_list)
    return render_template ("addconfirm.html", results_list= results_list)

#Issue a book to a borrower. Physical Books can only be loaned once at a time , eBooks and Audio Books can be loaned multiple times simultaneously
#staff type in book copy id and borrower id
@app.route("/staff/issuebooks")
def issuebooks():
    return render_template("issuebooks.html")

#show results of issuing books and update database.
@app.route( "/staff/issuebooks_result",  methods=["GET", "POST"])
def issuebooks_result():
    bookcopyid=request.form.get("bookid")
    borrowerid=request.form.get("borrowerid")
    todaydate = datetime.now().date()
    connection = getCursor()
    connection.execute ( "SELECT bookcopies.bookcopyid, bookcopies.format, loans.borrowerid, loans.returned, loans.loandate From loans RIGHT JOIN bookcopies \
        on loans.bookcopyid=bookcopies.bookcopyid WHERE bookcopies.bookcopyid = %s ORDER by loans.loandate DESC LIMIT 1  ;", (bookcopyid, ) )
    loans= connection.fetchall()
    print (loans)

    #an if condition to test if the book is a Physical one or not
    if loans[0][1] == "eBook" or loans[0][1] == "Audio Book" :
        connection = getCursor()
        connection.execute ( " INSERT INTO loans (bookcopyid, borrowerid , loandate, returned) VALUES (%s, %s,%s,0);", (bookcopyid, borrowerid, todaydate, ) )
        return render_template ("issuebook_success.html", bookcopyid=bookcopyid, borrowerid=borrowerid, todaydate=todaydate)

    elif (loans[0][1] == "Hardcover" or "paperback" or "Illustrated") and loans[0][3] == 1:
        connection = getCursor()
        connection.execute ( " INSERT INTO loans (bookcopyid, borrowerid , loandate, returned) VALUES (%s, %s,%s,0);", (bookcopyid, borrowerid, todaydate, ) )
        return render_template("issuebook_success.html", bookcopyid=bookcopyid, borrowerid=borrowerid, todaydate=todaydate)
        
    else:
        return render_template( "issuebook_fail.html")


#Return a book that has been on loan
@app.route("/staff/returnbooks")
def returnbooks():
    return render_template("returnbooks.html") 

#return results
@app.route("/staff/returnbooks_result",  methods=["GET", "POST"] )
def returnbooks_result():
    bookcopyid=request.form.get("bookid")
    borrowerid=request.form.get("borrowerid")
    todaydate = datetime.now().date()
    connection = getCursor()
    connection.execute ( " UPDATE loans SET returned = 1 WHERE bookcopyid= %s AND borrowerid= %s;", (bookcopyid, borrowerid, ))
    return render_template("return_success.html", borrowerid=borrowerid, bookcopyid=bookcopyid, todaydate=todaydate )

    
#Display a list of all overdue books & their borrowers. Group all overdue books by borrower 
@app.route("/staff/overduebooks")
def overduebooks():
    connection = getCursor()
    connection.execute ( " SELECT borrowers.firstname, borrowers.familyname, loans.borrowerid, books.booktitle, bookcopies.bookcopyid, DATEDIFF(CURDATE(),loans.loandate) AS daysonLoan FROM borrowers \
        INNER JOIN loans on loans.borrowerid=borrowers.borrowerid\
        INNER JOIN bookcopies on loans.bookcopyid= bookcopies.bookcopyid \
        INNER JOIN books on books.bookid=bookcopies.bookid\
        WHERE loans.returned = 0 and DATEDIFF(CURDATE(),loans.loandate) >=35;")
    overdue_list=connection.fetchall()
    print ( overdue_list)    
    return render_template("overduebooks.html", overdue_list=overdue_list) 

#Display a list (Loan Summary) showing the number of times each book has been loaned in total.
@app.route("/staff/loansummary")
def loansummary():
    connection = getCursor()
    connection.execute ("SELECT books.bookid, books.booktitle, COUNT(loans.loanid) FROM loans LEFT JOIN bookcopies \
        ON bookcopies.bookcopyid=loans.bookcopyid INNER JOIN books ON books.bookid=bookcopies.bookid \
        GROUP BY bookcopies.bookid ORDER BY COUNT(loans.loanid) DESC;")
    loansummary=connection.fetchall()

    return render_template("loansummary.html", loansummary=loansummary) 

#Display a list (Borrower Summary) showing all borrowers and the number of loans (past and current combined) in total they each have had.
@app.route("/staff/borrowersummary")
def borrowersummary():
    connection = getCursor()
    connection.execute (" SELECT borrowers.borrowerid, borrowers.firstname,borrowers.familyname, COUNT(loans.loanid) FROM loans LEFT JOIN borrowers \
        ON borrowers.borrowerid=loans.borrowerid GROUP BY loans.borrowerid ORDER BY COUNT(loans.loanid) DESC;")
    borrowersummary=connection.fetchall()
    return render_template("borrowersummary.html", borrowersummary=borrowersummary) 