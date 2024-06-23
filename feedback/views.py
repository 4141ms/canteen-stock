from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from feedback.models import Feedback
from backend.models import UserInfo
from django.core import serializers

import json

#展示现有反馈信息
def feedback_list(request):
    response = {}

    # 获取所有反馈信息
    feedbacks = Feedback.objects.all()
    print("here:::::",feedbacks)
    response['feedbacks'] = json.loads(serializers.serialize("json", feedbacks))
    
    return JsonResponse(response)


#创建反馈信息
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
    

#删除反馈信息
def delete_feedback(request):
    if request.method == "POST":
        # 从请求体中获取数据
        try:
            data = json.loads(request.body)
            feedback_id = data.get("feedback_id")
        except json.JSONDecodeError:
            return JsonResponse({
                'code': 400,
                "msg": '请求数据格式错误'
            })

        if feedback_id is None:
            return JsonResponse({
                'code': 400,
                "msg": '缺少反馈信息ID'
            })

        try:
            feedback = Feedback.objects.get(id=feedback_id)
        except Feedback.DoesNotExist:
            return JsonResponse({
                'code': 404,
                "msg": '反馈信息不存在'
            })

        feedback.delete()
        return JsonResponse({
            'code': 200,
            "msg": '反馈信息删除成功'
        })
    else:
        return JsonResponse({
            'code': 405,
            "msg": '仅支持POST请求'
        })


# 修改反馈信息
def update_feedback(request):
    if request.method == "POST":
        try:
            # 解析请求体中的 JSON 数据
            data = json.loads(request.body)
            feedback_id = data.get("feedback_id")
        except json.JSONDecodeError:
            return JsonResponse({
                'code': 400,
                "msg": '请求数据格式错误'
            })

        if feedback_id is None:
            return JsonResponse({
                'code': 400,
                "msg": '缺少反馈信息ID'
            })

        try:
            # 根据 feedback_id 获取反馈信息对象
            feedback = Feedback.objects.get(id=feedback_id)
        except Feedback.DoesNotExist:
            return JsonResponse({
                'code': 404,
                "msg": '反馈信息不存在'
            })

        # 更新反馈信息
        for key, value in data.items():
            setattr(feedback, key, value)
        feedback.save()

        # 返回更新成功的响应
        return JsonResponse({
            'code': 200,
            "msg": '反馈信息更新成功'
        })
    else:
        return JsonResponse({
            'code': 405,
            "msg": '仅支持POST请求'
        })