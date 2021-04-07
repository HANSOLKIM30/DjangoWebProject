from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.shortcuts import render, get_object_or_404

from pybo.models import Question


def index(request):
    """
    pybo 목록 출력
    """
    # 입력 파라미터
    # requset.GET.get(key, default Value)
    page = request.GET.get('page', '1')  # 페이지
    kw = request.GET.get('kw', '') # 검색어
    so = request.GET.get('so', 'recent')
    # 조회(날짜 순 정렬)
    if so == "recommend":
        # annotate -> Question 모델의 필드인 voter의 질문의 추천 수에 해당하는 num_voter 필드를 임시로 추가해 주는 함수
        question_list = Question.objects.annotate(num_voter=Count('voter')).order_by('-num_voter', '-create_date')
    elif so == "popular":
        question_list = Question.objects.annotate(num_answer=Count('answer')).order_by('-num_answer', '-create_date')
    else: #recent
        question_list = Question.objects.order_by('-create_date')
    
    # 검색
    if kw:
        question_list = question_list.filter(
            Q(subject__icontains=kw) | # 제목검색
            Q(content__icontains=kw) | # 내용검색
            Q(author__username__icontains=kw) | # 질문 글쓴이 검색
            Q(answer__author__username__icontains=kw) # 답변 글쓴이 검색
        ).distinct()

    # 페이징처리
    # Paginator 클래스를 이용하여 question_list를 페이징 객체 paginator로 변환한다. -> paginator에서 제공하는 여러 변수들을 템플릿에서 활용 가능.
    paginator = Paginator(question_list, 10)  # 페이지 당 10개씩 보여주기
    page_obj = paginator.get_page(page)

    context = {'question_list': page_obj, 'page': page, 'kw': kw, 'so': so}
    return render(request, 'pybo/question_list.html', context)


def detail(request, question_id):
    """
    pybo 내용 출력
    """
    # get_object_or_404: 모델의 기본키(pk)를 이용하여 모델 객체 한 건을 넘겨받거나, 없으면 404를 return
    question = get_object_or_404(Question, pk=question_id)
    context = {'question': question}
    return render(request, 'pybo/question_detail.html', context)
