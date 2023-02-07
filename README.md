# 636-final-library-app
# Structure 
# 1, This library web has two interfaces, one for the public and one for the staff to use

# 2, The public interface has two main functions, search function where users can search books by author or/and title, showing results through result.html template,  and book list function, showing results through booklist.html.

# 3, The Staff interface has nine functions, 1, search function, similar to the public search function, 2, borrowers function with borrowersearch.html and borrowerresult.html templates which help staff to search borrowers by name or/and ID. 3, Staff can also update or add a borrower, using the updateborrower, addborrower functions, updateaborrower.html and addborrower.html. THe results will be displayed through updateconfirm.html and addconfirm.html. 4, Issue books and return books functions are achieved through issuebooks.html and returnbook.html. Both failure or success will be displayed. 5, overdue books, loan summary and borrower summary functions are achieved through overduebooks.html, loansummary.html and borrowersummary.html.

# Assumptions and Design
# 1, I assume that most users will start using the web from searching the book or borrower. So that I put "search" as the first option of the menu. For both interfaces, I use visible navigation bars so that users are able to complete their tasks quickly and smoothly.

# 2, Users get feedback everytime when they are updating information, returning books or issuing books, with a page showing if they have successfully done so or a failure occurs.

# 3, All results or reports are clearly shown on tables, which are easy to understand. 

# 4, Any value input by users is passed across different pages through post method to keep it safe and secret. 

# 5, There is a base.html for both public and staff interface as these two interfaces require different menus and offer different features.

# changes required to support multiple branches
# 1, if the application is to support multiple library branches, more tables need to be added, such as a location table

# 2, when searching for available books, the locations of available books also need to be shown to the users. 

# 3, a feature which allows users to request a book from the other branchs should be added

# 4, The staff of different branches can use a same interface if different branches can share a same database.



