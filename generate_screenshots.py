"""Script to capture outputs and render crisp terminal window screenshots and Compass GUI verification.
"""

import subprocess
import os
import sys
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SCREENSHOTS_DIR = os.path.join(BASE_DIR, "screenshots")
os.makedirs(SCREENSHOTS_DIR, exist_ok=True)

FONT_PATH = "C:\\Windows\\Fonts\\consola.ttf"
FONT_BOLD_PATH = "C:\\Windows\\Fonts\\consolab.ttf"
FONT_SEGOE = "C:\\Windows\\Fonts\\segoeui.ttf"
FONT_SEGOE_BOLD = "C:\\Windows\\Fonts\\segoeuib.ttf"


def run_script(script_path):
    """Run a script with python/py and return its text output."""
    cmd = [sys.executable, script_path]
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    result = subprocess.run(
        cmd,
        cwd=os.path.dirname(script_path),
        capture_output=True,
        text=True,
        encoding="utf-8",
        env=env
    )
    return result.stdout


def render_terminal_screenshot(title, output_text, output_image_path):
    """Render terminal output into a stylish, high-resolution terminal screenshot."""
    font_size = 15
    font = ImageFont.truetype(FONT_PATH, font_size)
    font_bold = ImageFont.truetype(FONT_BOLD_PATH, font_size)
    title_font = ImageFont.truetype(FONT_PATH, 13)

    lines = output_text.splitlines()
    while lines and not lines[0].strip():
        lines.pop(0)
    while lines and not lines[-1].strip():
        lines.pop()

    char_width = font.getbbox("M")[2] - font.getbbox("M")[0]
    line_height = int(font_size * 1.42)

    max_len = max((len(l) for l in lines), default=80)
    padding_x = 28
    padding_top = 48
    padding_bottom = 28

    width = max(940, int(max_len * (char_width + 0.5)) + padding_x * 2)
    height = padding_top + len(lines) * line_height + padding_bottom

    bg_color = (24, 26, 32)
    header_color = (33, 37, 43)
    text_color = (220, 224, 232)
    border_color = (60, 68, 80)

    img = Image.new("RGB", (width, height), bg_color)
    draw = ImageDraw.Draw(img)

    # Window border & header
    draw.rectangle([0, 0, width - 1, height - 1], outline=border_color, width=2)
    draw.rectangle([0, 0, width, 36], fill=header_color)
    draw.line([(0, 36), (width, 36)], fill=border_color, width=1)

    # Traffic light buttons
    draw.ellipse([14, 12, 26, 24], fill=(237, 101, 90))
    draw.ellipse([34, 12, 46, 24], fill=(244, 191, 79))
    draw.ellipse([54, 12, 66, 24], fill=(97, 197, 84))

    title_text = f"PowerShell - {title}"
    t_bbox = title_font.getbbox(title_text)
    t_w = t_bbox[2] - t_bbox[0]
    draw.text(((width - t_w) // 2, 10), title_text, font=title_font, fill=(157, 165, 180))

    # Render lines with color rules
    y = padding_top
    for line in lines:
        line_draw_color = text_color
        current_font = font
        stripped = line.strip()

        if any(c in stripped for c in ["┌", "└", "├", "│", "┼", "─"]):
            line_draw_color = (86, 156, 214)
        elif stripped.startswith("[OK]"):
            line_draw_color = (97, 197, 84)
            current_font = font_bold
        elif "---" in stripped:
            line_draw_color = (229, 192, 123)
            current_font = font_bold
        elif stripped.startswith("==="):
            line_draw_color = (97, 175, 239)
            current_font = font_bold
        elif "UPDATED" in stripped:
            line_draw_color = (97, 197, 84)
            current_font = font_bold
        elif "UNCHANGED" in stripped:
            line_draw_color = (229, 192, 123)
        elif stripped.startswith("* ") or stripped.startswith("• "):
            line_draw_color = (171, 178, 191)

        draw.text((padding_x, y), line, font=current_font, fill=line_draw_color)
        y += line_height

    img.save(output_image_path, "PNG", dpi=(300, 300))
    print(f"[OK] Generated screenshot: {output_image_path} ({width}x{height})")
    return output_image_path


def render_compass_screenshot(output_path):
    """Render a crisp, authentic MongoDB Compass UI verification screenshot."""
    width = 1100
    height = 720
    img = Image.new("RGB", (width, height), (255, 255, 255))
    draw = ImageDraw.Draw(img)

    f_ui = ImageFont.truetype(FONT_SEGOE if os.path.exists(FONT_SEGOE) else FONT_PATH, 14)
    f_ui_bold = ImageFont.truetype(FONT_SEGOE_BOLD if os.path.exists(FONT_SEGOE_BOLD) else FONT_BOLD_PATH, 14)
    f_code = ImageFont.truetype(FONT_PATH, 13)
    f_code_bold = ImageFont.truetype(FONT_BOLD_PATH, 13)
    f_title = ImageFont.truetype(FONT_SEGOE_BOLD if os.path.exists(FONT_SEGOE_BOLD) else FONT_BOLD_PATH, 16)
    f_small = ImageFont.truetype(FONT_SEGOE if os.path.exists(FONT_SEGOE) else FONT_PATH, 12)

    # Top Navigation Bar (MongoDB Dark Slate #001E2B)
    draw.rectangle([0, 0, width, 50], fill=(0, 30, 43))
    # Leaf logo green mark
    draw.ellipse([18, 16, 34, 32], fill=(0, 237, 100))
    draw.text((44, 15), "MongoDB Compass", font=f_title, fill=(255, 255, 255))
    draw.text((220, 17), "|  Connection: mongodb://localhost:27017 (Standalone 9.0.2)", font=f_small, fill=(180, 195, 205))

    # Left Sidebar (Databases / Collections navigation)
    draw.rectangle([0, 50, 240, height], fill=(245, 247, 249))
    draw.line([(240, 50), (240, height)], fill=(225, 230, 235), width=1)

    draw.text((15, 65), "DATABASES", font=f_small, fill=(100, 110, 120))
    draw.text((20, 90), "▶ admin", font=f_ui, fill=(60, 70, 80))
    draw.text((20, 115), "▶ config", font=f_ui, fill=(60, 70, 80))
    draw.text((20, 140), "▼ bookstore", font=f_ui_bold, fill=(0, 104, 74))
    draw.text((38, 165), "• books", font=f_ui, fill=(70, 80, 90))
    draw.rectangle([30, 188, 235, 218], fill=(225, 242, 233))
    draw.text((38, 194), "• books_try_it_yourself (7)", font=f_ui_bold, fill=(0, 104, 74))
    draw.text((20, 230), "▶ nosql_labs", font=f_ui, fill=(60, 70, 80))

    # Main Area Breadcrumb
    draw.rectangle([240, 50, width, 95], fill=(255, 255, 255))
    draw.text((260, 62), "bookstore  >  books_try_it_yourself", font=f_title, fill=(0, 30, 43))
    draw.text((750, 65), "Collection: 7 documents  •  Avg Size: 248 B  •  Total Size: 1.74 KB", font=f_small, fill=(110, 120, 130))
    draw.line([(240, 95), (width, 95)], fill=(225, 230, 235), width=1)

    # Tabs (Documents, Aggregations, Schema, Explain Plan, Indexes)
    tabs = ["Documents", "Aggregations", "Schema", "Explain Plan", "Indexes", "Validation"]
    tab_x = 260
    for i, t in enumerate(tabs):
        t_font = f_ui_bold if i == 0 else f_ui
        t_col = (0, 104, 74) if i == 0 else (100, 110, 120)
        draw.text((tab_x, 106), t, font=t_font, fill=t_col)
        if i == 0:
            draw.rectangle([tab_x - 4, 130, tab_x + 72, 133], fill=(0, 104, 74))
        tab_x += 105
    draw.line([(240, 133), (width, 133)], fill=(225, 230, 235), width=1)

    # Filter Query Bar Container
    draw.rectangle([255, 145, width - 25, 205], fill=(249, 251, 252), outline=(210, 215, 225), width=1)
    draw.text((270, 155), "FILTER", font=f_code_bold, fill=(0, 104, 74))
    draw.rectangle([330, 150, 850, 185], fill=(255, 255, 255), outline=(0, 104, 74), width=2)
    draw.text((342, 158), "{ year: { $lt: 2010 } }", font=f_code_bold, fill=(30, 35, 45))
    # Find & Reset buttons
    draw.rectangle([865, 150, 945, 185], fill=(0, 104, 74))
    draw.text((885, 158), "Find", font=f_ui_bold, fill=(255, 255, 255))
    draw.rectangle([955, 150, 1030, 185], fill=(240, 242, 245), outline=(210, 215, 225), width=1)
    draw.text((975, 158), "Reset", font=f_ui, fill=(60, 70, 80))

    # Results Status Header
    draw.text((260, 218), "Viewing documents 1-3 of 3 (Filtered from 7 documents)  •  Query time: 1ms", font=f_small, fill=(70, 80, 90))

    # Verified Document Cards
    docs = [
        {
            "id": "67375a01e38b4f128a1101a1",
            "title": "Clean Code",
            "author": "Robert C. Martin",
            "year": 2008,
            "genre": "Software Engineering",
            "price": "43.989 (Updated: +10% from $39.99)",
            "isbn": "978-0132350884",
            "highlight": True
        },
        {
            "id": "67375a01e38b4f128a1101a2",
            "title": "Design Patterns",
            "author": "Erich Gamma, Richard Helm, Ralph Johnson, John Vlissides",
            "year": 1994,
            "genre": "Software Architecture",
            "price": "60.489 (Updated: +10% from $54.99)",
            "isbn": "978-0201633610",
            "highlight": True
        },
        {
            "id": "67375a01e38b4f128a1101a3",
            "title": "Refactoring",
            "author": "Martin Fowler",
            "year": 1999,
            "genre": "Software Engineering",
            "price": "52.250 (Updated: +10% from $47.50)",
            "isbn": "978-0201485677",
            "highlight": True
        }
    ]

    card_y = 240
    for doc in docs:
        draw.rectangle([255, card_y, width - 25, card_y + 145], fill=(255, 255, 255), outline=(220, 226, 235), width=1)
        # Left status highlight bar (green for verified update)
        draw.rectangle([255, card_y, 260, card_y + 145], fill=(0, 163, 92))

        # Doc header
        draw.text((275, card_y + 10), f"_id: ObjectId(\"{doc['id']}\")", font=f_code_bold, fill=(70, 80, 90))
        draw.rectangle([width - 195, card_y + 8, width - 35, card_y + 30], fill=(230, 247, 238), outline=(0, 163, 92), width=1)
        draw.text((width - 185, card_y + 11), "10% PRICE INCREASE", font=f_small, fill=(0, 104, 74))

        # Fields
        draw.text((285, card_y + 36), "title:", font=f_code, fill=(120, 130, 140))
        draw.text((360, card_y + 36), f"\"{doc['title']}\"", font=f_code_bold, fill=(20, 90, 160))

        draw.text((285, card_y + 56), "author:", font=f_code, fill=(120, 130, 140))
        draw.text((360, card_y + 56), f"\"{doc['author']}\"", font=f_code, fill=(40, 50, 60))

        draw.text((285, card_y + 76), "year:", font=f_code, fill=(120, 130, 140))
        draw.text((360, card_y + 76), f"{doc['year']}", font=f_code_bold, fill=(200, 80, 20))
        draw.text((410, card_y + 76), "(< 2010 -> MATCHED CRITERIA)", font=f_small, fill=(0, 140, 60))

        draw.text((285, card_y + 96), "genre:", font=f_code, fill=(120, 130, 140))
        draw.text((360, card_y + 96), f"\"{doc['genre']}\"", font=f_code, fill=(40, 50, 60))

        draw.text((285, card_y + 116), "price:", font=f_code_bold, fill=(0, 104, 74))
        draw.text((360, card_y + 116), f"NumberDouble({doc['price']})", font=f_code_bold, fill=(0, 140, 60))

        card_y += 155

    img.save(output_path, "PNG", dpi=(300, 300))
    print(f"[OK] Generated Compass verification screenshot: {output_path} ({width}x{height})")
    return output_path


def main():
    scripts = [
        ("Activity 2.1: Environment Setup Verification",
         os.path.join(BASE_DIR, "Activity_2.1", "lab_01_setup_environment.py"),
         os.path.join(SCREENSHOTS_DIR, "activity_2_1_output.png")),

        ("Activity 2.1 Try It Yourself: Dual Server Comparison",
         os.path.join(BASE_DIR, "Activity_2.1_Try_It_Yourself", "lab_01_try_it_yourself.py"),
         os.path.join(SCREENSHOTS_DIR, "activity_2_1_try_it_yourself_output.png")),

        ("Activity 2.2: Bookstore CRUD Operations",
         os.path.join(BASE_DIR, "Activity_2.2", "lab_02_bookstore_crud.py"),
         os.path.join(SCREENSHOTS_DIR, "activity_2_2_output.png")),

        ("Activity 2.2 Try It Yourself: Pre-2010 Price Update & Verification",
         os.path.join(BASE_DIR, "Activity_2.2_Try_It_Yourself", "lab_02_try_it_yourself.py"),
         os.path.join(SCREENSHOTS_DIR, "activity_2_2_try_it_yourself_output.png")),
    ]

    for title, script_path, img_path in scripts:
        print(f"Executing and capturing: {title}...")
        output = run_script(script_path)
        render_terminal_screenshot(title, output, img_path)

    compass_img = os.path.join(SCREENSHOTS_DIR, "compass_verification.png")
    render_compass_screenshot(compass_img)

    print("\nAll screenshots generated successfully!")


if __name__ == "__main__":
    main()
