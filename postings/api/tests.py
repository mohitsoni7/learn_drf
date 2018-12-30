from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from postings.models import BlogPost
from rest_framework.reverse import reverse as api_reverse
from rest_framework_jwt.settings import api_settings

payload_handler = api_settings.JWT_PAYLOAD_HANDLER
encode_handler = api_settings.JWT_ENCODE_HANDLER


# These tests are automated
# These tests are done on a blank DB


User = get_user_model()

class BlogPostAPITestCase(APITestCase):
    def setUp(self):
        user_obj = User(username='testUser', email='testuser@yopmail.com')
        user_obj.set_password('testPassword')
        user_obj.save()
        blog_post = BlogPost.objects.create(
            user=user_obj,
            title='Test Blog title',
            content='Test Blog content',
        )


    def test_single_user(self):
        """ User creation test """
        user_count = User.objects.count()
        self.assertEqual(user_count, 1)

    def test_single_post(self):
        """ Blog post creation test """
        post_count = BlogPost.objects.count()
        self.assertEqual(post_count, 1)
    
    def test_get_list(self):
        """ Get the list of objects test """
        data = {}
        url = api_reverse('api-postings:create-list-search')
        response = self.client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_item(self):
        """ Save some random post test """
        data = {'title': 'Random Title', 'content': 'This is some random content'}
        url = api_reverse('api-postings:create-list-search')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_item(self):
        """ Get the first item """
        blog_post = BlogPost.objects.first()
        data = {}
        url = blog_post.get_api_url()
        response = self.client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # print(response.data)
    
    def test_update_item(self):
        """ Update the first item """
        blog_post = BlogPost.objects.first()
        data = {
            'title': 'Updated title',
            'content': 'Updated content',
        }
        url = blog_post.get_api_url()
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        # print(response)

    def test_update_item_with_user(self):
        """ Update the first item """
        blog_post = BlogPost.objects.first()
        # print(blog_post.title)
        # print(blog_post.content)
        data = {
            'title': 'Updated title',
            'content': 'Updated content',
        }
        url = blog_post.get_api_url()

        user_obj = User.objects.first()

        payload = payload_handler(user_obj)
        token_response = encode_handler(payload)
        # print('*********************')
        # print(payload)
        # print(token_response)
        # print('*********************')

        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token_response) # Set a header for token

        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # print(response.data)
    
    def test_create_item_with_user(self):
        """ Update the first item """
        user_obj = User.objects.first()
        payload = payload_handler(user_obj)
        token_response = encode_handler(payload)
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token_response)
        data = {
            'title': 'Updated title',
            'content': 'Updated content',
        }
        url = api_reverse('api-postings:create-list-search')

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_user_ownership(self):
        owner = User.objects.create(username='newUser', email='newUser@yomail.com')
        owner.set_password('newUserPassword')
        owner.save()
        blog_post = BlogPost.objects.create(
            user=owner,
            title='Test Blog title',
            content='Test Blog content',
        )

        url = blog_post.get_api_url()

        user_obj = User.objects.first()
        self.assertNotEqual(user_obj.username, owner.username)
        payload = payload_handler(user_obj)
        token_response = encode_handler(payload)

        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token_response)

        data = {
            'title': 'Updated title',
            'content': 'Updated content',
        }

        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    def test_user_login(self):
        data = {
            'username': 'testUser',
            'password': 'testPassword',
        }
        url = api_reverse('api-login')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(response.data)
    
    def test_user_login_and_update(self):
        data = {
            'username': 'testUser',
            'password': 'testPassword',
        }
        url = api_reverse('api-login')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        token = response.data.get('token')
        if token is not None:
            blog_post = BlogPost.objects.first()
            print(blog_post.content)
            url = blog_post.get_api_url()
            data = {
            'title': 'Updated title',
            'content': 'Updated content',
            }
            self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
            response = self.client.put(url, data, format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            print(response.data.get('content'))

