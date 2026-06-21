import streamlit as st
import pandas as pd
from datetime import datetime
import pickle

# ── PAGE CONFIG ──────────────────────────────────────────────────────────────
st.set_page_config(page_title="Blue Planet Dashboard", layout="wide")

# ── GLOBAL CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
#MainMenu,footer,header{visibility:hidden;}
.block-container{padding:0 2rem 3rem !important;margin-top:0 !important;background:#eef3fb;max-width:100% !important;}

.topbar{
    background:linear-gradient(135deg, #0C4A6E, #06B6D4) !important;
    padding:14px 28px;
    display:flex;
    align-items:center;
    gap:14px;
    margin-bottom:24px;
    border-radius:0 0 14px 14px;
}
.topbar h2{margin:0;font-size:33px;font-weight:800;color:#fff;}
.topbar p{margin:2px 0 0;font-size:12px;color:#90caf9;text-transform:uppercase;letter-spacing:.05em;}
.topbar-badge{margin-left:auto;background:rgba(255,255,255,.15);color:#fff;font-size:11px;font-weight:700;padding:4px 12px;border-radius:20px;}

.sh{font-size:13px;font-weight:800;color:#0d47a1;text-transform:uppercase;letter-spacing:.08em;margin:22px 0 10px;padding:0 0 8px;border-bottom:2px solid #c5d8f7;}

.kpi{background:#fff;border-radius:14px;padding:22px 18px;text-align:center;border:1px solid #dce8f9;border-top:4px solid #0d47a1;box-shadow:0 2px 8px rgba(13,71,161,.06);}
.kpi-val{font-size:42px;font-weight:900;line-height:1;color:#0d47a1;margin-bottom:6px;}
.kpi-lbl{font-size:11px;font-weight:700;color:#78909c;text-transform:uppercase;letter-spacing:.07em;}
.kpi.green{border-top-color:#2e7d32;} .kpi.green .kpi-val{color:#2e7d32;}
.kpi.purple{border-top-color:#6a1b9a;} .kpi.purple .kpi-val{color:#6a1b9a;}
.kpi.amber{border-top-color:#bf360c;} .kpi.amber .kpi-val{color:#bf360c;}

div.stLinkButton a{display:block;width:100%;text-align:center;padding:13px 20px !important;border-radius:10px !important;font-size:15px !important;font-weight:700 !important;text-decoration:none !important;color:#fff !important;background:#0d47a1 !important;border:none !important;transition:filter .18s,transform .15s !important;}
div.stLinkButton a:hover{filter:brightness(1.12) !important;transform:translateY(-1px) !important;color:#fff !important;}
[data-testid="column"]:last-child div.stLinkButton a{background:#2e7d32 !important;}

[data-testid="stDataFrame"]{border-radius:12px;overflow:hidden;border:1.5px solid #b0c8f0 !important;}
[data-testid="stDataFrameContainer"] th{background:#dce8f9 !important;color:#0d47a1 !important;font-weight:800 !important;font-size:12px !important;padding:10px 12px !important;border-bottom:2px solid #90b4e8 !important;}
[data-testid="stDataFrameContainer"] td{font-size:13px !important;padding:9px 12px !important;border-bottom:1px solid #edf2fb !important;}
[data-testid="stDataFrameContainer"] tr:nth-child(even) td{background:#f5f8fe !important;}

div[data-baseweb="select"]>div{background:#fff !important;border:1.5px solid #b0c8f0 !important;border-radius:10px !important;min-height:44px !important;box-shadow:none !important;}
div[data-baseweb="select"]:focus-within>div{border-color:#0d47a1 !important;box-shadow:0 0 0 3px rgba(13,71,161,.1) !important;}

.no-sheet{background:#fce4ec;border:1.5px solid #f48fb1;color:#880e4f;padding:13px 18px;border-radius:10px;font-weight:700;text-align:center;}
.empty-state{background:#fff8e1;border:1.5px solid #ffe082;color:#bf360c;padding:14px;border-radius:10px;font-weight:700;text-align:center;}
.footer-note{margin-top:20px;padding:11px 16px;border-radius:10px;background:#dce8f9;color:#0d47a1;font-size:12px;font-weight:600;display:flex;gap:20px;}
[data-testid="stExpander"]{border:1.5px solid #0d47a1 !important;border-radius:10px !important;}</style>
""", unsafe_allow_html=True)


# ── TOPBAR ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="topbar">
    <span class="topbar-icon"></span>
    <div><h2>Blue Planet Infosolutions Pvt. Ltd.</h2><p>Intern Task Dashboard</p></div>
   
</div>
""", unsafe_allow_html=True)


# ── LOAD DATA ────────────────────────────────────────────────────────────────
MAIN_SHEET = "https://docs.google.com/spreadsheets/d/1zPkZg6lNEnHDySAIHUBAB8xFbZ7dM7MKN-mlSV8AKnY/export?format=csv"

try:
    with open("data.pkl", "rb") as f:
        df = pickle.load(f)
except Exception as e:
    st.error(f"❌ Error loading data: {e}")
    st.stop()

df = df.iloc[:, 1:]

if 'Date' not in df.columns or 'Intern Name' not in df.columns:
    st.error("Missing required columns: 'Date' or 'Intern Name'")
    st.stop()

df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
df = df.dropna(subset=['Date'])

today = pd.Timestamp.now(tz="Asia/Kolkata").date()
df['Date'] = df['Date'].dt.tz_localize(None)
df = df[df['Date'].dt.date <= today].sort_values("Date")
df['Day'] = df['Date'].dt.strftime('%A')
df['Intern Name'] = df['Intern Name'].astype(str).str.strip()


# ── INTERN SHEET LINKS ───────────────────────────────────────────────────────
intern_links = {
    "AT":             "https://docs.google.com/spreadsheets/d/xxxxx",
    "Rahul":          "https://docs.google.com/spreadsheets/d/yyyyy",
    "Harshada Magar": "https://docs.google.com/spreadsheets/d/14m3yRqwbPmHpWmgYxP9RnudDsHPgA3ki0vKeZLUyYwU/edit?usp=sharing",
    "Sreeja M":       "https://docs.google.com/spreadsheets/d/1xOBQkgZMIYjQuHNTttOW1CTLn86j4fRzS7znODu0WHE/edit?usp=sharing",
    "Devatha Siri":   "https://docs.google.com/spreadsheets/d/1saAd0onz12WhMpnCckIqy2tHdVXHst7SvK7y-Ep0gyM/edit?hl=id&gid=0#gid=0",
    "H. Lahari":      "https://docs.google.com/spreadsheets/d/19Ugy_pFKaPZgzKjEiHHhMmBvKFx-Mjf1ixnbOe0QfA4/edit?gid=0#gid=0",
    "Nasiya": "https://docs.google.com/spreadsheets/d/1kPQSAkEn07XLkSlWXmWTkvuFKdZWWKrwi8f5Yy1_aPA/edit?usp=sharing",
    "Zahid": "https://docs.google.com/spreadsheets/d/17VHHSF3oeCxTxUHzrYw77CwJkMt2L_qoUmUR1nk49b0/edit?usp=sharing",
    "Swetha":"https://docs.google.com/spreadsheets/d/1D5nWF-vhN155aZkPfYu2wXGetA4PAdwnjPvpRC5Pom4/edit?usp=sharing",
    "Riya":"https://docs.google.com/spreadsheets/d/1BmGbpYnwOlw6Vjx0voFa4WzIVHvC_-tC5cmuLCXfzck/edit?usp=sharing",
    "Kalyani":"https://docs.google.com/spreadsheets/d/1XgENzr4GJptLUpJTU3qVRITfIaTf1mU5uiy2D7Oxlrw/edit?gid=0#gid=0",
    "Saanvi":"https://docs.google.com/spreadsheets/d/1X1hhc0USSr2X-Mg1QDBNosRm8Fygy0nuV0uVWVjISOw/edit?gid=0#gid=0",
    "Zainab":"https://docs.google.com/spreadsheets/d/1WgOGMKu-cEXd2Bl7d2xTtAPd5ZzLF43G6B514RWNlxg/edit?gid=0#gid=0",
    "Abishek":"https://docs.google.com/spreadsheets/d/1NxjGAuZWVqTlCESNrpTwtAicR2UMECblC_neev3TXTY/edit?gid=0#gid=0",
    "Khushi":"https://docs.google.com/spreadsheets/d/1tKHaXIawLgRxwsV1PBDcogDGONV64a2AcNrSIZ45kXY/edit?gid=0#gid=0",
}

def is_valid_link(url):
    return url and "xxxxx" not in url and "yyyyy" not in url

def sheet_csv_url(link):
    try:
        sid = link.split("/d/")[1].split("/")[0]
        return f"https://docs.google.com/spreadsheets/d/{sid}/export?format=csv"
    except Exception:
        return None

intern_ids = {
    "AT":             1,
    "Rahul":          2,
    "Harshada Magar": 3,
    "Sreeja M":       4,
    "Devatha Siri":   5,
    "H. Lahari":      6,
    "Nasiya":         7,
    "Zahid":          8,
    "Swetha":         9,
    "Riya":           10,
    "Kalyani":        11,
    "Saanvi":         12,
    "Zainab":         13,
    "Abishek":        14,
    "Khushi":         15,
}


# ── FILTERS ──────────────────────────────────────────────────────────────────
st.markdown('<div class="sh">🔍 &nbsp;Filters</div>', unsafe_allow_html=True)
f1, f2 = st.columns([2, 2])

with f1:
    intern = st.selectbox(
        "Select Intern",
        sorted(df['Intern Name'].unique()),
        label_visibility="visible"
    )

with f2:
    selected_date = st.date_input("Select Date", value=today)

intern_df = df[df['Intern Name'] == intern].sort_values('Date')

# ── MERGE CLUBS COUNT INTO TASK TABLE ────────────────────────────────────────
if is_valid_link(intern_links.get(intern.strip(), "")):
    csv_url = sheet_csv_url(intern_links.get(intern.strip(), ""))
    if csv_url:
        try:
            _idf = pd.read_csv(csv_url)
            _idf['SchoolID'] = _idf['SchoolID'].astype(str).str.strip()
            clubs_count = _idf.groupby('SchoolID').size().reset_index(name='Clubs Collected')
            intern_df = intern_df.copy()
            intern_df['SchoolID'] = intern_df['SchoolID'].astype(str).str.strip()
            intern_df = intern_df.merge(clubs_count, on='SchoolID', how='left')
            intern_df['Clubs Collected'] = intern_df['Clubs Collected'].fillna(0).astype(int)
        except Exception:
            intern_df['Clubs Collected'] = 0
else:
    intern_df['Clubs Collected'] = 0


# ── CLUB COUNT ───────────────────────────────────────────────────────────────
sheet_task_count = 0
sheet_url = intern_links.get(intern.strip(), "")

if is_valid_link(sheet_url):
    csv_url = sheet_csv_url(sheet_url)
    if csv_url:
        try:
            intern_sheet_df = pd.read_csv(csv_url)
            sheet_task_count = len(intern_sheet_df)
        except Exception:
            sheet_task_count = 0


# ── KPIs ─────────────────────────────────────────────────────────────────────
st.markdown('<div class="sh">📊 &nbsp;Overview</div>', unsafe_allow_html=True)

task_count  = len(intern_df)
today_tasks = len(intern_df[intern_df['Date'].dt.date == today])
active_days = intern_df['Date'].dt.date.nunique()

k1, k2, k3, k4 = st.columns(4)
with k1:
    st.markdown(f'<div class="kpi blue"><div class="kpi-val">{task_count}</div><div class="kpi-lbl">Total Tasks</div></div>', unsafe_allow_html=True)
with k2:
    st.markdown(f'<div class="kpi green"><div class="kpi-val">{today_tasks}</div><div class="kpi-lbl">Today\'s Tasks</div></div>', unsafe_allow_html=True)
with k3:
    st.markdown(f'<div class="kpi purple"><div class="kpi-val">{sheet_task_count}</div><div class="kpi-lbl">Total Clubs Collected</div></div>', unsafe_allow_html=True)
with k4:
    st.markdown(f'<div class="kpi amber"><div class="kpi-val">{active_days}</div><div class="kpi-lbl">Active Days</div></div>', unsafe_allow_html=True)


# ── TASK TABLE ───────────────────────────────────────────────────────────────
st.markdown('<div class="sh">📋 &nbsp;Task Details</div>', unsafe_allow_html=True)

day_result = intern_df[intern_df['Date'].dt.date == selected_date]

if not day_result.empty:
    display_result = day_result.copy()
    display_result['Date'] = display_result['Date'].dt.strftime('%d-%b-%Y')
    st.dataframe(display_result, use_container_width=True, hide_index=True)
else:
    st.markdown(
        '<div class="empty-state">⚠️ No tasks found for the selected date</div>',
        unsafe_allow_html=True
    )


# ── ACTION BUTTONS ───────────────────────────────────────────────────────────
st.markdown('<div class="sh">🔗 &nbsp;Quick Actions</div>', unsafe_allow_html=True)

c1, c2 = st.columns(2)
with c1:
    if is_valid_link(sheet_url):
            st.link_button("📊 Open Your Data Sheet", sheet_url, use_container_width=True)
    else:
        st.markdown('<div class="no-sheet">⚠️ Spreadsheet Not Submitted</div>', unsafe_allow_html=True)
with c2:
    st.link_button("📝 Mark Attendance", "https://docs.google.com/forms/d/e/1FAIpQLScHz7fdRGl0RbMTyh_8N5VH9G0K1LDsszsZRqwHMe9CsXcqlA/viewform", use_container_width=True)


# ── INTERN SHEET DATA ────────────────────────────────────────────────────────
if is_valid_link(sheet_url):
    csv_url = sheet_csv_url(sheet_url)
    if csv_url:
        st.markdown('<div class="sh">📂 &nbsp;Collected Data</div>', unsafe_allow_html=True)
        with st.expander(f"📄 View {intern}'s Sheet"):
            try:
                intern_sheet_df = pd.read_csv(csv_url)
                st.dataframe(intern_sheet_df, use_container_width=True, hide_index=True)
            except Exception:
                st.error("Unable to load sheet data.")

intern_id = intern_ids.get(intern.strip(), "")
# ── PROMPT BUILDER ───────────────────────────────────────────────────────────
st.markdown('<div class="sh">🧠 &nbsp;Prompt Builder</div>', unsafe_allow_html=True)

institutes = day_result[['Institute Name','SchoolID']].dropna(subset=['Institute Name']).drop_duplicates().values.tolist() if not day_result.empty else []
with st.expander("Click an institute to generate a research prompt"):
    if not institutes:
        st.warning("No institute names found for the selected date.")
    else:
        cols = st.columns(min(len(institutes), 5))
        for i, (inst, school_id) in enumerate(institutes):
            with cols[i % 5]:
                if st.button(f"🏫 {inst}", key=f"pb_{i}", use_container_width=True):
                    prompt = f"""You are a web research agent with live browsing access.

Your ONLY job: find every student club, committee, cell,

association, and organization at {inst} and output a table.

NO explanations. NO excuses. NO asking for more info.

If a field is not found, leave it blank. Start the table immediately.

════════════════════════════════

STEP 1 — SEARCH (do this silently)

════════════════════════════════

Search the web for ALL of the following one by one:

"{inst} student clubs"
"{inst} student organizations"
"{inst} technical clubs"
"{inst} cultural clubs"
"{inst} NSS NCC"
"{inst} IEEE ISTE CSI ACM chapter"
"{inst} entrepreneurship cell innovation cell"
"{inst} coding club robotics club"
"{inst} dance music drama club"
"{inst} photography literary club"
"{inst} placement committee student council"
"{inst} women development cell"
"{inst} environment club"
"{inst} fest committee"
"{inst} committees cells"
"{inst} clubs site:instagram.com"
"{inst} clubs site:linkedin.com"
"{inst} annual report filetype:pdf"
"{inst} NAAC report filetype:pdf"

Also directly visit:
Official college website homepage
[college website]/clubs
[college website]/committees
[college website]/student-activities
[college website]/nss
[college website]/ncc

════════════════════════════════

STEP 2 — OUTPUT TABLE (immediately after searching)

════════════════════════════════

Output one row per club. All 25 columns, every row, no exceptions.

| GroupMemberID | SchoolID | ClubID | SchoolClubID | ClubName | ClubSchoolName | ClubDescription | ClubCategoryID | ClubStatus | ClubContactNumber | ClubLocation | ClubWebsite | ClubEmail | SocialLinks | ClubImagePath | PrimarySponsorID | PrimarySponsorName | ClubBudget | ClubPresidentID | ClubPresidentName | ClubPresidentPRN | ClubMentorID | ClubMentorName | DataCollectedByID | DataCollectedByName |
COLUMN RULES:

GroupMemberID → always set to 6
SchoolID → always set to {school_id}
ClubID → leave blank
SchoolClubID → generate using the initials of {inst} + a 3-digit sequential number padded with zeros.

INITIALS RULE: Take the first letter of each significant word in the college name (skip common words like "of", "and", "the", "for"). Then append 001, 002, 003… for each club.

Examples:

→ "Christian College of Engineering and Technology" → CCET001, CCET002, CCET003…

→ "Government Polytechnic Mungeli" → GPM001, GPM002, GPM003…

→ "Indian Institute of Technology Bombay" → IITB001, IITB002…

→ "Dr. Ambedkar Institute of Technology" → DAIT001, DAIT002…
ClubName → official full name of the club
ClubSchoolName → common short name or abbreviation
ClubDescription → one sentence describing the club's purpose
ClubCategoryID → use one of: Technical, Cultural, Social, Sports, Literary, Entrepreneurship, Professional, Other
ClubStatus → Active (default unless known otherwise)
ClubContactNumber → only if found; never invent
ClubLocation → college name and address
ClubWebsite → only if found; never invent
ClubEmail → only if found; never invent
SocialLinks → only if found; never invent
ClubImagePath → leave blank
PrimarySponsorID → leave blank
PrimarySponsorName → sponsoring body if known (e.g. Ministry of Youth Affairs, IEEE, AICTE)
ClubBudget → leave blank
ClubPresidentID → leave blank
ClubPresidentName → only if found; never invent
ClubPresidentPRN → only if found; never invent
ClubMentorID → leave blank
ClubMentorName → only if found; never invent
DataCollectedByID → always set to {intern_id}
DataCollectedByName → always set to {intern}

STRICT RULES:

✗ Never invent names, emails, phone numbers, or URLs

✗ Never write "BLANK" — just leave the cell empty

✗ Never truncate the table

✓ Blank cells are fine and expected
After the table write:

Total clubs found: [N]
Sources visited: [list]
Clubs with incomplete data: [N]
"""
                    st.components.v1.html(f"""
<textarea id="prompt-box" style="width:100%;height:200px;font-family:monospace;font-size:12px;padding:10px;border:1px solid #b0c8f0;border-radius:10px;resize:vertical;background:#f8faff;color:#1a1a2e">{prompt}</textarea>
<button onclick="
  navigator.clipboard.writeText(document.getElementById('prompt-box').value);
  this.textContent='✅ Copied!';
  this.style.background='#2e7d32';
  setTimeout(()=>{{this.textContent='📋 Copy Prompt';this.style.background='#0d47a1'}},2000)
" style="margin-top:8px;width:100%;padding:10px;background:#0d47a1;color:white;border:none;border-radius:8px;font-size:14px;font-weight:700;cursor:pointer">📋 Copy Prompt</button>
""", height=280)


# ── FOOTER NOTE ──────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer-note">
    <span>✔ After completing tasks, report to Team Leader</span>
    <span>✔ Share updates in communication group for HR tracking</span>
</div>
""", unsafe_allow_html=True)
