/* =========================================================
 *   صفحة إدخال بيانات الجامعات - JavaScript
 *   ========================================================= */

// ============ Utilities ============
function getCookie(name) {
    let v = null;
    if (document.cookie) {
        const cs = document.cookie.split(';');
        for (let i = 0; i < cs.length; i++) {
            const c = cs[i].trim();
            if (c.substring(0, name.length + 1) === (name + '=')) {
                v = decodeURIComponent(c.substring(name.length + 1));
                break;
            }
        }
    }
    return v;
}

function showMessage(text, type = 'success') {
    const msg = document.getElementById('formMessage');
    msg.textContent = text;
    msg.className = 'form-message show ' + type;
    setTimeout(() => {
        msg.classList.remove('show');
    }, 4000);
}

function showModalMessage(text, type = 'error') {
    const msg = document.getElementById('modalMessage');
    msg.textContent = text;
    msg.className = 'form-message show ' + type;
    setTimeout(() => {
        msg.classList.remove('show');
    }, 4000);
}

// ============ Load Stats ============
function loadStats() {
    fetch('/universities/api/stats/')
        .then(r => r.json())
        .then(data => {
            if (data.success) {
                document.getElementById('statUniversities').textContent = data.universities;
                document.getElementById('statFaculties').textContent = data.faculties;
            }
        })
        .catch(() => {});
}

// ============ Load Faculties ============
function loadFaculties() {
    const universityId = document.getElementById('universitySelect').value;
    const content = document.getElementById('facultiesContent');
    const title = document.getElementById('facultiesTitle');

    if (!universityId) {
        content.innerHTML = `
            <div class="empty-state">
                <i class="fa-solid fa-hand-pointer"></i>
                <h3>اختر جامعة من القائمة أعلاه</h3>
                <p>سيتم عرض جميع كلياتها مع النسب</p>
            </div>
        `;
        title.textContent = 'اختر جامعة لعرض كلياتها';
        return;
    }

    content.innerHTML = `
        <div style="text-align:center; padding:40px;">
            <i class="fa-solid fa-spinner fa-spin fa-2x" style="color:#1e40af;"></i>
            <p style="margin-top:15px; color:#64748b;">جاري التحميل...</p>
        </div>
    `;

    fetch(`/universities/api/university/${universityId}/faculties/`)
        .then(r => r.json())
        .then(data => {
            if (!data.success) {
                content.innerHTML = `<div class="empty-state"><h3>خطأ في التحميل</h3></div>`;
                return;
            }

            title.textContent = `كليات ${data.university_name} (${data.faculties.length})`;

            if (data.faculties.length === 0) {
                content.innerHTML = `
                    <div class="empty-state">
                        <i class="fa-solid fa-inbox"></i>
                        <h3>لا توجد كليات بعد</h3>
                        <p>ابدأ بإضافة أول كلية</p>
                    </div>
                `;
                return;
            }

            let html = `
                <table class="faculties-table">
                    <thead>
                        <tr>
                            <th>#</th>
                            <th>اسم الكلية</th>
                            <th style="text-align:center;">النسبة</th>
                            <th style="text-align:left;">إجراءات</th>
                        </tr>
                    </thead>
                    <tbody>
            `;

            data.faculties.forEach((f, i) => {
                const percentage = f.min_percentage !== null ? f.min_percentage + '%' : '—';

                html += `
                    <tr>
                        <td>${i + 1}</td>
                        <td class="faculty-name">${escapeHtml(f.name)}</td>
                        <td style="text-align:center;">
                            ${f.min_percentage !== null
                                ? `<span class="percentage-badge"><i class="fa-solid fa-percent"></i>${f.min_percentage}</span>`
                                : '<span style="color:#94a3b8;">—</span>'}
                        </td>
                        <td>
                            <div class="action-buttons">
                                <button class="btn-icon edit" onclick="editFaculty(${f.id}, '${escapeJs(f.name)}', ${f.min_percentage || 0})" title="تعديل">
                                    <i class="fa-solid fa-edit"></i>
                                </button>
                                <button class="btn-icon delete" onclick="deleteFaculty(${f.id}, '${escapeJs(f.name)}')" title="حذف">
                                    <i class="fa-solid fa-trash"></i>
                                </button>
                            </div>
                        </td>
                    </tr>
                `;
            });

            html += `</tbody></table>`;
            content.innerHTML = html;
        })
        .catch(err => {
            console.error(err);
            content.innerHTML = `<div class="empty-state"><h3>خطأ في الاتصال</h3></div>`;
        });
}

// ============ Save Faculty ============
function saveFaculty() {
    const universityId = document.getElementById('universitySelect').value;
    const facultyName = document.getElementById('facultyName').value.trim();
    const minPercentage = document.getElementById('minPercentage').value.trim();

    // Validation
    if (!universityId) {
        showMessage('⚠️ الرجاء اختيار الجامعة أولاً', 'error');
        document.getElementById('universitySelect').focus();
        return;
    }

    if (!facultyName) {
        showMessage('⚠️ الرجاء إدخال اسم الكلية', 'error');
        document.getElementById('facultyName').focus();
        return;
    }

    if (!minPercentage) {
        showMessage('⚠️ الرجاء إدخال النسبة', 'error');
        document.getElementById('minPercentage').focus();
        return;
    }

    const percentage = parseFloat(minPercentage);
    if (isNaN(percentage) || percentage < 0 || percentage > 100) {
        showMessage('⚠️ النسبة يجب أن تكون بين 0 و 100', 'error');
        document.getElementById('minPercentage').focus();
        return;
    }

    // Disable button
    const btn = document.getElementById('saveBtn');
    btn.disabled = true;
    btn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> جاري الحفظ...';

    const formData = new FormData();
    formData.append('university_id', universityId);
    formData.append('faculty_name', facultyName);
    formData.append('min_percentage', minPercentage);

    fetch('/universities/api/save-faculty/', {
        method: 'POST',
        headers: {'X-CSRFToken': getCookie('csrftoken')},
        body: formData,
    })
    .then(r => r.json())
    .then(data => {
        btn.disabled = false;
        btn.innerHTML = '<i class="fa-solid fa-save"></i> حفظ وإضافة أخرى';

        if (data.success) {
            if (data.is_update) {
                showMessage(`✅ تم تحديث "${data.faculty_name}" بنسبة ${data.min_percentage}%`, 'success');
            } else {
                showMessage(`✅ تم إضافة "${data.faculty_name}" بنسبة ${data.min_percentage}%`, 'success');
            }

            // Clear form
            document.getElementById('facultyName').value = '';
            document.getElementById('minPercentage').value = '';
            document.getElementById('facultyName').focus();

            // Reload faculties + stats
            loadFaculties();
            loadStats();
        } else {
            showMessage('❌ ' + data.error, 'error');
        }
    })
    .catch(err => {
        console.error(err);
        btn.disabled = false;
        btn.innerHTML = '<i class="fa-solid fa-save"></i> حفظ وإضافة أخرى';
        showMessage('❌ خطأ في الاتصال بالسيرفر', 'error');
    });
}

// ============ Edit Faculty ============
function editFaculty(facultyId, name, percentage) {
    document.getElementById('facultyName').value = name;
    document.getElementById('minPercentage').value = percentage;
    document.getElementById('facultyName').focus();

    // Scroll to form
    document.querySelector('.entry-card').scrollIntoView({ behavior: 'smooth', block: 'start' });

    showMessage(`✏️ جاهز لتعديل "${name}" — عدّل البيانات ثم احفظ`, 'success');
}

// ============ Delete Faculty ============
function deleteFaculty(facultyId, name) {
    if (!confirm(`هل أنت متأكد من حذف "${name}"؟`)) return;

    fetch(`/universities/api/faculty/${facultyId}/delete/`, {
        method: 'POST',
        headers: {'X-CSRFToken': getCookie('csrftoken')},
    })
    .then(r => r.json())
    .then(data => {
        if (data.success) {
            showMessage(`✅ تم حذف "${name}"`, 'success');
            loadFaculties();
            loadStats();
        } else {
            showMessage('❌ ' + data.error, 'error');
        }
    })
    .catch(() => showMessage('❌ خطأ في الاتصال', 'error'));
}

// ============ Reload Faculties ============
function reloadFaculties() {
    if (document.getElementById('universitySelect').value) {
        loadFaculties();
        loadStats();
    }
}

// ============ University Modal ============
function openUniversityModal() {
    document.getElementById('newUniversityName').value = '';
    document.getElementById('newUniversityType').value = 'government';
    document.getElementById('modalMessage').classList.remove('show');

    new bootstrap.Modal(document.getElementById('universityModal')).show();
}

function createUniversity() {
    const name = document.getElementById('newUniversityName').value.trim();
    const type = document.getElementById('newUniversityType').value;

    if (!name) {
        showModalMessage('⚠️ الرجاء إدخال اسم الجامعة');
        return;
    }

    const formData = new FormData();
    formData.append('name', name);
    formData.append('university_type', type);

    fetch('/universities/api/create-university/', {
        method: 'POST',
        headers: {'X-CSRFToken': getCookie('csrftoken')},
        body: formData,
    })
    .then(r => r.json())
    .then(data => {
        if (data.success) {
            // Add to select
            const select = document.getElementById('universitySelect');
            const option = document.createElement('option');
            option.value = data.university_id;
            option.textContent = data.university_name;
            option.selected = true;
            select.appendChild(option);

            // Close modal
            bootstrap.Modal.getInstance(document.getElementById('universityModal')).hide();

            // Show success
            showMessage(`✅ تم إضافة "${data.university_name}" — ابدأ بإضافة كلياتها`, 'success');

            // Focus on faculty name
            document.getElementById('facultyName').focus();

            // Reload
            loadStats();
            loadFaculties();
        } else {
            showModalMessage('❌ ' + data.error);
        }
    })
    .catch(() => showModalMessage('❌ خطأ في الاتصال'));
}

// ============ Helpers ============
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function escapeJs(text) {
    return text.replace(/'/g, "\\'").replace(/"/g, '\\"').replace(/\n/g, '\\n');
}

// ============ Events ============
document.addEventListener('DOMContentLoaded', function() {
    // Load initial stats
    loadStats();

    // University select change
    document.getElementById('universitySelect').addEventListener('change', function() {
        loadFaculties();
        if (this.value) {
            document.getElementById('facultyName').focus();
        }
    });

    // Enter key → save
    document.getElementById('facultyName').addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            e.preventDefault();
            document.getElementById('minPercentage').focus();
        }
    });

    document.getElementById('minPercentage').addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            e.preventDefault();
            saveFaculty();
        }
    });

    // Enter in university modal
    document.getElementById('newUniversityName').addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            e.preventDefault();
            createUniversity();
        }
    });
});