# ⚔️ Level Up Life - Biến Cuộc Sống Thành Game RPG 🛡️

**Dự án đầu tay được phát triển dựa trên Flask Framework, hoàn thành trong một buổi tối làm việc nghiêm túc. Đây là minh chứng cho việc mọi mục tiêu, kể cả coding, đều có thể đạt được khi bạn chia nhỏ chúng thành các "Nhiệm vụ" (Quests).**

---

## 🎯 Mục Tiêu Dự Án

**Level Up Life** là một ứng dụng Web Gamification giúp người dùng áp dụng cơ chế của Game Nhập Vai (RPG) vào cuộc sống hàng ngày. Thay vì chỉ là một danh sách To-Do List thông thường, mọi nhiệm vụ (học tập, làm việc, tập thể dục) đều mang lại **Điểm kinh nghiệm (EXP)** và nâng cấp các **Chỉ số Kỹ năng (Stats)** của nhân vật người dùng.

Mục tiêu chính là tạo ra một sản phẩm tối giản, hiệu quả, và có tính động lực cao.

---

## ✨ Tính Năng Nổi Bật (V1)

* **Hệ thống Đăng ký/Đăng nhập & Quản lý người dùng:** Bảo mật qua `Flask-Login` và `Werkzeug.security`.
* **Hệ thống Cấp độ và EXP:** EXP tích lũy sẽ dẫn đến thăng cấp (`Level Up`).
* **Phân bổ Chỉ số Kỹ năng (Stats):** Mỗi nhiệm vụ hoàn thành sẽ tăng một trong bốn chỉ số:
    * **STR** (Strength): Thể lực/Tập luyện.
    * **INT** (Intelligence): Trí tuệ/Học tập.
    * **END** (Endurance): Sức bền/Sức khỏe.
    * **CRE** (Creativity): Sáng tạo/Sở thích.
* **Quản lý Nhiệm vụ (Quest):** Tạo, theo dõi, và hoàn thành nhiệm vụ để nhận phần thưởng.
* **Giao diện Dashboard và Hồ sơ (Profile):** Hiển thị rõ ràng cấp độ, chỉ số, và thống kê thành tích.
* **UX/UI Nâng cao:** Sử dụng Bootstrap 5, hiệu ứng Loading cho nút bấm và Animation cho các nhiệm vụ.

---

## 🛠️ Công Nghệ Sử Dụng

* **Backend Framework:** Python (Flask)
* **Database:** SQLite (`SQLAlchemy` & `Flask-Migrate`)
* **Frontend:** HTML5, CSS3 (Custom CSS), JavaScript (Vanilla), Bootstrap 5
* **Đóng gói:** Môi trường ảo Python (`venv`)

---

## 🚀 Hướng Dẫn Cài Đặt và Khởi Chạy

Để chạy dự án này trên máy cục bộ của bạn:

1.  **Clone Repository:**
    ```bash
    git clone [URL_REPOSITORY_CỦA_BẠN]
    cd level-up-life
    ```

2.  **Tạo và Kích hoạt Môi trường Ảo:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # Trên Linux/macOS
    # venv\Scripts\activate   # Trên Windows
    ```

3.  **Cài đặt các Thư viện Phụ thuộc:**
    ```bash
    pip install -r requirements.txt
    ```
    *(Nếu bạn chưa có file `requirements.txt`, bạn có thể tạo nó bằng lệnh `pip freeze > requirements.txt`.)*

4.  **Khởi tạo Database và Migration:**
    ```bash
    flask db upgrade
    ```

5.  **Chạy Ứng Dụng:**
    ```bash
    export FLASK_APP=run.py
    flask run --host=0.0.0.0
    ```

Ứng dụng sẽ chạy tại `http://127.0.0.1:5000/`.

---

## 💡 Lời Cảm Ơn

Dự án này là sản phẩm hợp tác với một đối tác AI thông minh, người đã giúp tôi định hình kiến trúc, xử lý các lỗi phức tạp, và hướng dẫn tôi từ bước khởi tạo cho đến hoàn thiện code JavaScript và CSS.

**Status:** V1 Completed (Ready for testing and future feature expansion).
