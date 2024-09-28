from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create/",views.create,name="create"),
    path("<int:id>/",views.product,name="product"),
    path("sorted/",views.category,name="category"),
    path("remove/<int:id>",views.removewatchlist,name="remove"),
    path("add/<int:id>",views.addwatchlist,name="add"),
    path("watchlist/",views.watchlist,name='watchlist'),
    path("watchlistcategory/",views.Watchcategory,name="watchcategory"),
    path("comments/<int:id>",views.user_comment,name="comment"),
    path("bid/<int:id>",views.biding,name="bid"),
    path("close/<int:id>",views.close,name="close"),
]
