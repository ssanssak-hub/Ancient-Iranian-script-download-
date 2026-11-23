#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ساخت خودکار فهرست و نسخهٔ آیکون‌ها  →  iconapp/icons-manifest.json

اپلیکیشن «دبیر ایرانی» همین فایل را از آدرس زیر می‌خواند:
  https://raw.githubusercontent.com/ssanssak-hub/Ancient-Iranian-script-download-/main/iconapp/icons-manifest.json

قواعد نسخه:
  • آیکون جدید            → version = 1
  • محتوای آیکونِ هم‌نام عوض شد (حتی با پسوند دیگر، مثلاً gold.jpg ← gold.png) → version + 1
  • بدون تغییر            → همان نسخه
  • آیکونِ حذف‌شده‌ای که دوباره اضافه شود از نسخهٔ قبلی‌اش ادامه می‌دهد (نسخه هرگز عقب نمی‌رود)
  • فایل zip ← یک «بسته» است؛ نسخهٔ بسته و نسخهٔ تک‌تک آیکون‌های داخلش جدا نگه داشته می‌شود

نام یکتای آیکون (id) = نام فایل بدون پسوند، با حروف کوچک؛ هر نویسهٔ غیر از حرف/عدد/-/_ ← «_»
(دقیقاً همان قاعده‌ای که اپلیکیشن در IconStore.safeId دارد.)

اطلاعات اختیاری (نام فارسی/انگلیسی، دسته، توضیح، سازنده) را می‌توانید در  iconapp/icons-info.json بنویسید:
  { "gold": { "title": "طلایی", "title_en": "Gold", "category": "ساده", "author": "..." } }

اجرا (دستی):   python3 build_icons_manifest.py [پوشهٔ iconapp] [--out فایل]
در GitHub Actions با workflow همراهش خودکار اجرا می‌شود.
"""
import hashlib
import io
import json
import os
import sys
import zipfile
from datetime import datetime, timezone

IMAGE_EXT = {"png", "jpg", "jpeg", "jpe", "jfif", "webp", "gif", "bmp", "ico", "heic", "heif", "avif", "svg", "svgz"}
# اگر دو فایل هم‌نام (با پسوندهای مختلف) بود، این ترتیب برنده را تعیین می‌کند
EXT_PRIORITY = ["png", "webp", "svg", "svgz", "avif", "heic", "heif", "jpg", "jpeg", "jpe", "jfif", "gif", "bmp", "ico"]
MANIFEST_NAME = "icons-manifest.json"
INFO_NAME = "icons-info.json"
MAX_ENTRIES = 600
MAX_ENTRY_BYTES = 30 * 1024 * 1024
MAX_TOTAL_BYTES = 200 * 1024 * 1024
INFO_KEYS = ("title", "title_en", "category", "category_en", "description", "description_en", "author")


def ext_of(name):
    base = os.path.basename(name)
    i = base.rfind(".")
    return base[i + 1:].lower() if i > 0 else ""


def safe_id(name):
    n = os.path.basename(name.replace("\\", "/"))
    dot = n.rfind(".")
    if dot > 0:
        n = n[:dot]
    s = "".join(c if (c.isalnum() or c in "-_") else "_" for c in n.strip())
    s = s.strip("_")
    return (s or "icon")[:60].lower()


def unique(base, used):
    if base not in used:
        used.add(base)
        return base
    n = 2
    while "%s_%d" % (base, n) in used:
        n += 1
    out = "%s_%d" % (base, n)
    used.add(out)
    return out


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def zip_members(data, depth=0):
    """[(entry_path, bytes)] برای همهٔ تصویرهای داخل zip (zip تودرتو تا دو سطح)؛ همان قواعد اپلیکیشن."""
    out, total, count = [], 0, 0
    with zipfile.ZipFile(io.BytesIO(data)) as z:
        for info in z.infolist():
            count += 1
            if count > MAX_ENTRIES:
                break
            if info.is_dir():
                continue
            name = info.filename.replace("\\", "/")
            base = name.rsplit("/", 1)[-1]
            if name.startswith("__MACOSX/") or base.startswith("."):
                continue
            ext = ext_of(base)
            if ext not in IMAGE_EXT and not (ext == "zip" and depth < 2):
                continue
            if info.file_size > MAX_ENTRY_BYTES:
                continue
            buf = z.read(info)
            total += len(buf)
            if total > MAX_TOTAL_BYTES:
                break
            if ext == "zip":
                try:
                    out.extend(zip_members(buf, depth + 1))
                except zipfile.BadZipFile:
                    pass
            else:
                out.append((name, buf))
    return out


def load_json(path, default):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (OSError, ValueError):
        return default


def bump(prev, retired, key, digest):
    """prev = {'sha256':..,'version':..} یا None"""
    if prev:
        return prev["version"] if prev.get("sha256") == digest else prev["version"] + 1
    return retired.get(key, 0) + 1


def build(root, out_path):
    root = os.path.abspath(root)
    if not os.path.isdir(root):
        print("پوشه پیدا نشد:", root)
        return 1
    old = load_json(out_path, {})
    info = load_json(os.path.join(root, INFO_NAME), {})
    if not isinstance(info, dict):
        info = {}

    prev_icons = {i["id"]: i for i in old.get("icons", []) if isinstance(i, dict) and "id" in i}
    prev_packs = {p["id"]: p for p in old.get("packs", []) if isinstance(p, dict) and "id" in p}
    retired = dict(old.get("retired", {})) if isinstance(old.get("retired"), dict) else {}

    loose, zips = {}, []
    for dp, dn, fn in os.walk(root):
        dn[:] = sorted(d for d in dn if not d.startswith("."))
        for f in sorted(fn):
            if f.startswith(".") or f in (MANIFEST_NAME, INFO_NAME):
                continue
            full = os.path.join(dp, f)
            rel = os.path.relpath(full, root).replace(os.sep, "/")
            ext = ext_of(f)
            if ext in IMAGE_EXT:
                iid = safe_id(f)
                cur = loose.get(iid)
                if cur is None or EXT_PRIORITY.index(ext) < EXT_PRIORITY.index(ext_of(cur)):
                    if cur is not None:
                        print("هشدار: دو فایل هم‌نام «%s» و «%s»؛ فایل «%s» استفاده شد." % (cur, rel, rel))
                    loose[iid] = rel
                else:
                    print("هشدار: «%s» نادیده گرفته شد (هم‌نام با «%s»)." % (rel, cur))
            elif ext == "zip":
                zips.append(rel)

    icons, packs = [], []
    seen_keys = set()

    for iid in sorted(loose):
        rel = loose[iid]
        with open(os.path.join(root, rel), "rb") as fh:
            data = fh.read()
        digest = sha256(data)
        key = "icon:" + iid
        seen_keys.add(key)
        entry = {
            "id": iid,
            "file": rel,
            "version": bump(prev_icons.get(iid), retired, key, digest),
            "sha256": digest,
            "size": len(data),
        }
        meta = info.get(iid) if isinstance(info.get(iid), dict) else {}
        entry["title"] = str(meta.get("title") or iid.replace("_", " "))
        for k in INFO_KEYS:
            if k != "title" and meta.get(k):
                entry[k] = str(meta[k])
        icons.append(entry)

    used_packs = set()
    for rel in sorted(zips):
        with open(os.path.join(root, rel), "rb") as fh:
            data = fh.read()
        pid = unique(safe_id(rel), used_packs)
        digest = sha256(data)
        key = "pack:" + pid
        seen_keys.add(key)
        prev_p = prev_packs.get(pid)
        prev_members = {m["id"]: m for m in (prev_p or {}).get("icons", []) if isinstance(m, dict) and "id" in m}
        try:
            members_raw = zip_members(data)
        except zipfile.BadZipFile:
            print("هشدار: «%s» zip معتبر نیست؛ نادیده گرفته شد." % rel)
            continue
        used_ids, members = set(), []
        for name, buf in members_raw:
            mid = unique(safe_id(name), used_ids)
            mkey = "member:%s:%s" % (pid, mid)
            seen_keys.add(mkey)
            mdigest = sha256(buf)
            m = {
                "id": mid,
                "entry": name,
                "version": bump(prev_members.get(mid), retired, mkey, mdigest),
                "sha256": mdigest,
            }
            meta = info.get(mid) if isinstance(info.get(mid), dict) else {}
            if meta.get("title"):
                m["title"] = str(meta["title"])
            if meta.get("title_en"):
                m["title_en"] = str(meta["title_en"])
            members.append(m)
        pack = {
            "id": pid,
            "file": rel,
            "version": bump(prev_p, retired, key, digest),
            "sha256": digest,
            "size": len(data),
            "icons": sorted(members, key=lambda x: x["id"]),
        }
        meta = info.get(pid) if isinstance(info.get(pid), dict) else {}
        pack["title"] = str(meta.get("title") or pid.replace("_", " "))
        if meta.get("title_en"):
            pack["title_en"] = str(meta["title_en"])
        packs.append(pack)

    # نسخهٔ آیکون‌های حذف‌شده را نگه می‌داریم تا اگر دوباره آمدند نسخه عقب نرود
    for i in old.get("icons", []):
        k = "icon:" + i.get("id", "")
        if k not in seen_keys:
            retired[k] = max(retired.get(k, 0), i.get("version", 0))
    for p in old.get("packs", []):
        k = "pack:" + p.get("id", "")
        if k not in seen_keys:
            retired[k] = max(retired.get(k, 0), p.get("version", 0))
        for m in p.get("icons", []):
            mk = "member:%s:%s" % (p.get("id", ""), m.get("id", ""))
            if mk not in seen_keys:
                retired[mk] = max(retired.get(mk, 0), m.get("version", 0))
    for k in list(retired):
        if k in seen_keys:
            del retired[k]

    new = {
        "schema": 1,
        "base": os.path.basename(root),
        "icons": icons,
        "packs": packs,
        "retired": dict(sorted(retired.items())),
    }
    old_cmp = {k: v for k, v in old.items() if k not in ("generated_at", "revision")}
    if old and old_cmp == new:
        print("بدون تغییر: %d آیکون، %d بسته" % (len(icons), len(packs)))
        return 0

    new["revision"] = int(old.get("revision", 0)) + 1
    new["generated_at"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    text = json.dumps(new, ensure_ascii=False, indent=2, sort_keys=False) + "\n"
    tmp = out_path + ".tmp"
    with open(tmp, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)
    os.replace(tmp, out_path)
    print("نوشته شد: %s  (%d آیکون، %d بسته، revision %d)" % (out_path, len(icons), len(packs), new["revision"]))
    return 0


def main(argv):
    root, out = None, None
    i = 1
    while i < len(argv):
        if argv[i] == "--out" and i + 1 < len(argv):
            out = argv[i + 1]
            i += 2
        else:
            root = argv[i]
            i += 1
    if root is None:
        here = os.path.dirname(os.path.abspath(__file__))
        root = here if os.path.basename(here) == "iconapp" else "iconapp"
    if out is None:
        out = os.path.join(root, MANIFEST_NAME)
    return build(root, out)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
