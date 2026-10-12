let allData = [];
let progressData = {};
let currentFilter = 'all'; // 'all', 'completed', 'pending'
let searchQuery = '';
let selectedIndustry = 'all';

// Modal state
let currentModalIndex = -1;
let currentFilteredItems = [];

window.openImageModal = function(src, index) {
    const modal = document.getElementById('image-modal');
    const modalImg = document.getElementById('modal-img');
    if (!modal || !modalImg) return;
    currentModalIndex = index;
    modalImg.src = src;
    modal.classList.remove('hidden');
};

window.closeImageModal = function() {
    const modal = document.getElementById('image-modal');
    if (modal) modal.classList.add('hidden');
};

window.navigateModal = function(direction) {
    if (currentFilteredItems.length === 0) return;
    currentModalIndex += direction;
    if (currentModalIndex < 0) currentModalIndex = currentFilteredItems.length - 1;
    if (currentModalIndex >= currentFilteredItems.length) currentModalIndex = 0;
    
    const targetItem = currentFilteredItems[currentModalIndex];
    if (targetItem) {
        const modalImg = document.getElementById('modal-img');
        if (modalImg) modalImg.src = getImagePath(targetItem.industry, targetItem.profession);
    }
};

window.copyInfo = function(industry, profession) {
    const text = `${profession} (${industry})`;
    navigator.clipboard.writeText(text).then(() => {
        alert(`Copied: "${text}"`);
    }).catch(() => {
        prompt('Copy text:', text);
    });
};

// Auto-refresh timer interval
let autoRefreshTimer = null;

async function fetchProgress() {
    const timestamp = new Date().getTime();
    try {
        const res = await fetch(`images/batch_progress.json?_t=${timestamp}`);
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        return await res.json();
    } catch (err) {
        console.warn('Could not fetch images/batch_progress.json directly:', err);
        return null;
    }
}

async function fetchCSV() {
    try {
        const res = await fetch('Othe.app image generation industry profession and prompt - Sheet1.csv');
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const text = await res.text();
        return parseCSV(text);
    } catch (err) {
        console.warn('Could not fetch CSV directly:', err);
        return [];
    }
}

// Simple RFC-compliant CSV parser for the 3 columns: Industry, Profession, Prompt
function parseCSV(text) {
    const lines = [];
    let row = [''];
    let inQuotes = false;

    for (let i = 0; i < text.length; i++) {
        const c = text[i];
        const next = text[i + 1];

        if (c === '"') {
            if (inQuotes && next === '"') {
                row[row.length - 1] += '"';
                i++;
            } else {
                inQuotes = !inQuotes;
            }
        } else if (c === ',' && !inQuotes) {
            row.push('');
        } else if ((c === '\r' || c === '\n') && !inQuotes) {
            if (c === '\r' && next === '\n') i++;
            if (row.length > 1 || row[0] !== '') {
                lines.push(row);
            }
            row = [''];
        } else {
            row[row.length - 1] += c;
        }
    }
    if (row.length > 1 || row[0] !== '') {
        lines.push(row);
    }

    if (lines.length <= 1) return [];
    const headers = lines[0].map(h => h.trim());
    const indIdx = headers.indexOf('Industry');
    const profIdx = headers.indexOf('Profession');

    return lines.slice(1).map(r => ({
        industry: (r[indIdx] || '').trim(),
        profession: (r[profIdx] || '').trim()
    })).filter(r => r.industry && r.profession);
}

function sanitizeName(name) {
    return name.replace(/[/\\:*?"<>|]/g, '-').trim() || 'untitled';
}

function getImagePath(industry, profession) {
    const safeInd = sanitizeName(industry);
    const safeProf = sanitizeName(profession);
    return `images/${encodeURIComponent(safeInd)}/${encodeURIComponent(safeProf)}.png`;
}

async function loadData() {
    const statusEl = document.getElementById('last-updated');
    if (statusEl) statusEl.textContent = 'Updating...';

    const [progress, csvList] = await Promise.all([fetchProgress(), fetchCSV()]);

    if (!progress && (!csvList || csvList.length === 0)) {
        if (statusEl) statusEl.textContent = 'Failed to load progress file. Make sure images/batch_progress.json exists.';
        return;
    }

    progressData = progress || {};

    // Combine CSV items with progress
    const itemsMap = new Map();

    if (csvList && csvList.length > 0) {
        csvList.forEach(item => {
            const key = `${item.industry}::${item.profession}`;
            itemsMap.set(key, {
                industry: item.industry,
                profession: item.profession,
                key: key,
                status: 'pending',
                timestamp: null,
                bytes: 0
            });
        });
    }

    // Merge progress keys
    Object.entries(progressData).forEach(([key, info]) => {
        let existing = itemsMap.get(key);
        if (!existing) {
            existing = {
                industry: info.industry || key.split('::')[0],
                profession: info.profession || key.split('::')[1],
                key: key
            };
            itemsMap.set(key, existing);
        }
        existing.status = info.status || 'pending';
        existing.timestamp = info.timestamp || null;
        existing.bytes = info.bytes || 0;
    });

    allData = Array.from(itemsMap.values());

    updateMetrics();
    populateIndustryFilter();
    renderList();

    const now = new Date();
    if (statusEl) {
        statusEl.textContent = `Last updated: ${now.toLocaleTimeString()}`;
    }
}

function updateMetrics() {
    const total = allData.length;
    const completed = allData.filter(d => d.status === 'completed').length;
    const pending = total - completed;
    const pct = total > 0 ? ((completed / total) * 100).toFixed(1) : 0;

    const totalEl = document.getElementById('stat-total');
    const compEl = document.getElementById('stat-completed');
    const pendEl = document.getElementById('stat-pending');
    const pctEl = document.getElementById('stat-pct');
    const barEl = document.getElementById('progress-bar-fill');

    if (totalEl) totalEl.textContent = total;
    if (compEl) compEl.textContent = completed;
    if (pendEl) pendEl.textContent = pending;
    if (pctEl) pctEl.textContent = `${pct}%`;
    if (barEl) barEl.style.width = `${pct}%`;
}

function populateIndustryFilter() {
    const select = document.getElementById('industry-filter');
    if (!select) return;

    const currentVal = select.value;
    const industries = Array.from(new Set(allData.map(d => d.industry))).sort();

    select.innerHTML = '<option value="all">All Industries (97)</option>';
    industries.forEach(ind => {
        const count = allData.filter(d => d.industry === ind).length;
        const done = allData.filter(d => d.industry === ind && d.status === 'completed').length;
        const opt = document.createElement('option');
        opt.value = ind;
        opt.textContent = `${ind} (${done}/${count})`;
        select.appendChild(opt);
    });

    if (currentVal && Array.from(select.options).some(o => o.value === currentVal)) {
        select.value = currentVal;
    }
}

function renderList() {
    const grid = document.getElementById('items-grid');
    if (!grid) return;

    const filtered = allData.filter(item => {
        // Status filter
        if (currentFilter === 'completed' && item.status !== 'completed') return false;
        if (currentFilter === 'pending' && item.status === 'completed') return false;

        // Industry filter
        if (selectedIndustry !== 'all' && item.industry !== selectedIndustry) return false;

        // Search query
        if (searchQuery) {
            const q = searchQuery.toLowerCase();
            return item.profession.toLowerCase().includes(q) || item.industry.toLowerCase().includes(q);
        }

        return true;
    });

    currentFilteredItems = filtered;

    const countHeader = document.getElementById('filtered-count');
    if (countHeader) {
        countHeader.textContent = `Showing ${filtered.length} of ${allData.length} professions`;
    }

    if (filtered.length === 0) {
        grid.innerHTML = `
            <div class="empty-state">
                <p>No professions match the selected filter criteria.</p>
            </div>
        `;
        return;
    }

    grid.innerHTML = filtered.map(item => {
        const isDone = item.status === 'completed';
        const imgPath = getImagePath(item.industry, item.profession);
        const sizeKb = item.bytes ? `${(item.bytes / 1024 / 1024).toFixed(2)} MB` : '';
        const timeStr = item.timestamp ? new Date(item.timestamp).toLocaleTimeString() : '';
        const index = filtered.indexOf(item); // index within filtered array for modal navigation
        return `
            <div class="item-card ${isDone ? 'is-completed' : 'is-pending'}">
                <div class="card-thumb">
                    ${isDone ? `
                        <img src="${imgPath}" alt="${item.profession}" loading="lazy" onerror="this.onerror=null; this.parentElement.innerHTML='<div class=\'thumb-fallback\'>Image Missing</div>';">
                    ` : `
                        <div class="thumb-placeholder">
                            <span class="placeholder-icon">⏳</span>
                            <span>Pending Generation</span>
                        </div>
                    `}
                    <span class="badge ${isDone ? 'badge-success' : 'badge-warning'}">
                        ${isDone ? '✓ Generated' : '⏳ Pending'}
                    </span>
                </div>
                <div class="card-body">
                    <span class="card-industry" title="${item.industry}">${item.industry}</span>
                    <h3 class="card-title" title="${item.profession}">${item.profession}</h3>
                    <div class="card-meta">
                        ${isDone ? `
                            <span>${sizeKb}</span>
                            <span>${timeStr}</span>
                        ` : `
                            <span class="pending-note">Waiting in queue</span>
                        `}
                    </div>
                    ${isDone ? `
                        <div class="card-actions">
                            <button class="btn-view" data-src="${imgPath}" data-index="${index}" onclick="openImageModal(this.dataset.src, parseInt(this.dataset.index))">View Full Image ↗</button>
                            <button class="btn-copy" onclick="copyInfo('${item.industry}', '${item.profession}')">Copy</button>
                            <button class="btn-delete" onclick="deleteImage('${item.key}')">Delete</button>
                        </div>
                    ` : ''}
                </div>
            </div>
        `;

    }).join('');
}

// Event Listeners
document.addEventListener('DOMContentLoaded', () => {
    loadData();

    // Search input
    const searchInput = document.getElementById('search-input');

    // Delete image function
    window.deleteImage = async function(key) {
        if (!confirm('Are you sure you want to delete this image and its log entry?')) return;
        try {
            const res = await fetch('/delete_image', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ key })
            });
            if (res.ok) {
                // reload data to reflect changes
                loadData();
            } else {
                alert('Failed to delete image.');
            }
        } catch (e) {
            console.error(e);
            alert('Error while deleting image.');
        }
    };

    if (searchInput) {
        searchInput.addEventListener('input', (e) => {
            searchQuery = e.target.value.trim();
            renderList();
        });
    }

    // Filter Buttons
    document.querySelectorAll('.filter-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            currentFilter = btn.dataset.filter;
            renderList();
        });
    });

    // Industry select
    const indSelect = document.getElementById('industry-filter');
    if (indSelect) {
        indSelect.addEventListener('change', (e) => {
            selectedIndustry = e.target.value;
            renderList();
        });
    }

    // Manual Refresh button
    const refreshBtn = document.getElementById('btn-refresh');
    if (refreshBtn) {
        refreshBtn.addEventListener('click', () => {
            loadData();
        });
    }

    // Auto-refresh checkbox
    const autoCheckbox = document.getElementById('auto-refresh-toggle');
    if (autoCheckbox) {
        const toggleInterval = () => {
            if (autoCheckbox.checked) {
                if (!autoRefreshTimer) {
                    autoRefreshTimer = setInterval(loadData, 5000);
                }
            } else {
                if (autoRefreshTimer) {
                    clearInterval(autoRefreshTimer);
                    autoRefreshTimer = null;
                }
            }
        };
        autoCheckbox.addEventListener('change', toggleInterval);
        toggleInterval();
    }
});
