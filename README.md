# Quera Video Sharing 🎬

[![Persian](https://img.shields.io/badge/Language-Persian-green.svg)](#-توضیحات-فارسی)
[![English](https://img.shields.io/badge/Language-English-blue.svg)](#-english-description)

---

## 🇬🇧 English Description

This project is a fully-featured backend platform for video sharing, developed using **Django** and **Django REST Framework (DRF)**. It serves as a professional portfolio project demonstrating the management of videos, users, premium subscriptions, and user interactions (comments and ratings).

### 🚀 Key Features
* **Token Authentication:** Secure user registration and login using Token-based Authentication.
* **Video Management (CRUD):** Upload, edit, and manage videos categorized as Free or Premium.
* **Premium Subscription System (VIP):** Intelligent access control using custom permissions (`IsPremiumOrOwner`). Premium videos are exclusive to users with an active 30-day subscription.
* **Payment Simulator:** Mock payment gateway integration for purchasing and auto-activating user subscriptions.
* **User Interactions:** API endpoints for adding comments and assigning 1 to 5-star ratings to videos.
* **Automated API Documentation:** Interactive and comprehensive documentation for all endpoints using Swagger UI.
* **Automated Testing:** Comprehensive test coverage (APITestCase) ensuring the reliability of business logic, user authentication, and premium access control.

### 🛠️ Technologies Used
* **Language:** Python 3
* **Framework:** Django 6.1
* **API:** Django REST Framework (DRF)
* **Database:** SQLite (Scalable to PostgreSQL)
* **Documentation:** drf-spectacular (Swagger UI)

### ⚙️ Installation & Setup

1. Clone the repository:
git clone https://github.com/amirrezaparvaneh/quera_video_sharing.git
cd quera_video_sharing

2. Create and activate a virtual environment:
python -m venv venv
source venv/bin/activate  # On Linux/Mac
# venv\Scripts\activate   # On Windows

3. Apply database migrations:
python manage.py makemigrations
python manage.py migrate

4. Run the development server:
python manage.py runserver


### 📚 API Documentation
Once the server is running, you can explore and test all APIs interactively via Swagger UI:
* **Swagger UI:** `http://127.0.0.1:8000/api/docs/`

### 🧪 Running Tests
To verify the system's business logic and access controls, run the automated tests:

python manage.py test


---

## 🇮🇷 توضیحات فارسی

این پروژه یک پلتفرم بک‌اند کامل برای اشتراک‌گذاری ویدیو است که با استفاده از **Django** و **Django REST Framework (DRF)** توسعه یافته است. این سیستم به عنوان یک نمونه‌کار حرفه‌ای برای مدیریت ویدیوها، کاربران، اشتراک‌های ویژه (Premium) و تعاملات کاربران (ثبت نظر و امتیاز) طراحی شده است.

### 🚀 ویژگی‌های کلیدی
* **احراز هویت توکنی:** ثبت‌نام و ورود امن کاربران (Token-based Authentication).
* **مدیریت ویدیوها (CRUD):** آپلود، ویرایش و مدیریت ویدیوها با قابلیت دسته‌بندی به دو نوع رایگان و پرمیوم.
* **سیستم اشتراک ویژه (VIP):** کنترل دسترسی هوشمند با پرمیشن‌های اختصاصی (`IsPremiumOrOwner`). ویدیوهای پرمیوم فقط برای کاربرانی که اشتراک فعال ۳۰ روزه دارند قابل تماشا است.
* **شبیه‌ساز سیستم مالی:** شبیه‌سازی درگاه پرداخت برای خرید و فعال‌سازی خودکار اشتراک کاربران.
* **تعاملات کاربری:** امکان ثبت نظر (Comment) و اختصاص امتیاز ۱ تا ۵ ستاره (Rating) برای هر ویدیو.
* **مستندات خودکار API:** مستندسازی تعاملی و کامل تمام اندپوینت‌ها با استفاده از Swagger UI.
* **تست‌های خودکار:** دارای پوشش تست (Automated Tests) برای بررسی صحت عملکرد منطق تجاری سیستم، ثبت‌نام‌ها و دسترسی به ویدیوها.

### 🛠️ تکنولوژی‌های استفاده شده
* **زبان برنامه‌نویسی:** Python 3
* **فریم‌ورک:** Django 6.1
* **وب‌سرویس:** Django REST Framework
* **پایگاه داده:** SQLite (قابل ارتقا به PostgreSQL)
* **مستندات:** drf-spectacular (Swagger)

### ⚙️ نصب و راه‌اندازی

۱. کلون کردن پروژه:
git clone https://github.com/amirrezaparvaneh/quera_video_sharing.git
cd quera_video_sharing

۲. ساخت و فعال‌سازی محیط مجازی:
python -m venv venv
source venv/bin/activate  # در لینوکس/مک
# venv\Scripts\activate   # در ویندوز

۳. اعمال مایگریشن‌های دیتابیس:
python manage.py makemigrations
python manage.py migrate

۴. اجرای سرور:
python manage.py runserver


### 📚 مستندات API
پس از اجرای سرور، برای مشاهده، بررسی و تست تمام APIهای ساخته شده به صورت گرافیکی، به آدرس زیر مراجعه کنید:
* **Swagger UI:** `http://127.0.0.1:8000/api/docs/`

### 🧪 اجرای تست‌ها
برای اطمینان از صحت عملکرد سیستم امنیتی دسترسی به ویدیوهای پرمیوم و احراز هویت، تست‌های خودکار پروژه را اجرا کنید:

python manage.py test
