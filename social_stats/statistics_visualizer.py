"""
Модуль для визуализации статистики публикаций
Генерирует HTML отчеты и графики
"""
from datetime import datetime
from typing import Dict, List
import json


class StatisticsVisualizer:
    """Класс для визуализации статистики в виде HTML отчетов"""
    
    @staticmethod
    def generate_dashboard(report_data: Dict, output_file: str = 'statistics_dashboard.html') -> str:
        """Генерирует HTML дашборд со статистикой"""
        
        summary = report_data.get('summary', {})
        posts = report_data.get('posts', [])
        group_info = report_data.get('group_info', {})
        
        html_content = f"""
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Статистика ВК Публикаций</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
            color: #333;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 12px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            overflow: hidden;
        }}
        
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }}
        
        .header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
        }}
        
        .header p {{
            font-size: 1.1em;
            opacity: 0.9;
        }}
        
        .content {{
            padding: 40px;
        }}
        
        .metrics-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 40px;
        }}
        
        .metric-card {{
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            padding: 25px;
            border-radius: 10px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
            border-left: 5px solid #667eea;
            transition: transform 0.3s ease;
        }}
        
        .metric-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
        }}
        
        .metric-card.likes {{
            border-left-color: #ff6b6b;
        }}
        
        .metric-card.comments {{
            border-left-color: #4ecdc4;
        }}
        
        .metric-card.views {{
            border-left-color: #ffd93d;
        }}
        
        .metric-card.subscribers {{
            border-left-color: #6bcf7f;
        }}
        
        .metric-label {{
            font-size: 0.9em;
            color: #666;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 10px;
        }}
        
        .metric-value {{
            font-size: 2.5em;
            font-weight: bold;
            color: #333;
            margin-bottom: 5px;
        }}
        
        .metric-detail {{
            font-size: 0.85em;
            color: #999;
        }}
        
        .charts-section {{
            margin-bottom: 40px;
        }}
        
        .charts-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 30px;
            margin-bottom: 30px;
        }}
        
        .chart-container {{
            background: #f9f9f9;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
            position: relative;
            height: 300px;
        }}
        
        .chart-title {{
            font-size: 1.1em;
            font-weight: 600;
            margin-bottom: 15px;
            color: #333;
        }}
        
        .posts-table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 30px;
        }}
        
        .posts-table thead {{
            background: #f0f0f0;
        }}
        
        .posts-table th {{
            padding: 15px;
            text-align: left;
            font-weight: 600;
            color: #333;
            border-bottom: 2px solid #ddd;
        }}
        
        .posts-table td {{
            padding: 12px 15px;
            border-bottom: 1px solid #eee;
        }}
        
        .posts-table tr:hover {{
            background: #f9f9f9;
        }}
        
        .stat-highlight {{
            font-weight: 600;
            color: #667eea;
        }}
        
        .footer {{
            background: #f5f5f5;
            padding: 20px 40px;
            text-align: center;
            color: #999;
            font-size: 0.9em;
            border-top: 1px solid #eee;
        }}
        
        .section-title {{
            font-size: 1.5em;
            font-weight: bold;
            margin-bottom: 25px;
            color: #333;
            border-bottom: 3px solid #667eea;
            padding-bottom: 10px;
        }}
        
        .engagement-rate {{
            display: inline-block;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 10px 15px;
            border-radius: 20px;
            font-weight: 600;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📊 Статистика ВК Публикаций</h1>
            <p>Анализ производительности постов вашей группы</p>
            <p style="font-size: 0.9em; margin-top: 10px;">Обновлено: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}</p>
        </div>
        
        <div class="content">
            <!-- ОСНОВНЫЕ МЕТРИКИ -->
            <div class="section-title">📈 Основные Метрики</div>
            <div class="metrics-grid">
                <div class="metric-card likes">
                    <div class="metric-label">👍 Лайки</div>
                    <div class="metric-value">{summary.get('total_likes', 0)}</div>
                    <div class="metric-detail">Среднее: {summary.get('avg_likes_per_post', 0)}/пост</div>
                </div>
                
                <div class="metric-card comments">
                    <div class="metric-label">💬 Комментарии</div>
                    <div class="metric-value">{summary.get('total_comments', 0)}</div>
                    <div class="metric-detail">Среднее: {summary.get('avg_comments_per_post', 0)}/пост</div>
                </div>
                
                <div class="metric-card views">
                    <div class="metric-label">👁️ Просмотры</div>
                    <div class="metric-value">{summary.get('total_views', 0)}</div>
                    <div class="metric-detail">Среднее: {summary.get('avg_views_per_post', 0)}/пост</div>
                </div>
                
                <div class="metric-card subscribers">
                    <div class="metric-label">👥 Подписчики</div>
                    <div class="metric-value">{group_info.get('subscribers', 0)}</div>
                    <div class="metric-detail">Активная аудитория</div>
                </div>
                
                <div class="metric-card">
                    <div class="metric-label">🔄 Репосты</div>
                    <div class="metric-value">{summary.get('total_reposts', 0)}</div>
                    <div class="metric-detail">Вирусность постов</div>
                </div>
                
                <div class="metric-card">
                    <div class="metric-label">💯 Вовлеченность</div>
                    <div class="metric-value"><span class="engagement-rate">{summary.get('engagement_rate', 0)}%</span></div>
                    <div class="metric-detail">Взаимодействие / Просмотры</div>
                </div>
            </div>
            
            <!-- ГРАФИКИ -->
            <div class="charts-section">
                <div class="section-title">📉 Анализ Данных</div>
                
                <div class="charts-grid">
                    <div class="chart-container">
                        <div class="chart-title">Распределение Лайков по Постам</div>
                        <canvas id="likesChart"></canvas>
                    </div>
                    
                    <div class="chart-container">
                        <div class="chart-title">Распределение Просмотров</div>
                        <canvas id="viewsChart"></canvas>
                    </div>
                </div>
                
                <div class="charts-grid">
                    <div class="chart-container">
                        <div class="chart-title">Метрики Взаимодействия</div>
                        <canvas id="engagementChart"></canvas>
                    </div>
                    
                    <div class="chart-container">
                        <div class="chart-title">Активность по Датам</div>
                        <canvas id="activityChart"></canvas>
                    </div>
                </div>
            </div>
            
            <!-- ТАБЛИЦА ПОСТОВ -->
            <div class="section-title">📋 Детальная Информация по Постам</div>
            <table class="posts-table">
                <thead>
                    <tr>
                        <th>#</th>
                        <th>📅 Дата</th>
                        <th>📝 Текст</th>
                        <th>👍 Лайки</th>
                        <th>💬 Комментарии</th>
                        <th>👁️ Просмотры</th>
                        <th>🔄 Репосты</th>
                    </tr>
                </thead>
                <tbody>
        """
        
        # Добавляем таблицу с постами
        for idx, post in enumerate(posts, 1):
            html_content += f"""
                    <tr>
                        <td>{idx}</td>
                        <td>{post.get('date', 'N/A')}</td>
                        <td>{post.get('text', 'N/A')}</td>
                        <td><span class="stat-highlight">{post.get('likes', 0)}</span></td>
                        <td>{post.get('comments', 0)}</td>
                        <td><span class="stat-highlight">{post.get('views', 0)}</span></td>
                        <td>{post.get('reposts', 0)}</td>
                    </tr>
            """
        
        html_content += """
                </tbody>
            </table>
        </div>
        
        <div class="footer">
            <p>📊 Статистика подготовлена автоматически | VK Publisher Analytics Dashboard</p>
        </div>
    </div>
    
    <script>
        const posts = JSON.parse('""" + json.dumps(posts) + """');
        
        // График лайков
        const likesCtx = document.getElementById('likesChart').getContext('2d');
        new Chart(likesCtx, {
            type: 'bar',
            data: {
                labels: posts.map((p, i) => `Пост ${i + 1}`),
                datasets: [{
                    label: 'Лайки',
                    data: posts.map(p => p.likes),
                    backgroundColor: '#ff6b6b',
                    borderRadius: 5,
                    tension: 0.4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: true }
                },
                scales: {
                    y: { beginAtZero: true }
                }
            }
        });
        
        // График просмотров
        const viewsCtx = document.getElementById('viewsChart').getContext('2d');
        new Chart(viewsCtx, {
            type: 'line',
            data: {
                labels: posts.map((p, i) => `Пост ${i + 1}`),
                datasets: [{
                    label: 'Просмотры',
                    data: posts.map(p => p.views),
                    borderColor: '#ffd93d',
                    backgroundColor: 'rgba(255, 217, 61, 0.1)',
                    borderWidth: 3,
                    fill: true,
                    tension: 0.4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: true }
                },
                scales: {
                    y: { beginAtZero: true }
                }
            }
        });
        
        // График вовлеченности
        const engagementCtx = document.getElementById('engagementChart').getContext('2d');
        new Chart(engagementCtx, {
            type: 'doughnut',
            data: {
                labels: ['Лайки', 'Комментарии', 'Репосты'],
                datasets: [{
                    data: [
                        posts.reduce((a, p) => a + p.likes, 0),
                        posts.reduce((a, p) => a + p.comments, 0),
                        posts.reduce((a, p) => a + p.reposts, 0)
                    ],
                    backgroundColor: [
                        '#ff6b6b',
                        '#4ecdc4',
                        '#95e1d3'
                    ],
                    borderColor: '#fff',
                    borderWidth: 2
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { position: 'bottom' }
                }
            }
        });
        
        // График активности по датам
        const activityCtx = document.getElementById('activityChart').getContext('2d');
        new Chart(activityCtx, {
            type: 'radar',
            data: {
                labels: ['Лайки', 'Комментарии', 'Просмотры', 'Репосты'],
                datasets: [{
                    label: 'Среднее по постам',
                    data: [
                        """ + str(summary.get('avg_likes_per_post', 0)) + """,
                        """ + str(summary.get('avg_comments_per_post', 0)) + """,
                        """ + str(summary.get('avg_views_per_post', 0) / 100) + """,
                        """ + str(summary.get('total_reposts', 0) / len(posts) if posts else 0) + """
                    ],
                    borderColor: '#667eea',
                    backgroundColor: 'rgba(102, 126, 234, 0.1)',
                    borderWidth: 2,
                    fill: true
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    r: {
                        beginAtZero: true
                    }
                }
            }
        });
    </script>
</body>
</html>
        """
        
        # Сохраняем файл
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return output_file
    
    @staticmethod
    def generate_csv_report(posts: List[Dict], output_file: str = 'statistics_report.csv') -> str:
        """Генерирует CSV отчет со статистикой"""
        
        csv_content = "Post ID,Date,Likes,Comments,Views,Reposts,Text\n"
        
        for post in posts:
            csv_content += f"{post.get('post_id', 'N/A')},"
            csv_content += f"{post.get('date', 'N/A')},"
            csv_content += f"{post.get('likes', 0)},"
            csv_content += f"{post.get('comments', 0)},"
            csv_content += f"{post.get('views', 0)},"
            csv_content += f"{post.get('reposts', 0)},"
            text = post.get('text', 'N/A').replace(',', ';').replace('\n', ' ')
            csv_content += f"\"{text}\"\n"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(csv_content)
        
        return output_file
    
    @staticmethod
    def print_summary(report_data: Dict) -> None:
        """Выводит сводку статистики в консоль"""
        
        summary = report_data.get('summary', {})
        group_info = report_data.get('group_info', {})
        
        print("\n" + "="*60)
        print("📊 СТАТИСТИКА ВК ПУБЛИКАЦИЙ".center(60))
        print("="*60)
        
        print(f"\n📈 ОСНОВНЫЕ МЕТРИКИ:")
        print(f"  👍 Всего лайков:          {summary.get('total_likes', 0)}")
        print(f"  💬 Всего комментариев:    {summary.get('total_comments', 0)}")
        print(f"  👁️  Всего просмотров:     {summary.get('total_views', 0)}")
        print(f"  🔄 Всего репостов:        {summary.get('total_reposts', 0)}")
        
        print(f"\n📊 СРЕДНЕЕ ПО ПОСТАМ:")
        print(f"  👍 Лайков/пост:           {summary.get('avg_likes_per_post', 0)}")
        print(f"  💬 Комментариев/пост:     {summary.get('avg_comments_per_post', 0)}")
        print(f"  👁️  Просмотров/пост:      {summary.get('avg_views_per_post', 0)}")
        
        print(f"\n👥 ИНФОРМАЦИЯ О ГРУППЕ:")
        print(f"  Подписчиков:              {group_info.get('subscribers', 0)}")
        
        print(f"\n💯 ВОВЛЕЧЕННОСТЬ:")
        print(f"  Engagement Rate:          {summary.get('engagement_rate', 0)}%")
        
        print("\n" + "="*60 + "\n")