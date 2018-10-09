from app import app
from models import db, connect_db, Cupcake
import unittest
import json

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes-app-test'

connect_db(app)
db.create_all()


class ApplicationTest(unittest.TestCase):

    def setUp(self):
        """Set up our test client and make a new cupcake for each test to work with"""
        self.client = app.test_client()
        new_cupcake = Cupcake(
            flavor='testing', size='small', rating=10, id=1)
        db.session.add(new_cupcake)
        db.session.commit()

    def tearDown(self):
        """Delete all the cupcakes from the db after each test to start with clean data"""
        Cupcake.query.delete()
        db.session.commit()

    def test_get_cupcakes(self):
        """Test GET route at /cupcakes and make sure it returns json of all
        cupcakes"""

        result = self.client.get('/cupcakes')
        result_obj = result.json
        self.assertEqual(result.status_code, 200)
        self.assertIn('testing', result_obj['response'][0]['flavor'])
        self.assertIn('small', result_obj['response'][0]['size'])

    def test_add_cupcake(self):
        """Test POST route at /cupcakes and make sure it creates a cupcake and returns
        that cupcake instance details as JSON"""

        result = self.client.post(
            '/cupcakes', json=dict(
                id='3',
                flavor='strawberry',
                size='small',
                rating='5'))

        result_obj = result.json
        self.assertEqual(result.status_code, 200)
        self.assertIn('strawberry', result_obj['response']['flavor'])
        self.assertIn('small', result_obj['response']['size'])

    def test_edit_cupcake(self):
        """ Test PATCH route at /cupcakes/<int:cupcake_id> and make sure it update the 
            cupcake and returns that cupcake instance details as JSON
        """

        result = self.client.patch(
            '/cupcakes/1', json=dict(
                flavor='testsuccess',
                size='massive',
                rating='9001'))

        result_obj = result.json
        self.assertEqual(result.status_code, 200)
        self.assertIn('testsuccess', result_obj['response']['flavor'])
        self.assertIn('massive', result_obj['response']['size'])

    def test_delete_cupcake(self):
        """ Test DLETE route at /cupcakes/<int:cupcake_id> and make sure it 
            deletes the cupcake and returns JSON message of 'deleted'
        """

        result = self.client.delete('/cupcakes/1')

        result_obj = result.json
        self.assertEqual(result.status_code, 200)
        self.assertIn('deleted', result_obj['response']['message'])
