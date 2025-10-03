// Level Up Life - Main JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Auto-hide alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert-dismissible');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });

    // Confirm quest completion
    const completeButtons = document.querySelectorAll('form[action*="complete_quest"] button[type="submit"]');
    completeButtons.forEach(function(button) {
        button.addEventListener('click', function(e) {
            // Check if the confirmation is already handled via onclick in HTML
            if (this.getAttribute('onclick')) {
                return; 
            }
            const questTitle = this.closest('.quest-item').querySelector('h6').textContent.trim();
            if (!confirm(`Bạn có chắc muốn hoàn thành nhiệm vụ "${questTitle}"?`)) {
                e.preventDefault();
            }
        });
    });

    // Add loading state to buttons
    const submitButtons = document.querySelectorAll('button[type="submit"]');
    submitButtons.forEach(function(button) {
        button.addEventListener('click', function(e) {
            // Prevent double submission
            if (this.disabled) {
                e.preventDefault();
                return false;
            }

            const originalText = this.innerHTML;
            this.innerHTML = '<i class="fas fa-spinner fa-spin me-1"></i>Đang xử lý...';
            this.disabled = true;

            // Re-enable after 5 seconds (failsafe)
            setTimeout(() => {
                this.innerHTML = originalText;
                this.disabled = false;
            }, 5000);
        });
    });

    // Quest item animations
    const questItems = document.querySelectorAll('.quest-item');
    questItems.forEach(function(item, index) {
        item.style.animationDelay = `${index * 0.1}s`;
        item.classList.add('fade-in');
    });

    // --- LOGIC TỪ DASHBOARD.HTML: EXP progress bar animation ---
    const progressBars = document.querySelectorAll('.progress-bar[data-progress]'); // Chỉ chọn thanh có data-progress
    progressBars.forEach(function(bar) {
        const progressValue = bar.getAttribute('data-progress'); // Lấy giá trị từ data-progress
        bar.style.width = '0%'; // Bắt đầu từ 0
        setTimeout(() => {
            bar.style.transition = 'width 1.5s ease-in-out'; // Thêm transition cho mượt
            bar.style.width = progressValue + '%'; // Gán giá trị thực
        }, 100);
    });
    // -----------------------------------------------------------------


    // --- LOGIC TỪ CREATE_QUEST.HTML: Update preview when form changes ---
    const expField = document.getElementById('exp_reward');
    const questTypeField = document.getElementById('quest_type');
    const statRewardField = document.getElementById('stat_reward');
    
    function updatePreview() {
        if (!expField || !questTypeField || !statRewardField) return; // Thoát nếu không phải trang tạo nhiệm vụ

        const exp = expField.value || expField.getAttribute('value') || 10;
        const questType = questTypeField.value;
        const statReward = statRewardField.value || statRewardField.getAttribute('value') || 1;
        
        document.getElementById('preview-exp').textContent = exp;
        
        // Reset all stats
        document.getElementById('preview-str').textContent = '0';
        document.getElementById('preview-int').textContent = '0';
        document.getElementById('preview-end').textContent = '0';
        document.getElementById('preview-cre').textContent = '0';
        
        // Set the appropriate stat
        if (questType === 'strength') {
            document.getElementById('preview-str').textContent = statReward;
        } else if (questType === 'intelligence') {
            document.getElementById('preview-int').textContent = statReward;
        } else if (questType === 'endurance') {
            document.getElementById('preview-end').textContent = statReward;
        } else if (questType === 'creativity') {
            document.getElementById('preview-cre').textContent = statReward;
        }
    }

    if (expField && questTypeField && statRewardField) {
        expField.addEventListener('input', updatePreview);
        questTypeField.addEventListener('change', updatePreview);
        statRewardField.addEventListener('input', updatePreview);
        
        // Initial update
        updatePreview();
    }
    // -----------------------------------------------------------------
});

// Utility functions
function showToast(message, type = 'info') {
    // Create toast element
    const toast = document.createElement('div');
    toast.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
    toast.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
    toast.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(toast);
    
    // Auto remove after 4 seconds
    setTimeout(() => {
        if (toast.parentNode) {
            // Sử dụng bootstrap.Alert để đảm bảo hiệu ứng fade-out
            const bsAlert = new bootstrap.Alert(toast);
            bsAlert.close();
            // Sau khi fade-out, loại bỏ toast khỏi DOM
            setTimeout(() => {
                if (toast.parentNode) toast.parentNode.removeChild(toast);
            }, 500); // 500ms là thời gian cho hiệu ứng fade
        }
    }, 4000);
}

// Form validation enhancement (Optional, Flask-WTF đã xử lý chính)
function validateQuestForm() {
    const title = document.getElementById('title');
    const expReward = document.getElementById('exp_reward');
    
    // Giữ lại phần kiểm tra JS này để cung cấp phản hồi ngay lập tức (frontend validation)
    if (title && title.value.length < 3) {
        showToast('Tên nhiệm vụ phải có ít nhất 3 ký tự!', 'warning');
        return false;
    }
    
    if (expReward && (expReward.value < 1 || expReward.value > 100)) {
        showToast('EXP phải từ 1 đến 100!', 'warning');
        return false;
    }
    
    return true;
}

// Add smooth scrolling to anchors
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});