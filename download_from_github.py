"""
מוריד מודלים מ-GitHub (sumca1/layoutparser-models) ומאחד אותם
"""

import urllib.request
from pathlib import Path


def download_and_merge():
    """
    מוריד חלקי המודל מ-GitHub ומאחד אותם
    """
    print("=" * 70)
    print("📥 מוריד מודלים מ-GitHub")
    print("=" * 70)
    
    # בסיס URL
    base_url = "https://raw.githubusercontent.com/sumca1/layoutparser-models/main"
    
    # קבצים להורדה
    files = {
        "config.yml": f"{base_url}/config.yml",
        "model_final.pth.part0": f"{base_url}/model_final.pth.part0",
        "model_final.pth.part1": f"{base_url}/model_final.pth.part1",
    }
    
    # תיקיית יעד
    dest_dir = Path("C:/layoutparser_models/github")
    dest_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"\n📁 תיקיית יעד: {dest_dir}\n")
    
    # הורד כל קובץ
    downloaded_parts = []
    
    for filename, url in files.items():
        dest_path = dest_dir / filename
        
        print(f"📦 מוריד: {filename}")
        print(f"   מ: {url}")
        
        try:
            urllib.request.urlretrieve(url, str(dest_path))
            file_size = dest_path.stat().st_size / 1024 / 1024
            print(f"   ✅ הורד ({file_size:.1f} MB)\n")
            
            if filename.startswith("model_final.pth.part"):
                downloaded_parts.append(dest_path)
        
        except Exception as e:
            print(f"   ❌ שגיאה: {e}\n")
            if "404" in str(e):
                print("   💡 ה-repo עדיין לא קיים או הקובץ חסר")
                print(f"      בדוק: https://github.com/sumca1/layoutparser-models\n")
            return False
    
    # איחוד חלקים
    if len(downloaded_parts) > 0:
        print("=" * 70)
        print("🔧 מאחד חלקים...")
        print("=" * 70)
        
        model_path = dest_dir / "model_final.pth"
        
        with open(model_path, 'wb') as outfile:
            for part_path in sorted(downloaded_parts):
                print(f"   ⚙️  מעבד: {part_path.name}")
                with open(part_path, 'rb') as infile:
                    outfile.write(infile.read())
        
        final_size = model_path.stat().st_size / 1024 / 1024
        print(f"\n   ✅ מאוחד: model_final.pth ({final_size:.1f} MB)")
        
        # נקה חלקים (אופציונלי)
        clean = input("\n🗑️  למחוק את החלקים? (y/n): ").strip().lower()
        if clean == 'y':
            for part_path in downloaded_parts:
                part_path.unlink()
                print(f"   🗑️  נמחק: {part_path.name}")
    
    print("\n" + "=" * 70)
    print("✅ הכל מוכן!")
    print("=" * 70)
    print(f"""
📂 הקבצים נמצאים ב:
   {dest_dir}

📄 קבצים:
   • config.yml
   • model_final.pth ({final_size:.1f} MB)

🚀 עכשיו תוכל להשתמש ב-LayoutParser:

   from api.region_classifier import RegionClassifier
   
   classifier = RegionClassifier()
   regions = classifier.classify_regions('image.jpg')
""")
    
    return True


def main():
    print("\n" + "=" * 70)
    print("🎯 LayoutParser Model Downloader")
    print("🐙 מקור: github.com/sumca1/layoutparser-models")
    print("=" * 70)
    
    # בדוק אם כבר קיים
    existing_model = Path("C:/layoutparser_models/github/model_final.pth")
    
    if existing_model.exists():
        print(f"\n⚠️  המודל כבר קיים: {existing_model}")
        overwrite = input("האם להוריד מחדש? (y/n): ").strip().lower()
        if overwrite != 'y':
            print("✅ משתמש במודל הקיים")
            return
    
    # הורד ואחד
    success = download_and_merge()
    
    if not success:
        print("\n" + "=" * 70)
        print("💡 הוראות ליצירת ה-repo:")
        print("=" * 70)
        print("""
1. צור repo חדש: https://github.com/new
   שם: layoutparser-models
   Public: ✓

2. הורד את המודל ממקום עם גישה (VPN/מחשב אחר):
   wget https://www.dropbox.com/s/dgy9c10wykk4lq4/model_final.pth?dl=1

3. פצל אותו:
   python split_model.py

4. העלה ל-GitHub:
   git clone https://github.com/sumca1/layoutparser-models.git
   cd layoutparser-models
   cp model_final.pth.part* .
   cp config.yml .
   git add .
   git commit -m "Add model files"
   git push

5. הרץ שוב סקריפט זה
""")


if __name__ == '__main__':
    main()
