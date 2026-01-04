// 全局变量
let currentTab = 'overview';
let musicTypeData = null;
let albumTypeData = null;
let publishTrendData = null;
let topArtistsData = null;
let sentimentData = null;

// 颜色方案
const colors = ['#667eea', '#f093fb', '#4facfe', '#43e97b', '#fa709a', '#feca57', '#48dbfb', '#ff9ff3', '#54a0ff', '#00d2d3'];

// 页面加载时初始化
window.addEventListener('DOMContentLoaded', function() {
    console.log('页面加载完成，开始初始化...');
    checkStatus();
    loadAllData();
});

// 检查数据状态
async function checkStatus() {
    try {
        const response = await fetch('/api/status');
        const data = await response.json();
        
        const statusElement = document.getElementById('dataStatus');
        const sourceElement = document.getElementById('dataSource');
        
        if (data.loaded) {
            statusElement.textContent = '✓ 已加载';
            statusElement.classList.add('loaded');
            statusElement.classList.remove('error');
            
            if (data.is_netease_data) {
                sourceElement.textContent = '网易云音乐';
                sourceElement.classList.add('loaded');
            } else {
                sourceElement.textContent = 'Spotify';
                sourceElement.classList.add('loaded');
            }
        } else {
            statusElement.textContent = '✗ 未加载';
            statusElement.classList.add('error');
            statusElement.classList.remove('loaded');
            showDataFileInfo();
        }
    } catch (error) {
        console.error('检查状态失败:', error);
    }
}

// 加载所有数据
async function loadAllData() {
    await loadMusicTypeData();
    await loadAlbumTypeData();
    await loadPublishTrendData();
    await loadTopArtistsData();
    await loadSentimentData();
    await loadWordcloud();
}

// 加载音乐类型数据
async function loadMusicTypeData() {
    try {
        const response = await fetch('/api/music-type-distribution');
        if (response.ok) {
            musicTypeData = await response.json();
            renderMusicTypeChart();
        }
    } catch (error) {
        console.error('加载音乐类型数据失败:', error);
    }
}

// 加载专辑类型数据
async function loadAlbumTypeData() {
    try {
        const response = await fetch('/api/album-type-analysis');
        if (response.ok) {
            albumTypeData = await response.json();
            renderAlbumTypeChart();
            renderAlbumStatsTable();
        }
        
        const top10Response = await fetch('/api/album-type-top10');
        if (top10Response.ok) {
            const top10Data = await top10Response.json();
            renderAlbumTop10Chart(top10Data);
        }
    } catch (error) {
        console.error('加载专辑类型数据失败:', error);
    }
}

// 加载发布趋势数据
async function loadPublishTrendData() {
    try {
        const response = await fetch('/api/publish-trend');
        if (response.ok) {
            publishTrendData = await response.json();
            renderPublishTrendChart();
        }
    } catch (error) {
        console.error('加载发布趋势数据失败:', error);
    }
}

// 加载TOP作者数据
async function loadTopArtistsData() {
    try {
        const response = await fetch('/api/top-artists?top=5');
        if (response.ok) {
            topArtistsData = await response.json();
            renderTopArtistsChart();
            renderArtistsTable();
        }
    } catch (error) {
        console.error('加载作者数据失败:', error);
    }
}

// 加载情感分析数据
async function loadSentimentData() {
    try {
        const response = await fetch('/api/sentiment-trend');
        if (response.ok) {
            sentimentData = await response.json();
            renderSentimentDistChart();
            renderSentimentTrendChart();
        }
    } catch (error) {
        console.error('加载情感数据失败:', error);
    }
}

// 加载词云图
async function loadWordcloud() {
    try {
        const response = await fetch('/api/wordcloud');
        if (response.ok) {
            const data = await response.json();
            const container = document.getElementById('wordcloudContainer');
            
            if (data.image) {
                if (typeof data.image === 'string' && data.image.startsWith('data:image')) {
                    // Base64图片
                    container.innerHTML = `<img src="${data.image}" alt="词云图">`;
                } else if (data.image.word_freq) {
                    // Fallback: 显示词频列表
                    renderWordFrequencyFallback(data.image.word_freq, container);
                }
            }
        }
    } catch (error) {
        console.error('加载词云图失败:', error);
    }
}

// 渲染音乐类型饼图
function renderMusicTypeChart() {
    if (!musicTypeData || typeof Plotly === 'undefined') return;
    
    const data = [{
        values: musicTypeData.map(d => d.count),
        labels: musicTypeData.map(d => d.type),
        type: 'pie',
        marker: {
            colors: colors
        },
        textinfo: 'label+percent',
        textposition: 'auto',
        hovertemplate: '%{label}<br>数量: %{value}<br>占比: %{percent}<extra></extra>'
    }];
    
    const layout = {
        margin: { t: 20, b: 20, l: 20, r: 20 },
        showlegend: true,
        legend: {
            orientation: 'v',
            x: 1,
            y: 1
        }
    };
    
    Plotly.newPlot('musicTypeChart', data, layout, {responsive: true});
}

// 渲染专辑类型柱状图
function renderAlbumTypeChart() {
    if (!albumTypeData || typeof Plotly === 'undefined') return;
    
    const data = [{
        x: albumTypeData.map(d => d.type),
        y: albumTypeData.map(d => d.count),
        type: 'bar',
        marker: {
            color: albumTypeData.map((_, i) => colors[i % colors.length])
        },
        text: albumTypeData.map(d => d.count),
        textposition: 'auto',
        hovertemplate: '%{x}<br>数量: %{y}<br>平均人气: %{customdata:.1f}<extra></extra>',
        customdata: albumTypeData.map(d => d.avg_popularity)
    }];
    
    const layout = {
        margin: { t: 20, b: 80, l: 60, r: 20 },
        xaxis: {
            title: '专辑类型',
            tickangle: -45
        },
        yaxis: {
            title: '数量'
        }
    };
    
    Plotly.newPlot('albumTypeChart', data, layout, {responsive: true});
}

// 渲染专辑TOP10图表
function renderAlbumTop10Chart(data) {
    if (!data || typeof Plotly === 'undefined') return;
    
    const chartData = [{
        x: data.map(d => d.count),
        y: data.map(d => d.type),
        type: 'bar',
        orientation: 'h',
        marker: {
            color: data.map((_, i) => colors[i % colors.length])
        },
        text: data.map(d => `${d.percentage.toFixed(1)}%`),
        textposition: 'auto'
    }];
    
    const layout = {
        margin: { t: 20, b: 40, l: 120, r: 40 },
        xaxis: {
            title: '数量'
        },
        yaxis: {
            automargin: true
        }
    };
    
    Plotly.newPlot('albumTop10Chart', chartData, layout, {responsive: true});
}

// 渲染专辑统计表格
function renderAlbumStatsTable() {
    if (!albumTypeData) return;
    
    const container = document.getElementById('albumStatsTable');
    let html = '<table><thead><tr>';
    html += '<th>专辑类型</th><th>数量</th><th>占比</th><th>平均人气</th>';
    html += '</tr></thead><tbody>';
    
    albumTypeData.forEach(item => {
        html += '<tr>';
        html += `<td><strong>${item.type}</strong></td>`;
        html += `<td>${item.count}</td>`;
        html += `<td>${item.percentage.toFixed(1)}%</td>`;
        html += `<td>${item.avg_popularity.toFixed(1)}</td>`;
        html += '</tr>';
    });
    
    html += '</tbody></table>';
    container.innerHTML = html;
}

// 渲染发布趋势折线图
function renderPublishTrendChart() {
    if (!publishTrendData || typeof Plotly === 'undefined') return;
    
    const data = [{
        x: publishTrendData.map(d => d.year),
        y: publishTrendData.map(d => d.count),
        type: 'scatter',
        mode: 'lines+markers',
        line: {
            color: '#667eea',
            width: 3
        },
        marker: {
            size: 8,
            color: '#764ba2'
        },
        fill: 'tozeroy',
        fillcolor: 'rgba(102, 126, 234, 0.2)',
        hovertemplate: '年份: %{x}<br>发布数量: %{y}<extra></extra>'
    }];
    
    const layout = {
        margin: { t: 20, b: 60, l: 60, r: 40 },
        xaxis: {
            title: '年份',
            tickmode: 'linear',
            dtick: 2
        },
        yaxis: {
            title: '发布数量'
        },
        hovermode: 'closest'
    };
    
    Plotly.newPlot('publishTrendChart', data, layout, {responsive: true});
}

// 渲染TOP作者图表
function renderTopArtistsChart() {
    if (!topArtistsData || typeof Plotly === 'undefined') return;
    
    const data = [{
        x: topArtistsData.map(d => d.artist),
        y: topArtistsData.map(d => d.count),
        type: 'bar',
        marker: {
            color: topArtistsData.map((_, i) => colors[i % colors.length]),
            line: {
                color: 'white',
                width: 2
            }
        },
        text: topArtistsData.map(d => d.count),
        textposition: 'auto',
        hovertemplate: '%{x}<br>作品数: %{y}<br>平均人气: %{customdata:.1f}<extra></extra>',
        customdata: topArtistsData.map(d => d.avg_popularity)
    }];
    
    const layout = {
        margin: { t: 20, b: 100, l: 60, r: 40 },
        xaxis: {
            title: '作者',
            tickangle: -45
        },
        yaxis: {
            title: '作品数量'
        }
    };
    
    Plotly.newPlot('topArtistsChart', data, layout, {responsive: true});
}

// 渲染作者表格
function renderArtistsTable() {
    if (!topArtistsData) return;
    
    const container = document.getElementById('artistsTable');
    let html = '<table><thead><tr>';
    html += '<th>排名</th><th>作者</th><th>作品数量</th><th>平均人气</th>';
    html += '</tr></thead><tbody>';
    
    topArtistsData.forEach((artist, index) => {
        html += '<tr>';
        html += `<td><strong>${index + 1}</strong></td>`;
        html += `<td>${artist.artist}</td>`;
        html += `<td>${artist.count}</td>`;
        html += `<td>${artist.avg_popularity.toFixed(1)}</td>`;
        html += '</tr>';
    });
    
    html += '</tbody></table>';
    container.innerHTML = html;
}

// 渲染情感分布饼图
function renderSentimentDistChart() {
    if (!sentimentData || typeof Plotly === 'undefined') return;
    
    const data = [{
        values: [sentimentData.positive, sentimentData.neutral, sentimentData.negative],
        labels: ['积极', '中性', '消极'],
        type: 'pie',
        marker: {
            colors: ['#43e97b', '#feca57', '#fa709a']
        },
        textinfo: 'label+percent',
        textposition: 'auto'
    }];
    
    const layout = {
        margin: { t: 20, b: 20, l: 20, r: 20 }
    };
    
    Plotly.newPlot('sentimentDistChart', data, layout, {responsive: true});
}

// 渲染情感趋势图
function renderSentimentTrendChart() {
    if (!sentimentData || !sentimentData.trend || typeof Plotly === 'undefined') return;
    
    const dates = sentimentData.trend.map(d => d.date);
    
    const data = [
        {
            x: dates,
            y: sentimentData.trend.map(d => d.positive),
            name: '积极',
            type: 'scatter',
            mode: 'lines+markers',
            line: { color: '#43e97b', width: 2 },
            marker: { size: 6 }
        },
        {
            x: dates,
            y: sentimentData.trend.map(d => d.neutral),
            name: '中性',
            type: 'scatter',
            mode: 'lines+markers',
            line: { color: '#feca57', width: 2 },
            marker: { size: 6 }
        },
        {
            x: dates,
            y: sentimentData.trend.map(d => d.negative),
            name: '消极',
            type: 'scatter',
            mode: 'lines+markers',
            line: { color: '#fa709a', width: 2 },
            marker: { size: 6 }
        }
    ];
    
    const layout = {
        margin: { t: 20, b: 60, l: 60, r: 40 },
        xaxis: {
            title: '时间'
        },
        yaxis: {
            title: '百分比 (%)'
        },
        hovermode: 'x unified',
        legend: {
            orientation: 'h',
            y: -0.2
        }
    };
    
    Plotly.newPlot('sentimentTrendChart', data, layout, {responsive: true});
}

// Fallback: 词频列表
function renderWordFrequencyFallback(wordFreq, container) {
    let html = '<div style="padding: 20px;"><h4 style="text-align: center; color: #667eea; margin-bottom: 20px;">热门关键词</h4>';
    html += '<div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(150px, 1fr)); gap: 10px;">';
    
    const sortedWords = Object.entries(wordFreq).sort((a, b) => b[1] - a[1]).slice(0, 30);
    const maxCount = sortedWords[0][1];
    
    sortedWords.forEach(([word, count]) => {
        const fontSize = 0.8 + (count / maxCount) * 1.5;
        html += `<div style="text-align: center; padding: 10px; background: #f8f9fa; border-radius: 8px;">
            <div style="font-size: ${fontSize}em; font-weight: bold; color: #667eea;">${word}</div>
            <div style="font-size: 0.8em; color: #666;">${count}次</div>
        </div>`;
    });
    
    html += '</div></div>';
    container.innerHTML = html;
}

// 切换标签页
function showTab(tabName) {
    // 隐藏所有标签页
    document.querySelectorAll('.tab-content').forEach(tab => {
        tab.classList.remove('active');
    });
    
    // 移除所有按钮的active类
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    
    // 显示选中的标签页
    document.getElementById('tab-' + tabName).classList.add('active');
    
    // 激活对应的按钮 - 通过tabName查找对应按钮
    const buttons = document.querySelectorAll('.tab-btn');
    buttons.forEach(btn => {
        if (btn.textContent.includes(getTabIcon(tabName))) {
            btn.classList.add('active');
        }
    });
    
    currentTab = tabName;
}

// 获取标签页图标
function getTabIcon(tabName) {
    const icons = {
        'overview': '📊 数据概览',
        'album': '💿 专辑分析',
        'trend': '📈 发布趋势',
        'artists': '👨‍🎤 作者分析',
        'sentiment': '💭 情感分析'
    };
    return icons[tabName] || '';
}

// 重新加载数据
async function reloadData() {
    const btn = document.getElementById('reloadBtn');
    btn.disabled = true;
    btn.textContent = '🔄 加载中...';
    
    try {
        const response = await fetch('/api/reload');
        const data = await response.json();
        
        if (data.success) {
            await checkStatus();
            await loadAllData();
            showSuccess('数据重新加载成功！');
        } else {
            showError('数据加载失败，请检查数据文件');
        }
    } catch (error) {
        console.error('重新加载失败:', error);
        showError('重新加载时发生错误');
    } finally {
        btn.disabled = false;
        btn.textContent = '🔄 重新加载数据';
    }
}

// 显示错误消息
function showError(message) {
    alert('错误: ' + message);
}

// 显示成功消息
function showSuccess(message) {
    alert('成功: ' + message);
}

// 显示数据文件信息
function showDataFileInfo() {
    const container = document.getElementById('musicTypeChart');
    if (container) {
        container.innerHTML = `
            <div class="info-message">
                <h3>📁 数据文件未找到</h3>
                <p><strong>请运行以下命令生成数据:</strong></p>
                <p><code>python netease_scraper.py</code></p>
                <p>这将生成示例数据或爬取真实的网易云音乐数据</p>
            </div>
        `;
    }
}
