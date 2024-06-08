from django.db import models
from django.utils import timezone
from backend.models import UserInfo  # backend为包含 UserInfo 模型的应用程序名

# 反馈信息的表
class Feedback(models.Model):
    user = models.ForeignKey(UserInfo, on_delete=models.CASCADE)
    user_name = models.CharField(max_length=128)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
