// VK Post Generator - JavaScript функции

// Инициализация при загрузке страницы
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

function initializeApp() {
    // Инициализация Bootstrap компонентов
    initBootstrapComponents();
    
    // Инициализация форм
    initForms();
    
    // Инициализация модальных окон
    initModals();
    
    // Инициализация уведомлений
    initNotifications();
    
    // Инициализация таблиц
    initTables();
    
    console.log('VK Post Generator инициализирован');
}

// Инициализация Bootstrap компонентов
function initBootstrapComponents() {
    // Инициализация выпадающих меню
    const dropdowns = document.querySelectorAll('.dropdown-toggle');
    dropdowns.forEach(dropdown => {
        new bootstrap.Dropdown(dropdown);
    });
    
    // Инициализация тултипов
    const tooltips = document.querySelectorAll('[data-bs-toggle="tooltip"]');
    tooltips.forEach(tooltip => {
        new bootstrap.Tooltip(tooltip);
    });
    
    // Инициализация поповеров
    const popovers = document.querySelectorAll('[data-bs-toggle="popover"]');
    popovers.forEach(popover => {
        new bootstrap.Popover(popover);
    });
}

// Инициализация форм
function initForms() {
    // Валидация форм в реальном времени
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        // Добавляем классы для анимации
        const inputs = form.querySelectorAll('input, textarea, select');
        inputs.forEach(input => {
            input.addEventListener('focus', function() {
                this.parentElement.classList.add('focused');
            });
            
            input.addEventListener('blur', function() {
                this.parentElement.classList.remove('focused');
            });
        });
    });
    
    // Обработка формы генерации поста
    const generateForm = document.getElementById('generateForm');
    if (generateForm) {
        generateForm.addEventListener('submit', handleGenerateSubmit);
    }
}

// Инициализация модальных окон
function initModals() {
    // Автоматическое закрытие модальных окон по таймеру
    const modals = document.querySelectorAll('.modal');
    modals.forEach(modal => {
        modal.addEventListener('shown.bs.modal', function() {
            // Фокус на первый элемент
            const firstInput = this.querySelector('input, button, select, textarea');
            if (firstInput) {
                firstInput.focus();
            }
        });
    });
}

// Инициализация уведомлений
function initNotifications() {
    // Автоматическое скрытие уведомлений через 5 секунд
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            if (alert && !alert.classList.contains('alert-permanent')) {
                const bsAlert = new bootstrap.Alert(alert);
                bsAlert.close();
            }
        }, 5000);
    });
}

// Инициализация таблиц
function initTables() {
    // Добавление сортировки в таблицы
    const tables = document.querySelectorAll('.table');
    tables.forEach(table => {
        const headers = table.querySelectorAll('th[data-sort]');
        headers.forEach(header => {
            header.style.cursor = 'pointer';
            header.addEventListener('click', function() {
                sortTable(table, this.cellIndex, this.dataset.sort);
            });
        });
    });
}

// Обработка отправки формы генерации
function handleGenerateSubmit(e) {
    const form = e.target;
    const submitBtn = form.querySelector('button[type="submit"]');
    
    // Валидация формы
    if (!validateGenerateForm(form)) {
        e.preventDefault();
        return false;
    }
    
    // Показываем индикатор загрузки
    showLoadingState(submitBtn);
    
    // Показываем модальное окно прогресса
    showGenerationProgress();
    
    return true;
}

// Валидация формы генерации
function validateGenerateForm(form) {
    const topic = form.querySelector('#topic');
    const tone = form.querySelector('#tone');
    
    let isValid = true;
    
    // Проверка темы
    if (!topic.value.trim()) {
        showFieldError(topic, 'Тема поста обязательна для заполнения');
        isValid = false;
    } else if (topic.value.trim().length < 3) {
        showFieldError(topic, 'Тема должна содержать минимум 3 символа');
        isValid = false;
    } else {
        clearFieldError(topic);
    }
    
    // Проверка тона
    if (!tone.value) {
        showFieldError(tone, 'Выберите тон поста');
        isValid = false;
    } else {
        clearFieldError(tone);
    }
    
    return isValid;
}

// Показ ошибки поля
function showFieldError(field, message) {
    field.classList.add('is-invalid');
    
    let feedback = field.parentElement.querySelector('.invalid-feedback');
    if (!feedback) {
        feedback = document.createElement('div');
        feedback.className = 'invalid-feedback';
        field.parentElement.appendChild(feedback);
    }
    feedback.textContent = message;
}

// Очистка ошибки поля
function clearFieldError(field) {
    field.classList.remove('is-invalid');
    const feedback = field.parentElement.querySelector('.invalid-feedback');
    if (feedback) {
        feedback.remove();
    }
}

// Показ состояния загрузки
function showLoadingState(button) {
    button.disabled = true;
    const originalText = button.innerHTML;
    button.setAttribute('data-original-text', originalText);
    button.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Обработка...';
}

// Восстановление состояния кнопки
function restoreButtonState(button) {
    button.disabled = false;
    const originalText = button.getAttribute('data-original-text');
    if (originalText) {
        button.innerHTML = originalText;
    }
}

// Показ прогресса генерации
function showGenerationProgress() {
    const modal = document.getElementById('generationModal');
    if (modal) {
        const bsModal = new bootstrap.Modal(modal, {
            backdrop: 'static',
            keyboard: false
        });
        bsModal.show();
        
        // Запуск анимации прогресса
        animateGenerationProgress();
    }
}

// Анимация прогресса генерации
function animateGenerationProgress() {
    const steps = [
        { selector: '.step-item:nth-child(1)', icon: 'fas fa-file-alt', text: 'Генерация текста поста...' },
        { selector: '.step-item:nth-child(2)', icon: 'fas fa-image', text: 'Создание описания изображения...' },
        { selector: '.step-item:nth-child(3)', icon: 'fas fa-palette', text: 'Генерация изображения...' }
    ];
    
    const progressBar = document.getElementById('progressBar');
    let currentStep = 0;
    
    function updateStep() {
        if (currentStep < steps.length) {
            const step = document.querySelector(steps[currentStep].selector);
            if (step) {
                const icon = step.querySelector('i');
                const text = step.querySelector('span');
                
                // Обновляем иконку
                icon.className = `fas fa-check ${steps[currentStep].icon} text-success`;
                
                // Обновляем текст
                text.textContent = steps[currentStep].text;
                
                // Обновляем прогресс
                const progress = ((currentStep + 1) / steps.length) * 100;
                if (progressBar) {
                    progressBar.style.width = progress + '%';
                }
                
                currentStep++;
                
                if (currentStep < steps.length) {
                    setTimeout(updateStep, 2000);
                }
            }
        }
    }
    
    // Запускаем первый шаг
    setTimeout(updateStep, 500);
}

// Сортировка таблицы
function sortTable(table, columnIndex, sortType) {
    const tbody = table.querySelector('tbody');
    const rows = Array.from(tbody.querySelectorAll('tr'));
    
    // Определяем направление сортировки
    const currentSort = table.getAttribute('data-sort-direction') || 'asc';
    const newSort = currentSort === 'asc' ? 'desc' : 'asc';
    
    // Сортируем строки
    rows.sort((a, b) => {
        const aValue = a.cells[columnIndex].textContent.trim();
        const bValue = b.cells[columnIndex].textContent.trim();
        
        let result = 0;
        
        if (sortType === 'date') {
            result = new Date(aValue) - new Date(bValue);
        } else if (sortType === 'number') {
            result = parseFloat(aValue) - parseFloat(bValue);
        } else {
            result = aValue.localeCompare(bValue, 'ru', { sensitivity: 'base' });
        }
        
        return newSort === 'desc' ? -result : result;
    });
    
    // Обновляем DOM
    rows.forEach(row => tbody.appendChild(row));
    
    // Сохраняем состояние сортировки
    table.setAttribute('data-sort-direction', newSort);
    
    // Обновляем индикаторы сортировки
    updateSortIndicators(table, columnIndex, newSort);
}

// Обновление индикаторов сортировки
function updateSortIndicators(table, columnIndex, direction) {
    const headers = table.querySelectorAll('th');
    headers.forEach((header, index) => {
        header.classList.remove('sort-asc', 'sort-desc');
        if (index === columnIndex) {
            header.classList.add(direction === 'asc' ? 'sort-asc' : 'sort-desc');
        }
    });
}

// AJAX запросы
function makeAjaxRequest(url, options = {}) {
    return fetch(url, {
        method: options.method || 'GET',
        headers: {
            'Content-Type': 'application/json',
            'X-Requested-With': 'XMLHttpRequest',
            ...options.headers
        },
        body: options.body ? JSON.stringify(options.body) : undefined
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    })
    .catch(error => {
        console.error('AJAX Error:', error);
        showNotification('Произошла ошибка при выполнении запроса', 'error');
        throw error;
    });
}

// Показ уведомления
function showNotification(message, type = 'info', duration = 5000) {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
    alertDiv.style.top = '20px';
    alertDiv.style.right = '20px';
    alertDiv.style.zIndex = '9999';
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(alertDiv);
    
    // Автоматическое удаление
    setTimeout(() => {
        if (alertDiv.parentElement) {
            alertDiv.remove();
        }
    }, duration);
}

// Функции для работы с постами
function viewPost(postId) {
    makeAjaxRequest(`/api/posts`)
        .then(data => {
            const post = data.find(p => p.id === postId);
            if (post) {
                displayPostModal(post);
            }
        })
        .catch(error => {
            showNotification('Ошибка при загрузке поста', 'error');
        });
}

function displayPostModal(post) {
    const modal = document.getElementById('postModal');
    const content = document.getElementById('postContent');
    
    if (modal && content) {
        content.innerHTML = `
            <div class="row">
                <div class="col-md-6">
                    <h6><strong>Тема:</strong> ${post.topic}</h6>
                    <p><strong>Тон:</strong> <span class="badge bg-secondary">${post.tone}</span></p>
                    <p><strong>Статус:</strong> 
                        ${post.published ? 
                            '<span class="badge bg-success"><i class="fas fa-check me-1"></i>Опубликован</span>' : 
                            '<span class="badge bg-warning"><i class="fas fa-edit me-1"></i>Черновик</span>'
                        }
                    </p>
                    <p><strong>Создан:</strong> ${new Date(post.created_at).toLocaleString('ru-RU')}</p>
                    ${post.published_at ? `<p><strong>Опубликован:</strong> ${new Date(post.published_at).toLocaleString('ru-RU')}</p>` : ''}
                </div>
                <div class="col-md-6">
                    ${post.image_url ? 
                        `<img src="${post.image_url}" class="img-fluid rounded" alt="Изображение поста" style="max-height: 200px;">` : 
                        '<div class="text-muted text-center p-4 bg-light rounded"><i class="fas fa-image fa-3x"></i><br>Изображение не создано</div>'
                    }
                </div>
            </div>
            <hr>
            <h6><strong>Содержание поста:</strong></h6>
            <div class="bg-light p-3 rounded" style="white-space: pre-line;">${post.content}</div>
            ${post.image_description ? `
                <hr>
                <h6><strong>Описание изображения:</strong></h6>
                <p class="text-muted">${post.image_description}</p>
            ` : ''}
        `;
        
        const bsModal = new bootstrap.Modal(modal);
        bsModal.show();
    }
}

function deletePost(postId) {
    if (confirm('Вы уверены, что хотите удалить этот пост? Это действие нельзя отменить.')) {
        makeAjaxRequest(`/api/posts/${postId}`, { method: 'DELETE' })
            .then(() => {
                showNotification('Пост успешно удален', 'success');
                // Обновляем страницу
                setTimeout(() => location.reload(), 1000);
            })
            .catch(error => {
                showNotification('Ошибка при удалении поста', 'error');
            });
    }
}

// Функции для копирования в буфер обмена
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        showNotification('Скопировано в буфер обмена', 'success', 2000);
    }).catch(err => {
        console.error('Failed to copy: ', err);
        showNotification('Ошибка при копировании', 'error');
    });
}

// Экспорт функций для глобального использования
window.VKPostGenerator = {
    viewPost,
    deletePost,
    copyToClipboard,
    showNotification,
    makeAjaxRequest
};