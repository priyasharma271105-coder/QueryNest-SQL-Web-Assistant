/**
 * QueryNest Voice Input Module — voice-input.js
 * ─────────────────────────────────────────────
 * Supports: Hindi (hi-IN) and English (en-IN / en-US)
 * Features:
 *   - Auto language detection (Hindi / English)
 *   - Devanagari → English keyword translation
 *   - Hinglish → English normalization
 *   - Works on any input: chat box, search box
 *   - Non-programming queries blocked with error
 *
 * Usage:
 *   QNVoice.init('micBtn', 'chatInput');
 *   QNVoice.init('searchMicBtn', 'searchInput');
 */

var QNVoice = (function () {
    'use strict';

    // ── Devanagari + Hinglish → English map ───────────────────────
    var HINDI_TO_ENG = {
        // Devanagari (pure Hindi)
        'प्राइम नंबर':   'prime number',
        'प्राइम नम्बर':  'prime number',
        'फिबोनाची':      'fibonacci',
        'फैक्टोरियल':    'factorial',
        'पैलिंड्रोम':    'palindrome',
        'बबल सॉर्ट':    'bubble sort',
        'सॉर्टिंग':      'sorting',
        'सॉर्ट':         'sort',
        'लूप':           'loop',
        'ऐरे':           'array',
        'फंक्शन':        'function',
        'क्लास':         'class',
        'टेबल बनाओ':    'create table',
        'टेबल':          'table',
        'बनाओ':          'create',
        'डालो':          'insert',
        'दिखाओ':         'select',
        'अपडेट करो':    'update',
        'डिलीट करो':    'delete',
        'पायथन':         'python',
        'जावा':          'java',
        'सी प्लस प्लस': 'c++',
        'मोंगो':         'mongodb',
        'एसक्यूएल':      'sql',
        'आर्मस्ट्रांग':   'armstrong',
        'हर्षद नंबर':    'harshad number',
        'हर्षद':         'harshad',
        'स्वैप':         'swap',
        'रिवर्स':        'reverse',
        'पैटर्न':        'pattern',
        'रिकर्सन':       'recursion',
        'पॉइंटर':        'pointer',
        'का कोड दो':    '',
        'का कोड':       '',
        'कोड दो':       '',
        'दिखाएं':        'show',
        'बताओ':          '',
        'नंबर':          'number',
        'नम्बर':         'number',
        'सीरीज':         'series',
        'प्रोग्राम':     'program',
        'डेटाबेस':       'database',
        'इवन':           'even',
        'ऑड':           'odd',
        'तक':            'till',
        // Hinglish (Roman script)
        'prime ka code': 'prime number',
        'fibonacci ka code': 'fibonacci',
        'ka code do': '',
        'ka code': '',
        'code do': '',
        'batao': '',
        'mujhe': '',
        'chahiye': '',
        'python mein': 'python',
        'python me': 'python',
        'c mein': 'c',
        'c me': 'c',
        'java mein': 'java',
        'java me': 'java',
        'cpp mein': 'cpp',
        'c++ mein': 'c++',
        'sql mein': 'sql',
        'mysql mein': 'mysql',
        'mongodb mein': 'mongodb',
        'swap karo': 'swap',
        'reverse karo': 'reverse',
        'sort karo': 'sort',
        'print karo': 'print',
        'banao': 'create',
        'dikhao': 'select',
        'dalo': 'insert',
        'hatao': 'delete',
        'badlo': 'update',
        'even numbers': 'even numbers',
        'odd numbers': 'odd numbers',
        'prime number': 'prime number',
        'prime no': 'prime number',
        'armstrong no': 'armstrong number',
        'fibo': 'fibonacci',
    };

    // ── Programming keywords for gate check ──────────────────────
    var PROG_KEYWORDS = [
        'prime','fibonacci','factorial','palindrome','armstrong','swap','even','odd',
        'sort','search','array','loop','function','class','recursion','pointer',
        'stack','queue','linked list','tree','graph','binary','pattern','matrix',
        'string','reverse','anagram','harshad','happy','perfect','gcd','lcm',
        'select','insert','update','delete','create','drop','alter','join','table',
        'group by','index','view','trigger','procedure','transaction',
        'find','aggregate','lookup','mongodb','insertone','updateone',
        'python','java','c++','cpp','sql','mysql','javascript',
        'oop','inheritance','interface','exception','file handling',
        'bubble','insertion','selection','merge','quick','linear','binary',
        'number','series','code','program','algorithm','data structure',
        'print','output','compile','run','debug','error',
        // Hindi keywords (after translation)
        'prime number','even number','odd number','harshad','armstrong',
    ];

    // ── Check if query is programming/DB related ──────────────────
    function isProgrammingQuery(text) {
        var q = text.toLowerCase();
        return PROG_KEYWORDS.some(function(kw) { return q.indexOf(kw) !== -1; });
    }

    // ── Check if text contains Devanagari script ──────────────────
    function isDevanagari(text) {
        return /[\u0900-\u097F]/.test(text);
    }

    // ── Translate Hindi/Hinglish to English ───────────────────────
    function translateToEnglish(text) {
        var result = text.toLowerCase().trim();

        // Replace all known Hindi/Hinglish phrases
        Object.keys(HINDI_TO_ENG).forEach(function(hindi) {
            var eng = HINDI_TO_ENG[hindi];
            result = result.split(hindi).join(eng);
        });

        // Remove remaining Devanagari characters
        result = result.replace(/[\u0900-\u097F]+/g, ' ');

        // Clean up extra spaces
        result = result.replace(/\s+/g, ' ').trim();

        return result;
    }

    // ── Speech recognition setup ──────────────────────────────────
    var SR = window.SpeechRecognition || window.webkitSpeechRecognition;

    /**
     * Initialize voice input on a button + input pair
     * @param {string} btnId   - ID of the mic button element
     * @param {string} inputId - ID of the text input element
     * @param {object} options - { onResult, onError, onStart, onEnd }
     */
    function init(btnId, inputId, options) {
        var btn   = document.getElementById(btnId);
        var input = document.getElementById(inputId);
        options   = options || {};

        if (!btn || !input) {
            console.warn('[QNVoice] Element not found:', btnId, inputId);
            return;
        }

        if (!SR) {
            btn.style.opacity = '0.4';
            btn.title = 'Voice: Chrome/Edge mein kaam karta hai';
            btn.onclick = function () {
                alert('🎤 Voice input sirf Chrome ya Edge browser mein kaam karta hai.');
            };
            return;
        }

        var rec = new SR();
        rec.continuous      = false;
        rec.interimResults  = false;
        rec.maxAlternatives = 1;
        var listening = false;

        // ── Language cycling: Hindi → English India → English US ──
        var langs = ['hi-IN', 'en-IN', 'en-US'];
        var langIdx = 0;  // start with Hindi
        rec.lang = langs[langIdx];

        function setListening(val) {
            listening = val;
            if (val) {
                btn.classList.add('recording');
                btn.textContent = '🔴';
                btn.title = 'Bol raha hoon... (click to stop)';
            } else {
                btn.classList.remove('recording');
                btn.textContent = '🎤';
                btn.title = 'Voice input — Hindi ya English bolein';
            }
        }

        btn.onclick = function () {
            if (listening) {
                rec.stop();
                return;
            }
            rec.lang = langs[langIdx];
            try {
                rec.start();
            } catch(e) {
                console.warn('[QNVoice] start error:', e);
            }
        };

        // ── Long-press to switch language ─────────────────────────
        var pressTimer;
        btn.addEventListener('mousedown', function() {
            pressTimer = setTimeout(function() {
                langIdx = (langIdx + 1) % langs.length;
                var labels = ['🇮🇳 हिंदी', '🇮🇳 English (IN)', '🇺🇸 English (US)'];
                btn.title = 'Language: ' + labels[langIdx];
                showToast('Voice language: ' + labels[langIdx]);
            }, 700);
        });
        btn.addEventListener('mouseup', function() { clearTimeout(pressTimer); });
        btn.addEventListener('mouseleave', function() { clearTimeout(pressTimer); });

        rec.onstart = function () { setListening(true); if (options.onStart) options.onStart(); };
        rec.onend   = function () { setListening(false); if (options.onEnd) options.onEnd(); };

        rec.onresult = function (e) {
            var rawText = e.results[0][0].transcript.trim();
            console.log('[QNVoice] Raw:', rawText, '| Lang:', rec.lang);

            // ── Translate to English if Hindi detected ────────────
            var finalText = rawText;
            if (isDevanagari(rawText) || rec.lang === 'hi-IN') {
                finalText = translateToEnglish(rawText);
                console.log('[QNVoice] Translated:', finalText);
            }

            // ── Put text in input field ───────────────────────────
            if (finalText) {
                input.value = finalText;
                input.focus();

                // Trigger input event so any listeners update
                var ev = new Event('input', { bubbles: true });
                input.dispatchEvent(ev);

                if (options.onResult) {
                    options.onResult(finalText, rawText);
                }
            }
        };

        rec.onerror = function (e) {
            setListening(false);
            if (e.error === 'no-speech') {
                showToast('Koi awaaz nahi suni. Dobara try karein.');
                return;
            }
            if (e.error === 'not-allowed') {
                showToast('Microphone access denied. Browser settings check karein.');
                return;
            }
            if (e.error === 'aborted') return;
            console.warn('[QNVoice] Error:', e.error);
            if (options.onError) options.onError(e.error);
        };
    }

    // ── Small toast notification ──────────────────────────────────
    function showToast(msg) {
        var old = document.getElementById('qn-voice-toast');
        if (old) old.remove();
        var t = document.createElement('div');
        t.id = 'qn-voice-toast';
        t.textContent = msg;
        t.style.cssText = [
            'position:fixed','bottom:80px','left:50%','transform:translateX(-50%)',
            'background:rgba(107,76,227,0.95)','color:#fff','padding:8px 18px',
            'border-radius:20px','font-size:13px','z-index:9999',
            'animation:fadeIn .2s ease','pointer-events:none'
        ].join(';');
        document.body.appendChild(t);
        setTimeout(function() { if(t.parentNode) t.remove(); }, 2500);
    }

    // ── Public API ────────────────────────────────────────────────
    return {
        init: init,
        translateToEnglish: translateToEnglish,
        isProgrammingQuery: isProgrammingQuery,
        isDevanagari: isDevanagari,
    };

})();
