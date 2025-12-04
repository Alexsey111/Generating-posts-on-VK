"""
Пример использования модулей статистики
Демонстрирует сбор и отображение статистики постов
"""
from post_statistics import PostStatistics
from statistics_visualizer import StatisticsVisualizer
import config as conf


def collect_and_display_statistics():
    """Собирает статистику и генерирует отчеты"""
    
    print("🔄 Инициализация сбора статистики...")
    
    # Инициализируем класс статистики
    stats = PostStatistics(conf.vk_api_key, conf.vk_group_id)
    
    try:
        # Получаем детальный отчет по последним 20 постам
        print("📊 Сбор информации о последних постах...")
        report = stats.get_detailed_report(num_posts=20)
        
        # Выводим сводку в консоль
        print("\n✅ Статистика собрана успешно!")
        StatisticsVisualizer.print_summary(report)
        
        # Генерируем HTML дашборд
        print("🎨 Генерирование HTML дашборда...")
        dashboard_file = StatisticsVisualizer.generate_dashboard(
            report, 
            output_file='vk_statistics_dashboard.html'
        )
        print(f"✅ HTML дашборд создан: {dashboard_file}")
        
        # Генерируем CSV отчет
        print("📄 Генерирование CSV отчета...")
        csv_file = StatisticsVisualizer.generate_csv_report(
            report.get('posts', []),
            output_file='vk_statistics_report.csv'
        )
        print(f"✅ CSV отчет создан: {csv_file}")
        
        return report
        
    except Exception as e:
        print(f"❌ Ошибка при сборе статистики: {e}")
        return None


def get_single_post_analysis(post_id: int):
    """Анализ одного конкретного поста"""
    
    print(f"\n🔍 Анализ поста #{post_id}...")
    
    stats = PostStatistics(conf.vk_api_key, conf.vk_group_id)
    
    try:
        # Получаем статистику поста
        post_stat = stats.get_post_stats(post_id)
        
        if not post_stat:
            print("❌ Пост не найден")
            return None
        
        print("\n" + "="*50)
        print("📊 СТАТИСТИКА ПОСТА".center(50))
        print("="*50)
        print(f"Post ID:      {post_stat.get('post_id')}")
        print(f"Дата:         {post_stat.get('date')}")
        print(f"Текст:        {post_stat.get('text')}")
        print(f"👍 Лайки:     {post_stat.get('likes')}")
        print(f"💬 Комментарии: {post_stat.get('comments')}")
        print(f"🔄 Репосты:   {post_stat.get('reposts')}")
        print(f"👁️ Просмотры: {post_stat.get('views')}")
        print("="*50 + "\n")
        
        return post_stat
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return None


def get_group_analytics(days: int = 30):
    """Получить статистику группы за период"""
    
    from datetime import datetime, timedelta
    
    print(f"\n📈 Получение статистики группы за последние {days} дней...")
    
    stats = PostStatistics(conf.vk_api_key, conf.vk_group_id)
    
    try:
        # Вычисляем даты
        date_to = datetime.now()
        date_from = date_to - timedelta(days=days)
        
        # Получаем статистику
        group_stats = stats.get_group_stats(
            date_from=date_from.strftime('%Y-%m-%d'),
            date_to=date_to.strftime('%Y-%m-%d')
        )
        
        print("\n" + "="*50)
        print(f"📊 СТАТИСТИКА ГРУППЫ ({days} дней)".center(50))
        print("="*50)
        print(f"Период:               {group_stats.get('period')}")
        print(f"👁️ Просмотры:         {group_stats.get('views')}")
        print(f"👤 Посетители:        {group_stats.get('visitors')}")
        print(f"📢 Охват:             {group_stats.get('reach')}")
        print(f"👥 Охват подписчиков: {group_stats.get('reach_subscribers')}")
        print(f"👍 Позитивные:        {group_stats.get('positive_feedback')}")
        print(f"👎 Негативные:        {group_stats.get('negative_feedback')}")
        print("="*50 + "\n")
        
        return group_stats
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return None


def get_followers():
    """Получить количество подписчиков"""
    
    print("\n👥 Получение количества подписчиков...")
    
    stats = PostStatistics(conf.vk_api_key, conf.vk_group_id)
    
    try:
        followers = stats.get_followers_count()
        print(f"✅ Подписчиков: {followers}")
        return followers
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return None


def interactive_menu():
    """Интерактивное меню для выбора операций"""
    
    print("\n" + "="*60)
    print("🎯 СТАТИСТИКА ВК ПУБЛИКАЦИЙ - ИНТЕРАКТИВНОЕ МЕНЮ".center(60))
    print("="*60)
    print("""
1. 📊 Получить полный отчет со статистикой (последние 20 постов)
2. 🔍 Анализ одного поста
3. 📈 Статистика группы за период
4. 👥 Количество подписчиков
5. ❌ Выход
    """)
    print("="*60)
    
    choice = input("Выберите опцию (1-5): ").strip()
    
    if choice == '1':
        collect_and_display_statistics()
    elif choice == '2':
        try:
            post_id = int(input("Введите ID поста: "))
            get_single_post_analysis(post_id)
        except ValueError:
            print("❌ Некорректный ID поста")
    elif choice == '3':
        try:
            days = int(input("Количество дней для анализа (по умолчанию 30): ") or "30")
            get_group_analytics(days)
        except ValueError:
            print("❌ Некорректное значение")
    elif choice == '4':
        get_followers()
    elif choice == '5':
        print("👋 До свидания!")
        return False
    else:
        print("❌ Некорректный выбор")
    
    return True


if __name__ == "__main__":
    print("""
    
    ╔════════════════════════════════════════════════════════╗
    ║   📊 VK Publisher - Статистика Публикаций              ║
    ║   Версия 1.0                                           ║
    ╚════════════════════════════════════════════════════════╝
    
    """)
    
    # Запускаем полный отчет по умолчанию
    print("🚀 Запуск автоматического сбора статистики...\n")
    collect_and_display_statistics()
    
    # Интерактивное меню
    while True:
        if not interactive_menu():
            break
        input("\nНажмите Enter для продолжения...")