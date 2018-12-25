from django.conf.urls import url
from . import views
from .forms import RegisterFormView

urlpatterns = [
    url(r'^error/$', views.for_login_only, name='for_login_only'),

    url(r'^$', views.index, name='index'),
    url(r'^FAQ/$', views.FAQ, name='FAQ'),

    url(r'^register/$', RegisterFormView.as_view()),
    url(r'^create_profile/$', views.user_add_info, name='user_add_info'),
    url(r'^edit_profile/$', views.user_edit_info, name='user_edit_info'),

    url(r'^user/(?P<login>\w+)/$', views.user_profile, name='user_profile'),
    url(r'^user/(?P<login>\w+)/test_(?P<pkt>\d+)/$', views.user_profile_with_graph,
        name='user_profile_with_graph'),

    url(r'^tests/$', views.tests_list, name='tests_list'),

    url(r'^test_(?P<pkt>\d+)/$', views.test_detail, name='test_detail'),
    url(r'^test_(?P<pkt>\d+)/questions/$', views.questions_detail, name='questions_detail'),
    url(r'^test_(?P<pkt>\d+)/result/$', views.test_result, name='test_result'),
]