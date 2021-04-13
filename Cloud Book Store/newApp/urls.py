from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name ='index'),
    path('trending_list', views.trendingList, name = 'trendingList'),




    path('userSignUp', views.signup, name ='UserSignUp'),
    path('users/login', views.login, name = 'login'),
    path('user/profile', views.userProfile, name = 'userProfile'),
    path('users/change_password', views.userChangePasswd, name ='userChangePasswd'),
    path('user/edit_profile', views.userEditProfile, name = 'userEditProfile'),
    path('users/add_address', views.userAddAddress, name = "userAddAddress"),
    path('users/change_primary_addr/<int:addr_no>', views.setPrimaryAddress, name = "setPrimaryAddress"),
    path('users/logout', views.userLogout, name ='logout'),


    path('users/searchBooks', views.searchBooks, name = 'searchBooks'),
    path('users/searchViewBook/<int:book_id>/', views.searchViewBook, name = 'searchViewBook'),


    path('users/userCart', views.userCart, name = 'userCart'),
    path('users/addToCart/<int:stock_id>/', views.addToCart, name = 'addToCart'),
    path('users/updateCart/<int:cart_id>', views.updateCart, name = 'updateCart'),
    path('users/deleteCart/<int:cart_id>/', views.deleteCart, name = 'deleteCart'),
    path('users/cartView/<int:cart_id>/', views.cartView, name = 'cartView'),


    path('users/confirmAddress', views.confirmAddress, name = 'confirmAddress'),
    path('users/userAddAsPrimaryAddress/<int:address_id>', views.userAddAsPrimaryAddress, name = 'userAddAsPrimaryAddress'),
    path('users/userPlaceOrder/<int:address_no>', views.userPlaceOrder, name = 'userPlaceOrder'),


    path('users/userOrderList', views.userOrderList, name = 'userOrderList'),
    path('users/userDeliveredOrder', views.userDeliveredOrder, name = 'userDeliveredOrder'),
    path('users/userCancelledOrder', views.userCancelledOrder, name = 'userCancelledOrder'),
    path('users/userInProcessOrder', views.userInProcessOrder, name = 'userInProcessOrder'),
    path('users/userOrderDetails/<int:order_id>/', views.userOrderDetails,   name = 'userOrderDetails'),
    path('users/userCancelOrder<int:order_id>/', views.userCancelOrder, name = 'userCancelOrder'),
    path('users/userComplaint<int:order_id>/', views.userComplaint, name = 'userComplaint'),


    path('users/addToReadList<int:book_id>/', views.addToReadList, name = 'addToReadList'),
    path('users/userReview<int:book_id>/', views.userReview, name = 'userReview'),


    path('users/userBookList', views.userBookList,  name = "userBookList"),
    path('viewBook/<int:book_id>/', views.viewBook, name= 'viewBook'),    
    path('removeBook/<int:book_id>/', views.userRemoveBook, name = 'removeBook'),


    path('users/trending_list', views.userTrendingList, name = "userTrendingList"),
    path('seller_list', views.sellerList, name = "sellerList"),
    path('users/store_address/<str:email>', views.sellerListStoreAddress, name = "sellerListStoreAddress"),




    path('storeSignUp', views.storeSignUp, name = 'storeSignUp'),
    path('storeLogin',views.storeLogin, name= 'storeLogIn'),
    path('store/storeProfile', views.storeProfile, name = 'storeProfile'),
    path('store/edit_profie', views.storeEditProfile, name = 'storeEditProfile'),
    path('store/change_password', views.storeChangePasswd, name = "storeChangePasswd"),
    path('store/storeLogout', views.storeLogout, name = 'storeLogout'),
    

    path('store/storeSearchBooks', views.storeSearchBooks, name = 'storeSearchBooks'),
    path('store/addBookfromSearch/<int:book_id>/', views.addBookfromSearch, name = 'addBookfromSearch'),


    path('store/addBook', views.storeBookAdd, name = 'storeAddBook'),

    
    path('store/book_list', views.storeBookView, name = "storeBookView"),
    path('store/delete_book/<int:book_id>/', views.storeBookDel, name = "storeBookDel"),
    path('store/update_book/<int:book_id>/', views.storeUpdateBook, name = "storeUpdateBook"),


    path('store/user_list', views.storeUserList, name = "storeUserList"),
    path('store/user_address/<str:user_id>/', views.storeUserAddress, name = "storeUserAddress"),
    

    path('store/order_list', views.storeOrderList, name = 'storeOrderList'),
    path('orderDelivered', views.deliveredOrder, name = 'deliveredOrder'),
    path('orderCancelled', views.cancelledOrder, name = 'cancelledOrder'),
    path('orderProcessing', views.inProcessOrder, name='inProcessOrder'),
    path('orderDetails/<slug:order_id>/', views.orderDetails, name = 'orderDetails'),


    path('setDelivered/<slug:order_id>/', views.setDelivered, name='setDelivered'),
    path('setExpectedDeliveryDate/<slug:order_id>/', views.setExpectedDeliveryDate, name='setExpectedDeliveryDate'), 
    path('setProcessing/<slug:order_id>/', views.setProcessing, name='setProcessing'),
    path('setCancelled/<slug:order_id>/', views.setCancelled, name='setCancelled'),  


    path('store/storeSales', views.storeSalesList, name ='storeSalesList'), 

    
    path('store/trending_list', views.storeTrendingList, name = "storeTrendingList"),
]

