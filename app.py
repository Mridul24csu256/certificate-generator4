import streamlit as st
import pandas as pd
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import zipfile
from streamlit_drawable_canvas import st_canvas

st.set_page_config(layout="wide")
st.title("🎉 Advanced Certificate Generator with Drag, Snap, Bold & Italic")

SNAP_THRESHOLD = 10  # pixels

# ------------------ Helper Functions ------------------
def get_font_style(font_file, size, font_choice, built_in_fonts=None, selected_builtin_font=None, bold=False, italic=False):
    if font_choice == "Uploaded" and font_file:
        return ImageFont.truetype(BytesIO(font_file.getvalue()), size)
    elif font_choice == "Built-in":
        font_map = {
            ("Arial", False, False): "fonts/arial.ttf",
            ("Arial", True, False): "fonts/arial_bold.ttf",
            ("Arial", False, True): "fonts/arial_italic.ttf",
            ("Arial", True, True): "fonts/arial_bold_italic.ttf",
            ("Times New Roman", False, False): "fonts/times.ttf",
            ("Times New Roman", True, False): "fonts/times_bold.ttf",
            ("Times New Roman", False, True): "fonts/import streamlit as st
import pandas as pd
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import zipfile
from streamlit_drawable_canvas import st_canvas

st.set_page_config(layout="wide")
st.title("🎉 Advanced Certificate Generator with Drag, Snap, Bold & Italic")

SNAP_THRESHOLD = 10  # pixels

# ------------------ Helper Functions ------------------
def get_font_style(font_file, size, font_choice, built_in_fonts=None, selected_builtin_font=None, bold=False, italic=False):
    if font_choice == "Uploaded" and font_file:
        return ImageFont.truetype(BytesIO(font_file.getvalue()), size)
    elif font_choice == "Built-in":
        font_map = {
            ("Arial", False, False): "fonts/arial.ttf",
            ("Arial", True, False): "fonts/arial_bold.ttf",
            ("Arial", False, True): "fonts/arial_italic.ttf",
            ("Arial", True, True): "fonts/arial_bold_italic.ttf",
            ("Times New Roman", False, False): "fonts/times.ttf",
            ("Times New Roman", True, False): "fonts/times_bold.ttf",
            ("Times New Roman", False, True): "fonts/times_italic.ttf",
            ("Times New Roman", True, True): "fonts/times_bold_italic.ttf",
            ("Courier New", False, False): "fonts/courier.ttf",
            ("Courier New", True, False): "fonts/courier_bold.ttf",
            ("Courier New", False, True): "fonts/courier_italic.ttf",
            ("Courier New", True, True): "fonts/courier_bold_italic.ttf",
        }
        font_path = font_map.get((selected_builtin_font, bold, italic), "fonts/arial.ttf")
        return ImageFont.truetype(font_path, size)
    else:
        return ImageFont.load_default()

def snap_position(x, y, text_width, text_height, canvas_width, canvas_height, other_boxes=[]):
    center_x = canvas_width // 2 - text_width // 2
    center_y = canvas_height // 2 - text_height // 2
    if abs(x - center_x) < SNAP_THRESHOLD:
        x = center_x
    if abs(y - center_y) < SNAP_THRESHOLD:
        y = center_y
    for box in other_boxes:
        bx, by = box
        if abs(x - bx) < SNAP_THRESHOLD:
            x = bx
        if abs(y - by) < SNAP_THRESHOLD:
            y = by
    return x, y

# ------------------ Upload Template ------------------
template_file = st.file_uploader("Upload Certificate Template (PNG/JPG)", type=["png", "jpg", "jpeg"])
if not template_file:
    st.stop()
template = Image.open(template_file).convert("RGB")
st.image(template, caption="Certificate Template Preview", use_container_width=True)

# ------------------ Font Selection ------------------
font_choice = st.radio("Choose Font Source", ["Uploaded", "Built-in"])
font_file = None
built_in_fonts = {
    "Arial": "fonts/arial.ttf",
    "Times New Roman": "fonts/times.ttf",
    "Courier New": "fonts/courier.ttf",
}
selected_builtin_font = None
if font_choice == "Uploaded":
    font_file = st.file_uploader("Upload Custom Font (.ttf)", type=["ttf"])
else:
    selected_builtin_font = st.selectbox("Select Built-in Font", list(built_in_fonts.keys()))

# ------------------ Upload Data File ------------------
data_file = st.file_uploader("Upload Data File (CSV/Excel)", type=["csv", "xlsx"])
if not data_file:
    st.stop()
if data_file.name.endswith(".csv"):
    df = pd.read_csv(data_file)
else:
    df = pd.read_excel(data_file)
st.write("### Preview Data")
st.dataframe(df.head())

# ------------------ Column Selection ------------------
selected_columns = st.multiselect("Select Columns to Print", df.columns)
if not selected_columns:
    st.stop()

# ------------------ Text Boxes & Positioning ------------------
column_text_boxes = {}
for col in selected_columns:
    st.subheader(f"Text Boxes for {col}")
    num_boxes = st.number_input(f"Number of text boxes for {col}", 1, 5, 1, key=f"num_{col}")
    boxes = []

    for i in range(num_boxes):
        st.write(f"Configure Text Box {i+1} for {col}")
        text_prefix = st.text_input(f"Prefix for box {i+1}", "", key=f"prefix_{col}_{i}")
        text_suffix = st.text_input(f"Suffix for box {i+1}", "", key=f"suffix_{col}_{i}")
        font_size = st.slider(f"Font size for box {i+1}", 10, 100, 40, key=f"size_{col}_{i}")
        font_color = st.color_picker(f"Font color for box {i+1}", "#000000", key=f"color_{col}_{i}")
        bold = st.checkbox(f"Bold", key=f"bold_{col}_{i}")
        italic = st.checkbox(f"Italic", key=f"italic_{col}_{i}")

        # Create temporary template with guides
        temp_img = template.copy()
        draw = ImageDraw.Draw(temp_img)
        sample_text = f"{text_prefix}{df.iloc[0][col]}{text_suffix}"
        font = get_font_style(font_file, font_size, font_choice, built_in_fonts, selected_builtin_font, bold, italic)
        
        # Updated: Use textbbox instead of textsize
        bbox = draw.textbbox((0, 0), sample_text, font=font)
        text_size = (bbox[2] - bbox[0], bbox[3] - bbox[1])
        
        rect_x, rect_y = 50, 50
        draw.rectangle([rect_x, rect_y, rect_x + text_size[0], rect_y + text_size[1]], outline="red", width=2)
        draw.line([temp_img.width // 2, 0, temp_img.width // 2, temp_img.height], fill="blue", width=1)
        draw.line([0, temp_img.height // 2, temp_img.width, temp_img.height // 2], fill="blue", width=1)

        # Canvas
        canvas_result = st_canvas(
            fill_color="rgba(0,0,0,0)",
            stroke_width=1,
            stroke_color="black",
            background_image=temp_img,  # Pass PIL Image directly
            update_streamlit=True,
            height=template.height,
            width=template.width,
            drawing_mode="rect",
            key=f"canvas_{col}_{i}",
        )

        # Position & Snap
        if canvas_result.json_data and "objects" in canvas_result.json_data and canvas_result.json_data["objects"]:
            rect = canvas_result.json_data["objects"][0]
            raw_x = int(rect["left"])
            raw_y = int(rect["top"])
        else:
            raw_x, raw_y = rect_x, rect_y

        other_boxes = [(b["pos"][0], b["pos"][1]) for b in boxes]
        x, y = snap_position(raw_x, raw_y, text_size[0], text_size[1], temp_img.width,
.ttf",
            ("Times New Roman", True, True): "fonts/times_bold_italic.ttf",
            ("Courier New", False, False): "fonts/courier.ttf",
            ("Courier New", True, False): "fonts/courier_bold.ttf",
            ("Courier New", False, True): "fonts/courier_italic.ttf",
            ("Courier New", True, True): "fonts/courier_bold_italic.ttf",
        }
        font_path = font_map.get((selected_builtin_font, bold, italic), "fonts/arial.ttf")
        return ImageFont.truetype(font_path, size)
    else:
        return ImageFont.load_default()

def snap_position(x, y, text_width, text_height, canvas_width, canvas_height, other_boxes=[]):
    center_x = canvas_width // 2 - text_width // 2
    center_y = canvas_height // 2 - text_height // 2
    if abs(x - center_x) < SNAP_THRESHOLD:
        x = center_x
    if abs(y - center_y) < SNAP_THRESHOLD:
        y = center_y
    for box in other_boxes:
        bx, by = box
        if abs(x - bx) < SNAP_THRESHOLD:
            x = bx
        if abs(y - by) < SNAP_THRESHOLD:
            y = by
    return x, y

# ------------------ Upload Template ------------------
template_file = st.file_uploader("Upload Certificate Template (PNG/JPG)", type=["png", "jpg", "jpeg"])
if not template_file:
    st.stop()
template = Image.open(template_file).convert("RGB")
st.image(template, caption="Certificate Template Preview", use_container_width=True)

# ------------------ Font Selection ------------------
font_choice = st.radio("Choose Font Source", ["Uploaded", "Built-in"])
font_file = None
built_in_fonts = {
    "Arial": "fonts/arial.ttf",
    "Times New Roman": "fonts/times.ttf",
    "Courier New": "fonts/courier.ttf",
}
selected_builtin_font = None
if font_choice == "Uploaded":
    font_file = st.file_uploader("Upload Custom Font (.ttf)", type=["ttf"])
else:
    selected_builtin_font = st.selectbox("Select Built-in Font", list(built_in_fonts.keys()))

# ------------------ Upload Data File ------------------
data_file = st.file_uploader("Upload Data File (CSV/Excel)", type=["csv", "xlsx"])
if not data_file:
    st.stop()
if data_file.name.endswith(".csv"):
    df = pd.read_csv(data_file)
else:
    df = pd.read_excel(data_file)
st.write("### Preview Data")
st.dataframe(df.head())

# ------------------ Column Selection ------------------
selected_columns = st.multiselect("Select Columns to Print", df.columns)
if not selected_columns:
    st.stop()

# ------------------ Text Boxes & Positioning ------------------
column_text_boxes = {}
for col in selected_columns:
    st.subheader(f"Text Boxes for {col}")
    num_boxes = st.number_input(f"Number of text boxes for {col}", 1, 5, 1, key=f"num_{col}")
    boxes = []

    for i in range(num_boxes):
        st.write(f"Configure Text Box {i+1} for {col}")
        text_prefix = st.text_input(f"Prefix for box {i+1}", "", key=f"prefix_{col}_{i}")
        text_suffix = st.text_input(f"Suffix for box {i+1}", "", key=f"suffix_{col}_{i}")
        font_size = st.slider(f"Font size for box {i+1}", 10, 100, 40, key=f"size_{col}_{i}")
        font_color = st.color_picker(f"Font color for box {i+1}", "#000000", key=f"color_{col}_{i}")
        bold = st.checkbox(f"Bold", key=f"bold_{col}_{i}")
        italic = st.checkbox(f"Italic", key=f"italic_{col}_{i}")

        # Create temporary template with guides
        temp_img = template.copy()
        draw = ImageDraw.Draw(temp_img)
        sample_text = f"{text_prefix}{df.iloc[0][col]}{text_suffix}"
        font = get_font_style(font_file, font_size, font_choice, built_in_fonts, selected_builtin_font, bold, italic)
        
        # Updated: Use textbbox instead of textsize
        bbox = draw.textbbox((0, 0), sample_text, font=font)
        text_size = (bbox[2] - bbox[0], bbox[3] - bbox[1])
        
        rect_x, rect_y = 50, 50
        draw.rectangle([rect_x, rect_y, rect_x + text_size[0], rect_y + text_size[1]], outline="red", width=2)
        draw.line([temp_img.width // 2, 0, temp_img.width // 2, temp_img.height], fill="blue", width=1)
        draw.line([0, temp_img.height // 2, temp_img.width, temp_img.height // 2], fill="blue", width=1)

        # Canvas
        canvas_result = st_canvas(
            fill_color="rgba(0,0,0,0)",
            stroke_width=1,
            background_image=temp_img.convert("RGBA"),  # ensure RGBA
            update_streamlit=True,
            height=template.height,
            width=template.width,
            drawing_mode="rect",
            key=f"canvas_{col}_{i}",
        )

        # Position & Snap
        if canvas_result.json_data and "objects" in canvas_result.json_data and canvas_result.json_data["objects"]:
            rect = canvas_result.json_data["objects"][0]
            raw_x = int(rect["left"])
            raw_y = int(rect["top"])
        else:
            raw_x, raw_y = rect_x, rect_y

        other_boxes = [(b["pos"][0], b["pos"][1]) for b in boxes]
        x, y = snap_position(raw_x, raw_y, text_size[0], text_size[1], temp_img.width, temp_img.height, other_boxes)

        boxes.append({
            "prefix": text_prefix,
            "suffix": text_suffix,
            "size": font_size,
            "color": font_color,
            "bold": bold,
            "italic": italic,
            "pos": (x, y)
        })

    column_text_boxes[col] = boxes

# ------------------ Preview First Certificate ------------------
if st.button("👀 Preview First Certificate"):
    sample_row = df.iloc[0]
    cert = template.copy()
    draw = ImageDraw.Draw(cert)
    for col, boxes in column_text_boxes.items():
        for box in boxes:
            text = f"{box['prefix']}{sample_row[col]}{box['suffix']}"
            font = get_font_style(font_file, box["size"], font_choice, built_in_fonts, selected_builtin_font, box["bold"], box["italic"])
            
            # Updated: compute text size if needed
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            
            x, y = box["pos"]
            if box["bold"] and font_choice == "Uploaded":
                draw.text((x, y), text, font=font, fill=box["color"])
                draw.text((x+1, y), text, font=font, fill=box["color"])
            else:
                draw.text((x, y), text, font=font, fill=box["color"])
    st.image(cert, caption="Preview Certificate", use_container_width=True)

# ------------------ Generate All Certificates ------------------
if st.button("🎉 Generate All Certificates"):
    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, "w") as zipf:
        for _, row in df.iterrows():
            cert = template.copy()
            draw = ImageDraw.Draw(cert)
            for col, boxes in column_text_boxes.items():
                for box in boxes:
                    text = f"{box['prefix']}{row[col]}{box['suffix']}"
                    font = get_font_style(font_file, box["size"], font_choice, built_in_fonts, selected_builtin_font, box["bold"], box["italic"])
                    
                    # Updated: compute text size if needed
                    bbox = draw.textbbox((0, 0), text, font=font)
                    text_width = bbox[2] - bbox[0]
                    text_height = bbox[3] - bbox[1]
                    
                    x, y = box["pos"]
                    if box["bold"] and font_choice == "Uploaded":
                        draw.text((x, y), text, font=font, fill=box["color"])
                        draw.text((x+1, y), text, font=font, fill=box["color"])
                    else:
                        draw.text((x, y), text, font=font, fill=box["color"])
            img_bytes = BytesIO()
            cert.save(img_bytes, format="PNG")
            img_bytes.seek(0)
            zipf.writestr(f"{row[selected_columns[0]]}_certificate.png", img_bytes.read())
    zip_buffer.seek(0)
    st.success("✅ Certificates generated successfully!")
    st.download_button(
        label="⬇️ Download All Certificates (ZIP)",
        data=zip_buffer,
        file_name="certificates.zip",
        mime="application/zip"
    )
