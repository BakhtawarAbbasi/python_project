import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io

st.set_page_config(page_title="Meme Factory", page_icon="😂")
st.title("🤖 Instant Meme Generator")

# Image upload section
uploaded_image = st.file_uploader("Meme ke liye photo chuno", type=["jpg", "png"])

# Text inputs
top_text = st.text_input("Top Text")
bottom_text = st.text_input("Bottom Text")

# Customization options
font_size = st.slider("Font Size", 20, 60, 40)
text_color = st.color_picker("Text Color", "#FFFFFF")

if uploaded_image and (top_text or bottom_text):
    # Image processing start
    img = Image.open(uploaded_image)
    draw = ImageDraw.Draw(img)
    width, height = img.size
    
    # Font settings
    font = ImageFont.truetype("arial.ttf", font_size)
    
    # Top text positioning
    if top_text:
        text_width = draw.textlength(top_text, font=font)
        x = (width - text_width) / 2
        draw.text((x, 10), top_text, fill=text_color, font=font)
    
    # Bottom text positioning
    if bottom_text:
        text_width = draw.textlength(bottom_text, font=font)
        x = (width - text_width) / 2
        draw.text((x, height-50), bottom_text, fill=text_color, font=font)
    
    # Show final image
    st.image(img, caption="Your Custom Meme")
    
    # Download button
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    st.download_button(
        label="📸 Download Meme",
        data=buf.getvalue(),
        file_name="my_meme.png",
        mime="image/png"
    )
else:
    st.warning("First upload image and then write a text!")