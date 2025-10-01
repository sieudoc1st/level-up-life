from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, IntegerField, BooleanField, SelectField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo, NumberRange, ValidationError
from app.models import User

# --- 1. Form Đăng Nhập ---
class LoginForm(FlaskForm):
    # Cho phép người dùng nhập Tên đăng nhập hoặc Email
    login_identity = StringField('Tên tài khoản / Email', validators=[DataRequired()])
    
    password = PasswordField('Mật khẩu', validators=[DataRequired()])
    remember_me = BooleanField('Ghi nhớ đăng nhập')
    submit = SubmitField('Đăng nhập')


# --- 2. Form Đăng Ký ---
class RegisterForm(FlaskForm):
    username = StringField('Tên đăng nhập', validators=[
        DataRequired(), 
        Length(min=4, max=20, message='Tên đăng nhập phải từ 4-20 ký tự')
    ])
    email = StringField('Email', validators=[
        DataRequired(), 
        Email(message='Email không hợp lệ')
    ])
    password = PasswordField('Mật khẩu', validators=[
        DataRequired(), 
        Length(min=6, message='Mật khẩu phải ít nhất 6 ký tự')
    ])
    # Đổi tên trường để nhất quán
    confirm_password = PasswordField('Xác nhận mật khẩu', validators=[
        DataRequired(), 
        EqualTo('password', message='Mật khẩu xác nhận không khớp')
    ])
    submit = SubmitField('Đăng ký')
    
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Tên đăng nhập đã tồn tại. Vui lòng chọn tên khác.')
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email đã được sử dụng. Vui lòng chọn email khác.')


# --- 3. Form Tạo Nhiệm Vụ ---
class QuestForm(FlaskForm):
    title = StringField('Tên nhiệm vụ', validators=[
        DataRequired(), 
        Length(max=200, message='Tên nhiệm vụ không được quá 200 ký tự')
    ])
    description = TextAreaField('Mô tả', validators=[Length(max=500, message='Mô tả không được quá 500 ký tự')])
    
    exp_reward = IntegerField('Điểm kinh nghiệm', validators=[
        DataRequired(), 
        NumberRange(min=1, max=100, message='EXP phải từ 1-100')
    ], default=10)
    
    # Danh sách các chỉ số (Stats)
    STAT_CHOICES = [
        ('strength', 'Thể lực (Strength)'),
        ('intelligence', 'Trí tuệ (Intelligence)'),
        ('endurance', 'Sức bền (Endurance)'),
        ('creativity', 'Sáng tạo (Creativity)')
    ]
    quest_type = SelectField('Chỉ số nhận thưởng', choices=STAT_CHOICES, validators=[DataRequired()])
    
    stat_reward = IntegerField('Điểm thưởng chỉ số', validators=[
    # THÊM DataRequired() VÀO ĐÂY
    DataRequired(message='Không được để trống'), 
    NumberRange(min=0, max=10, message='Điểm thưởng kỹ năng từ 0-10')
    ], default=1)
    
    is_daily = BooleanField('Nhiệm vụ hàng ngày', default=True)
    submit = SubmitField('Tạo nhiệm vụ')