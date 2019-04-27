"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


import os
from unittest import TestCase

from models import db, User, Message, FollowersFollowee
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
            email="test7@test.com",
            username="testuser1",
            password="HASHED_PASSWORD",
            id=5100
        )
        
        db.session.add(u1)

        u2 = User(
            email="test8@test.com",
            username="testuser2",
            password="HASHED_PASSWORD",
            id=5200
        )
        db.session.add(u2)
        db.session.commit()

        follow = FollowersFollowee(followee_id=u1.id,
                                   follower_id=u2.id)
        
        db.session.add(follow)
        db.session.commit()


        self.assertEqual(u1.following[0].id, 5200)
        self.assertEqual(str(u1.following), "[<User #5200: testuser2, test8@test.com>]")


    def test_is_not_following(self):
        """tests that user1 is not following user2"""

        u1 = User(
            email="test90@test.com",
            username="testuser1",
            password="HASHED_PASSWORD",
            id=5300
        )
        
        db.session.add(u1)

        u2 = User(
            email="test80@test.com",
            username="testuser2",
            password="HASHED_PASSWORD",
            id=5400
        )
        db.session.add(u2)
        db.session.commit()

        self.assertEqual(u1.following, [])


    def test_is_followed_by(self):
        """ test that user1 is followed by user2 """


        u1 = User(
            email="test45@test.com",
            username="testuser1",
            password="HASHED_PASSWORD",
            id=5700
        )
        
        db.session.add(u1)

        u2 = User(
            email="test20@test.com",
            username="testuser2",
            password="HASHED_PASSWORD",
            id=5800
        )
        db.session.add(u2)
        db.session.commit()

        follow = FollowersFollowee(followee_id=u1.id,
                                   follower_id=u2.id)
        
        db.session.add(follow)
        db.session.commit()

        self.assertEqual(u2.followers[0].id, 5700)
        self.assertEqual(str(u2.followers), "[<User #5700: testuser1, test45@test.com>]")

    def test_is_not_followed_by(self):
        """tests that user1 is not followed by user2"""

        u1 = User(
            email="test10@test.com",
            username="testuser1",
            password="HASHED_PASSWORD",
            id=5300
        )
        
        db.session.add(u1)

        u2 = User(
            email="test2@test.com",
            username="testuser2",
            password="HASHED_PASSWORD",
            id=5400
        )
        db.session.add(u2)
        db.session.commit()

        self.assertEqual(u2.followers, [])


    def test_create_new_user(self):
        """ test if signup() successfully create a new user given valid credentials and redirect to the home page"""

        self.client = app.test_client()
        result = self.client.post("/signup",
                data={'username':'Haley',
                      'email': 'test5@gmail.com',
                      'password': 'test',
                      'image_url': 'https://upload.wikimedia.org/wikipedia/commons/2/2f/Pied-winged_swallow_%28Hirundo_leucosoma%29.jpg'})
   
        test_user = User.signup(username="Kitty",   
                                     email="test2@gmail.com",
                                     password="test1",
                                     image_url="https://upload.wikimedia.org/wikipedia/commons/2/2f/Pied-winged_swallow_%28Hirundo_leucosoma%29.jpg")


        

        db.session.add(test_user)
        db.session.commit()
        test_username = User.query.order_by(User.username).first().username
        test_email = User.query.filter_by(username='Kitty').first().email

        self.assertEqual(result.status_code, 200)
        self.assertEqual(test_user.username, 'Kitty')
        self.assertEqual(str(test_username), "Kitty")
        self.assertEqual(str(test_email), "test2@gmail.com")

    def test_fail_to_create_user(self):
        """ test if signup() fail to create a new user if any of the validations fail"""
        test_user1 = User.signup(username="Kristina",
                                 email="test1@gmail.com",
                                 password="test1",
                                 image_url="https://upload.wikimedia.org/wikipedia/commons/2/2f/Pied-winged_swallow_%28Hirundo_leucosoma%29.jpg")
        db.session.add(test_user1)
        db.session.commit()

        test_user2 = User.signup(username="Kristina",
                                email="test1@gmail.com",
                                password="test1",
                                image_url="https://upload.wikimedia.org/wikipedia/commons/2/2f/Pied-winged_swallow_%28Hirundo_leucosoma%29.jpg")

        with self.assertRaises(ie):
            db.session.add(test_user2)
            db.session.commit()
        
        db.session.rollback()

        self.assertEqual(len(User.query.all()), 1)

    def test_user_authenticate(self):
        """ successfully returns a user when given a valid username and password """
        test_user = User.signup(username="Kristina",
                                 email="test1@gmail.com",
                                 password="test1",
                                 image_url="https://upload.wikimedia.org/wikipedia/commons/2/2f/Pied-winged_swallow_%28Hirundo_leucosoma%29.jpg")
        db.session.add(test_user)
        db.session.commit()

        test_login = User.authenticate(username="Kristina",
                                password="test1")

        self.assertTrue(test_login)
    
    def test_wrong_username(self):
        """ fails to return a user when the username is invalid """
        test_user = User.signup(username="Kristina",
                                 email="test1@gmail.com",
                                 password="test1",
                                 image_url="https://upload.wikimedia.org/wikipedia/commons/2/2f/Pied-winged_swallow_%28Hirundo_leucosoma%29.jpg")
        db.session.add(test_user)
        db.session.commit()

        test_login = User.authenticate(username="Buffy", password="test1")
    
        self.assertFalse(test_login)

    def test_wrong_password(self):
        """ fails to return a user when the username is invalid """
        test_user = User.signup(username="Kristina",
                                email="test1@gmail.com",
                                password="test1",
                                image_url="https://upload.wikimedia.org/wikipedia/commons/2/2f/Pied-winged_swallow_%28Hirundo_leucosoma%29.jpg")
        db.session.add(test_user)
        db.session.commit()

        test_login = User.authenticate(username="Kristina", password="kitty")

        self.assertFalse(test_login)
        
