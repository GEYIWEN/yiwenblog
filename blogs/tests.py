from django.test import TestCase
from django.urls import resolve, reverse
from blogs.views import cv,blog_detail
# Create your tests here.

class URLTest(TestCase):

    #To test the url address of resume page
      def test_resolve_url_to_cv_test(self):
        find = resolve('/cv')
        self.assertEqual(find.func,cv)

    #To test the url address of blog detail page which I can update my project experience at any time through the form in the background
      def test_resolve_url_to_blog_detail_test(self):
         find = resolve('/blog/3/')
         self.assertEqual(find.func,blog_detail)
