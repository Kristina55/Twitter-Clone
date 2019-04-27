"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


import os
from unittest import TestCase

from models import db, User, Message, FollowersFollowee, Like
from sqlalchemy.exc import IntegrityError as ie, InvalidRequestError

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"


# Now we can import app

from app import app

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()


class UserModelTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Message.query.delete()
        FollowersFollowee.query.delete()

        self.client = app.test_client()        

    def test_message_model(self):
        """Does basic model work?"""

        u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD",
            id=6000
        )

        db.session.add(u)
        db.session.commit()

        m = Message(text="Happy Friday", user_id=u.id)
        db.session.add(m)
        db.session.commit()

        # User should have one messages
        self.assertEqual(len(u.messages), 1)
        self.assertNotEqual(len(u.messages), [])
    
    def test_author(self):
        """ user1 wrote message 1"""
        u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD",
            id=7000
        )
        db.session.add(u)
        db.session.commit()

        m = Message(
            text="Happy Friday", user_id=u.id
        )

        db.session.add(m)
        db.session.commit()

        self.assertEqual(m.user_id, 7000)


    def test_not_author(self):
        """ user1 did not write message 1"""
        u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD",
            id=7000
        )
        db.session.add(u)


        author = User(
            email="test1@test.com",
            username="test1user",
            password="HASHED_PASSWORD",
            id=700
        )
        db.session.add(author)
        db.session.commit()

        m = Message(
            text="Happy Friday", user_id=700
        )

        db.session.add(m)
        db.session.commit()

        self.assertNotEqual(m.user_id, 7000)
        self.assertEqual(m.user_id, 700)

    def test_liked_message(self):
        u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD",
            id=9000
        )
        db.session.add(u)
        db.session.commit()

        m = Message(
            text="Happy Friday", user_id=u.id
        )

        db.session.add(m)
        db.session.commit()

        l = Like(
            user_id=u.id,
            message_id=m.id
        )

        db.session.add(l)
        db.session.commit()
        self.assertEqual(m.liked_messages[0].id, 9000)

