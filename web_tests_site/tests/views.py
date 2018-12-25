from django.shortcuts import render, get_object_or_404, redirect
from math import ceil
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from .forms import UserAddForm

from .models import User_Info
from .models import Passed_Test
from .models import Test
from .models import Question
from .models import Answer

class User_answers:
    def __init__(self, answers_arr = [], c_question = 0):
        self.answers_arr = answers_arr
        self.c_question = c_question

    def ret_c_question(self):
        return self.c_question

    def inc_question(self):
        self.c_question += 1

def index(request):
    return render(request, 'tests/index.html')

def for_login_only(request):
    return render(request, 'tests/for_login_only.html')

def FAQ(request):
    return render(request, 'tests/FAQ.html')

def tests_list(request):
    tests = Test.objects.order_by('name')
    return render(request, 'tests/tests_list.html', {'tests' : tests})

def test_detail(request, pkt):
    test = get_object_or_404(Test, pk=pkt)
    return render(request, 'tests/test_detail.html', {'test': test})

def questions_detail(request, pkt):
    test = get_object_or_404(Test, pk=pkt)

    questions = Question.objects.filter(test_id=pkt)
    question_f = Question.objects.filter(test_id=pkt).first()
    answers = Answer.objects.filter(question_id=question_f.pk)

    for question in questions:
        ans_buf = Answer.objects.filter(question_id=question.pk)
        answers = ans_buf.union(answers)
    return render(request, 'tests/questions_detail.html', {'test': test, 'questions': questions, 'answers': answers,
                                                           'pkt': pkt})

def test_result(request, pkt):
    result = 0
    ans = dict()

    questions = Question.objects.filter(test_id=pkt)

    for question in questions:
        buf = "ans_" + str(question.pk)
        ind = str(question.correct_answer)

        ans_ = ans[ind] = request.POST.get(buf)

        if ans_ == question.correct_answer:
            result += 1

    result = result / Question.objects.filter(test_id=pkt).count() * 100
    ceil(result)

    if request.user.is_authenticated:
        user_ = get_object_or_404(User, username=request.user.username)
        test_ = get_object_or_404(Test, pk=pkt)
        Passed_Test.objects.create(test_id=test_, result=result, user_id=user_)

    return render(request, 'tests/test_result.html', {'ans': ans, 'result': result})

@login_required
def user_profile(request, login):
    if request.user.get_username() == login:
        user_ = get_object_or_404(User, username=login)

        if User_Info.objects.filter(user_id=user_.pk).exists():
            user_info = User_Info.objects.get(user_id=user_.pk)

            if Passed_Test.objects.filter(user_id=user_.pk).exists():

                passed_tests_id = Passed_Test.objects.filter(user_id=user_.pk)
                passed_tests_id_f = Passed_Test.objects.filter(user_id=user_.pk).first()
                passed_tests = Test.objects.filter(name=passed_tests_id_f.test_id)

                for passed_test_id in passed_tests_id:
                    t_buf = Test.objects.filter(name=passed_test_id.test_id)
                    passed_tests = t_buf.union(passed_tests)
                return render(request, 'tests/user_profile.html',
                              {'user_info': user_info, 'passed_tests': passed_tests})
            else:
                passed_tests = False
                return render(request, 'tests/user_profile.html',
                              {'user_info': user_info, 'passed_tests': passed_tests})
        else:
            return redirect('user_add_info')
    else:
        return render(request, 'tests/for_login_only.html')

@login_required
def user_profile_with_graph(request, login, pkt):
    if request.user.get_username() == login:
        user_ = get_object_or_404(User, username=login)

        if User_Info.objects.filter(user_id=user_.pk).exists():
            user_info = User_Info.objects.get(user_id=user_.pk)

            passed_tests_id = Passed_Test.objects.filter(user_id=user_.pk)
            passed_tests_id_f = Passed_Test.objects.filter(user_id=user_.pk).first()
            passed_tests = Test.objects.filter(name=passed_tests_id_f.test_id)

            for passed_test_id in passed_tests_id:
                t_buf = Test.objects.filter(name=passed_test_id.test_id)
                passed_tests = t_buf.union(passed_tests)

            main_test = get_object_or_404(Test, pk=pkt)
            passed_test_info = Passed_Test.objects.filter(user_id=user_.pk, test_id=main_test.pk)

            val = list()
            for test_info in passed_test_info:
                bufer = list()
                bufer.append(str(test_info.date))
                bufer.append(test_info.result)
                val.append(bufer)

            return render(request, 'tests/user_profile_with_graph.html',
                          {'user_info': user_info, 'passed_tests': passed_tests,
                           'val': val, 'main_test': main_test})
        else:
            return redirect('user_add_info')
    else:
        return render(request, 'tests/for_login_only.html')

def user_add_info(request):
    user_ = get_object_or_404(User, username=request.user.get_username())

    if User_Info.objects.filter(user_id=user_.pk).exists():
        return render(request, 'tests/for_login_only.html')
    else:
        if request.method == "POST":
            form = UserAddForm(request.POST)
            if form.is_valid():
                user_new = form.save(commit=False)
                user_new.user_id = request.user
                user_new.save()
                return redirect('user_profile', login=request.user.get_username())
        else:
            form = UserAddForm()
        return render(request, 'tests/user_add_info.html', {'form': form})

@login_required
def user_edit_info(request):
    user_ = get_object_or_404(User, username=request.user.get_username())

    if User_Info.objects.filter(user_id=user_.pk).exists():
        user_new = User_Info.objects.get(user_id=user_.pk)
        if request.method == "POST":
            form = UserAddForm(request.POST, instance=user_new)
            if form.is_valid():
                user_new = form.save(commit=False)
                user_new.user_id = request.user
                user_new.save()
                return redirect('user_profile', login=request.user.get_username())
        else:
            form = UserAddForm(instance=user_new)
        return render(request, 'tests/user_edit_info.html', {'form': form})
    else:
        return render(request, 'tests/for_login_only.html')