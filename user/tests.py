from flask_testing import TestCase
from flask import session

from application import create_app as create_app_base
from application import db
from user.models import User

class UserTest(TestCase):

    # SQLALCHEMY_DATABASE_URI = 'sqlite:////Users/pat/Desktop/flask_demo/test_data.db'
    # TESTING = True

    def create_app(self):
        return create_app_base(
                            SQLALCHEMY_DATABASE_URI = 'sqlite:////Users/pat/Desktop/flask_demo/test_data.db',
                            TESTING = True,
                            WTF_CSRF_ENABLED=False)

    def setUp(self):
        db.create_all()
        self.app_factory = self.create_app()
        self.app = self.app_factory.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def user_dict(self):
        return dict(
            first_name="Pat",
            last_name="Crouse",
            username="pjcrouse",
            email="pat@example.com",
            password="test123",
            confirm="test123"
            )

    def test_register_user(self):
        # basic Registration test
        rv = self.app.post('/register', data=self.user_dict(), follow_redirects=True)

        user_from_db = User.query.filter_by(username=self.user_dict()['username'])
        assert(user_from_db)

    def test_login_user(self):
        #create user
        self.app.post('/register', data=self.user_dict())
        #login user
        rv = self.app.post('/login', data=dict(username=self.user_dict()['username'],
                                                password=self.user_dict()['password']))
        # use context mgmr
        with self.app as c:
            #navigate back to homepage
            rv = c.get('/')
            #ensure session username is set
            assert session.get('username') == self.user_dict()['username']
