# from django.http import HttpResponse
# from django.views import View
# from django.shortcuts import redirect
# from django.utils.http import urlencode
# from django.urls import reverse
# from django.contrib.auth.mixins import LoginRequiredMixin
# from django.shortcuts import render

# class ManualProjectedView(View):
#     def get(self, request):
#         if request.user.is_authenticated:
#             return HttpResponse("Secret")
#         url = reverse("login") + "?" + urlencode({"next:"})
#         return redirect(url)

# class ProtectedView(LoginRequiredMixin, View):
#     def get(self, request):
#         return render(request, "index.html")