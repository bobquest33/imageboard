#!flask/bin/python
import os
import unittest

from config import basedir
from app import app, db
from app.views import generate_tripcode

class TestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test.db')
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_generate_tripcode(self):
        assert "test" == generate_tripcode("test")[0]
        assert "test" == generate_tripcode("test#trip")[0]
        assert "51df83ac21" == generate_tripcode("test#arst")[1]
        assert "51df83ac21" == generate_tripcode("#arst")[1]

if __name__ == '__main__':
    unittest.main()
