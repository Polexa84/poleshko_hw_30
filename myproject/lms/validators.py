from rest_framework import serializers
import re

def validate_youtube_link(value):
    """
    Валидирует ссылку на видео, проверяя, что она относится к youtube.com.
    """
    if not isinstance(value, str):  # Проверяем, что value - строка
        return value # Если не строка, пропускаем. Это может быть нужно для редактирования.
    if value:  # Проверяем, что ссылка не пуста
        youtube_pattern = r"^(https?://)?(www\.)?(youtube\.com|youtu\.be)/.+$"
        if not re.match(youtube_pattern, value):
            raise serializers.ValidationError("Разрешены только ссылки на youtube.com.")
    return value # Возвращаем значение, если валидация пройдена (или ссылка пустая).