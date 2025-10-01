from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from config import Config

# Khởi tạo Extensions (được khởi tạo ngoài hàm create_app để dễ import)
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
bcrypt = Bcrypt()


def create_app(config_class=Config):
    # Khởi tạo ứng dụng Flask
    app = Flask(__name__)
    # Đọc cấu hình từ class Config
    app.config.from_object(config_class)

    # Khởi tạo Extensions với ứng dụng
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    bcrypt.init_app(app)

    # Cấu hình Flask-Login
    # ĐIỀU CHỈNH: Chúng ta sẽ dùng tên Blueprint là 'routes' như đã thống nhất ban đầu
    login_manager.login_view = 'routes.login' 
    login_manager.login_message = 'Vui lòng đăng nhập để truy cập trang này.'
    login_manager.login_message_category = 'info'

    # Đăng ký Blueprint
    from app.routes import main, auth # THAY ĐỔI: Import cả hai Blueprint
    app.register_blueprint(main)
    app.register_blueprint(auth)
    
    return app


# User Loader phải được định nghĩa sau khi db được khởi tạo, 
# nhưng trước khi ứng dụng được tạo, nên đặt nó ở ngoài hàm create_app là đúng.
@login_manager.user_loader
def load_user(user_id):
    # LƯU Ý: Phải import User từ app.models
    from app.models import User
    return User.query.get(int(user_id))