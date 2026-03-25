"""
============================================================
File: tests/test_cases.py
Purpose: Unit tests for /cases endpoints.
Tests: POST case, GET by user, add/remove contributions,
       get contributions, unsubmitted cases.
Includes negative tests.
============================================================
"""

import unittest
import json
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, db


class TestCases(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = app.test_client()
        with app.app_context():
            db.create_all()
        # Create a user and contribution to work with
        self.client.post('/users',
                         data=json.dumps({'name': 'Kathy', 'email': 'k@test.com'}),
                         content_type='application/json')
        self.client.post('/contributions',
                         data=json.dumps({
                             'product_name': 'Automated reconciliation',
                             'category': 'process',
                             'price': 88.5
                         }),
                         content_type='application/json')

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    # ── POST /cases ──────────────────────────────────────────

    def test_create_case_success(self):
        """POST /cases — creates case for valid user."""
        response = self.client.post(
            '/cases',
            data=json.dumps({'user_id': 1, 'submitted': False}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertEqual(data['user_id'], 1)
        self.assertEqual(data['submitted'], False)

    def test_create_case_invalid_user(self):
        """POST /cases — 404 for nonexistent user."""
        response = self.client.post(
            '/cases',
            data=json.dumps({'user_id': 999}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 404)

    def test_create_case_no_data(self):
        """POST /cases — 400 with no data."""
        response = self.client.post('/cases',
                                    content_type='application/json')
        self.assertEqual(response.status_code, 400)

    # ── GET /cases/user/<id> ─────────────────────────────────

    def test_get_cases_for_user(self):
        """GET /cases/user/<id> — returns user's cases."""
        self.client.post('/cases',
                         data=json.dumps({'user_id': 1}),
                         content_type='application/json')
        response = self.client.get('/cases/user/1')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(len(data), 1)

    def test_get_cases_for_nonexistent_user(self):
        """GET /cases/user/<id> — 404 for nonexistent user."""
        response = self.client.get('/cases/user/999')
        self.assertEqual(response.status_code, 404)

    # ── PUT /cases/<id>/add_contribution/<contrib_id> ────────

    def test_add_contribution_to_case(self):
        """PUT add_contribution — links contribution to case."""
        self.client.post('/cases',
                         data=json.dumps({'user_id': 1}),
                         content_type='application/json')
        response = self.client.put('/cases/1/add_contribution/1')
        self.assertEqual(response.status_code, 200)

    def test_add_contribution_duplicate(self):
        """PUT add_contribution — 409 for duplicate."""
        self.client.post('/cases',
                         data=json.dumps({'user_id': 1}),
                         content_type='application/json')
        self.client.put('/cases/1/add_contribution/1')
        response = self.client.put('/cases/1/add_contribution/1')
        self.assertEqual(response.status_code, 409)

    def test_add_contribution_case_not_found(self):
        """PUT add_contribution — 404 for nonexistent case."""
        response = self.client.put('/cases/999/add_contribution/1')
        self.assertEqual(response.status_code, 404)

    def test_add_contribution_contrib_not_found(self):
        """PUT add_contribution — 404 for nonexistent contribution."""
        self.client.post('/cases',
                         data=json.dumps({'user_id': 1}),
                         content_type='application/json')
        response = self.client.put('/cases/1/add_contribution/999')
        self.assertEqual(response.status_code, 404)

    # ── GET /cases/<id>/contributions ────────────────────────

    def test_get_contributions_for_case(self):
        """GET /cases/<id>/contributions — returns case contributions."""
        self.client.post('/cases',
                         data=json.dumps({'user_id': 1}),
                         content_type='application/json')
        self.client.put('/cases/1/add_contribution/1')
        response = self.client.get('/cases/1/contributions')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(len(data), 1)

    def test_get_contributions_case_not_found(self):
        """GET /cases/<id>/contributions — 404 for nonexistent case."""
        response = self.client.get('/cases/999/contributions')
        self.assertEqual(response.status_code, 404)

    # ── DELETE /cases/<id>/remove_contribution/<contrib_id> ──

    def test_remove_contribution_from_case(self):
        """DELETE remove_contribution — unlinks contribution."""
        self.client.post('/cases',
                         data=json.dumps({'user_id': 1}),
                         content_type='application/json')
        self.client.put('/cases/1/add_contribution/1')
        response = self.client.delete('/cases/1/remove_contribution/1')
        self.assertEqual(response.status_code, 200)

    def test_remove_contribution_not_in_case(self):
        """DELETE remove_contribution — 404 when not in case."""
        self.client.post('/cases',
                         data=json.dumps({'user_id': 1}),
                         content_type='application/json')
        response = self.client.delete('/cases/1/remove_contribution/1')
        self.assertEqual(response.status_code, 404)

    # ── GET /cases/unsubmitted ───────────────────────────────

    def test_get_unsubmitted_cases(self):
        """GET /cases/unsubmitted — returns unsubmitted cases."""
        self.client.post('/cases',
                         data=json.dumps({'user_id': 1, 'submitted': False}),
                         content_type='application/json')
        self.client.post('/cases',
                         data=json.dumps({'user_id': 1, 'submitted': True}),
                         content_type='application/json')
        response = self.client.get('/cases/unsubmitted')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['submitted'], False)


if __name__ == '__main__':
    unittest.main()
