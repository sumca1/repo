#!/usr/bin/env python3
"""
מאחד את חלקי model_final.pth לקובץ אחד
"""

from pathlib import Path


def merge_parts():
    """מאחד את החלקים"""
    print("=" * 60)
    print("🔧 מאחד חלקי המודל")
    print("=" * 60)
    
    # מצא חלקים
    parts = sorted(Path('.').glob('model_final.pth.part*'))
    
    if not parts:
        print("\n❌ לא נמצאו חלקים!")
        print("חפש קבצים: model_final.pth.part0, model_final.pth.part1, ...")
        return False
    
    print(f"\n📦 נמצאו {len(parts)} חלקים:")
    total_size = 0
    for part in parts:
        size = part.stat().st_size / 1024 / 1024
        total_size += size
        print(f"   • {part.name} ({size:.1f} MB)")
    
    print(f"\n📊 גודל כולל: {total_size:.1f} MB")
    
    # איחוד
    output = Path('model_final.pth')
    
    if output.exists():
        print(f"\n⚠️  {output.name} כבר קיים")
        overwrite = input("האם לדרוס? (y/n): ").strip().lower()
        if overwrite != 'y':
            print("❌ בוטל")
            return False
    
    print(f"\n🔧 מאחד ל-{output.name}...")
    
    with open(output, 'wb') as outfile:
        for i, part in enumerate(parts):
            print(f"   ⚙️  מעבד חלק {i+1}/{len(parts)}: {part.name}")
            with open(part, 'rb') as infile:
                outfile.write(infile.read())
    
    final_size = output.stat().st_size / 1024 / 1024
    
    print(f"\n✅ הצלחה!")
    print(f"📄 נוצר: {output.name} ({final_size:.1f} MB)")
    
    # שאל האם למחוק חלקים
    print("\n🗑️  האם למחוק את החלקים? (שמור מקום)")
    delete = input("(y/n): ").strip().lower()
    
    if delete == 'y':
        for part in parts:
            part.unlink()
            print(f"   🗑️  נמחק: {part.name}")
        print("✅ החלקים נמחקו")
    
    return True


if __name__ == '__main__':
    print("\n" + "=" * 60)
    print("🎯 LayoutParser Model Merger")
    print("=" * 60)
    
    success = merge_parts()
    
    if success:
        print("\n" + "=" * 60)
        print("🚀 המודל מוכן לשימוש!")
        print("=" * 60)
        print("""
עכשיו תוכל להשתמש ב:

    import layoutparser as lp
    
    model = lp.Detectron2LayoutModel(
        config_path='config.yml',
        model_path='model_final.pth',
        label_map={
            0: "Text", 
            1: "Title", 
            2: "List", 
            3: "Table", 
            4: "Figure"
        }
    )
""")
