from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, HiddenField
from wtforms.validators import DataRequired, Email, EqualTo


class RegisterForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    confirm_password = PasswordField('confirm_password', validators=[DataRequired(), EqualTo('password')])  # 比较表单中的密码是否一致
    email = StringField('email', validators=[DataRequired(), Email()])  # 会检测邮箱格式是否合法


class LoginForm(FlaskForm):
    email = StringField('email', validators=[DataRequired(), Email()])
    password = PasswordField('password', validators=[DataRequired()])
    next = HiddenField()


class PostForm(FlaskForm):
    title = StringField('title', validators=[DataRequired()])
    content = StringField('content', validators=[DataRequired()])
    tags = StringField('tags', validators=[DataRequired()])

class CommentForm(FlaskForm):
    content = StringField('content', validators=[DataRequired()])