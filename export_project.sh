#!/bin/bash
# سكريبت لتصدير كل ملفات المشروع في ملف واحد

OUTPUT_FILE="project_dump.txt"

# امسح الملف إذا كان موجوداً
> "$OUTPUT_FILE"

echo "========================================" >> "$OUTPUT_FILE"
echo "📦 PROJECT DUMP - $(date)" >> "$OUTPUT_FILE"
echo "========================================" >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"

# ==================== 1. بنية المشروع ====================
echo "========================================" >> "$OUTPUT_FILE"
echo "🗂️ 1. هيكلة المشروع" >> "$OUTPUT_FILE"
echo "========================================" >> "$OUTPUT_FILE"
find . -type f \( -name "*.py" -o -name "*.html" -o -name "*.css" -o -name "*.js" -o -name "*.txt" -o -name "*.md" \) \
    -not -path "*/venv/*" \
    -not -path "*/env/*" \
    -not -path "*/__pycache__/*" \
    -not -path "*/migrations/*" \
    -not -path "*/staticfiles/*" \
    -not -path "*/node_modules/*" \
    -not -path "*/.git/*" \
    | sort >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"

# ==================== 2. ملفات Python ====================
echo "========================================" >> "$OUTPUT_FILE"
echo "🐍 2. ملفات Python" >> "$OUTPUT_FILE"
echo "========================================" >> "$OUTPUT_FILE"

find . -type f -name "*.py" \
    -not -path "*/venv/*" \
    -not -path "*/env/*" \
    -not -path "*/__pycache__/*" \
    -not -path "*/migrations/*" \
    -not -path "*/.git/*" \
    | sort | while read file; do
    echo "" >> "$OUTPUT_FILE"
    echo "─────── 📄 $file ───────" >> "$OUTPUT_FILE"
    cat "$file" >> "$OUTPUT_FILE"
    echo "" >> "$OUTPUT_FILE"
done

# ==================== 3. ملفات HTML ====================
echo "" >> "$OUTPUT_FILE"
echo "========================================" >> "$OUTPUT_FILE"
echo "📄 3. ملفات HTML" >> "$OUTPUT_FILE"
echo "========================================" >> "$OUTPUT_FILE"

find . -type f -name "*.html" \
    -not -path "*/venv/*" \
    -not -path "*/__pycache__/*" \
    -not -path "*/.git/*" \
    | sort | while read file; do
    echo "" >> "$OUTPUT_FILE"
    echo "─────── 📄 $file ───────" >> "$OUTPUT_FILE"
    cat "$file" >> "$OUTPUT_FILE"
    echo "" >> "$OUTPUT_FILE"
done

# ==================== 4. ملفات CSS ====================
echo "" >> "$OUTPUT_FILE"
echo "========================================" >> "$OUTPUT_FILE"
echo "🎨 4. ملفات CSS" >> "$OUTPUT_FILE"
echo "========================================" >> "$OUTPUT_FILE"

find . -type f -name "*.css" \
    -not -path "*/venv/*" \
    -not -path "*/.git/*" \
    | sort | while read file; do
    echo "" >> "$OUTPUT_FILE"
    echo "─────── 📄 $file ───────" >> "$OUTPUT_FILE"
    cat "$file" >> "$OUTPUT_FILE"
    echo "" >> "$OUTPUT_FILE"
done

# ==================== 5. ملفات JS ====================
echo "" >> "$OUTPUT_FILE"
echo "========================================" >> "$OUTPUT_FILE"
echo "⚡ 5. ملفات JavaScript" >> "$OUTPUT_FILE"
echo "========================================" >> "$OUTPUT_FILE"

find . -type f -name "*.js" \
    -not -path "*/venv/*" \
    -not -path "*/.git/*" \
    | sort | while read file; do
    echo "" >> "$OUTPUT_FILE"
    echo "─────── 📄 $file ───────" >> "$OUTPUT_FILE"
    cat "$file" >> "$OUTPUT_FILE"
    echo "" >> "$OUTPUT_FILE"
done

# ==================== 6. ملف requirements ====================
echo "" >> "$OUTPUT_FILE"
echo "========================================" >> "$OUTPUT_FILE"
echo "📦 6. requirements.txt" >> "$OUTPUT_FILE"
echo "========================================" >> "$OUTPUT_FILE"
if [ -f "requirements.txt" ]; then
    cat requirements.txt >> "$OUTPUT_FILE"
fi

# ==================== النتيجة النهائية ====================
echo "" >> "$OUTPUT_FILE"
echo "========================================" >> "$OUTPUT_FILE"
echo "✅ تم إنشاء الملف بنجاح!" >> "$OUTPUT_FILE"
echo "عدد الأسطر: $(wc -l < $OUTPUT_FILE)" >> "$OUTPUT_FILE"
echo "حجم الملف: $(du -h $OUTPUT_FILE | cut -f1)" >> "$OUTPUT_FILE"
echo "========================================" >> "$OUTPUT_FILE"

echo "✅ تم! الملف: $OUTPUT_FILE"
echo "📊 عدد الأسطر: $(wc -l < $OUTPUT_FILE)"
echo "📦 الحجم: $(du -h $OUTPUT_FILE | cut -f1)"
