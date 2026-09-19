/* =========================================================
 *   دليل التقديم - JavaScript
 *   ========================================================= */

document.addEventListener('DOMContentLoaded', function() {

    // ============ 1. Accordion (فتح/إغلاق الكروت) ============
    window.toggleCard = function(button) {
        const card = button.closest('.accordion-card');
        if (!card) return;
        card.classList.toggle('open');
    };

    // ============ 2. شريط تقدم القراءة ============
    const progressBar = document.getElementById('readingProgress');
    if (progressBar) {
        window.addEventListener('scroll', function() {
            const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
            const docHeight = document.documentElement.scrollHeight - document.documentElement.clientHeight;
            const progress = (scrollTop / docHeight) * 100;
            progressBar.style.width = progress + '%';
        });
    }

    // ============ 3. زر العودة للأعلى ============
    const backToTop = document.getElementById('backToTop');
    if (backToTop) {
        window.addEventListener('scroll', function() {
            if (window.pageYOffset > 400) {
                backToTop.classList.add('show');
            } else {
                backToTop.classList.remove('show');
            }
        });
    }

    window.scrollToTop = function() {
        window.scrollTo({ top: 0, behavior: 'smooth' });
    };

    // ============ 4. البحث الداخلي ============
    const searchInput = document.getElementById('guideSearch');
    const searchClear = document.querySelector('.search-clear');
    const searchResults = document.getElementById('searchResults');
    const allCards = document.querySelectorAll('[data-searchable]');

    if (searchInput) {
        searchInput.addEventListener('input', function() {
            const query = this.value.trim().toLowerCase();

            // إظهار/إخفاء زر المسح
            if (searchClear) {
                searchClear.style.display = query ? 'flex' : 'none';
            }

            if (query.length < 2) {
                if (searchResults) searchResults.style.display = 'none';
                allCards.forEach(card => card.style.display = '');
                return;
            }

            // البحث
            const results = [];
            allCards.forEach(card => {
                const searchable = card.getAttribute('data-searchable') || '';
                if (searchable.includes(query)) {
                    card.style.display = '';
                    const titleEl = card.querySelector('strong, h3, h4');
                    if (titleEl) {
                        results.push({
                            title: titleEl.textContent.trim(),
                            element: card,
                        });
                    }
                } else {
                    card.style.display = 'none';
                }
            });

            // عرض النتائج السريعة
            if (searchResults && results.length > 0) {
                searchResults.innerHTML = results.slice(0, 8).map(r => `
                    <div class="search-result-item" onclick="jumpToResult(this)">
                        <strong>${r.title}</strong>
                        <small>اضغط للانتقال</small>
                    </div>
                `).join('');
                searchResults.style.display = 'block';

                // إضافة مرجع للعنصر
                const items = searchResults.querySelectorAll('.search-result-item');
                items.forEach((item, i) => {
                    item.dataset.targetId = results[i].element.dataset.sectionId || '';
                });
            } else if (searchResults) {
                searchResults.innerHTML = '<div style="padding:20px; text-align:center; color:#94a3b8;">لا توجد نتائج</div>';
                searchResults.style.display = 'block';
            }
        });
    }

    window.clearSearch = function() {
        if (searchInput) {
            searchInput.value = '';
            searchInput.dispatchEvent(new Event('input'));
        }
    };

    window.jumpToResult = function(element) {
        const targetId = element.dataset.targetId;
        if (targetId) {
            const section = document.querySelector(`[data-section-id="${targetId}"]`);
            if (section) {
                section.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }
        }
        if (searchResults) searchResults.style.display = 'none';
    };

    // ============ 5. العداد التنازلي ============
    function updateCountdowns() {
        const countdowns = document.querySelectorAll('[data-countdown]');
        countdowns.forEach(el => {
            const targetDate = new Date(el.dataset.countdown);
            const now = new Date();
            const diff = targetDate - now;

            if (diff <= 0) {
                el.classList.add('countdown-past');
                el.innerHTML = '<span style="font-size:0.8rem;">انتهى</span>';
                return;
            }

            const days = Math.floor(diff / (1000 * 60 * 60 * 24));

            const numberEl = el.querySelector('.countdown-number');
            if (numberEl) {
                numberEl.textContent = days;
            }
        });
    }

    updateCountdowns();
    setInterval(updateCountdowns, 60000); // كل دقيقة

    // ============ 6. مشاركة الدليل ============
    window.shareGuide = function() {
        const shareData = {
            title: document.title,
            text: 'دليل التقديم للجامعات السودانية',
            url: window.location.href,
        };

        if (navigator.share) {
            navigator.share(shareData).catch(() => {
                copyToClipboard(window.location.href);
            });
        } else {
            copyToClipboard(window.location.href);
        }
    };

    function copyToClipboard(text) {
        if (navigator.clipboard) {
            navigator.clipboard.writeText(text).then(() => {
                showToast('✅ تم نسخ الرابط');
            }).catch(() => {
                fallbackCopy(text);
            });
        } else {
            fallbackCopy(text);
        }
    }

    function fallbackCopy(text) {
        const ta = document.createElement('textarea');
        ta.value = text;
        ta.style.position = 'fixed';
        ta.style.opacity = '0';
        document.body.appendChild(ta);
        ta.select();
        try {
            document.execCommand('copy');
            showToast('✅ تم نسخ الرابط');
        } catch (e) {
            alert('الرابط: ' + text);
        }
        document.body.removeChild(ta);
    }

    function showToast(message) {
        const existing = document.getElementById('guideToast');
        if (existing) existing.remove();

        const toast = document.createElement('div');
        toast.id = 'guideToast';
        toast.textContent = message;
        toast.style.cssText = `
            position: fixed;
            bottom: 30px;
            left: 50%;
            transform: translateX(-50%);
            background: #1e293b;
            color: white;
            padding: 14px 28px;
            border-radius: 12px;
            font-weight: 700;
            z-index: 9999;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
            animation: slideUpToast 0.3s ease;
        `;
        document.body.appendChild(toast);
        setTimeout(() => toast.remove(), 2500);
    }

    // إضافة animation
    const style = document.createElement('style');
    style.textContent = `
        @keyframes slideUpToast {
            from { opacity: 0; transform: translateX(-50%) translateY(20px); }
            to   { opacity: 1; transform: translateX(-50%) translateY(0); }
        }
    `;
    document.head.appendChild(style);

    // ============ 7. فتح أول كرت من كل قسم عند الطباعة ============
    window.addEventListener('beforeprint', function() {
        document.querySelectorAll('.accordion-card').forEach(card => {
            card.classList.add('open');
        });
    });

});