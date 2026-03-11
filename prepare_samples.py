#!/usr/bin/env python3
"""Prepare sample images and JSON data for the GRADE project page."""

import json
import os
import shutil

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SAMPLES_DIR = os.path.join(BASE_DIR, "static", "images", "samples")
DATA_DIR = os.path.join(BASE_DIR, "data")
os.makedirs(SAMPLES_DIR, exist_ok=True)
os.makedirs(DATA_DIR, exist_ok=True)

# Data source
RESULT_JSON = "/mnt/nas-new/home/yangxue/lmx/image/json_data/v1/subset/bagel/result.json"

# Consistency display mapping
CONSISTENCY_MAP = {
    "overall": "Localized",
    "style": "Style",
    "none": "Independence",
}

# Selected samples: (task_id, discipline, display_taxonomy)
# One sample per sub_task (taxonomy), picked from result.json
SAMPLES = [
    # Mathematics (sub_task -> display name)
    ("math_math_3",      "Mathematics", "2D Geometry"),
    ("math_math_69",     "Mathematics", "3D Geometry"),
    ("math_math_99",     "Mathematics", "Functions"),
    ("math_static_5",    "Mathematics", "Statistics"),
    ("math_math_122",    "Mathematics", "Graph Theory"),
    # Physics
    ("physics_task_56",  "Physics", "Mechanics"),
    ("physics_task_14",  "Physics", "Optics"),
    ("physics_task_33",  "Physics", "Electromagnetism"),
    ("physics_task_45",  "Physics", "Thermodynamics"),
    ("engineering_task_7","Physics", "Engineering Drawing"),
    # Chemistry
    ("chemistry_task_8",  "Chemistry", "Atomic Periodic"),
    ("chemistry_task_4",  "Chemistry", "Inorganic Lab"),
    ("chemistry_task_64", "Chemistry", "Organic Structure"),
    ("chemistry_task_66", "Chemistry", "Organic Mechanism"),
    ("chemistry_task_24", "Chemistry", "Physical Chemistry"),
    ("chemistry_task_87", "Chemistry", "Organic Redox"),
    ("chemistry_task_2",  "Chemistry", "Organic Acid"),
    # Biology
    ("biology_task_22",  "Biology", "Ecology"),
    ("biology_task_34",  "Biology", "Cell Biology"),
    ("biology_task_18",  "Biology", "Human Physiology"),
    ("biology_task_38",  "Biology", "Molecular Biology"),
    # Computer Science
    ("ComputerScience_task_2",  "Computer Science", "Linear Structures"),
    ("ComputerScience_task_1",  "Computer Science", "Graph Algorithms"),
    ("ComputerScience_task_35", "Computer Science", "Tree Structures"),
    ("ComputerScience_task_15", "Computer Science", "AI & Computer Vision"),
    ("ComputerScience_task_32", "Computer Science", "Operating Systems"),
    ("ComputerScience_task_33", "Computer Science", "Architecture & Compilers"),
    # Economics
    ("eco_task_50",  "Economics", "Consumer Choice"),
    ("eco_task_42",  "Economics", "Macro"),
    ("eco_task_56",  "Economics", "Labor"),
    ("eco_task_100", "Economics", "Public Economics"),
    ("eco_task_130", "Economics", "Finance"),
    ("eco_task_146", "Economics", "Market Power & IO"),
    # History
    ("his_task_1",  "History", "Administrative Labeling"),
    ("his_task_6",  "History", "Route Mapping"),
    ("his_task_9",  "History", "Timeline Alignment"),
    # Geography
    ("geography_task_33", "Geography", "Earth Geometry"),
    ("geography_task_37", "Geography", "Ocean & Hydrology"),
    ("geography_task_4",  "Geography", "Atmosphere & Climate"),
    ("geography_task_27", "Geography", "Lithosphere & Pedosphere"),
    # Music
    ("music_task_4",  "Music", "Pitch & Transposition"),
    ("music_task_10", "Music", "Performance Markings"),
    ("music_task_21", "Music", "Rhythm & Meter"),
    ("music_task_45", "Music", "Harmony & Theory"),
    # Sports
    ("sports_task_4",       "Sports", "Sports Anatomy"),
    ("sports_task_16",      "Sports", "Sports Tactic"),
    ("sports_task_27",      "Sports", "Sports Nutrition"),
    ("board_games_task_4",  "Sports", "Board (Chess)"),
    ("board_games_task_6",  "Sports", "Board (Go)"),
    ("board_games_task_13", "Sports", "Board (Chinese Chess)"),
]

# Discipline order and icons
DISCIPLINE_META = {
    "Mathematics": {"icon": "📐", "order": 0},
    "Physics": {"icon": "⚡", "order": 1},
    "Chemistry": {"icon": "🧪", "order": 2},
    "Biology": {"icon": "🧬", "order": 3},
    "Computer Science": {"icon": "💻", "order": 4},
    "Economics": {"icon": "📊", "order": 5},
    "History": {"icon": "📜", "order": 6},
    "Geography": {"icon": "🌍", "order": 7},
    "Music": {"icon": "🎵", "order": 8},
    "Sports": {"icon": "⚽", "order": 9},
}


def copy_image(src_path, task_id, suffix):
    """Copy image to samples dir. Returns relative path from static/images/."""
    ext = os.path.splitext(src_path)[1]
    dst_name = f"{task_id}_{suffix}{ext}"
    dst_path = os.path.join(SAMPLES_DIR, dst_name)
    shutil.copy2(src_path, dst_path)
    return f"samples/{dst_name}"


def main():
    # Load data source
    with open(RESULT_JSON) as f:
        data = json.load(f)

    # Index by task_id
    task_map = {d["task_id"]: d for d in data}

    # Clear old samples
    if os.path.exists(SAMPLES_DIR):
        shutil.rmtree(SAMPLES_DIR)
    os.makedirs(SAMPLES_DIR, exist_ok=True)

    # Build output structure
    output = {}

    for task_id, discipline, display_taxonomy in SAMPLES:
        if task_id not in task_map:
            print(f"WARNING: task_id '{task_id}' not found in result.json, skipping!")
            continue

        item = task_map[task_id]
        input_rel = copy_image(item["image_path"], task_id, "input")
        gt_rel = copy_image(item["gt"], task_id, "gt")

        if discipline not in output:
            output[discipline] = {
                "display_name": discipline,
                "icon": DISCIPLINE_META[discipline]["icon"],
                "order": DISCIPLINE_META[discipline]["order"],
                "taxonomies": {},
            }

        output[discipline]["taxonomies"][display_taxonomy] = {
            "task_id": task_id,
            "text": item["text"],
            "input_img": input_rel,
            "gt_img": gt_rel,
            "consistency": CONSISTENCY_MAP.get(item["consistency"], item["consistency"]),
            "questions": item["questions"],
        }

    # Write samples.json
    out_path = os.path.join(DATA_DIR, "samples.json")
    with open(out_path, "w") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    # Stats
    total_samples = sum(len(v["taxonomies"]) for v in output.values())
    img_count = len(os.listdir(SAMPLES_DIR))
    print(f"Generated {total_samples} samples across {len(output)} disciplines")
    print(f"Images: {img_count} files in {SAMPLES_DIR}")
    print(f"JSON saved to: {out_path}")


if __name__ == "__main__":
    main()
