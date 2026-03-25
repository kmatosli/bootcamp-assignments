"""
============================================================
File: tests/test_contributions.py
Purpose: Unit tests for /contributions endpoints.
Tests: GET all, GET by ID, POST, PUT, DELETE
Includes negative tests for 404 cases.
============================================================
"""

import unittest
import json
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, db


class TestContributions(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = app.test_client()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def _create_contribution(self, name='Test Contribution',
                              category='process', price=88.5):
        return self.client.post(
            '/contributions',
            data=json.dumps({
                'product_name': name,
                'category': category,
                'price': price,
                'description': 'Test description'
            }),
            content_type='application/json'
        )

    # ── POST /contributions ──────────────────────────────────

    def test_create_contribution_success(self):
        """POST /contributions — creates valid contribution."""
        response = self._create_contribution(
            'Automated monthly reconciliation', 'process', 88.5
        )
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertEqual(data['product_name'], 'Automated monthly reconciliation')
        self.assertEqual(data['category'], 'process')
        self.assertEqual(data['price'], 88.5)

    def test_create_contribution_no_data(self):
        """POST /contributions — 400 with no data."""
        response = self.client.post('/contributions',
                                    content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_create_contribution_revenue_category(self):
        """POST /contributions — revenue category accepted."""
        response = self._create_contribution(
            'Closed Q3 enterprise deal', 'revenue', 96.0
        )
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertEqual(data['category'], 'revenue')

    # ── GET /contributions ───────────────────────────────────

    def test_get_all_contributions_empty(self):
        """GET /contributions — empty list when none exist."""
        response = self.client.get('/contributions')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data), [])

    def test_get_all_contributions(self):
        """GET /contributions — returns all contributions."""
        self._create_contribution('Contribution 1')
        self._create_contribution('Contribution 2', 'revenue', 95.0)
        response = self.client.get('/contributions')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(len(data), 2)

    # ── GET /contributions/<id> ──────────────────────────────

    def test_get_contribution_by_id(self):
        """GET /contributions/<id> — returns correct contribution."""
        self._create_contribution('Target Contribution')
        response = self.client.get('/contributions/1')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['product_name'], 'Target Contribution')

    def test_get_contribution_not_found(self):
        """GET /contributions/<id> — 404 for nonexistent."""
        response = self.client.get('/contributions/999')
        self.assertEqual(response.status_code, 404)

    # ── PUT /contributions/<id> ──────────────────────────────

    def test_update_contribution_success(self):
        """PUT /contributions/<id> — updates impact score."""
        self._create_contribution('Update Test', 'process', 70.0)
        response = self.client.put(
            '/contributions/1',
            data=json.dumps({'price': 85.0}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['price'], 85.0)

    def test_update_contribution_not_found(self):
        """PUT /contributions/<id> — 404 for nonexistent."""
        response = self.client.put(
            '/contributions/999',
            data=json.dumps({'price': 90.0}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 404)

    # ── DELETE /contributions/<id> ───────────────────────────

    def test_delete_contribution_success(self):
        """DELETE /contributions/<id> — deletes contribution."""
        self._create_contribution()
        response = self.client.delete('/contributions/1')
        self.assertEqual(response.status_code, 200)
        get_response = self.client.get('/contributions/1')
        self.assertEqual(get_response.status_code, 404)

    def test_delete_contribution_not_found(self):
        """DELETE /contributions/<id> — 404 for nonexistent."""
        response = self.client.delete('/contributions/999')
        self.assertEqual(response.status_code, 404)


if __name__ == '__main__':
    unittest.main()
