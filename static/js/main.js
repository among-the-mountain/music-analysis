// 全局变量
let clusterStats = null;
let clusterSamples = null;

// 颜色方案
const colors = [
    '#667eea',
    '#f093fb',
    '#4facfe',
    '#43e97b',
    '#fa709a'
];

// 情绪簇名称映射
const clusterNames = [
    '高能激情簇',
    '轻松愉悦簇',
    '平静内敛簇',
    '活力舞曲簇',
    '深沉情感簇'
];

// 特征中文名称映射
const featureNames = {
    'danceability': '舞曲性',
    'energy': '能量值',
    'valence': '快乐度',
    'acousticness': '原声度',
    'instrumentalness': '器乐度',
    'liveness': '现场感',
    'speechiness': '语音度'
};

// 页面加载时初始化
window.addEventListener('DOMContentLoaded', function() {
    console.log('页面加载完成，开始初始化...');
    checkStatus();
    loadData();
});

// 检查数据状态
async function checkStatus() {
    try {
        const response = await fetch('/api/status');
        const data = await response.json();
        
        const statusElement = document.getElementById('dataStatus');
        if (data.loaded) {
            statusElement.textContent = '✓ 已加载';
            statusElement.classList.add('loaded');
            statusElement.classList.remove('error');
        } else if (!data.file_exists) {
            statusElement.textContent = '✗ 数据文件不存在';
            statusElement.classList.add('error');
            statusElement.classList.remove('loaded');
            showDataFileInfo();
        } else {
            statusElement.textContent = '✗ 未加载';
            statusElement.classList.add('error');
            statusElement.classList.remove('loaded');
        }
    } catch (error) {
        console.error('检查状态失败:', error);
    }
}

// 加载所有数据
async function loadData() {
    try {
        // 加载聚类统计
        const statsResponse = await fetch('/api/cluster-stats');
        if (statsResponse.ok) {
            clusterStats = await statsResponse.json();
            console.log('聚类统计数据:', clusterStats);
            renderCharts();
            renderStats();
        } else {
            showError('无法加载数据，请确保数据文件存在并已正确加载');
        }
        
        // 加载样本音乐
        const samplesResponse = await fetch('/api/cluster-samples?n=8');
        if (samplesResponse.ok) {
            clusterSamples = await samplesResponse.json();
            console.log('样本数据:', clusterSamples);
            renderSamples();
        }
    } catch (error) {
        console.error('加载数据失败:', error);
        showError('加载数据时发生错误');
    }
}

// 渲染图表
function renderCharts() {
    if (!clusterStats) return;
    
    renderRadarChart();
    renderScatterChart();
}

// 渲染雷达图
function renderRadarChart() {
    if (typeof Plotly === 'undefined') {
        renderRadarChartFallback();
        return;
    }
    
    const traces = clusterStats.map((cluster, index) => {
        const features = cluster.features;
        const featureKeys = Object.keys(features);
        
        return {
            type: 'scatterpolar',
            r: featureKeys.map(key => features[key]),
            theta: featureKeys.map(key => featureNames[key] || key),
            fill: 'toself',
            name: clusterNames[index] || `簇 ${index}`,
            line: {
                color: colors[index % colors.length]
            },
            fillcolor: colors[index % colors.length],
            opacity: 0.6
        };
    });
    
    const layout = {
        polar: {
            radialaxis: {
                visible: true,
                range: [0, 1]
            }
        },
        showlegend: true,
        legend: {
            orientation: 'h',
            y: -0.2
        },
        margin: {
            l: 80,
            r: 80,
            t: 40,
            b: 80
        }
    };
    
    Plotly.newPlot('radarChart', traces, layout, {responsive: true});
}

// 渲染散点图
function renderScatterChart() {
    if (typeof Plotly === 'undefined') {
        renderScatterChartFallback();
        return;
    }
    
    const traces = clusterStats.map((cluster, index) => {
        const features = cluster.features;
        
        return {
            x: [features.energy || 0],
            y: [features.valence || 0],
            mode: 'markers',
            type: 'scatter',
            name: clusterNames[index] || `簇 ${index}`,
            marker: {
                size: [cluster.count / 10],
                sizemode: 'diameter',
                sizeref: 2,
                color: colors[index % colors.length],
                line: {
                    color: 'white',
                    width: 2
                }
            },
            text: `${clusterNames[index]}<br>数量: ${cluster.count}`,
            hovertemplate: '%{text}<br>能量值: %{x:.2f}<br>快乐度: %{y:.2f}<extra></extra>'
        };
    });
    
    const layout = {
        title: '',
        xaxis: {
            title: '能量值 (Energy)',
            range: [0, 1],
            gridcolor: '#e5e5e5'
        },
        yaxis: {
            title: '快乐度 (Valence)',
            range: [0, 1],
            gridcolor: '#e5e5e5'
        },
        showlegend: true,
        legend: {
            orientation: 'h',
            y: -0.2
        },
        plot_bgcolor: '#f8f9fa',
        margin: {
            l: 60,
            r: 40,
            t: 40,
            b: 80
        }
    };
    
    Plotly.newPlot('scatterChart', traces, layout, {responsive: true});
}

// 渲染统计信息
function renderStats() {
    if (!clusterStats) return;
    
    const container = document.getElementById('statsContainer');
    container.innerHTML = '';
    
    clusterStats.forEach((cluster, index) => {
        const card = document.createElement('div');
        card.className = 'stat-card';
        card.style.borderLeftColor = colors[index % colors.length];
        
        const features = cluster.features;
        const featureItems = Object.keys(features)
            .map(key => `
                <li>
                    <span class="feature-name">${featureNames[key] || key}</span>
                    <span class="feature-value">${features[key].toFixed(3)}</span>
                </li>
            `).join('');
        
        card.innerHTML = `
            <h3>${clusterNames[index] || `簇 ${index}`}</h3>
            <div class="stat-count">音乐数量: ${cluster.count} 首</div>
            <ul class="feature-list">
                ${featureItems}
            </ul>
        `;
        
        container.appendChild(card);
    });
}

// 渲染样本音乐
function renderSamples() {
    if (!clusterSamples) return;
    
    const container = document.getElementById('samplesContainer');
    container.innerHTML = '';
    container.className = 'samples-container';
    
    clusterSamples.forEach((clusterData, index) => {
        const clusterDiv = document.createElement('div');
        clusterDiv.className = 'cluster-samples';
        
        let tracksHtml = '';
        clusterData.tracks.forEach(track => {
            const featureBadges = Object.keys(track)
                .filter(key => key !== 'name' && key !== 'artists' && featureNames[key])
                .slice(0, 3) // 只显示前3个特征
                .map(key => `
                    <span class="feature-badge">${featureNames[key]}: ${track[key].toFixed(2)}</span>
                `).join('');
            
            tracksHtml += `
                <div class="track-item">
                    <div class="track-name">${track.name}</div>
                    <div class="track-artist">🎤 ${track.artists}</div>
                    <div class="track-features">${featureBadges}</div>
                </div>
            `;
        });
        
        clusterDiv.innerHTML = `
            <h3>${clusterNames[index] || `簇 ${index}`}</h3>
            ${tracksHtml}
        `;
        
        container.appendChild(clusterDiv);
    });
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
            await loadData();
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
    const container = document.getElementById('statsContainer');
    if (container) {
        container.innerHTML = `
            <div class="error-message">
                <strong>错误:</strong> ${message}
            </div>
        `;
    }
}

// 显示成功消息
function showSuccess(message) {
    // 可以实现一个toast通知
    console.log('成功:', message);
}

// 显示数据文件信息
function showDataFileInfo() {
    const container = document.getElementById('statsContainer');
    if (container) {
        container.innerHTML = `
            <div class="info-message">
                <h3>📁 如何获取数据文件</h3>
                <p><strong>步骤 1:</strong> 访问 Kaggle 下载 Spotify Tracks Dataset</p>
                <p><strong>步骤 2:</strong> 将下载的 CSV 文件重命名为 <code>spotify_tracks.csv</code></p>
                <p><strong>步骤 3:</strong> 将文件放置在项目根目录</p>
                <p><strong>步骤 4:</strong> 点击"重新加载数据"按钮</p>
                <br>
                <p>推荐数据集: <a href="https://www.kaggle.com/datasets/maharshipandya/-spotify-tracks-dataset" target="_blank">Spotify Tracks Dataset on Kaggle</a></p>
            </div>
        `;
    }
}

// Fallback 雷达图（使用 HTML/CSS）
function renderRadarChartFallback() {
    const container = document.getElementById('radarChart');
    let html = '<div class="fallback-chart"><h4 style="text-align: center; color: #667eea;">情绪簇特征对比表</h4>';
    html += '<table style="width: 100%; border-collapse: collapse; margin-top: 20px;">';
    html += '<thead><tr style="background: #667eea; color: white;"><th style="padding: 10px; border: 1px solid #ddd;">簇名称</th>';
    
    const firstCluster = clusterStats[0];
    const featureKeys = Object.keys(firstCluster.features);
    featureKeys.forEach(key => {
        html += `<th style="padding: 10px; border: 1px solid #ddd;">${featureNames[key]}</th>`;
    });
    html += '</tr></thead><tbody>';
    
    clusterStats.forEach((cluster, index) => {
        html += `<tr style="background: ${index % 2 === 0 ? '#f8f9fa' : 'white'};">`;
        html += `<td style="padding: 10px; border: 1px solid #ddd; font-weight: bold; color: ${colors[index]}">${clusterNames[index]}</td>`;
        featureKeys.forEach(key => {
            const value = cluster.features[key];
            const percentage = (value * 100).toFixed(1);
            html += `<td style="padding: 10px; border: 1px solid #ddd; text-align: center;">
                <div style="background: #e0e7ff; height: 20px; width: 100%; border-radius: 10px; overflow: hidden;">
                    <div style="background: ${colors[index]}; height: 100%; width: ${percentage}%;"></div>
                </div>
                <small>${value.toFixed(3)}</small>
            </td>`;
        });
        html += '</tr>';
    });
    
    html += '</tbody></table></div>';
    container.innerHTML = html;
}

// Fallback 散点图（使用 HTML/CSS）
function renderScatterChartFallback() {
    const container = document.getElementById('scatterChart');
    let html = '<div class="fallback-chart"><h4 style="text-align: center; color: #667eea;">能量值 vs 快乐度分布</h4>';
    html += '<div style="position: relative; width: 100%; height: 350px; border: 2px solid #e5e5e5; border-radius: 10px; margin-top: 20px; background: #f8f9fa;">';
    
    // 添加坐标轴
    html += '<div style="position: absolute; bottom: 0; left: 0; right: 0; height: 2px; background: #333;"></div>';
    html += '<div style="position: absolute; bottom: 0; left: 0; top: 0; width: 2px; background: #333;"></div>';
    html += '<div style="position: absolute; bottom: -25px; right: 10px; font-size: 12px; color: #666;">能量值 (Energy) →</div>';
    html += '<div style="position: absolute; top: 10px; left: -80px; font-size: 12px; color: #666; transform: rotate(-90deg); transform-origin: left;">快乐度 (Valence) →</div>';
    
    // 添加数据点
    clusterStats.forEach((cluster, index) => {
        const energy = cluster.features.energy || 0;
        const valence = cluster.features.valence || 0;
        const x = energy * 90 + 5; // 5-95%
        const y = (1 - valence) * 90 + 5; // 倒置Y轴
        const size = Math.max(20, Math.min(60, cluster.count / 20));
        
        html += `<div style="position: absolute; left: ${x}%; bottom: ${100-y}%; 
                 width: ${size}px; height: ${size}px; 
                 background: ${colors[index]}; 
                 border-radius: 50%; 
                 border: 2px solid white;
                 box-shadow: 0 2px 5px rgba(0,0,0,0.2);
                 transform: translate(-50%, 50%);
                 display: flex; align-items: center; justify-content: center;
                 font-size: 10px; color: white; font-weight: bold;
                 cursor: pointer;"
                 title="${clusterNames[index]}\n数量: ${cluster.count}\n能量值: ${energy.toFixed(2)}\n快乐度: ${valence.toFixed(2)}">
                 ${index+1}
                 </div>`;
    });
    
    html += '</div>';
    
    // 添加图例
    html += '<div style="margin-top: 20px; display: flex; flex-wrap: wrap; gap: 10px; justify-content: center;">';
    clusterStats.forEach((cluster, index) => {
        html += `<div style="display: flex; align-items: center; gap: 5px;">
                 <div style="width: 15px; height: 15px; background: ${colors[index]}; border-radius: 50%;"></div>
                 <span style="font-size: 12px;">${clusterNames[index]} (${cluster.count})</span>
                 </div>`;
    });
    html += '</div></div>';
    
    container.innerHTML = html;
}
