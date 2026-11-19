/**
 * QueryNest — AI Assistant Module
 * Fixed: proper error handling, correct response parsing, no stale history issues
 */

let chatHistory = [];
let _lastChatLang = '';

// Clear chat history when language changes
window.clearChatHistory = function clearChatHistory() {
    chatHistory = [];
    const chatBox = document.getElementById('chatBox');
    if (chatBox) {
        chatBox.innerHTML = '<div class="chat-message assistant"><div class="message-content"><span style="color:rgba(220,200,255,.5);font-size:12px;">🔄 Language changed — Chat cleared. Naya sawaal poochho!</span></div></div>';
    }
}

// ── Send message to AI ─────────────────────────────────────────
window.sendMessage = async function sendMessage() {
    const input   = document.getElementById('aiInput');
    const chatBox = document.getElementById('chatBox');
    const sendBtn = document.querySelector('.btn-send');
    if (!input || !chatBox) return;

    const message = input.value.trim();
    if (!message) return;

    // Detect active language from nav tab or langSelect
    let lang = document.getElementById('langSelect')?.value || 'python';
    const activeTab = document.querySelector('.nav-tab.active');
    if (activeTab) {
        const tabLang = activeTab.getAttribute('data-lang') || 'python';
        const tabMap  = { sql:'sql', mysql:'mysql', mongodb:'mongodb',
                          python:'python', java:'java', cpp:'cpp',
                          'c/c++':'cpp', c:'c', all:'python' };
        lang = tabMap[tabLang] || lang;
    }

    // Clear history if language changed
    if (_lastChatLang && _lastChatLang !== lang) {
        chatHistory = [];
    }
    _lastChatLang = lang;

    appendMsg(chatBox, 'user', esc(message));
    input.value = '';
    chatHistory.push({ role: 'user', content: message });
    if (sendBtn) sendBtn.disabled = true;

    // Typing indicator
    const dots = document.createElement('div');
    dots.className = 'chat-message assistant';
    dots.id = 'typing-dots';
    dots.innerHTML = '<div class="message-content"><div class="typing-dots"><span></span><span></span><span></span></div></div>';
    chatBox.appendChild(dots);
    chatBox.scrollTop = chatBox.scrollHeight;

    try {
        // Keep last 6 messages only
        const trimmedHistory = chatHistory.slice(-6);

        const systemPrompt =
            'You are QueryNest AI — a smart, friendly programming assistant like ChatGPT.\n' +
            'Current language focus: ' + lang.toUpperCase() + '.\n' +
            'BEHAVIOR:\n' +
            '1. Write code ONLY in ' + lang.toUpperCase() + ' unless user asks for another language\n' +
            '2. Give COMPLETE, WORKING code — no placeholders or "..." shortcuts\n' +
            '3. Add short inline comments on important lines\n' +
            '4. Wrap ALL code in triple backticks with language label\n' +
            '5. After code, show expected output as a comment block\n' +
            '6. Respond in Hinglish — friendly and conversational tone\n' +
            '7. Explain HOW the code works in 2-3 sentences\n' +
            '8. NEVER refuse programming questions — always give a complete answer\n' +
            '9. For complex problems, break down logic before writing code';

        const resp = await fetch('/api/anthropic', {
            method:      'POST',
            headers:     { 'Content-Type': 'application/json' },
            credentials: 'include',
            body: JSON.stringify({
                system:   systemPrompt,
                messages: trimmedHistory,
            }),
        });

        document.getElementById('typing-dots')?.remove();

        if (!resp.ok) {
            const errText = await resp.text();
            throw new Error('Server error ' + resp.status + ': ' + errText.slice(0, 100));
        }

        const d = await resp.json();

        // Extract reply
        let reply = '';
        if (Array.isArray(d.content) && d.content.length > 0) {
            reply = d.content.find(b => b.type === 'text')?.text || '';
        }
        if (!reply && d.reply)   reply = d.reply;
        if (!reply && d.error)   reply = '⚠️ ' + d.error;
        if (!reply && d.message) reply = d.message;
        if (!reply) reply = '⚠️ Koi response nahi mila. Dobara try karo.';

        chatHistory.push({ role: 'assistant', content: reply });
        appendMsg(chatBox, 'assistant', formatAIText(reply));

        // Auto-load code to editor
        const code = extractCodeFromText(reply);
        if (code && typeof lastSearchCode !== 'undefined') lastSearchCode = code;

    } catch (e) {
        document.getElementById('typing-dots')?.remove();
        console.error('[QueryNest AI] Error:', e);
        appendMsg(chatBox, 'assistant', formatAIText(
            '⚠️ **Error:** ' + e.message + '\n\nDobara try karo.'
        ));
    } finally {
        if (sendBtn) sendBtn.disabled = false;
        chatBox.scrollTop = chatBox.scrollHeight;
    }
}

// ── Append message ─────────────────────────────────────────────
function appendMsg(box, role, html) {
    const d = document.createElement('div');
    d.className = 'chat-message ' + role;
    d.innerHTML = '<div class="message-content">' + html + '</div>';
    box.appendChild(d);
    box.scrollTop = box.scrollHeight;
}

// ── Format AI response ─────────────────────────────────────────
function formatAIText(text) {
    const codeBlocks = [];

    // 1. Extract code blocks and protect them with placeholders
    text = text.replace(/```(\w+)?\n?([\s\S]*?)```/g, function (_, l, code) {
        const placeholder = '___CODEBLOCK_' + codeBlocks.length + '___';
        const langLabel = (l || 'code').toUpperCase();
        // Preserve indentation: normalize CRLF and trim only leading/trailing blank lines
        let cleanCode = code.replace(/\r\n/g, '\n').replace(/^\n+|\s+$/g, '');
        let escaped = esc(cleanCode);
        escaped = escaped
            .replace(/(\/\/[^\n]*)/g,  '<span style="color:#6ee7b7;font-style:italic;">$1</span>')
            .replace(/(--\s[^\n]*)/g,  '<span style="color:#6ee7b7;font-style:italic;">$1</span>')
            .replace(/((?:^|\n)(#[^\n]*))/g, '$1<span style="color:#6ee7b7;font-style:italic;">$2</span>');

        const blockHtml = '<div class="code-wrap" style="margin:8px 0;border-radius:10px;overflow:hidden;border:1px solid rgba(107,76,227,.4);background:#0e0022;">'
            + '<div style="display:flex;align-items:center;justify-content:space-between;padding:6px 10px;background:rgba(255,255,255,.05);border-bottom:1px solid rgba(107,76,227,.25);">'
            + '<span style="font-size:11px;font-weight:700;color:#a78bfa;letter-spacing:.04em;">' + esc(langLabel) + '</span>'
            + '<button type="button" class="code-copy" onclick="copyCodeBlock(this)" style="background:rgba(167,139,250,.15);border:1px solid rgba(167,139,250,.35);color:#c4b5fd;border-radius:6px;padding:4px 10px;cursor:pointer;font-size:12px;font-weight:700;">📋 Copy</button>'
            + '</div>'
            + '<pre style="background:transparent;border:none;border-radius:0;padding:12px;margin:0;font-family:\'JetBrains Mono\',monospace;font-size:12px;overflow-x:auto;color:#a5f3fc;white-space:pre;">' + escaped + '</pre>'
            + '</div>';

        codeBlocks.push(blockHtml);
        return placeholder;
    });

    // 2. Format inline markdown and convert line breaks ONLY on non-code text
    text = text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
    text = text.replace(/`([^`]+)`/g,     '<code style="background:rgba(107,76,227,.3);padding:2px 5px;border-radius:4px;font-size:12px;font-family:monospace;">$1</code>');
    text = text.replace(/\n/g, '<br>');

    // 3. Restore protected code blocks
    text = text.replace(/___CODEBLOCK_(\d+)___/g, function (_, idx) {
        return codeBlocks[Number(idx)];
    });

    return text;
}

// ── Extract code block ─────────────────────────────────────────
function extractCodeFromText(text) {
    const m = text.match(/```[\w]*\n?([\s\S]*?)```/);
    return m ? m[1].trim() : '';
}

// ── Ask AI from search panel ───────────────────────────────────
window.askAIFromSearch = function askAIFromSearch(query) {
    const panel = document.getElementById('searchResultPanel');
    if (panel) panel.style.display = 'none';

    // Support both aiInput (queries page) and chatInput (home_premium page)
    const aiInput = document.getElementById('aiInput') || document.getElementById('chatInput');
    if (!aiInput) return;
    aiInput.scrollIntoView({ behavior: 'smooth', block: 'center' });
    setTimeout(function () {
        aiInput.value = query;
        aiInput.focus();
        // Support both sendMessage (queries page) and sendChat (home_premium page)
        if (typeof sendMessage === 'function') sendMessage();
        else if (typeof sendChat === 'function') sendChat();
    }, 700);
}

// ── Helper: escape HTML ────────────────────────────────────────
function esc(s) {
    return s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
}

window.copyCodeBlock = function copyCodeBlock(btn) {
    const wrap = btn && btn.closest ? btn.closest('.code-wrap') : null;
    const pre = wrap ? wrap.querySelector('pre') : null;
    if (!pre) return;

    let text = '';
    if (pre.querySelector('br')) {
        const clone = pre.cloneNode(true);
        clone.querySelectorAll('br').forEach(br => br.replaceWith('\n'));
        text = clone.textContent || '';
    } else {
        text = pre.textContent || '';
    }
    text = text.replace(/\r\n/g, '\n');
    if (!text) return;

    const orig = btn.textContent;
    const done = function () {
        btn.textContent = '✅ Copied!';
        btn.style.color = '#6ee7b7';
        setTimeout(function () {
            btn.textContent = orig;
            btn.style.color = '#c4b5fd';
        }, 1800);
    };
    const fallback = function () {
        const ta = document.createElement('textarea');
        ta.value = text;
        ta.setAttribute('readonly', '');
        ta.style.position = 'fixed';
        ta.style.left = '-9999px';
        document.body.appendChild(ta);
        ta.select();
        try { document.execCommand('copy'); } catch (e) {}
        document.body.removeChild(ta);
    };
    if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(text).then(done).catch(function () { fallback(); done(); });
    } else {
        fallback();
        done();
    }
};
