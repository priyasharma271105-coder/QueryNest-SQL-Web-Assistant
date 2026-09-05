/**
 * QueryNest — UI Module
 * Handles: nav tabs (filterLang), language cards, username load, logout
 */

'use strict';

// ── Nav Tab Filter ────────────────────────────────────────────
function filterLang(lang, el) {
    // Update active tab and set data-lang
    document.querySelectorAll('.nav-tab').forEach(t => t.classList.remove('active'));
    el.classList.add('active');
    el.setAttribute('data-lang', lang.toLowerCase());  // ensure data-lang is always set

    // Sync language selector with tab
    const tabToLang = {
        'all': null, 'sql': 'sql', 'mysql': 'mysql', 'mongodb': 'mongodb',
        'python': 'python', 'java': 'java', 'c/c++': 'cpp', 'cpp': 'cpp',
    };
    const mappedLang = tabToLang[lang.toLowerCase()];
    if (mappedLang) {
        const sel = document.getElementById('langSelect');
        if (sel) {
            sel.value = mappedLang;
            if (typeof updateLanguage === 'function') updateLanguage();
        }
    }
    // Close search results when switching tab
    const panel = document.getElementById('searchResultPanel');
    if (panel) panel.style.display = 'none';
}

// ── Load username into nav ────────────────────────────────────
async function loadUsername() {
    try {
        const r = await fetch('/api/me');
        const d = await r.json();
        if (d.success && d.user?.name) {
            const el = document.getElementById('nav-username');
            if (el) el.textContent = d.user.name.split(' ')[0];
        }
    } catch (e) {
        // Silently ignore — user may not be logged in
    }
}

// ── Logout ────────────────────────────────────────────────────
function logout() {
    if (confirm('Logout karna chahte ho?')) {
        window.location.href = '/logout';
    }
}

// ── Init on page load ─────────────────────────────────────────
document.addEventListener('DOMContentLoaded', function () {
    loadUsername();
});
