import streamlit as st
from fpdf import FPDF
from PIL import Image
import re
import tempfile
import os

# Function to sanitize text by replacing unsupported Unicode characters
def sanitize_text(text):
    if text:
        # Replace common Unicode characters with their closest ASCII equivalents
        text = text.replace('\u2013', '-')  # Replace en dash with hyphen
        text = text.replace('\u2019', "'")  # Replace right single quotation mark with apostrophe
        text = text.replace('\u2018', "'")  # Replace left single quotation mark with apostrophe
        text = text.replace('\u201c', '"')  # Replace left double quotation mark with double quote
        text = text.replace('\u201d', '"')  # Replace right double quotation mark with double quote
        # Add more replacements as needed
    return text

# Function to generate PDF with Profile Picture and Resume Sections
def generate_pdf(name, email, phone, linkedin, github, about_me, education, experience, skills, certifications, image_file):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    # Theme Styling (Hardcoded to "Professional")
    primary_color = (0, 51, 102)  # Dark blue
    secondary_color = (0, 102, 204)  # Light blue

    pdf.set_draw_color(*primary_color)
    pdf.set_text_color(*primary_color)
    pdf.set_line_width(1)
    pdf.rect(5, 5, 200, 287)  # Border

    # Profile Picture
    if image_file is not None:
        # Save the uploaded image to a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp_file:
            img = Image.open(image_file)
            img.save(tmp_file.name, format="PNG")
            tmp_file_path = tmp_file.name

        # Add the image to the PDF
        pdf.image(tmp_file_path, x=20, y=20, w=50, h=50)
        pdf.ln(60)  # Space for image

        # Clean up the temporary file
        os.remove(tmp_file_path)

    # Name and Contact Info
    pdf.set_font("Arial", "B", 24)
    pdf.cell(0, 10, sanitize_text(name), ln=True, align='L')
    pdf.set_font("Arial", "I", 12)
    pdf.set_text_color(*secondary_color)
    pdf.cell(0, 10, f"Phone: {sanitize_text(phone)}", ln=True, align='L')
    pdf.cell(0, 10, f"Email: {sanitize_text(email)}", ln=True, align='L')
    pdf.cell(0, 10, f"LinkedIn: {sanitize_text(linkedin)} | GitHub: {sanitize_text(github)}", ln=True, align='L')
    pdf.ln(10)

    # Resume Sections
    sections = {
        "About Me": about_me,
        "Education": education,
        "Experience": experience,
        "Skills": skills,
        "Certifications": certifications
    }
    for section, content in sections.items():
        pdf.set_font("Arial", "B", 16)
        pdf.set_text_color(*primary_color)
        pdf.cell(0, 10, section, ln=True)
        pdf.set_font("Arial", "", 12)
        pdf.set_text_color(0, 0, 0)  # Black for content
        pdf.multi_cell(0, 10, sanitize_text(content))
        pdf.ln(5)

    return pdf

# Validation Functions
def validate_email(email):
    regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(regex, email)

def validate_phone(phone):
    regex = r'^\+?[0-9]{10,15}$'
    return re.match(regex, phone)

def validate_url(url):
    regex = r'^(https?://)?(www\.)?([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}(/\S*)?$'
    return re.match(regex, url)

# Streamlit App Layout with Advanced Styling
st.markdown("""
    <style>
    .main { background-color: #f5f5f5; font-family: Arial; }
    .stButton>button { background-color: #4CAF50; color: white; border-radius: 10px; }
    .stTextInput>div>div>input { border-radius: 10px; }
    .stTextArea>div>div>textarea { border-radius: 10px; }
    .stSelectbox>div>div>select { border-radius: 10px; }
    .stFileUploader>div>div>button { border-radius: 10px; }
    .stProgress>div>div>div>div { background-color: #4CAF50; }
    .resume-preview { background-color: white; padding: 20px; border-radius: 10px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); }
    .resume-preview h1 { color: #003366; }  /* Dark blue for name */
    .resume-preview h2 { color: #0066cc; }  /* Light blue for section headings */
    .resume-preview p { color: #333; }  /* Dark gray for text */
    .resume-preview .contact-details { background-color: #f0f8ff; padding: 15px; border-radius: 10px; }  /* Light blue background for contact details */
    .resume-preview .contact-details p { color: #0066cc; }  /* Light blue for contact details text */
    .profile-image { border-radius: 50%; width: 100px; height: 100px; object-fit: cover; }
    </style>
""", unsafe_allow_html=True)

st.title("Interactive Resume Builder")
st.sidebar.header("Enter Your Details")

# Progress Bar
if 'progress' not in st.session_state:
    st.session_state.progress = 0

# Input Fields with Validation
with st.sidebar.expander("Personal Information"):
    name = st.text_input("Full Name")
    email = st.text_input("Email")
    phone = st.text_input("Phone Number")
    linkedin = st.text_input("LinkedIn Profile")
    github = st.text_input("GitHub Profile")

    # Validate Email, Phone, and URLs
    if email and not validate_email(email):
        st.error("Please enter a valid email address.")
    if phone and not validate_phone(phone):
        st.error("Please enter a valid phone number.")
    if linkedin and not validate_url(linkedin):
        st.error("Please enter a valid LinkedIn URL.")
    if github and not validate_url(github):
        st.error("Please enter a valid GitHub URL.")

    # Update Progress
    if name and email and phone and linkedin and github:
        st.session_state.progress = 25

# About Me Section
with st.sidebar.expander("About Me"):
    about_me = st.text_area("Write something about yourself")

    # Update Progress
    if about_me:
        st.session_state.progress = 35

with st.sidebar.expander("Education & Experience"):
    education = st.text_area("Education Details")
    experience = st.text_area("Work Experience")

    # Update Progress
    if education and experience:
        st.session_state.progress = 50

with st.sidebar.expander("Skills & Certifications"):
    skills = st.text_area("Skills")
    certifications = st.text_area("Certifications")

    # Update Progress
    if skills and certifications:
        st.session_state.progress = 75

# Profile Picture Upload
with st.sidebar.expander("Profile Picture"):
    image = st.file_uploader("Upload Your Profile Picture", type=["jpg", "jpeg", "png"])
    if image is not None:
        img = Image.open(image)
        st.image(img, caption="Profile Picture", use_container_width=True)  # Fixed deprecated parameter
        st.session_state.progress = 100

# Display Progress Bar
st.sidebar.progress(st.session_state.progress)
st.sidebar.write(f"Completion: {st.session_state.progress}%")

# Preview Resume
if st.sidebar.button("Preview Resume"):
    if name and email and phone and about_me and education and experience and skills:
        st.markdown("<div class='resume-preview'>", unsafe_allow_html=True)
        
        # Two-column layout
        col1, col2 = st.columns([1, 3])

        # Left Column (Profile Picture and Contact Details)
        with col1:
            if image is not None:
                st.image(img, caption="", width=100, use_container_width=False)
            st.markdown("<div class='contact-details'>", unsafe_allow_html=True)
            st.markdown("<h2>Contact Details</h2>", unsafe_allow_html=True)
            st.markdown(f"<p><strong>Phone:</strong> {phone}</p>", unsafe_allow_html=True)
            st.markdown(f"<p><strong>Email:</strong> {email}</p>", unsafe_allow_html=True)
            st.markdown(f"<p><strong>LinkedIn:</strong> {linkedin}</p>", unsafe_allow_html=True)
            st.markdown(f"<p><strong>GitHub:</strong> {github}</p>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        # Right Column (Name, About Me, Education, Experience, Skills, Certifications)
        with col2:
            st.markdown(f"<h1>{name}</h1>", unsafe_allow_html=True)
            st.markdown("<h2>About Me</h2>", unsafe_allow_html=True)
            st.markdown(f"<p>{about_me}</p>", unsafe_allow_html=True)
            st.markdown("<h2>Education</h2>", unsafe_allow_html=True)
            st.markdown(f"<p>{education}</p>", unsafe_allow_html=True)
            st.markdown("<h2>Experience</h2>", unsafe_allow_html=True)
            st.markdown(f"<p>{experience}</p>", unsafe_allow_html=True)
            st.markdown("<h2>Skills</h2>", unsafe_allow_html=True)
            st.markdown(f"<p>{skills}</p>", unsafe_allow_html=True)
            st.markdown("<h2>Certifications</h2>", unsafe_allow_html=True)
            st.markdown(f"<p>{certifications}</p>", unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.error("Please fill out all required fields.")

# Generate and Download PDF
if st.sidebar.button("Download as PDF"):
    if name and email and phone and about_me and education and experience and skills:
        pdf = generate_pdf(name, email, phone, linkedin, github, about_me, education, experience, skills, certifications, image)
        pdf.output("resume.pdf")
        with open("resume.pdf", "rb") as file:
            btn = st.download_button(label="Download Resume", data=file, file_name="resume.pdf", mime="application/pdf")
    else:
        st.error("Please fill out all required fields.")