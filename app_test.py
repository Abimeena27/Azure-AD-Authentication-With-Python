import unittest
from flask import Flask, render_template, request
from flask_testing import TestCase
from app import app, login

class TestApp(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        return app

    def test_index(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('login.html')

    def test_login_invalid_email(self):
        response = self.client.post('/login', data={'Input': 'oveya.kowsisara@gmail.com'})
        # self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed("C:\\Users\\vtknn\\OneDrive\\Desktop\\CAFE-Final\\templates\\error.html")



    def test_login_valid_email(self):
        # Assuming 'valid@example.com' is a valid email in jsuser.user_principal_names
        response = self.client.post('/login', data={'Input': 'pandi@rainbowbutterfly28022004gma.onmicrosoft.com'})
        #self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('C:\\Users\\vtknn\\OneDrive\\Desktop\\CAFE-Final\\templates\\Shopify.html')

if __name__ == '__main__':
    unittest.main()
