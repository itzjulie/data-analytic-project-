import streamlit as st

def render_tailwind_header(title: str, subtitle: str, badge_text: str = "Live Analytics"):
    """
    Renders an enterprise header with Tailwind CSS styling inside an isolated iframe.
    """
    html_code = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <script src="https://cdn.tailwindcss.com"></script>
    </head>
    <body class="bg-transparent font-sans m-0 p-0">
        <header class="bg-gradient-to-r from-slate-900 via-blue-950 to-slate-900 border-b border-slate-700/60 rounded-2xl shadow-lg p-5 mb-3 text-white">
            <div class="flex flex-col md:flex-row md:items-center md:justify-between gap-3">
                <div>
                    <div class="flex items-center gap-2">
                        <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-semibold bg-blue-500/20 text-blue-300 border border-blue-400/30">
                            {badge_text}
                        </span>
                        <span class="text-xs text-slate-400 font-mono">Project 66 · ABES MCA</span>
                    </div>
                    <h1 class="text-2xl font-black tracking-tight text-white mt-1.5">{title}</h1>
                    <p class="text-xs text-slate-300 mt-0.5">{subtitle}</p>
                </div>
                <div class="flex items-center gap-2 text-xs text-slate-300 bg-slate-800/80 px-3 py-1.5 rounded-lg border border-slate-700/50 self-start md:self-auto font-mono">
                    <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
                    <span>Database: SQLite 3.42+ (app.db)</span>
                </div>
            </div>
        </header>
    </body>
    </html>
    """
    st.components.v1.html(html_code, height=125, scrolling=False)


def render_kpi_card(title: str, value: str, subtext: str, badge: str, color: str = "blue"):
    """
    Renders a responsive KPI metric card utilizing Tailwind CSS classes.
    Supported colors: 'blue', 'emerald', 'rose', 'amber', 'purple', 'indigo'.
    """
    color_map = {
        "blue": {"bg": "bg-blue-50", "text": "text-blue-700", "border": "border-blue-200"},
        "emerald": {"bg": "bg-emerald-50", "text": "text-emerald-700", "border": "border-emerald-200"},
        "rose": {"bg": "bg-rose-50", "text": "text-rose-700", "border": "border-rose-200"},
        "amber": {"bg": "bg-amber-50", "text": "text-amber-700", "border": "border-amber-200"},
        "indigo": {"bg": "bg-indigo-50", "text": "text-indigo-700", "border": "border-indigo-200"}
    }
    theme = color_map.get(color, color_map["blue"])

    html_code = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <script src="https://cdn.tailwindcss.com"></script>
    </head>
    <body class="bg-transparent font-sans m-0 p-1">
        <div class="bg-white rounded-xl border border-slate-200/80 shadow-sm hover:shadow-md transition-all duration-200 p-4">
            <div class="flex items-center justify-between">
                <span class="text-xs font-semibold tracking-wider uppercase text-slate-500">{title}</span>
                <span class="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-bold {theme['bg']} {theme['text']} border {theme['border']}">
                    {badge}
                </span>
            </div>
            <div class="text-2xl font-black tracking-tight text-slate-900 mt-2">{value}</div>
            <div class="text-xs text-slate-500 font-medium mt-1">{subtext}</div>
        </div>
    </body>
    </html>
    """
    st.components.v1.html(html_code, height=115, scrolling=False)


def render_alert_box(title: str, message: str, alert_type: str = "warning"):
    """
    Renders a prominent Tailwind alert box for clinical threshold breaches.
    """
    type_map = {
        "warning": {"bg": "bg-rose-50", "border": "border-rose-300", "text": "text-rose-900", "badge": "bg-rose-100 text-rose-800", "icon": "⚠️"},
        "info": {"bg": "bg-blue-50", "border": "border-blue-300", "text": "text-blue-900", "badge": "bg-blue-100 text-blue-800", "icon": "ℹ️"},
        "success": {"bg": "bg-emerald-50", "border": "border-emerald-300", "text": "text-emerald-900", "badge": "bg-emerald-100 text-emerald-800", "icon": "✓"}
    }
    t = type_map.get(alert_type, type_map["warning"])

    html_code = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <script src="https://cdn.tailwindcss.com"></script>
    </head>
    <body class="bg-transparent font-sans m-0 p-1">
        <div class="{t['bg']} border-l-4 {t['border']} rounded-r-xl p-3.5 shadow-sm">
            <div class="flex items-start gap-2.5">
                <span class="text-base">{t['icon']}</span>
                <div>
                    <h4 class="text-xs font-bold uppercase tracking-wide {t['text']}">{title}</h4>
                    <p class="text-xs {t['text']} mt-0.5 leading-relaxed">{message}</p>
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    st.components.v1.html(html_code, height=75, scrolling=False)
