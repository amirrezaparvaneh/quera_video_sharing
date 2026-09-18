# 🎬 Quera Video Sharing

<p align="center">
  <a href="#persian">🇮🇷 راهنمای فارسی</a> · <a href="#english">🇬🇧 English guide</a>
</p>

<a id="persian"></a>

<div dir="rtl">

## 🇮🇷 معرفی پروژه

این پروژه، بک‌اند یک پلتفرم اشتراک‌گذاری ویدیو است که با <b dir="ltr">Django</b> و <b dir="ltr">Django REST Framework</b> توسعه یافته است. امکانات آن شامل مدیریت کاربران، ویدیوهای رایگان و ویژه، اشتراک‌ها، پرداخت‌های شبیه‌سازی‌شده، نظرات و امتیازها است.

### ✨ امکانات

- **احراز هویت:** ثبت‌نام و ورود کاربران با توکن.
- **مدیریت ویدیو:** ایجاد، مشاهده، ویرایش و حذف اطلاعات ویدیوها با امکان تعیین رایگان یا ویژه بودن آن‌ها.
- **اشتراک ویژه:** بررسی فعال بودن اشتراک برای دسترسی به جزئیات ویدیوهای ویژه؛ کاربران کارکنان نیز دسترسی دارند.
- **پرداخت شبیه‌سازی‌شده:** ثبت پرداخت و فعال‌سازی اشتراک کاربران.
- **تعامل کاربران:** ثبت نظر و امتیاز برای ویدیوها.
- **مستندات تعاملی:** مشاهده و آزمایش رابط‌های برنامه‌نویسی از طریق <span dir="ltr">Swagger UI</span>.
- **تست‌های خودکار:** بررسی منطق برنامه و دسترسی‌ها با تست‌های پروژه.

### 🛠️ فناوری‌ها

نام ابزارها و نسخه‌های ثبت‌شده در فایل وابستگی‌ها در جدول زیر آمده‌اند:

</div>

<div dir="ltr">

| Component | Technology |
| --- | --- |
| Language | Python |
| Framework | Django `6.1.1` |
| REST API | Django REST Framework `3.18.1` |
| Database | SQLite |
| API documentation | drf-spectacular `0.30.0` |
| Dependencies | `requirements.txt` |

</div>

<div dir="rtl">

### ⚙️ نصب و راه‌اندازی

پیش از شروع، پایتون، ابزار نصب بسته‌های آن و گیت باید روی سیستم نصب باشند.

#### ۱. دریافت پروژه

</div>

<div dir="ltr">

```bash
git clone https://github.com/amirrezaparvaneh/quera_video_sharing.git
cd quera_video_sharing
```

</div>

<div dir="rtl">

#### ۲. ساخت محیط مجازی

</div>

<div dir="ltr">

```bash
python -m venv .venv
```

</div>

<div dir="rtl">

**فعال‌سازی در لینوکس و مک:**

</div>

<div dir="ltr">

```bash
source .venv/bin/activate
```

</div>

<div dir="rtl">

**فعال‌سازی در پاورشل ویندوز:**

</div>

<div dir="ltr">

```powershell
.\.venv\Scripts\Activate.ps1
```

</div>

<div dir="rtl">

#### ۳. نصب وابستگی‌ها

</div>

<div dir="ltr">

```bash
python -m pip install -r requirements.txt
```

</div>

<div dir="rtl">

#### ۴. آماده‌سازی پایگاه داده

</div>

<div dir="ltr">

```bash
python manage.py migrate
```

</div>

<div dir="rtl">

#### ۵. اجرای سرور توسعه

</div>

<div dir="ltr">

```bash
python manage.py runserver
```

</div>

<div dir="rtl">

### 📚 مستندات تعاملی

پس از اجرای سرور، نشانی زیر را در مرورگر باز کنید تا مستندات را ببینید و درخواست‌ها را آزمایش کنید:

</div>

<div dir="ltr">

```text
http://127.0.0.1:8000/api/docs/
```

</div>

<div dir="rtl">

### 🧪 اجرای تست‌ها

در محیط مجازی فعال و از پوشهٔ اصلی پروژه، دستور زیر را اجرا کنید:

</div>

<div dir="ltr">

```bash
python manage.py test
```

</div>

---

<a id="english"></a>

<div dir="ltr">

## 🇬🇧 About the project

A video-sharing backend built with **Django** and **Django REST Framework**. The project includes user accounts, free and premium videos, subscriptions, simulated payments, comments, and ratings.

### ✨ Features

- **Authentication:** User registration and token-based login.
- **Video management:** Create, retrieve, update, and delete video records, with free and premium categories.
- **Premium access:** Active-subscription checks for premium video details, with access also granted to staff users.
- **Simulated payments:** Record payments and activate user subscriptions.
- **User interactions:** Add comments and ratings to videos.
- **Interactive documentation:** Explore and test API endpoints through Swagger UI.
- **Automated tests:** Project tests for application logic and access permissions.

### 🛠️ Technology stack

Versions below reflect the repository's `requirements.txt` file.

| Component | Technology |
| --- | --- |
| Language | Python |
| Framework | Django `6.1.1` |
| REST API | Django REST Framework `3.18.1` |
| Database | SQLite |
| API documentation | drf-spectacular `0.30.0` |

### ⚙️ Installation and setup

Install Python, pip, and Git before starting.

#### 1. Clone the repository

```bash
git clone https://github.com/amirrezaparvaneh/quera_video_sharing.git
cd quera_video_sharing
```

#### 2. Create a virtual environment

```bash
python -m venv .venv
```

**Activate on Linux or macOS:**

```bash
source .venv/bin/activate
```

**Activate in Windows PowerShell:**

```powershell
.\.venv\Scripts\Activate.ps1
```

#### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

#### 4. Apply database migrations

```bash
python manage.py migrate
```

#### 5. Start the development server

```bash
python manage.py runserver
```

### 📚 Interactive API documentation

With the server running, open the following address in your browser to explore the API and try requests:

```text
http://127.0.0.1:8000/api/docs/
```

### 🧪 Run tests

From the project root, with the virtual environment active:

```bash
python manage.py test
```

</div>
