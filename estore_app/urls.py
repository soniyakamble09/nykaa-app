from django.urls import path
from estore import settings
from . import views
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home),    
    path('product/<pid>', views.product),
    path('register', views.register),
    path('login', views.user_login),
    path('logout',views.user_logout),
    path('catfilter/<cv>',views.catfilter),
    path('sort/<sv>',views.sort),
    path('range',views.range),
    path('addtocart/<pid>',views.addtocart),
    path('viewcart',views.viewcart),
    path('remove/<cid>',views.remove),
    path('updateqty/<cid>/<qv>',views.updateqty),
    path('placeorder',views.placeorder),
    path('removeorder/<oid>',views.removeorder),
    path('makepayment',views.makepayment),
    path('sendmail',views.sendusermail),    
    path('about', views.about),
    path('contact', views.contact),
    path('thanks', views.thanks),
    path('prodfilter',views.prodfilter)
]

if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)