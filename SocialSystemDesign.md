# پروژه: شبکه اجتماعی پیشرفته (Advanced Social Media System)

---

## 1. پیش‌نیازهای ذهنی و فنی

- Python 3.10.4
- Django 5.4
- MySQL 8.3
- Git
- Trello

---

## 2. برنامه‌ریزی پروژه (Project Planning)

### موضوع پروژه

شبکه اجتماعی (Social Media)

### Problem Statement

- نبود بستری برای ارتباط مستقیم کاربران با یکدیگر
- عدم وجود سیستم امن برای مدیریت ارتباطات، محتوای شخصی و تعاملی
- نیاز به پلتفرمی با رابط کاربری ساده، امن و سریع برای اشتراک‌گذاری پست‌ها

### Proposed Solution

ساخت یک شبکه اجتماعی با قابلیت ثبت‌نام، ایجاد پست، دنبال کردن کاربران، لایک، کامنت، و پیام‌رسانی.

### گروه‌های هدف (Users)

- زنان
- مردان

---

## 3. تحلیل و نیازمندی‌ها (Requirement and Analysis)

### Functional Requirements

1. ثبت‌نام و ورود کاربران (Authentication)
2. ایجاد و ویرایش پروفایل
3. دنبال‌کردن و دنبال‌شدن (Follow/Unfollow)
4. ساخت پست متنی یا تصویری
5. لایک کردن و کامنت گذاشتن روی پست‌ها
6. ارسال پیام خصوصی بین کاربران (Chat)
7. جستجوی کاربران و پست‌ها
8. قابلیت گزارش‌کردن پست یا کاربر
9. اعلان‌ها (Notifications)

### Non-Functional Requirements

- امنیت (Security)
- بهینه‌سازی (Optimization)
- رابط کاربری مناسب (Best UI)
- قابلیت مقیاس‌پذیری (Scalability)
- سهولت نگهداری (Maintainability)
- سازگاری با موبایل (Responsiveness)

---

## 4. طراحی سیستم (System Design)

1. طراحی ERD (نمودار رابطه موجودیت‌ها)
2. طراحی معماری (MVT + DRF)
3. طراحی UX/UI (با Figma یا ابزار دیگر)
4. طراحی فلوچارت تعامل کاربر

---

## 5. پیاده‌سازی (Implementation)

1. ساخت اپ‌ها (create apps)
2. طراحی مدل‌ها (create models)
3. ساخت فرم‌ها (create forms)
4. ساخت viewها
5. تعریف مسیرهای URL
6. اتصال به پایگاه داده
7. استفاده از Git برای کنترل نسخه

---

## 6. آزمون (Testing)
- ساخت اپ‌های accounts، posts، profiles، chat، notifications
- طراحی مدل‌ها با رعایت رابطه‌ها
- استفاده از DRF برای API‌ها
- پیاده‌سازی views برای APIView و GenericView
- استفاده از signals برای auto-create پروفایل و نوتیفیکیشن

1. آزمون دستی (Manual Testing)
2. آزمون خودکار با Django TestCase
3. آزمون امنیت (Security Test)
4. آزمون رابط کاربری (UI/UX Testing)
5. آزمون استفاده‌پذیری (Usability Testing)

---

## 7. استقرار (Deployment)

1. استفاده از GitLab یا GitHub
2. انتخاب سرور مانند Render
3. تنظیمات Production
4. گرفتن بک‌آپ از پایگاه داده
5. استفاده از `.env` برای حفاظت از اطلاعات حساس
6. استفاده از HTTPS
7. تنظیم Static و Media files
8. مانیتورینگ با ابزارهایی مانند Sentry یا UptimeRobot
