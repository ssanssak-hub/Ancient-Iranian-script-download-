استودیو ساخت و ویرایش فونت — نسخه 1.5.0 (کد نسخه 8)

این پوشه (createfonts) را اپلیکیشن برای دانلود استودیو می‌خواند:
- font-studio.zip       : بستهٔ استودیو (manifest.json + web/)
- fontstudio.meta.json  : اطلاعات نسخه (version = عدد صحیح = versionCode مانیفست)

امکانات: Font Pro Lab، Preflight و گزارش JSON سلامت فونت، Preview زنده، نقشهٔ پوشش یونیکد عربی/فارسی،
اتصال خودکار حروف، Smart Kerning، GPOS mark-to-base، Component Glyph، Batch Glyph Generator،
مقایسهٔ قبل/بعد، بازرس محورهای Variable Font.

نکته برای انتشار: فایل‌های زیپ و meta را دستی ویرایش نکنید (هش‌ها نامعتبر می‌شود). همیشه با
PersianFontKeyboard/tools/FontStudioPackager.java بسازید و هر دو فایل را با هم در این پوشه بگذارید.
در اسکریپت‌ها و HTML بسته، از event handler درون‌خطی (onclick="…") استفاده نکنید؛ CSP اپ آن را مسدود می‌کند.
بررسی سلامت، ابزار تشخیصی است و جایگزین تست نهایی فونت روی سیستم‌عامل‌ها و مرورگرهای هدف نیست.
