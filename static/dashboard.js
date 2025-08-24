async function fetchLatest() {
    try {
        // Show refresh indicator
        const refreshIndicator = document.getElementById('refresh-indicator');
        if (refreshIndicator) {
            refreshIndicator.style.display = 'inline-block';
        }
        
        const res = await fetch('/api/today/latest');
        if (!res.ok) return;
        const data = await res.json();
        
        let totalTemps = [];
        let feverCount = 0;
        
        for (const [workerId, payload] of Object.entries(data)) {
            const row = document.querySelector(`tr[data-worker-id="${workerId}"]`);
            if (!row) continue;
            
            const tempCell = row.querySelector('.temp');
            const timeCell = row.querySelector('.time');
            const statusCell = row.querySelector('.status');
            
            if (payload.temperature_c !== null && payload.temperature_c !== undefined) {
                const temp = Number(payload.temperature_c);
                totalTemps.push(temp);
                
                // Update temperature display with elegant badge and visual thermometer
                const tempIcon = tempCell.querySelector('i');
                tempCell.innerHTML = `
                    <div class="flex items-center space-x-3">
                        <div class="temp-visual" style="background: linear-gradient(to top, 
                            ${temp >= 38 ? '#ef4444' : temp >= 37.5 ? '#f59e0b' : '#10b981'} 0%, 
                            ${temp >= 37 ? '#f59e0b' : '#10b981'} 50%, 
                            #10b981 100%)"></div>
                        <div>
                            <span class="temp-indicator ${
                                temp >= 38 ? 'temp-danger-badge' : 
                                temp >= 37.5 ? 'temp-warning-badge' : 'temp-normal-badge'
                            }">
                                ${temp.toFixed(1)}°C
                            </span>
                            <p class="text-xs text-slate-500 mt-0.5">
                                ${temp >= 38 ? 'Critical' : temp >= 37.5 ? 'Elevated' : 'Normal'}
                            </p>
                        </div>
                    </div>
                `;
                
                // Update time display
                timeCell.innerHTML = `
                    <div class="flex items-center space-x-2">
                        <i class="fas fa-clock text-slate-400"></i>
                        <span class="font-mono text-sm">${payload.recorded_local}</span>
                    </div>
                `;
                
                // Update status badge
                if (temp >= 38.0) {
                    feverCount++;
                    statusCell.innerHTML = `
                        <span class="status-badge bg-red-100 text-red-700 border-red-200">
                            <i class="fas fa-exclamation-triangle mr-1 animate-pulse"></i>
                            Fever Alert
                        </span>
                    `;
                    row.classList.add('fever-alert');
                } else if (temp >= 37.5) {
                    statusCell.innerHTML = `
                        <span class="status-badge bg-amber-100 text-amber-700 border-amber-200">
                            <i class="fas fa-eye mr-1"></i>
                            Monitor
                        </span>
                    `;
                    row.classList.remove('fever-alert');
                } else {
                    statusCell.innerHTML = `
                        <span class="status-badge status-online">
                            <i class="fas fa-check-circle mr-1"></i>
                            Normal
                        </span>
                    `;
                    row.classList.remove('fever-alert');
                }
                
                // Add visual feedback for data updates
                tempCell.style.transform = 'scale(1.05)';
                setTimeout(() => {
                    tempCell.style.transform = 'scale(1)';
                }, 300);
                
            } else {
                tempCell.innerHTML = `
                    <div class="flex items-center space-x-2">
                        <i class="fas fa-thermometer-half text-slate-400"></i>
                        <span class="text-slate-400">—</span>
                    </div>
                `;
                timeCell.innerHTML = `
                    <div class="flex items-center space-x-2">
                        <i class="fas fa-clock text-slate-400"></i>
                        <span class="text-slate-400">—</span>
                    </div>
                `;
                statusCell.innerHTML = `
                    <span class="status-badge bg-slate-100 text-slate-600 border-slate-200">
                        <i class="fas fa-hourglass-half mr-1"></i>
                        Waiting
                    </span>
                `;
                row.classList.remove('fever-alert');
            }
        }
        
        // Update statistics
        updateStatistics(totalTemps, feverCount);
        
        // Update last refresh indicator
        updateLastRefresh();
        
        // Hide refresh indicator
        if (refreshIndicator) {
            setTimeout(() => {
                refreshIndicator.style.display = 'none';
            }, 500);
        }
        
    } catch (e) {
        console.error('Error fetching temperature data:', e);
        showConnectionError();
        
        // Hide refresh indicator on error
        const refreshIndicator = document.getElementById('refresh-indicator');
        if (refreshIndicator) {
            refreshIndicator.style.display = 'none';
        }
    }
}


// Statistics and helper functions
function updateStatistics(temperatures, feverCount) {
    // Update fever count
    const feverCountEl = document.getElementById('fever-count');
    if (feverCountEl) {
        feverCountEl.textContent = feverCount;
        
        // Add animation if fever count increased
        if (feverCount > 0) {
            feverCountEl.parentElement.parentElement.style.animation = 'pulse-danger 2s infinite';
        } else {
            feverCountEl.parentElement.parentElement.style.animation = 'none';
        }
    }
    
    // Update average temperature
    const avgTempEl = document.getElementById('avg-temp');
    if (avgTempEl && temperatures.length > 0) {
        const avgTemp = temperatures.reduce((sum, temp) => sum + temp, 0) / temperatures.length;
        avgTempEl.textContent = `${avgTemp.toFixed(1)}°C`;
        
        // Color-code the average
        const card = avgTempEl.closest('.stat-card');
        if (avgTemp >= 38) {
            card.style.background = 'linear-gradient(135deg, #ef4444 0%, #dc2626 100%)';
        } else if (avgTemp >= 37.5) {
            card.style.background = 'linear-gradient(135deg, #f59e0b 0%, #d97706 100%)';
        } else {
            card.style.background = 'linear-gradient(135deg, #f59e0b 0%, #d97706 100%)';
        }
    }
    
    // Update last update time
    const lastUpdateEl = document.getElementById('last-update');
    if (lastUpdateEl) {
        lastUpdateEl.textContent = 'Just now';
    }
}

function updateLastRefresh() {
    const now = new Date();
    const timeString = now.toLocaleTimeString();
    
    // Update system status timestamp
    const lastUpdateEl = document.getElementById('last-update');
    if (lastUpdateEl) {
        lastUpdateEl.textContent = timeString;
    }
}

function showConnectionError() {
    let errorMsg = document.getElementById('connection-error');
    if (!errorMsg) {
        errorMsg = document.createElement('div');
        errorMsg.id = 'connection-error';
        errorMsg.className = 'flash-message flash-danger';
        errorMsg.innerHTML = '⚠️ Connection error - Unable to fetch latest temperature data';
        document.querySelector('main').insertBefore(errorMsg, document.querySelector('main').firstChild);
    }
    
    // Auto-hide after 5 seconds
    setTimeout(() => {
        if (errorMsg) errorMsg.remove();
    }, 5000);
}

// Add loading indicator on page load
function addLoadingIndicator() {
    const table = document.getElementById('readings-table');
    if (table) {
        table.classList.add('loading');
        setTimeout(() => {
            table.classList.remove('loading');
        }, 1000);
    }
}

// Poll every 11 seconds (ThingSpeak typical cadence is 10s)
setInterval(fetchLatest, 11000);

// Initialize on page load
window.addEventListener('DOMContentLoaded', () => {
    addLoadingIndicator();
    fetchLatest();
});
