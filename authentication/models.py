from django.db import models

# Create your models here.
"""
class User(models.Model):
    username = models.CharField(max_length=50)
    email = db.Column(db.String(120),index=True,unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    about_me=db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default = datetime.utcnow)
    def __repr__(self):
        return '<User '+self.username+'>'
    def set_password(self,password):
        self.password_hash=generate_password_hash(password)
    def check_password(self,password):
        return check_password_hash(self.password_hash,password)
    def avatar(self,size):
        digest = md5(self.email.lower().encode("utf-8")).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest,size)
"""
