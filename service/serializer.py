import re

from rest_framework import serializers

from service.models import User, Comments, Post


class PhoneValidator:
    def __call__(self, value):
        if len(str(value)) != 11:
            raise serializers.ValidationError("Номер телефона должен состоять из 11 цифр")
        if str(value)[0] != "7":
            raise serializers.ValidationError("Номер телефона должен начинаться с 7")


class ForbiddenWordsValidator:
    list_forbidden_words = ["ерунда", "глупость", "чепуха"]

    def __call__(self, value):
        list_value = value.lower().split()
        if set(self.list_forbidden_words) & set(list_value):
            raise serializers.ValidationError(f"В заголовоке есть запрещенные слова: {self.list_forbidden_words}")


class EmailValidator:
    list_allowed_email = ["mail.ru", "yandex.ru"]

    def __call__(self, value):
        list_value = value.split("@")
        if not set(self.list_allowed_email) & set(list_value):
            raise serializers.ValidationError(f"Разрешены домены: {self.list_allowed_email}")


class PasswordValidator:
    pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[A-Za-z\d]{8,}$"

    def __call__(self, value):
        if re.match(self.pattern, value) is None:
            raise serializers.ValidationError("Пароль должен содержать цифры и буквы в верхнем и нижнем регистре. "
                                              "Пароль должен быть не менее 8 символов")


class UserSerializers(serializers.ModelSerializer):
    email = serializers.EmailField(validators=[EmailValidator()])
    phone = serializers.IntegerField(validators=[PhoneValidator()])
    password = serializers.CharField(validators=[PasswordValidator()])

    def create(self, validated_data):
        user = super().create(validated_data)
        user.set_password(user.password)
        user.save()

        return user

    class Meta:
        model = User
        fields = "__all__"


class CommentsSerializers(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field="username")

    class Meta:
        model = Comments
        fields = "__all__"


class PostSerializers(serializers.ModelSerializer):
    title = serializers.CharField(validators=[ForbiddenWordsValidator()])
    author = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field="username")
    comments = serializers.SlugRelatedField(queryset=Comments.objects.all(), slug_field="text", many=True)

    class Meta:
        model = Post
        fields = "__all__"
