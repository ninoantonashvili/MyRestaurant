from rest_framework import serializers
from .models import Category, Dish, BasketItem, Basket

class BasketItemSerializer(serializers.ModelSerializer):
    dishId = serializers.IntegerField(source='dish.id')
    count = serializers.IntegerField(source='itemCount')

    class Meta:
        model = BasketItem
        fields = ['dishId', 'count']

class BasketSerializer(serializers.ModelSerializer):
    items = BasketItemSerializer(many=True, read_only=True, source='items.all')
    total_price = serializers.ReadOnlyField()
    class Meta:
        model = Basket
        fields = ['id', 'total_price', 'items']

class AddBasketItemSerializer(serializers.Serializer):
    dish_id = serializers.IntegerField()
    count = serializers.IntegerField()

    def validate_dish_id(self, value):
        if not Dish.objects.filter(id=value).exists():
            raise serializers.ValidationError("Dish does not exist.")
        return value

class RemoveBasketItemSerializer(serializers.Serializer):
    dish_id = serializers.IntegerField()
    item_count_to_delete = serializers.IntegerField(min_value=1)

class DishSerializer(serializers.ModelSerializer):
    imageUrl = serializers.CharField(required=False)
    class Meta:
        model = Dish
        fields = '__all__'

class DishFilterSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100, required=False)
    spicy = serializers.IntegerField(min_value=0, max_value=4, required=False)
    withNut = serializers.BooleanField(required=False)
    isVegetarian = serializers.BooleanField(required=False)
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), required=False)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
