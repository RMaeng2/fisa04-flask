from flask import Flask, render_template, request, Blueprint, g
import os
from ml_model.ml_inference import load_model, predict
from ml_model.forms import InsuranceForm  # forms.py에서 폼 클래스 가져오기
from board.views.auth_views import login_required
from ml_model.models import Insurance
from app import db


mbp = Blueprint('ml', __name__, url_prefix='/ml')


@mbp.route('/', methods=['GET', 'POST'])
@login_required
def inference():
    form = InsuranceForm()  # forms.py에 정의된 폼 객체 생성

    # 실습2. forms.py에 작성된 form을 활용하여 데이터를 한번에 입력받을 수 있도록 활용
    if form.validate_on_submit():  # 폼이 제출되고 유효성 검사를 통과한 경우
        age = form.age.data
        bmi = form.bmi.data
        children = form.children.data
        smoker = 1 if form.smoker.data == "예" else 0
        sex = 1 if form.sex.data == "남성" else 0
        region = form.region.data

        # 지역을 원-핫 인코딩
        region_nw = 1 if region == "북서" else 0
        region_ne = 1 if region == "북동" else 0
        region_sw = 1 if region == "남서" else 0

        # 모델 로드 및 예측
        model = load_model()
        input_values = [[age, bmi, children, smoker, sex, region_nw, region_ne, region_sw]]
        prediction = predict(input_values, model)
        print(prediction)

        # 결과 페이지 렌더링
        return render_template('ml/result.html', prediction=prediction[0])

    # 폼 페이지 렌더링
    return render_template('ml/form.html', form=form)