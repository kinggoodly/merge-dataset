import os, glob, shutil, random

# === CONFIG ===

# 1. Folder mapping → class id
FOLDER_CLASS_MAP = {
    "your dataset name": 0,      
    "your dataset name": 1,       
    "your dataset name": 2,     
    "your dataset name": 3              
}

# 2. Root path
DATASET_ROOT = "your path"
TARGET_ROOT = "your path"

# 3. Target folders
IMG_ALL = os.path.join(TARGET_ROOT, "images/all")
LBL_ALL = os.path.join(TARGET_ROOT, "labels/all")
SPLITS = ["train", "valid", "test"]
RATIO = {"train": 0.8, "valid": 0.1, "test": 0.1}

# === CREATE DIRS ===
for split in SPLITS:
    os.makedirs(os.path.join(TARGET_ROOT, split, "images"), exist_ok=True)
    os.makedirs(os.path.join(TARGET_ROOT, split, "labels"), exist_ok=True)
os.makedirs(IMG_ALL, exist_ok=True)
os.makedirs(LBL_ALL, exist_ok=True)

# === STEP 1: Remap + Copy ===
print("🔁 Remapping and copying...")
for folder, class_id in FOLDER_CLASS_MAP.items():
    label_dir = os.path.join(DATASET_ROOT, folder, "labels")
    image_dir = os.path.join(DATASET_ROOT, folder, "images")

    if not os.path.exists(label_dir) or not os.path.exists(image_dir):
        print(f"❌ Skipping {folder}: images or labels not found")
        continue

    lbl_paths = glob.glob(os.path.join(label_dir, "*.txt"))
    img_paths = glob.glob(os.path.join(image_dir, "*.[jp][pn]g"))

    print(f"📂 {folder}: {len(img_paths)} images, {len(lbl_paths)} labels")

    for lbl_path in lbl_paths:
        new_lines = []
        with open(lbl_path, "r") as f:
            for line in f:
                parts = line.strip().split()
                parts[0] = str(class_id)
                new_lines.append(" ".join(parts))
        with open(lbl_path, "w") as f:
            f.write("\n".join(new_lines))

    for img in img_paths:
        shutil.copy(img, IMG_ALL)
    for lbl in lbl_paths:
        shutil.copy(lbl, LBL_ALL)

print("✅ Done remap and copy.")

# === STEP 2: Split ===
print("✂️ Splitting into train/val/test...")
img_exts = (".jpg", ".jpeg", ".png", ".JPG", ".PNG", ".JPEG")
all_imgs = [f for f in os.listdir(IMG_ALL) if f.endswith(img_exts)]
random.shuffle(all_imgs)
total = len(all_imgs)
offset = 0

for split in SPLITS:
    count = int(total * RATIO[split])
    split_files = all_imgs[offset:offset + count]
    offset += count

    for f in split_files:
        img_src = os.path.join(IMG_ALL, f)
        lbl_src = os.path.join(LBL_ALL, os.path.splitext(f)[0] + ".txt")

        img_dst = os.path.join(TARGET_ROOT, split, "images", f)
        lbl_dst = os.path.join(TARGET_ROOT, split, "labels", os.path.basename(lbl_src))

        shutil.copy(img_src, img_dst)
        if os.path.exists(lbl_src):
            shutil.copy(lbl_src, lbl_dst)
        else:
            print(f"⚠️ No label found for {f}, skipping label.")

    print(f"✅ {split} done: {len(split_files)} files")

print("🎉 All done!")

