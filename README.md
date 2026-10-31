
# Quera Video Sharing 🎬

[![Persian](https://img.shields.io/badge/Language-Persian-green.svg)](#persian)
[![English](https://img.shields.io/badge/Language-English-blue.svg)](#english)

## English

### Overview

A Django REST API for a video-sharing application, with user accounts, video uploads, comments, ratings, watch history, and simulated subscriptions and payments. This repository contains the backend; it does not include a frontend, video transcoding, or a streaming service. The implementation is a development project with known limitations listed below.

### Features

- Registration with a unique email address, username/password login, and DRF authentication tokens.
- Video endpoints with file uploads and a premium flag; only staff can manage videos, and premium videos are limited to subscribers.
- Video detail logic that increments the view counter and records authenticated users' watch history.
- Comment and rating endpoints with owner-only changes and 1–5 scores, one rating per user and video.
- User-scoped subscription, payment, payment-history, and watch-history listings.
- Simulated payments that create and activate a 30-day subscription; separate renewal and cancellation endpoints.
- Django admin, session authentication, OpenAPI schema, and Swagger UI.

### Tech stack

Versions below are pinned in `requirements.txt`; Python 3.14.4 is the interpreter in the inspected local environment.

| Component | Version / configuration |
| --- | --- |
| Python | 3.14.4 locally |
| Django | 6.1.1 |
| Django REST Framework | 3.18.1 |
| drf-spectacular | 0.30.0 |
| Database | SQLite (`db.sqlite3`) |
| Authentication | DRF tokens and Django sessions |
| Application interfaces | WSGI and ASGI |

### Setup 🚀

You need Git, Python with `venv`, and access to a package index containing the pinned dependencies. The commands below use a Unix-like shell. The checked-in settings use SQLite and do not load an `.env` file.

1. Clone the repository and enter its directory:

   ```bash
   git clone https://github.com/amirrezaparvaneh/quera_video_sharing.git
   cd quera_video_sharing
   ```

2. Create and activate a virtual environment (the inspected environment uses Python 3.14):

   ```bash
   python3.14 -m venv venv
   source venv/bin/activate
   ```

   On Windows PowerShell, use:

   ```powershell
   py -3.14 -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

3. Install the dependencies:

   ```bash
   python -m pip install -r requirements.txt
   ```

4. Apply the existing migrations to create the local database:

   ```bash
   python manage.py migrate
   ```

5. Optionally create an administrator:

   ```bash
   python manage.py createsuperuser
   ```

6. Check the configuration and start the development server:

   ```bash
   python manage.py check
   python manage.py runserver
   ```

The server listens at `http://127.0.0.1:8000/`. There is no homepage route; open `/api/docs/` for Swagger UI or `/admin/` for administration. The raw OpenAPI schema is at `/api/schema/`, and the browsable API's session login is at `/api-auth/login/`.

### API reference

All paths below are relative to the local server and include their required trailing slash. CRUD means list/create with `GET`/`POST` on the collection, and retrieve/update/delete with `GET`/`PUT`/`PATCH`/`DELETE` on `/<id>/`.

| Path | Methods | Purpose |
| --- | --- | --- |
| `/api/users/register/` | POST | Register and return a token, user ID, and username |
| `/api/users/login/` | POST | Authenticate and return a token, user ID, and username |
| `/api/videos/videos/` | CRUD | Video metadata and file uploads |
| `/api/videos/comments/` | CRUD | Comments |
| `/api/videos/ratings/` | CRUD | Ratings |
| `/api/videos/watch-history/` | GET | Current user's watch history, newest first |
| `/api/finance/subscriptions/` | GET | Current user's subscriptions; detail at `/<id>/` |
| `/api/finance/payments/` | CRUD | Current user's simulated payments |
| `/api/finance/payments-history/` | GET | Current user's separate payment-history records, newest first |
| `/api/finance/cancel/` | POST | Deactivate the user's subscription |
| `/api/finance/renew/` | POST | Extend or reactivate a subscription for 30 days |

Registration and login accept anonymous requests. Videos and their comments and ratings can be read by anyone, but the file of a premium video is hidden in lists and its detail page is open only to staff and to users with an active, unexpired subscription. Only staff can create, change, or delete videos. Comments and ratings need a logged-in user, can be changed only by their owner (or staff), and for premium videos require premium access. A rating is a score from 1 to 5, one per user and video. Payments are simulated at a fixed price (`SUBSCRIPTION_PRICE`), are created but not edited, and each payment or renewal extends the user's single subscription by 30 days. Finance and history endpoints require authentication.

### Example requests

Register a user:

```bash
curl -X POST http://127.0.0.1:8000/api/users/register/ \
  -H 'Content-Type: application/json' \
  -d '{"username":"demo","email":"demo@example.com","password":"ExamplePassword123!"}'
```

Log in:

```bash
curl -X POST http://127.0.0.1:8000/api/users/login/ \
  -H 'Content-Type: application/json' \
  -d '{"username":"demo","password":"ExamplePassword123!"}'
```

Copy the returned `token` into a shell variable. The authorization scheme is `Token`:

```bash
export API_TOKEN='replace-with-returned-token'
curl http://127.0.0.1:8000/api/videos/watch-history/ \
  -H "Authorization: Token $API_TOKEN"
```

Upload a video using an existing local file:

```bash
curl -X POST http://127.0.0.1:8000/api/videos/videos/ \
  -H "Authorization: Token $API_TOKEN" \
  -F 'title=Demo video' \
  -F 'description=An example upload' \
  -F 'is_premium=false' \
  -F 'video_file=@/absolute/path/to/video.mp4'
```

Create a simulated payment and a new 30-day subscription:

```bash
curl -X POST http://127.0.0.1:8000/api/finance/payments/ \
  -H "Authorization: Token $API_TOKEN" \
  -H 'Content-Type: application/json' \
  -d '{"amount":"50000.00"}'
```

No money is transferred. The payment amount is supplied by the client and no currency is defined. Renewal separately writes a `PaymentHistory` entry with amount `50000` and status `Success`; creating a `Payment` does not create that history entry.

### Project layout

```text
core/             Settings, root URLs, WSGI and ASGI entry points
users/            Custom user model, registration, login, and tests
videos/           Videos, comments, ratings, permissions, history, and tests
subscriptions/    Subscriptions, simulated payments, and payment history
*/migrations/     Database migrations for each application
docs/             Entity relationship diagram (.drawio and .svg)
manage.py         Django management entry point
requirements.txt  Pinned dependencies
```

The diagram in `docs/` is a design reference and does not include the newer `PaymentHistory` model. Consult the models and migrations for the implemented schema.

### Checks and known limitations

Run the test suite (41 tests covering registration, login, video and premium access, comments, ratings, watch history, and subscriptions; uploads go to a temporary media directory):

```bash
python manage.py test
```

Configuration is read from environment variables. Defaults suit local development; for any real deployment set `DJANGO_DEBUG=False`, `DJANGO_SECRET_KEY`, and `DJANGO_ALLOWED_HOSTS` (the app refuses to start without a secret key when debug is off). Uploaded files are stored under `media/` and served by Django only while `DEBUG` is on.

Known limitations:

- **Billing:** payments are simulated, with no payment gateway. `Payment` and `PaymentHistory` are separate records, not a unified ledger.
- **View accounting:** opening a video's detail page counts as a view, not as confirmed playback, and repeated requests add watch-history rows.
- **Media delivery:** the file URLs of premium videos are visible to anyone who has access, and the media files themselves are not protected once the URL is known. Production storage and protected delivery need separate configuration.
- **Database:** SQLite is used for local development.

---

<a name="persian"></a>

## فارسی

### معرفی

این پروژه یک API مبتنی بر Django برای اشتراک‌گذاری ویدیو است و حساب کاربری، بارگذاری ویدیو، نظر، امتیاز، تاریخچه تماشا و اشتراک و پرداخت شبیه‌سازی‌شده را ارائه می‌کند. مخزن فقط شامل بک‌اند است و رابط کاربری، تبدیل فرمت ویدیو یا سرویس استریم ندارد. پروژه در وضعیت توسعه قرار دارد و محدودیت‌های فعلی آن در ادامه آمده است.

### قابلیت‌ها

- ثبت‌نام با ایمیل یکتا، ورود با نام کاربری و رمز عبور و دریافت توکن DRF.
- API ایجاد، مشاهده، ویرایش و حذف ویدیو، همراه با بارگذاری فایل و تعیین وضعیت ویژه.
- منطق افزایش شمارنده بازدید هنگام دریافت جزئیات ویدیو و ثبت تاریخچه برای کاربران واردشده.
- API ایجاد، مشاهده، ویرایش و حذف نظر و امتیاز.
- فهرست اشتراک‌ها، پرداخت‌ها و تاریخچه پرداخت و تماشای مختص هر کاربر.
- پرداخت شبیه‌سازی‌شده برای ایجاد و فعال‌سازی اشتراک ۳۰روزه و مسیرهای جداگانه تمدید و لغو.
- پنل مدیریت Django، احراز هویت نشست‌محور، اسکیما OpenAPI و رابط Swagger UI.

### فناوری‌ها

نسخه‌های زیر در `requirements.txt` ثبت شده‌اند. نسخه پایتون در محیط محلی بررسی‌شده 3.14.4 است.

| مؤلفه | نسخه یا تنظیمات |
| --- | --- |
| Python | نسخه 3.14.4 در محیط محلی |
| Django | 6.1.1 |
| Django REST Framework | 3.18.1 |
| drf-spectacular | 0.30.0 |
| پایگاه داده | SQLite در فایل `db.sqlite3` |
| احراز هویت | توکن DRF و نشست Django |
| رابط اجرای برنامه | WSGI و ASGI |

### نصب و راه‌اندازی 🚀

به Git، پایتون همراه با `venv` و دسترسی به مخزن بسته‌های حاوی نسخه‌های مشخص‌شده نیاز دارید. دستورهای اصلی برای محیط‌های شبه‌یونیکس هستند. تنظیمات موجود از SQLite استفاده می‌کنند و فایل `.env` را نمی‌خوانند.

۱. مخزن را دریافت کنید و وارد پوشه پروژه شوید:

```bash
git clone https://github.com/amirrezaparvaneh/quera_video_sharing.git
cd quera_video_sharing
```

۲. محیط مجازی را بسازید و فعال کنید؛ محیط بررسی‌شده از Python 3.14 استفاده می‌کند:

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

۴. برای ساخت پایگاه داده محلی، مایگریشن‌های موجود را اعمال کنید:

```bash
python manage.py migrate
```

۵. در صورت نیاز، کاربر مدیر بسازید:

```bash
python manage.py createsuperuser
```

۶. تنظیمات را بررسی و سرور توسعه را اجرا کنید:

```bash
python manage.py check
python manage.py runserver
```

آدرس سرور `http://127.0.0.1:8000/` است. مسیر صفحه اصلی تعریف نشده است؛ برای مستندات تعاملی به `/api/docs/` و برای پنل مدیریت به `/admin/` بروید. اسکیما OpenAPI در `/api/schema/` و ورود نشست‌محور API در `/api-auth/login/` قرار دارد.

### مسیرهای API

مسیرها نسبت به آدرس سرور هستند و اسلش پایانی دارند. CRUD به معنی دریافت فهرست و ایجاد با `GET` و `POST` روی مسیر مجموعه، و دریافت جزئیات، ویرایش و حذف با `GET`، `PUT`، `PATCH` و `DELETE` روی مسیر `/<id>/` است.

| مسیر | متدها | کاربرد |
| --- | --- | --- |
| `/api/users/register/` | POST | ثبت‌نام و دریافت توکن، شناسه و نام کاربری |
| `/api/users/login/` | POST | ورود و دریافت توکن، شناسه و نام کاربری |
| `/api/videos/videos/` | CRUD | اطلاعات و فایل ویدیو |
| `/api/videos/comments/` | CRUD | نظرها |
| `/api/videos/ratings/` | CRUD | امتیازها |
| `/api/videos/watch-history/` | GET | تاریخچه تماشای کاربر، از جدید به قدیم |
| `/api/finance/subscriptions/` | GET | اشتراک‌های کاربر؛ جزئیات در `/<id>/` |
| `/api/finance/payments/` | CRUD | پرداخت‌های شبیه‌سازی‌شده کاربر |
| `/api/finance/payments-history/` | GET | رکوردهای جداگانه تاریخچه پرداخت، از جدید به قدیم |
| `/api/finance/cancel/` | POST | غیرفعال‌سازی اشتراک کاربر |
| `/api/finance/renew/` | POST | تمدید یا فعال‌سازی مجدد اشتراک برای ۳۰ روز |

ثبت‌نام و ورود بدون احراز هویت قابل استفاده‌اند. همه می‌توانند ویدیوها، نظرها و امتیازها را بخوانند؛ اما فایل ویدیوی ویژه در فهرست پنهان است و صفحه جزئیات آن فقط برای کارکنان و کاربران دارای اشتراک فعال و منقضی‌نشده باز می‌شود. فقط کارکنان می‌توانند ویدیو بسازند، ویرایش کنند یا حذف کنند. نظر و امتیاز به کاربر واردشده نیاز دارد، فقط توسط مالک آن (یا کارکنان) قابل تغییر است و برای ویدیوی ویژه دسترسی ویژه لازم است. امتیاز عددی از ۱ تا ۵ است و برای هر کاربر و ویدیو فقط یکی ثبت می‌شود. پرداخت‌ها با قیمت ثابت (`SUBSCRIPTION_PRICE`) شبیه‌سازی می‌شوند، فقط ساخته و خوانده می‌شوند و هر پرداخت یا تمدید، اشتراک واحد کاربر را ۳۰ روز تمدید می‌کند. مسیرهای مالی و تاریخچه نیز مخصوص کاربران واردشده‌اند.

### نمونه درخواست‌ها

ثبت‌نام:

```bash
curl -X POST http://127.0.0.1:8000/api/users/register/ \
  -H 'Content-Type: application/json' \
  -d '{"username":"demo","email":"demo@example.com","password":"ExamplePassword123!"}'
```

ورود:

```bash
curl -X POST http://127.0.0.1:8000/api/users/login/ \
  -H 'Content-Type: application/json' \
  -d '{"username":"demo","password":"ExamplePassword123!"}'
```

مقدار `token` دریافتی را در متغیر زیر قرار دهید. پیشوند احراز هویت `Token` است:

```bash
export API_TOKEN='replace-with-returned-token'
curl http://127.0.0.1:8000/api/videos/watch-history/ \
  -H "Authorization: Token $API_TOKEN"
```

بارگذاری یک فایل ویدیوی موجود در سیستم:

```bash
curl -X POST http://127.0.0.1:8000/api/videos/videos/ \
  -H "Authorization: Token $API_TOKEN" \
  -F 'title=Demo video' \
  -F 'description=An example upload' \
  -F 'is_premium=false' \
  -F 'video_file=@/absolute/path/to/video.mp4'
```

ایجاد پرداخت شبیه‌سازی‌شده و اشتراک جدید ۳۰روزه:

```bash
curl -X POST http://127.0.0.1:8000/api/finance/payments/ \
  -H "Authorization: Token $API_TOKEN" \
  -H 'Content-Type: application/json' \
  -d '{"amount":"50000.00"}'
```

هیچ وجهی منتقل نمی‌شود. مبلغ پرداخت را کلاینت تعیین می‌کند و واحد پول مشخص نشده است. تمدید به‌صورت جداگانه یک رکورد `PaymentHistory` با مبلغ `50000` و وضعیت `Success` ثبت می‌کند؛ ایجاد `Payment` چنین رکوردی ایجاد نمی‌کند.

### ساختار پروژه

| مسیر | محتوا |
| --- | --- |
| `core/` | تنظیمات، مسیرهای اصلی و ورودی‌های WSGI و ASGI |
| `users/` | مدل کاربر، ثبت‌نام، ورود و تست‌ها |
| `videos/` | ویدیو، نظر، امتیاز، مجوزها، تاریخچه و تست‌ها |
| `subscriptions/` | اشتراک، پرداخت شبیه‌سازی‌شده و تاریخچه پرداخت |
| `*/migrations/` | مایگریشن‌های پایگاه داده هر برنامه |
| `docs/` | نمودار ارتباط موجودیت‌ها با فرمت‌های drawio و SVG |
| `manage.py` | اجرای دستورهای مدیریتی Django |
| `requirements.txt` | وابستگی‌ها با نسخه مشخص |

نمودار پوشه `docs/` یک مرجع طراحی است و مدل جدیدتر `PaymentHistory` را ندارد. برای ساختار پیاده‌سازی‌شده، مدل‌ها و مایگریشن‌ها را بررسی کنید.

### بررسی‌ها و محدودیت‌های شناخته‌شده

اجرای تست‌ها (۴۱ تست برای ثبت‌نام، ورود، دسترسی به ویدیو و ویدیوی ویژه، نظر، امتیاز، تاریخچه تماشا و اشتراک؛ فایل‌های بارگذاری‌شده در پوشه موقت رسانه ذخیره می‌شوند):

```bash
python manage.py test
```

پیکربندی از متغیرهای محیطی خوانده می‌شود. مقادیر پیش‌فرض برای توسعه محلی مناسب‌اند؛ برای استقرار واقعی `DJANGO_DEBUG=False`، `DJANGO_SECRET_KEY` و `DJANGO_ALLOWED_HOSTS` را تنظیم کنید (وقتی debug خاموش باشد و کلید مخفی تنظیم نشده باشد، برنامه اجرا نمی‌شود). فایل‌های بارگذاری‌شده در پوشه `media/` ذخیره می‌شوند و فقط وقتی `DEBUG` روشن است توسط Django ارائه می‌شوند.

محدودیت‌های شناخته‌شده:

- **پرداخت:** پرداخت‌ها شبیه‌سازی‌شده‌اند و درگاه پرداخت ندارند. `Payment` و `PaymentHistory` رکوردهای جداگانه‌اند و دفتر مالی یکپارچه نیستند.
- **شمارش بازدید:** باز کردن صفحه جزئیات ویدیو بازدید حساب می‌شود، نه پخش تأییدشده؛ درخواست‌های تکراری رکورد جدید در تاریخچه می‌سازند.
- **ارائه رسانه:** نشانی فایل ویدیوی ویژه برای کسی که دسترسی دارد دیده می‌شود و خود فایل‌ها پس از دانستن نشانی محافظت نشده‌اند. ذخیره‌سازی عملیاتی و ارائه محافظت‌شده به پیکربندی جداگانه نیاز دارد.
- **پایگاه داده:** برای توسعه محلی از SQLite استفاده می‌شود.
