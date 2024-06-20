
from requests import Response
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Basket, BasketItem, Category, Dish
from .serializers import AddBasketItemSerializer, BasketSerializer, CategorySerializer, DishFilterSerializer, DishSerializer, RemoveBasketItemSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class BasketDetailView(generics.RetrieveAPIView):
    queryset = Basket.objects.all()
    serializer_class = BasketSerializer

class BasketListView(generics.ListCreateAPIView):
    queryset = Basket.objects.all()
    serializer_class = BasketSerializer

class AddToBasketView(APIView):
    @swagger_auto_schema(
        operation_description="Add a dish to the basket",
        request_body=AddBasketItemSerializer,
        responses={
            200: BasketSerializer,
            400: "Bad Request",
            404: "Not Found"
        }
    )
    def post(self, request, basket_id):
        print("Request data:", request.data)  # Debugging statement
        serializer = AddBasketItemSerializer(data=request.data)
        if serializer.is_valid():
            dish_id = serializer.validated_data['dish_id']
            count = serializer.validated_data['count']
            try:
                basket = Basket.objects.get(id=basket_id)
            except Basket.DoesNotExist:
                return Response({'error': 'Basket does not exist.'}, status=status.HTTP_404_NOT_FOUND)
            
            dish = Dish.objects.get(id=dish_id)
            basket_item, created = BasketItem.objects.get_or_create(dish=dish, itemCount=count)
            
            if not created:
                basket_item.itemCount += count
                basket_item.save()
            
            basket.items.add(basket_item)
            basket.total_price += dish.price * count
            basket.save()
            
            return Response(BasketSerializer(basket).data, status=status.HTTP_200_OK)
        
        print("Serializer errors:", serializer.errors)  # Debugging statement
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class RemoveFromBasketView(APIView):
    @swagger_auto_schema(
        operation_description="remove dish from the basket",
        request_body=RemoveBasketItemSerializer
    )
    def post(self, request, basket_id):
        serializer = RemoveBasketItemSerializer(data=request.data)
        if serializer.is_valid():
            dish_id = serializer.validated_data['dish_id']
            item_count_to_delete = serializer.validated_data['item_count_to_delete']
            
            try:
                basket = Basket.objects.get(id=basket_id)
            except Basket.DoesNotExist:
                return Response({'error': 'Basket does not exist.'}, status=status.HTTP_404_NOT_FOUND)
            
            try:
                dish = Dish.objects.get(id=dish_id)
            except Dish.DoesNotExist:
                return Response({'error': 'Dish does not exist.'}, status=status.HTTP_404_NOT_FOUND)
            
            try:
                basket_item = BasketItem.objects.get(basket=basket, dish=dish)
            except BasketItem.DoesNotExist:
                return Response({'error': 'Basket item does not exist.'}, status=status.HTTP_404_NOT_FOUND)
            
            if basket_item.itemCount < item_count_to_delete:
                return Response({'error': 'Item count to delete exceeds available count.'}, status=status.HTTP_400_BAD_REQUEST)
            
            basket.total_price -= dish.price * item_count_to_delete
            basket.total_price = max(basket.total_price, 0)  # Ensure total_price doesn't go below zero
            
            if basket_item.itemCount == item_count_to_delete:
                basket.items.remove(basket_item)
                basket_item.delete()
            else:
                basket_item.itemCount -= item_count_to_delete
                basket_item.save()
            
            basket.save()
            
            return Response(BasketSerializer(basket).data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class DishListView(generics.ListCreateAPIView):
    queryset = Dish.objects.all()
    serializer_class = DishSerializer

class DishDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Dish.objects.all()
    serializer_class = DishSerializer


class DishFilterView(generics.ListAPIView):
    queryset = Dish.objects.all()
    serializer_class = DishSerializer
    filter_backends = []  
    filterset_class = None  

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('name', openapi.IN_QUERY, description="Filter dishes by name (case insensitive)", type=openapi.TYPE_STRING),
            openapi.Parameter('spicy', openapi.IN_QUERY, description="Filter dishes by spiciness level (0-4)", type=openapi.TYPE_INTEGER),
            openapi.Parameter('withNut', openapi.IN_QUERY, description="Filter dishes whether they contain nuts or not", type=openapi.TYPE_BOOLEAN),
            openapi.Parameter('isVegetarian', openapi.IN_QUERY, description="Filter dishes whether they are vegetarian or not", type=openapi.TYPE_BOOLEAN),
            openapi.Parameter('category', openapi.IN_QUERY, description="Filter dishes by category", type=openapi.TYPE_INTEGER),
        ]
    )
    def get(self, request, *args, **kwargs):
        serializer = DishFilterSerializer(data=request.query_params)
        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            spicy = serializer.validated_data.get('spicy')
            withNut = serializer.validated_data.get('withNut')
            isVegetarian = serializer.validated_data.get('isVegetarian')
            category = serializer.validated_data.get('category')

            queryset = self.get_queryset()
            if name:
                queryset = queryset.filter(name__icontains=name)
            if spicy is not None:
                queryset = queryset.filter(spicy=spicy)
            if withNut is not None:
                queryset = queryset.filter(withNut=withNut)
            if isVegetarian is not None:
                queryset = queryset.filter(isVegetarian=isVegetarian)
            if category:
                queryset = queryset.filter(category=category)

            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)\
            
class CategoryListView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
