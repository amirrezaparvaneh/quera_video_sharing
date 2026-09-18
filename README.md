<p align="center">
  <a href="#english">🇬🇧 English</a> &nbsp;|&nbsp; <a href="#persian">🇮🇷 فارسی</a>
</p>

# Quera Video Sharing 🎬

## English

### Overview

A Django REST API for a video-sharing application, with user accounts, video uploads, comments, ratings, watch history, and simulated subscriptions and payments. This repository contains the backend; it does not include a frontend, video transcoding, or a streaming service. The implementation is a development project with known limitations listed below.

### Features

- Registration with a unique email address, username/password login, and DRF authentication tokens.
- Video CRUD endpoints with file uploads and a premium flag.
- Video detail logic that increments the view counter and records authenticated users' watch history.
- Comment and rating CRUD endpoints.
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

Registration and login accept anonymous requests. Video, comment, and rating writes require authentication. Finance and history endpoints require authentication. Premium video object access permits staff or users with an active subscription; see the access-control limitations below.

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

### Checks and current limitations

Run the existing suite:

```bash
python manage.py test
```

The suite contains five tests for registration and video access; `subscriptions/tests.py` has no test cases. Video tests write uploaded files through the configured storage. During this documentation review, tests were run with a temporary media directory to avoid leaving uploads in the source tree.

Known issues retained unchanged in this comment/documentation cleanup:

- **Video retrieval:** `VideoViewSet.retrieve()` uses `Response` without importing it, causing a `NameError` after updating the counter and, for authenticated users, history. Two video-access tests error for this reason.
- **Duplicate model definitions:** `videos/models.py` defines `WatchHistory` twice and declares `Video.views_count` twice. Django emits a model-registration warning; `manage.py check` otherwise reports no issues.
- **Subscription renewal and cancellation:** a user can have multiple subscriptions, but these views assume one. Multiple records can raise `MultipleObjectsReturned`; renewal for a user without a subscription tries to create one without the required `end_date`.
- **Premium access:** the permission checks `is_active` without checking expiry. Object permissions do not filter the public video list, which includes premium metadata and file references.
- **Write permissions and ratings:** there is no owner-only enforcement for video, comment, or rating changes. Ratings have no explicit 1–5 range or per-user/video uniqueness rule. Registration uses `create_user()` without explicitly applying the configured password validators.
- **View accounting:** retrieving details counts as a view rather than confirmed playback; counter updates are not atomic, and repeated requests create additional watch-history rows.
- **Billing:** payments are simulated and the payment/subscription writes are not wrapped in an explicit transaction. `Payment` and `PaymentHistory` are separate records, not a unified billing ledger.
- **Media and deployment:** `MEDIA_ROOT`, `MEDIA_URL`, and media-serving routes are not configured. Uploaded files use the `videos/` upload prefix with default storage settings; playback is not configured. Settings include `DEBUG=True`, a development secret, and an empty `ALLOWED_HOSTS`. Deployment, protected media delivery, and production storage require separate configuration.

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

ثبت‌نام و ورود بدون احراز هویت قابل استفاده‌اند. تغییر ویدیو، نظر و امتیاز به احراز هویت نیاز دارد؛ مسیرهای مالی و تاریخچه نیز مخصوص کاربران واردشده هستند. دسترسی به شیء ویدیوی ویژه برای کارکنان یا دارندگان اشتراک فعال مجاز است؛ محدودیت‌های این کنترل دسترسی در ادامه توضیح داده شده است.

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

### بررسی‌ها و محدودیت‌های فعلی

اجرای تست‌های موجود:

```bash
python manage.py test
```

پنج تست برای ثبت‌نام و دسترسی به ویدیو وجود دارد؛ فایل `subscriptions/tests.py` فاقد مورد آزمون است. تست‌های ویدیو در فضای ذخیره‌سازی تنظیم‌شده فایل ایجاد می‌کنند. در این بازبینی، تست‌ها با پوشه موقت رسانه اجرا شدند تا فایل آزمایشی در کد پروژه باقی نماند.

موارد زیر در این پاک‌سازی توضیحات و مستندسازی، بدون تغییر باقی مانده‌اند:

- **دریافت جزئیات ویدیو:** متد `VideoViewSet.retrieve()` از `Response` بدون ایمپورت استفاده می‌کند و پس از افزایش بازدید و ثبت تاریخچه برای کاربر واردشده، خطای `NameError` می‌دهد. دو تست دسترسی به ویدیو به همین علت خطا دارند.
- **تعریف‌های تکراری:** مدل `WatchHistory` و فیلد `Video.views_count` هرکدام دوبار در `videos/models.py` تعریف شده‌اند. Django هشدار ثبت مجدد مدل می‌دهد؛ دستور `manage.py check` در سایر بررسی‌ها مشکلی گزارش نمی‌کند.
- **تمدید و لغو اشتراک:** مدل اجازه چند اشتراک برای یک کاربر را می‌دهد، اما این مسیرها وجود تنها یک اشتراک را فرض می‌کنند. چند رکورد ممکن است خطای `MultipleObjectsReturned` ایجاد کند؛ تمدید برای کاربر بدون اشتراک نیز تلاش می‌کند رکوردی بدون فیلد اجباری `end_date` بسازد.
- **دسترسی ویژه:** مجوز فقط `is_active` را بررسی می‌کند و تاریخ انقضا را در نظر نمی‌گیرد. مجوز سطح شیء، فهرست عمومی ویدیوها را فیلتر نمی‌کند؛ اطلاعات و ارجاع فایل ویدیوهای ویژه نیز در فهرست هستند.
- **مجوز تغییر و امتیازدهی:** تغییر ویدیو، نظر و امتیاز به مالک محدود نشده است. امتیاز بازه صریح ۱ تا ۵ یا قید یکتایی برای هر کاربر و ویدیو ندارد. ثبت‌نام از `create_user()` استفاده می‌کند، بدون اینکه اعتبارسنج‌های رمز عبور تنظیم‌شده را صریحاً اجرا کند.
- **شمارش بازدید:** دریافت جزئیات به‌عنوان بازدید ثبت می‌شود، نه پخش تأییدشده. افزایش شمارنده اتمیک نیست و درخواست‌های تکراری رکوردهای جدید تاریخچه ایجاد می‌کنند.
- **پرداخت:** پرداخت‌ها شبیه‌سازی‌شده‌اند و عملیات ثبت پرداخت و اشتراک در تراکنش صریح قرار نگرفته‌اند. `Payment` و `PaymentHistory` رکوردهای جداگانه هستند و دفتر مالی یکپارچه‌ای تشکیل نمی‌دهند.
- **رسانه و استقرار:** `MEDIA_ROOT`، `MEDIA_URL` و مسیر ارائه فایل رسانه تنظیم نشده‌اند. فایل‌ها با پیشوند `videos/` و تنظیمات پیش‌فرض ذخیره‌سازی ثبت می‌شوند؛ پخش ویدیو تنظیم نشده است. تنظیمات شامل `DEBUG=True`، کلید توسعه و `ALLOWED_HOSTS` خالی هستند. استقرار عملیاتی، ارائه محافظت‌شده رسانه و ذخیره‌سازی عملیاتی به پیکربندی جداگانه نیاز دارند.
