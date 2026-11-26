# زیرساخت «استودیو ساخت و ویرایش فونت» (بخش اپلیکیشن)

استودیو **داخل اپلیکیشن نیست**؛ یک بستهٔ زیپ جدا است که کاربر دانلود (یا از حافظه «انزیپ») می‌کند.
اپلیکیشن فقط «میزبان» است: بسته را امن نصب می‌کند و صفحهٔ وب آن را داخل یک WebView بدون اینترنت اجرا می‌کند.

## ۱) ساختار بسته (زیپ)

```
manifest.json      ← مشخصات + SHA-256 همهٔ فایل‌ها
manifest.sig       ← امضای ECDSA P-256 مانیفست (Base64)   [در حالت توسعه اختیاری]
web/index.html     ← صفحهٔ ورودی
web/...            ← js / wasm / css / تصویر / فونت‌های نمونه
```

`manifest.json`:

```json
{
  "id": "font-studio",
  "applicationId": "irani.script.keyboards",
  "versionCode": 1,
  "versionName": "1.0.0",
  "minAppVersionCode": 1,
  "hostApi": 1,
  "entry": "web/index.html",
  "files": { "web/index.html": "<sha256>", "web/app.js": "<sha256>" }
}
```

- `applicationId` باید با اپلیکیشن یکی باشد ← بسته فقط روی همین اپلیکیشن نصب می‌شود.
- فایل اضافه/کم/دستکاری‌شده نسبت به `files` ← نصب رد می‌شود.
- پسوندهای مجاز: html htm js mjs css json wasm map txt md png jpg jpeg webp svg gif ico woff woff2 ttf otf bin dat csv
- سقف‌ها: ۶۰۰۰ فایل، ۴۰۰ مگابایت کل، ۱۲۰ مگابایت هر فایل. فایل‌های `__MACOSX` و `.DS_Store` نادیده گرفته می‌شوند.
- `manifest.json` باید در **ریشهٔ** زیپ باشد (نه داخل یک پوشه).

## ۲) ساخت و امضا

```bash
java tools/FontStudioPackager.java genkey keys/                 # یک‌بار؛ private.b64 را محرمانه نگه دارید
# محتوای keys/public.b64 را در res/values/fontstudio_keys.xml (font_studio_pubkey) بگذارید

java tools/FontStudioPackager.java pack web/ out/font-studio.zip \
     --version-code 1 --version-name 1.0.0 --key keys/private.b64
```

خروجی: `font-studio.zip` و `fontstudio.meta.json`. هر دو را در پوشهٔ **`createfonts`** مخزن
`ssanssak-hub/Ancient-Iranian-script-download-` بگذارید (آدرس خام:
`https://raw.githubusercontent.com/ssanssak-hub/Ancient-Iranian-script-download-/main/createfonts/`).

- کلید عمومی **خالی** = «حالت توسعه»: بستهٔ بی‌امضا هم نصب می‌شود (برای آزمایش).
- کلید عمومی **پر** = فقط بستهٔ امضاشده با کلید شما نصب می‌شود.
- برای متن فارسی از `--notes-file notes-fa.txt` (فایل UTF-8) و برای انگلیسی از `--notes-en-file` استفاده کنید. `fontstudio.meta.json` شامل `version`، `versionName`، `sha256`، `size`، `zip`، `minAppVersionCode`، `releasedAt`، `notes` و `notesEn` است و همین اطلاعات به اپلیکیشن داده می‌شود.

## ۳) امنیت اجرا

- صفحه از `https://appassets.androidplatform.net/studio/…` (فقط از پوشهٔ بستهٔ نصب‌شده) بارگذاری می‌شود.
- هر درخواست بیرون از این آدرس (اینترنت، `file://`، `content://`) **مسدود** است؛ CSP هم هیچ منبع بیرونی را نمی‌پذیرد.
- اسکریپت‌های **inline** مجاز نیستند؛ همهٔ JS باید فایل جدا باشد. (event handler درون‌خطی مثل `onclick="…"` هم مسدود است؛ با `addEventListener` یا `.onclick = fn` ببندید.)
- در `fontstudio.meta.json` فیلد `version` باید **عدد صحیح** و برابر `versionCode` مانیفست باشد. `wasm` مجاز است (`'wasm-unsafe-eval'`) و Worker از همین origin یا `blob:`.
- دوربین، میکروفن و موقعیت هرگز داده نمی‌شود.
- فونت‌های رمزنگاری‌شدهٔ دانلودی اپلیکیشن (SecureFontStore) به استودیو داده نمی‌شوند.

## ۴) رابط جاوااسکریپت (`window.FontStudioHost`)

در `index.html` اضافه کنید: `<script src="/__host/host.js"></script>`

| API | توضیح |
|---|---|
| `FontStudioHost.info` | `apiVersion, appVersionName, appVersionCode, androidSdk, lang ("fa"/"en"), rtl, dark, density, colors{background,toolbar,toolbarText,text}, packageVersion*, wsQuotaBytes, launch{action,fontName}` |
| `on(type, fn)` / `off` | رویدادها: `pause` و `resume` (برای ذخیرهٔ خودکار) |
| `pickFiles({multiple})` | → `[{id,name,size,mime,url}]` (آرایهٔ خالی = لغو) |
| `fetchBytes(url)` | → `Uint8Array` (برای `url` فایل‌های انتخاب‌شده) |
| `saveFile(data, name, mime)` | ذخیره در حافظه با انتخاب‌گر سیستم → `{saved, name}` |
| `shareFile(data, name, mime)` | برگهٔ اشتراک‌گذاری اندروید |
| `appFonts.list()` | فونت‌های اپلیکیشن: `{name, display, kind(bundled/downloaded/custom), exportable, isDefault, isSelected}` |
| `appFonts.exportToStudio(name)` | → `{name, bytes}` (فقط `exportable`) |
| `appFonts.install(data, displayName)` | افزودن TTF/OTF/TTC به فونت‌های اپلیکیشن |
| `ws.list/stat/usage/remove/move/putText/getText/put/read` | فضای کار خصوصی (پروژه‌ها، بازیابی خودکار؛ سهمیهٔ ۱ گیگابایت). با حذف استودیو پاک نمی‌شود |
| `toast, copyText, pasteText, openExternal(https), haptic, keepScreenOn, setOrientation('auto'/'portrait'/'landscape')` | سیستم |
| `setUnsaved(bool)` | هنگام خروج با تغییر ذخیره‌نشده هشدار نشان داده می‌شود |
| `setBackHandler(fn)` | `fn` اگر `true` برگرداند، دکمهٔ بازگشت مصرف شده است |
| `openManager()` / `close()` | صفحهٔ مدیریت استودیو / بستن |

`launch.action`: `none` | `new` | `editAppDefault` | `editAppFont` | `openFile`.

آدرس‌های مجازی: `/studio/…` (بسته)، `/__io/…` (فایل‌های موقت رد و بدل‌شده)، `/__ws/…` (فضای کار)، `/__host/host.js`.

## ۵) آزمایش بدون موتور

`tools/fontstudio-sample/web` یک صفحهٔ آزمایشی است که همهٔ APIهای بالا را امتحان می‌کند.
با `pack` (بدون `--key`) زیپ بسازید و با دکمهٔ «انزیپ فایل زیپ» در صفحهٔ استودیو نصب کنید.

## ۶) نکتهٔ انتشار در گوگل‌پلی

بسته فقط HTML/JS/WASM است که داخل WebView اجرا می‌شود (کد بومی/DEX دانلود نمی‌شود)، و دسترسی آن به اندروید
فقط از راه همین پل محدود است. اگر روزی فلیور `play` ساختید، قبل از انتشار سیاست «کد دانلودشده» را دوباره مرور کنید.

## ۷) قابلیت‌ها و ارتقای مستقل استودیو

- `FontStudioHost.capabilities()` → `{apiVersion, features:[…]}` و `FontStudioHost.has(name)`. در اپ‌های قدیمی‌تر این تابع نیست؛ استودیو باید در این حالت فهرست پایهٔ hostApi=1 را فرض کند و خطا ندهد.
- قانون: فهرست `FEATURES` در `FontStudioBridge.kt` فقط **اضافه** می‌شود؛ هرگز حذف/تغییر نام نمی‌دهیم.
- برای اینکه آپدیت استودیو به آپدیت اپ نیاز نداشته باشد: `--min-app` و `--host-api` را بالا نبرید (سقف در `tools/fontstudio-test/policy.json`) و ابزار تازه را فقط با JS/WASM بنویسید.
- اپ یک نسخهٔ قبلی از استودیو نگه می‌دارد؛ در صفحهٔ مدیریت دکمهٔ «بازگشت به نسخهٔ قبلی» هست.
- قبل از انتشار: `python tools/fontstudio-test/preflight.py <createfonts>`.
