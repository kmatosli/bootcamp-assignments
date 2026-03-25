"""
============================================================
File: tests/test_users.py
Purpose: Unit tests for /users endpoints.
Tests: GET all, GET by ID, POST, PUT, DELETE
Includes negative tests for 404 and 409 cases.
============================================================
"""

import unittest
import json
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, db


class TestUsers(unittest.TestCase):

    def setUp(self):
        """Set up test client and fresh database."""
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = app.test_client()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        """Clean up after each test."""
        with app.app_context():
            db.session.remove()
            db.drop_all()

    # ── POST /users ──────────────────────────────────────────

    def test_create_user_success(self):
        """POST /users — create a valid user."""
        response = self.client.post(
            '/users',
            data=json.dumps({
                'name': 'Kathy Matos',
                'email': 'kmatosli@yahoo.com',
                'job_title': 'Senior Operations Analyst',
                'company': 'Acme Financial',
                'address': 'Chicago, IL'
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertEqual(data['name'], 'Kathy Matos')
        self.assertEqual(data['email'], 'kmatosli@yahoo.com')

    def test_create_user_duplicate_email(self):
        """POST /users — duplicate email returns 409."""
        payload = json.dumps({
            'name': 'Kathy Matos',
            'email': 'kmatosli@yahoo.com'
        })
        self.client.post('/users', data=payload,
                         content_type='application/json')
        response = self.client.post('/users', data=payload,
                                    content_type='application/json')
        self.assertEqual(response.status_code, 409)

    def test_create_user_no_data(self):
        """POST /users — no data returns 400."""
        response = self.client.post('/users',
                                    content_type='application/json')
        self.assertEqual(response.status_code, 400)

    # ── GET /users ───────────────────────────────────────────

    def test_get_all_users_empty(self):
        """GET /users — returns empty list when no users."""
        response = self.client.get('/users')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 0)

    def test_get_all_users(self):
        """GET /users — returns all users."""
        self.client.post('/users',
                         data=json.dumps({'name': 'Test', 'email': 'test@test.com'}),
                         content_type='application/json')
        response = self.client.get('/users')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(len(data), 1)

    # ── GET /users/<id> ──────────────────────────────────────

    def test_get_user_by_id_success(self):
        """GET /users/<id> — returns correct user."""
        self.client.post('/users',
                         data=json.dumps({'name': 'Kathy', 'email': 'k@test.com'}),
                         content_type='application/json')
        response = self.client.get('/users/1')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['id'], 1)

    def test_get_user_not_found(self):
        """GET /users/<id> — 404 for nonexistent user."""
        response = self.client.get('/users/999')
        self.assertEqual(response.status_code, 404)

    # ── PUT /users/<id> ──────────────────────────────────────

    def test_update_user_success(self):
        """PUT /users/<id> — updates user fields."""
        self.client.post('/users',
                         data=json.dumps({'name': 'Kathy', 'email': 'k@test.com'}),
                         content_type='application/json')
        response = self.client.put(
            '/users/1',
            data=json.dumps({'job_title': 'Director of Operations'}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['job_title'], 'Director of Operations')

    def test_update_user_not_found(self):
        """PUT /users/<id> — 404 for nonexistent user."""
        response = self.client.put(
            '/users/999',
            data=json.dumps({'name': 'Ghost'}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 404)

    # ── DELETE /users/<id> ───────────────────────────────────

    def test_delete_user_success(self):
        """DELETE /users/<id> — deletes user."""
        self.client.post('/users',
                         data=json.dumps({'name': 'Kathy', 'email': 'k@test.com'}),
                         content_type='application/json')
        response = self.client.delete('/users/1')
        self.assertEqual(response.status_code, 200)
        # Confirm gone
        get_response = self.client.get('/users/1')
        self.assertEqual(get_response.status_code, 404)

    def test_delete_user_not_found(self):
        """DELETE /users/<id> — 404 for nonexistent user."""
        response = self.client.delete('/users/999')
        self.assertEqual(response.status_code, 404)


if __name__ == '__main__':
    unittest.main()
