"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


import os
from unittest import TestCase

from models import db, User, Message, FollowersFollowee

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

    def test_user_model(self):
        """Does basic model work?"""

        u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        db.session.add(u)
        db.session.commit()

        # User should have no messages & no followers
        self.assertEqual(len(u.messages), 0)
        self.assertEqual(len(u.followers), 0)

    def test_repr(self):
        """tests user repr method works correctly"""

        u = User(
            email="test1@test.com",
            username="testuser1",
            password="HASHED_PASSWORD",
            id=5000
        )

        db.session.add(u)
        db.session.commit()
        self.assertEqual(repr(u), "<User #5000: testuser1, test1@test.com>")

    def test_is_following(self):
        """tests that user1 is following user2"""
        u1 = User(
            email="test1@test.com",
            username="testuser1",
            password="HASHED_PASSWORD",
            id=5100
        )
        db.session.add(u1)

        u2 = User(
            email="test2@test.com",
            username="testuser2",
            password="HASHED_PASSWORD",
            id=5200
        )
        db.session.add(u2)

        follow = FollowersFollowee(followee_id=u1.id,
                                   follower_id=u2.id)

        db.session.add(follow)
        db.commit()

        print('****', u1.followers.id)

        print('****', follow)

        self.assertEqual(User.is_following)

