from ma import ma
from models.user import UserModel


class UserSchema(ma.SQLAlchemyAutoSchema):

    class Meta:
        model = UserModel
        load_only=("password",)
        load_instance=True
