import streamlit as st
import cv2
import numpy as np
from PIL import Image, ImageEnhance, ImageDraw, ImageFont, ImageFilter, ImageOps
import zipfile
import io

# Custom CSS for Enhanced UI & Animation
st.markdown("""
    <style>
        body {
            background-color: #f0f2f6;
            font-family: 'Arial', sans-serif;
        }
        .stButton>button {
            color: white;
            background-color: #6c63ff;
            border-radius: 10px;
            transition: all 0.3s ease;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            padding: 10px 20px;
            font-size: 16px;
        }
        .stButton>button:hover {
            transform: scale(1.05) translateY(-2px);
            box-shadow: 0 8px 16px rgba(0, 0, 0, 0.3);
            background-color: #4e47cc;
        }
        .stSlider>div>div>div>div {
            background-color: #6c63ff !important;
        }
        .stTextInput>div>div>input {
            border-radius: 10px;
            border: 2px solid #6c63ff;
            padding: 10px;
        }
        .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
            color: #6c63ff;
        }
        .stImage>img {
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            transition: all 0.3s ease;
        }
        .stImage>img:hover {
            transform: scale(1.02);
            box-shadow: 0 8px 16px rgba(0, 0, 0, 0.3);
        }
    </style>
    """, unsafe_allow_html=True)

st.title("🎨 Advanced Pencil Sketch & Collage Maker")

# Add theme customization
st.sidebar.header("Theme")
theme = st.sidebar.selectbox("Choose Theme", ["Light", "Dark"])
if theme == "Dark":
    st.markdown("""
        <style>
            body {
                background-color: #1e1e1e;
                color: #ffffff;
            }
            .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
                color: #6c63ff;
            }
        </style>
        """, unsafe_allow_html=True)

# Multiple Image Upload
uploaded_files = st.file_uploader("Upload Images", type=['jpg', 'jpeg', 'png'], accept_multiple_files=True)

if uploaded_files:
    images = []
    sketches = []

    # Add image preview in sidebar
    st.sidebar.header("Uploaded Images")
    for uploaded_file in uploaded_files:
        st.sidebar.image(Image.open(uploaded_file), caption=uploaded_file.name, width=100)

    # Add progress bar
    progress_bar = st.progress(0)

    # Processing Each Uploaded Image
    for i, uploaded_file in enumerate(uploaded_files):
        with st.spinner(f'Processing {uploaded_file.name}...'):
            image = Image.open(uploaded_file)

            # Add cropping option
            st.sidebar.header(f"Crop Image - {uploaded_file.name}")
            crop_enabled = st.sidebar.checkbox(f"Enable Cropping for {uploaded_file.name}", key=f"crop_{uploaded_file.name}")
            if crop_enabled:
                left = st.sidebar.slider("Left", 0, image.width, 0, key=f"left_{uploaded_file.name}")
                top = st.sidebar.slider("Top", 0, image.height, 0, key=f"top_{uploaded_file.name}")
                right = st.sidebar.slider("Right", 0, image.width, image.width, key=f"right_{uploaded_file.name}")
                bottom = st.sidebar.slider("Bottom", 0, image.height, image.height, key=f"bottom_{uploaded_file.name}")
                image = image.crop((left, top, right, bottom))
                st.image(image, caption='Cropped Image', use_container_width=True)

            # Add rotation option
            st.sidebar.header(f"Rotate Image - {uploaded_file.name}")
            rotate_angle = st.sidebar.slider("Rotation Angle", -180, 180, 0, key=f"rotate_{uploaded_file.name}")
            if rotate_angle != 0:
                image = image.rotate(rotate_angle, expand=True)
                st.image(image, caption='Rotated Image', use_container_width=True)

            # Add resizing option
            st.sidebar.header(f"Resize Image - {uploaded_file.name}")
            resize_enabled = st.sidebar.checkbox(f"Enable Resizing for {uploaded_file.name}", key=f"resize_{uploaded_file.name}")
            if resize_enabled:
                new_width = st.sidebar.slider("Width", 100, 2000, image.width, key=f"width_{uploaded_file.name}")
                new_height = st.sidebar.slider("Height", 100, 2000, image.height, key=f"height_{uploaded_file.name}")
                image = image.resize((new_width, new_height))
                st.image(image, caption='Resized Image', use_container_width=True)

            # Convert PIL Image to OpenCV format
            img_cv = np.array(image.convert('RGB'))
            img_cv = cv2.cvtColor(img_cv, cv2.COLOR_RGB2BGR)
            
            # Pencil Sketch Conversion
            gray_image = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
            inverted_image = 255 - gray_image
            blurred = cv2.GaussianBlur(inverted_image, (21, 21), sigmaX=0, sigmaY=0)
            inverted_blurred = 255 - blurred
            sketch = cv2.divide(gray_image, inverted_blurred, scale=256.0)
            
            # Convert Sketch to PIL Format for Filters
            sketch_pil = Image.fromarray(sketch).convert("RGB")
            
            # Save Images for Collage
            images.append(image)
            sketches.append(sketch_pil)

            # Filters: Brightness, Contrast, Blur, Sharpen
            st.sidebar.header(f"Adjust Filters for {uploaded_file.name}")
            brightness = st.sidebar.slider("Brightness", 0.5, 2.0, 1.0, key=f"brightness_{uploaded_file.name}")
            contrast = st.sidebar.slider("Contrast", 0.5, 2.0, 1.0, key=f"contrast_{uploaded_file.name}")
            filter_type = st.sidebar.selectbox("Filter", ["None", "Sepia", "Black & White", "Blur", "Sharpen", "Emboss", "Edge Enhance", "Colorize"], key=f"filter_{uploaded_file.name}")
            
            enhancer = ImageEnhance.Brightness(sketch_pil)
            sketch_pil = enhancer.enhance(brightness)
            
            enhancer = ImageEnhance.Contrast(sketch_pil)
            sketch_pil = enhancer.enhance(contrast)
            
            # Extra Filters
            if filter_type == "Sepia":
                sepia = np.array(sketch_pil)
                sepia = cv2.transform(sepia, np.matrix([[0.393, 0.769, 0.189],
                                                       [0.349, 0.686, 0.168],
                                                       [0.272, 0.534, 0.131]]))
                sepia = np.clip(sepia, 0, 255)
                sketch_pil = Image.fromarray(sepia.astype('uint8'))
            
            elif filter_type == "Black & White":
                bw = np.array(sketch_pil.convert('L'))
                sketch_pil = Image.fromarray(bw).convert('RGB')
            
            elif filter_type == "Blur":
                sketch_pil = sketch_pil.filter(ImageFilter.GaussianBlur(radius=3))
            
            elif filter_type == "Sharpen":
                sketch_pil = sketch_pil.filter(ImageFilter.UnsharpMask(radius=2, percent=150, threshold=3))
            
            elif filter_type == "Emboss":
                sketch_pil = sketch_pil.filter(ImageFilter.EMBOSS)
            
            elif filter_type == "Edge Enhance":
                sketch_pil = sketch_pil.filter(ImageFilter.EDGE_ENHANCE)
            
            elif filter_type == "Colorize":
                color = st.sidebar.color_picker("Choose Color", "#FF5733", key=f"color_{uploaded_file.name}")
                r, g, b = int(color[1:3], 16), int(color[3:5], 16), int(color[5:7], 16)
                sketch_pil = ImageOps.colorize(sketch_pil.convert("L"), (r, g, b), (255, 255, 255))
            
            # Add watermark option
            st.sidebar.header(f"Add Watermark - {uploaded_file.name}")
            watermark_text = st.sidebar.text_input("Watermark Text", key=f"watermark_{uploaded_file.name}")
            if watermark_text:
                draw = ImageDraw.Draw(sketch_pil)
                font = ImageFont.load_default()
                
                # Use textbbox to get the bounding box of the text
                text_bbox = draw.textbbox((0, 0), watermark_text, font=font)
                text_width = text_bbox[2] - text_bbox[0]
                text_height = text_bbox[3] - text_bbox[1]
                
                x = sketch_pil.width - text_width - 10
                y = sketch_pil.height - text_height - 10
                draw.text((x, y), watermark_text, fill="white", font=font)
                st.image(sketch_pil, caption='Image with Watermark', use_container_width=True)

            # Display Pencil Sketch with Filters Applied
            st.image(sketch_pil, caption='Pencil Sketch (with Filters)', use_container_width=True)

            # Download Option for Each Image
            img_bytes = io.BytesIO()
            sketch_pil.save(img_bytes, format="PNG")
            st.download_button(f"Download Sketch - {uploaded_file.name}", data=img_bytes.getvalue(), file_name=f"sketch_{uploaded_file.name}", mime="image/png")

            # Update progress bar
            progress_bar.progress((i + 1) / len(uploaded_files))

    # Collage Option
    if len(sketches) > 1:
        st.subheader("Create Collage")
        cols = st.slider("Number of Columns", 1, len(sketches), 2)
        
        # Define widths and heights for collage
        widths, heights = zip(*(i.size for i in sketches))
        
        # Add collage layout options
        st.subheader("Collage Layout")
        layout = st.selectbox("Choose Layout", ["Grid", "Vertical", "Horizontal"])

        if layout == "Grid":
            total_width = max(widths) * cols
            total_height = sum(heights) // cols
            collage = Image.new('RGB', (total_width, total_height), (255, 255, 255))
            x_offset = 0
            y_offset = 0
            for i, img in enumerate(sketches):
                collage.paste(img, (x_offset, y_offset))
                x_offset += img.size[0]
                if (i + 1) % cols == 0:
                    x_offset = 0
                    y_offset += img.size[1]
        elif layout == "Vertical":
            total_width = max(widths)
            total_height = sum(heights)
            collage = Image.new('RGB', (total_width, total_height), (255, 255, 255))
            y_offset = 0
            for img in sketches:
                collage.paste(img, (0, y_offset))
                y_offset += img.size[1]
        elif layout == "Horizontal":
            total_width = sum(widths)
            total_height = max(heights)
            collage = Image.new('RGB', (total_width, total_height), (255, 255, 255))
            x_offset = 0
            for img in sketches:
                collage.paste(img, (x_offset, 0))
                x_offset += img.size[0]
        
        # Custom Text
        text = st.text_input("Enter Text for Collage")
        if text:
            draw = ImageDraw.Draw(collage)
            font = ImageFont.load_default()
            draw.text((10, 10), text, fill="black", font=font)
        
        # Sticker
        sticker_option = st.selectbox("Add Sticker", ["None", "Star", "Heart"])
        if sticker_option != "None":
            sticker_img = Image.open(f"stickers/{sticker_option.lower()}.png").convert("RGBA")
            collage.paste(sticker_img, (total_width - 100, total_height - 100), sticker_img)
        
        st.image(collage, caption='Collage of Pencil Sketches', use_container_width=True)

        # Download Collage
        img_bytes = io.BytesIO()
        collage.save(img_bytes, format="PNG")
        st.download_button("Download Collage", data=img_bytes.getvalue(), file_name="collage.png", mime="image/png")

    # Add save all sketches option
    if st.button("Download All Sketches as ZIP"):
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as zip_file:
            for i, sketch in enumerate(sketches):
                img_bytes = io.BytesIO()
                sketch.save(img_bytes, format="PNG")
                zip_file.writestr(f"sketch_{i+1}.png", img_bytes.getvalue())
        st.download_button("Download ZIP", data=zip_buffer.getvalue(), file_name="sketches.zip", mime="application/zip")