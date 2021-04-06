from django import forms
from pybo.models import Question, Answer, Comment


# form.ModelForm을 ***상속***받아 모델 폼을 만듦.
# 모델 폼은 말 그대로 모델과 연결된 폼이며, 모델 폼 객체를 저장하면 연결된 모델의 데이터를 저장할 수 있다.
class QuestionForm(forms.ModelForm):
    # 장고 모델 폼은 내부 클래스로 Meta 클래스를 반드시 가져야 하며, Meta 클래스에는 모델 폼이 사용할 모델과 모델의 필드들을 적어야 한다.
    class Meta:
        model = Question
        fields = ['subject', 'content']

        # 21-04-01: form.as_p 대신 수동 폼 작성을 위해 widgets 주석처리
        # widgets -> attrs등의 속성을 통해 스타일 지정 가능.
        # widgets = {
        #     'subject': forms.TextInput(attrs={'class': 'form-control'}),
        #     'content': forms.Textarea(attrs={'class': 'form-control', 'rows':10}),
        # }

        # labels -> Form의 컬럼명을 변경 가능.
        labels = {
            'subject': '제목',
            'content': '내용',
        }


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['content']

        labels = {
            'content': '답변내용',
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        labels = {
            'content': '댓글내용',
        }
