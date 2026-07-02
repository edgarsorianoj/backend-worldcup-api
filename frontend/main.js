/* =========================================================
 *  World Cup API · Frontend
 *  - Consumo exclusivo vía Axios (sin fetch).
 *  - Skeleton loading, progress bar, toasts, atajos teclado.
 *  - Chips de filtros activos, "Actualizado hace Xs".
 *  - Búsqueda + filtro confederación + ordenamiento.
 * ======================================================= */

(function () {
    'use strict';

    /* ---------------- Configuración ---------------- */
    const API_BASE_URL = 'http://127.0.0.1:8000';
    const ENDPOINTS = {
        selections: `${API_BASE_URL}/selections`,
        byId: (id) => `${API_BASE_URL}/selections/${id}`,
    };

    const SKELETON_COUNT = 8;
    const TOAST_DURATION = 3500;
    const SEARCH_DEBOUNCE = 150;
    const PROGRESS_MIN_TIME = 400; // evita parpadeo si la respuesta es < 400ms

    /* ---------------- Estado de la app ---------------- */
    const state = {
        selections: [],
        filtered: [],
        searchTerm: '',
        confederation: '',
        sortBy: 'country',
        lastUpdate: null,
    };

    /* ---------------- Selectores DOM cacheados ---------------- */
    const dom = {};

    function cacheDom() {
        dom.grid = document.getElementById('selectionsGrid');
        dom.searchInput = document.getElementById('searchInput');
        dom.searchClear = document.getElementById('searchClear');
        dom.confederationFilter = document.getElementById('confederationFilter');
        dom.sortBy = document.getElementById('sortBy');
        dom.reloadBtn = document.getElementById('reloadBtn');
        dom.retryBtn = document.getElementById('retryBtn');
        dom.clearFiltersBtn = document.getElementById('clearFiltersBtn');

        dom.loadingState = document.getElementById('loadingState');
        dom.errorState = document.getElementById('errorState');
        dom.emptyState = document.getElementById('emptyState');
        dom.noDataState = document.getElementById('noDataState');
        dom.errorMessage = document.getElementById('errorMessage');

        dom.resultsCount = document.getElementById('resultsCount');
        dom.resultsSection = document.getElementById('selections');

        dom.totalSelections = document.getElementById('totalSelections');
        dom.totalConfederations = document.getElementById('totalConfederations');
        dom.totalChampions = document.getElementById('totalChampions');
        dom.lastUpdateEl = document.getElementById('lastUpdate');

        dom.navToggle = document.getElementById('navToggle');
        dom.navLinks = document.getElementById('navLinks');

        dom.backToTop = document.getElementById('backToTop');
        dom.toastContainer = document.getElementById('toastContainer');
        dom.progressBar = document.getElementById('progressBar');
        dom.scrollProgress = document.getElementById('scrollProgress');
        dom.scrollProgressFill = dom.scrollProgress?.querySelector('.scroll-progress__fill');

        dom.modal = document.getElementById('detailModal');
        dom.modalFlag = document.getElementById('modalFlag');
        dom.modalConfederation = document.getElementById('modalConfederation');
        dom.modalTitle = document.getElementById('modalTitle');
        dom.modalCaptain = document.getElementById('modalCaptain');
        dom.modalCoach = document.getElementById('modalCoach');
        dom.modalCups = document.getElementById('modalCups');

        dom.activeFilters = document.getElementById('activeFilters');
        dom.activeChips = document.getElementById('activeChips');
        dom.clearAllChips = document.getElementById('clearAllChips');

        dom.shortcutsHint = document.getElementById('shortcutsHint');
        dom.closeShortcuts = document.getElementById('closeShortcuts');

        dom.navLinksItems = document.querySelectorAll('[data-link]');
    }

    /* ---------------- Capa de API (Axios) ---------------- */
    const api = {
        async getSelections() {
            const response = await axios.get(ENDPOINTS.selections);
            return Array.isArray(response.data) ? response.data : [];
        },
    };

    /* ---------------- Helpers ---------------- */
    function escapeHtml(value) {
        if (value === null || value === undefined) return '';
        return String(value)
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;')
            .replace(/'/g, '&#39;');
    }

    function getInitials(country) {
        if (!country) return '?';
        return country
            .split(/\s+/)
            .map((word) => word[0])
            .join('')
            .slice(0, 2)
            .toUpperCase();
    }

    function showOnly(visibleElement) {
        const all = [dom.loadingState, dom.errorState, dom.emptyState, dom.noDataState];
        all.forEach((el) => el && el.setAttribute('hidden', ''));
        if (visibleElement) {
            visibleElement.removeAttribute('hidden');
        }
    }

    function setGridVisible(visible) {
        if (visible) {
            dom.grid.removeAttribute('hidden');
        } else {
            dom.grid.setAttribute('hidden', '');
        }
    }

    function setResultsBusy(busy) {
        if (busy) {
            dom.resultsSection.setAttribute('aria-busy', 'true');
        } else {
            dom.resultsSection.setAttribute('aria-busy', 'false');
        }
    }

    function showProgress(active) {
        if (!dom.progressBar) return;
        if (active) {
            dom.progressBar.classList.add('is-active');
        } else {
            dom.progressBar.classList.remove('is-active');
        }
    }

    /* ---------------- Skeletons ---------------- */
    function renderSkeletons() {
        const html = Array.from({ length: SKELETON_COUNT }, () => `
            <div class="skeleton" aria-hidden="true">
                <div class="skeleton__head">
                    <div class="skeleton__flag sk-line"></div>
                    <div class="skeleton__lines">
                        <div class="sk-line sk-line--title"></div>
                        <div class="sk-line sk-line--sub"></div>
                    </div>
                </div>
                <div class="skeleton__body">
                    <div class="sk-line sk-line--row"></div>
                    <div class="sk-line sk-line--row sk-line--row-short"></div>
                </div>
            </div>
        `).join('');
        dom.loadingState.innerHTML = html;
    }

    /* ---------------- Toasts ---------------- */
    function showToast(message, type = 'info', duration = TOAST_DURATION) {
        if (!dom.toastContainer) return;

        const icons = { success: '✓', error: '✕', info: 'i' };

        const toast = document.createElement('div');
        toast.className = `toast toast--${type}`;
        toast.setAttribute('role', type === 'error' ? 'alert' : 'status');
        toast.innerHTML = `
            <span class="toast__icon" aria-hidden="true">${icons[type] || icons.info}</span>
            <span class="toast__text">${escapeHtml(message)}</span>
            <button class="toast__close" type="button" aria-label="Cerrar notificación">×</button>
        `;

        toast.querySelector('.toast__close').addEventListener('click', () => {
            dismissToast(toast);
        });

        dom.toastContainer.appendChild(toast);

        setTimeout(() => dismissToast(toast), duration);
    }

    function dismissToast(toast) {
        if (!toast || !toast.parentNode) return;
        if (toast.classList.contains('is-leaving')) return;
        toast.classList.add('is-leaving');
        toast.addEventListener('animationend', () => toast.remove(), { once: true });
    }

    /* ---------------- Tarjeta ---------------- */
    function renderCard(selection, index) {
        const { country, confederation, captain, coach, world_cups, flag } = selection;
        const trophies = Number(world_cups) || 0;
        const flagUrl = escapeHtml(flag);
        const flagFallback = escapeHtml(getInitials(country));
        const stagger = Math.min(index, 12) * 40;

        const trophyClass = trophies > 0 ? 'card__trophy card__trophy--has' : 'card__trophy';
        const trophyLabel = trophies > 0 ? `🏆 ${trophies}` : '—';

        return `
            <li
                class="card"
                data-id="${escapeHtml(String(selection.id ?? ''))}"
                style="--stagger: ${stagger}ms"
                role="button"
                tabindex="0"
                aria-label="Ver detalle de ${escapeHtml(country)}"
            >
                <div class="card__head">
                    <div class="card__flag">
                        <img
                            src="${flagUrl}"
                            alt=""
                            loading="lazy"
                            onerror="this.outerHTML='<span class=&quot;card__flag-fallback&quot;>${flagFallback}</span>'"
                        />
                    </div>
                    <div class="card__title-wrap">
                        <h3 class="card__title">${escapeHtml(country)}</h3>
                        <p class="card__confederation">${escapeHtml(confederation)}</p>
                    </div>
                    <span class="${trophyClass}" title="Mundiales ganados">${trophyLabel}</span>
                </div>
                <div class="card__body">
                    <dl class="card__row">
                        <dt>Capitán</dt>
                        <dd>${escapeHtml(captain)}</dd>
                    </dl>
                    <dl class="card__row">
                        <dt>DT</dt>
                        <dd>${escapeHtml(coach)}</dd>
                    </dl>
                </div>
                <span class="card__arrow" aria-hidden="true">
                    <svg viewBox="0 0 24 24" width="12" height="12">
                        <path d="M5 12h14M13 5l7 7-7 7" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    </svg>
                </span>
            </li>
        `;
    }

    function renderGrid(selections) {
        if (!selections.length) {
            dom.grid.innerHTML = '';
            setGridVisible(false);
            return;
        }
        dom.grid.innerHTML = selections.map((s, i) => renderCard(s, i)).join('');
        setGridVisible(true);
    }

    /* ---------------- Modal ---------------- */
    function openModal(selection) {
        if (!dom.modal) return;

        dom.modalFlag.src = selection.flag;
        dom.modalFlag.alt = `Bandera de ${selection.country}`;
        dom.modalConfederation.textContent = selection.confederation;
        dom.modalTitle.textContent = selection.country;
        dom.modalCaptain.textContent = selection.captain;
        dom.modalCoach.textContent = selection.coach;
        dom.modalCups.textContent = selection.world_cups > 0
            ? `${selection.world_cups} 🏆`
            : 'Sin título';

        dom.modal.removeAttribute('hidden');
        dom.modal.classList.remove('is-leaving');
        document.body.style.overflow = 'hidden';

        const closeBtn = dom.modal.querySelector('.modal__close');
        if (closeBtn) setTimeout(() => closeBtn.focus(), 50);
    }

    function closeModal() {
        if (!dom.modal || dom.modal.hasAttribute('hidden')) return;
        dom.modal.classList.add('is-leaving');
        setTimeout(() => {
            dom.modal.setAttribute('hidden', '');
            dom.modal.classList.remove('is-leaving');
            document.body.style.overflow = '';
        }, 250);
    }

    /* ---------------- Active filters (chips) ---------------- */
    function updateActiveFilters() {
        const chips = [];

        if (state.searchTerm.trim()) {
            chips.push({
                type: 'search',
                label: `“${state.searchTerm.trim()}”`,
                remove: () => {
                    state.searchTerm = '';
                    dom.searchInput.value = '';
                    dom.searchClear.setAttribute('hidden', '');
                },
            });
        }

        if (state.confederation) {
            chips.push({
                type: 'confederation',
                label: state.confederation,
                remove: () => {
                    state.confederation = '';
                    dom.confederationFilter.value = '';
                },
            });
        }

        if (chips.length === 0) {
            dom.activeFilters.setAttribute('hidden', '');
            dom.activeChips.innerHTML = '';
            return;
        }

        dom.activeFilters.removeAttribute('hidden');
        dom.activeChips.innerHTML = chips
            .map((chip, i) => `
                <span class="chip" data-chip-index="${i}">
                    ${escapeHtml(chip.label)}
                    <button class="chip__remove" type="button" aria-label="Quitar filtro">×</button>
                </span>
            `)
            .join('');

        // Vincular handlers
        dom.activeChips.querySelectorAll('.chip').forEach((el) => {
            const idx = Number(el.dataset.chipIndex);
            el.querySelector('.chip__remove').addEventListener('click', () => {
                chips[idx].remove();
                applyFilters();
            });
        });
    }

    /* ---------------- Summary ---------------- */
    function populateConfederationFilter(selections) {
        const unique = [
            ...new Set(selections.map((s) => s.confederation).filter(Boolean)),
        ].sort();

        const currentValue = state.confederation;
        dom.confederationFilter.innerHTML =
            '<option value="">Todas las confederaciones</option>' +
            unique
                .map(
                    (conf) =>
                        `<option value="${escapeHtml(conf)}">${escapeHtml(conf)}</option>`
                )
                .join('');
        dom.confederationFilter.value = currentValue;
    }

    function animateCount(element, target, duration = 800) {
        if (!element) return;
        const start = 0;
        const startTime = performance.now();
        const isInt = Number.isInteger(target);

        function tick(now) {
            const elapsed = now - startTime;
            const progress = Math.min(elapsed / duration, 1);
            const eased = 1 - Math.pow(1 - progress, 3);
            const current = start + (target - start) * eased;
            element.textContent = isInt
                ? Math.floor(current).toString()
                : current.toFixed(0);
            if (progress < 1) {
                requestAnimationFrame(tick);
            } else {
                element.textContent = isInt ? String(target) : target.toFixed(0);
            }
        }
        requestAnimationFrame(tick);
    }

    function updateSummary(selections) {
        const total = selections.length;
        const confederations = new Set(
            selections.map((s) => s.confederation).filter(Boolean)
        );
        const champions = selections.filter((s) => Number(s.world_cups) > 0).length;

        animateCount(dom.totalSelections, total);
        animateCount(dom.totalConfederations, confederations.size);
        animateCount(dom.totalChampions, champions);
    }

    function updateLastUpdate() {
        if (!state.lastUpdate) {
            dom.lastUpdateEl.textContent = '—';
            return;
        }
        const now = Date.now();
        const diff = Math.floor((now - state.lastUpdate) / 1000);

        if (diff < 5) {
            dom.lastUpdateEl.textContent = 'ahora';
        } else if (diff < 60) {
            dom.lastUpdateEl.textContent = `hace ${diff}s`;
        } else if (diff < 3600) {
            dom.lastUpdateEl.textContent = `hace ${Math.floor(diff / 60)}m`;
        } else {
            dom.lastUpdateEl.textContent = `hace ${Math.floor(diff / 3600)}h`;
        }
    }

    function startLastUpdateTicker() {
        updateLastUpdate();
        // Actualiza cada 10 segundos
        setInterval(updateLastUpdate, 10000);
    }

    function updateResultsCount(filtered, total) {
        const hasFilters = state.searchTerm.trim() || state.confederation;
        let text;
        if (total === 0) {
            text = 'Sin datos';
        } else if (hasFilters) {
            text = `${filtered.length} / ${total}`;
        } else {
            text = `${total} selecciones`;
        }
        dom.resultsCount.textContent = text;

        dom.resultsCount.classList.remove('is-updated');
        void dom.resultsCount.offsetWidth;
        dom.resultsCount.classList.add('is-updated');
        setTimeout(() => dom.resultsCount.classList.remove('is-updated'), 600);
    }

    /* ---------------- Filtros / orden ---------------- */
    function applyFilters() {
        const term = state.searchTerm.trim().toLowerCase();
        const conf = state.confederation;

        let filtered = state.selections.filter((s) => {
            const matchesTerm = term
                ? String(s.country).toLowerCase().includes(term)
                : true;
            const matchesConf = conf ? s.confederation === conf : true;
            return matchesTerm && matchesConf;
        });

        // Orden
        filtered = sortSelections(filtered, state.sortBy);

        state.filtered = filtered;
        updateActiveFilters();

        if (state.selections.length === 0) {
            showOnly(dom.noDataState);
            setGridVisible(false);
            updateResultsCount(0, 0);
            return;
        }

        if (filtered.length === 0) {
            showOnly(dom.emptyState);
            setGridVisible(false);
            updateResultsCount(0, state.selections.length);
            return;
        }

        showOnly(null);
        renderGrid(filtered);
        updateResultsCount(filtered, state.selections.length);
    }

    function sortSelections(list, sortBy) {
        const sorted = [...list];
        switch (sortBy) {
            case 'world_cups':
                sorted.sort((a, b) => {
                    const diff = (Number(b.world_cups) || 0) - (Number(a.world_cups) || 0);
                    if (diff !== 0) return diff;
                    return String(a.country).localeCompare(String(b.country));
                });
                break;
            case 'confederation':
                sorted.sort((a, b) => {
                    const c = String(a.confederation).localeCompare(String(b.confederation));
                    if (c !== 0) return c;
                    return String(a.country).localeCompare(String(b.country));
                });
                break;
            case 'country':
            default:
                sorted.sort((a, b) =>
                    String(a.country).localeCompare(String(b.country))
                );
        }
        return sorted;
    }

    function clearAllFilters() {
        state.searchTerm = '';
        state.confederation = '';
        dom.searchInput.value = '';
        dom.searchClear.setAttribute('hidden', '');
        dom.confederationFilter.value = '';
        applyFilters();
        showToast('Filtros limpiados', 'info', 2000);
    }

    /* ---------------- Carga de datos ---------------- */
    let isLoading = false;
    let progressTimer = null;

    async function loadSelections(showFeedback = false) {
        if (isLoading) return;
        isLoading = true;

        setResultsBusy(true);
        renderSkeletons();
        showOnly(dom.loadingState);
        setGridVisible(false);
        dom.resultsCount.textContent = 'Cargando…';
        setButtonLoading(dom.reloadBtn, true);
        showProgress(true);

        // Asegurar mínimo de tiempo de progress para evitar parpadeo
        const progressStartedAt = Date.now();

        try {
            const data = await api.getSelections();
            state.selections = data;

            if (data.length === 0) {
                showOnly(dom.noDataState);
                setGridVisible(false);
                updateResultsCount(0, 0);
                updateSummary([]);
                if (showFeedback) showToast('La API no devolvió datos', 'info');
                return;
            }

            populateConfederationFilter(data);
            updateSummary(data);
            applyFilters();
            state.lastUpdate = Date.now();
            updateLastUpdate();

            if (showFeedback) {
                showToast(`${data.length} selecciones cargadas`, 'success');
            }
        } catch (error) {
            handleApiError(error);
            if (showFeedback) showToast('Error al cargar datos', 'error');
        } finally {
            const elapsed = Date.now() - progressStartedAt;
            const remaining = Math.max(0, PROGRESS_MIN_TIME - elapsed);
            setTimeout(() => {
                setResultsBusy(false);
                setButtonLoading(dom.reloadBtn, false);
                showProgress(false);
                isLoading = false;
            }, remaining);
        }
    }

    function setButtonLoading(button, loading) {
        if (!button) return;
        if (loading) {
            button.classList.add('is-loading');
            button.disabled = true;
        } else {
            button.classList.remove('is-loading');
            button.disabled = false;
        }
    }

    function handleApiError(error) {
        const message =
            error?.response?.data?.detail ||
            error?.message ||
            'Error desconocido al conectar con la API.';
        dom.errorMessage.textContent = `${message} — Verificá que el backend FastAPI esté ejecutándose en ${API_BASE_URL}`;
        showOnly(dom.errorState);
        setGridVisible(false);
        dom.resultsCount.textContent = 'Error';
        updateSummary([]);
    }

    /* ---------------- Scroll progress ---------------- */
    function initScrollProgress() {
        if (!dom.scrollProgressFill) return;

        const update = () => {
            const scrollTop = window.scrollY;
            const docHeight = document.documentElement.scrollHeight - window.innerHeight;
            const progress = docHeight > 0 ? (scrollTop / docHeight) * 100 : 0;
            dom.scrollProgressFill.style.width = `${Math.min(100, Math.max(0, progress))}%`;
        };

        window.addEventListener('scroll', update, { passive: true });
        window.addEventListener('resize', update);
        update();
    }

    /* ---------------- Back to top ---------------- */
    function initBackToTop() {
        if (!dom.backToTop) return;
        const toggle = () => {
            if (window.scrollY > 500) {
                dom.backToTop.removeAttribute('hidden');
            } else {
                dom.backToTop.setAttribute('hidden', '');
            }
        };
        window.addEventListener('scroll', toggle, { passive: true });
        toggle();
        dom.backToTop.addEventListener('click', () => {
            window.scrollTo({ top: 0, behavior: 'smooth' });
        });
    }

    /* ---------------- Scrollspy nav ---------------- */
    function initScrollspy() {
        const sections = ['selections', 'stats', 'about']
            .map((id) => document.getElementById(id))
            .filter(Boolean);
        if (!sections.length || !dom.navLinksItems.length) return;

        const setActive = (id) => {
            dom.navLinksItems.forEach((link) => {
                const targetId = link.getAttribute('href')?.replace('#', '');
                if (targetId === id) {
                    link.classList.add('nav__link--active');
                } else {
                    link.classList.remove('nav__link--active');
                }
            });
        };

        if (!('IntersectionObserver' in window)) return;

        const observer = new IntersectionObserver(
            (entries) => {
                entries.forEach((entry) => {
                    if (entry.isIntersecting) {
                        setActive(entry.target.id);
                    }
                });
            },
            { rootMargin: '-40% 0px -55% 0px' }
        );
        sections.forEach((s) => observer.observe(s));
    }

    /* ---------------- Atajos de teclado ---------------- */
    function initKeyboardShortcuts() {
        document.addEventListener('keydown', (event) => {
            const target = event.target;
            const isInputFocused =
                target.tagName === 'INPUT' ||
                target.tagName === 'TEXTAREA' ||
                target.tagName === 'SELECT' ||
                target.isContentEditable;

            // Cerrar modal/menú con Esc
            if (event.key === 'Escape') {
                if (!dom.modal.hasAttribute('hidden')) {
                    closeModal();
                    return;
                }
                if (dom.shortcutsHint && !dom.shortcutsHint.hasAttribute('hidden')) {
                    dom.shortcutsHint.setAttribute('hidden', '');
                    return;
                }
                if (dom.navLinks?.classList.contains('is-open')) {
                    dom.navLinks.classList.remove('is-open');
                    dom.navToggle?.classList.remove('is-open');
                    return;
                }
            }

            // "/" para buscar (solo si no estamos escribiendo)
            if (event.key === '/' && !isInputFocused) {
                event.preventDefault();
                dom.searchInput.focus();
                dom.searchInput.select();
                return;
            }

            // "R" para recargar (sin modifier, no en input)
            if ((event.key === 'r' || event.key === 'R') && !isInputFocused && !event.metaKey && !event.ctrlKey) {
                event.preventDefault();
                loadSelections(true);
                return;
            }

            // "?" para mostrar atajos (con shift)
            if (event.key === '?' && !isInputFocused) {
                event.preventDefault();
                if (dom.shortcutsHint) {
                    dom.shortcutsHint.removeAttribute('hidden');
                }
                return;
            }
        });

        if (dom.closeShortcuts && dom.shortcutsHint) {
            dom.closeShortcuts.addEventListener('click', () => {
                dom.shortcutsHint.setAttribute('hidden', '');
            });
            dom.shortcutsHint.addEventListener('click', (event) => {
                if (event.target === dom.shortcutsHint) {
                    dom.shortcutsHint.setAttribute('hidden', '');
                }
            });
        }
    }

    /* ---------------- Listeners ---------------- */
    function bindEvents() {
        // Búsqueda con debounce
        let searchTimer = null;
        dom.searchInput.addEventListener('input', (event) => {
            const value = event.target.value || '';
            dom.searchClear.toggleAttribute('hidden', value.length === 0);

            clearTimeout(searchTimer);
            searchTimer = setTimeout(() => {
                state.searchTerm = value;
                applyFilters();
            }, SEARCH_DEBOUNCE);
        });

        dom.searchClear.addEventListener('click', () => {
            dom.searchInput.value = '';
            state.searchTerm = '';
            dom.searchClear.setAttribute('hidden', '');
            applyFilters();
            dom.searchInput.focus();
        });

        dom.confederationFilter.addEventListener('change', (event) => {
            state.confederation = event.target.value || '';
            applyFilters();
            if (state.confederation) {
                showToast(`Filtrando por ${state.confederation}`, 'info', 1800);
            }
        });

        dom.sortBy.addEventListener('change', (event) => {
            state.sortBy = event.target.value || 'country';
            applyFilters();
        });

        dom.reloadBtn.addEventListener('click', () => loadSelections(true));
        dom.retryBtn.addEventListener('click', () => loadSelections(true));
        dom.clearFiltersBtn.addEventListener('click', clearAllFilters);
        if (dom.clearAllChips) {
            dom.clearAllChips.addEventListener('click', clearAllFilters);
        }

        // Click/teclado en tarjeta → modal
        dom.grid.addEventListener('click', (event) => {
            const card = event.target.closest('.card');
            if (!card) return;
            const id = card.dataset.id;
            const selection = state.selections.find((s) => String(s.id) === id);
            if (selection) openModal(selection);
        });

        dom.grid.addEventListener('keydown', (event) => {
            if (event.key !== 'Enter' && event.key !== ' ') return;
            const card = event.target.closest('.card');
            if (!card) return;
            event.preventDefault();
            const id = card.dataset.id;
            const selection = state.selections.find((s) => String(s.id) === id);
            if (selection) openModal(selection);
        });

        // Modal: cerrar
        if (dom.modal) {
            dom.modal.addEventListener('click', (event) => {
                if (event.target.matches('[data-close-modal]')) closeModal();
            });
        }

        // Menú móvil
        if (dom.navToggle && dom.navLinks) {
            dom.navToggle.addEventListener('click', () => {
                const open = dom.navLinks.classList.toggle('is-open');
                dom.navToggle.classList.toggle('is-open', open);
                dom.navToggle.setAttribute('aria-expanded', String(open));
            });
            dom.navLinks.addEventListener('click', (event) => {
                if (event.target.matches('[data-link]')) {
                    dom.navLinks.classList.remove('is-open');
                    dom.navToggle.classList.remove('is-open');
                }
            });
        }
    }

    /* ---------------- Init ---------------- */
    function init() {
        if (typeof axios === 'undefined') {
            dom.errorMessage.textContent =
                'Axios no se cargó correctamente. Revisá tu conexión a internet o el CDN.';
            showOnly(dom.errorState);
            return;
        }

        cacheDom();
        renderSkeletons();
        bindEvents();
        initScrollProgress();
        initBackToTop();
        initScrollspy();
        initKeyboardShortcuts();
        startLastUpdateTicker();
        loadSelections();
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
