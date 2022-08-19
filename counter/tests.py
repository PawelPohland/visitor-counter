from utils.test_db import TestDB
from application import create_app as create_app_base
from application import db

import os
import unittest
import pathlib

from dotenv import load_dotenv
env_dir = pathlib.Path(__file__).parents[1]
load_dotenv(os.path.join(env_dir, '.flaskenv'))


class CounterTest(unittest.TestCase):
    def create_app(self):
        return create_app_base(SQLALCHEMY_DATABASE_URI=self.db_uri, TESTING=True, SECRET_KEY="mySecret!")

    def setUp(self):
        self.test_db = TestDB()
        self.db_uri = self.test_db.create_db()
        self.app_factory = self.create_app()
        self.app = self.app_factory.test_client()

        with self.app_factory.app_context():
            db.create_all()

    def tearDown(self):
        with self.app_factory.app_context():
            db.drop_all()

        self.test_db.drop_db()

    def test_counter(self):
        rv = self.app.get("/")
        assert "1" in str(rv.data)

        rv = self.app.get("/")
        assert "2" in str(rv.data)
