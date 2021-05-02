from flask_wtf import FlaskForm
from wtforms.fields import SelectField, SubmitField


class VerifyingForm(FlaskForm):
    select = SelectField(choices=[('123', 'Подтвердить',
                                   'faqwelse', 'Отклонить')])
    submit = SubmitField('Подтвердить')
