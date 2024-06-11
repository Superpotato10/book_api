from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, APIClient

from books.models import Author, Book, Publisher, Genre
from orders.models import Order, OrderItem
from orders.serializers.order_serializer import ReadOrderSerializer

UserModel = get_user_model()


class OrderAPITest(APITestCase):
    url = '/api/orders/'

    def create_user(self, username, password='password', is_manager=False):
        user = UserModel.objects.create(username=username, password=password, is_manager=is_manager)
        token = Token.objects.create(user=user)
        client = APIClient(HTTP_AUTHORIZATION='Token ' + token.key)
        return (user, client)

    def create_book(self, author, publisher, genre):
        book = Book.objects.create(title=f'Book {author.name}',
                                   publication_date='1992-03-05',
                                   author=author,
                                   publisher=publisher,
                                   pages=100,
                                   price=1000)

        book.genres.set(genre)
        return book

    def setUp(self):
        self.anonymous = (None, APIClient())
        self.standard = self.create_user(username='standard')
        self.manager = self.create_user(username='manager', is_manager=True)

        self.authors = [
            Author.objects.create(name='Author #1', birth_date='1990-01-01'),
            Author.objects.create(name='Author #2', birth_date='1991-02-04'),
            Author.objects.create(name='Author #3', birth_date='1992-03-05'),
        ]

        self.publishers = [
            Publisher.objects.create(name='Publisher #1', is_active=True, category=Publisher.Category.GENERAL),
            Publisher.objects.create(name='Publisher #2', is_active=True, category=Publisher.Category.EDUCATIONAL),
            Publisher.objects.create(name='Publisher #3', is_active=True, category=Publisher.Category.SCIENCE),
        ]

        genre = Genre.objects.create(name='Horror')

        self.books = [self.create_book(author, publisher, [genre])
                      for (author, publisher) in zip(self.authors, self.publishers)]

        (user, _) = self.standard

        self.orders = [
            Order.objects.create(address='Address #1', status=Order.Status.PENDING, user=user),
            Order.objects.create(address='Address #2', status=Order.Status.DELIVERED, user=user),
            Order.objects.create(address='Address #3', status=Order.Status.SHIPPED, user=user),
        ]

        for order_i in range(len(self.orders)):
            order = self.orders[order_i]
            OrderItem.objects.create(order=order, book=self.books[order_i], quantity=1, user=user)

    def test_order_list(self):
        (_, anonymous) = self.anonymous
        anonymous_response = anonymous.get(self.url)
        self.assertEqual(anonymous_response.status_code, status.HTTP_401_UNAUTHORIZED)

        (_, standard) = self.standard
        client_response = standard.get(self.url)
        self.assertEqual(client_response.status_code, status.HTTP_200_OK)

        (_, manager) = self.manager
        manager_response = manager.get(self.url)
        self.assertEqual(manager_response.status_code, status.HTTP_200_OK)

        comparing_data = manager_response.data['results']
        expected_data = ReadOrderSerializer(self.orders, many=True).data
        self.assertEqual(comparing_data, expected_data)

    def test_order_detail(self):
        order = self.orders[0]

        (_, anonymous) = self.anonymous
        anonymous_response = anonymous.get(f'{self.url}{order.id}/')
        self.assertEqual(anonymous_response.status_code, status.HTTP_401_UNAUTHORIZED)

        (_, standard) = self.standard
        client_response = standard.get(f'{self.url}{order.id}/')
        self.assertEqual(client_response.status_code, status.HTTP_200_OK)

        (_, manager) = self.manager
        manager_response = manager.get(f'{self.url}{order.id}/')
        self.assertEqual(manager_response.status_code, status.HTTP_200_OK)

        comparing_data = manager_response.data
        expected_data = ReadOrderSerializer(order).data

        self.assertEqual(comparing_data, expected_data)

    def test_order_create(self):
        new_order = {
            'address': 'test address',
            'items': [
                {'book': self.books[0].id, 'quantity': 10},
                {'book': self.books[1].id, 'quantity': 1},
            ]
        }

        (_, anonymous) = self.anonymous
        anonymous_response = anonymous.post(self.url, new_order, format='json')
        self.assertEqual(anonymous_response.status_code, status.HTTP_401_UNAUTHORIZED)

        (_, standard) = self.standard
        client_response = standard.post(self.url, data=new_order, format='json')
        self.assertEqual(client_response.status_code, status.HTTP_201_CREATED)

        order_id = client_response.data['id']
        existed_order = Order.objects.get(id=order_id)

        self.assertIsNotNone(existed_order)

    def test_delete_order(self):
        order = self.orders[0]

        (_, anonymous) = self.anonymous
        anonymous_response = anonymous.delete(f'{self.url}{order.id}/')
        self.assertEqual(anonymous_response.status_code, status.HTTP_401_UNAUTHORIZED)

        (_, standard) = self.standard
        client_response = standard.delete(f'{self.url}{order.id}/')
        self.assertEqual(client_response.status_code, status.HTTP_403_FORBIDDEN)

        (_, manager) = self.manager
        manager_response = manager.delete(f'{self.url}{order.id}/')
        self.assertEqual(manager_response.status_code, status.HTTP_204_NO_CONTENT)

        existed_order = Order.objects.filter(id=order.id).first()
        self.assertIsNone(existed_order)
