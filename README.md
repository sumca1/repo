# repo
PubLayNet pretrained models for layout analysis - NetFree friendly mirror
# LayoutParser Models

מודלים מאומנים לזיהוי מבנה מסמכים (Layout Analysis) - **PubLayNet**

> 🎯 **Mirror של מודלי LayoutParser** - זמין למשתמשי NetFree (Dropbox חסום)

## 📦 מה כלול?

מודל **PubLayNet - Faster R-CNN R50 FPN 3x** מאומן על מאות אלפי מסמכים אקדמיים.

**מזהה אוטומטית:**
- 📄 **Text** - טקסט רגיל
- 📌 **Title** - כותרות
- 📊 **Table** - טבלאות
- 🖼️ **Figure** - תמונות וגרפים
- 📝 **List** - רשימות

**דיוק:** 90-95% | **גודל:** ~160MB | **פורמט:** PyTorch

---

## 🚀 הורדה מהירה (סקריפט מוכן)

**אופציה 1: הרץ סקריפט אוטומטי**

הורד את [download_from_github.py](https://raw.githubusercontent.com/sumca1/layoutparser-models/main/download_from_github.py) והרץ:

```bash
python download_from_github.py
```

הסקריפט יוריד, יאחד ויכין את המודל אוטומטית!

---

## 📥 הורדה ידנית (שלב אחר שלב)

### דרך 1: Python

```python
import urllib.request
from pathlib import Path

# בסיס URL
base = "https://raw.githubusercontent.com/sumca1/layoutparser-models/main"

# קבצים להורדה
files = {
    "config.yml": f"{base}/config.yml",
    "model_final.pth.part0": f"{base}/model_final.pth.part0",
    "model_final.pth.part1": f"{base}/model_final.pth.part1",
}

# תיקיית יעד
dest_dir = Path("layoutparser_models")
dest_dir.mkdir(exist_ok=True)

# הורד כל קובץ
for filename, url in files.items():
    print(f"📥 מוריד: {filename}")
    urllib.request.urlretrieve(url, str(dest_dir / filename))
    print(f"   ✅ הורד!")

# איחוד החלקים
print("\n🔧 מאחד חלקים...")
with open(dest_dir / "model_final.pth", 'wb') as outfile:
    for i in [0, 1]:
        part_file = dest_dir / f"model_final.pth.part{i}"
        with open(part_file, 'rb') as infile:
            outfile.write(infile.read())
        part_file.unlink()  # מחיקת חלק אחרי איחוד

print("✅ model_final.pth מוכן!")
```

### דרך 2: wget/curl (Linux/Mac)

```bash
# הורד חלקים
wget https://raw.githubusercontent.com/sumca1/layoutparser-models/main/model_final.pth.part0
wget https://raw.githubusercontent.com/sumca1/layoutparser-models/main/model_final.pth.part1
wget https://raw.githubusercontent.com/sumca1/layoutparser-models/main/config.yml

# איחוד
cat model_final.pth.part0 model_final.pth.part1 > model_final.pth

# ניקוי
rm model_final.pth.part*
```

### דרך 3: PowerShell (Windows)

```powershell
$base = "https://raw.githubusercontent.com/sumca1/layoutparser-models/main"

# הורד חלקים
Invoke-WebRequest "$base/model_final.pth.part0" -OutFile "model_final.pth.part0"
Invoke-WebRequest "$base/model_final.pth.part1" -OutFile "model_final.pth.part1"
Invoke-WebRequest "$base/config.yml" -OutFile "config.yml"

# איחוד
Get-Content model_final.pth.part0,model_final.pth.part1 -Encoding Byte -ReadCount 0 | Set-Content model_final.pth -Encoding Byte

# ניקוי
Remove-Item model_final.pth.part*
```

---

## 🔧 שימוש עם LayoutParser

אחרי ההורדה:

```python
import layoutparser as lp

# טען את המודל המקומי
model = lp.Detectron2LayoutModel(
    config_path='layoutparser_models/config.yml',
    model_path='layoutparser_models/model_final.pth',
    label_map={0: "Text", 1: "Title", 2: "List", 3: "Table", 4: "Figure"}
)

# זיהוי מבנה
import cv2
image = cv2.imread('document.jpg')
layout = model.detect(image)

# הדפס תוצאות
for block in layout:
    print(f"{block.type}: {block.coordinates}")
```

---

## 📁 מבנה Repository

```
layoutparser-models/
├── README.md                    # המדריך הזה
├── config.yml                   # קובץ תצורה (2KB)
├── model_final.pth.part0        # חלק 1 של המודל (95MB)
├── model_final.pth.part1        # חלק 2 של המודל (65MB)
├── download_from_github.py      # סקריפט הורדה אוטומטי
└── merge.py                     # סקריפט איחוד
```

**למה מפוצל?** GitHub מגביל קבצים ל-100MB. המודל המקורי 160MB, לכן פוצל ל-2 חלקים.

---

## 📊 פרטים טכניים

| מאפיין | ערך |
|--------|-----|
| **Architecture** | Faster R-CNN |
| **Backbone** | ResNet-50 + FPN |
| **Dataset** | PubLayNet (360K+ documents) |
| **Input** | RGB images (any size) |
| **Output** | Bounding boxes + labels |
| **mAP** | ~90-95% |
| **Framework** | Detectron2 (PyTorch) |

---

## 🔗 קישורים

- **LayoutParser Repository:** https://github.com/Layout-Parser/layout-parser
- **Paper:** [LayoutParser: A Unified Toolkit for Document Image Analysis](https://arxiv.org/abs/2103.15348)
- **Documentation:** https://layout-parser.readthedocs.io/
- **PubLayNet Dataset:** https://github.com/ibm-aur-nlp/PubLayNet

---

## 💡 שימושים נפוצים

✅ **OCR Pipeline** - זיהוי אזורים לפני OCR  
✅ **Document Understanding** - ניתוח מבנה מסמכים  
✅ **Table Extraction** - זיהוי טבלאות  
✅ **Academic Papers** - עיבוד מאמרים מדעיים  
✅ **Historical Documents** - דיגיטציה של ארכיונים  

---

## 🐛 פתרון בעיות

### הורדה נכשלת
```python
# בדוק חיבור
import urllib.request
try:
    urllib.request.urlopen("https://github.com", timeout=5)
    print("✅ חיבור תקין")
except:
    print("❌ בעיית חיבור - בדוק אינטרנט")
```

### המודל לא נטען
```python
# וודא שהקבצים קיימים
from pathlib import Path
model_file = Path("layoutparser_models/model_final.pth")
config_file = Path("layoutparser_models/config.yml")

if model_file.exists():
    print(f"✅ Model: {model_file.stat().st_size / 1024 / 1024:.1f} MB")
else:
    print("❌ Model חסר")

if config_file.exists():
    print(f"✅ Config: {config_file.stat().st_size} bytes")
else:
    print("❌ Config חסר")
```

### שגיאת זיכרון
```python
# הקטן רזולוציית תמונה
import cv2
image = cv2.imread('document.jpg')
scale = 0.5  # הקטן ל-50%
image = cv2.resize(image, None, fx=scale, fy=scale)
```

---

## 📜 רישיון

**Apache License 2.0** - כמו הפרויקט המקורי

זהו Mirror/Fork של [Layout-Parser](https://github.com/Layout-Parser/layout-parser) ליצירת גישה למשתמשי NetFree (המודלים המקוריים נמצאים ב-Dropbox החסום).

---

## 🙏 תודות

- **Layout-Parser Team** - על הפיתוח המקורי
- **Detectron2** - Facebook AI Research
- **PubLayNet** - IBM Research

---

## 📧 תמיכה

יש בעיה? פתח [Issue](https://github.com/sumca1/layoutparser-models/issues)

**עדכון אחרון:** נובמבר 2025
