from django.urls import path
<<<<<<< HEAD
from .views import *

urlpatterns = [
    path('', index, name='home'),
    path('cats/<int:catid>/', categories)
]
=======
from django.urls import path, include
from .views import *

urlpatterns = [
path('', index, name='home'),
path('about/', about, name='about'),
path('addpage/', addpage, name='addpage'),
path('contact/', contact, name='contact'),
path('login/', login, name='login'),
path('category/<int:cat_id>/', show_category, name='category'),

# path('cat/<slug:catid>/', categories),
]
>>>>>>> 1860828192de2b003f031cabe0dad3d55f782c34
