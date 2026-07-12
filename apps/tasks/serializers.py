from datetime import date
from rest_framework import serializers
from .models import Task


class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = "__all__"
        read_only_fields = (
            "id",
            "user",
            "created_at",
            "updated_at",
        )

    def validate_due_date(self, value):
        if value < date.today():
            raise serializers.ValidationError(
                "Due date cannot be in the past."
            )
        return value

    def validate_tags(self, value):
        if len(value) > 5:
            raise serializers.ValidationError(
                "You can add a maximum of 5 tags."
            )
        return value

    def validate_title(self, value):
        if len(value.strip()) < 3:
            raise serializers.ValidationError(
                "Title must be at least 3 characters long."
            )
        return value