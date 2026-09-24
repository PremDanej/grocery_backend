```text
grocery_backend/
├── manage.py
├── db.sqlite3
├── requirements.txt
├── core/                 
│   ├── __init__.py
│   ├── settings.py       
│   ├── urls.py           
│   ├── asgi.py
│   └── wsgi.py
├── users/                
│   ├── models.py         # UserProfile model
│   ├── serializers.py    # UserProfileSerializer
│   ├── views.py
│   └── urls.py
├── catalog/              
│   ├── models.py         # Category, Product models
│   ├── serializers.py    # CategorySerializer, ProductSerializer
│   ├── views.py
│   └── urls.py
└── orders/               
    ├── models.py         # CartItem, Order, OrderItem, UserAddress
    ├── serializers.py    # OrderSerializer, CartItemSerializer, etc.
    ├── views.py
    └── urls.py
```