"""MINI-ERP - single-file Streamlit enterprise management system.
Run:  pip install streamlit pandas  &&  streamlit run app.py
"""
import streamlit as st
import pandas as pd
from datetime import date, datetime
 
st.set_page_config(page_title="MINI-ERP", layout="wide", initial_sidebar_state="expanded")
 
# ---------------------------------------------------------------- THEME
CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@500;700;900&family=Inter:wght@300;400;500;600&family=Cairo:wght@400;600;700&display=swap');
:root{--bg:#050409;--v1:#7c3aed;--v2:#9333ea;--ink:#ede9fe;--mute:#a79bc9;--glass:rgba(124,58,237,.08);--line:rgba(147,51,234,.28)}
html,body,.stApp{background:radial-gradient(1200px 600px at 80% -10%,rgba(124,58,237,.22),transparent 60%),
 radial-gradient(900px 500px at -10% 110%,rgba(147,51,234,.16),transparent 60%),var(--bg)!important;
 color:var(--ink);font-family:'Inter','Cairo',sans-serif}
header[data-testid="stHeader"]{background:transparent}
.block-container{padding-top:2rem;max-width:1250px}
h1,h2,h3{font-family:'Cinzel','Cairo',serif!important;letter-spacing:.04em;color:var(--ink)}
p,label,span,div,li{font-family:'Inter','Cairo',sans-serif}
section[data-testid="stSidebar"]{background:linear-gradient(180deg,#0a0714,#050409);border-right:1px solid var(--line)}
.brand{font-family:'Cinzel',serif;font-weight:900;font-size:1.7rem;letter-spacing:.18em;
 background:linear-gradient(90deg,#c4b5fd,#9333ea);-webkit-background-clip:text;-webkit-text-fill-color:transparent}
.company{color:var(--mute);font-size:.85rem;margin-bottom:1rem}
.glass{background:var(--glass);border:1px solid var(--line);border-radius:16px;padding:1.2rem 1.4rem;
 backdrop-filter:blur(14px);-webkit-backdrop-filter:blur(14px);box-shadow:0 8px 32px rgba(0,0,0,.45)}
.kpi{direction:rtl;text-align:right}
.kpi .l{color:var(--mute);font-size:.8rem;font-family:'Cairo',sans-serif}
.kpi .v{font-family:'Cinzel',serif;font-size:1.7rem;font-weight:700;color:#e9d5ff}
.page-title{direction:rtl;text-align:right;font-family:'Cairo',sans-serif!important;font-weight:700;font-size:1.9rem;
 border-bottom:1px solid var(--line);padding-bottom:.6rem;margin-bottom:1.2rem}
.rtl{direction:rtl;text-align:right;font-family:'Cairo',sans-serif}
.stButton>button,.stFormSubmitButton>button,.stDownloadButton>button{background:linear-gradient(135deg,#7c3aed,#9333ea);color:#fff;
 border:0;border-radius:10px;padding:.6rem 1.4rem;font-weight:600;font-family:'Cairo','Inter',sans-serif;transition:.25s}
.stButton>button:hover,.stFormSubmitButton>button:hover,.stDownloadButton>button:hover{box-shadow:0 0 24px rgba(147,51,234,.6);transform:translateY(-1px);color:#fff}
.stTextInput input,.stNumberInput input,.stTextArea textarea,div[data-baseweb="select"]>div{background:rgba(124,58,237,.07)!important;
 border:1px solid var(--line)!important;color:var(--ink)!important;border-radius:10px!important}
.stProgress>div>div>div>div{background:linear-gradient(90deg,#7c3aed,#c084fc)}
div[data-testid="stDataFrame"]{border:1px solid var(--line);border-radius:12px;overflow:hidden}
div[role="radiogroup"] label{background:transparent;border:1px solid transparent;border-radius:10px;padding:.35rem .7rem;direction:rtl;transition:.2s}
div[role="radiogroup"] label:hover{background:var(--glass);border-color:var(--line)}
div[role="radiogroup"] label>div:first-child{display:none}
.hero{min-height:56vh;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;
 animation:fadeIn 2.2s ease both}
.hero h1{font-size:clamp(2.6rem,8vw,5.5rem);font-weight:900;letter-spacing:.3em;margin:0;
 background:linear-gradient(90deg,#ddd6fe,#9333ea 55%,#7c3aed);-webkit-background-clip:text;-webkit-text-fill-color:transparent}
.hero p{max-width:640px;color:var(--mute);font-size:1.05rem;line-height:1.8;margin-top:1rem;font-family:'Cairo','Inter',sans-serif}
.rule{width:90px;height:2px;background:linear-gradient(90deg,transparent,#9333ea,transparent);margin:1.4rem auto;animation:grow 2.6s ease both}
.formwrap{animation:fadeIn 3s ease both}
@keyframes fadeIn{from{opacity:0;transform:translateY(14px)}to{opacity:1;transform:none}}
@keyframes grow{from{width:0}to{width:90px}}
@media (prefers-reduced-motion:reduce){*{animation:none!important}}
</style>
"""
HIDE_SIDEBAR = "<style>section[data-testid='stSidebar'],div[data-testid='collapsedControl']{display:none}</style>"
st.markdown(CSS, unsafe_allow_html=True)
 
# ---------------------------------------------------------------- STATE
INV_COLS = ["الصنف", "الكمية", "تكلفة الوحدة", "سعر البيع"]
 
 
def init_state():
    d = st.session_state
    d.setdefault("logged", False)
    d.setdefault("company", "")
    d.setdefault("email", "")
    d.setdefault("inv", pd.DataFrame(
        [["حاسوب محمول", 25, 18000.0, 22500.0], ["هاتف ذكي", 60, 7000.0, 9200.0],
         ["سماعات لاسلكية", 120, 600.0, 950.0], ["راوتر شبكات", 40, 1100.0, 1650.0]], columns=INV_COLS))
    d.setdefault("purchases", pd.DataFrame(columns=["التاريخ", "الصنف", "الكمية", "تكلفة الوحدة", "الإجمالي", "المورد"]))
    d.setdefault("sales", pd.DataFrame(columns=["التاريخ", "العميل", "الصنف", "الكمية", "سعر البيع", "الإيراد", "التكلفة"]))
    d.setdefault("production", pd.DataFrame(columns=["التاريخ", "المنتج", "المخطط", "المنتج فعليا", "الكفاءة %"]))
    d.setdefault("board", pd.DataFrame(
        [["هدف الإيرادات السنوي", 5000000.0, 0.0, "قيد التنفيذ"], ["توسعة فرع جديد", 800000.0, 150000.0, "قيد الدراسة"],
         ["تطوير نظام المبيعات", 300000.0, 120000.0, "قيد التنفيذ"]],
        columns=["البند", "المستهدف", "المحقق", "الحالة"]))
    d.setdefault("docs", [])
    d.setdefault("marketing", pd.DataFrame(
        [["حملة البحث المدفوع", 40000.0, 168000.0, 52000, 640], ["إعلانات التواصل الاجتماعي", 25000.0, 70000.0, 98000, 410],
         ["البريد التسويقي", 6000.0, 27000.0, 18000, 150]],
        columns=["الحملة", "الإنفاق", "الإيراد المنسوب", "النقرات", "التحويلات"]))
    d.setdefault("crm", pd.DataFrame(
        [["Huawei", "تأخر توريد", "عالية", "مفتوحة"], ["Lenovo", "استفسار عن ضمان", "متوسطة", "قيد المعالجة"],
         ["Xiaomi", "طلب عرض سعر", "منخفضة", "مغلقة"]], columns=["العميل", "الموضوع", "الأولوية", "الحالة"]))
    d.setdefault("hr", pd.DataFrame(
        [["سلمى", "مديرة المبيعات", 22000.0, "نشط"], ["عبد الرحمن", "مسؤول المخزون", 15000.0, "نشط"]],
        columns=["الموظف", "الوظيفة", "الراتب الشهري", "الحالة"]))
    d.setdefault("pr", pd.DataFrame(
        [["مؤتمر الابتكار التقني", "فعالية", "2026-11-15", "مخطط"], ["بيان صحفي للإطلاق", "إعلام", "2026-10-30", "قيد الإعداد"]],
        columns=["النشاط", "النوع", "التاريخ", "الحالة"]))
 
 
init_state()
S = st.session_state
 
 
def clean_inv(df):
    df = df.copy()
    df["الصنف"] = df["الصنف"].astype(str).str.strip()
    df = df[(df["الصنف"] != "") & (df["الصنف"] != "None") & (df["الصنف"] != "nan")]
    for c in INV_COLS[1:]:
        df[c] = pd.to_numeric(df[c], errors="coerce").fillna(0)
    return df.reset_index(drop=True)
 
 
def money(x):
    return f"{x:,.0f}"
 
 
def kpi(col, label, value):
    col.markdown(f'<div class="glass kpi"><div class="l">{label}</div><div class="v">{value}</div></div>', unsafe_allow_html=True)
 
 
def title(t):
    st.markdown(f'<div class="page-title">{t}</div>', unsafe_allow_html=True)
 
 
def totals():
    inv, s, p = S.inv, S.sales, S.purchases
    revenue = float(s["الإيراد"].sum()) if len(s) else 0.0
    cogs = float(s["التكلفة"].sum()) if len(s) else 0.0
    purchases = float(p["الإجمالي"].sum()) if len(p) else 0.0
    salaries = float(S.hr.loc[S.hr["الحالة"] == "نشط", "الراتب الشهري"].sum())
    ads = float(S.marketing["الإنفاق"].sum())
    stock_val = float((inv["الكمية"] * inv["تكلفة الوحدة"]).sum())
    profit = revenue - cogs - salaries - ads
    return dict(revenue=revenue, cogs=cogs, purchases=purchases, salaries=salaries, ads=ads, stock_val=stock_val, profit=profit)
 
 
# ---------------------------------------------------------------- LANDING
def landing():
    st.markdown(HIDE_SIDEBAR, unsafe_allow_html=True)
    st.markdown("""<div class="hero"><h1>MINI-ERP</h1><div class="rule"></div>
    <p>منصة متكاملة لإدارة المؤسسات: مخزون ومبيعات ومشتريات وإنتاج وموارد بشرية وتقارير مالية لحظية، في نظام واحد أنيق وسريع.</p></div>""",
                unsafe_allow_html=True)
    _, mid, _ = st.columns([1, 1.4, 1])
    with mid:
        st.markdown('<div class="formwrap">', unsafe_allow_html=True)
        with st.form("onboard"):
            email = st.text_input("البريد الإلكتروني الإداري", placeholder="admin@company.com")
            comp = st.text_input("اسم الشركة أو المحل", placeholder="اسم المنشأة")
            ok = st.form_submit_button("ابدأ بشكل مجاني", use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
        if ok:
            if "@" not in email or "." not in email.split("@")[-1]:
                st.error("أدخل بريدا إلكترونيا صحيحا.")
            elif not comp.strip():
                st.error("أدخل اسم الشركة أو المحل.")
            else:
                S.email, S.company, S.logged = email.strip(), comp.strip(), True
                st.rerun()
 
 
# ---------------------------------------------------------------- MODULES
def board():
    title("مجلس الإدارة")
    t = totals()
    c = st.columns(4)
    kpi(c[0], "الإيرادات", money(t["revenue"]))
    kpi(c[1], "صافي الربح", money(t["profit"]))
    kpi(c[2], "قيمة المخزون", money(t["stock_val"]))
    kpi(c[3], "عدد الموظفين", len(S.hr))
    st.markdown("#### جدول الخطة الاستراتيجية (قابل للتعديل مباشرة)")
    ed = st.data_editor(S.board, num_rows="dynamic", use_container_width=True, key="ed_board",
                        column_config={"الحالة": st.column_config.SelectboxColumn(options=["قيد الدراسة", "قيد التنفيذ", "مكتمل", "متوقف"])})
    S.board = ed
    st.download_button("تنزيل الجدول (CSV)", ed.to_csv(index=False).encode("utf-8-sig"), "board_sheet.csv", "text/csv")
 
 
def legal():
    title("الشؤون القانونية والإدارية")
    tab1, tab2 = st.tabs(["محرر المستندات", "الأرشيف"])
    with tab1:
        name = st.text_input("عنوان المستند", key="doc_title")
        body = st.text_area("نص المستند", height=300, key="doc_body")
        c1, c2 = st.columns(2)
        if c1.button("حفظ في الأرشيف"):
            if name.strip() and body.strip():
                S.docs.append({"العنوان": name.strip(), "النص": body, "التاريخ": datetime.now().strftime("%Y-%m-%d %H:%M")})
                st.success("تم حفظ المستند.")
            else:
                st.warning("أدخل العنوان والنص قبل الحفظ.")
        html = (f"<html dir='rtl'><head><meta charset='utf-8'></head><body><h2>{name}</h2>"
                f"<p>{body.replace(chr(10), '<br>')}</p><hr><small>{S.company}</small></body></html>")
        c2.download_button("تنزيل بصيغة Word", html.encode("utf-8"), f"{name or 'document'}.doc", "application/msword")
    with tab2:
        if not S.docs:
            st.info("الأرشيف فارغ. احفظ مستندا من المحرر ليظهر هنا.")
        for i, d in enumerate(reversed(S.docs)):
            with st.expander(f'{d["العنوان"]}  |  {d["التاريخ"]}'):
                st.markdown(f'<div class="rtl">{d["النص"]}</div>'.replace("\n", "<br>"), unsafe_allow_html=True)
 
 
def inventory():
    title("إدارة المخزون")
    st.caption("أي تعديل هنا ينعكس فورا على المبيعات والمشتريات والحسابات.")
    ed = st.data_editor(S.inv, num_rows="dynamic", use_container_width=True, key="ed_inv",
                        column_config={"الكمية": st.column_config.NumberColumn(min_value=0, step=1),
                                       "تكلفة الوحدة": st.column_config.NumberColumn(min_value=0.0, format="%.2f"),
                                       "سعر البيع": st.column_config.NumberColumn(min_value=0.0, format="%.2f")})
    S.inv = clean_inv(ed)
    inv = S.inv
    c = st.columns(3)
    kpi(c[0], "عدد الأصناف", len(inv))
    kpi(c[1], "إجمالي الوحدات", money(inv["الكمية"].sum()))
    kpi(c[2], "قيمة المخزون بالتكلفة", money((inv["الكمية"] * inv["تكلفة الوحدة"]).sum()))
    low = inv[inv["الكمية"] < 20]
    if len(low):
        st.warning("أصناف منخفضة المخزون: " + "، ".join(low["الصنف"]))
 
 
def purchasing():
    title("المشتريات")
    inv = S.inv
    with st.form("po", clear_on_submit=True):
        c = st.columns(4)
        item = c[0].selectbox("الصنف", list(inv["الصنف"]) if len(inv) else [])
        qty = c[1].number_input("الكمية", min_value=1, value=10, step=1)
        cost = c[2].number_input("تكلفة الوحدة", min_value=0.0, value=100.0)
        sup = c[3].text_input("المورد")
        ok = st.form_submit_button("تسجيل أمر شراء")
    if ok and item:
        i = S.inv.index[S.inv["الصنف"] == item][0]
        old_q, old_c = S.inv.at[i, "الكمية"], S.inv.at[i, "تكلفة الوحدة"]
        S.inv.at[i, "تكلفة الوحدة"] = round((old_q * old_c + qty * cost) / (old_q + qty), 2)  # weighted average cost
        S.inv.at[i, "الكمية"] = old_q + qty
        row = {"التاريخ": date.today().isoformat(), "الصنف": item, "الكمية": qty, "تكلفة الوحدة": cost,
               "الإجمالي": qty * cost, "المورد": sup or "غير محدد"}
        S.purchases = pd.concat([S.purchases, pd.DataFrame([row])], ignore_index=True)
        st.success(f"تمت إضافة {qty} وحدة إلى مخزون: {item}")
    c = st.columns(2)
    kpi(c[0], "إجمالي المشتريات", money(S.purchases["الإجمالي"].sum() if len(S.purchases) else 0))
    kpi(c[1], "عدد الأوامر", len(S.purchases))
    st.markdown("#### سجل المشتريات")
    st.dataframe(S.purchases, use_container_width=True, hide_index=True)
 
 
def production():
    title("الإنتاج والتصنيع")
    with st.form("prod", clear_on_submit=True):
        c = st.columns(3)
        item = c[0].selectbox("المنتج", list(S.inv["الصنف"]) if len(S.inv) else [])
        plan = c[1].number_input("الكمية المخططة", min_value=1, value=100, step=1)
        done = c[2].number_input("الكمية المنتجة فعليا", min_value=0, value=90, step=1)
        ok = st.form_submit_button("تسجيل دفعة إنتاج")
    if ok and item:
        eff = round(min(done / plan, 1.0) * 100, 1)
        i = S.inv.index[S.inv["الصنف"] == item][0]
        S.inv.at[i, "الكمية"] += done
        row = {"التاريخ": date.today().isoformat(), "المنتج": item, "المخطط": plan, "المنتج فعليا": done, "الكفاءة %": eff}
        S.production = pd.concat([S.production, pd.DataFrame([row])], ignore_index=True)
        st.success("تم تسجيل الدفعة وإضافة الكمية المنتجة إلى المخزون.")
    p = S.production
    avg = float(p["الكفاءة %"].mean()) if len(p) else 0.0
    st.markdown(f'<div class="rtl">متوسط كفاءة الإنتاج: {avg:.1f}%</div>', unsafe_allow_html=True)
    st.progress(min(avg / 100, 1.0))
    for _, r in p.tail(5).iterrows():
        st.markdown(f'<div class="rtl">{r["المنتج"]} ({r["التاريخ"]}) - {r["الكفاءة %"]}%</div>', unsafe_allow_html=True)
        st.progress(min(float(r["الكفاءة %"]) / 100, 1.0))
    st.dataframe(p, use_container_width=True, hide_index=True)
 
 
def pos():
    title("المبيعات ونقاط البيع")
    inv = S.inv[S.inv["الكمية"] > 0]
    if inv.empty:
        st.info("لا توجد أصناف متاحة في المخزون.")
    else:
        with st.form("pos", clear_on_submit=True):
            c = st.columns(3)
            item = c[0].selectbox("الصنف", list(inv["الصنف"]))
            qty = c[1].number_input("الكمية", min_value=1, value=1, step=1)
            cust = c[2].text_input("اسم العميل", value="عميل نقدي")
            ok = st.form_submit_button("إتمام عملية البيع")
        if ok:
            i = S.inv.index[S.inv["الصنف"] == item][0]
            stock = S.inv.at[i, "الكمية"]
            if qty > stock:
                st.error(f"الكمية المطلوبة ({qty}) أكبر من المتاح ({int(stock)}).")
            else:
                price, cost = S.inv.at[i, "سعر البيع"], S.inv.at[i, "تكلفة الوحدة"]
                S.inv.at[i, "الكمية"] = stock - qty  # real-time stock deduction
                row = {"التاريخ": datetime.now().strftime("%Y-%m-%d %H:%M"), "العميل": cust, "الصنف": item, "الكمية": qty,
                       "سعر البيع": price, "الإيراد": qty * price, "التكلفة": qty * cost}
                S.sales = pd.concat([S.sales, pd.DataFrame([row])], ignore_index=True)
                st.success(f"تمت العملية. إجمالي الفاتورة: {money(qty * price)}. المتبقي في المخزون: {int(stock - qty)}")
    c = st.columns(3)
    kpi(c[0], "إجمالي المبيعات", money(S.sales["الإيراد"].sum() if len(S.sales) else 0))
    kpi(c[1], "عدد العمليات", len(S.sales))
    kpi(c[2], "وحدات مباعة", money(S.sales["الكمية"].sum() if len(S.sales) else 0))
    st.markdown("#### المخزون الحالي")
    st.dataframe(S.inv, use_container_width=True, hide_index=True)
    st.markdown("#### سجل المبيعات")
    st.dataframe(S.sales, use_container_width=True, hide_index=True)
 
 
def marketing():
    title("التسويق")
    ed = st.data_editor(S.marketing, num_rows="dynamic", use_container_width=True, key="ed_mkt")
    S.marketing = ed
    sp, rv = float(ed["الإنفاق"].sum()), float(ed["الإيراد المنسوب"].sum())
    conv, clk = float(ed["التحويلات"].sum()), float(ed["النقرات"].sum())
    c = st.columns(4)
    kpi(c[0], "ROAS", f"{rv / sp:.2f}x" if sp else "0.00x")
    kpi(c[1], "تكلفة التحويل (CPA)", money(sp / conv) if conv else "0")
    kpi(c[2], "معدل التحويل", f"{conv / clk * 100:.2f}%" if clk else "0%")
    kpi(c[3], "إجمالي الإنفاق", money(sp))
    if len(ed):
        d = ed.set_index("الحملة")
        st.bar_chart((d["الإيراد المنسوب"] / d["الإنفاق"].replace(0, pd.NA)).astype(float).fillna(0), color="#9333ea")
 
 
def crm():
    title("خدمة العملاء")
    with st.form("tk", clear_on_submit=True):
        c = st.columns(4)
        cl = c[0].selectbox("العميل", ["Huawei", "Lenovo", "Xiaomi", "أخرى"])
        sub = c[1].text_input("الموضوع")
        pr = c[2].selectbox("الأولوية", ["منخفضة", "متوسطة", "عالية"])
        ok = c[3].form_submit_button("فتح تذكرة")
    if ok and sub.strip():
        S.crm = pd.concat([S.crm, pd.DataFrame([[cl, sub, pr, "مفتوحة"]], columns=S.crm.columns)], ignore_index=True)
    ed = st.data_editor(S.crm, num_rows="dynamic", use_container_width=True, key="ed_crm",
                        column_config={"الحالة": st.column_config.SelectboxColumn(options=["مفتوحة", "قيد المعالجة", "مغلقة"]),
                                       "الأولوية": st.column_config.SelectboxColumn(options=["منخفضة", "متوسطة", "عالية"])})
    S.crm = ed
    c = st.columns(3)
    kpi(c[0], "إجمالي التذاكر", len(ed))
    kpi(c[1], "مفتوحة", int((ed["الحالة"] == "مفتوحة").sum()))
    kpi(c[2], "نسبة الإغلاق", f"{(ed['الحالة'] == 'مغلقة').mean() * 100:.0f}%" if len(ed) else "0%")
 
 
def finance():
    title("الحسابات والمالية")
    t = totals()
    c = st.columns(4)
    kpi(c[0], "الإيرادات", money(t["revenue"]))
    kpi(c[1], "تكلفة البضاعة المباعة", money(t["cogs"]))
    kpi(c[2], "صافي الربح / الخسارة", money(t["profit"]))
    kpi(c[3], "قيمة المخزون", money(t["stock_val"]))
    st.markdown("<br>", unsafe_allow_html=True)
    rep = pd.DataFrame({"البند": ["الإيرادات", "تكلفة البضاعة المباعة", "الرواتب", "الإنفاق التسويقي", "صافي الربح", "إجمالي المشتريات"],
                        "القيمة": [t["revenue"], -t["cogs"], -t["salaries"], -t["ads"], t["profit"], t["purchases"]]})
    l, r = st.columns([1, 1.2])
    l.markdown("#### قائمة الدخل")
    l.dataframe(rep, use_container_width=True, hide_index=True)
    r.markdown("#### توزيع المصروفات")
    r.bar_chart(pd.DataFrame({"القيمة": [t["cogs"], t["salaries"], t["ads"]]}, index=["تكلفة البضاعة", "الرواتب", "التسويق"]), color="#7c3aed")
    if t["profit"] >= 0:
        st.success("المنشأة في حالة ربح حاليا.")
    else:
        st.error("المنشأة في حالة خسارة حاليا. راجع المصروفات الثابتة أو ارفع حجم المبيعات.")
    st.download_button("تنزيل التقرير المالي (CSV)", rep.to_csv(index=False).encode("utf-8-sig"), "financial_report.csv", "text/csv")
 
 
def hr():
    title("الموارد البشرية")
    ed = st.data_editor(S.hr, num_rows="dynamic", use_container_width=True, key="ed_hr",
                        column_config={"الحالة": st.column_config.SelectboxColumn(options=["نشط", "إجازة", "منتهي"])})
    S.hr = ed
    act = ed[ed["الحالة"] == "نشط"]
    c = st.columns(3)
    kpi(c[0], "عدد الموظفين", len(ed))
    kpi(c[1], "الموظفون النشطون", len(act))
    kpi(c[2], "إجمالي الرواتب الشهرية", money(act["الراتب الشهري"].sum()))
 
 
def pr():
    title("العلاقات العامة")
    ed = st.data_editor(S.pr, num_rows="dynamic", use_container_width=True, key="ed_pr",
                        column_config={"النوع": st.column_config.SelectboxColumn(options=["فعالية", "إعلام", "شراكة", "مسؤولية مجتمعية"]),
                                       "الحالة": st.column_config.SelectboxColumn(options=["مخطط", "قيد الإعداد", "منفذ", "ملغى"])})
    S.pr = ed
    c = st.columns(3)
    kpi(c[0], "إجمالي الأنشطة", len(ed))
    kpi(c[1], "منفذة", int((ed["الحالة"] == "منفذ").sum()))
    kpi(c[2], "مخططة", int((ed["الحالة"] == "مخطط").sum()))
 
 
PAGES = {
    "مجلس الإدارة": board, "الشؤون القانونية والإدارية": legal, "إدارة المخزون": inventory, "المشتريات": purchasing,
    "الإنتاج والتصنيع": production, "المبيعات ونقاط البيع": pos, "التسويق": marketing, "خدمة العملاء": crm,
    "الحسابات والمالية": finance, "الموارد البشرية": hr, "العلاقات العامة": pr,
}
 
# ---------------------------------------------------------------- ROUTER
if not S.logged:
    landing()
else:
    with st.sidebar:
        st.markdown('<div class="brand">MINI-ERP</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="company rtl">{S.company}<br>{S.email}</div>', unsafe_allow_html=True)
        page = st.radio("الأقسام", list(PAGES.keys()), label_visibility="collapsed")
        st.markdown("---")
        if st.button("تسجيل الخروج", use_container_width=True):
            for k in list(S.keys()):
                del S[k]
            st.rerun()
    PAGES[page]()
 