/* =========================================================
   Main JavaScript - توب سينير
   ========================================================= */

// ===================== 1. فتح/إغلاق قائمة الموبايل =====================
function toggleMenu() {
    const navMenu = document.getElementById('navMenu');
    if (navMenu) navMenu.classList.toggle('open');
}

document.addEventListener('click', function (e) {
    const nav = document.getElementById('navMenu');
    const toggle = document.querySelector('.menu-toggle');
    if (!nav || !toggle) return;

    if (nav.classList.contains('open') &&
        !nav.contains(e.target) &&
        !toggle.contains(e.target)) {
        nav.classList.remove('open');
    }
});

// ===================== 2. التنبيه (Toast) =====================
let toastTimeout;
function showToast(message) {
    const toast = document.getElementById('toast');
    const msg = document.getElementById('toastMsg');
    if (!toast || !msg) return;

    msg.textContent = message;
    toast.classList.add('show');

    clearTimeout(toastTimeout);
    toastTimeout = setTimeout(() => {
        toast.classList.remove('show');
    }, 3500);
}

// ===================== 3. معالجة النماذج =====================
function handleForm(event) {
    event.preventDefault();
    showToast('تم إرسال بياناتك بنجاح! سنتواصل معك قريباً.');
    event.target.reset();
}