import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import pandas as pd
import os
from io import BytesIO

st.set_page_config(page_title="Certificate Generator", layout="wide")
st.title("🖼 Certificate Generator")

# -------------------- Upload Certificate Template --------------------
template_file = st.file_uploader("Upload Certificate Template (PNG/JPG)", type=["png", "jpg", "jpeg"])

# -------------------- Upload Font --------------------
st.subheader("Upload Custom Font (Optional)")
uploaded_font = st.file_uploader("Upload .ttf Font File", type=["ttf"])

# -------------------- Built-in Font Selection --------------------
st.subheader("Or Use Built-in Font")
built_in_fonts = ["Arial", "Times", "Courier"]
selected_builtin_font = st.selectbox("Select Font", [""] + built_in_fonts)

bold = st.checkbox("Bold")
italic = st.checkbox("Italic")
font_size = st.number_input("Font Size", min_value=10, max_value=200, value=40)

# -------------------- Text Input --------------------
st.subheader("Certificate Details")
recipient_name = st.text_input("Recipient Name", "John Doe")
course_name = st.text_input("Course / Event Name", "Python Bootcamp")
date_text = st.text_input("Date", "01 Sep 2025")

# -------------------- Font Helper Function --------------------
def get_font_style(font_file=None, font_size=40, selected_builtin_font=None, bold=False, italic=False):
    """
    Returns a PIL ImageFont object.
    """
    # 1️⃣ Uploaded font
    if font_file:
        font_bytes = font_file.read()
        return ImageFont.truetype(BytesIO(font_bytes), font_size)

    # 2️⃣ Built-in fonts
    if selected_builtin_font:
        base_path = "fonts"  # Ensure your fonts are in this folder
        font_name = selected_builtin_font.lower()

        if bold and italic:
            font_file_name = f"{font_name}_bold_italic.ttf"
        elif bold:
            font_file_name = f"{font_name}_bold.ttf"
        elif italic:
            font_file_name = f"{font_name}_italic.ttf"
        else:
            font_file_name = f"{font_name}.ttf"

        font_path = os.path.join(base_path, font_file_name)

        if not os.path.isfile(font_path):
            st.error(f"Font not found: {font_path}")
            return ImageFont.load_default()

        return ImageFont.truetype(font_path, font_size)

    # 3️⃣ Fallback
    return ImageFont.load_default()

# -------------------- Generate Certificate --------------------
if st.button("Generate Certificate"):

    if template_file is None:
        st.warning("Please upload a certificate template first!")
    else:
        # Open template
        template = Image.open(template_file).convert("RGB")
        draw = ImageDraw.Draw(template)

        # Load font
        font = get_font_style(
            font_file=uploaded_font,
            font_size=font_size,
            selected_builtin_font=selected_builtin_font,
            bold=bold,
            italic=italic
        )

        # Define positions (adjust according to your template)
        width, height = template.size
        name_position = (width//2, height//2 - 50)
        course_position = (width//2, height//2 + 10)
        date_position = (width//2, height//2 + 70)

        # Draw text centered
        def draw_centered_text(draw, text, position, font, fill=(0,0,0)):
            w, h = draw.textsize(text, font=font)
            x, y = position
            draw.text((x - w/2, y - h/2), text, font=font, fill=fill)

        draw_centered_text(draw, recipient_name, name_position, font)
        draw_centered_text(draw, course_name, course_position, font)
        draw_centered_text(draw, date_text, date_position, font)

        # Display
        st.image(template, use_column_width=True)

        # Download button
        buf = BytesIO()
        template.save(buf, format="JPEG")
        byte_im = buf.getvalue()
        st.download_button(
            label="Download Certificate",
            data=byte_im,
            file_name=f"{recipient_name}_certificate.jpg",
            mime="image/jpeg"
        )
