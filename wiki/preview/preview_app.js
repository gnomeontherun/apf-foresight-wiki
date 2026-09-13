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

    // Keyboard shortcut: 'Esc' to clear sidebar search
    if (searchInput) {
      searchInput.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
          searchInput.value = '';
          currentFilterTerm = '';
          applyFilter();
          searchInput.blur();
        }
      });
    }
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

  // 5. Search Engine & Helpers
  function escapeHtml(str) {
    if (!str) return '';
    return String(str)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#039;');
  }

  function highlightTerms(text, terms) {
    if (!text) return '';
    const safe = escapeHtml(text);
    if (!terms || !terms.length) return safe;
    const cleanTerms = Array.from(new Set(terms.map(t => t.trim()).filter(t => t.length > 0)))
      .sort((a, b) => b.length - a.length);
    if (!cleanTerms.length) return safe;
    const pattern = cleanTerms.map(t => t.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')).join('|');
    const regex = new RegExp(`(${pattern})`, 'gi');
    return safe.replace(regex, '<mark class="highlight-match">$1</mark>');
  }

  function searchCatalog(catalog, query, compFilter) {
    if (!catalog || !catalog.length) return [];
    const q = (query || '').trim().toLowerCase();
    if (!q) return [];

    const terms = q.split(/\s+/).filter(Boolean);
    const scored = [];

    for (let i = 0; i < catalog.length; i++) {
      const item = catalog[i];
      if (compFilter && compFilter !== 'all' && item.c !== compFilter) {
        continue;
      }

      const tLower = item.t.toLowerCase();
      const aLower = (item.a || '').toLowerCase();
      const pLower = (item.pName || '').toLowerCase();
      const cLower = item.c.toLowerCase();
      const combined = `${tLower} ${aLower} ${pLower} ${cLower}`;

      let allMatch = true;
      for (let j = 0; j < terms.length; j++) {
        if (!combined.includes(terms[j])) {
          allMatch = false;
          break;
        }
      }
      if (!allMatch) continue;

      let score = 0;
      if (tLower === q) score += 500;
      else if (tLower.startsWith(q)) score += 250;
      else if (tLower.includes(q)) score += 150;

      for (let j = 0; j < terms.length; j++) {
        const term = terms[j];
        if (tLower.includes(term)) score += 40;
        if (tLower.startsWith(term) || tLower.includes(' ' + term) || tLower.includes('(' + term)) score += 30;
        if (aLower.includes(term)) score += 35;
        if (pLower.includes(term)) score += 15;
        if (cLower === term) score += 20;
      }

      score += Math.max(0, 40 - Math.floor(item.t.length / 3));
      scored.push({ item, score });
    }

    scored.sort((a, b) => b.score - a.score);
    return scored.map(s => s.item);
  }

  // 6. Global Command Palette / Search Modal (Cmd+K / /)
  function initGlobalSearchModal() {
    const catalog = window.APF_CATALOG || [];
    const articleRel = window.location.pathname.includes('/articles/') ? '' : 'articles/';

    let modal = document.getElementById('globalSearchModal');
    if (!modal) {
      modal = document.createElement('div');
      modal.id = 'globalSearchModal';
      modal.className = 'search-modal-backdrop';
      modal.setAttribute('role', 'dialog');
      modal.setAttribute('aria-modal', 'true');
      modal.setAttribute('aria-label', 'Search 1,000 Foresight Articles');
      modal.innerHTML = `
        <div class="search-modal-card">
          <div class="search-modal-input-wrap">
            <span class="search-modal-icon">🔍</span>
            <input type="text" id="globalModalSearchInput" class="search-modal-input" placeholder="Search 1,000 articles, theorists, methods (e.g. CLA, Delphi, Shell, Inayatullah)..." autocomplete="off" spellcheck="false">
            <button type="button" class="search-modal-close" id="closeGlobalSearchBtn" aria-label="Close search modal">Esc</button>
          </div>
          <div class="search-modal-filter-bar" id="modalCompFilterBar">
            <span class="filter-pill active" data-comp="all">All Competencies</span>
            <span class="filter-pill" data-comp="Framing">Framing</span>
            <span class="filter-pill" data-comp="Scanning">Scanning</span>
            <span class="filter-pill" data-comp="Futuring">Futuring</span>
            <span class="filter-pill" data-comp="Designing">Designing</span>
            <span class="filter-pill" data-comp="Adapting">Adapting</span>
            <span class="filter-pill" data-comp="Leading">Leading</span>
          </div>
          <div id="globalModalSearchResults" class="search-modal-results"></div>
          <div class="search-modal-footer">
            <div class="search-modal-hints">
              <span><kbd>↑</kbd> <kbd>↓</kbd> Navigate</span>
              <span><kbd>↵</kbd> Open</span>
              <span><kbd>Esc</kbd> Close</span>
            </div>
            <div id="globalModalResultCount">1,000 articles cataloged</div>
          </div>
        </div>
      `;
      document.body.appendChild(modal);
    }

    const input = document.getElementById('globalModalSearchInput');
    const closeBtn = document.getElementById('closeGlobalSearchBtn');
    const resultsContainer = document.getElementById('globalModalSearchResults');
    const countEl = document.getElementById('globalModalResultCount');
    const filterPills = modal.querySelectorAll('.search-modal-filter-bar .filter-pill');

    let activeComp = 'all';
    let currentResults = [];
    let selectedIndex = -1;

    const CANON_SUGGESTIONS = [
      { t: "Causal Layered Analysis (CLA)", s: "0271_Causal_Layered_Analysis_(CLA)", c: "Futuring", p: 6, pName: "Alternative Futures & Scenario Archetypes", a: "Sohail Inayatullah", w: 712 },
      { t: "The Futures Cone (Plausible, Possible, Probable, Preferable)", s: "0003_The_Futures_Cone_(Plausible,_Possible,_Probable,_Preferable)", c: "Framing", p: 1, pName: "Foundations, Epistemology & Epistemic Pluralism", a: "Charles Taylor, Hancock & Bezold, Joseph Voros", w: 685 },
      { t: "Delphi Method (Classical, Policy & Real-Time Delphi)", s: "0236_Delphi_Method_(Classical,_Policy_and_Real-Time_Delphi)", c: "Futuring", p: 5, pName: "Delphi, Expert Elicitation & Consensus Forecasting", a: "Norman Dalkey, Olaf Helmer, Theodore Gordon", w: 684 },
      { t: "Horizon Scanning (Environmental Scanning Principles)", s: "0136_Horizon_Scanning_(Environmental_Scanning_Principles)", c: "Scanning", p: 4, pName: "Environmental & Horizon Scanning Systems", a: "Francis Aguilar, APF Scanning Competency", w: 581 },
      { t: "Shell Scenario Planning Methodology", s: "0272_Shell_Scenario_Planning_Methodology", c: "Futuring", p: 6, pName: "Alternative Futures & Scenario Archetypes", a: "Pierre Wack, Kees van der Heijden, Peter Schwartz", w: 704 },
      { t: "Three Horizons Framework", s: "0014_Temporal_Horizons_(H1,_H2,_H3_Epistemology)", c: "Framing", p: 1, pName: "Foundations, Epistemology & Epistemic Pluralism", a: "Bill Sharpe, Andrew Curry", w: 552 },
      { t: "Backcasting (Normative Pathway Design)", s: "0326_Backcasting_(Normative_Pathway_Design)", c: "Futuring", p: 7, pName: "Visioning, Backcasting & Normative Futures", a: "John B. Robinson", w: 641 },
      { t: "Anticipatory Governance", s: "0004_Anticipatory_Governance", c: "Framing", p: 1, pName: "Foundations, Epistemology & Epistemic Pluralism", a: "David Guston, Ray Quay, Leon Fuerth", w: 612 }
    ];

    function renderSuggestions() {
      currentResults = CANON_SUGGESTIONS.filter(item => activeComp === 'all' || item.c === activeComp);
      selectedIndex = -1;
      let html = `
        <div style="padding:8px 12px 6px; font-size:11px; font-weight:700; text-transform:uppercase; letter-spacing:1px; color:var(--text-muted);">
          ✦ Featured Canon &amp; Popular Methods
        </div>
      `;
      html += currentResults.map((item, idx) => `
        <a href="${articleRel}${item.s}.html" class="search-modal-item" data-idx="${idx}">
          <div class="search-item-title">
            <span>${escapeHtml(item.t)}</span>
            <span class="competency-tag tag-${item.c}" style="font-size:10.5px; padding:2px 7px;">✦ ${item.c}</span>
          </div>
          <div class="search-item-meta">
            <span>🏛️ Pillar ${item.p}: ${escapeHtml(item.pName)}</span>
            ${item.a ? `<span>&bull; 👤 <span class="search-item-author">${escapeHtml(item.a)}</span></span>` : ''}
            <span>&bull; 📄 ${item.w} words</span>
          </div>
        </a>
      `).join('');
      resultsContainer.innerHTML = html;
      countEl.textContent = '1,000 articles cataloged';
      attachResultItemEvents();
    }

    function renderResults(results, query, terms) {
      currentResults = results;
      selectedIndex = -1;
      if (!results.length) {
        resultsContainer.innerHTML = `
          <div style="text-align:center; padding:40px 20px; color:var(--text-muted);">
            <div style="font-size:28px; margin-bottom:8px;">🔍</div>
            <div style="font-size:15px; font-weight:600; color:var(--text-main); margin-bottom:4px;">No articles found</div>
            <div style="font-size:13px; max-width:440px; margin:0 auto; line-height:1.5;">
              No match for <em>"${escapeHtml(query)}"</em>${activeComp !== 'all' ? ` in ${activeComp}` : ''}. Try searching core theorists (Inayatullah, Bell, Dator, Polak) or methods (CLA, Delphi, Cone).
            </div>
          </div>
        `;
        countEl.textContent = '0 results';
        return;
      }

      const display = results.slice(0, 30);
      let html = `
        <div style="padding:8px 12px 6px; font-size:11px; font-weight:700; text-transform:uppercase; letter-spacing:1px; color:var(--text-muted); display:flex; justify-content:space-between;">
          <span>Search Results (${results.length.toLocaleString()})</span>
          ${results.length > 30 ? `<span>Showing top 30</span>` : ''}
        </div>
      `;
      html += display.map((item, idx) => `
        <a href="${articleRel}${item.s}.html" class="search-modal-item" data-idx="${idx}">
          <div class="search-item-title">
            <span>${highlightTerms(item.t, terms)}</span>
            <span class="competency-tag tag-${item.c}" style="font-size:10.5px; padding:2px 7px;">✦ ${item.c}</span>
          </div>
          <div class="search-item-meta">
            <span>🏛️ Pillar ${item.p}: ${escapeHtml(item.pName)}</span>
            ${item.a ? `<span>&bull; 👤 <span class="search-item-author">${highlightTerms(item.a, terms)}</span></span>` : ''}
            <span>&bull; 📄 ${item.w} words</span>
          </div>
        </a>
      `).join('');
      resultsContainer.innerHTML = html;
      countEl.textContent = `${results.length.toLocaleString()} ${results.length === 1 ? 'article' : 'articles'} found`;
      attachResultItemEvents();
    }

    function attachResultItemEvents() {
      const items = resultsContainer.querySelectorAll('.search-modal-item');
      items.forEach(it => {
        it.addEventListener('mouseenter', () => {
          const idx = parseInt(it.getAttribute('data-idx'), 10);
          if (!isNaN(idx)) {
            selectedIndex = idx;
            highlightSelectedItem();
          }
        });
      });
    }

    function highlightSelectedItem() {
      const items = resultsContainer.querySelectorAll('.search-modal-item');
      items.forEach((it, idx) => {
        if (idx === selectedIndex) {
          it.classList.add('active');
          it.scrollIntoView({ block: 'nearest' });
        } else {
          it.classList.remove('active');
        }
      });
    }

    function performModalSearch() {
      const q = input.value.trim();
      if (!q) {
        renderSuggestions();
      } else {
        const terms = q.toLowerCase().split(/\s+/).filter(Boolean);
        const matches = searchCatalog(catalog, q, activeComp);
        renderResults(matches, q, terms);
      }
    }

    function openModal() {
      modal.classList.add('open');
      input.focus();
      input.select();
      performModalSearch();
    }

    function closeModal() {
      modal.classList.remove('open');
      selectedIndex = -1;
    }

    input.addEventListener('input', performModalSearch);
    closeBtn.addEventListener('click', closeModal);

    modal.addEventListener('click', (e) => {
      if (e.target === modal) {
        closeModal();
      }
    });

    filterPills.forEach(pill => {
      pill.addEventListener('click', () => {
        filterPills.forEach(p => p.classList.remove('active'));
        pill.classList.add('active');
        activeComp = pill.getAttribute('data-comp');
        performModalSearch();
      });
    });

    window.addEventListener('keydown', (e) => {
      const isOpen = modal.classList.contains('open');

      if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === 'k') {
        e.preventDefault();
        if (isOpen) {
          closeModal();
        } else {
          openModal();
        }
        return;
      }

      const tag = (document.activeElement && document.activeElement.tagName) || '';
      const isInputFocused = tag === 'INPUT' || tag === 'TEXTAREA' || tag === 'SELECT' || (document.activeElement && document.activeElement.isContentEditable);
      if (e.key === '/' && !isInputFocused && !isOpen) {
        if (isMediaHub) {
          const mSearch = document.getElementById('mediaSearch');
          if (mSearch) {
            e.preventDefault();
            mSearch.focus();
            mSearch.select();
            return;
          }
        }
        e.preventDefault();
        openModal();
        return;
      }

      if (!isOpen) return;

      if (e.key === 'Escape') {
        e.preventDefault();
        closeModal();
      } else if (e.key === 'ArrowDown') {
        e.preventDefault();
        if (currentResults.length > 0) {
          selectedIndex = (selectedIndex + 1) % currentResults.length;
          highlightSelectedItem();
        }
      } else if (e.key === 'ArrowUp') {
        e.preventDefault();
        if (currentResults.length > 0) {
          selectedIndex = (selectedIndex - 1 + currentResults.length) % currentResults.length;
          highlightSelectedItem();
        }
      } else if (e.key === 'Enter') {
        if (currentResults.length > 0) {
          e.preventDefault();
          const targetItem = selectedIndex >= 0 ? currentResults[selectedIndex] : currentResults[0];
          if (targetItem) {
            window.location.href = `${articleRel}${targetItem.s}.html`;
          }
        }
      }
    });

    document.querySelectorAll('.global-search-trigger').forEach(btn => {
      btn.addEventListener('click', (e) => {
        e.preventDefault();
        openModal();
      });
    });
  }

  // 7. Hero Portal Search (Homepage In-Page & Autocomplete)
  function initHeroPortalSearch() {
    const heroInput = document.getElementById('heroPortalSearch');
    if (!heroInput) return;

    const catalog = window.APF_CATALOG || [];
    const dropdown = document.getElementById('heroSearchDropdown');
    const resultsSection = document.getElementById('heroSearchResultsSection');
    const resultsGrid = document.getElementById('searchResultsGrid');
    const defaultContent = document.getElementById('portalDefaultContent');
    const clearBtn = document.getElementById('clearPortalSearchBtn');
    const queryTitle = document.getElementById('searchQueryTitle');
    const matchCount = document.getElementById('searchMatchCount');

    let heroSelectedIndex = -1;
    let heroMatches = [];

    function clearSearch() {
      heroInput.value = '';
      if (dropdown) {
        dropdown.classList.remove('open');
        dropdown.innerHTML = '';
      }
      if (resultsSection) {
        resultsSection.classList.remove('active');
      }
      if (defaultContent) {
        defaultContent.style.display = 'block';
      }
      heroSelectedIndex = -1;
      heroMatches = [];
    }

    function renderDropdown(matches, q, terms) {
      if (!dropdown) return;
      if (!matches.length) {
        dropdown.innerHTML = `
          <div style="padding:16px 20px; color:var(--text-muted); text-align:center; font-size:13.5px;">
            No articles found matching <strong>"${escapeHtml(q)}"</strong>. Try methods (CLA, Delphi) or theorists (Inayatullah, Dator).
          </div>
        `;
        dropdown.classList.add('open');
        return;
      }

      const top = matches.slice(0, 7);
      let html = top.map((item, idx) => `
        <a href="articles/${item.s}.html" class="hero-dropdown-item ${idx === heroSelectedIndex ? 'active' : ''}" data-idx="${idx}">
          <div>
            <div class="title">${highlightTerms(item.t, terms)}</div>
            <div class="subtitle">
              <span>🏛️ Pillar ${item.p}</span>
              ${item.a ? ` &bull; 👤 <span>${highlightTerms(item.a, terms)}</span>` : ''}
            </div>
          </div>
          <span class="competency-tag tag-${item.c}" style="font-size:11px; padding:2px 8px; flex-shrink:0;">✦ ${item.c}</span>
        </a>
      `).join('');

      if (matches.length > 7) {
        html += `
          <div style="padding:10px 18px; font-size:12px; font-weight:600; text-align:center; background:var(--bg-page); color:var(--apf-cyan); border-top:1px solid var(--border-subtle); cursor:pointer;" id="seeAllHeroResults">
            ↓ See all ${matches.length.toLocaleString()} matching articles in page view below
          </div>
        `;
      }

      dropdown.innerHTML = html;
      dropdown.classList.add('open');

      const seeAll = document.getElementById('seeAllHeroResults');
      if (seeAll) {
        seeAll.addEventListener('click', () => {
          dropdown.classList.remove('open');
          resultsSection.scrollIntoView({ behavior: 'smooth' });
        });
      }
    }

    function renderInPageGrid(matches, q, terms) {
      if (!resultsSection || !resultsGrid) return;
      if (defaultContent) defaultContent.style.display = 'none';
      resultsSection.classList.add('active');

      if (queryTitle) queryTitle.textContent = `Search Results for "${q}"`;
      if (matchCount) matchCount.textContent = `Found ${matches.length.toLocaleString()} ${matches.length === 1 ? 'article' : 'articles'} across 1,000 entries`;

      if (!matches.length) {
        resultsGrid.innerHTML = `
          <div style="grid-column:1/-1; text-align:center; padding:60px 20px; color:var(--text-muted); background:var(--bg-surface); border-radius:12px; border:1px solid var(--border-light);">
            <div style="font-size:36px; margin-bottom:12px;">🔍</div>
            <h3 style="font-size:18px; margin-bottom:8px; color:var(--text-main);">No matching foresight articles found</h3>
            <p style="font-size:14px; max-width:480px; margin:0 auto 20px;">We couldn't find any articles matching "${escapeHtml(q)}". Try searching across the 6 core competencies or using alternative keywords.</p>
            <button type="button" class="tool-btn" id="heroNoResultsClearBtn" style="padding:8px 20px;">Clear Search</button>
          </div>
        `;
        const noResBtn = document.getElementById('heroNoResultsClearBtn');
        if (noResBtn) noResBtn.addEventListener('click', clearSearch);
        return;
      }

      const display = matches.slice(0, 48);
      let html = display.map(item => `
        <div class="search-result-card">
          <div>
            <div style="display:flex; justify-content:space-between; align-items:flex-start; gap:8px; margin-bottom:10px;">
              <span class="competency-tag tag-${item.c}">✦ ${item.c}</span>
              <span style="font-size:11.5px; color:var(--text-muted); font-weight:600;">Pillar ${item.p}</span>
            </div>
            <h3 style="font-size:16px; font-weight:700; margin:0 0 8px 0; line-height:1.35;">
              <a href="articles/${item.s}.html" style="color:var(--text-main); text-decoration:none;">
                ${highlightTerms(item.t, terms)}
              </a>
            </h3>
            ${item.a ? `<div style="font-size:12.5px; color:var(--text-muted); margin-bottom:10px;">Theorists: <strong style="color:var(--text-main);">${highlightTerms(item.a, terms)}</strong></div>` : ''}
            <div style="font-size:12px; color:var(--text-muted); margin-bottom:14px; line-height:1.45;">
              ${escapeHtml(item.pName)}
            </div>
          </div>
          <div style="display:flex; justify-content:space-between; align-items:center; border-top:1px solid var(--border-subtle); padding-top:10px; font-size:12px;">
            <span style="color:var(--text-muted);">${item.w.toLocaleString()} words (~${Math.max(2, Math.ceil(item.w / 200))} min)</span>
            <a href="articles/${item.s}.html" class="wiki-link" style="font-weight:600; color:var(--apf-cyan); text-decoration:none;">Read Article &rarr;</a>
          </div>
        </div>
      `).join('');

      if (matches.length > 48) {
        html += `
          <div style="grid-column:1/-1; text-align:center; margin-top:20px; padding:20px; background:var(--bg-surface); border-radius:10px; border:1px solid var(--border-light);">
            <p style="margin:0 0 10px 0; font-size:14px; color:var(--text-muted);">Showing first 48 of ${matches.length.toLocaleString()} matching articles.</p>
            <p style="margin:0; font-size:13px; color:var(--text-muted);">Refine your search term or use the <kbd class="kbd-shortcut">⌘K</kbd> Global Command Palette to filter by competency.</p>
          </div>
        `;
      }

      resultsGrid.innerHTML = html;
    }

    heroInput.addEventListener('input', (e) => {
      const q = e.target.value.trim();
      if (!q) {
        clearSearch();
        return;
      }
      const terms = q.toLowerCase().split(/\s+/).filter(Boolean);
      heroMatches = searchCatalog(catalog, q, 'all');
      renderDropdown(heroMatches, q, terms);
      renderInPageGrid(heroMatches, q, terms);
    });

    if (clearBtn) {
      clearBtn.addEventListener('click', clearSearch);
    }

    document.addEventListener('click', (e) => {
      if (dropdown && !heroInput.contains(e.target) && !dropdown.contains(e.target)) {
        dropdown.classList.remove('open');
      }
    });

    heroInput.addEventListener('focus', () => {
      if (heroInput.value.trim() && heroMatches.length && dropdown) {
        dropdown.classList.add('open');
      }
    });

    heroInput.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') {
        clearSearch();
        heroInput.blur();
      } else if (e.key === 'ArrowDown' && dropdown && dropdown.classList.contains('open')) {
        e.preventDefault();
        const topCount = Math.min(heroMatches.length, 7);
        if (topCount > 0) {
          heroSelectedIndex = (heroSelectedIndex + 1) % topCount;
          const items = dropdown.querySelectorAll('.hero-dropdown-item');
          items.forEach((it, i) => it.classList.toggle('active', i === heroSelectedIndex));
        }
      } else if (e.key === 'ArrowUp' && dropdown && dropdown.classList.contains('open')) {
        e.preventDefault();
        const topCount = Math.min(heroMatches.length, 7);
        if (topCount > 0) {
          heroSelectedIndex = (heroSelectedIndex - 1 + topCount) % topCount;
          const items = dropdown.querySelectorAll('.hero-dropdown-item');
          items.forEach((it, i) => it.classList.toggle('active', i === heroSelectedIndex));
        }
      } else if (e.key === 'Enter') {
        if (dropdown && dropdown.classList.contains('open') && heroMatches.length > 0) {
          e.preventDefault();
          const target = heroSelectedIndex >= 0 ? heroMatches[heroSelectedIndex] : heroMatches[0];
          if (target) {
            window.location.href = `articles/${target.s}.html`;
          }
        }
      }
    });
  }

  // 8. Initialize
  initTheme();
  document.addEventListener('DOMContentLoaded', () => {
    renderSidebar();
    initMediaHub();
    initGlobalSearchModal();
    initHeroPortalSearch();

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
