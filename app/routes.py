from flask import Blueprint, render_template, flash, redirect, url_for, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from datetime import datetime, date
from app import db, bcrypt
from app.models import User, Quest, Completion
from app.forms import LoginForm, RegisterForm, QuestForm

# Create blueprints
main = Blueprint('main', __name__)
auth = Blueprint('auth', __name__)

# Authentication routes
# app/routes.py - Hàm login() (Phiên bản đã tối ưu)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        # Lấy dữ liệu người dùng nhập vào (có thể là username hoặc email)
        identity = form.login_identity.data
        
        # 1. Thử tìm bằng Email
        user = User.query.filter_by(email=identity).first()
        
        # 2. Nếu không tìm thấy, thử tìm bằng Tên đăng nhập
        if user is None:
            user = User.query.filter_by(username=identity).first()
            
        # Kiểm tra người dùng tồn tại VÀ mật khẩu hợp lệ
        if user and bcrypt.check_password_hash(user.password_hash, form.password.data):
            # Cập nhật thời gian đăng nhập
            user.last_login = datetime.utcnow()
            db.session.commit()
            
            login_user(user, remember=form.remember_me.data)
            flash(f'Chào mừng trở lại, {user.username}! 🎮', 'success')
            
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.dashboard'))
        else:
            flash('Tên tài khoản, Email, hoặc mật khẩu không đúng!', 'danger')
    
    return render_template('login.html', title='Đăng nhập', form=form)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    form = RegisterForm()
    if form.validate_on_submit():
        # Hash password
        password_hash = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        
        # Create new user
        user = User(
            username=form.username.data,
            email=form.email.data,
            password_hash=password_hash
        )
        
        db.session.add(user)
        db.session.commit()
        
        flash(f'Chào mừng {user.username} đến với Level Up Life! 🚀', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('register.html', title='Đăng ký', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Đã đăng xuất thành công. Hẹn gặp lại! 👋', 'info')
    return redirect(url_for('auth.login'))

# Main application routes
@main.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    return redirect(url_for('auth.login'))

@main.route('/dashboard')
@login_required
def dashboard():
    # Get active quests for current user
    quests = Quest.query.filter_by(user_id=current_user.id, is_active=True).order_by(Quest.created_at.desc()).all()
    
    # Add completion status to each quest
    for quest in quests:
        quest.completed_today = quest.is_completed_today()
    
    # Get today's completed quests count
    today = date.today()
    today_completions = Completion.query.filter_by(
        user_id=current_user.id,
        completed_date=today
    ).count()
    
    # Get total completions
    total_completions = Completion.query.filter_by(user_id=current_user.id).count()
    
    stats = {
        'today_completions': today_completions,
        'total_completions': total_completions,
        'active_quests': len(quests),
        'exp_to_next': current_user.exp_to_next_level(),
        'exp_progress': current_user.exp_progress_percentage()
    }
    
    return render_template('dashboard.html', 
                         title='Dashboard', 
                         quests=quests, 
                         stats=stats)

@main.route('/create_quest', methods=['GET', 'POST'])
@login_required
def create_quest():
    form = QuestForm()
    if form.validate_on_submit():
        # Set stat rewards based on quest type
        quest = Quest(
            title=form.title.data,
            description=form.description.data,
            exp_reward=form.exp_reward.data,
            is_daily=form.is_daily.data,
            user_id=current_user.id
        )
        # THÊM: Thiết lập tất cả stat reward về 0 để tránh tích lũy
        quest.strength_reward = 0
        quest.intelligence_reward = 0
        quest.endurance_reward = 0
        quest.creativity_reward = 0
        # Set appropriate stat reward based on quest type
        if form.quest_type.data == 'strength':
            quest.strength_reward = form.stat_reward.data
        elif form.quest_type.data == 'intelligence':
            quest.intelligence_reward = form.stat_reward.data
        elif form.quest_type.data == 'endurance':
            quest.endurance_reward = form.stat_reward.data
        elif form.quest_type.data == 'creativity':
            quest.creativity_reward = form.stat_reward.data
        
        db.session.add(quest)
        db.session.commit()
        
        flash(f'Nhiệm vụ "{quest.title}" đã được tạo thành công! 🎯', 'success')
        return redirect(url_for('main.dashboard'))
    
    return render_template('create_quest.html', title='Tạo nhiệm vụ', form=form)

@main.route('/complete_quest/<int:quest_id>', methods=['POST'])
@login_required
def complete_quest(quest_id):
    quest = Quest.query.get_or_404(quest_id)
    
    # Verify quest belongs to current user
    if quest.user_id != current_user.id:
        flash('Bạn không có quyền hoàn thành nhiệm vụ này!', 'danger')
        return redirect(url_for('main.dashboard'))
    
    # Check if already completed today
    if quest.is_completed_today():
        flash('Nhiệm vụ này đã được hoàn thành hôm nay rồi!', 'warning')
        return redirect(url_for('main.dashboard'))
    
    # Create completion record
    completion = Completion(
        user_id=current_user.id,
        quest_id=quest.id,
        exp_earned=quest.exp_reward,
        strength_earned=quest.strength_reward,
        intelligence_earned=quest.intelligence_reward,
        endurance_earned=quest.endurance_reward,
        creativity_earned=quest.creativity_reward
    )
    
    # Update user stats
    current_user.exp += quest.exp_reward
    current_user.strength += quest.strength_reward
    current_user.intelligence += quest.intelligence_reward
    current_user.endurance += quest.endurance_reward
    current_user.creativity += quest.creativity_reward
    
    # Check for level up
    old_level = current_user.level
    new_level = current_user.check_and_level_up()
    
    db.session.add(completion)
    db.session.commit()
    
    # Flash appropriate message
    if new_level > old_level:
        flash(f'🎉 CHÚC MỪNG! Bạn đã lên cấp {new_level}! Nhiệm vụ "{quest.title}" hoàn thành (+{quest.exp_reward} EXP)', 'success')
    else:
        flash(f'✅ Nhiệm vụ "{quest.title}" hoàn thành! (+{quest.exp_reward} EXP)', 'success')
    
    return redirect(url_for('main.dashboard'))

@main.route('/toggle_quest/<int:quest_id>', methods=['POST'])
@login_required
def toggle_quest(quest_id):
    quest = Quest.query.get_or_404(quest_id)
    
    # Verify quest belongs to current user
    if quest.user_id != current_user.id:
        flash('Bạn không có quyền thay đổi nhiệm vụ này!', 'danger')
        return redirect(url_for('main.dashboard'))
    
    quest.is_active = not quest.is_active
    db.session.commit()
    
    status = "kích hoạt" if quest.is_active else "tạm dừng"
    flash(f'Nhiệm vụ "{quest.title}" đã được {status}!', 'info')
    
    return redirect(url_for('main.dashboard'))

@main.route('/delete_quest/<int:quest_id>', methods=['POST'])
@login_required
def delete_quest(quest_id):
    quest = Quest.query.get_or_404(quest_id)
    
    # Verify quest belongs to current user
    if quest.user_id != current_user.id:
        flash('Bạn không có quyền xóa nhiệm vụ này!', 'danger')
        return redirect(url_for('main.dashboard'))
    
    quest_title = quest.title
    db.session.delete(quest)
    db.session.commit()
    
    flash(f'Nhiệm vụ "{quest_title}" đã được xóa!', 'info')
    return redirect(url_for('main.dashboard'))

@main.route('/profile')
@login_required
def profile():
    # Get completion statistics
    total_completions = Completion.query.filter_by(user_id=current_user.id).count()
    
    # Get completions this week/month for charts
    from datetime import datetime, timedelta
    
    week_ago = datetime.now() - timedelta(days=7)
    month_ago = datetime.now() - timedelta(days=30)
    
    week_completions = Completion.query.filter(
        Completion.user_id == current_user.id,
        Completion.completed_at >= week_ago
    ).count()
    
    month_completions = Completion.query.filter(
        Completion.user_id == current_user.id,
        Completion.completed_at >= month_ago
    ).count()
    
    stats = {
        'total_completions': total_completions,
        'week_completions': week_completions,
        'month_completions': month_completions,
        'total_quests': Quest.query.filter_by(user_id=current_user.id).count(),
        'active_quests': Quest.query.filter_by(user_id=current_user.id, is_active=True).count()
    }
    
    return render_template('profile.html', title='Hồ sơ', stats=stats)
