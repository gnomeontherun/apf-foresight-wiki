/**
 * APF Foresight Wiki: Interactive Preview Application
 * Powers offline navigation, live instant search across 1,000 entries,
 * the 2,700-item Media & Literature Canon hub, competency filtering,
 * official APF logo branding, dark/light theme toggle, and accordion navigation.
 */

(function () {
  'use strict';

  // 1. Theme Management
  function initTheme() {
    const saved = localStorage.getItem('apf_theme') || 'light';
    document.documentElement.setAttribute('data-theme', saved);
  }

  function toggleTheme() {
    const current = document.documentElement.getAttribute('data-theme') || 'light';
    const next = current === 'light' ? 'dark' : 'light';
    document.documentElement.setAttribute('data-theme', next);
    localStorage.setItem('apf_theme', next);
  }

  // 2. Identify Current Page
  function getCurrentSlug() {
    const path = window.location.pathname;
    const filename = path.substring(path.lastIndexOf('/') + 1);
    return filename.replace('.html', '');
  }

  const isMainPage = !window.location.pathname.includes('/articles/') && !window.location.pathname.includes('resources.html') && !window.location.pathname.includes('review.html');
  const isMediaHub = window.location.pathname.includes('resources.html');
  const isReviewHub = window.location.pathname.includes('review.html');
  const currentSlug = getCurrentSlug();

  // 3. Render Sidebar
  function renderSidebar() {
    const mount = document.getElementById('sidebar-mount');
    if (!mount) return;

    const catalog = window.APF_CATALOG || [];
    const rootRel = window.location.pathname.includes('/articles/') ? '../' : '';
    const articleRel = window.location.pathname.includes('/articles/') ? '' : 'articles/';

    // Group catalog by pillar
    const pillars = {};
    for (const item of catalog) {
      if (!pillars[item.p]) {
        pillars[item.p] = {
          num: item.p,
          dir: item.pDir,
          name: item.pName,
          items: []
        };
      }
      pillars[item.p].items.push(item);
    }

    mount.innerHTML = `
      <div class="sidebar">
        <div class="brand">
          <div class="brand-header-flex">
            <a href="${rootRel}index.html">
              <img src="${rootRel}assets/apf_wiki_official_lockup.jpg" alt="Official APF Logo" class="brand-logo-img">
            </a>
            <div>
              <div class="brand-subtitle">Association of Professional Futurists</div>
              <a href="${rootRel}index.html" class="brand-title">
                APF Foresight Wiki
              </a>
            </div>
          </div>
          <div class="brand-stats">
            <span>📚 1,000 Articles</span> &bull; 
            <span><a href="${rootRel}review.html" style="color:#fbbf24; text-decoration:underline;">Review Queue</a></span> &bull; 
            <span><a href="${rootRel}resources.html" style="color:var(--apf-accent); text-decoration:underline;">2,700 Media</a></span>
          </div>
        </div>

        <div class="sidebar-controls">
          <a href="${rootRel}resources.html" class="sidebar-nav-button" title="Explore 2,700 Books, Journals, Podcasts, Blogs & Talks">
            <span>📚</span> Media &amp; Literature Canon (2,700) &rarr;
          </a>
          <a href="${rootRel}review.html" class="sidebar-nav-button sidebar-review-button" title="Editorial Review & Peer Validation Queue">
            <span>📝</span> Editorial Review Queue (Drafts) &rarr;
          </a>

          <div class="search-input-wrapper">
            <input type="text" id="articleSearch" class="search-input" placeholder="Search 1,000 entries... (/ to focus)" autocomplete="off">
            <span id="searchClear" class="search-clear">&times;</span>
          </div>
          <div class="filter-pills" id="competencyPills">
            <span class="filter-pill active" data-comp="all">All</span>
            <span class="filter-pill" data-comp="Framing">Framing</span>
            <span class="filter-pill" data-comp="Scanning">Scanning</span>
            <span class="filter-pill" data-comp="Futuring">Futuring</span>
            <span class="filter-pill" data-comp="Designing">Designing</span>
            <span class="filter-pill" data-comp="Adapting">Adapting</span>
            <span class="filter-pill" data-comp="Leading">Leading</span>
          </div>
          <div class="sidebar-tools">
            <span id="resultCount">Showing 1,000 entries</span>
            <button type="button" id="randomBtn" class="tool-btn">🎲 Random Entry</button>
          </div>
        </div>

        <div class="nav-tree" id="navTree">
          ${Object.values(pillars).map(p => `
            <div class="pillar-group" id="group-p${p.num}">
              <div class="pillar-header" data-pnum="${p.num}">
                <span>${p.num}. ${p.name}</span>
                <span class="pillar-count">${p.items.length}</span>
              </div>
              <div class="pillar-items" id="items-p${p.num}">
                ${p.items.map(it => `
                  <a href="${articleRel}${it.s}.html" 
                     class="nav-item ${it.s === currentSlug ? 'active' : ''}" 
                     data-slug="${it.s}" 
                     data-title="${it.t.toLowerCase()}" 
                     data-comp="${it.c}" 
                     data-pnum="${it.p}"
                     title="${it.t} (${it.c})">
                    ${it.t}
                  </a>
                `).join('')}
              </div>
            </div>
          `).join('')}
        </div>
      </div>
    `;

    // Attach Event Handlers
    setupSidebarEvents(catalog, articleRel);
  }

  function setupSidebarEvents(catalog, articleRel) {
    const searchInput = document.getElementById('articleSearch');
    const searchClear = document.getElementById('searchClear');
    const resultCount = document.getElementById('resultCount');
    const pills = document.querySelectorAll('.filter-pill');
    const headers = document.querySelectorAll('.pillar-header');
    const randomBtn = document.getElementById('randomBtn');

    let activeComp = 'all';
    let currentFilterTerm = '';

    // Auto-expand pillar for current article
    if (currentSlug) {
      const activeItem = document.querySelector(`.nav-item[data-slug="${currentSlug}"]`);
      if (activeItem) {
        const group = activeItem.closest('.pillar-group');
        if (group) {
          group.classList.add('open');
          setTimeout(() => {
            activeItem.scrollIntoView({ block: 'center', behavior: 'smooth' });
          }, 100);
        }
      }
    }

    // Toggle pillar accordion
    headers.forEach(h => {
      h.addEventListener('click', () => {
        const group = h.closest('.pillar-group');
        group.classList.toggle('open');
      });
    });

    // Random Article Picker
    if (randomBtn) {
      randomBtn.addEventListener('click', () => {
        if (!catalog.length) return;
        const rand = catalog[Math.floor(Math.random() * catalog.length)];
        window.location.href = `${articleRel}${rand.s}.html`;
      });
    }

    // Filter Logic
    function applyFilter() {
      const term = currentFilterTerm.trim().toLowerCase();
      let visibleCount = 0;

      document.querySelectorAll('.pillar-group').forEach(group => {
        let groupHasVisible = false;
        const items = group.querySelectorAll('.nav-item');

        items.forEach(item => {
          const title = item.getAttribute('data-title') || '';
          const comp = item.getAttribute('data-comp') || '';
          const matchText = !term || title.includes(term);
          const matchComp = activeComp === 'all' || comp === activeComp;

          if (matchText && matchComp) {
            item.style.display = 'block';
            groupHasVisible = true;
            visibleCount++;
          } else {
            item.style.display = 'none';
          }
        });

        if (term.length > 0) {
          group.classList.toggle('open', groupHasVisible);
          group.style.display = groupHasVisible ? 'block' : 'none';
        } else {
          group.style.display = groupHasVisible ? 'block' : 'none';
        }
      });

      resultCount.textContent = `${visibleCount.toLocaleString()} ${visibleCount === 1 ? 'entry' : 'entries'} found`;
      searchClear.style.display = term ? 'block' : 'none';
    }

    // Search input
    if (searchInput) {
      searchInput.addEventListener('input', (e) => {
        currentFilterTerm = e.target.value;
        applyFilter();
      });
    }

    if (searchClear) {
      searchClear.addEventListener('click', () => {
        searchInput.value = '';
        currentFilterTerm = '';
        applyFilter();
        searchInput.focus();
      });
    }

    // Competency pills
    pills.forEach(pill => {
      pill.addEventListener('click', () => {
        pills.forEach(p => p.classList.remove('active'));
        pill.classList.add('active');
        activeComp = pill.getAttribute('data-comp');
        applyFilter();
      });
    });

    // Keyboard shortcuts: '/' to search, 'Esc' to clear
    document.addEventListener('keydown', (e) => {
      if (e.key === '/' && document.activeElement !== searchInput && (!isMediaHub || document.activeElement.id !== 'mediaSearch')) {
        e.preventDefault();
        const target = isMediaHub ? document.getElementById('mediaSearch') : searchInput;
        if (target) {
          target.focus();
          target.select();
        }
      } else if (e.key === 'Escape' && document.activeElement === searchInput) {
        searchInput.value = '';
        currentFilterTerm = '';
        applyFilter();
        searchInput.blur();
      }
    });
  }

  // 4. Media Canon Hub Initialization
  function initMediaHub() {
    if (!isMediaHub) return;

    const mediaGrid = document.getElementById('mediaGrid');
    const mediaSearch = document.getElementById('mediaSearch');
    const mediaCountBadge = document.getElementById('mediaCountBadge');
    const tabs = document.querySelectorAll('.media-tab');
    const compPills = document.querySelectorAll('.media-comp-pill');
    const exportBibtexBtn = document.getElementById('exportBibtexBtn');
    const exportCsvBtn = document.getElementById('exportCsvBtn');

    const mediaList = window.FORESIGHT_MEDIA_CANON || [];
    let currentTypeFilter = 'all';
    let currentCompFilter = 'all';
    let currentSearchTerm = '';
    let visibleLimit = 120;

    function getBadgeClass(type) {
      if (type === 'Book') return 'badge-book';
      if (type === 'Journal Article') return 'badge-journal';
      if (type === 'Podcast') return 'badge-podcast';
      if (type === 'Blog / Newsletter') return 'badge-blog';
      return 'badge-talk';
    }

    function renderCards(items) {
      if (!mediaGrid) return;
      if (!items.length) {
        mediaGrid.innerHTML = `
          <div style="grid-column: 1/-1; text-align: center; padding: 60px 20px; color: var(--text-muted);">
            <div style="font-size: 32px; margin-bottom: 12px;">🔍</div>
            <h3 style="font-size: 18px; margin-bottom: 6px;">No foresight media resources found</h3>
            <p style="font-size: 14px;">Try adjusting your keyword search or category filters.</p>
          </div>
        `;
        if (mediaCountBadge) mediaCountBadge.textContent = '0 items';
        return;
      }

      const displayList = currentSearchTerm ? items : items.slice(0, visibleLimit);

      const cardsHtml = displayList.map(item => `
        <div class="media-card" data-id="${item.id}" data-type="${item.media_type}" data-comp="${item.apf_competency}">
          <div class="media-card-top">
            <span class="media-badge-type ${getBadgeClass(item.media_type)}">${item.media_type}</span>
            <span class="competency-tag tag-${item.apf_competency}">✦ ${item.apf_competency}</span>
          </div>

          <h3 class="media-card-title">${item.title}</h3>
          <div class="media-card-creator">
            <strong>${item.creator}</strong> &bull; <span>${item.year_or_date}</span>
            ${item.journal ? ` &bull; <em>${item.journal}</em>` : ''}
          </div>

          <div class="media-card-summary">
            ${item.summary}
          </div>

          <div class="media-card-significance">
            <strong>Significance:</strong> ${item.significance}
          </div>

          <div class="media-tags-list">
            ${(item.tags || []).slice(0, 4).map(t => `<span class="media-tag-pill">#${t}</span>`).join('')}
          </div>

          <div class="media-card-footer">
            <span style="font-size: 11px; color: var(--text-muted);">ID: ${item.id} &bull; Pillar ${item.thematic_pillar}</span>
            <a href="${item.source_or_doi}" target="_blank" rel="noopener noreferrer" class="media-access-link">
              Access Resource ↗
            </a>
          </div>
        </div>
      `).join('');

      let moreBtnHtml = '';
      if (!currentSearchTerm && items.length > visibleLimit) {
        const remaining = items.length - visibleLimit;
        moreBtnHtml = `
          <div style="grid-column: 1/-1; text-align: center; margin: 30px 0 20px 0;">
            <button type="button" id="loadMoreMediaBtn" class="tool-btn" style="padding: 12px 28px; font-size: 14px; font-weight: 700; border-radius: 8px; background: var(--apf-navy); color: white; border: 1px solid var(--border-light); cursor: pointer; box-shadow: var(--shadow-sm);">
              ↓ Load Next 120 Resources (${remaining.toLocaleString()} more available)
            </button>
            <button type="button" id="loadAllMediaBtn" class="tool-btn" style="padding: 12px 20px; font-size: 13px; font-weight: 600; border-radius: 8px; margin-left: 12px; background: var(--bg-surface); cursor: pointer;">
              Show All ${items.length.toLocaleString()}
            </button>
          </div>
        `;
      }

      mediaGrid.innerHTML = cardsHtml + moreBtnHtml;

      const loadMoreBtn = document.getElementById('loadMoreMediaBtn');
      if (loadMoreBtn) {
        loadMoreBtn.addEventListener('click', () => {
          visibleLimit += 120;
          renderCards(items);
        });
      }

      const loadAllBtn = document.getElementById('loadAllMediaBtn');
      if (loadAllBtn) {
        loadAllBtn.addEventListener('click', () => {
          visibleLimit = items.length;
          renderCards(items);
        });
      }

      if (mediaCountBadge) {
        mediaCountBadge.textContent = `${items.length.toLocaleString()} items`;
      }
    }

    function getFilteredItems() {
      const term = currentSearchTerm.trim().toLowerCase();
      return mediaList.filter(item => {
        // Type filter
        const matchType = currentTypeFilter === 'all' || item.media_type.toLowerCase().includes(currentTypeFilter.toLowerCase());
        // Competency filter
        const matchComp = currentCompFilter === 'all' || item.apf_competency === currentCompFilter;
        // Search term filter
        const textToSearch = `${item.title} ${item.creator} ${item.summary} ${item.significance} ${(item.tags || []).join(' ')} ${item.source_or_doi || ''}`.toLowerCase();
        const matchSearch = !term || textToSearch.includes(term);

        return matchType && matchComp && matchSearch;
      });
    }

    function updateView() {
      visibleLimit = 120;
      const filtered = getFilteredItems();
      renderCards(filtered);
    }

    // Tab buttons
    tabs.forEach(tab => {
      tab.addEventListener('click', () => {
        tabs.forEach(t => t.classList.remove('active'));
        tab.classList.add('active');
        currentTypeFilter = tab.getAttribute('data-type');
        updateView();
      });
    });

    // Competency pills
    compPills.forEach(pill => {
      pill.addEventListener('click', () => {
        compPills.forEach(p => p.classList.remove('active'));
        pill.classList.add('active');
        currentCompFilter = pill.getAttribute('data-comp');
        updateView();
      });
    });

    // Search input
    if (mediaSearch) {
      mediaSearch.addEventListener('input', (e) => {
        currentSearchTerm = e.target.value;
        updateView();
      });
    }

    // Export to BibTeX
    if (exportBibtexBtn) {
      exportBibtexBtn.addEventListener('click', () => {
        const filtered = getFilteredItems();
        let bib = '% APF Global Foresight Media & Literature Canon\n% Exported from APF Foresight Wiki\n\n';
        filtered.forEach(item => {
          const key = item.id.replace('-', '');
          const entryType = item.media_type === 'Book' ? 'book' : item.media_type === 'Journal Article' ? 'article' : 'misc';
          bib += `@${entryType}{${key},\n`;
          bib += `  title = {${item.title}},\n`;
          bib += `  author = {${item.creator}},\n`;
          bib += `  year = {${item.year_or_date}},\n`;
          if (item.journal) bib += `  journal = {${item.journal}},\n`;
          if (item.volume) bib += `  volume = {${item.volume}},\n`;
          if (item.source_or_doi) bib += `  url = {${item.source_or_doi}},\n`;
          bib += `  note = {APF Competency: ${item.apf_competency} | Pillar: ${item.pillar_name}}\n`;
          bib += `}\n\n`;
        });

        downloadFile(bib, 'apf_foresight_media_canon.bib', 'text/plain');
      });
    }

    // Export to CSV
    if (exportCsvBtn) {
      exportCsvBtn.addEventListener('click', () => {
        const filtered = getFilteredItems();
        const headers = ["ID", "Title", "Creator", "Year", "Media Type", "APF Competency", "Pillar", "Summary", "Significance", "Source/DOI"];
        let csv = headers.map(h => `"${h}"`).join(',') + '\n';

        filtered.forEach(item => {
          const row = [
            item.id,
            item.title,
            item.creator,
            item.year_or_date,
            item.media_type,
            item.apf_competency,
            item.pillar_name,
            item.summary,
            item.significance,
            item.source_or_doi
          ].map(val => `"${(val || '').toString().replace(/"/g, '""')}"`);
          csv += row.join(',') + '\n';
        });

        downloadFile(csv, 'apf_foresight_media_canon.csv', 'text/csv');
      });
    }

    function downloadFile(content, filename, mime) {
      const blob = new Blob([content], { type: mime });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = filename;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
    }

    // Initial render
    updateView();
  }

  // 5. Initialize
  initTheme();
  document.addEventListener('DOMContentLoaded', () => {
    renderSidebar();
    initMediaHub();

    const themeBtns = document.querySelectorAll('.theme-toggle-btn');
    themeBtns.forEach(b => b.addEventListener('click', toggleTheme));
  });

  window.filterByCompetency = function (comp) {
    const pill = document.querySelector(`.filter-pill[data-comp="${comp}"]`);
    if (pill) {
      pill.click();
      window.scrollTo({ top: 0, behavior: 'smooth' });
    }
  };

})();
