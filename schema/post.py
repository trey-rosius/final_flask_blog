from ma import ma
from models.post import PostModel


class PostSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = PostModel
        include_fk=True
        load_instance=True
