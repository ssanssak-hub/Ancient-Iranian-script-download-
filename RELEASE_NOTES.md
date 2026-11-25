<!-- ╔══════════════════════════════════════════════════════════════╗ -->
<!-- ║            📝 راهنمای یادداشت انتشار (RELEASE_NOTES)         ║ -->
<!-- ╚══════════════════════════════════════════════════════════════╝ -->
<!--  -->
<!-- 🔹 قبل از هر انتشار، تغییرات را زیر همین تیترها با جملات ساده بنویسید. -->
<!-- 🔹 هر مورد باید با «- » شروع شود (خط تیره + فاصله). -->
<!-- 🔹 تیتری که موردی ندارد را پاک کنید تا در Release خالی دیده نشود. -->
<!-- 🔹 خطوطی که مثل همین خط داخل کامنت هستند در Release نمایش داده نمی‌شوند. -->
<!-- 🔹 هر کامنت باید فقط یک خط باشد، و از خط جداکننده (سه خط تیره) استفاده نکنید. -->
<!-- 🔹 تا وقتی موردی ننویسید یا فایل را عوض نکنید، از پیام کامیت‌ها استفاده می‌شود. -->
<!--  -->
<!-- ┌────────────────── پیشوندهای کامیت (وقتی این فایل خالی است) ──────────────────┐ -->
<!-- │ feat:      ✨ ویژگی جدید            ← مثال: feat: افزودن انتخاب تم            │ -->
<!-- │ fix:       🐛 رفع باگ               ← مثال: fix: رفع کرش هنگام چرخش صفحه       │ -->
<!-- │ docs:      📚 مستندات               ← مثال: docs: بروزرسانی راهنما             │ -->
<!-- │ style:     🔧 ظاهر و چیدمان          ← مثال: style: بهبود فاصله دکمه‌ها         │ -->
<!-- │ refactor:  🔧 مرتب‌سازی کد           ← مثال: refactor: ساده‌سازی کیبورد         │ -->
<!-- │ perf:      🔧 سرعت و بهینه‌سازی      ← مثال: perf: بارگذاری سریع‌تر فونت        │ -->
<!-- │ chore:     ⚙️ کار فنی (نمایش داده نمی‌شود)                                     │ -->
<!-- │ build:     ⚙️ تنظیمات بیلد (نمایش داده نمی‌شود)                                │ -->
<!-- │ ci:        ⚙️ workflow (نمایش داده نمی‌شود)                                    │ -->
<!-- │ بدون پیشوند: 📌 سایر تغییرات                                                   │ -->
<!-- └──────────────────────────────────────────────────────────────────────────────┘ -->
<!--  -->
<!-- قالب کامل: نوع(محدوده): توضیح ← مثال: fix(keyboard): رفع نمایش اشتباه حرف U -->
<!-- پیشوند باید با حروف کوچک باشد و بلافاصله بعدش «:» بیاید. -->
<!--  -->
<!-- ────────────────────────── از اینجا به پایین را پر کنید ────────────────────────── -->
### تغییرات در نسخه جدید اپلیکیشن 
### ✨ ویژگی‌های جدید
- 📊 افزوده شدن ورود و خروجی فایل Excel (XLSX) و Word (DOCX) در فرهنگ واژگان؛ هم در «دیکشنری‌های من» و هم در «ذخیره / دریافت از حافظه» و اشتراک‌گذاری
- 🗂️ افزوده شدن منوی «ذخیره / دریافت از حافظه» با دو انتخاب ورود فایل و خروجی گرفتن از هر دیکشنری (JSON، SQLite، Excel، Word، CSV، PDF)
- 📝 افزوده شدن پذیرش جدول‌های ساخته‌شده توسط خود کاربر در Excel و Word (سرستون فارسی مثل «واژه | معنی»، یا حتی بدون سرستون، و فهرست «واژه = معنی» در Word)
- ✨ افزوه شدن دانلود ، ساخت و ارسال ایموجی متحرک در تالار عمومی و نظرات و ویرایشگر اصلی اپلیکیشن  همچنین ارسال به برنامه‌های دیگر
- 🎙️ افزوده شدن آیکون «موتور تبدیل صدا به متن» و «موتور گفتار» به بالای صفحهٔ اصلی، کیبورد اپلیکیشن و صفحهٔ تبدیل دبیره 
- 🎤 افزوده شدن «موتور تبدیل صدا به متن» به فرهنگ واژگان
- 🎲 افزوده شدن بازی واژگان و ده ها امکانات دیگر 
- 📋 افزودن شدن امکان اضافه کردن دست خط ویژه خودتان برای هر واژه
- 🗃️ افزودن شدن قابلیت دانلود و ارسال استیکر ثابت و متحرک 
- 🎲 افزوده شدن swipe type با تایپ کشیدنی
- 🌐 افزوده شدن زبان انگلیسی به اپلیکیشن 
- 🗣️ افزوده شدن آیتم «اپلیکیشن سخنگو» به منوی اصلی: توضیح کامل، وضعیت TalkBack، تنظیمات اعلام‌ها، خواندن هر کلید کیبورد با لمس و خواندن متن کادر اصلی
- 📜 افزوده شدن تور اولیه آموزشی برای اپلیکشین
- 🖍️ افزوده شدن دست کم ۵۰ قلم ۳ بعدی ثابت 
- 🗨️ افزوده شدن تالار عمومی برای چت و پروفایل شخصی
- 🕹️ امکان چت با هوش مصنوعی
- 🤖 امکان ترجمه بصورت آنلاین و تطابق نوشته با واقعیت مجازی
- 🖨️ افزودن شدن قابلیت تبدیل متن و qr code و برعکس 
- 🖨️ امکان چاپ سه بعدی و دو بعدی
- 🔦 افزوده شدن «برش و حکاکی لیزری» 
- 🖋️ افزوده شدن آیتم «سامانه قلم نوری» (Stylus / S-Pen) 
- افزوده شدن ✍️ نوشتن با دست‌خط در فرهنگ واژگان
- 🗃️ افزودن شدن قابلیت آپلود و دانلود آهنگ فایل یادگیری از و به مخزن اپلیکیشن برای زبان ها و دبیره های باستانی 
- 🧩 افزوده شدن آیتم «ویجت صفحه اصلی» به منوی اصلی
- 🧾 افزوده شدن تالار عمومی آفلاین برای چت بدون نیاز به من
- 📜 افزوده شدن تالار کتیبه ها VR به فرهنگ واژگان
- 🔁 افزوده شدن آیکون اپلیکیشن برای تغییر آیکون اپلیکشین
- 🔐 افزوده شدن سیستم امنیتی یا قفل بیومتریک برای قفل کردن اپلیکشین
- ✒️ افزوده شدن استودیو ساخت و ویرایش فونت برای فونت های شخصی و تجاری 
### 🐛 رفع باگ ها
- 🛠 رفع خطای بیلد و ستاره‌دار کردن واژه‌ها در واژگان کاربردی (ذخیره در پشتیبان هم می‌آید)
- 🔄 رفع چندین باگ در ناهمسانی حروف و اتصالات حروف در هام دبیره یا خط پهلوی کتابی
- 📚 رفع باگ در عدم همگام سازی قلم های سه بعدی ثابت در تنظیمات منو اصلی
### 🔧 بهبودها
- ✅ بهبود در ساختار اپلیکیشن و UX و فونت پیشفرض اپلیکیشن
- 🏆 بهبود در حالت minimize کتابخانه و امکان بزرگ نمایی کردن
- 👾 امکان اضافه شدن اضافه کردن واکنش یا ریکت متحرک و ثابت به پیام ها
- 🖨️ بهبود در کارکرد چاپ سه بعدی
- 💾 تنظیمات «سامانه قلم نوری» در پشتیبان‌گیری و بازیابی هم ذخیره می‌شود و پیام راهنمای آن به تور آموزشی اولیه (فارسی و English) افزوده شد 

## 🇬🇧 English
### ✨ New features
- ✨ Added downloading, creating, and sending animated emoji in the public forum, comments, and the app’s main editor, as well as sending to other apps
- 🎙️ Added the “Speech to text” and “Speech engine” icons to the top of the main screen, the app keyboard and the script converter 
- 🎤 Added the “Speech to text” engine to the dictionary
- 🎲 Added a word game and dozens of other features
- 📋 You can now add your own handwriting for every word
- 🗃️ Added the ability to download and send static and animated stickers
- 🎲 Added swipe typing to the app keyboard
- 🌐 Added English to the app: new “زبان / Language” item in the main menu; switching to English makes the whole app English and left-to-right
- 🗣️ Added the “Talking app” item to the main menu: full description, TalkBack status, announcement settings, reading every keyboard key on touch and reading the main text box
- 📜 Added an intro tour for the app (also available in English)
- 🖍️ Added at least 50 fixed 3D pens
- 🗨️ Added a public forum for chat and a personal profile
- 🕹️ AI chat
- 🤖 Online translation and matching text with augmented reality
- 🖨️ 3D and 2D printing
- 🔦 Added “Laser cutting and engraving” (next to 3D printing in the printing system) with G-code output for diode lasers
- 🖋️ Added the “Stylus system” (S-Pen) item to the main menu
- ✍️ Handwriting input in the Dictionary
- 🗃️ Upload and download learning audio files to and from the app repository for ancient languages and scripts
- 📠 Added text-to-QR-code conversion and vice versa
- 🧩 Added the “Home screen widget” item to the main menu
- 🧾 Added offline public hall to dictionary item , it works with WiFi direct or Bluetooth
- 📜 Added inscription hall (VR) to dictionary item
- 🔁 Added app icon to main menu, to change app icon
- 🔐 Added biometrics system for locking application
- ✒️ Added create & edit font studio to create and edit personal & businessal fonts
### 🐛 Bug fixes
- 🛠 Fixed a build error and starring words in Common Words (it is also included in backups)
- 🔄 Fixed several bugs in letter mismatches and joins in Ham-Dabireh / Book Pahlavi script
- 📚 Fixed fixed 3D pens not syncing in the main menu settings
### 🔧 Improvements
- ✅ Improved the app structure, UX and the default app font
- 🏆 Improved the library's minimize mode and added zoom
- 👾 Added the ability to add animated and static reactions to messages
- 🖨️ Improved 3D printing
- 💾 Stylus system settings are now included in backup and restore, and its guide message was added to the intro tour (Persian and English)
