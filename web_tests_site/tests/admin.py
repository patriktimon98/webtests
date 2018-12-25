from django.contrib import admin

from .models import User_Info
from .models import Passed_Test
from .models import Test
from .models import Question
from .models import Answer

admin.site.register(User_Info)
admin.site.register(Passed_Test)
admin.site.register(Test)
admin.site.register(Question)
admin.site.register(Answer)