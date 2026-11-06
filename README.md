# Quera Video Sharing

[![Language: English](https://img.shields.io/badge/Language-English-blue.svg)](#english)
[![Language: Persian](https://img.shields.io/badge/Language-Persian-green.svg)](#فارسی)
![Django](https://img.shields.io/badge/Django-6.1-092E20?logo=django&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.14-3776AB?logo=python&logoColor=white)

<a id="english"></a>

## English

A Django REST API for a video-sharing service. It provides user accounts, video uploads, comments, ratings, watch history, and simulated subscriptions and payments.

This repository is the backend only. It does not include a frontend, video transcoding, or a streaming service.

### Contents

- [Features](#features)
- [Tech stack](#tech-stack)
- [Getting started](#getting-started)
- [API reference](#api-reference)
- [Example requests](#example-requests)
- [Project structure](#project-structure)
- [Testing](#testing)
- [Configuration](#configuration)
- [Known limitations](#known-limitations)

### Features

- **Accounts:** registration with a unique email address, username and password login, and token authentication.
- **Videos:** create, read, update, and delete videos with file uploads. Only staff can manage videos. Premium videos are restricted to subscribers.
- **Views and history:** opening a video's detail page increments its view counter and, for authenticated users, records a watch-history entry.
- **Engagement:** comments and ratings (1 to 5, one rating per user and video). Only the owner, or staff, can change or delete them.
- **Subscriptions and payments:** simulated payments create or extend a 30-day subscription. Renewal and cancellation are separate endpoints.
- **Tooling:** Django admin, session authentication for the browsable API, an OpenAPI schema, and Swagger UI.

### Tech stack

| Component | Version or configuration |
| --- | --- |
| Python | 3.14 |
| Django | 6.1.1 |
| Django REST Framework | 3.18.1 |
| drf-spectacular | 0.30.0 |
| Database | SQLite (`db.sqlite3`) |
| Authentication | DRF tokens and Django sessions |

Exact dependency versions are pinned in [`requirements.txt`](requirements.txt).

### Getting started

**Prerequisites:** Git, Python 3.14 with `venv`, and access to a package index.

1. Clone the repository:

   ```bash
   git clone https://github.com/amirrezaparvaneh/quera_video_sharing.git
   cd quera_video_sharing
   ```

2. Create and activate a virtual environment:

   ```bash
   python3.14 -m venv venv
   source venv/bin/activate
   ```

   On Windows (PowerShell):

   ```powershell
   py -3.14 -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

3. Install the dependencies:

   ```bash
   python -m pip install -r requirements.txt
   ```

4. Apply the migrations:

   ```bash
   python manage.py migrate
   ```

5. Optionally, create an administrator account:

   ```bash
   python manage.py createsuperuser
   ```

6. Verify the configuration and start the development server:

   ```bash
   python manage.py check
   python manage.py runserver
   ```

The server listens on `http://127.0.0.1:8000/`. The root URL has no page. Use these instead:

| URL | Purpose |
| --- | --- |
| `/api/v1/docs/` | Swagger UI |
| `/api/v1/schema/` | Raw OpenAPI schema |
| `/admin/` | Django admin |
| `/api-auth/login/` | Session login for the browsable API |

### API reference

All paths are relative to the server root and end with a trailing slash. For CRUD resources, the collection path supports `GET` (list) and `POST` (create), and the `<id>/` path supports `GET`, `PUT`, `PATCH`, and `DELETE`.

| Path | Methods | Description |
| --- | --- | --- |
| `/api/v1/users/register/` | `POST` | Register a user; returns a token, user ID, and username |
| `/api/v1/users/login/` | `POST` | Log in; returns a token, user ID, and username |
| `/api/v1/videos/videos/` | CRUD | Video metadata and file uploads |
| `/api/v1/videos/comments/` | CRUD | Comments |
| `/api/v1/videos/ratings/` | CRUD | Ratings |
| `/api/v1/videos/watch-history/` | `GET` | The current user's watch history, newest first |
| `/api/v1/finance/subscriptions/` | `GET` | The current user's subscriptions; details at `<id>/` |
| `/api/v1/finance/payments/` | CRUD | The current user's simulated payments |
| `/api/v1/finance/payments-history/` | `GET` | The current user's payment-history records, newest first |
| `/api/v1/finance/renew/` | `POST` | Extend or reactivate the subscription for 30 days |
| `/api/v1/finance/cancel/` | `POST` | Deactivate the current user's subscription |

**Access rules**

- Registration and login are open to anonymous users.
- Anyone can read videos, comments, and ratings. The file of a premium video is hidden from list responses. Its detail page is available only to staff and to users with an active, unexpired subscription.
- Only staff can create, update, or delete videos.
- Comments and ratings require authentication. Only their owner (or staff) can change them. Premium videos require premium access.
- Finance and history endpoints require authentication.

**Payments**

Payments are simulated. No money is transferred, and no payment gateway is involved. The price is fixed by `SUBSCRIPTION_PRICE` (50000). Each payment or renewal extends the user's single subscription by 30 days.

### Example requests

Replace `http://127.0.0.1:8000` with your server address if it differs.

**Register a user**

```bash
curl -X POST http://127.0.0.1:8000/api/v1/users/register/ \
  -H 'Content-Type: application/json' \
  -d '{"username":"demo","email":"demo@example.com","password":"ExamplePassword123!"}'
```

**Log in**

```bash
curl -X POST http://127.0.0.1:8000/api/v1/users/login/ \
  -H 'Content-Type: application/json' \
  -d '{"username":"demo","password":"ExamplePassword123!"}'
```

Store the returned `token` value. Requests use the `Token` authorization scheme:

```bash
export API_TOKEN='replace-with-returned-token'
curl http://127.0.0.1:8000/api/v1/videos/watch-history/ \
  -H "Authorization: Token $API_TOKEN"
```

**Upload a video** (staff account required)

```bash
curl -X POST http://127.0.0.1:8000/api/v1/videos/videos/ \
  -H "Authorization: Token $API_TOKEN" \
  -F 'title=Demo video' \
  -F 'description=An example upload' \
  -F 'is_premium=false' \
  -F 'video_file=@/absolute/path/to/video.mp4'
```

**Create a simulated payment** (activates a 30-day subscription)

```bash
curl -X POST http://127.0.0.1:8000/api/v1/finance/payments/ \
  -H "Authorization: Token $API_TOKEN" \
  -H 'Content-Type: application/json' \
  -d '{"amount":"50000.00"}'
```

Note: the client supplies `amount`, and no currency is defined. Renewal (`/finance/renew/`) writes a `PaymentHistory` record with amount `50000` and status `Success`. Creating a `Payment` does not write that record.

### Project structure

```text
core/             Settings, root URL configuration, WSGI and ASGI entry points
users/            Custom user model, registration, login, and tests
videos/           Videos, comments, ratings, permissions, watch history, and tests
subscriptions/    Subscriptions, simulated payments, payment history, and tests
*/migrations/     Database migrations for each app
docs/             Entity relationship diagram (draw.io source and SVG)
manage.py         Django management entry point
requirements.txt  Pinned dependencies
```

The diagram in `docs/` is a design reference. It does not include the `PaymentHistory` model. The models and migrations are the source of truth for the implemented schema.

### Testing

```bash
python manage.py test
```

The suite contains 41 tests covering registration, login, video and premium access, comments, ratings, watch history, and subscriptions. Uploaded files are written to a temporary media directory during tests.

### Configuration

Settings are read from environment variables. The defaults are for local development only.

| Variable | Default | Description |
| --- | --- | --- |
| `DJANGO_DEBUG` | `True` | Enables debug mode. Set to `False` in production. |
| `DJANGO_SECRET_KEY` | none | Required when `DJANGO_DEBUG` is `False`. |
| `DJANGO_ALLOWED_HOSTS` | empty | Comma-separated list of allowed host names. |

For a production deployment, set `DJANGO_DEBUG=False`, `DJANGO_SECRET_KEY`, and `DJANGO_ALLOWED_HOSTS`. Django refuses to start when debug mode is off and no secret key is set.

Uploaded files are stored in `media/`. Django serves them only while `DEBUG` is enabled.

### Known limitations

- **Payments:** payments are simulated and there is no payment gateway. `Payment` and `PaymentHistory` are separate records, not a unified ledger.
- **View counting:** opening a video's detail page counts as a view, not as confirmed playback. Repeated requests add watch-history entries.
- **Media delivery:** the file URL of a premium video is visible to anyone who has access to it, and the file itself is not protected once its URL is known. Production storage and protected delivery require separate configuration.
- **Database:** SQLite is used for local development.

---

<a id="فارسی"></a>

## فارسی

یک API مبتنی بر Django REST Framework برای سرویس اشتراک‌گذاری ویدیو. این پروژه حساب کاربری، بارگذاری ویدیو، نظر، امتیاز، تاریخچه تماشا و اشتراک و پرداخت شبیه‌سازی‌شده را پوشش می‌دهد.

این مخزن فقط بک‌اند است و رابط کاربری، تبدیل فرمت ویدیو و سرویس استریم ندارد.

### فهرست

- [قابلیت‌ها](#قابلیت‌ها)
- [فناوری‌ها](#فناوری‌ها)
- [شروع کار](#شروع-کار)
- [مرجع API](#مرجع-api)
- [نمونه درخواست‌ها](#نمونه-درخواست‌ها)
- [ساختار پروژه](#ساختار-پروژه)
- [تست‌ها](#تست‌ها)
- [پیکربندی](#پیکربندی)
- [محدودیت‌های شناخته‌شده](#محدودیت‌های-شناخته‌شده)

### قابلیت‌ها

- **حساب کاربری:** ثبت‌نام با ایمیل یکتا، ورود با نام کاربری و رمز عبور، و احراز هویت با توکن.
- **ویدیو:** ایجاد، مشاهده، ویرایش و حذف ویدیو همراه با بارگذاری فایل. فقط کارکنان می‌توانند ویدیو را مدیریت کنند. ویدیوهای ویژه فقط برای مشترکان قابل دسترسی‌اند.
- **بازدید و تاریخچه:** باز کردن صفحه جزئیات ویدیو، شمارنده بازدید را افزایش می‌دهد و برای کاربران واردشده رکورد تاریخچه تماشا ثبت می‌کند.
- **تعامل:** نظر و امتیاز (از ۱ تا ۵، با یک امتیاز برای هر کاربر و ویدیو). فقط مالک یا کارکنان می‌توانند آن‌ها را تغییر یا حذف کنند.
- **اشتراک و پرداخت:** پرداخت شبیه‌سازی‌شده یک اشتراک ۳۰ روزه ایجاد یا تمدید می‌کند. تمدید و لغو اشتراک مسیرهای جداگانه دارند.
- **ابزارهای توسعه:** پنل مدیریت Django، احراز هویت نشست‌محور برای رابط مرورگر API، اسکیمای OpenAPI و Swagger UI.

### فناوری‌ها

| مؤلفه | نسخه یا پیکربندی |
| --- | --- |
| Python | 3.14 |
| Django | 6.1.1 |
| Django REST Framework | 3.18.1 |
| drf-spectacular | 0.30.0 |
| پایگاه داده | SQLite (فایل `db.sqlite3`) |
| احراز هویت | توکن DRF و نشست Django |

نسخه دقیق وابستگی‌ها در [`requirements.txt`](requirements.txt) ثبت شده است.

### شروع کار

**پیش‌نیازها:** Git، Python 3.14 همراه با `venv` و دسترسی به مخزن بسته‌ها.

۱. مخزن را دریافت کنید:

   ```bash
   git clone https://github.com/amirrezaparvaneh/quera_video_sharing.git
   cd quera_video_sharing
   ```

۲. محیط مجازی بسازید و فعال کنید:

   ```bash
   python3.14 -m venv venv
   source venv/bin/activate
   ```

   در PowerShell ویندوز:

   ```powershell
   py -3.14 -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

۳. وابستگی‌ها را نصب کنید:

   ```bash
   python -m pip install -r requirements.txt
   ```

۴. مایگریشن‌ها را اعمال کنید:

   ```bash
   python manage.py migrate
   ```

۵. در صورت نیاز، حساب مدیر بسازید:

   ```bash
   python manage.py createsuperuser
   ```

۶. پیکربندی را بررسی و سرور توسعه را اجرا کنید:

   ```bash
   python manage.py check
   python manage.py runserver
   ```

سرور روی `http://127.0.0.1:8000/` اجرا می‌شود. مسیر ریشه صفحه‌ای ندارد. از مسیرهای زیر استفاده کنید:

| نشانی | کاربرد |
| --- | --- |
| `/api/v1/docs/` | Swagger UI |
| `/api/v1/schema/` | اسکیمای خام OpenAPI |
| `/admin/` | پنل مدیریت Django |
| `/api-auth/login/` | ورود نشست‌محور برای رابط مرورگر API |

### مرجع API

همه مسیرها نسبت به ریشه سرور هستند و با اسلش پایانی ختم می‌شوند. برای منابع CRUD، مسیر مجموعه از `GET` (فهرست) و `POST` (ایجاد) پشتیبانی می‌کند و مسیر `<id>/` از `GET`، `PUT`، `PATCH` و `DELETE`.

| مسیر | متدها | توضیح |
| --- | --- | --- |
| `/api/v1/users/register/` | `POST` | ثبت‌نام؛ بازگرداندن توکن، شناسه و نام کاربری |
| `/api/v1/users/login/` | `POST` | ورود؛ بازگرداندن توکن، شناسه و نام کاربری |
| `/api/v1/videos/videos/` | CRUD | اطلاعات ویدیو و بارگذاری فایل |
| `/api/v1/videos/comments/` | CRUD | نظرها |
| `/api/v1/videos/ratings/` | CRUD | امتیازها |
| `/api/v1/videos/watch-history/` | `GET` | تاریخچه تماشای کاربر جاری، از جدید به قدیم |
| `/api/v1/finance/subscriptions/` | `GET` | اشتراک‌های کاربر جاری؛ جزئیات در `<id>/` |
| `/api/v1/finance/payments/` | CRUD | پرداخت‌های شبیه‌سازی‌شده کاربر جاری |
| `/api/v1/finance/payments-history/` | `GET` | رکوردهای تاریخچه پرداخت کاربر جاری، از جدید به قدیم |
| `/api/v1/finance/renew/` | `POST` | تمدید یا فعال‌سازی مجدد اشتراک برای ۳۰ روز |
| `/api/v1/finance/cancel/` | `POST` | غیرفعال‌سازی اشتراک کاربر جاری |

**قواعد دسترسی**

- ثبت‌نام و ورود برای کاربران ناشناس باز است.
- همه می‌توانند ویدیوها، نظرها و امتیازها را بخوانند. فایل ویدیوی ویژه در پاسخ فهرست پنهان است. صفحه جزئیات آن فقط برای کارکنان و کاربرانی با اشتراک فعال و منقضی‌نشده در دسترس است.
- فقط کارکنان می‌توانند ویدیو ایجاد، ویرایش یا حذف کنند.
- نظر و امتیاز نیاز به احراز هویت دارند. فقط مالک آن‌ها (یا کارکنان) می‌تواند تغییرشان دهد. برای ویدیوی ویژه، دسترسی ویژه لازم است.
- مسیرهای مالی و تاریخچه نیز نیاز به احراز هویت دارند.

**پرداخت**

پرداخت‌ها شبیه‌سازی می‌شوند. هیچ وجهی منتقل نمی‌شود و درگاه پرداختی وجود ندارد. قیمت با `SUBSCRIPTION_PRICE` (برابر ۵۰۰۰۰) تعیین می‌شود. هر پرداخت یا تمدید، اشتراک واحد کاربر را ۳۰ روز تمدید می‌کند.

### نمونه درخواست‌ها

اگر آدرس سرور شما متفاوت است، `http://127.0.0.1:8000` را جایگزین کنید.

**ثبت‌نام کاربر**

```bash
curl -X POST http://127.0.0.1:8000/api/v1/users/register/ \
  -H 'Content-Type: application/json' \
  -d '{"username":"demo","email":"demo@example.com","password":"ExamplePassword123!"}'
```

**ورود**

```bash
curl -X POST http://127.0.0.1:8000/api/v1/users/login/ \
  -H 'Content-Type: application/json' \
  -d '{"username":"demo","password":"ExamplePassword123!"}'
```

مقدار `token` دریافتی را ذخیره کنید. درخواست‌ها از طرح احراز هویت `Token` استفاده می‌کنند:

```bash
export API_TOKEN='replace-with-returned-token'
curl http://127.0.0.1:8000/api/v1/videos/watch-history/ \
  -H "Authorization: Token $API_TOKEN"
```

**بارگذاری ویدیو** (نیاز به حساب کارکنان)

```bash
curl -X POST http://127.0.0.1:8000/api/v1/videos/videos/ \
  -H "Authorization: Token $API_TOKEN" \
  -F 'title=Demo video' \
  -F 'description=An example upload' \
  -F 'is_premium=false' \
  -F 'video_file=@/absolute/path/to/video.mp4'
```

**ایجاد پرداخت شبیه‌سازی‌شده** (فعال‌سازی اشتراک ۳۰ روزه)

```bash
curl -X POST http://127.0.0.1:8000/api/v1/finance/payments/ \
  -H "Authorization: Token $API_TOKEN" \
  -H 'Content-Type: application/json' \
  -d '{"amount":"50000.00"}'
```

نکته: مبلغ را کلاینت ارسال می‌کند و واحد پول تعریف نشده است. تمدید (`/finance/renew/`) یک رکورد `PaymentHistory` با مبلغ `50000` و وضعیت `Success` ثبت می‌کند. ایجاد `Payment` چنین رکوردی نمی‌سازد.

### ساختار پروژه

```text
core/             تنظیمات، مسیرهای اصلی و ورودی‌های WSGI و ASGI
users/            مدل کاربر، ثبت‌نام، ورود و تست‌ها
videos/           ویدیو، نظر، امتیاز، مجوزها، تاریخچه تماشا و تست‌ها
subscriptions/    اشتراک، پرداخت شبیه‌سازی‌شده، تاریخچه پرداخت و تست‌ها
*/migrations/     مایگریشن‌های پایگاه داده هر برنامه
docs/             نمودار ارتباط موجودیت‌ها (فایل draw.io و SVG)
manage.py         نقطه ورود دستورهای مدیریتی Django
requirements.txt  وابستگی‌ها با نسخه مشخص
```

نمودار پوشه `docs/` مرجع طراحی است و مدل `PaymentHistory` را ندارد. برای ساختار واقعی پایگاه داده، مدل‌ها و مایگریشن‌ها ملاک هستند.

### تست‌ها

```bash
python manage.py test
```

این مجموعه شامل ۴۱ تست است که ثبت‌نام، ورود، دسترسی به ویدیو و ویدیوی ویژه، نظر، امتیاز، تاریخچه تماشا و اشتراک را پوشش می‌دهد. فایل‌های بارگذاری‌شده در طول تست‌ها در یک پوشه موقت ذخیره می‌شوند.

### پیکربندی

تنظیمات از متغیرهای محیطی خوانده می‌شوند. مقادیر پیش‌فرض فقط برای توسعه محلی مناسب‌اند.

| متغیر | پیش‌فرض | توضیح |
| --- | --- | --- |
| `DJANGO_DEBUG` | `True` | فعال‌سازی حالت دیباگ. در محیط عملیاتی `False` قرار دهید. |
| `DJANGO_SECRET_KEY` | ندارد | وقتی `DJANGO_DEBUG` برابر `False` است الزامی است. |
| `DJANGO_ALLOWED_HOSTS` | خالی | فهرست نام میزبان‌های مجاز، جدا شده با کاما. |

در استقرار واقعی، `DJANGO_DEBUG=False`، `DJANGO_SECRET_KEY` و `DJANGO_ALLOWED_HOSTS` را تنظیم کنید. اگر حالت دیباگ خاموش باشد و کلید مخفی تنظیم نشده باشد، Django اجرا نمی‌شود.

فایل‌های بارگذاری‌شده در پوشه `media/` ذخیره می‌شوند. Django فقط وقتی `DEBUG` فعال است آن‌ها را ارائه می‌کند.

### محدودیت‌های شناخته‌شده

- **پرداخت:** پرداخت‌ها شبیه‌سازی‌شده‌اند و درگاه پرداخت ندارند. `Payment` و `PaymentHistory` رکوردهای جداگانه‌اند و دفتر مالی یکپارچه نیستند.
- **شمارش بازدید:** باز کردن صفحه جزئیات ویدیو بازدید حساب می‌شود، نه پخش تأییدشده. درخواست‌های تکراری رکورد جدید در تاریخچه ثبت می‌کنند.
- **ارائه رسانه:** نشانی فایل ویدیوی ویژه برای هر کسی که دسترسی دارد قابل مشاهده است و پس از دانستن نشانی، خود فایل محافظت نمی‌شود. ذخیره‌سازی عملیاتی و ارائه محافظت‌شده نیاز به پیکربندی جداگانه دارند.
- **پایگاه داده:** برای توسعه محلی از SQLite استفاده می‌شود.
