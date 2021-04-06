from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404

from pybo.models import Question


def index(request):
    """
    pybo 목록 출력
    """
    # 입력 파라미터
    # requset.GET.page(key, default Value)
    page = request.GET.get('page', '1')  # 페이지

    # 조회(날짜 순 정렬)
    question_list = Question.objects.order_by('-create_date')

    # 페이징처리
    # Paginator 클래스를 이용하하여 question_list를 페이징 객체 paginator로 변환한다. -> paginator에서 제공하는 여러 변수들을 템플릿에서 활용 가능.
    paginator = Paginator(question_list, 10)  # 페이지 당 10개씩 보여주기
    page_obj = paginator.get_page(page)

    context = {'question_list': page_obj}
    return render(request, 'pybo/question_list.html', context)


def detail(request, question_id):
    """
    pybo 내용 출력
    """
    # get_object_or_404: 모델의 기본키(pk)를 이용하여 모델 객체 한 건을 넘겨받거나, 없으면 404를 return
    question = get_object_or_404(Question, pk=question_id)
    context = {'question': question}
    return render(request, 'pybo/question_detail.html', context)
