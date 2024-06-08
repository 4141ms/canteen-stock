from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from feedback.models import Feedback
from backend.models import UserInfo

import json

def create_feedback(request):
    if request.method == "POST":
        try:
            data = request.body.decode("utf-8")
            json_data = json.loads(data)
        except json.decoder.JSONDecodeError:
            return JsonResponse({
                'code': 400,
                "msg": '请求数据格式错误'
            })

        user_id = json_data.get("user_id")
        # user_name = json_data.get("username")
        content = json_data.get("content")

        # if not all([user_id, user_name, content]):
        if not all([user_id,content]):
            return JsonResponse({
                'code': 400,
                "msg": '缺少必要的参数'
            })

        try:
            user_info = UserInfo.objects.get(id=user_id)
        except UserInfo.DoesNotExist:
            return JsonResponse({
                'code': 404,
                "msg": '用户不存在'
            })

        feedback = Feedback.objects.create(
            user=user_info,
            user_name=user_info.user.username,
            content=content
        )

        return JsonResponse({
            'code': 201,
            "msg": '反馈信息创建成功',
            "feedback": {
                "feedback_id": feedback.id,
                "user_id": feedback.user.id,
                "user_name": feedback.user.user.username,  # 确认 user_name 使用 feedback.user_name
                "content": feedback.content,
                "created_at": feedback.created_at.strftime('%Y-%m-%d %H:%M:%S')
            }
        })
    else:
        return JsonResponse({
            'code': 405,
            "msg": '仅支持POST请求'
        })
