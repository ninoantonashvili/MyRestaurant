from django.urls import path
from .views import AddToBasketView, BasketDetailView, BasketListView, CategoryListView, DishDetailView, DishFilterView, DishListView, RemoveFromBasketView

urlpatterns = [
    path('baskets/<int:pk>/', BasketDetailView.as_view(), name='basket-detail'),
    path('baskets/', BasketListView.as_view(), name='basket-list'), 
    # path('baskets/', CreateBasketView.as_view(), name='basket-add'),  

    path('baskets/<int:basket_id>/add/', AddToBasketView.as_view(), name='add-to-basket'),
    path('baskets/<int:basket_id>/remove/', RemoveFromBasketView.as_view(), name='remove-from-basket'),

    path('dishes/', DishListView.as_view(), name='dish-list'),
    path('dishes/<int:pk>/', DishDetailView.as_view(), name='dish-detail'),
    path('dishes/filter/', DishFilterView.as_view(), name='dish-filter'),

    path('categories/', CategoryListView.as_view(), name='category-list'),
]
