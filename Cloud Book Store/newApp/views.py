from django.http import HttpResponse
from django.db import connection, transaction
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from datetime import datetime, date
from django.utils import formats
from . forms import *
from . views import *



#HOMEPAGE OF THE PLATFORM
#Function to display the homepage of the Online Book Shopping Platform
def index(request):
    if request.session.has_key('user_id'):
        return redirect('userProfile')
    elif request.session.has_key('email'):
        return redirect('storeProfile')
    else:
        return render(request = request, template_name = 'home.html')




#Function to display trending books in the platform
def trendingList(request):
    if request.session.has_key('user_id'):
        return redirect('userProfile')
    elif request.session.has_key('email'):
        return redirect('storeProfile')
    else:
        if request.method == "POST":
            Parameter  = request.POST["Parameter"]

            if Parameter == "Rating":
                entry_count = 10
                cursor = connection.cursor()
                query_fetch_book = '''SELECT book_id, title, author, publisher, genre, year_of_publish, copies_sold, rating
                                      FROM Book
                                      ORDER BY rating
                                      DESC LIMIT 10'''

                cursor.execute(query_fetch_book)
                q_result = cursor.fetchall()
            
            else:
                entry_count = 10
                cursor = connection.cursor()
                query_fetch_book = '''SELECT book_id, title, author, publisher, genre, year_of_publish, copies_sold, rating
                                      FROM Book
                                      ORDER BY copies_sold
                                      DESC LIMIT 10'''

                cursor.execute(query_fetch_book)
                q_result = cursor.fetchall()

            # t_list = Book.objects.all().order_by('-copies_sold')[:10]
            trending_list = []
            # print(q_result)
            for query_result in q_result:
                t_list = {}
                t_list['title']             = query_result[1]
                t_list['author']            = query_result[2]
                t_list['publisher']         = query_result[3]
                t_list['genre']             = query_result[4]
                t_list['year_of_publish']   = query_result[5]
                t_list['copies_sold']       = query_result[6]
                t_list['rating']            = query_result[7]
                trending_list.append(t_list)


            return render(request, 'trending_list.html', {"t_list": trending_list})
        else:
            entry_count = 10
            cursor = connection.cursor()
            query_fetch_book = '''SELECT book_id, title, author, publisher, genre, year_of_publish, copies_sold, rating
                                  FROM Book
                                  ORDER BY copies_sold
                                  DESC LIMIT 10'''


            cursor.execute(query_fetch_book)
            q_result = cursor.fetchall()

            trending_list = []
            for query_result in q_result:
                t_list = {}
                t_list['title']             = query_result[1]
                t_list['author']            = query_result[2]
                t_list['publisher']         = query_result[3]
                t_list['genre']             = query_result[4]
                t_list['year_of_publish']   = query_result[5]
                t_list['copies_sold']       = query_result[6]
                t_list['rating']            = query_result[7]
                trending_list.append(t_list)


            # t_list = Book.objects.all().order_by('-copies_sold')[:10]

            return render(request, 'trending_list.html', {"t_list": trending_list})









#CUSTOMER FUNCTIONS
#Customer Sign Up function
#Atomic Transaction
def signup(request):
    if request.session.has_key('user_id'):
        return redirect('userProfile')
    elif request.session.has_key('email'):
        return redirect('storeProfile')
    else:
        if request.method == 'POST':
            form = SignupForm(request.POST)


            if form.is_valid():
                user_id         = form.cleaned_data.get('user_id')
                email           = form.cleaned_data.get('email')
                password        = form.cleaned_data.get('password')
                first_name      = form.cleaned_data.get('first_name')
                middle_name     = form.cleaned_data.get('middle_name')
                last_name       = form.cleaned_data.get('last_name')
                phone_no        = form.cleaned_data.get('phone_no')
                address_line1   = form.cleaned_data.get('address_line1')
                address_line2   = form.cleaned_data.get('address_line2')
                city            = form.cleaned_data.get('city')
                district        = form.cleaned_data.get('district')
                state           = form.cleaned_data.get('state')
                zip_code        = form.cleaned_data.get('zip_code')
                no_of_addr      = 1

                # newUser = Customer()
                # newUser.user_id = form.cleaned_data.get('user_id')
                # newUser.email = form.cleaned_data.get('email')
                # newUser.password = form.cleaned_data.get('password')
                # newUser.first_name = form.cleaned_data.get('first_name')
                # newUser.middle_name = form.cleaned_data.get('middle_name')
                # newUser.last_name = form.cleaned_data.get('last_name')
                # newUser.phone_no = form.cleaned_data.get('phone_no')
                # newUser.save()

                #username = form.cleaned_data.get('user_id')
                #raw_password = form.cleaned_data.get('password')
                #user = authenticate(username=username, password=raw_password)
                #login(request, user)
                #messages.info(request, "Welcome to KGP")
                # userCount = Customer.objects.filter(user_id = user_id).count()
                cursor = connection.cursor()
                query_fetch_user = '''SELECT COUNT(*)
                                      FROM Customer
                                      WHERE user_id=%s OR email=%s'''
                cursor.execute(query_fetch_user, [user_id, email])
                q_result = cursor.fetchone()
                userCount = q_result[0]
                print(userCount)

                with transaction.atomic():
                    if userCount == 0:
                        # form.save()
                                                                                    #1. Saving the user
                        query_add_user = '''INSERT INTO Customer(user_id, email, password, first_name, middle_name, last_name, phone_no, no_of_addr)
                                            VALUES (%s, %s, %s, %s, %s, %s, %s, 1)'''
                        cursor.execute(query_add_user, [user_id, email, password, first_name, middle_name, last_name, phone_no])


                                                                                    #2. Saving the user address
                        user_address                = Customer_address()
                        user_address.user_id        = Customer.objects.get(user_id = user_id)
                        user_address.address_no     = no_of_addr
                        user_address.is_current     = True
                        user_address.address_line1  = address_line1
                        user_address.address_line2  = address_line2
                        user_address.city           = city
                        user_address.district       = district 
                        user_address.state          = state
                        user_address.zip_code       = zip_code
                        user_address.save()

                        username = form.cleaned_data.get('first_name')
                        email    = form.cleaned_data.get('email')

                        userinfo = {}
                        userinfo['username'] = username
                        userinfo['email']    = email

                        return render(request, 'users/signUpSuccess.html', context={"user":userinfo})               
                    else:
                        messages.error(request, "user_id or email alrerady taken")
                        return render(request, 'users/signUpFail.html', {})
            else:
                messages.error(request, "Invalid Form Details")
                return render(request, 'users/signUpFail.html', {})    
        else:
            form = SignupForm()

        return render(request, 'users/sign_up.html', {'form': form})




#Customer LogIn Function
def login(request):
    if request.session.has_key('user_id'):
        return redirect('userProfile')
    elif request.session.has_key('email'):
        return redirect('storeProfile')
    else:
        if request.method == "POST":
            form = LoginForm(request.POST)
            if form.is_valid():
                user_id     = form.cleaned_data.get('user_id')
                raw_password= form.cleaned_data.get('password')
                
                # userCount = Customer.objects.filter(user_id = username, password = raw_password)
                cursor = connection.cursor()
                query_user_check = '''SELECT COUNT(*)
                                      FROM Customer
                                      WHERE user_id=%s AND password=%s'''
                cursor.execute(query_user_check, [user_id, raw_password])
                q_result = cursor.fetchone()
                userCount = q_result[0]
                print(userCount)

                
                if userCount == 1:
                    messages.info(request, f"You are now logged in as {user_id}")
                    
                    request.session['user_id'] = request.POST['user_id']
                    return redirect('userProfile')
                else:
                    messages.error(request, "Invalid Username or Password")
                    return render(request, 'users/logInFail.html', {})
            else:
                messages.error(request, "Invalid Form Input")
                return render(request, 'users/logInFail.html', {})
        else:
            form = LoginForm()
            return render(request, "users/login.html", context= {"form":form})




#Customer Profile
def userProfile(request):
    if request.session.has_key('user_id'):
        userid      = request.session['user_id']
        
        # user        = Customer.objects.filter(user_id = userid)
        cursor = connection.cursor()
        query_fetch_user = '''SELECT first_name, email
                              FROM Customer
                              WHERE user_id=%s'''
        cursor.execute(query_fetch_user, [userid])
        user = cursor.fetchone()

        query = {}
        query['username']   = user[0]
        query['email']      = user[1]


        return render(request, 'users/profile.html', {"user":query})
    else:
        return render(request, 'users/logInFail.html', {})




#Function to change the profile details of the users
#Atomic Transaction
def userChangePasswd(request):
    if userSessionCheck(request) == True:
        if request.method == "POST":
            form = userChangePasswdForm(request.POST)

            if form.is_valid():
                old_password = form.cleaned_data.get('old_password')
                new_password = form.cleaned_data.get('new_password')

                userid = request.session['user_id']

                # user = Customer.objects.filter(user_id = user_id)[0]
                cursor1 = connection.cursor()
                query_fetch_user = '''SELECT user_id, first_name, password, email
                                      FROM Customer
                                      WHERE user_id=%s'''
                cursor1.execute(query_fetch_user, [userid])
                user = cursor1.fetchone()

                userinfo = {}
                userinfo['user_id']  = user[0]
                userinfo['email']    = user[3] 

                with transaction.atomic():
                    if user[2] == old_password:
                        # user.password = new_password
                        # user.save()
                        cursor2 = connection.cursor()
                        query_update_pswd = '''UPDATE Customer
                                               SET password=%s
                                               WHERE user_id=%s'''
                        cursor2.execute(query_update_pswd, [new_password, userid])

                        messages.info(request, "Password Changed Succesfully")
                        return redirect('userProfile')
                    else:
                        messages.error(request, "Wrong Old Password")
            else:
                messages.error(request, "Wrong Old Password")
        else:
            form = userChangePasswdForm()
            userid = request.session['user_id']

            cursor1 = connection.cursor()
            query_fetch_user = '''SELECT user_id, first_name, password, email
                                  FROM Customer
                                  WHERE user_id=%s'''
            cursor1.execute(query_fetch_user, [userid])
            user = cursor1.fetchone()

            userinfo = {}
            userinfo['user_id']     = user[0]
            userinfo['email']       = user[3]
            userinfo['first_name']  = user[1]

        return render(request, "users/change_password.html", context= {"form":form, 'user': userinfo})
    else:
        messages.error(request, "Not Logged In")
        return redirect('login')




#Function to Edit User Profile
#Atomic Transaction
def userEditProfile(request):
    if userSessionCheck(request) == True:
        if request.method == "POST":
            form = UserProfileForm(request.POST)
            
            if form.is_valid():
                userid         = form.cleaned_data.get('user_id')



                cursor1 = connection.cursor()
                query_fetch_user = '''SELECT user_id, first_name, password, email
                                      FROM Customer
                                      WHERE user_id=%s'''
                cursor1.execute(query_fetch_user, [userid])
                user = cursor1.fetchone()

                userinfo = {}
                userinfo['user_id']  = user[0]
                userinfo['email']    = user[3] 


                with transaction.atomic():
                    # user            = Customer.objects.filter(user_id = user_id)[0]
                    new_phone_no   = form.cleaned_data.get('phone_no')
                    new_first_name = form.cleaned_data.get('first_name')
                    new_middle_name= form.cleaned_data.get('middle_name')
                    new_last_name  = form.cleaned_data.get('last_name')
                    # user.save()

                    query_update_user = '''UPDATE Customer
                                           SET first_name=%s, middle_name=%s, last_name=%s, phone_no=%s
                                           WHERE user_id=%s'''
                    cursor1.execute(query_update_user, [new_first_name, new_middle_name, new_last_name, new_phone_no, userid])


                messages.info(request, "Profile Edited Sucesfully")
                return redirect('userProfile')
            else:
                messages.error(request, "Invalid Form")
        else:
            userid  = request.session['user_id']
            

            cursor1 = connection.cursor()
            query_fetch_user = '''SELECT user_id, email, first_name, middle_name, last_name, phone_no
                                  FROM Customer
                                  WHERE user_id=%s'''
            cursor1.execute(query_fetch_user, [userid])
            q_result = cursor1.fetchone()

            user = {}
            user['user_id']     = q_result[0]
            user['email']       = q_result[1]
            user['first_name']  = q_result[2]
            user['middle_name'] = q_result[3]
            user['last_name']   = q_result[4]
            user['phone_no']    = q_result[5]



            # user        = Customer.objects.filter(user_id = user_id)[0]
            fields      = {'user_id':user['user_id'], 'email':user['email'], 'first_name':user['first_name'],'phone_no':user['phone_no'], 'middle_name':user['middle_name'], 'last_name':user['last_name']}
            form        = UserProfileForm(initial=fields)

        return render(request, 'users/userProfileEdit.html', {"form":form})
    else:
        messages.error(request, "Not Logged In")
        return redirect('login')





#Function to Add address
#Atomic Transaction
def userAddAddress(request):
    if userSessionCheck(request) == True:
        userid = request.session['user_id']


        # user = Customer.objects.filter(user_id = user_id)[0]
        cursor1 = connection.cursor()
        query_fetch_user = '''SELECT user_id, email, first_name, middle_name, last_name, no_of_addr, phone_no
                              FROM Customer
                              WHERE user_id=%s'''
        cursor1.execute(query_fetch_user, [userid])
        user = cursor1.fetchone()

        userinfo = {}
        userinfo['user_id']     = user[0]
        userinfo['email']       = user[1]
        userinfo['first_name']  = user[2]
        userinfo['middle_name'] = user[3]
        userinfo['last_name']   = user[4]
        userinfo['no_addr']     = user[5]
        userinfo['phone_no']    = user[6]

        

        if request.method == "POST":
            form = addNewAddress(request.POST)

            if form.is_valid():
                with transaction.atomic():
                    address                 = Customer_address()
                    address.user_id         = Customer.objects.get(user_id = userid)
                    address.address_line1   = form.cleaned_data.get('address_line1')
                    address.address_line2   = form.cleaned_data.get('address_line2')
                    address.city            = form.cleaned_data.get('city')
                    address.state           = form.cleaned_data.get('state')
                    address.district        = form.cleaned_data.get('district')
                    address.zip_code        = form.cleaned_data.get('zip_code')
                    address.address_no      = form.cleaned_data.get('addr_no')
                    address.is_current      = form.cleaned_data.get('is_current')
                    

                    if address.is_current == True:
                        addresses = Customer_address.objects.filter(user_id = userid)
                        
                        for addr in addresses:
                            addr.is_current = False
                            addr.save()
                    else:
                        address.is_current = False


                    address.save()

                    userupdate = Customer.objects.get(user_id = userid)
                    userupdate.no_of_addr += 1
                    userupdate.save()
                    # no_of_addr = userinfo['no_addr'] + 1
                    # query_update_user = '''UPDATE Customer
                    #                        SET no_of_addr = %d
                    #                        WHERE user_id=%s'''
                    # cursor1.execute(query_update_user, [no_of_addr, userid])


                
                messages.info(request, "Address Added Sucesfully")
                return redirect('userProfile')
            else:
                messages.error(request, "Invalid Form")
        else:
            form = addNewAddress(initial={"addr_no":user[5]+1})

        return render(request, 'users/add_address.html', {"form":form, "user":userinfo})
    else:
        messages.error(request, "Not Logged In")
        return redirect('login')




#Function to set on address as primary address
#Atomic Transaction
def setPrimaryAddress(request, addr_no):
    if userSessionCheck(request) == True:
        userid = request.session['user_id']
        # user = Customer.objects.filter(user_id = user_id)[0]
        cursor1 = connection.cursor()
        query_fetch_user = '''SELECT user_id, email, first_name, middle_name, last_name, no_of_addr, phone_no
                              FROM Customer
                              WHERE user_id=%s'''
        cursor1.execute(query_fetch_user, [userid])
        user = cursor1.fetchone()

        userinfo = {}
        userinfo['user_id']     = user[0]
        userinfo['email']       = user[1]
        userinfo['first_name']  = user[2]
        userinfo['middle_name'] = user[3]
        userinfo['last_name']   = user[4]
        userinfo['no_addr']     = user[5]
        userinfo['phone_no']    = user[6]


        if request.method == "POST":
            with transaction.atomic():
                address = Customer_address.objects.filter(user_id = userid)
                
                for addr in address:
                    addr.is_current = False
                    addr.save()


                addressupdate = Customer_address.objects.get(user_id = userid, address_no = addr_no)
                addressupdate.is_current = True
                addressupdate.save()

                messages.success(request, "Primary Address changed Successfully")
            return redirect('userAddAddress')
        else:
            address_list = Customer_address.objects.filter(user_id = userid)

        return render(request, 'users/change_primary_addr.html', {"address_list":address_list, "user":userinfo})
    else:
        messages.error(request, "Not Logged In")
        return redirect('login')




#Function to logout the user
def userLogout(request):
    try:
        del request.session['user_id']
    except :
        pass
    return redirect( 'index')














#Request contains serach parameter and user_id and returns the list of books
def searchBooks(request):
    if userSessionCheck(request) == True:
        userid = request.session['user_id']

        user_row    = fetchUserRow(userid)                                          #1. Store details from the session
        username    = user_row[3]                                                   #Store ID 
        email       = user_row[1]


        search_term = ''

        if request.method == "GET":
            if 'search' in request.GET:
                search_term = request.GET['search']
                filter = request.GET['filter']

                #1. Checking the main book table with search input
                if(filter == 'title'):
                    books_avl = Book.objects.filter( title__contains = search_term ).order_by('title')
                if(filter == 'genre'):
                    books_avl = Book.objects.filter( genre__contains = search_term ).order_by('title')
                if(filter == 'publisher'):
                    books_avl = Book.objects.filter( publisher__contains = search_term ).order_by('title')
                if(filter == 'author'):
                    books_avl = Book.objects.filter( author__contains = search_term ).order_by('title')

                books = books_avl

                # #2. Checking the Store Availability and collecting all options
                # books = []
                # for book in books_avl:
                #     book_in_store = Book_available.objetcs.filter(book_id = book.book_id)

                #     for options in book_in_store:
                #         book_option = {}
                #         book_option['book_id']          = book.book_id 
                #         book_option['title']            = book.title 
                #         book_option['author']           = book.author 
                #         book_option['publisher']        = book.publisher 
                #         book_option['genre']            = book.genre
                #         book_option['year_of_publish']  = book.year_of_publish 
                #         book_option['copies_sold']      = book.copies_sold 
                #         book_option['rating']           = book.rating

                #         book_option['stock_id']         = options.book_available_id
                #         book_option['store_id']         = options.store_email.store_id
                #         book_option['email']            = options.store_email.email
                #         book_option['price']            = options.price
                #         book_option['copies left']      = options.no_of_copies

                #         books.append(book_option)

            # books = Book.objects.all()
            print(books)
            return render(request, 'users/searchResult.html', {'username': username, 'useremail': email, 'books' : books, 'search_term': search_term, 'filter': filter })
        else:
            return redirect('userProfile')
    else:
        messages.error(request, "Not Logged In")
        return redirect('login')




#Function to view details of the book
def searchViewBook(request, book_id):
    if userSessionCheck(request) == True:
        userid = request.session['user_id']

        user_row    = fetchUserRow(userid)                                          #1. Store details from the session
        username    = user_row[3]                                                    #Store ID 
        email       = user_row[1]

        if request.method == "POST":
            return redirect('userProfile')
        else:
            options = Book_available.objects.filter(book_id = book_id)


            # book = Book.objects.get(book_id = book_id)
            cursor = connection.cursor()
            query = '''SELECT book_id, title, author, publisher, genre, year_of_publish, copies_sold, rating
                       FROM Book
                       WHERE book_id=%s'''
            cursor.execute(query, [book_id])
            q_result = cursor.fetchone()

            book = {}
            book['book_id']         = q_result[0]
            book['title']           = q_result[1]
            book['author']          = q_result[2]
            book['publisher']       = q_result[3]
            book['genre']           = q_result[4]
            book['year_of_publish'] = q_result[5]
            book['copies_sold']     = q_result[6]
            book['rating']          = q_result[7]

            return render(request, 'users/searchViewBook.html', {'username': username, 'useremail': email, 'book': book, 'sellers': options})
    else:
        messages.error(request, "Not Logged In")
        return redirect('login')







#Returns books added by the particular user
def userCart(request):
    if userSessionCheck(request) == True:
        if request.method == "GET":

            userid = request.session['user_id']
            
            user_row    = fetchUserRow(userid)                                          #1. Store details from the session
            username    = user_row[3]                                                   #Store ID 
            useremail   = user_row[1]


            cart_books = Cart.objects.filter(user_id = userid)
            
            total_price   = 0

            books_in_cart = []
            for book in cart_books:
                cart_instance = {}

                total_price = total_price + book.no_of_copies*book.price

                # cart_instance['book']       = Book.objects.get(book_id = book.book_id.book_id)
                cursor = connection.cursor()
                query = '''SELECT book_id, title, author, publisher, genre, year_of_publish, copies_sold, rating
                           FROM Book
                           WHERE book_id=%s'''
                cursor.execute(query, [book.book_id.book_id])
                q_result = cursor.fetchone()

                cart_instance['book_id']        = q_result[0]
                cart_instance['title']          = q_result[1]
                cart_instance['author']         = q_result[2]
                cart_instance['publisher']      = q_result[3]
                cart_instance['genre']          = q_result[4]
                cart_instance['year_of_publish']= q_result[5]
                cart_instance['copies_sold']    = q_result[6]
                cart_instance['rating']         = q_result[7]
                cart_instance['num_of_copies']  = book.no_of_copies
                cart_instance['price']          = book.price
                cart_instance['date_of_entry']  = book.date_of_entry
                cart_instance['cart_id']        = book.cart_id
                books_in_cart.append(cart_instance)

            return render(request, 'users/userCart.html', {'username': username, 'useremail': useremail, 'books' : books_in_cart, 'total_price' : total_price})
        else:
            return redirect('userProfile')
    else:
        messages.error(request, "Not Logged In")
        return redirect('login')




#Returns books added by the particular user
#Atomic Transaction
def addToCart(request, stock_id):
    if userSessionCheck(request) == True:
        userid = request.session['user_id']

        user_row    = fetchUserRow(userid)                                          #1. Store details from the session
        username    = user_row[3]                                                   #Store ID 
        email       = user_row[1]

        if request.method == "GET":
            return redirect('userCart')
        else:
            with transaction.atomic():
                #1. Get the stock
                stock = Book_available.objects.get(book_available_id = stock_id)

                #2. Get the Book
                book = Book.objects.get(book_id = stock.book_id.book_id)

                #2. Get the Store
                store = Book_store.objects.get(email = stock.store_email.email)

                #3. Get the Customer
                user = Customer.objects.get(user_id = userid)

                copies = int(request.POST['no_of_copies'], 10)
                print(type(copies))

                #4. Add to the cart
                addBook = Cart()
                addBook.book_id     = book
                addBook.store_id    = store
                addBook.user_id     = user

                addBook.no_of_copies = copies
                addBook.price        = stock.price
                addBook.save()

            messages.success(request, 'Added to cart')
            return redirect('userCart')

    else:
        messages.error(request, "Not Logged In")
        return redirect('login')




#Updates cart entries added by the particular user
#Atomic Transaction
def updateCart(request, cart_id):
    if userSessionCheck(request) == True:
        userid = request.session['user_id']

        user_row    = fetchUserRow(userid)                                          #1. Store details from the session
        username    = user_row[3]                                                   #Store ID 
        email       = user_row[1]

        if request.method == "POST":
            with transaction.atomic():
                #1. Get the cart
                cart_entry = Cart.objects.get(cart_id = cart_id)


                #2. Get the Data
                copies = int(request.POST['copies'], 10)

                if copies == 0:
                    cart_entry.delete()
                else:
                    #3. Update
                    cart_entry.no_of_copies  = copies
                    cart_entry.save()

            messages.success(request, 'Cart Updated')
            return redirect('userCart')
        else:
            return redirect('userCart')
    else:
        messages.error(request, "Not Logged In")
        return redirect('login')




#Function to delete from cart
#Atomic Transaction
def deleteCart(request, cart_id):
    if userSessionCheck(request) == True:
        userid = request.session['user_id']

        user_row    = fetchUserRow(userid)                                          #1. Store details from the session
        username    = user_row[3]                                                   #Store ID 
        email       = user_row[1]

        if request.method == "POST":
            with transaction.atomic():
                #1. Get the cart
                cart_entry = Cart.objects.get(cart_id = cart_id)

                #2. Delete
                cart_entry.delete()

            messages.success(request, 'Deleted Successfully')
            return redirect('userCart')
        else:
            return redirect('userCart')
    else:
        messages.error(request, "Not Logged In")
        return redirect('login')




#Function to view Cart Details
def cartView(request, cart_id):
    if userSessionCheck(request) == True:
        userid = request.session['user_id']

        user_row    = fetchUserRow(userid)                                          #1. Store details from the session
        username    = user_row[3]                                                    #Store ID 
        email       = user_row[1]

        if request.method == "POST":
            return redirect('userProfile')
        else:
            cart_entry = Cart.objects.get(cart_id = cart_id)
            options = Book_available.objects.filter(book_id = cart_entry.book_id.book_id, store_email = cart_entry.store_id.email)


            # book = Book.objects.get(book_id = book_id)
            cursor = connection.cursor()
            query = '''SELECT book_id, title, author, publisher, genre, year_of_publish, copies_sold, rating
                       FROM Book
                       WHERE book_id=%s'''
            cursor.execute(query, [cart_entry.book_id.book_id])
            q_result = cursor.fetchone()

            book = {}
            book['book_id']         = q_result[0]
            book['title']           = q_result[1]
            book['author']          = q_result[2]
            book['publisher']       = q_result[3]
            book['genre']           = q_result[4]
            book['year_of_publish'] = q_result[5]
            book['copies_sold']     = q_result[6]
            book['rating']          = q_result[7]

            return render(request, 'users/cartView.html', {'username': username, 'useremail': email, 'book': book, 'sellers': options})
    else:
        messages.error(request, "Not Logged In")
        return redirect('login')








#Functions to Order from the User
def confirmAddress(request):
    if userSessionCheck(request) == True:
        userid = request.session['user_id']
        
        user_row    = fetchUserRow(userid)                                          #1. Store details from the session
        username    = user_row[3]                                                   #Store ID 
        useremail   = user_row[1]

        user_id = request.session['user_id']

        addresses= Customer_address.objects.filter(user_id = user_id)
        primary_address = ''
        other_address = []

        for address in addresses:
            if(address.is_current):
                primary_address = address
            else:
                other_address.append(address)

        return render(request, 'users/confirmAddress.html',  {'username': username, 'useremail': useremail, 'primary_address': primary_address,'other_address': other_address})
    else:
        messages.error(request, "Not Logged In")
        return redirect('login')




#Function to add as primary address during the checkout
#Atomic Transaction
def userAddAsPrimaryAddress(request, address_id):
    if userSessionCheck(request) == True:
        userid = request.session['user_id']
        
        user_row    = fetchUserRow(userid)                                          #1. Store details from the session
        username    = user_row[3]                                                   #Store ID 
        useremail   = user_row[1]

        print(address_id)
        with transaction.atomic():
            all_address = Customer_address.objects.filter(user_id = userid)

            for address in all_address:
                address.is_current = False
                address.save()

            p_address = Customer_address.objects.get(address_id = address_id)
            p_address.is_current = True


            p_address.save()

        messages.success(request, 'Address Set As Primary')
        return redirect('confirmAddress')
    else:
        messages.error(request, "Not Logged In")
        return redirect('login')




#Funciton to place order
#Atomic Transaction
def userPlaceOrder(request, address_no):
    if userSessionCheck(request) == True:
        userid = request.session['user_id']
        
        user_row    = fetchUserRow(userid)                                          #1. Store details from the session
        username    = user_row[3]                                                   #Store ID 
        useremail   = user_row[1]        

        #1. Fetch all orders
        all_orders = Cart.objects.filter(user_id = userid)
        user_obj   = Customer.objects.get(user_id = userid)

        store_list = []
        price_list = []
        book_store_ind = []
        count = 0

        with transaction.atomic():
            #2. Get all the distinct stores 
            for books in all_orders:
                if books.store_id in store_list:
                    price_list[store_list.index(books.store_id)] += books.price*(books.no_of_copies)
                    
                else:
                    store_list.append(books.store_id)
                    price_list.append(books.price*(books.no_of_copies))

                    user_lst_cnt = Users_list.objects.filter(user_id = userid , store_email = books.store_id.email).count()

                    if user_lst_cnt == 0:    
                        user_list_entry = Users_list()
                        user_list_entry.user_id       = user_obj
                        user_list_entry.store_email   = books.store_id
                        user_list_entry.save()
                
                book_store_ind.append(store_list.index(books.store_id))
                count += 1
            
            #3. Create Order List
            order_id= [] 
            for i in range(0,len(store_list)):
                newOrder  = Order()
                print("The order Id is\n\n", newOrder.order_id)
                

                newOrder.user_id        = Customer.objects.get(user_id = userid)
                newOrder.store_id       = store_list[i]
                newOrder.total_price    = price_list[i]
                newOrder.address_no     = address_no
                newOrder.status         = 'Processing'
                newOrder.save()

                print("This ID: ", newOrder.order_id)

                order_id.append(newOrder.order_id)

            #4. Updating the table Book Ordered
            count =0
            for book in all_orders:
                newBook                 = Book_ordered()
                print("New Book Book_ordered_id:", newBook.Book_ordered_id)

                book_avail = Book_available.objects.get(book_id = book.book_id.book_id, store_email = book.store_id.email)
                book_avail.no_of_copies = book_avail.no_of_copies - book.no_of_copies

                newBook.book_id         = book.book_id
                newBook.store_id        = book.store_id
                newBook.order_id        = Order.objects.get(order_id = order_id[book_store_ind[count]])
                newBook.no_of_copies    = book.no_of_copies
                newBook.save()
                book_avail.save()



                print("New Book Book_ordered_id:", newBook.Book_ordered_id)
                count +=1
            
            #5. Clean the cart
            Cart.objects.filter(user_id = userid ).delete()



        messages.success(request, 'Order Placed Successfully')
        return redirect('userProfile')
    else:
        messages.error(request, "Not Logged In")
        return redirect('login')








#Shows the Options to see the three different types of order list
def userOrderList(request):
    if userSessionCheck(request) == True:
        userid = request.session['user_id']
        
        cursor = connection.cursor()
        query = '''SELECT user_id, first_name, email
                   FROM Customer
                   WHERE user_id=%s'''

        cursor.execute(query, [userid])
        q_result_store = cursor.fetchone()
        
        user = {}
        user['email']       = q_result_store[2]
        user['first_name']  = q_result_store[1]


        return render(request, 'users/userOrders.html', {'user' : user})
    else:
        messages.error(request, "Not Logged In")
        return redirect('login')




#User function to display the delivered order list
def userDeliveredOrder(request):
    if userSessionCheck(request) == True:
        userid = request.session['user_id']
        
        cursor = connection.cursor()
        query = '''SELECT user_id, first_name, email
                   FROM Customer
                   WHERE user_id=%s'''

        cursor.execute(query, [userid])
        q_result_store = cursor.fetchone()
        
        user = {}
        username      = q_result_store[2]
        useremail     = q_result_store[1]
        

        status      = "Delivered"                                                        #2. Status to be searched

        # cursor = connection.cursor()
        # query = '''SELECT *
        #            FROM Order 
        #            WHERE store_id.pk=%d AND status=%s'''
        # cursor.execute(query, [store_id, status])
        # q_result = cursor.fetchall()

        
        q_result = Order.objects.filter(user_id = userid, status = status).order_by('-date_of_order')   #3. Selecting all the rows from the Order table with the given store_id and status
        
        return render(request, 'users/deliveredOrders.html', {'username': username, 'useremail' : useremail,  'q_result' : q_result})
    else:
        messages.error(request, "Not Logged In")
        return redirect('login')




#User function to display the processing order list
def userInProcessOrder(request):
    if userSessionCheck(request) == True:
        userid = request.session['user_id']
        
        cursor = connection.cursor()
        query = '''SELECT user_id, first_name, email
                   FROM Customer
                   WHERE user_id=%s'''

        cursor.execute(query, [userid])
        q_result_store = cursor.fetchone()
        
        user = {}
        username      = q_result_store[2]
        useremail     = q_result_store[1]
        

        status      = "Processing"                                                        #2. Status to be searched

        # cursor = connection.cursor()
        # query = '''SELECT *
        #            FROM Order 
        #            WHERE store_id.pk=%d AND status=%s'''
        # cursor.execute(query, [store_id, status])
        # q_result = cursor.fetchall()

        
        q_result = Order.objects.filter(user_id = userid, status = status).order_by('-date_of_order')   #3. Selecting all the rows from the Order table with the given store_id and status
        
        return render(request, 'users/processingOrder.html', {'username': username, 'useremail' : useremail,  'q_result' : q_result})
    else:
        messages.error(request, "Not Logged In")
        return redirect('login')




#User function to display the Cancelled order list
def userCancelledOrder(request):
    if userSessionCheck(request) == True:
        userid = request.session['user_id']
        
        cursor = connection.cursor()
        query = '''SELECT user_id, first_name, email
                   FROM Customer
                   WHERE user_id=%s'''

        cursor.execute(query, [userid])
        q_result_store = cursor.fetchone()
        
        user = {}
        username      = q_result_store[2]
        useremail     = q_result_store[1]
        

        status      = "Cancelled"                                                        #2. Status to be searched

        # cursor = connection.cursor()
        # query = '''SELECT *
        #            FROM Order 
        #            WHERE store_id.pk=%d AND status=%s'''
        # cursor.execute(query, [store_id, status])
        # q_result = cursor.fetchall()

        
        q_result = Order.objects.filter(user_id = userid, status = status).order_by('-date_of_order')   #3. Selecting all the rows from the Order table with the given store_id and status
        
        return render(request, 'users/cancelledOrder.html', {'username': username, 'useremail' : useremail,  'q_result' : q_result})
    else:
        messages.error(request, "Not Logged In")
        return redirect('login')




#User Function to display the details of all the orders
def userOrderDetails(request, order_id):
    if userSessionCheck(request) == True:
        userid = request.session['user_id']
        
        cursor = connection.cursor()                                                                #1. Fetching the User
        query = '''SELECT user_id, first_name, email
                   FROM Customer
                   WHERE user_id=%s'''

        cursor.execute(query, [userid])
        q_result_store = cursor.fetchone()
        
        user = {}
        username      = q_result_store[2]
        useremail     = q_result_store[1]
        



        q_result_order = Order.objects.get(order_id = order_id)                                     #2. Fetching the given order by order_id


        cursor = connection.cursor()                                                                #3. Fetching all the books in the order with id order_id
        # query1 = '''SELECT *
        #             FROM Book_ordered
        #             WHERE order_id =%s'''
        # cursor.execute(query1, [order_id])
        # q_result_bk_ids = cursor.fetchall()
        q_result_bk_ids = Book_ordered.objects.filter(order_id = order_id)                      

        
        address = Customer_address.objects.get(user_id = q_result_order.user_id, address_no = q_result_order.address_no)    #4. Fetching the address where to be sent

        q_result_final = []                                                                                         #List of book and their details                         
        q_result = []                                                                                               #List of books

        for bk_id in q_result_bk_ids:                                                                               #5. Creating a list of books to be sent for html rendering
            instance = {} 

            #books_fetch = Book.objects.get(book_id = bk_id.book_id.pk)                                             #Book entry fetched from the table
            query_fetch_book = '''SELECT *
                                  FROM Book
                                  WHERE book_id=%s'''                                                               #Book id with its details
            cursor.execute(query_fetch_book, [bk_id.book_id.pk])
            books_fetch = cursor.fetchone()

            
            book_avail_price = Book_available.objects.get(book_id = bk_id.book_id.pk, store_email = q_result_order.store_id.email)        #Price entry from the Book_available table            
            # query_fetch_price = '''SELECT *
            #                        FROM Book_available
            #                        WHERE book_id=%s AND store_email=%s'''
            # cursor.execute(query_fetch_price, [bk_id.book_id.pk, email])
            # book_avail_price = cursor.fetchone()


            # instance['id'] = books_fetch.book_id
            # instance['title'] = books_fetch.title
            # instance['author'] = books_fetch.author
            instance['id']      = books_fetch[0]
            instance['title']   = books_fetch[1]
            instance['author']  = books_fetch[2]
            instance['price']   = book_avail_price.price
            instance['copies']  = bk_id.no_of_copies


            q_result_final.append(instance)
            q_result.append(books_fetch)

        if q_result_order.status == "Delivered":
            return  render(request, 'users/deliveredOrderDetails.html', {'username': username, 'useremail' : useremail, 'q_result_order' : q_result_order, 'books' : q_result, 'copies' : q_result_final , 'address' : address})
        elif q_result_order.status == "Processing":
            form1 = DateInputForm()
            form2 = TextInputForm()
            return  render(request, 'users/processingOrderDetails.html', {'dateform1' : form1, 'dateform2' : form1, 'textform' : form2, 'username': username, 'useremail' : useremail, 'q_result_order' : q_result_order, 'books' : q_result, 'copies' : q_result_final , 'address' : address})            
        elif q_result_order.status == "Cancelled":
            return  render(request, 'users/cancelledOrderDetails.html', {'username': username, 'useremail' : useremail, 'q_result_order' : q_result_order, 'books' : q_result, 'copies' : q_result_final , 'address' : address})            
    else:
        messages.error(request, "Not Logged In")
        return redirect('login')




#USer function to Cancel Order
def userCancelOrder(request, order_id):
    if userSessionCheck(request) == True:
        userid = request.session['user_id']
        
        cursor = connection.cursor()
        query = '''SELECT user_id, first_name, email
                   FROM Customer
                   WHERE user_id=%s'''

        cursor.execute(query, [userid])
        q_result_store = cursor.fetchone()
        
        user = {}
        username      = q_result_store[2]
        useremail     = q_result_store[1]

        form = TextInputForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                remarks = form.cleaned_data.get('text')

                q_result_order = Order.objects.get(order_id = order_id)                #2. Fetching the given order by order_id

                q_result_order.delivered_date       = None
                q_result_order.status               = "Cancelled"
                q_result_order.cancelled_date       = date.today()
                q_result_order.cancelled_by         = "User"
                q_result_order.cancellation_remarks = remarks 


                order_books = Book_ordered.objects.filter(order_id = order_id)

                for books in order_books:
                    copies = books.no_of_copies

                    aval_book = Book_available.objects.get(book_id = books.book_id.book_id, store_email = q_result_order.store_id.email)
                    aval_book.no_of_copies = aval_book.no_of_copies + copies 
                    aval_book.save()

                q_result_order.save()

            return redirect('userInProcessOrder')
        else:
            messages.error(request, "Invalid  Data Entered")
    else:
        messages.error(request, "Not Logged In")
        return redirect('login')



#User function to Complain on an order
#Atomic Transaction
def userComplaint(request, order_id):
    if userSessionCheck(request) == True:
        userid = request.session['user_id']
        
        cursor = connection.cursor()                                                                #1. Fetching the User
        query = '''SELECT user_id, first_name, email
                   FROM Customer
                   WHERE user_id=%s'''

        cursor.execute(query, [userid])
        q_result_store = cursor.fetchone()
        
        user = {}
        username      = q_result_store[2]
        useremail     = q_result_store[1]
        



        q_result_order = Order.objects.get(order_id = order_id)                                     #2. Fetching the given order by order_id


        cursor = connection.cursor()                                                                #3. Fetching all the books in the order with id order_id
        # query1 = '''SELECT *
        #             FROM Book_ordered
        #             WHERE order_id =%s'''
        # cursor.execute(query1, [order_id])
        # q_result_bk_ids = cursor.fetchall()
        q_result_bk_ids = Book_ordered.objects.filter(order_id = order_id)                      

        
        address = Customer_address.objects.get(user_id = q_result_order.user_id, address_no = q_result_order.address_no)    #4. Fetching the address where to be sent

        q_result_final = []                                                                                         #List of book and their details                         
        q_result = []                                                                                               #List of books

        for bk_id in q_result_bk_ids:                                                                               #5. Creating a list of books to be sent for html rendering
            instance = {} 

            #books_fetch = Book.objects.get(book_id = bk_id.book_id.pk)                                             #Book entry fetched from the table
            query_fetch_book = '''SELECT *
                                  FROM Book
                                  WHERE book_id=%s'''                                                               #Book id with its details
            cursor.execute(query_fetch_book, [bk_id.book_id.pk])
            books_fetch = cursor.fetchone()

            
            book_avail_price = Book_available.objects.get(book_id = bk_id.book_id.pk, store_email = q_result_order.store_id.email)        #Price entry from the Book_available table            
            # query_fetch_price = '''SELECT *
            #                        FROM Book_available
            #                        WHERE book_id=%s AND store_email=%s'''
            # cursor.execute(query_fetch_price, [bk_id.book_id.pk, email])
            # book_avail_price = cursor.fetchone()


            # instance['id'] = books_fetch.book_id
            # instance['title'] = books_fetch.title
            # instance['author'] = books_fetch.author
            instance['id']      = books_fetch[0]
            instance['title']   = books_fetch[1]
            instance['author']  = books_fetch[2]
            instance['price']   = book_avail_price.price
            instance['copies']  = bk_id.no_of_copies


            q_result_final.append(instance)
            q_result.append(books_fetch)

        if request.method == "GET":
            return render(request, 'users/userComplaint.html', {'username': username, 'useremail' : useremail, 'q_result_order' : q_result_order, 'books' : q_result, 'copies' : q_result_final , 'address' : address})
        else:
            with transaction.atomic():
                text = request.POST['complaint']

                complain = Complaint_record()
                complain.order_id = Order.objects.get(order_id = order_id)

                complaints = Complaint_record.objects.filter(order_id = order_id).count()
                comp_no = complaints + 1

                complain.complain_no = comp_no
                complain.description = text
                complain.save()

            messages.success(request, 'Complain submitted')
            return redirect('userOrderList') 
    else:
        messages.error(request, "Not Logged In")
        return redirect('login')







#Function to add to user to read list
def addToReadList(request, book_id):
    if userSessionCheck(request) == True:
        userid = request.session['user_id']

        user_row    = fetchUserRow(userid)                                          #1. Store details from the session
        username    = user_row[3]                                                   #Store ID 
        email       = user_row[1]

        if request.method == "GET":
            return redirect('userProfile')
        else:
            with transaction.atomic():
                #1. Get the Book
                book = Book.objects.get(book_id = book_id)

                #2. Get the User
                user = Customer.objects.get(user_id = userid)


                #3. Save the instance
                bookToRead = To_read_list()
                bookToRead.book_id = book
                bookToRead.user_id = user
                bookToRead.save()

            messages.success(request, 'Added to To Read List')
            return redirect('searchViewBook', book_id = book_id)
    else:
        messages.error(request, "Not Logged In")
        return redirect('login')




#Funnction to get user reviews
#Atomic Transactions
def userReview(request, book_id):
    if userSessionCheck(request) == True:
        userid = request.session['user_id']

        user_row    = fetchUserRow(userid)                                          #1. Store details from the session
        username    = user_row[3]                                                   #Store ID 
        email       = user_row[1]

        if request.method == "GET":

            # book = Book.objects.get(book_id = book_id)
            cursor  = connection.cursor()
            query   = '''SELECT book_id, title, author, publisher, genre, year_of_publish, copies_sold, rating
                         FROM Book
                         WHERE book_id=%s'''
            cursor.execute(query, [book_id])
            q_result = cursor.fetchone()



            book = {}
            book['book_id']         = q_result[0]
            book['title']           = q_result[1]
            book['author']          = q_result[2]
            book['publisher']       = q_result[3]
            book['genre']           = q_result[4]
            book['year_of_publish'] = q_result[5]
            book['copies_sold']     = q_result[6]
            book['rating']          = q_result[7]


            return render(request, 'users/reviewBook.html', {'username': username, 'useremail': email, 'book':book})
        else:
            with transaction.atomic():
                #1. Get the Book
                book = Book.objects.get(book_id = book_id)

                #2. Get the User
                user = Customer.objects.get(user_id = userid)

                #3. Get the details
                description   = request.POST['review']
                rating        = float(request.POST['rating'])

                #4. Update rating
                reviews = Review.objects.filter(book_id = book_id)
                final_rating = 0.0
                rate_sum = 0.0
                count = 0
                for review in reviews:
                    count = count + 1
                    rate_sum = rate_sum + review.rating

                final_rating = (rate_sum + rating)


                review_flag = Review.objects.filter(user_id = userid, book_id = book_id).count()

                
                if review_flag == 0:

                    #4. Save the instance
                    userReview = Review()
                    userReview.book_id      = book
                    userReview.user_id      = user
                    userReview.description  = description
                    userReview.rating       = rating
                    book.rating             = final_rating/(count + 1)
                    book.save()
                    userReview.save() 
                else:
                    review_instance             = Review.objects.get(user_id = userid, book_id = book_id)
                    review_instance.description = description
                    book.rating                 = (final_rating - review_instance.rating)/(count)
                    review_instance.rating      = rating
                    book.save()
                    review_instance.save()



            messages.success(request, 'Review Submitted')
            return redirect('searchViewBook', book_id = book_id)
    else:
        messages.error(request, "Not Logged In")
        return redirect('login')




#Request contains user_id and accordingly we will return the to read List 
def userBookList(request):
    if userSessionCheck(request) == True:

        userid = request.session['user_id']

        user_row    = fetchUserRow(userid)                                          #1. Store details from the session
        username    = user_row[3]                                                   #Store ID 
        email       = user_row[1]
        
        if request.method == 'POST':
            return redirect('userProfile')
        else:
            BookObjectList = To_read_list.objects.filter(user_id= userid)
            book_list= []

            cursor = connection.cursor()
            for book in BookObjectList:

                #book_object = Book.objects.filter(book_id = book.book_id.book_id)
                query = '''SELECT book_id, title, author, publisher, genre
                           FROM Book
                           WHERE book_id=%s'''
                cursor.execute(query, [book.book_id.book_id])
                book_object = cursor.fetchone()


                # for book_fin in book_object:
                #     book_list.append({'title':book_fin.title, 'author': book_fin.author, 'book_id':book_fin.book_id})\
                book_list.append({'book_id': book_object[0], 'title':book_object[1], 'author': book_object[2], 'publisher': book_object[3],'genre': book_object[4]})

                
            return render(request, 'users/book_list.html', {'username': username, 'useremail': email, 'book_list':book_list})
    else:
        messages.error(request, "Not Logged In")
        return redirect('login')




#To remove Book from user's read list
#Atomic Transaction
def userRemoveBook(request, book_id):
    if userSessionCheck(request) == True:
        userid = request.session['user_id']

        user_row    = fetchUserRow(userid)                                          #1. Store details from the session
        username    = user_row[3]                                                  #Store ID 
        email       = user_row[1]


        if request.method == 'POST':
            return redirect('userBookList')
        else:

            with transaction.atomic():
                To_read_list.objects.filter(book_id = book_id, user_id = userid).delete()

            messages.success(request, "Book Successfully Deleted")
            return redirect('userBookList')

    else:
        messages.error(request, "Not Logged In")
        return redirect('login')



#Function to view details of the book
def viewBook(request, book_id):
    if userSessionCheck(request) == True:
        userid = request.session['user_id']

        user_row    = fetchUserRow(userid)                                          #1. Store details from the session
        username    = user_row[3]                                                  #Store ID 
        email       = user_row[1]

        if request.method == 'POST':
            return redirect('userBookList')
        else:
            sellers = Book_available.objects.filter(book_id = book_id)


            # book = Book.objects.get(book_id = book_id)
            cursor = connection.cursor()
            query = '''SELECT book_id, title, author, publisher, genre, year_of_publish, copies_sold, rating
                       FROM Book
                       WHERE book_id=%s'''
            cursor.execute(query, [book_id])
            q_result = cursor.fetchone()

            book = {}
            book['book_id']         = q_result[0]
            book['title']           = q_result[1]
            book['author']          = q_result[2]
            book['publisher']       = q_result[3]
            book['genre']           = q_result[4]
            book['year_of_publish'] = q_result[5]
            book['copies_sold']     = q_result[6]
            book['rating']          = q_result[7]

            return render(request, 'users/viewBook.html', {'username': username, 'useremail': email, 'book': book, 'sellers': sellers})
    else:
        messages.error(request, "Not Logged In")
        return redirect('login')





#Returns all the order made by the user
def userOrders(request):
    return HttpResponse("Orders by the user")




#Function to store the user complaints
def userOrderComplain(request):
    return HttpResponse("Return Complain correspoding to this user and a given order")












#Function to display all the store details
def sellerList(request):
    if userSessionCheck(request) == True:
        userid      = request.session['user_id']
        user_row    = fetchUserRow(userid)                                          #1. Store details from the session
        username    = user_row[3]                                                   #Store ID 
        email       = user_row[1]


        # storeList = Book_store.objects.all()
        cursor = connection.cursor()
        query_fetch_stores = '''SELECT store_id, store_name, email, website, phone_no, rating, address_line1, address_line2, city, district, state, zip_code
                                FROM Book_store
                                ORDER BY store_name'''
        cursor.execute(query_fetch_stores)
        q_result = cursor.fetchall()

        storeList = []
        for store in q_result:
            storeinfo = {}
            storeinfo['store_id']   = store[0]
            storeinfo['store_name'] = store[1]
            storeinfo['email']      = store[2]
            storeinfo['website']    = store[3]
            storeinfo['href']       = "//" + store[3]
            storeinfo['phone_no']   = store[4]
            storeinfo['rating']     = store[5]
            storeList.append(storeinfo)


        return render(request, 'users/seller_list.html', {"username": username, "email": email, "storeList": storeList})
    else:
        messages.error(request, "Not Logged In")
        return redirect('login')




#Fuction to display store address
def sellerListStoreAddress(request, email):
    if userSessionCheck(request) == True:
        userid      = request.session['user_id']
        user_row    = fetchUserRow(userid)                                          #1. Store details from the session
        username    = user_row[3]                                                  #Store ID 
        useremail   = user_row[1]


        cursor = connection.cursor()
        query_fetch_store = '''SELECT store_id, store_name, email, website, phone_no, rating, address_line1, address_line2, city, district, state, zip_code
                               FROM Book_store
                               WHERE email=%s'''

        cursor.execute(query_fetch_store, [email])
        q_result = cursor.fetchone()

        store = {}
        store['store_id']       = q_result[0]
        store['store_name']     = q_result[1]
        store['email']          = q_result[2]
        store['website']        = q_result[3]
        store['phone_no']       = q_result[4]
        store['rating']         = q_result[5]
        store['address_line1']  = q_result[6]
        store['address_line2']  = q_result[7]
        store['city']           = q_result[8]
        store['district']       = q_result[9]
        store['state']          = q_result[10]
        store['zip_code']       = q_result[11]





        # store = Book_store.objects.filter(email = email)[0]
        return render(request, 'users/store_address.html', {"username": username, "useremail": useremail, 'store':store})
    else:
        messages.error(request, "Not Logged In")
        return redirect('login')




#Trending list of user
def userTrendingList(request):
    if userSessionCheck(request) == True:
        if request.method == "POST":
            userid      = request.session['user_id']
            user_row    = fetchUserRow(userid)                                          #1. Store details from the session
            username    = user_row[3]                                                  #Store ID 
            email       = user_row[1]




            Parameter   = request.POST["Parameter"]

            if Parameter == "Rating":
                entry_count = 10
                cursor = connection.cursor()
                query_fetch_book = '''SELECT book_id, title, author, publisher, genre, year_of_publish, copies_sold, rating
                                      FROM Book
                                      ORDER BY rating
                                      DESC LIMIT 10'''

                cursor.execute(query_fetch_book)
                q_result = cursor.fetchall()
            
            else:
                entry_count = 10
                cursor = connection.cursor()
                query_fetch_book = '''SELECT book_id, title, author, publisher, genre, year_of_publish, copies_sold, rating
                                      FROM Book
                                      ORDER BY copies_sold
                                      DESC LIMIT 10'''

                cursor.execute(query_fetch_book)
                q_result = cursor.fetchall()


            trending_list = []
            print(q_result)
            for query_result in q_result:
                t_list = {}
                t_list['title']             = query_result[1]
                t_list['author']            = query_result[2]
                t_list['publisher']         = query_result[3]
                t_list['genre']             = query_result[4]
                t_list['year_of_publish']   = query_result[5]
                t_list['copies_sold']       = query_result[6]
                t_list['rating']            = query_result[7]
                trending_list.append(t_list)





            # t_list = Book.objects.all().order_by('-copies_sold')[:10]

            return render(request, 'users/trending_list.html', {"username": username, "email": email, "t_list": trending_list})
        else:
            userid      = request.session['user_id']
            user_row    = fetchUserRow(userid)                                          #1. Store details from the session
            username    = user_row[3]                                                  #Store ID 
            email       = user_row[1]

            entry_count = 10
            cursor = connection.cursor()
            query_fetch_book = '''SELECT book_id, title, author, publisher, genre, year_of_publish, copies_sold, rating
                                  FROM Book
                                  ORDER BY copies_sold
                                  DESC LIMIT 10'''


            cursor.execute(query_fetch_book)
            q_result = cursor.fetchall()

            trending_list = []
            for query_result in q_result:
                t_list = {}
                t_list['title']             = query_result[1]
                t_list['author']            = query_result[2]
                t_list['publisher']         = query_result[3]
                t_list['genre']             = query_result[4]
                t_list['year_of_publish']   = query_result[5]
                t_list['copies_sold']       = query_result[6]
                t_list['rating']            = query_result[7]
                trending_list.append(t_list)


            # t_list = Book.objects.all().order_by('-copies_sold')[:10]

            return render(request, 'users/trending_list.html', {"username": username, "email": email, "t_list": trending_list})
    else:
        messages.error(request, "Not Logged In")
        return redirect('login')






















#STORE FUNCTIONS
#Store function for Store Sign Up
#Atomic Transaction
def storeSignUp(request):
    if request.method == "POST":
        form = StoreSignUp(request.POST)
        if form.is_valid():
            store_name      = form.cleaned_data.get('store_name')
            email           = form.cleaned_data.get('email')
            password        = form.cleaned_data.get('password')
            website         = form.cleaned_data.get('website')
            phone_no        = form.cleaned_data.get('phone_no')
            address_line1   = form.cleaned_data.get('address_line1')
            address_line2   = form.cleaned_data.get('address_line2')
            city            = form.cleaned_data.get('city')
            district        = form.cleaned_data.get('district')
            state           = form.cleaned_data.get('state')
            zip_code        = form.cleaned_data.get('zip_code')
            print(type(phone_no))

            # storeCount = Book_store.objects.filter(email = email).count()
            cursor = connection.cursor()                                    #Taking out all the store entries with same email                               
            query_fetch_store = '''SELECT COUNT(*)
                                   FROM Book_store
                                   WHERE email=%s'''
            cursor.execute(query_fetch_store, [email])
            q_result = cursor.fetchone()
            storeCount = q_result[0]


            if storeCount == 0: 
                with transaction.atomic():
                                             #Check if the store with same email exsists or not
                    # form.save()

                    query_add_store = '''INSERT INTO Book_store(store_name, email, password, website, phone_no, address_line1, address_line2, city, district, state, zip_code)
                                        VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''
                    cursor.execute(query_add_store, [store_name, email, password, website, phone_no, address_line1, address_line2, city, district, state, zip_code])


                    storename   = form.cleaned_data.get('store_name')
                    email       = form.cleaned_data.get('email')

                    storeinfo   = {}
                    storeinfo['store_name'] = storename
                    storeinfo['email']      = email

                return render(request, 'store/signUpSuccess.html', context={'store':storeinfo})
            else:
                messages.error(request, 'Email Address already exists')
                return render(request, 'store/signUpFail.html', {})
        else:
            messages.error(request, "Invalid Form")
            return render(request, 'store/signUpFail.html', {})
    else:
        form = StoreSignUp()
    return render(request, 'store/storeSignUp.html', {"form":form})





#Store function for Store Log In
def storeLogin(request):
    if request.method == "POST":
        form = storeLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password')


            #storeCount = Book_store.objects.filter(email = email, password = raw_password).count()
            #q_result = Book_store.objects.filter(email = email, password = raw_password)
            cursor = connection.cursor()
            query = '''SELECT COUNT(*)
                       FROM Book_store
                       WHERE email=%s AND password=%s'''
            cursor.execute(query, [email, raw_password])
            q_result = cursor.fetchone()
            storeCount = q_result[0]


            if storeCount == 1:
                messages.info(request, f"You are now logged in with Email Id: {email}")
                #curr_store = Book_store.objects.filter(email = email, password = raw_password).first()
                request.session['email'] = request.POST['email']
                return redirect('storeProfile')
            else:
                messages.error(request, "Invalid Email or Password")
                return render(request, 'store/logInFail.html', {})
        else:
            messages.error(request, "Invalid Email or PASSWORD")
            return render(request, 'store/logInFail.html', {})
    else:
        form = storeLoginForm()
        return render(request, "store/storeLogin.html", context= {"form":form})





#Store function to display homepage of the Store
def storeProfile(request):
    if request.session.has_key('email'):
        storeemail = request.session['email']


        # query = Book_store.objects.filter(email = storeemail)
        cursor = connection.cursor()
        query_fetch_store = '''SELECT store_name, email
                               FROM Book_store
                               WHERE email=%s'''
        cursor.execute(query_fetch_store, [storeemail])
        store = cursor.fetchone()

        query = {}
        query['store_name'] = store[0]
        query['email'] = store[1]


        return render(request, 'store/storeProfile.html', {'store':query})
    else:
        return render(request, 'store/logInFail.html', {})





#Store function to Edit Store profile details
#Atomic Transaction
def storeEditProfile(request):
    if storeSessionCheck(request) == True:
        if request.method == "POST":
            form = StoreProfile(request.POST)
            if form.is_valid():
                email = form.cleaned_data.get('email')

                #store = Book_store.objects.filter(email = email)[0]
                cursor1 = connection.cursor()
                query_fetch_store = '''SELECT store_id, store_name, email
                                       FROM Book_store
                                       WHERE email=%s'''
                cursor1.execute(query_fetch_store, [email])
                store = cursor1.fetchone()

                storeinfo = {}
                storeinfo['email']      = store[2]
                storeinfo['store_name'] = store[1]


                with transaction.atomic():
                    new_website         = form.cleaned_data.get('website')
                    new_phone_no        = form.cleaned_data.get('phone_no')
                    new_address_line1   = form.cleaned_data.get('address_line1')
                    new_address_line2   = form.cleaned_data.get('address_line2')
                    new_city            = form.cleaned_data.get('city')
                    new_state           = form.cleaned_data.get('state')
                    new_district        = form.cleaned_data.get('district')
                    new_zip_code        = form.cleaned_data.get('zip_code')

                    query_update_store = '''UPDATE Book_store
                                            SET website=%s, phone_no=%s, address_line1=%s, address_line2=%s, city=%s, state=%s, district=%s, zip_code=%s
                                            WHERE email=%s'''
                    cursor1.execute(query_update_store, [new_website, new_phone_no, new_address_line1, new_address_line2, new_city, new_state, new_district, new_zip_code, store[2]])
                    # transaction.commit()


                    # store.website = form.cleaned_data.get('website')
                    # store.phone_no = form.cleaned_data.get('phone_no')
                    # store.rating = form.cleaned_data.get('rating')
                    # store.address_line1 = form.cleaned_data.get('address_line1')
                    # store.address_line2 = form.cleaned_data.get('address_line2')
                    # store.city = form.cleaned_data.get('city')
                    # store.state = form.cleaned_data.get('state')
                    # store.district = form.cleaned_data.get('district')
                    # store.zip_code = form.cleaned_data.get('zip_code')
                    # store.save()

                messages.info(request, "Profile Edited Sucesfully")
                return redirect('storeProfile')
            else:
                messages.error(request, "Invalid Form")
        else:
            storeemail = request.session['email']
            # store = Book_store.objects.filter(email = storeemail)[0]
            cursor2 = connection.cursor()
            query_fetch_store = '''SELECT store_id, store_name, email, website, phone_no, rating, address_line1, address_line2, city, district, state, zip_code
                                   FROM Book_store
                                   WHERE email=%s'''
            cursor2.execute(query_fetch_store, [storeemail])
            store = cursor2.fetchone()


            storeinfo = {}
            storeinfo['email']      = store[2]
            storeinfo['store_name'] = store[1]

            # fields = {'store_name':store.store_name, 'email':store.email, 'website':store.website,'phone_no':store.phone_no, 'rating':store.rating, 'address_line1':store.address_line1, 'address_line2':store.address_line2,
            # 'city':store.city, 'district':store.district, 'state':store.state, 'zip_code':store.zip_code}
            fields = {'store_name': store[1], 'email': store[2], 'website': store[3],'phone_no': store[4], 'rating':store[5], 'address_line1':store[6], 'address_line2':store[7],
            'city':store[8], 'district':store[9], 'state':store[10], 'zip_code':store[11]}
            form = StoreProfile(initial=fields)

        return render(request, 'store/storeProfileEdit.html', {"form":form, 'store': storeinfo})
    else:
        messages.error(request, "Not Logged In")
        return redirect('storeLogin')





#Store function to change password
#Atomic Transaction
def storeChangePasswd(request):
    if storeSessionCheck(request) == True:
        if request.method == "POST":
            form = storeChangePasswdForm(request.POST)
            if form.is_valid():
                old_password = form.cleaned_data.get('old_password')
                new_password = form.cleaned_data.get('new_password')

                storeemail = request.session['email']

                # store = Book_store.objects.filter(email = store_id)[0]
                cursor1 = connection.cursor()
                query_fetch_store = '''SELECT store_name, password, email
                                       FROM Book_Store
                                       WHERE email=%s'''
                cursor1.execute(query_fetch_store, [storeemail])
                store = cursor1.fetchone()

                storeinfo = {}
                storeinfo['email']      = store[2]
                storeinfo['store_name'] = store[0]

                if store[1] == old_password:
                    with transaction.atomic():
                        cursor2 = connection.cursor()
                        query_update_pswd = '''UPDATE Book_store
                                               SET password=%s
                                               WHERE email=%s'''
                        cursor2.execute(query_update_pswd, [new_password, storeemail])

                        # store.password = new_password
                        # store.save()
                    messages.info(request, "Password Changed Succesfully")
                    return redirect('storeProfile')
                else:
                    messages.error(request, "Wrong Old Password")
            else:
                messages.error(request, "Invalid Input")
        else:
            form = storeChangePasswdForm()
            storeemail = request.session['email']

            # store = Book_store.objects.filter(email = store_id)[0]
            cursor1 = connection.cursor()
            query_fetch_store = '''SELECT store_name, password, email
                                   FROM Book_Store
                                   WHERE email=%s'''
            cursor1.execute(query_fetch_store, [storeemail])
            store = cursor1.fetchone()

            storeinfo = {}
            storeinfo['email']      = store[2]
            storeinfo['store_name'] = store[0]

        return render(request, "store/change_password.html", context= {"form":form, 'store': storeinfo})
    else:
        messages.error(request, "Not Logged In")
        return redirect('storeLogin')





#Function to Logout the session
def storeLogout(request):
    try:
        del request.session['email']
    except :
        pass
    return redirect('index')





#Store Function to Search Books
def storeSearchBooks(request):
    if storeSessionCheck(request) == True:
        email       = request.session['email']

        store_row   = fetchStoreRow(email)                                        #1. Store details from the session
        store_id    = store_row[0]                                                 #Store ID 
        store_name  = store_row[1]    


        search_term = ''

        if request.method == "GET":
            if 'search' in request.GET:
                search_term = request.GET['search']
                filter = request.GET['filter']

                #1. Checking the main book table with search input
                if(filter == 'title'):
                    books_avl = Book.objects.filter( title__contains = search_term ).order_by('title')
                if(filter == 'genre'):
                    books_avl = Book.objects.filter( genre__contains = search_term ).order_by('title')
                if(filter == 'publisher'):
                    books_avl = Book.objects.filter( publisher__contains = search_term ).order_by('title')
                if(filter == 'author'):
                    books_avl = Book.objects.filter( author__contains = search_term ).order_by('title')

                books = books_avl

                # #2. Checking the Store Availability and collecting all options
                # books = []
                # for book in books_avl:
                #     book_in_store = Book_available.objetcs.filter(book_id = book.book_id)

                #     for options in book_in_store:
                #         book_option = {}
                #         book_option['book_id']          = book.book_id 
                #         book_option['title']            = book.title 
                #         book_option['author']           = book.author 
                #         book_option['publisher']        = book.publisher 
                #         book_option['genre']            = book.genre
                #         book_option['year_of_publish']  = book.year_of_publish 
                #         book_option['copies_sold']      = book.copies_sold 
                #         book_option['rating']           = book.rating

                #         book_option['stock_id']         = options.book_available_id
                #         book_option['store_id']         = options.store_email.store_id
                #         book_option['email']            = options.store_email.email
                #         book_option['price']            = options.price
                #         book_option['copies left']      = options.no_of_copies

                #         books.append(book_option)

            # books = Book.objects.all()
            print(books)
            return render(request, 'store/searchResult.html', {'store_name': store_name, 'store_email': email, 'books' : books, 'search_term': search_term, 'filter': filter })
        else:
            return redirect('storeProfile')
    else:
        messages.error(request, "Not Logged In")
        return redirect('storeLogin')




#Function to add book from the search result
#Atomic Transaction
def addBookfromSearch(request, book_id):
    if storeSessionCheck(request) == True:
        email       = request.session['email']

        store_row   = fetchStoreRow(email)                                        #1. Store details from the session
        store_id    = store_row[0]                                                #Store ID 
        store_name  = store_row[1]                                               #Store name extracted


        if request.method == "POST":

            with transaction.atomic():
                price = float(request.POST['price'])
                copies= int(request.POST['copies'], 10)

                available = Book_available.objects.filter(book_id = book_id, store_email = email).count()
                if available == 0:
                    stock = Book_available()
                    stock.book_id       = Book.objects.get(book_id = book_id)
                    stock.store_email   = Book_store.objects.get(email = email)
                    stock.price         = price 
                    stock.no_of_copies  = copies
                    stock.save()
                    # cursor = connection.cursor()
                    # query_del = '''DELETE
                    #                FROM Book_available
                    #                WHERE book_id=%s'''
                    # cursor.execute(query_del, [book_id])
                    messages.success(request, "Book added successfully")
                    return redirect('storeProfile')
                else:
                    messages.success(request, " Cannot Add. Book already in the Stock")
                    return redirect('storeProfile')
        else:
                return redirect('storeProfile')

        return redirect('storeProfile')
    else:
        messages.error(request, "Not Logged In")
        return redirect('storeLogin')




#Store Function to add book by the store user 
#Atomic Transaction   
def storeBookAdd(request):
    if storeSessionCheck(request) == True:
        if request.method == "POST":
            storeemail = request.session['email']

            cursor1 = connection.cursor()
            query_fetch_store = '''SELECT store_name, email
                                   FROM Book_Store
                                   WHERE email=%s'''
            cursor1.execute(query_fetch_store, [storeemail])
            q1_result = cursor1.fetchone()

            store = {}
            store['store_name'] = q1_result[0]
            store['email']      = q1_result[1]


            form = bookAddForm(request.POST)


            if form.is_valid():
                title           = form.cleaned_data.get('title')                        #1. Obtaining the form data
                author          = form.cleaned_data.get('author')
                publisher       = form.cleaned_data.get('publisher')
                genre           = form.cleaned_data.get('genre')
                year_of_publish = form.cleaned_data.get('year_of_publish')
                no_of_books     = form.cleaned_data.get('no_of_books')
                price           = form.cleaned_data.get('price')



                query_title     = title.upper()
                query_author    = author.upper()
                query_publisher = publisher.upper()

                cursor2 = connection.cursor()                                           #2. Checking if the book exsisits or not already
                query_fetch_books = '''SELECT COUNT(*)
                                       FROM Book
                                       WHERE UPPER(title)=%s AND UPPER(author)=%s AND UPPER(publisher)=%s'''

                cursor2.execute(query_fetch_books, [query_title, query_author, query_publisher])
                q_result = cursor2.fetchone()
                this_book_count = q_result[0]
                # this_book_count = Book.objects.filter(title = newUser.title, publisher = newUser.publisher).count()
                

                with transaction.atomic():
                    if this_book_count == 0:
                        copies_sold = 0
                                                                    #3. Saving in the main Book table
                        query_add_Book = '''INSERT INTO Book(title, author, publisher, genre, year_of_publish, copies_sold)
                                            VALUES (%s, %s, %s, %s, %s, 0)'''
                        cursor1.execute(query_add_Book, [title, author, publisher, genre, year_of_publish])



                                                                    #4. Fetch the Book id of the Book Inserted
                        query_book = '''SELECT book_id
                                        FROM Book
                                        WHERE UPPER(title)=%s AND UPPER(author)=%s AND UPPER(publisher)=%s'''
                        cursor1.execute(query_book, [query_title, query_author, query_publisher])
                        q_book_result = cursor1.fetchone()

                        q_book_id = q_book_result[0]
                        print(q_book_id)


                                                                    #5. Add it to Book_available table
                        bookAddedtoStore            = Book_available()
                        bookAddedtoStore.book_id    = Book.objects.get(book_id = q_book_id)
                        bookAddedtoStore.store_email= Book_store.objects.get(email = storeemail)
                        bookAddedtoStore.price      = price
                        bookAddedtoStore.no_of_copies = no_of_books
                        bookAddedtoStore.save()

                        # q_add = '''INSERT INTO Book_available(book_id, store_email, no_of_copies, price)
                        #            VALUES (%s, %s, %s, %s)'''
                        # cursor1.execute(q_add, [q_book_id, storeemail, no_of_books, price])

                    else:
                                                                    #1. Get the book id from the central book database
                        # book_id_ = Book.objects.filter(title = title, publisher= publisher)[0].book_id
                        query_book = '''SELECT book_id
                                        FROM Book
                                        WHERE UPPER(title)=%s AND UPPER(author)=%s AND UPPER(publisher)=%s'''
                        cursor1.execute(query_book, [query_title, query_author, query_publisher])
                        q_book_result = cursor1.fetchone()

                        q_book_id = q_book_result[0]
                        print(q_book_id)


                                                                    #2. Get the count of entries in Book available table
                        cnt = Book_available.objects.filter(book_id = q_book_id, store_email = storeemail).count()
                        # query_book_avl = '''SELECT COUNT(*)
                        #                     FROM Book_available
                        #                     WHERE book_id=%s AND store_email=%s '''
                        # cursor1.execute(query_book_avl, [q_book_id, storeemail])
                        # q_result_bk_avl = cursor1.fetchone()
                        # cnt = q_result_bk_avl[0]
                        # print(cnt)

                        
                        if cnt == 0:
                            bookAddedtoStore            = Book_available()
                            bookAddedtoStore.book_id    = Book.objects.get(book_id = q_book_id)
                            bookAddedtoStore.store_email= Book_store.objects.get(email = storeemail)
                            bookAddedtoStore.price      = price
                            bookAddedtoStore.no_of_copies = no_of_books
                            bookAddedtoStore.save()
                        else :
                            storeBook           = Book_available.objects.get(book_id = q_book_id, store_email = storeemail)
                            storeBook.no_of_copies = storeBook.no_of_copies + no_of_books
                            storeBook.price        = price
                            storeBook.save()


                messages.success(request, "Book Successfully Added")

            else:
                messages.error(request, "Invalid Book Data Entered")

            return render(request, 'store/addBook.html',{"form":form, 'store': store})
        else:
            storeemail = request.session['email']

            cursor1 = connection.cursor()
            query_fetch_store = '''SELECT store_name, email
                                   FROM Book_Store
                                   WHERE email=%s'''
            cursor1.execute(query_fetch_store, [storeemail])
            q1_result = cursor1.fetchone()

            store = {}
            store['store_name'] = q1_result[0]
            store['email']      = q1_result[1]
                  
            addBookForm = bookAddForm()
            return render(request, 'store/addBook.html',{"form":addBookForm, 'store': store})
        
    else:
        messages.error(request, "Not Logged In")
        return redirect('storeLogin')





#Store function to display the list of stock books in the store
def storeBookView(request):
    if storeSessionCheck(request) == True:
        storeemail = request.session['email']

        # store = Book_store.objects.filter(email = store_id)[0]
        cursor1 = connection.cursor()
        query_fetch_store = '''SELECT store_name, email
                               FROM Book_Store
                               WHERE email=%s'''
        cursor1.execute(query_fetch_store, [storeemail])
        q1_result = cursor1.fetchone()

        store = {}
        store['store_name'] = q1_result[0]
        store['email']      = q1_result[1]

        books = Book_available.objects.filter(store_email = storeemail)
        # query_fetch_avail = '''SELECT book_id, no_of_copies, price
        #                        FROM Book_available
        #                        WHERE store_email=%s'''
        # cursor1.execute(query_fetch_avail, [storeemail])
        # books = cursor1.fetchall()

        book_list = []
        for b in books:
            # book = Book.objects.filter(book_id = b.book_id.book_id)[0]
            cursor2 = connection.cursor()
            query_fetch_book = '''SELECT book_id, title, author, publisher, genre, year_of_publish, copies_sold, rating
                                  FROM Book
                                  WHERE book_id=%s'''
            cursor2.execute(query_fetch_book, [b.book_id.book_id])
            q2_result = cursor2.fetchone()

            print(q2_result)

            book = {}
            book['book_id']         = q2_result[0]
            book['title']           = q2_result[1]
            book['author']          = q2_result[2]
            book['publisher']       = q2_result[3]
            book['genre']           = q2_result[4]
            book['year_of_publish'] = q2_result[5]
            book['copies_sold']     = q2_result[6]
            book['rating']          = q2_result[7]
            book_list.append({'book':book, 'price':b.price, 'copies':b.no_of_copies})
        
        # cursor = connection.cursor()
        # query = '''SELECT Book.book_id, Book.title, Book.author, Book.publisher, Book.genre, Book.year_of_publish, Book.price, Book.copies_sold, Book.rating
        # FROM Book, Book_available WHERE Book_available.store_email = %s AND Book.book_id = Book_available.book_id'''
        # cursor.execute(query, [store_id])
        # book_list = cursor.fetchall()

        return render(request, 'store/book_list.html', {"book_list": book_list, "store":store})
    else:
        messages.error(request, "Not Logged In")
        return redirect('storeLogin')





#Store function to delete a book entry from the store
def storeBookDel(request, book_id):
    if storeSessionCheck(request) == True:
        email       = request.session['email']
        store_row   = fetchStoreRow(email)                                        #1. Store details from the session
        store_id    = store_row[0]                                                 #Store ID 
        store_name  = store_row[1]                                               #Store name extracted

        with transaction.atomic():
            Book_available.objects.filter(book_id = book_id, store_email = email).delete()

            # cursor = connection.cursor()
            # query_del = '''DELETE
            #                FROM Book_available
            #                WHERE book_id=%s'''
            # cursor.execute(query_del, [book_id])

        return redirect('storeBookView')
    else:
        messages.error(request, "Not Logged In")
        return redirect('storeLogin')





#Store function to update book details
#Atomic Transaction
def storeUpdateBook(request, book_id):
    if storeSessionCheck(request) == True:
        email       = request.session['email']
        store_row   = fetchStoreRow(email)                                          #1. Store details from the session
        store_id    = store_row[0]                                                  #Store ID 
        store_name  = store_row[1]                                                  #Store name extracted

        with transaction.atomic():
            price   = float(request.POST["price"])
            copies  = int(request.POST["copies"])

            bookAndStore                = Book_available.objects.get(book_id = book_id, store_email = email)
            bookAndStore.price          = price
            bookAndStore.no_of_copies   = copies
            bookAndStore.save()

        return redirect('storeBookView')

        # else:
        #     updateForm = updateBookForm()
        #     return render(request, 'store/updateBook.html',{"form":updateForm})
        
        # if request.session.has_key('email'):
        #     posts = request.session['email']
        #     query = Book_store.objects.filter(email = posts)
        #     return render(request, 'store/storeProfile.html', {"query":query})    
    else:
        messages.error(request, "Not Logged In")
        return redirect('storeLogin')




#Shows the Options to see the three different types of order list
def storeOrderList(request):
    if storeSessionCheck(request) == True:
        email = request.session['email']
        
        cursor = connection.cursor()
        query = '''SELECT store_name, email
                   FROM Book_store
                   WHERE email=%s'''

        cursor.execute(query, [email])
        q_result_store = cursor.fetchone()
        
        q_result = {}
        q_result['email']       = q_result_store[1]
        q_result['store_name']  = q_result_store[0]


        return render(request, 'store/storeOrders.html', {'q_result' : q_result})
    else:
        messages.error(request, "Not Logged In")
        return redirect('storeLogin')





#Store function to display the order list of the store
def deliveredOrder(request):
    if storeSessionCheck(request) == True:
        email       = request.session['email']
        store_row   = fetchStoreRow(email)                                          #1. Store details from the session
        store_id    = store_row[0]                                                  #Store ID 
        store_name  = store_row[1]                                                  #Store name extracted
        
        status      = "Delivered"                                                        #2. Status to be searched

        # cursor = connection.cursor()
        # query = '''SELECT *
        #            FROM Order 
        #            WHERE store_id.pk=%d AND status=%s'''
        # cursor.execute(query, [store_id, status])
        # q_result = cursor.fetchall()

        
        q_result = Order.objects.filter(store_id = store_id, status = status).order_by('-date_of_order')   #3. Selecting all the rows from the Order table with the given store_id and status
        return render(request, 'store/deliveredOrders.html', {'store_email': email, 'store_name' : store_name,  'q_result' : q_result})
    else:
        messages.error(request, "Not Logged In")
        return redirect('storeLogin')





#Store function to display the order list of the store
def inProcessOrder(request):
    if storeSessionCheck(request) == True:
        email       = request.session['email']
        store_row   = fetchStoreRow(email)                                          #1. Store details from the session
        store_id    = store_row[0]                                                  #Store ID 
        store_name  = store_row[1]                                                  #Store name extracted
        
        status      = "Processing"                                                  #2. Status to be searched

        # cursor = connection.cursor()
        # query = '''SELECT *
        #            FROM Order 
        #            WHERE store_id.pk=%d AND status=%s'''
        # cursor.execute(query, [store_id, status])
        # q_result = cursor.fetchall()

        
        q_result = Order.objects.filter(store_id = store_id, status = status).order_by('-date_of_order')   #3. Selecting all the rows from the Order table with the given store_id and status
        return render(request, 'store/processingOrder.html', {'store_email': email, 'store_name' : store_name,  'q_result' : q_result})
    else:
        messages.error(request, "Not Logged In")
        return redirect('storeLogin')





#Store function to display the order list of the store
def cancelledOrder(request):
    if storeSessionCheck(request) == True:
        email       = request.session['email']
        store_row   = fetchStoreRow(email)                                          #1. Store details from the session
        store_id    = store_row[0]                                                  #Store ID 
        store_name  = store_row[1]                                                  #Store name extracted
        
        status      = "Cancelled"                                                        #2. Status to be searched

        # cursor = connection.cursor()
        # query = '''SELECT *
        #            FROM Order 
        #            WHERE store_id.pk=%d AND status=%s'''
        # cursor.execute(query, [store_id, status])
        # q_result = cursor.fetchall()

        
        q_result = Order.objects.filter(store_id = store_id, status = status).order_by('-date_of_order')   #3. Selecting all the rows from the Order table with the given store_id and status
        return render(request, 'store/cancelledOrder.html', {'store_email': email, 'store_name' : store_name,  'q_result' : q_result})
    else:
        messages.error(request, "Not Logged In")
        return redirect('storeLogin')





#Store function to set the delivered date
#Atomic Transaction
def setDelivered(request, order_id):
    if storeSessionCheck(request) == True:
        form = DateInputForm(request.POST)
        if form.is_valid():
            date = form.cleaned_data.get('date')
            
            email = request.session['email']
            store_row = fetchStoreRow(email)                                        #1. Store details from the session
            store_id  = store_row[0]                                                 #Store ID 
            store_name = store_row[1]                                               #Store name extracted
            
            with transaction.atomic():
                q_result_order = Order.objects.get(store_id = store_id, order_id = order_id)                #2. Fetching the given order by order_id

                books_order    = Book_ordered.objects.filter(order_id = order_id)
                copies_sold = 0
                for entry in books_order:
                    book_instance = Book.objects.get(book_id = entry.book_id.book_id)
                    book_instance.copies_sold = book_instance.copies_sold + entry.no_of_copies

                    book_instance.save()



                q_result_order.delivered_date   = date
                q_result_order.status           = "Delivered"
                q_result_order.save()

            return redirect('inProcessOrder')
        else:
            messages.error(request, "Invalid Book Data Entered")
    else:
        messages.error(request, "Not Logged In")
        return redirect('storeLogin')





#Store function to set the expected delivery date
#Atomic Transaction
def setExpectedDeliveryDate(request, order_id):
    if storeSessionCheck(request) == True:
        form = DateInputForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                date = form.cleaned_data.get('date')

                email       = request.session['email']
                store_row   = fetchStoreRow(email)                                          #1. Store details from the session
                store_id    = store_row[0]                                                  #Store ID 
                store_name  = store_row[1]                                                  #Store name extracted


                q_result_order = Order.objects.get(store_id = store_id, order_id = order_id)                #2. Fetching the given order by order_id

                q_result_order.expected_delivery_date = date
                q_result_order.save()
            return redirect('inProcessOrder')
        else:
            messages.error(request, "Invalid Book Data Entered")
    else:
        messages.error(request, "Not Logged In")
        return redirect('storeLogin')





#Store function to set the order as processing
#Atomic Transaction
def setProcessing(request, order_id):
    if storeSessionCheck(request) == True:            
            email       = request.session['email']
            store_row   = fetchStoreRow(email)                                          #1. Store details from the session
            store_id    = store_row[0]                                                  #Store ID 
            store_name  = store_row[1]                                                  #Store name extracted
            
            with transaction.atomic():
                q_result_order = Order.objects.get(store_id = store_id, order_id = order_id)                #2. Fetching the given order by order_id

                old_status                      = q_result_order.status
                q_result_order.delivered_date   = None
                q_result_order.cancelled_date   = None
                q_result_order.status           = "Processing"
                q_result_order.save()

            if old_status == "Delivered":
                return redirect('deliveredOrder')
            elif old_status == "Cancelled":
                return redirect('cancelledOrder')
    else:
        messages.error(request, "Not Logged In")
        return redirect('storeLogin')





#Function to set the order as cancelled
#Atomic Transaction
def setCancelled(request, order_id):
    if storeSessionCheck(request) == True:
        form = TextInputForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                remarks = form.cleaned_data.get('text')

                email       = request.session['email']
                store_row   = fetchStoreRow(email)                                        #1. Store details from the session
                store_id    = store_row[0]                                                 #Store ID 
                store_name  = store_row[1]                                               #Store name extracted


                q_result_order = Order.objects.get(store_id = store_id, order_id = order_id)                #2. Fetching the given order by order_id

                q_result_order.delivered_date       = None
                q_result_order.cancelled_date       = None
                q_result_order.status               = "Cancelled"
                q_result_order.cancelled_date       = date.today()
                q_result_order.cancelled_by         = "Store"
                q_result_order.cancellation_remarks = remarks 
                q_result_order.save()

                order_books = Book_ordered.objects.filter(order_id = order_id)

                for books in order_books:
                    copies = books.no_of_copies

                    aval_book = Book_available.objects.get(book_id = books.book_id.book_id, store_email = email)
                    aval_book.no_of_copies = aval_book.no_of_copies + copies 
                    aval_book.save()



            return redirect('inProcessOrder')
        else:
            messages.error(request, "Invalid Book Data Entered")
    else:
        messages.error(request, "Not Logged In")
        return redirect('storeLogin')





#Store Function to display the details of all the orders
def orderDetails(request, order_id):
    if storeSessionCheck(request) == True:
        email       = request.session['email']
        store_row   = fetchStoreRow(email)                                          #1. Store details from the session
        store_id    = store_row[0]                                                  #Store ID 
        store_name  = store_row[1]                                                  #Store name extracted

        
        q_result_order = Order.objects.get(store_id = store_id, order_id = order_id)                #2. Fetching the given order by order_id


        cursor = connection.cursor()                                                                #3. Fetching all the books in the order with id order_id
        # query1 = '''SELECT *
        #             FROM Book_ordered
        #             WHERE order_id =%s'''
        # cursor.execute(query1, [order_id])
        # q_result_bk_ids = cursor.fetchall()
        q_result_bk_ids = Book_ordered.objects.filter(order_id = order_id)                      

        
        address = Customer_address.objects.get(user_id = q_result_order.user_id, address_no = q_result_order.address_no)    #4. Fetching the address where to be sent

        q_result_final = []                                                                                         #List of book and their details                         
        q_result = []                                                                                               #List of books

        for bk_id in q_result_bk_ids:                                                                               #5. Creating a list of books to be sent for html rendering
            instance = {} 

            #books_fetch = Book.objects.get(book_id = bk_id.book_id.pk)                                             #Book entry fetched from the table
            query_fetch_book = '''SELECT *
                                  FROM Book
                                  WHERE book_id=%s'''                                                               #Book id with its details
            cursor.execute(query_fetch_book, [bk_id.book_id.pk])
            books_fetch = cursor.fetchone()

            
            book_avail_price = Book_available.objects.get(book_id = bk_id.book_id.pk, store_email = email)        #Price entry from the Book_available table            
            # query_fetch_price = '''SELECT *
            #                        FROM Book_available
            #                        WHERE book_id=%s AND store_email=%s'''
            # cursor.execute(query_fetch_price, [bk_id.book_id.pk, email])
            # book_avail_price = cursor.fetchone()


            # instance['id'] = books_fetch.book_id
            # instance['title'] = books_fetch.title
            # instance['author'] = books_fetch.author
            instance['id']      = books_fetch[0]
            instance['title']   = books_fetch[1]
            instance['author']  = books_fetch[2]
            instance['price']   = book_avail_price.price
            instance['copies']  = bk_id.no_of_copies


            q_result_final.append(instance)
            q_result.append(books_fetch)

        if q_result_order.status == "Delivered":
            return  render(request, 'store/deliveredOrderDetails.html', {'store_email': email, 'store_name' : store_name, 'q_result_order' : q_result_order, 'books' : q_result, 'copies' : q_result_final , 'address' : address})
        elif q_result_order.status == "Processing":
            form1 = DateInputForm()
            form2 = TextInputForm()
            return  render(request, 'store/processingOrderDetails.html', {'dateform1' : form1, 'dateform2' : form1, 'textform' : form2, 'store_email': email, 'store_name' : store_name, 'q_result_order' : q_result_order, 'books' : q_result, 'copies' : q_result_final , 'address' : address})            
        elif q_result_order.status == "Cancelled":
            return  render(request, 'store/cancelledOrderDetails.html', {'store_email': email, 'store_name' : store_name, 'q_result_order' : q_result_order, 'books' : q_result, 'copies' : q_result_final , 'address' : address})            

    else:
        messages.error(request, "Not Logged In")
        return redirect('storeLogin')





#Extract data from order schema and returns books according to status 
def storeSalesList(request):
    if storeSessionCheck(request) == True:
        if request.method == "POST":
            storeemail = request.session['email']

            cursor1 = connection.cursor()
            query = '''SELECT store_id, store_name, email
                       FROM Book_store
                       WHERE email=%s'''

            cursor1.execute(query, [storeemail])
            q_result_store = cursor1.fetchone()
            
            store = {}
            store_email     = q_result_store[2]
            store_name      = q_result_store[1]
            store_id        = q_result_store[0]




            start_date = request.POST['start_date']
            end_date   = request.POST['end_date']
            if start_date != None or end_date != None:

                order_list = Order.objects.filter(store_id = store_id, status = "Delivered", delivered_date__range = [start_date, end_date]).order_by('-delivered_date')[:20]

                total_amt = 0
                for order in order_list:
                    total_amt = total_amt + order.total_price
            else:
                messages.error(request, "Enter the Date correctly")


            return render(request, 'store/salesList.html', {'store_email': store_email, 'store_name' : store_name,'o_list': order_list, 'amount': total_amt})

        else:
            storeemail = request.session['email']

            cursor1 = connection.cursor()
            query = '''SELECT store_id, store_name, email
                       FROM Book_store
                       WHERE email=%s'''

            cursor1.execute(query, [storeemail])
            q_result_store = cursor1.fetchone()
            
            store = {}
            store_email     = q_result_store[2]
            store_name      = q_result_store[1]
            store_id        = q_result_store[0]


            order_list = Order.objects.filter(store_id = store_id, status = "Delivered").order_by('-date_of_order')[:20]

            total_amt = 0
            for order in order_list:
                total_amt = total_amt + order.total_price

            return render(request, 'store/salesList.html', {'store_email': store_email, 'store_name' : store_name,'o_list': order_list, 'amount': total_amt})
    else:
        messages.error(request, "Not Logged In")
        return redirect('storeLogin')





#Uses user_id and store_id 
def storeUserList(request):
    if storeSessionCheck(request) == True:
        storeemail = request.session['email']

        cursor1 = connection.cursor()
        query = '''SELECT store_name, email
                   FROM Book_store
                   WHERE email=%s'''

        cursor1.execute(query, [storeemail])
        q_result_store = cursor1.fetchone()
        
        store = {}
        store['email']       = q_result_store[1]
        store['store_name']  = q_result_store[0]
        # store = Book_store.objects.get(email = storeemail)
        

        users = Users_list.objects.filter(store_email = storeemail)

        user_list = []
        for u in users:
            cursor2 = connection.cursor()
            query_fetch_user = '''SELECT user_id, first_name, middle_name, last_name, email, phone_no
                                  FROM Customer
                                  WHERE user_id=%s '''
            cursor2.execute(query_fetch_user, [u.user_id.user_id])
            query_result_user = cursor2.fetchone()

            user = {}
            user['user_id']     = query_result_user[0] 
            user['first_name']  = query_result_user[1] 
            user['middle_name'] = query_result_user[2] 
            user['last_name']   = query_result_user[3] 
            user['email']       = query_result_user[4] 
            user['phone_no']    = query_result_user[5] 
             # user = Customer.objects.filter(user_id = u.user_id.user_id)[0]
            
            user_list.append(user)
        
        return render(request, 'store/user_list.html', {"user_list": user_list, "store":store})
    else:
        messages.error(request, "Not Logged In")
        return redirect('storeLogin')




#Display the user address
def storeUserAddress(request, user_id):
    if storeSessionCheck(request) == True:
        email       = request.session['email']
        store_row   = fetchStoreRow(email)                                          #1. Store details from the session
        store_id    = store_row[0]                                                  #Store ID 
        store_name  = store_row[1]                                                  #Store name extracted


        cursor = connection.cursor()
        query_fetch_user = '''SELECT first_name, middle_name, last_name, email
                              FROM Customer
                              WHERE user_id=%s'''
        cursor.execute(query_fetch_user, [user_id])
        query_result = cursor.fetchone()

        user = {}
        user['first_name']  = query_result[0]
        user['middle_name'] = query_result[1]
        user['last_name']   = query_result[2]
        user['email']       = query_result[3]
        print(user)
        # user = Customer.objects.filter(user_id = user_id)[0]


        address = Customer_address.objects.get(user_id = user_id, is_current = True)

        return render(request, 'store/user_address.html', {'store_email': email, 'store_name' : store_name, 'address':address, 'user':user})
    else:
        messages.error(request, "Not Logged In")
        return redirect('storeLogin')




#Store Trending List
def storeTrendingList(request):
    if storeSessionCheck(request) == True:
        if request.method == "POST":
            email       = request.session['email']
            store_row   = fetchStoreRow(email)                                          #1. Store details from the session
            store_id    = store_row[0]                                                  #Store ID 
            store_name  = store_row[1]




            Parameter  = request.POST["Parameter"]

            if Parameter == "Rating":
                entry_count = 10
                cursor = connection.cursor()
                query_fetch_book = '''SELECT book_id, title, author, publisher, genre, year_of_publish, copies_sold, rating
                                      FROM Book
                                      ORDER BY rating
                                      DESC LIMIT 10'''

                cursor.execute(query_fetch_book)
                q_result = cursor.fetchall()
            
            else:
                entry_count = 10
                cursor = connection.cursor()
                query_fetch_book = '''SELECT book_id, title, author, publisher, genre, year_of_publish, copies_sold, rating
                                      FROM Book
                                      ORDER BY copies_sold
                                      DESC LIMIT 10'''

                cursor.execute(query_fetch_book)
                q_result = cursor.fetchall()


            trending_list = []
            print(q_result)
            for query_result in q_result:
                t_list = {}
                t_list['title']             = query_result[1]
                t_list['author']            = query_result[2]
                t_list['publisher']         = query_result[3]
                t_list['genre']             = query_result[4]
                t_list['year_of_publish']   = query_result[5]
                t_list['copies_sold']       = query_result[6]
                t_list['rating']            = query_result[7]
                trending_list.append(t_list)





            # t_list = Book.objects.all().order_by('-copies_sold')[:10]

            return render(request, 'store/trending_list.html', {'store_email': email, 'store_name' : store_name, "t_list": trending_list})
        else:
            email       = request.session['email']
            store_row   = fetchStoreRow(email)                                          #1. Store details from the session
            store_id    = store_row[0]                                                  #Store ID 
            store_name  = store_row[1]


            entry_count = 10
            cursor = connection.cursor()
            query_fetch_book = '''SELECT book_id, title, author, publisher, genre, year_of_publish, copies_sold, rating
                                  FROM Book
                                  ORDER BY copies_sold
                                  DESC LIMIT 10'''


            cursor.execute(query_fetch_book)
            q_result = cursor.fetchall()

            trending_list = []
            for query_result in q_result:
                t_list = {}
                t_list['title']             = query_result[1]
                t_list['author']            = query_result[2]
                t_list['publisher']         = query_result[3]
                t_list['genre']             = query_result[4]
                t_list['year_of_publish']   = query_result[5]
                t_list['copies_sold']       = query_result[6]
                t_list['rating']            = query_result[7]
                trending_list.append(t_list)


            # t_list = Book.objects.all().order_by('-copies_sold')[:10]

            return render(request, 'store/trending_list.html', {'store_email': email, 'store_name' : store_name, "t_list": trending_list})

    else:
        messages.error(request, "Not Logged In")
        return redirect('storeLogin') 









#Miscellaneous functions
# Function to check if the HTTP request is on session
def storeSessionCheck(request):
    if request.session.has_key('email'):
        email = request.session['email']
        cursor = connection.cursor()
        query = '''SELECT *
                   FROM Book_store
                   WHERE email=%s'''

        cursor.execute(query, [email])
        q_result = cursor.fetchall()
        storeCount = len(q_result)

        if storeCount == 1:
            return True
        else:
            return False
    else:
        return False


#Function to check if the HTTP request is on session
def userSessionCheck(request):
    if request.session.has_key('user_id'):
        userid = request.session['user_id']
        cursor = connection.cursor()
        query = '''SELECT *
                   FROM Customer
                   WHERE user_id=%s'''

        cursor.execute(query, [userid])
        q_result = cursor.fetchall()
        userCount = len(q_result)

        if userCount == 1:
            return True
        else:
            return False
    else:
        return False




#Function to fetch the row of the store table
def fetchStoreRow(email):
    cursor = connection.cursor()
    query = '''SELECT *
               FROM Book_store
               WHERE email=%s'''

    cursor.execute(query, [email])
    q_result = cursor.fetchone()
    return q_result



#Function to fetch the row of the user table
def fetchUserRow(userid):
    cursor = connection.cursor()
    query = '''SELECT user_id, email, password, first_name, middle_name, last_name, phone_no, no_of_addr
               FROM Customer
               WHERE user_id=%s'''
    cursor.execute(query, [userid])
    q_result = cursor.fetchone()
    return q_result




