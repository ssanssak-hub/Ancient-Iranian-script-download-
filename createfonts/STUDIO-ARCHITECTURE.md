# معماری «استودیو ساخت و ویرایش فونت» — مرجع برای ادامهٔ توسعه
(نسخهٔ ۱.۷.۰، versionCode=10. این فایل برای این است که بعداً بدون فرستادن فایل‌های اپ بشود کار را ادامه داد. اگر ساختار عوض شد، این فایل را هم به‌روز کنید.)

## ۱) تصویر کلی
- استودیو یک وب‌اپ HTML/JS خالص است که داخل WebView اپ (applicationId: `irani.script.keyboards`) از آدرس `https://appassets.androidplatform.net/studio/web/index.html` اجرا می‌شود.
- اپ فقط «پل» (`FontStudioBridge` ← `window.FontStudioHost` از `/__host/host.js`) می‌دهد: انتخاب فایل، ذخیره، اشتراک، فونت‌های اپ، فضای کار، کلیپ‌بورد، دکمهٔ برگشت و … . همهٔ موتور فونت JS است.
- کاربر بستهٔ استودیو را از پوشهٔ `createfonts` مخزن دانلود می‌کند: `font-studio.zip` + `fontstudio.meta.json` (+ README.txt و همین فایل که اپ نمی‌خواند).
- **قانون طلایی:** `minAppVersionCode=1` و `hostApi=1` بماند و فقط JS/WASM اضافه شود؛ آن‌وقت هر ارتقا فقط عوض‌کردن دو فایل است (`tools/fontstudio-test/policy.json` همین را اجبار می‌کند).

## ۲) محتویات بسته (`font-studio.zip`)
`manifest.json` + `web/` شامل: `index.html`، `style.css` و `js/` با این ترتیب بارگذاری (ترتیب مهم است):
`/__host/host.js` ← macnames ← sfnt ← cff ← export ← editor ← svgimport ← layout ← trace ← app ← app2 ← advanced ← pro ← ultra ← ultra2.

| فایل | نقش |
|---|---|
| `macnames.js` | نام‌های استاندارد Mac گلیف (`FS.MAC_NAMES`) |
| `sfnt.js` | خواندن/نوشتن TTF/OTF/WOFF1/TTC: `FS.sfnt.loadFont(buf)` ← مدل فونت، `buildFont(font)` ← بایت‌ها |
| `cff.js` | خواندن CFF و تبدیل به درجه‌دو (`FS.cff`) |
| `export.js` | WOFF/WOFF2/EOT/SVG/ZIP، بستهٔ وب و اندروید، پروژه (`FS.io`) و هندسهٔ پایه (`FS.geom.explicit/normalized/pathD`) |
| `editor.js` | ویرایشگر بوم گلیف، `FS.editor` (`snap/restore/normalizeGlyph/addExtrema/signedArea`) |
| `svgimport.js` / `trace.js` | ورود SVG / ردیابی تصویر |
| `layout.js` | GSUB/GPOS: `FS.layout.open(font)`، `addLookup`، `addFeature`، `commit`، kerning، `suggestJoining` |
| `app.js` | هستهٔ UI: وضعیت `S`، تب‌ها، تاریخچه، نام‌ها، متریک، اعتبارسنجی، `window.StudioApp` |
| `app2.js` | کرنینگ، ویژگی‌های OpenType، ردیابی تصویر (UI) |
| `advanced.js` | Font Pro Lab: Preflight، پیش‌نمایش زنده، نقشهٔ پوشش |
| `pro.js` | Auto joining، Smart Kerning، Component، Batch، Mark، Variable Lab (قدیمی) |
| `ultra.js` (۱.۶.۰) | وزن/Offset، پاک‌سازی نقاط، فاصله‌گذاری، متریک عمودی، نگاشت فارسی/عربی، Mark-to-Base/Mark، نام‌گذاری |
| `ultra2.js` (۱.۷.۰) | حذف همپوشانی، ناحیه‌های هم‌ترازی/اُورشوت |

## ۳) مدل داده
- `S` (در `StudioApp.S` و `StudioDebug.S`): `font, name, meta, hist, redo, tab, dirty, ttf, origBytes, page, q, filter, ed, testGen`؛ `S.gi` اندیس گلیف فعلی.
- فونت: `font.upm`، `font.glyphs[]`، `font.hhea{asc,desc,gap}`، `font.os2{typoAsc,typoDesc,typoGap,winAsc,winDesc,useTypo,xHeight,capHeight,weight…}`، `font.post{italicAngle…}`، `font.names[]`، `font.extra` (جدول‌های نگه‌داشته‌شده مثل fvar).
- گلیف: `{name, adv, unicodes:[], contours:[[{x,y,on}]]}`. **همهٔ طرح‌ها درجه‌دو (TrueType-style)**: نقطهٔ `on:false` نقطهٔ کنترل است و بین دو off-curve پشت‌سرهم یک on-curve ضمنی هست (`FS.geom.normalized` آن را صریح می‌کند). CFF هنگام خواندن به درجه‌دو تبدیل می‌شود. جهت: بیرونی ساعت‌گرد، حفره پادساعت‌گرد؛ قاعدهٔ پر شدن nonzero.
- GSUB/GPOS به‌صورت بایت خام نگه‌داری می‌شوند و فقط lookup‌های ویرایش‌شده/تازه بازنویسی می‌شوند؛ ارجاع‌ها **با اندیس گلیف** است. پس حذف/جابه‌جایی گلیف‌ها (مثل subset) بدون بازنویسی lookupها ممکن نیست؛ نام گلیف عوض‌کردن بی‌خطر است.

## ۴) `window.StudioApp` (API ابزارها)
`S, T(fa,en), $, toast, busy(msg)→Promise, modal(html,bind), closeModal, ask, fail(e), esc, hex, go(tab), pushHistory(items), changed(gi,structural), Host, caps, fam(), fixDirections(g), flushLayout, fa`.
- **الگوی تغییر گلیف با Undo:** `before=FS.editor.snap(g)` ← تغییر ← `after=snap(g)` ← `A.pushHistory([{gi,before,after}])` ← `S.ttf=null; S.dirty=true; Host.setUnsaved(true); A.changed(gi,true)`. نمونهٔ کامل: `runOn/touch` در `ultra.js` و `runBatch/touch` در `ultra2.js`.
- حتماً بعد از `FS.editor.normalizeGlyph(g)` مختصات صحیح می‌شوند.
- افزودن پنل به تب «ابزارها»: `var old=A.afterTools; A.afterTools=function(m){ if(old) old(m); /* افزودن <details> به m */ };`
- متن‌ها دوزبانه با `T('فارسی','English')`. رابط تمام‌صفحه مثل `fs-lab ul-lab` و کارت‌ها `card ul-card` (CSS در `style.css`).

## ۵) افزودن یک ابزار تازه (روال)
1. فایل `web/js/xxx.js` بنویسید (IIFE، `var A=window.StudioApp`)؛ توابع محض را قبل از `if(!A) return` روی `root.StudioXxx` بگذارید تا بیرون از UI تست‌پذیر باشند.
2. `<script src="js/xxx.js">` را در انتهای `index.html` (بعد از `ultra2.js`) اضافه کنید.
3. هیچ‌چیز بیرونی نخواهید: بدون `eval`، بدون `onclick="…"` درون‌خطی، بدون اسکریپت inline، بدون درخواست اینترنتی/CDN. WASM مجاز است. فایل‌های بزرگ‌تر از ۱۲۰MB در نصب‌کننده رد می‌شوند.
4. فقط «اضافه کردن» به پل مجاز است؛ هر `Host.xxx` که استفاده می‌کنید باید در `host.js` اپ باشد (تست ۳۸ بررسی می‌کند).
5. نسخه را بالا ببرید و بسازید (بخش ۶)، تست کنید (بخش ۷).

## ۶) ساخت بسته
```
java tools/FontStudioPackager.java pack <پوشهٔ web> createfonts/font-studio.zip \
  --version-code N --version-name X.Y.Z --min-app 1 --host-api 1 \
  --notes-file notes-fa.txt --notes-en-file notes-en.txt --released YYYY-MM-DD
```
zip و meta را **با هم** در `createfonts` بگذارید؛ دستی ویرایششان نکنید (SHA-256 فایل‌ها داخل manifest است). `meta.version == manifest.versionCode` باید باشد. بسته بدون امضاست (`font_studio_pubkey` خالی)؛ با کلید: `--key`.
قبل از انتشار `README.txt` و `CHANGES.md` را هم به‌روز کنید.

## ۷) تست
- شبیه‌ساز نصب اپ: `python tools/fontstudio-test/app_sim.py createfonts/fontstudio.meta.json createfonts/font-studio.zip`.
- کامل: `python tools/fontstudio-test/preflight.py createfonts --previous-version <کد قبلی>` (نیاز: playwright+chromium، fonttools، و در مخزن شما `FontStudioPathHandler.kt` برای CSP و فونت `assets/fonts/irani_dAbirI.ttf`).
- تست رابط: `node tools/fontstudio-test/e2e.js --pkg <پوشهٔ باز‌شدهٔ zip> --out out --bigfont <ttf> --csp <فایل CSP، بدون خط‌جدید انتهایی> --shim <host.js استخراج‌شده از FontStudioShim.kt> --features <فهرست FEATURES>`. مراحل ۲۷ و ۲۹ تعداد ثابت ۱۱۰۳۷ گلیف فونت `irani_dAbirI.ttf` را انتظار دارند؛ با فونت دیگر عمداً رد می‌شوند.
- تست الگوریتم‌ها بدون اپ: صفحهٔ خالی Chromium با `macnames,sfnt,cff,export,editor,<ابزار>` + `Path2D.fill('nonzero')` برای مقایسهٔ پیکسلی (روش تست حذف همپوشانی). `FS.sfnt.loadFont` روی فونت‌های سیستم کار می‌کند.

## ۸) اپ (Kotlin) — فقط وقتی لازم است
مسیر: `app/PersianFontKeyboard/app/src/main/java/com/example/persianfontkeyboard/fontstudio/`
`FontStudioBridge.kt` (پل؛ `API_VERSION`، `FEATURES` که فقط زیاد می‌شود)، `FontStudioShim.kt` (host.js)، `FontStudioStore.kt` (نگه‌داری نسخه + نسخهٔ قبلی)، `FontStudioInstaller.kt` (نصب/راستی‌آزمایی SHA)، `FontStudioRemote.kt` (بررسی meta)، `FontStudioHubActivity.kt` (صفحهٔ مدیریت و بازگشت)، `FontStudioPathHandler.kt` (سرو فایل و CSP). مستند پل: `docs/FONT_STUDIO_HOST_API.md`، معماری: `GUIDE-fa.md`.
Kotlin در محیط من هرگز کامپایل نشده؛ بعد از تغییر اپ یک بیلد بگیرید.

## ۹) نکته‌های تجربه‌شده
- در `index.html` ترتیب اسکریپت‌ها مهم است؛ ابزار جدید آخر بیاید.
- هدر CSP نباید خط‌جدید داشته باشد (وگرنه ناوبری ERR_ABORTED می‌شود).
- پس از `snap/restore` Undo فقط `contours/adv/unicodes/name` را برمی‌گرداند؛ تغییر جداول دیگر (hhea/os2/GPOS) با Undo برنمی‌گردد.
- حذف همپوشانی با تلورانس‌های `VTOL/ETOL=0.3` و `DELTA=0.03` تنظیم شده و برای برخوردهای تقریباً مماس پل‌زدن شکاف دارد؛ نتیجه همیشه راستی‌آزمایی می‌شود. تغییر این اعداد را حتماً با تست تصادفی دوباره بسنجید.
- Kerning/GPOS کلاس‌دار فقط خوانده می‌شود؛ ویرایش فقط روی جفت‌های ساده است.

## ۱۰) ایده‌های بعدی (هنوز ساخته نشده)
Subset (نیازمند بازنویسی اندیس‌ها در GSUB/GPOS)، تولید سبک Italic/Oblique دسته‌ای، Variable instance، کلاس‌بندی Kerning، تولید حروف از اسکلت+نقطه برای فارسی، auto-hinting/gasp.
