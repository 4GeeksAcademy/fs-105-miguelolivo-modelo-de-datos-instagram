from eralchemy2 import render_er
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime

db = SQLAlchemy()

# (User)
class User(db.Model):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)

    posts = relationship("Post", backref="user")
    comments = relationship("Comment", backref="user")
    likes = relationship("Like", backref="user")
    followers = relationship("Follower", foreign_keys='Follower.user_to_id', backref="followed")
    following = relationship("Follower", foreign_keys='Follower.user_from_id', backref="follower")

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
        }

# (Post)
class Post(db.Model):
    __tablename__ = "post"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    image_url: Mapped[str] = mapped_column(nullable=False)
    caption: Mapped[str] = mapped_column(String(255), nullable=True)

    comments = relationship("Comment", backref="post")
    likes = relationship("Like", backref="post")

    def serialize(self):
        return {
            "id": self.id,
            "image_url": self.image_url,
            "caption": self.caption,
            "user_id": self.user_id,
        }

# (Comment)
class Comment(db.Model):
    __tablename__ = "comment"

    id: Mapped[int] = mapped_column(primary_key=True)
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    content: Mapped[str] = mapped_column(String(300), nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "content": self.content,
            "post_id": self.post_id,
            "user_id": self.user_id,
        }

# (Like)
class Like(db.Model):
    __tablename__ = "like"

    id: Mapped[int] = mapped_column(primary_key=True)
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))

    def serialize(self):
        return {
            "id": self.id,
            "post_id": self.post_id,
            "user_id": self.user_id,
        }

# (Follower)
class Follower(db.Model):
    __tablename__ = "follower"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_from_id: Mapped[int] = mapped_column(ForeignKey("user.id"))  # quién sigue
    user_to_id: Mapped[int] = mapped_column(ForeignKey("user.id"))    # a quién sigue

    def serialize(self):
        return {
            "id": self.id,
            "user_from_id": self.user_from_id,
            "user_to_id": self.user_to_id,
        }

# ⚠️ Genera el diagrama UML a partir de los modelos
try:
    render_er(db.Model, "diagram.png")
    print("Diagrama generado exitosamente como diagram.png")
except Exception as e:
    print("❌ Error al generar el diagrama")
    print(e)
