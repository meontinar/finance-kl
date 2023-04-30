from django.urls import path
from django.views.decorators.cache import cache_page
from .views import *

urlpatterns = [
    # path('api/v1/courselist/', CourseViewSet.as_view({'get': 'list'})),
    path('', CourseHome.as_view(), name='home'),
    path('courses/', Courses.as_view(), name='courses'),
    path('programs/', CourseHome.as_view(), name='pricing'),
    path('category/<slug:cat_slug>/', CourseCategory.as_view(), name='category'),
    path('course/<slug:cour_slug>/', ShowCourse.as_view(), name='course'),
    path('about/', about, name='about'),
    path('addcourse/', AddCourse.as_view(), name='add_course'),
    path('contact/', ContactFormView.as_view(), name='contact'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('register/', RegisterUser.as_view(), name='register'),
]