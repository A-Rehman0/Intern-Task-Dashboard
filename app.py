import streamlit as st
import pandas as pd
import pickle
from datetime import datetime

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Blue Planet Dashboard", layout="wide")
st.set_page_config(layout="wide")
# ---------------- CSS ----------------
st.markdown("""
<style>
#MainMenu, footer, header {visibility: hidden;}

.block-container {
    padding: 0 2rem 1rem 2rem !important;
    margin-top: 0 !important;
    background-color: #eef5ff;
}

.block-container > div:first-child {
    margin-top: 0 !important;
}
/* HEADER */
.topbar {
    background-color: #0a58ca;
    padding: 14px 20px;
    border-radius: 10px;
    color: white;
    margin-bottom: 20px;
}

/* CARD */
.card {
    background: white;
    padding: 18px;
    border-radius: 12px;
    box-shadow: 0 3px 8px rgba(0,0,0,0.05);
}

/* KPI */
.kpi {
    text-align: center;
    padding: 4px 6px;
    border-radius: 10px;
    background: white;
    box-shadow: 0 2px 5px rgba(0,0,0,0.05);
}

.kpi h1 {
    color: #0a58ca;
    margin: 0;
    font-size: 32px;   /* increased safely */
}

.kpi p {
    color: gray;
    font-size: 14px;   /* slightly bigger */
    margin: 0;
    position:center;
}

/* SECTION */
.section {
    font-size: 18px;
    font-weight: 600;
    margin: 10px 0;
    color: #0a58ca;
}
/* Table border */
.stDataFrame div[data-testid="stDataFrameContainer"] table {
    border: 2px solid #0a58ca;
    border-collapse: collapse;
}
.stDataFrame div[data-testid="stDataFrameContainer"] table td,
.stDataFrame div[data-testid="stDataFrameContainer"] table th {
    border: 1px solid #0a58ca;
}
.stDataFrame div[data-testid="stDataFrameContainer"] table th {
    background-color: #e6f0ff;
    color: #0a58ca;
}
.block-container {
    padding: 0 2rem;
    background-color: #eef5ff;
}

/* Topbar */
.topbar {
    background-color: #0a58ca;
    padding: 14px 20px;
    border-radius: 10px;
    color: white;
    margin-bottom: 20px;
}

/* Selectbox border */
.css-1v3fvcr input,
.stSelectbox div[role="combobox"] input {
    border: 2px solid #0a58ca !important;
    border-radius: 8px;
    padding: 6px;
}
            

            
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown("""
<div class="topbar">
    <h2>🌍 Blue Planet Infosolutions Pvt. Ltd.</h2>
    <p>Intern Task Dashboard</p>
</div>
""", unsafe_allow_html=True)

# ---------------- LOAD DATA ----------------
try:
    df = pd.read_csv("https://docs.google.com/spreadsheets/d/1zPkZg6lNEnHDySAIHUBAB8xFbZ7dM7MKN-mlSV8AKnY/export?format=csv")
    # df2 = pd.read_csv("https://docs.google.com/spreadsheets/d/1wutMpP4n_6cFW2V2FnQKef5DQ_cfgUG3yZXE6hwNXCA/export?format=csv")

    # df = pd.concat([df1, df2], ignore_index=True)

except:
    st.error("Error loading file")
    st.stop()

df = df.iloc[:, 1:] 

if 'Date' not in df.columns or 'Intern Name' not in df.columns:
    st.error("Missing required columns")
    st.stop()

# ---------------- CLEAN ----------------
df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
df = df.dropna(subset=['Date'])

# IST date (DO NOT CHANGE - as per your instruction)
today = pd.Timestamp.now(tz="Asia/Kolkata").date()

df['Date'] = df['Date'].dt.tz_localize(None)
df = df[df['Date'].dt.date <= today]        
df = df.sort_values("Date")


# ---------------- FILTER CARD ----------------
intern_links = {
    "AT": "https://docs.google.com/spreadsheets/d/xxxxx",
    "Rahul": "https://docs.google.com/spreadsheets/d/yyyyy",
    "Harshada Magar": "https://docs.google.com/spreadsheets/d/14m3yRqwbPmHpWmgYxP9RnudDsHPgA3ki0vKeZLUyYwU/edit?usp=sharing",
    "Sreeja M":"https://docs.google.com/spreadsheets/d/1xOBQkgZMIYjQuHNTttOW1CTLn86j4fRzS7znODu0WHE/edit?usp=sharing",
    "Devatha Siri":"https://docs.google.com/spreadsheets/d/1saAd0onz12WhMpnCckIqy2tHdVXHst7SvK7y-Ep0gyM/edit?hl=id&gid=0#gid=0",
    "H. Lahari":"https://docs.google.com/spreadsheets/d/19Ugy_pFKaPZgzKjEiHHhMmBvKFx-Mjf1ixnbOe0QfA4/edit?gid=0#gid=0",
}
# ---------------- FILTER CARD ----------------

st.markdown("""
<style>

/* ---------- SECTION HEADER ---------- */
.section {
    font-size: 22px;
    font-weight: 700;
    color: #111827;
    margin-bottom: 14px;
    padding-bottom: 8   px;
    border-bottom: 2px solid #e5e7eb;
}

/* ---------- LABEL ---------- */
label {
    font-size: 14px !important;
    font-weight: 600 !important;
    color: #374151 !important;
}

/* ---------- SELECTBOX ---------- */
div[data-baseweb="select"] > div {
    background: #ffffff !important;
    border: 1px solid #d1d5db !important;
    border-radius: 10px !important;
    min-height: 48px !important;
    box-shadow: none !important;
    transition: all 0.2s ease !important;

    font-size: 20px !important;   /* change size here */
    font-weight: 600 !important;  /* optional */
    font-family: 'Fira Code', monospace;
}
/* ---------- HOVER ---------- */
div[data-baseweb="select"] > div:hover {
    border-color: #9ca3af !important;
}

/* ---------- FOCUS ---------- */
div[data-baseweb="select"]:focus-within > div {
    border-color: #2563eb !important;
    box-shadow: 0 0 0 2px rgba(37, 99, 235, 0.12) !important;
}

/* ---------- TEXT ---------- */
div[data-baseweb="select"] span {
    color: #111827 !important;
    font-size: 14px !important;
    font-weight: 500 !important;
}

</style>
""", unsafe_allow_html=True)

# ---------- FILTER HEADER ----------
st.markdown(
    '<div class="section">Filters</div>',
    unsafe_allow_html=True
)

# ---------- FILTERS ----------
f1, f2 = st.columns([2, 2])

with f1:
    intern = st.selectbox(
        "Select Intern",
        sorted(df['Intern Name'].unique(), reverse=True)
    )

# ---------- FILTERED DATA ----------
intern_df = df[df['Intern Name'] == intern].sort_values(
    by='Intern Name',
    ascending=False
)

sheet_task_count = 0

sheet_url = intern_links.get(intern.strip())

if sheet_url and "xxxxx" not in sheet_url and "yyyyy" not in sheet_url:

    try:
        # Extract Sheet ID
        sheet_id = sheet_url.split("/d/")[1].split("/")[0]

        # CSV Export URL
        csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"

        # Read Sheet Data
        intern_sheet_df = pd.read_csv(csv_url)

        # Count rows/tasks
        sheet_task_count = len(intern_sheet_df)

    except:
        sheet_task_count = 0




# ---------------- DATE ----------------
default_date = today

with f2:
    selected_date = st.date_input("Select Date", value=default_date)

# ---------------- KPI SECTION ----------------
st.markdown('<div class="section">📊 Overview</div>', unsafe_allow_html=True)

k1, k2, k3 ,k4= st.columns(4)

task_count = len(intern_df)
today_tasks = len(intern_df[intern_df['Date'].dt.date == today])
active_days = intern_df['Date'].dt.date.nunique()

with k1:
    st.markdown(f"""
    <div class="kpi">
        <h1>{task_count}</h1>
        <p>Total Tasks</p>
    </div>
    """, unsafe_allow_html=True)

with k2:
    st.markdown(f"""
    <div class="kpi">
        <h1>{today_tasks}</h1>
        <p>Today's Tasks</p>
    </div>
    """, unsafe_allow_html=True)

with k4:
    st.markdown(f"""
    <div class="kpi">
        <h1>{active_days}</h1>
        <p>Active Days</p>
    </div>
    """, unsafe_allow_html=True)

with k3:
    st.markdown(f"""
    <div class="kpi">
        <h1>{sheet_task_count}</h1>
        <p>Total Clubs Collected</p>
    </div>
    """, unsafe_allow_html=True)

# ---------------- TABLE ----------------
st.markdown('<div class="section">📋 Task Details</div>', unsafe_allow_html=True)

result = intern_df[intern_df['Date'].dt.date == selected_date]

if not result.empty:
    st.dataframe(result, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

else:
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #f59e0b, #fbbf24);
        padding: 14px;
        border-radius: 12px;
        color: white;
        font-size: 16px;
        font-weight: 600;
        text-align: center;
        box-shadow: 0 4px 10px rgba(251, 191, 36, 0.3);
    ">
        ⚠️ No tasks found
    </div>
    """, unsafe_allow_html=True)
    st.markdown("")



# ---------------- FOOTER ----------------
# ---------------- CLEAN INTERN NAMES ----------------
df['Intern Name'] = df['Intern Name'].astype(str).str.strip()

# ---------------- INTERN SHEET LINKS ----------------


# ---------------- GET SELECTED INTERN LINK ----------------
sheet_link = intern_links.get(intern.strip())

# ---------------- FOOTER ----------------
c1, c2 = st.columns(2)

with c1:
    if sheet_link:
        st.link_button(
            "📊 Open Your Data Sheet",
            sheet_link,
            use_container_width=True
        )

        st.markdown("""
        <style> 
        div.stLinkButton > a {
            background-color: #2563eb !important;
            color: white !important;
            border-radius: 12px !important;
            padding: 12px 20px !important;
            font-size: 16px !important;
            font-weight: 600 !important;
            border: none !important;
            text-align: center !important;
        }

        div.stLinkButton > a:hover {
            background-color: #1d4ed8 !important;
            color: white !important;
        }
        </style>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
            <div style="
                background-color:#ff4b4b;
                padding:15px;
                border-radius:10px;
                color:white;
                font-weight:bold;
                text-align:center;
            ">
            ⚠️ Spreadsheet Not Submitted
            </div>
            """, unsafe_allow_html=True)
        
    st.markdown("")

with c2:
    st.link_button(
    "📝 Mark Attendance",
    "https://docs.google.com/forms/d/e/1FAIpQLScHz7fdRGl0RbMTyh_8N5VH9G0K1LDsszsZRqwHMe9CsXcqlA/viewform",
    use_container_width=True
)
    

st.markdown("""
<style>
div.stLinkButton > a {
    background: linear-gradient(135deg, #16a34a, #22c55e) !important;
    color: white !important;
    border-radius: 14px !important;
    padding: 14px 22px !important;
    font-size: 17px !important;
    font-weight: 700 !important;
    border: none !important;
    text-align: center !important;
    box-shadow: 0 4px 12px rgba(34, 197, 94, 0.3) !important;
    transition: all 0.3s ease !important;
}

div.stLinkButton > a:hover {
    background: linear-gradient(135deg, #15803d, #16a34a) !important;
    transform: translateY(-2px) !important;
    color: white !important;
}
</style>
""", unsafe_allow_html=True)
# ---------------- Dropdown ----------------
# import pandas as pd
# import streamlit as st

sheet_url = intern_links.get(intern.strip())
if not sheet_url:
    st.error("Please enter a valid Google Sheet URL.")
    st.stop()

try:
    sheet_id = sheet_url.split("/d/")[1].split("/")[0]
    csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"

    intern_sheet_df = pd.read_csv(csv_url)

    # st.markdown("#### View Your Collected Data (Click your name 👇)")

    # with st.expander(f"📄 {intern} Sheet Data"):
    #     st.dataframe(intern_sheet_df, use_container_width=True)

except Exception as e:
    st.error("Failed to load sheet data.")
    st.exception(e)


# ---------------- INTERN SHEET DATA ----------------

sheet_url = intern_links.get(intern.strip())

if sheet_url and "xxxxx" not in sheet_url and "yyyyy" not in sheet_url:

    try:
        # Extract Sheet ID
        sheet_id = sheet_url.split("/d/")[1].split("/")[0]

        # CSV Export URL
        csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"

        # Read Sheet Data
        intern_sheet_df = pd.read_csv(csv_url)

        st.markdown("#### View Your Collected Data (Click your name 👇)")

        with st.expander(f"📄 {intern} Sheet Data"):

            st.dataframe(
                intern_sheet_df,
                use_container_width=True
            )

    except:
        st.error("Unable to load selected intern sheet")

else:
    st.warning("No valid sheet link available")
    
filtered = intern_df[
    intern_df['Date'].dt.date == selected_date
]['Institute Name'].dropna()

if filtered.empty:
    st.warning("No Institute Name found for selected date.")
    value = ""
else:
    value = filtered.iloc[0]

prompt_df = pd.DataFrame([[value]], columns=["Institute Name"])

with st.expander("Prompt Builder"):
    col1, col2, col3, col4, col5 = st.columns(5)

    cols = [col1, col2, col3, col4, col5]

    for i, inst in enumerate(filtered):
        col = cols[i % 5]

        with col:
            if st.button(inst, key=f"btn_{i}"):
                 prompt = f"""You are a web research agent with live browsing access.
Your ONLY job: find every student club, committee, cell,
association, and organization at {inst} and output a table.

NO explanations. NO excuses. NO asking for more info.
If a field is not found, leave it blank. Start the table immediately.

════════════════════════════════
STEP 1 — SEARCH (do this silently)
════════════════════════════════
Search the web for ALL of the following one by one:
- "{inst} student clubs"
- "{inst} student organizations"
- "{inst} technical clubs"
- "{inst} cultural clubs"
- "{inst} NSS NCC"
- "{inst} IEEE ISTE CSI ACM chapter"
- "{inst} entrepreneurship cell innovation cell"
- "{inst} coding club robotics club"
- "{inst} dance music drama club"
- "{inst} photography literary club"
- "{inst} placement committee student council"
- "{inst} women development cell"
- "{inst} environment club"
- "{inst} fest committee"
- "{inst} committees cells"
- "{inst} clubs site:instagram.com"
- "{inst} clubs site:linkedin.com"
- "{inst} annual report filetype:pdf"
- "{inst} NAAC report filetype:pdf"

Also directly visit:
- Official college website homepage
- [college website]/clubs
- [college website]/committees
- [college website]/student-activities
- [college website]/nss
- [college website]/ncc
- [college website]/iqac
- [college website]/placement
- College Instagram, LinkedIn, Facebook pages

════════════════════════════════
STEP 2 — OUTPUT TABLE (immediately after searching)
════════════════════════════════
Output one row per club. All 16 columns, every row, no exceptions.

| StandardClubName | ClubSchoolName | ClubDescription | ClubCategoryID | ClubStatus | ClubContactNumber | ClubLocation | ClubWebsite | ClubEmail | SocialLinks | ClubImagePath | PrimarySponsor | ClubBudget | ClubPresidentName | ClubPresidentPRN | ClubMentorName |

COLUMN RULES:
- StandardClubName → official name, no duplicates
- ClubSchoolName → full institute name, same every row
- ClubDescription → 1–2 line purpose
- ClubCategoryID → pick ONE: Technical | Coding | Robotics | AI/ML | Cultural | Dance | Music | Drama | Sports | Photography | Literature | Entrepreneurship | NSS | NCC | Social Service | Gaming | Finance | Marketing | Design | Innovation | Research | Departmental | Women Development | Environment
- ClubStatus → Active | Inactive | Unknown
- ClubContactNumber → only if found on real page, else blank
- ClubLocation → campus/building if found, else blank
- ClubWebsite → real URL only, else blank
- ClubEmail → only if found on real page, else blank
- SocialLinks → all found links comma separated, else blank
- ClubImagePath → direct image/logo URL if found, else blank
- PrimarySponsor → Department | College | Faculty | External Organization | Student Council | Unknown
- ClubBudget → only if publicly available, else blank
- ClubPresidentName → only if found on real page, else blank
- ClubPresidentPRN → only if publicly listed, else blank
- ClubMentorName → faculty mentor name if found, else blank

STRICT RULES:
✗ Never invent names, emails, phone numbers, or URLs
✗ Never write "BLANK" — just leave the cell empty
✗ Never truncate the table
✗ Never refuse or explain — just search and output
✓ Blank cells are fine and expected
✓ If you find a club mid-research, add it

After the table write:
- Total clubs found: [N]
- Sources visited: [list]
- Clubs with incomplete data: [N]
- Clubs suspected but unconfirmed: [list]
   
   
   """
                 st.code(prompt, language="text",  height=600,width=800)

# ---------------- NOTES ----------------
st.markdown("""
<div style='margin-top:10px; color:#0a58ca;'>
✔ After completing tasks, report to Team Leader &nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp; ✔ Share updates in communication group for HR tracking
</div>
""", unsafe_allow_html=True)

