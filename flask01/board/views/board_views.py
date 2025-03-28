# Blueprint 기능을 사용해서 collection/no1/
# Blueprint 기능을 사용해서 collection/no2/
from flask import Blueprint, render_template, redirect, url_for, request
from ..models import Question
from ..forms import QuestionForm, AnswerForm
from app import db
from datetime import datetime

cbp = Blueprint('board', __name__, url_prefix='/board')

# templates 디렉토리 안에 들어있는 file 경로를 읽고, board 안에 있는 객체
# @cbp.route('/list')
# def list():
#     question = Question.query.all()
#     return render_template('board/boardList.html', question_list=question)

@cbp.route('/list')
def list():
    page = request.args.get('page', type=int, default=1)  # 페이지
    question_list = Question.query.order_by(Question.create_date.desc())
    question_list = question_list.paginate(page=page, per_page=10)
    return render_template('board/boardList.html', question_list=question_list)

# 개별 게시글을 조회할 수 있는 함수
@cbp.route('/detail/<int:question_id>/')
def detail(question_id):
    # get_or_404 : 메서드로 값을 조회하면 404 에러를 발생시킨다.
    # question = Question.query.get(question_id)
    question = Question.query.get_or_404(question_id)
    form = AnswerForm()
    return render_template('board/boardDetail.html', question=question, form=form, question_id=question_id)


# 개별 게시글을 작성
# 1. 작성버튼을 누르면 게시글을 작성하기 위한 form으로 이동
# 2. 완료 버튼을 누르면 db에 글을 저장하고, 저장된 글의 Detail로 이동하거나 전체 list로 이동한다.
@cbp.route('/create', methods=['GET', 'POST'])
def create():
    form = QuestionForm()
    if request.method == 'POST' and form.validate_on_submit():
        question = Question(subject=form.subject.data, content=form.content.data, create_date=datetime.now())
        db.session.add(question)
        db.session.commit()
        return redirect(url_for('board.list'))
    return render_template('board/questionForm.html', form=form)



# 개별 게시글을 삭제


# 개별 게시글을 수정


@cbp.route('/no1')
def hello2():
    return f'{__name__} 첫번째'
    
@cbp.route('/no2')
def hello3():
    return f'{__name__} 두번째'
    