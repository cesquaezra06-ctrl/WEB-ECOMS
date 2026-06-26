import streamlit as st
import urllib.parse
from datetime import datetime
import json
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

st.set_page_config(page_title="Fonmora - Education Platform & Consultant", layout="wide", initial_sidebar_state="collapsed")

# WhatsApp Configuration
WHATSAPP_PHONE = "628174163999"  
WHATSAPP_BUSINESS_PHONE = "628174163999"  

# Email Configuration
EMAIL_SENDER = "fonmora.id@gmail.com"  
EMAIL_PASSWORD = "your-app-password"  
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
BUSINESS_EMAIL = "fonmora.id@gmail.com"  

# McKinsey-inspired CSS styling
st.markdown("""
<style>
    /* Menyembunyikan elemen bawaan Streamlit agar lebih bersih */
    header {visibility: hidden;}
    
            /* Animasi Halus (Fade In Up) */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    .animate-fade-in {
        animation: fadeInUp 0.8s ease-out forwards;
        opacity: 0; /* Sengaja disembunyikan di awal biar efek munculnya terasa */
    }
            
    /* Warna Utama McKinsey: Navy #051c2c, Bright Blue #00508f, White #ffffff, Gray #f4f4f4 */
    .title-mck { color: #051c2c; font-weight: 700; font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; letter-spacing: -0.5px; }
    .text-mck { color: #051c2c; font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; line-height: 1.6; }
    
    /* Tombol Korporat (Sharp Edges) */
    .btn-blue {
        background-color: #00508f; color: white !important; padding: 12px 28px;
        border-radius: 0px; text-decoration: none; font-weight: 600;
        display: inline-block; border: none; cursor: pointer; margin-top: 15px;
        transition: background-color 0.3s ease;
    }
    .btn-blue:hover { background-color: #003b6d; }
    
    /* Outline Button */
    .btn-outline {
        background-color: transparent; color: #00508f !important; padding: 10px 26px;
        border-radius: 0px; text-decoration: none; font-weight: 600;
        display: inline-block; border: 2px solid #00508f; cursor: pointer; margin-top: 15px;
        transition: all 0.3s ease;
    }
    .btn-outline:hover { background-color: #00508f; color: white !important; }

    /* Card Services (McKinsey Style Top-Border) */
    .service-card {
        background: white; padding: 30px 20px 20px 0; 
        text-align: left; margin-bottom: 20px; 
        border-top: 3px solid #051c2c; /* Garis atas khas konsultan */
    }
    
    /* Container Biru Gelap (How it Works & Consultation) */
    .dark-container {
        background-color: #051c2c; color: white; 
        padding: 60px 50px; margin: 40px 0;
        border-radius: 0px;
    }

    /* Override warna untuk kontainer gelap */
    .dark-container .title-mck { color: #ffffff !important; }
    .dark-container .text-mck { color: #e0e0e0 !important; }
    
    .number-step { font-size: 32px; font-weight: 300; margin-bottom: 10px; display: block; color: #00508f; }
    
    /* Style untuk tautan Navbar */
    .nav-link { text-decoration: none; color: #051c2c; font-weight: 500; transition: color 0.3s; font-size: 15px; margin-left: 20px;}
    .nav-link:hover { color: #00508f; }

    /* Force Streamlit app background to white */
    .stApp, body { background: #ffffff !important; }
</style>
""", unsafe_allow_html=True)


current_page = st.query_params.get("page", "home").lower()

# Corporate Navbar
navbar_html = """
<div style="display: flex; justify-content: space-between; align-items: center; padding: 20px 0; border-bottom: 1px solid #e0e0e0; margin-bottom: 40px;">
    <h2 class="title-mck" style="margin:0; letter-spacing: 1px;">FONMORA</h2>
    <div style="display: flex; align-items: center;">
        <a href="?page=home" target="_self" class="nav-link">Home</a>
        <a href="?page=about" target="_self" class="nav-link">About</a>
        <a href="?page=services" target="_self" class="nav-link">Capabilities</a>
        <a href="?page=consultation" target="_self" class="nav-link" style="color: #00508f; font-weight: 700;">Consultation</a>
    </div>
</div>
"""
st.markdown(navbar_html, unsafe_allow_html=True)

def page_home():
    # HERO SECTION (Left aligned, strong typography, dark overlay)
    st.markdown("""
    <div class="animate-fade-in" style="background-image: linear-gradient(to right, rgba(5, 28, 44, 0.95) 0%, rgba(5, 28, 44, 0.6) 50%, rgba(5, 28, 44, 0.2) 100%), url('https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=1600&q=80'); 
                background-size: cover; background-position: center; padding: 120px 60px; color: white;">
        <div style="max-width: 600px;">
            <p style="font-size: 14px; text-transform: uppercase; letter-spacing: 2px; margin-bottom: 10px; font-weight: 600;">Financial Consulting</p>
            <h1 style="font-size: 54px; font-weight: 700; line-height: 1.1; margin: 0 0 20px 0; font-family: 'Helvetica Neue', sans-serif;">
                Retail & Small Business Financial Strategies.
            </h1>
            <p style="font-size: 20px; font-weight: 300; margin-bottom: 40px; line-height: 1.5; color: #f4f4f4;">
                We help businesses and individuals make better, data-driven financial decisions to accelerate growth and stability.
            </p>
            <a href="?page=consultation" target="_self" class="btn-blue">Book a Free Consultation</a>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # CAPABILITIES OVERVIEW
    st.markdown("<div style='margin-top: 60px;'></div>", unsafe_allow_html=True)
    
    col_text, col_cards = st.columns([1, 2])
    with col_text:
        st.markdown("<h2 class='title-mck' style='font-size: 32px;'>How we help clients</h2>", unsafe_allow_html=True)
        st.markdown("<p class='text-mck'>Financial management consulting, strategic decision support, training, and product-based financial tools designed for operational excellence.</p>", unsafe_allow_html=True)
        st.markdown("<a href='?page=services' target='_self' class='btn-outline'>Explore our capabilities</a>", unsafe_allow_html=True)

    with col_cards:
        st.markdown("""
        <div style="background: #f4f4f4; padding: 40px; border-left: 4px solid #00508f;">
            <h4 class="title-mck" style="margin-bottom: 15px;">Featured Capabilities</h4>
            <div style="display: flex; flex-direction: column; gap: 15px;">
                <div style="border-bottom: 1px solid #ddd; padding-bottom: 10px;">
                    <strong>Financial Management</strong><br>
                    <span style="font-size: 14px; color: #051c2c;">Daily finance operations, accounting systems, and cash flow control.</span>
                </div>
                <div style="border-bottom: 1px solid #ddd; padding-bottom: 10px;">
                    <strong>Education & Training</strong><br>
                    <span style="font-size: 14px; color: #051c2c;">Master the language of money through practical courses.</span>
                </div>
                <div>
                    <strong>Ready-to-Use Templates</strong><br>
                    <span style="font-size: 14px; color: #051c2c;">Professional templates to track business performance in minutes.</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # HOW IT WORKS (Insights / Methodology style)
    st.markdown("""
    <div class="dark-container" style="display: flex; gap: 50px; flex-wrap: wrap; align-items: center;">
        <div style="flex: 1; min-width: 300px;">
            <h2 class="title-mck" style="font-size: 36px; margin-bottom: 20px;">Our approach</h2>
            <p style="font-size: 18px; color: #e0e0e0; font-weight: 300; margin-bottom: 30px;">
                We combine deep industry expertise with practical tools to transform your financial foundation.
            </p>
            <img src="https://images.unsplash.com/photo-1552664730-d307ca884978?auto=format&fit=crop&w=800&q=80" style="width: 100%; object-fit: cover; border: 1px solid rgba(255,255,255,0.2);" />
        </div>
        <div style="flex: 1.5; min-width: 300px; display: flex; flex-direction: column; gap: 30px;">
            <div style="border-top: 1px solid rgba(255,255,255,0.3); padding-top: 20px;">
                <span class="number-step" style="color: white; font-weight: 600; font-size: 20px;">01. Financial Management Consulting</span>
                <p style="font-size:15px; color: #e0e0e0; margin-top:10px; line-height:1.6;">Build a strong financial foundation with daily finance management, cash flow control, tax handling, and accounting systems designed for smooth operations.</p>
            </div>
            <div style="border-top: 1px solid rgba(255,255,255,0.3); padding-top: 20px;">
                <span class="number-step" style="color: white; font-weight: 600; font-size: 20px;">02. Strategic Financial Decision Support</span>
                <p style="font-size:15px; color: #e0e0e0; margin-top:10px; line-height:1.6;">Get expert guidance for pricing, cost structure, budgeting, and finance strategy to make smarter decisions for your business growth.</p>
            </div>
            <div style="border-top: 1px solid rgba(255,255,255,0.3); padding-top: 20px;">
                <span class="number-step" style="color: white; font-weight: 600; font-size: 20px;">03. Education & Training Platform</span>
                <p style="font-size:15px; color: #e0e0e0; margin-top:10px; line-height:1.6;">Master the language of money. We offer practical courses and workshops designed for business owners, professionals, and teams.</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def page_about():
    st.markdown("<h1 class='title-mck' style='font-size: 42px;'>About Fonmora</h1>", unsafe_allow_html=True)
    st.markdown("<div style='height: 4px; width: 60px; background-color: #00508f; margin-bottom: 30px;'></div>", unsafe_allow_html=True)
    
# SESUDAHNYA:
    st.markdown("""
<div class="img-zoom-container" style="margin-bottom: 30px; border: 1px solid #eee;">
    <img src="https://images.unsplash.com/photo-1600880292203-757bb62b4baf?auto=format&fit=crop&w=1200&q=80" style="width: 100%; max-height: 500px; object-fit: cover; object-position: center 25%; display: block;" />
</div>
""", unsafe_allow_html=True)    
    st.markdown("""
    <p class='text-mck' style='font-size: 22px; font-weight: 300; margin-top: 30px; margin-bottom: 40px; line-height: 1.5;'>
    We help businesses and individuals make better financial decisions through expert consulting, scalable training, and practical tools.
    </p>
    
    <div style='display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 40px; margin-top: 40px;'>
        <div>
            <h3 class='title-mck' style='font-size: 20px; border-bottom: 1px solid #ccc; padding-bottom: 10px;'>Our Scope</h3>
            <ul class='text-mck' style='font-size: 15px; list-style-type: none; padding-left: 0; margin-top: 15px;'>
                <li style='margin-bottom: 20px;'>
                    <strong style='color: #051c2c; font-size: 16px;'>Financial Management Consulting</strong><br>
                    <span style='font-size: 14px; color: #051c2c; line-height: 1.5; display: inline-block; margin-top: 4px;'>
                        Streamlining daily operations, setting up robust accounting systems, and maintaining strict cash flow control.
                    </span>
                </li>
                <li style='margin-bottom: 20px;'>
                    <strong style='color: #051c2c; font-size: 16px;'>Strategic Financial Decision Support</strong><br>
                    <span style='font-size: 14px; color: #051c2c; line-height: 1.5; display: inline-block; margin-top: 4px;'>
                        Providing data-driven guidance for pricing, cost optimization, budgeting, and long-term corporate strategy.
                    </span>
                </li>
                <li style='margin-bottom: 20px;'>
                    <strong style='color: #051c2c; font-size: 16px;'>Education & Training Platform</strong><br>
                    <span style='font-size: 14px; color: #051c2c; line-height: 1.5; display: inline-block; margin-top: 4px;'>
                        Elevating financial literacy through scalable, practical courses and workshops designed for professionals and teams.
                    </span>
                </li>
                <li style='margin-bottom: 20px;'>
                    <strong style='color: #051c2c; font-size: 16px;'>Financial Platform & Template Sales</strong><br>
                    <span style='font-size: 14px; color: #051c2c; line-height: 1.5; display: inline-block; margin-top: 4px;'>
                        Equipping businesses with standardized, ready-to-use digital tools and formatted frameworks for Excel and Notion.
                    </span>
                </li>
            </ul>
        </div>
        <div>
            <h3 class='title-mck' style='font-size: 20px; border-bottom: 1px solid #ccc; padding-bottom: 10px;'>Areas of Expertise</h3>
            <ul class='text-mck' style='font-size: 15px; padding-left: 20px; margin-top: 15px;'>
                <li style='margin-bottom: 15px;'>Cash flow & budgeting</li>
                <li style='margin-bottom: 15px;'>Pricing & cost structure optimization</li>
                <li style='margin-bottom: 15px;'>Corporate finance strategy</li>
            </ul>
        </div>
    </div>
    
    <div style='background-color: #f4f4f4; padding: 40px; margin-top: 50px; border-left: 4px solid #051c2c;'>
        <h3 class='title-mck' style='margin-top: 0;'>Business Model</h3>
        <div style='display: flex; gap: 30px; flex-wrap: wrap; margin-top: 20px;'>
            <div style='flex: 1; min-width: 200px;'>
                <strong style='color: #00508f;'>Layer 1: Consulting</strong>
                <p class='text-mck' style='font-size: 14px;'>High-touch, bespoke advisory services tailored to specific corporate needs.</p>
            </div>
            <div style='flex: 1; min-width: 200px;'>
                <strong style='color: #00508f;'>Layer 2: Courses</strong>
                <p class='text-mck' style='font-size: 14px;'>Scalable educational platforms to elevate team financial literacy.</p>
            </div>
            <div style='flex: 1; min-width: 200px;'>
                <strong style='color: #00508f;'>Layer 3: Tools & Templates</strong>
                <p class='text-mck' style='font-size: 14px;'>Standardized applications and formatted Excel/Notion frameworks.</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def page_services():
    # 1. Inject CSS Khusus untuk halaman ini (Efek Hover & Transisi)
    st.markdown("""
    <style>
        .cap-card {
            background: #ffffff;
            border: 1px solid #e0e0e0;
            border-top: 4px solid #051c2c;
            padding: 40px 30px;
            transition: all 0.4s ease;
            height: 100%;
            display: flex;
            flex-direction: column;
        }
        .cap-card:hover {
            transform: translateY(-10px);
            box-shadow: 0 15px 30px rgba(0,0,0,0.1);
            border-top: 4px solid #00508f;
        }
        .cap-icon {
            font-size: 45px;
            margin-bottom: 20px;
        }
        .learn-more-link {
            color: #051c2c; 
            text-decoration: none; 
            font-weight: 700; 
            font-size: 14px; 
            text-transform: uppercase; 
            letter-spacing: 1px; 
            display: inline-flex; 
            align-items: center; 
            transition: color 0.3s ease;
        }
        .cap-card:hover .learn-more-link {
            color: #00508f;
        }
    </style>
    """, unsafe_allow_html=True)

    # 2. Hero Banner dengan Gambar Latar
    st.markdown("""
    <div style="background-image: linear-gradient(to right, rgba(5, 28, 44, 0.95), rgba(5, 28, 44, 0.5)), url('https://images.unsplash.com/photo-1460925895917-afdab827c52f?auto=format&fit=crop&w=1600&q=80'); 
                height: 350px; background-size: cover; background-position: center; display: flex; align-items: center; padding: 0 60px; margin-bottom: 50px;">
        <div>
            <h1 style="color: white; font-size: 52px; font-family: 'Helvetica Neue', sans-serif; margin: 0; font-weight: 700;">Our Capabilities</h1>
            <div style="height: 4px; width: 60px; background-color: #00508f; margin: 20px 0;"></div>
            <p style="color: #f4f4f4; font-size: 20px; font-weight: 300; max-width: 700px; margin: 0; line-height: 1.5;">
                Delivering strategic financial advisory, practical education, and specialized digital tools to build a resilient operational foundation.
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # 3. Grid Kartu Layanan (dengan Ikon dan Efek Hover)
    col1, col2, col3 = st.columns(3)
    services = [
        "Financial Management Consulting",
        "Education & Training Platform",
        "Financial Platform & Products"
    ]
    
    icons = {
        "Financial Management Consulting": "📈", 
        "Education & Training Platform": "🎓",
        "Financial Platform & Products": "💻"
    }

    descriptions = {
        "Financial Management Consulting": "We help you manage daily business finances with precision. From setting up proper accounting systems and managing cash flow to handling taxes, ensuring operations run smoothly and safely.",
        "Education & Training Platform": "Master the language of money. Practical courses and workshops designed for business owners, professionals, and teams to make better money decisions.",
        "Financial Platform & Products": "Professionally designed, ready-to-use templates and calculators for Excel, Google Sheets, and Notion. Track your budget, expenses, and business performance in minutes."
    }

    for i, srv in enumerate(services):
        with [col1, col2, col3][i % 3]:
            description = descriptions.get(srv, "")
            icon = icons.get(srv, "🔹")
            
            if srv == "Financial Management Consulting":
                target_page = "product_showcase"
            elif srv == "Financial Platform & Products":
                target_page = "financial_products"
            else:
                target_page = "consultation"
                
            st.markdown(f"""
            <div class="cap-card">
                <div class="cap-icon">{icon}</div>
                <h4 class="title-mck" style="font-size: 22px; margin-bottom: 15px;">{srv}</h4>
                <p class="text-mck" style="font-size:15px; margin-bottom: 30px; flex-grow: 1; line-height: 1.6;">{description}</p>
                <a href="?page={target_page}" target="_self" class="learn-more-link">
                    Explore Details <span style="font-size: 18px; margin-left: 5px;">&rarr;</span>
                </a>
            </div>
            """, unsafe_allow_html=True)
            
    # 4. Banner Call-to-Action di Bagian Bawah
    st.markdown("""
    <div style="background-color: #f4f4f4; padding: 40px 50px; margin-top: 60px; display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; border-left: 4px solid #051c2c;">
        <div style="flex: 1; min-width: 300px;">
            <h3 class="title-mck" style="font-size: 24px; margin: 0 0 10px 0;">Not sure which capability fits your needs?</h3>
            <p class="text-mck" style="margin: 0; font-size: 16px;">Speak with our advisory team to diagnose your financial challenges and find the right structural solution.</p>
        </div>
        <div style="margin-top: 15px;">
            <a href="?page=consultation" target="_self" class="btn-blue" style="margin: 0;">Schedule a Discussion</a>
        </div>
    </div>
    """, unsafe_allow_html=True)

def page_product_showcase():
    st.markdown("<h1 class='title-mck' style='font-size: 42px;'>Financial Management Consulting</h1>", unsafe_allow_html=True)
    st.markdown("<p class='text-mck' style='font-size: 18px; margin-bottom: 40px;'>Specialized advisory solutions tailored to distinct business ecosystems.</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style="border-top: 3px solid #051c2c; padding-top: 20px; height: 100%; display: flex; flex-direction: column;">
            <h4 class="title-mck" style="font-size: 20px;">Small Business</h4>
            <p class="text-mck" style="font-size:15px; flex-grow: 1;">Complete financial infrastructure for SMEs. Comprehensive accounting, bookkeeping, and cash flow lifecycle management.</p>
            <a href="?page=consultation" target="_self" class="btn-blue" style="text-align: center; width: 100%; padding: 10px;">Consult Now</a>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="border-top: 3px solid #00508f; padding-top: 20px; height: 100%; display: flex; flex-direction: column;">
            <h4 class="title-mck" style="font-size: 20px;">Tax & Payments</h4>
            <p class="text-mck" style="font-size:15px; flex-grow: 1;">Strategic tax planning, compliance audits, and optimization of payment gateways to maximize capital retention.</p>
            <a href="?page=consultation" target="_self" class="btn-blue" style="text-align: center; width: 100%; padding: 10px;">Consult Now</a>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="border-top: 3px solid #051c2c; padding-top: 20px; height: 100%; display: flex; flex-direction: column;">
            <h4 class="title-mck" style="font-size: 20px;">Fintech Operations</h4>
            <p class="text-mck" style="font-size:15px; flex-grow: 1;">Modern financial technology integrations for seamless digital transactions, automated reporting, and data analytics.</p>
            <a href="?page=consultation" target="_self" class="btn-blue" style="text-align: center; width: 100%; padding: 10px;">Consult Now</a>
        </div>
        """, unsafe_allow_html=True)

def page_financial_products():
    st.markdown("<h1 class='title-mck' style='font-size: 42px;'>Financial Platform & Products</h1>", unsafe_allow_html=True)
    st.markdown("<p class='text-mck' style='font-size: 18px; margin-bottom: 40px;'>Streamline your business tracking with our professionally designed, ready-to-use templates.</p>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1.5])
    
    with col1:
        # Visualisasi bentuk file template
        st.markdown("""
        <div style="background-color: #f4f4f4; border: 1px solid #ddd; border-top: 4px solid #00508f; padding: 40px; text-align: center; height: 100%; display: flex; flex-direction: column; justify-content: center;">
            <div style="font-size: 70px; margin-bottom: 20px;">📊</div>
            <h3 style="color: #051c2c; font-family: 'Helvetica Neue', sans-serif; margin-bottom: 10px; font-size: 22px;">P&L Dapur Sejati.xls</h3>
            <p style="color: #051c2c; font-size: 14px;">Microsoft Excel Template</p>
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown("""
        <h3 class='title-mck' style='font-size: 26px; margin-top: 0;'>P&L Dapur Sejati.xls</h3>
        <p class='text-mck' style='font-size: 16px; margin-bottom: 20px;'>
        A comprehensive and automated Profit & Loss (P&L) template tailored specifically for F&B businesses. Stop building spreadsheets from scratch and gain instant clarity on your monthly financial performance.
        </p>
        
        <strong style="color: #051c2c; font-size: 16px;">Included Modules:</strong>
        <ul class='text-mck' style='font-size: 15px; padding-left: 20px; margin-top: 10px; margin-bottom: 30px;'>
            <li style='margin-bottom: 8px;'><b>12-Month Consolidated P&L:</b> Automatically aggregates data from January to December into a clean, executive-level dashboard.</li>
            <li style='margin-bottom: 8px;'><b>Pendapatan (Revenue Tracker):</b> Dedicated sheet to meticulously record daily transactions and revenue streams.</li>
            <li style='margin-bottom: 8px;'><b>Biaya (Cost Management):</b> Pre-structured expense categorization including <i>Biaya Bahan Baku</i> (Raw Materials) and <i>Biaya Pelengkap</i> (Supplementary F&B costs).</li>
            <li style='margin-bottom: 8px;'><b>Formula Automation:</b> Embedded formulas requiring zero technical setup—simply input the data.</li>
        </ul>
        """, unsafe_allow_html=True)
        
        # Pesan otomatis WhatsApp untuk pemesanan template
        wa_message = "Hello Fonmora, I am interested in purchasing the P&L Dapur Sejati.xls template. Could you please provide the pricing details?"
        wa_link = f"https://wa.me/{WHATSAPP_BUSINESS_PHONE}?text={urllib.parse.quote(wa_message)}"
        
        # Tombol Ask for Price (menggunakan gaya McKinsey corporate button)
        st.markdown(f"""
        <a href="{wa_link}" target="_blank" class="btn-blue" style="display: inline-flex; align-items: center; gap: 8px; font-size: 15px;">
            💬 Ask for Price
        </a>
        """, unsafe_allow_html=True)

# Email/WA Backend Functions
def send_whatsapp_message(phone_number, message):
    return f"https://wa.me/{phone_number}?text={urllib.parse.quote(message)}"

def send_email(to_email, subject, html_content):
    try:
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = EMAIL_SENDER
        msg['To'] = to_email
        part = MIMEText(html_content, 'html')
        msg.attach(part)
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.send_message(msg)
        return True, "Email sent successfully"
    except Exception as e:
        return False, f"Email error: {str(e)}"

def send_confirmation_email(first_name, email, phone_number, message_content):
    html_content = f"""
    <html>
        <head>
            <style>
                body {{ font-family: 'Helvetica Neue', Arial, sans-serif; background-color: #f4f4f4; }}
                .container {{ background-color: white; padding: 40px; max-width: 600px; margin: 0 auto; border-top: 4px solid #051c2c; }}
                .header {{ color: #051c2c; padding-bottom: 20px; border-bottom: 1px solid #eee; }}
                .content {{ padding: 20px 0; color: #333; line-height: 1.6; }}
                .booking-details {{ background-color: #f9f9f9; padding: 20px; border-left: 3px solid #00508f; margin: 20px 0; color: #333; }}
                .footer {{ color: #777; font-size: 12px; margin-top: 40px; padding-top: 20px; border-top: 1px solid #eee; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header"><h2>Fonmora Advisory Request</h2></div>
                <div class="content">
                    <p>Dear <strong>{first_name}</strong>,</p>
                    <p>Thank you for reaching out to Fonmora. We have received your consultation request.</p>
                    <div class="booking-details">
                        <p><strong>Name:</strong> {first_name}</p>
                        <p><strong>Email:</strong> {email}</p>
                        <p><strong>Phone:</strong> {phone_number}</p>
                        <p><strong>Inquiry:</strong><br>{message_content}</p>
                        <p><strong>Date:</strong> {datetime.now().strftime('%d %B %Y')}</p>
                    </div>
                    <p>Our advisory team will review your requirements and contact you within 24 hours to schedule your session.</p>
                </div>
                <div class="footer">
                    <p>© 2026 Fonmora - Professional Financial Consultants</p>
                    <p>Email: {BUSINESS_EMAIL}</p>
                </div>
            </div>
        </body>
    </html>
    """
    return send_email(email, "Consultation Request Received - Fonmora", html_content)

def send_admin_notification(first_name, last_name, email, phone_number, message_content):
    html_content = f"<html><body><h3>New Consultation Request</h3><p>Name: {first_name} {last_name}<br>Email: {email}<br>Phone: {phone_number}</p><p>Message: {message_content}</p></body></html>"
    return send_email(BUSINESS_EMAIL, f"New Inquiry - {first_name} {last_name}", html_content)

def save_consultation_data(data):
    filename = "consultations.json"
    consultations = []
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            consultations = json.load(f)
    consultations.append(data)
    with open(filename, 'w') as f:
        json.dump(consultations, f, indent=2)

def page_consultation():
    st.markdown("""
    <div style="background-color: #f4f4f4; padding: 60px 40px; border-left: 5px solid #051c2c; margin-bottom: 40px;">
        <h1 class="title-mck" style="font-size: 38px; margin: 0 0 10px 0;">Request a consultation</h1>
        <p class="text-mck" style="font-size: 18px; margin: 0;">Connect with our advisory team to discuss your business objectives.</p>
    </div>
    """, unsafe_allow_html=True)
    
    with st.form("consultation_form"):
        col1, col2 = st.columns(2)
        with col1:
            first_name = st.text_input("First Name", placeholder="Enter your first name")
            email = st.text_input("Business Email", placeholder="name@company.com")
        with col2:
            last_name = st.text_input("Last Name", placeholder="Enter your last name")
            phone_number = st.text_input("Phone Number", placeholder="+62 812 345 6789")
            
        message_content = st.text_area("How can we assist you?", placeholder="Please provide details about your inquiry...", height=150)
        
        contact_method = st.radio("Preferred Contact Method:", ["Email", "WhatsApp", "Both"], horizontal=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        submitted = st.form_submit_button("Submit Request", type="primary")
        
        if submitted:
            if not all([first_name, last_name, phone_number, email, message_content]):
                st.error("Please fill in all required fields.")
            else:
                clean_phone = ''.join(filter(str.isdigit, phone_number))
                if not clean_phone.startswith('62'):
                    clean_phone = '62' + clean_phone.lstrip('0')
                
                consultation_data = {
                    "timestamp": datetime.now().isoformat(),
                    "first_name": first_name, "last_name": last_name,
                    "email": email, "phone_number": phone_number,
                    "message": message_content, "contact_method": contact_method
                }
                save_consultation_data(consultation_data)
                
                consultation_summary = f"*FONMORA INQUIRY*\n\nName: {first_name} {last_name}\nEmail: {email}\nPhone: {phone_number}\n\nMessage:\n{message_content}"
                email_success, email_message = send_confirmation_email(first_name, email, phone_number, message_content)
                send_admin_notification(first_name, last_name, email, phone_number, message_content)
                
                st.success("✅ Inquiry successfully submitted. Our team will contact you shortly.")
                
                if contact_method in ["WhatsApp", "Both"]:
                    st.markdown("---")
                    whatsapp_link = send_whatsapp_message(clean_phone, consultation_summary)
                    st.markdown(f"**Immediate Assistance:** [Start WhatsApp Chat]({whatsapp_link})")

# Routing
if current_page == "home": 
    page_home()
elif current_page == "about": 
    page_about()
elif current_page == "services": 
    page_services()
elif current_page == "consultation": 
    page_consultation()
elif current_page == "product_showcase": 
    page_product_showcase()
elif current_page == "financial_products": 
    page_financial_products()
else: 
    page_home()

# ==========================================
# CORPORATE FOOTER
# ==========================================
st.markdown("<div class='animate-fade-in'>", unsafe_allow_html=True)
st.markdown("<hr style='margin: 80px 0 40px 0; border-color: #e0e0e0;'>", unsafe_allow_html=True)
# Mengatur rasio kolom agar kolom pertama sedikit lebih lebar untuk teks deskripsi
f1, f2, f3, f4 = st.columns([1.5, 1, 1, 1])

with f1: 
    st.markdown("""
    <h3 class='title-mck' style='font-size: 20px; margin-bottom: 15px;'>FONMORA</h3>
    <p class='text-mck' style='font-size: 14px; line-height: 1.6; margin-bottom: 25px; padding-right: 20px;'>
        Empowering retail and small businesses through strategic financial advisory, practical education, and ready-to-use digital tools.
    </p>
    <div style='display: flex; gap: 20px;'>
        <a href='#' style='text-decoration:none; color: #051c2c; font-weight: 600; font-size: 14px; border-bottom: 1px solid transparent; transition: border-color 0.3s;' onmouseover="this.style.borderBottom='1px solid #051c2c'" onmouseout="this.style.borderBottom='1px solid transparent'">LinkedIn</a>
        <a href='#' style='text-decoration:none; color: #051c2c; font-weight: 600; font-size: 14px; border-bottom: 1px solid transparent; transition: border-color 0.3s;' onmouseover="this.style.borderBottom='1px solid #051c2c'" onmouseout="this.style.borderBottom='1px solid transparent'">Instagram</a>
    </div>
    """, unsafe_allow_html=True)

with f2: 
    st.markdown("""
    <strong class='text-mck' style='font-size: 15px; color: #051c2c;'>Quick Links</strong><br><br>
    <div style='display: flex; flex-direction: column; gap: 12px;'>
        <a href='?page=home' target='_self' style='text-decoration:none; color: #051c2c; font-size: 14px; transition: color 0.3s;' onmouseover="this.style.color='#00508f'" onmouseout="this.style.color='#051c2c'">Home</a>
        <a href='?page=about' target='_self' style='text-decoration:none; color: #051c2c; font-size: 14px; transition: color 0.3s;' onmouseover="this.style.color='#00508f'" onmouseout="this.style.color='#051c2c'">About Us</a>
        <a href='?page=services' target='_self' style='text-decoration:none; color: #051c2c; font-size: 14px; transition: color 0.3s;' onmouseover="this.style.color='#00508f'" onmouseout="this.style.color='#051c2c'">Capabilities</a>
        <a href='?page=financial_products' target='_self' style='text-decoration:none; color: #051c2c; font-size: 14px; transition: color 0.3s;' onmouseover="this.style.color='#00508f'" onmouseout="this.style.color='#051c2c'">Financial Products</a>
    </div>
    """, unsafe_allow_html=True)

with f3: 
    st.markdown(f"""
    <strong class='text-mck' style='font-size: 15px; color: #051c2c;'>Connect</strong><br><br>
    <div style='display: flex; flex-direction: column; gap: 12px;'>
        <a href='https://wa.me/{WHATSAPP_BUSINESS_PHONE}?text=Hello%20Fonmora' target='_blank' style='text-decoration:none; color: #00508f; font-size: 14px; font-weight: 600;'>
            WhatsApp Support &nearr;
        </a>
        <a href='mailto:fonmora.id@gmail.com' style='text-decoration:none; color: #051c2c; font-size: 14px; transition: color 0.3s;' onmouseover="this.style.color='#00508f'" onmouseout="this.style.color='#051c2c'">fonmora.id@gmail.com</a>
        <span style='color: #051c2c; font-size: 14px; line-height: 1.5;'>Semarang, Central Java<br>Indonesia</span>
    </div>
    """, unsafe_allow_html=True)

with f4: 
    st.markdown("""
    <strong class='text-mck' style='font-size: 15px; color: #051c2c;'>Business Info</strong><br><br>
    <div style='display: flex; flex-direction: column; gap: 12px;'>
        <span style='color: #051c2c; font-size: 14px;'><strong>Mon - Fri:</strong> 09:00 - 17:00 WIB</span>
        <div style='height: 1px; background-color: #eee; margin: 8px 0;'></div>
        <a href='#' style='text-decoration:none; color: #051c2c; font-size: 13px; transition: color 0.3s;' onmouseover="this.style.color='#00508f'" onmouseout="this.style.color='#051c2c'">Terms of Use</a>
        <a href='#' style='text-decoration:none; color: #051c2c; font-size: 13px; transition: color 0.3s;' onmouseover="this.style.color='#00508f'" onmouseout="this.style.color='#051c2c'">Privacy Policy</a>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='text-align:left; margin-top:50px; padding-bottom:20px; color: #051c2c; font-size: 13px; font-family: sans-serif; border-top: 1px solid #eee; padding-top: 20px;'>© 2026 Fonmora. All rights reserved.</div>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)