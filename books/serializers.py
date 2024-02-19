from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Book

class BookSerializer(serializers.ModelSerializer):

    class Meta:
        model = Book
        fields = ('id', 'title', 'subtitle', 'content', 'author', 'isbn', 'price',)

    def validate(self, data):
        title = data.get('title', None)
        author = data.get('author', None)

        # sarlovha faqat harflardan tashkil topganligini tekshiradi.
        if not title.isalpha():
            raise ValidationError({
                'status': False,
                'message': "Kitob sarlovhasi harflardan tashkil topgan bo'lishi kerak!"
            })

        # sarlovha va muallif ma'lumotlar bazasida borligini tekshiradi
        if Book.objects.filter(title=title, author=author).exists():
            raise ValidationError({
                'status': False,
                'message': "Kitob ma'lumotlar bazasida mavjud"
            })

        return data

    def validate_price(self, price):
        if price < 0 or price > 9999999999:
            raise ValidationError({
                'status': False,
                'message': "Kitob narxi noto'g'ri kiritilgan"
            })
