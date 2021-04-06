from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from pybo.forms import QuestionForm
from pybo.models import Question


@login_required(login_url='common:login')
def question_create(request):
    """
    pybo 질문 등록
    """
    # 동일한 URL 요청을 POST, GET 요청 방식에 따라 다르게 처리
    # QuestionForm 객체도 POST, GET 요청 방식에 따라 다르게 생성
    # GET -> 입력 값 없이 객체를 생성함. -> form.as_p 태그가 객체의 요소에 맞춰 자동으로 화면 구성
    # POST -> 화면에서 전달받은 데이터로 폼의 값이 채워지도록 객체 생성
    # form.is_valid -> POST 요청으로 받은 form이 유효한지 검사한다.
    # question = form.save(commit=False) -> 폼 자체를 생성, 임시저장(commit = False)
    if request.method == "POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.create_date = timezone.now()
            question.author = request.user #추가한 속성 author 적용
            question.save()
            return redirect('pybo:index')
    else:
        # QuestionForm 클래스 -> 질문을 등록하기 위해 장고에서 제공하는 폼
        form = QuestionForm()
    context = {'form': form}
    return render(request, 'pybo/question_form.html', context)


@login_required(login_url='common/login')
def question_modify(request, question_id):
    """
    pybo 질문 수정
    """
    question = get_object_or_404(Question, pk=question_id)

    if request.user != question.author:
        messages.error(request, '수정권한이 없습니다.')
        return redirect('pybo:detail', question_id=question.id)

    if request.method == "POST":
        #위 코드는 조회한 질문 question을 기본값으로 하여 화면으로 전달받은 입력값들을 덮어써서 QuestionForm을 생성하라는 의미이다.
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.modify_date = timezone.now()
            question.save()
            return redirect('pybo:detail', question_id=question.id)
    else:
        # instance 매개변수에 question을 지정하면 기존 값을 폼에 채울 수 있다.
        form = QuestionForm(instance=question)
    context = {'form': form}
    return render(request, 'pybo/question_form.html', context)


@login_required(login_url='common/login')
def question_delete(request, question_id):
    """
    pybo 질문 삭제
    """
    question = get_object_or_404(Question, pk=question_id)

    if request.user != question.author:
        messages.error(request, '삭제 권한이 없습니다.')
        return redirect('pybo:detail', question_id=question.id)
    else:
        question.delete()
    return redirect('pybo:index')