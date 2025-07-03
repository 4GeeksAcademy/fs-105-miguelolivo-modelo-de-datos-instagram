from eralchemy2 import render_er
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship


db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # sin contraseña por seguridad
        }

# (Post)


class Post(db.Model):
    __tablename__ = "post"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("user.id"))  # conexión con usuario
    image_url: Mapped[str] = mapped_column(nullable=False)  # URL de la imagen
    caption: Mapped[str] = mapped_column(
        String(255), nullable=True)  # descripción opcional

    #  Relation User
    user = relationship("User", backref="posts")

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
    post_id: Mapped[int] = mapped_column(
        ForeignKey("post.id"))  # a qué post comenta
    user_id: Mapped[int] = mapped_column(
        ForeignKey("user.id"))  # quién comenta
    content: Mapped[str] = mapped_column(
        String(300), nullable=False)  # contenido del comentario

    # relation User y Post
    user = relationship("User", backref="comments")
    post = relationship("Post", backref="comments")

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
    post_id: Mapped[int] = mapped_column(
        ForeignKey("post.id"))  # qué post le gusta
    user_id: Mapped[int] = mapped_column(
        ForeignKey("user.id"))  # quién dio el like

    # Relation User y Post
    user = relationship("User", backref="likes")
    post = relationship("Post", backref="likes")

    def serialize(self):
        return {
            "id": self.id,
            "post_id": self.post_id,
            "user_id": self.user_id,
        }


# ⚠️ Genera el diagrama UML a partir de los modelos
try:
    render_er(db.Model, "diagram.png")
    print("✅ Diagrama generado exitosamente como diagram.png")
except Exception as e:
    print("❌ Error al generar el diagrama")
    print(e)
