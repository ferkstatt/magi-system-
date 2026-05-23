"""
マギシステム — Web版
Streamlit Community Cloud で無料ホスティング・iPhone対応
"""

import base64
import html as html_lib
import io
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

import streamlit as st
from dotenv import load_dotenv

load_dotenv()

# ─── ページ設定（必ず最初に呼ぶ）────────────────────────────────────────────
st.set_page_config(
    page_title="MAGI SYSTEM",
    page_icon="△",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─── サイバーパンク CSS ──────────────────────────────────────────────────────
CYBER_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;600;900&family=Share+Tech+Mono&display=swap');

/* ═══ 背景・ベース ═══ */
.stApp {
    background-color: #010b14 !important;
    background-image:
        linear-gradient(rgba(0,255,180,0.022) 1px, transparent 1px),
        linear-gradient(90deg, rgba(0,255,180,0.022) 1px, transparent 1px);
    background-size: 48px 48px;
}

/* スキャンライン */
.stApp::after {
    content: '';
    position: fixed;
    inset: 0;
    background: repeating-linear-gradient(
        0deg,
        rgba(0,0,0,0.04) 0px,
        rgba(0,0,0,0.04) 1px,
        transparent 1px,
        transparent 3px
    );
    pointer-events: none;
    z-index: 9999;
}

p, div:not(.stFileUploader div), span:not(.stFileUploader span), li {
    font-family: 'Share Tech Mono', 'Hiragino Sans', 'Yu Gothic', 'Meiryo', monospace !important;
}

/* ═══ ヘッダー ═══ */
.magi-header {
    text-align: center;
    padding: 28px 0 20px;
    margin-bottom: 18px;
    position: relative;
}
.magi-header::after {
    content: '';
    display: block;
    height: 1px;
    background: linear-gradient(90deg,
        transparent 0%,
        rgba(0,255,159,0.1) 10%,
        #00ff9f 35%,
        #00ccff 50%,
        #00ff9f 65%,
        rgba(0,255,159,0.1) 90%,
        transparent 100%);
    margin-top: 18px;
}
.nerv-badge {
    font-size: 0.62rem;
    letter-spacing: 0.4em;
    color: #0d3322 !important;
    margin-bottom: 10px;
}
.magi-title {
    font-family: 'Orbitron', sans-serif !important;
    font-size: clamp(2.2rem, 6vw, 4rem);
    font-weight: 900;
    letter-spacing: 0.55em;
    color: #00ff9f !important;
    text-shadow:
        0 0 10px #00ff9f,
        0 0 30px rgba(0,255,159,0.5),
        0 0 80px rgba(0,255,159,0.2);
    margin: 0;
    line-height: 1;
}
.magi-sub {
    font-size: 0.68rem;
    color: #1a6644 !important;
    letter-spacing: 0.3em;
    margin-top: 8px;
}
.magi-nodes {
    font-size: 0.62rem;
    color: #0d3322 !important;
    letter-spacing: 0.25em;
    margin-top: 5px;
}

/* ═══ 入力セクション ═══ */
.input-section {
    background: rgba(0, 12, 28, 0.8);
    border: 1px solid rgba(0,255,159,0.12);
    border-radius: 3px;
    padding: 18px 20px 14px;
    margin-bottom: 14px;
    position: relative;
}
.input-section::before {
    content: 'QUERY TERMINAL';
    position: absolute;
    top: -9px; left: 16px;
    background: #010b14;
    padding: 0 8px;
    font-size: 0.62rem;
    letter-spacing: 0.2em;
    color: #1a6644 !important;
}

/* textarea */
.stTextArea > div > div > textarea {
    background: rgba(0, 6, 16, 0.95) !important;
    border: 1px solid rgba(0,255,159,0.2) !important;
    color: #7affd4 !important;
    font-size: 0.95rem !important;
    border-radius: 2px !important;
    caret-color: #00ff9f;
    resize: vertical !important;
}
.stTextArea > div > div > textarea:focus {
    border-color: rgba(0,255,159,0.55) !important;
    box-shadow: 0 0 14px rgba(0,255,159,0.1) !important;
    outline: none !important;
}
.stTextArea label {
    font-size: 0.68rem !important;
    color: #1a6644 !important;
    letter-spacing: 0.18em !important;
    font-family: 'Orbitron', sans-serif !important;
}

/* ファイルアップローダー：内部には一切干渉しない */
.stFileUploader > div {
    background: rgba(0, 6, 16, 0.6) !important;
}

/* ═══ ボタン ═══ */
.stButton > button {
    background: transparent !important;
    border: 1px solid #00ff9f !important;
    color: #00ff9f !important;
    font-family: 'Orbitron', sans-serif !important;
    font-size: 0.78rem !important;
    letter-spacing: 0.35em !important;
    padding: 13px 0 !important;
    border-radius: 2px !important;
    transition: all 0.15s ease !important;
    text-shadow: 0 0 8px rgba(0,255,159,0.5);
}
.stButton > button:hover {
    background: rgba(0,255,159,0.07) !important;
    box-shadow: 0 0 28px rgba(0,255,159,0.2), inset 0 0 12px rgba(0,255,159,0.05) !important;
}
.stButton > button:active {
    background: rgba(0,255,159,0.12) !important;
}

/* ═══ パネル ═══ */
.magi-panel {
    border-radius: 3px;
    overflow: hidden;
    margin-bottom: 10px;
    border: 1px solid rgba(0,255,159,0.12);
    background: linear-gradient(160deg, rgba(0,15,32,0.95) 0%, rgba(0,8,20,0.98) 100%);
}
.panel-topbar {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 9px 14px;
    border-bottom: 1px solid rgba(255,255,255,0.05);
    background: rgba(0,0,0,0.3);
}
.panel-led {
    width: 7px; height: 7px;
    border-radius: 50%;
    flex-shrink: 0;
}
.panel-computer {
    font-family: 'Orbitron', sans-serif !important;
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.18em;
}
.panel-ai {
    font-size: 0.62rem;
    opacity: 0.5;
    letter-spacing: 0.1em;
    margin-left: 4px;
}
.panel-tag {
    font-size: 0.6rem;
    margin-left: auto;
    letter-spacing: 0.08em;
    opacity: 0.45;
    padding: 2px 6px;
    border: 1px solid currentColor;
    border-radius: 2px;
}
.panel-body {
    padding: 14px 16px;
    min-height: 140px;
    font-size: 0.83rem;
    line-height: 1.75;
    white-space: pre-wrap;
    word-break: break-word;
}

/* MELCHIOR — 緑 */
.p-m { border-color: rgba(16,163,127,0.28); }
.p-m .panel-topbar { border-bottom-color: rgba(16,163,127,0.15); }
.p-m .panel-led { background: #10a37f; box-shadow: 0 0 7px #10a37f; }
.p-m .panel-computer { color: #10a37f !important; text-shadow: 0 0 8px rgba(16,163,127,0.45); }
.p-m .panel-ai, .p-m .panel-tag { color: #10a37f !important; }
.p-m .panel-body { color: #80f0c8 !important; }

/* BALTHASAR — 青 */
.p-b { border-color: rgba(66,133,244,0.28); }
.p-b .panel-topbar { border-bottom-color: rgba(66,133,244,0.15); }
.p-b .panel-led { background: #4285f4; box-shadow: 0 0 7px #4285f4; }
.p-b .panel-computer { color: #4285f4 !important; text-shadow: 0 0 8px rgba(66,133,244,0.45); }
.p-b .panel-ai, .p-b .panel-tag { color: #4285f4 !important; }
.p-b .panel-body { color: #a8c8ff !important; }

/* CASPAR — オレンジ */
.p-c { border-color: rgba(204,120,92,0.28); }
.p-c .panel-topbar { border-bottom-color: rgba(204,120,92,0.15); }
.p-c .panel-led { background: #cc785c; box-shadow: 0 0 7px #cc785c; }
.p-c .panel-computer { color: #cc785c !important; text-shadow: 0 0 8px rgba(204,120,92,0.45); }
.p-c .panel-ai, .p-c .panel-tag { color: #cc785c !important; }
.p-c .panel-body { color: #f0c0a0 !important; }

/* ═══ ジャッジパネル ═══ */
.magi-judge {
    border: 1px solid rgba(255,215,0,0.22);
    background: linear-gradient(160deg, rgba(18,14,0,0.97) 0%, rgba(8,6,0,0.99) 100%);
    border-radius: 3px;
    overflow: hidden;
    margin: 14px 0 4px;
}
.judge-topbar {
    padding: 9px 14px;
    background: rgba(255,215,0,0.04);
    border-bottom: 1px solid rgba(255,215,0,0.12);
    display: flex; align-items: center; gap: 10px;
}
.judge-led {
    width: 7px; height: 7px; border-radius: 50%;
    background: #ffd700;
    box-shadow: 0 0 8px #ffd700;
    flex-shrink: 0;
}
.judge-label {
    font-family: 'Orbitron', sans-serif !important;
    font-size: 0.72rem;
    letter-spacing: 0.22em;
    color: #ffd700 !important;
    text-shadow: 0 0 10px rgba(255,215,0,0.4);
}
.judge-body {
    padding: 16px 18px;
    font-size: 0.86rem;
    line-height: 1.8;
    color: #ffe080 !important;
    white-space: pre-wrap;
    word-break: break-word;
}

/* ═══ スピナー ═══ */
.stSpinner > div {
    border-top-color: #00ff9f !important;
}

/* ═══ Streamlit の余分な要素を非表示 ═══ */
#MainMenu, footer, header { visibility: hidden !important; }
.block-container {
    padding-top: 0.5rem !important;
    padding-bottom: 1rem !important;
    max-width: 100% !important;
}
[data-testid="stDecoration"] { display: none !important; }

/* ═══ モバイル対応 ═══ */
@media (max-width: 640px) {
    .magi-title { letter-spacing: 0.25em; }
    .panel-body { font-size: 0.78rem; }
}
</style>
"""

st.markdown(CYBER_CSS, unsafe_allow_html=True)


# ─── キー取得 ────────────────────────────────────────────────────────────────

def _key(name: str) -> str | None:
    try:
        return st.secrets[name]
    except Exception:
        return os.getenv(name)


# ─── API 呼び出し ────────────────────────────────────────────────────────────

def ask_chatgpt(question: str, image_bytes: bytes | None, image_mime: str | None) -> str:
    import openai
    k = _key("OPENAI_API_KEY")
    if not k:
        raise ValueError("OPENAI_API_KEY が未設定です")
    client = openai.OpenAI(api_key=k)
    if image_bytes:
        b64 = base64.standard_b64encode(image_bytes).decode()
        content = [
            {"type": "image_url", "image_url": {"url": f"data:{image_mime};base64,{b64}"}},
            {"type": "text", "text": question},
        ]
    else:
        content = question
    res = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": content}],
        max_tokens=2048,
    )
    return res.choices[0].message.content


def ask_gemini(question: str, image_bytes: bytes | None, image_mime: str | None) -> str:
    from google import genai
    k = _key("GOOGLE_API_KEY")
    if not k:
        raise ValueError("GOOGLE_API_KEY が未設定です")
    client = genai.Client(api_key=k)
    if image_bytes:
        import PIL.Image
        img = PIL.Image.open(io.BytesIO(image_bytes)).convert("RGB")
        contents = [question, img]
    else:
        contents = question
    res = client.models.generate_content(model="gemini-2.0-flash", contents=contents)
    return res.text


def ask_claude(question: str, image_bytes: bytes | None, image_mime: str | None) -> str:
    import anthropic
    k = _key("ANTHROPIC_API_KEY")
    if not k:
        raise ValueError("ANTHROPIC_API_KEY が未設定です")
    client = anthropic.Anthropic(api_key=k)
    if image_bytes:
        b64 = base64.standard_b64encode(image_bytes).decode()
        content = [
            {"type": "image", "source": {"type": "base64", "media_type": image_mime, "data": b64}},
            {"type": "text", "text": question},
        ]
    else:
        content = question
    res = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=2048,
        messages=[{"role": "user", "content": content}],
    )
    return res.content[0].text


def judge_responses(question: str, responses: dict[str, str], has_image: bool) -> str:
    import anthropic
    k = _key("ANTHROPIC_API_KEY")
    if not k:
        raise ValueError("ANTHROPIC_API_KEY が未設定です")
    client = anthropic.Anthropic(api_key=k)
    sections = "\n\n".join(f"=== {name} ===\n{text}" for name, text in responses.items())
    image_note = "（質問には画像も添付されていました）" if has_image else ""
    prompt = f"""あなたは公平なAI評価者です。以下の質問{image_note}に対して3つのAIが回答しました。
各回答を評価し、最も優れた回答を選んでください。

【質問】
{question}

【各AIの回答】
{sections}

以下の観点で各回答を100点満点で採点し、理由を簡潔に述べてください：
1. 正確性（情報は正しいか）
2. 完全性（質問に十分答えているか）
3. 明確さ（わかりやすいか）
4. 実用性（実際に役立つか）

採点後、「最優秀回答: [AI名] ([点数]点)」の形式で最終判定を下し、
その回答が優れている理由を2〜3文で説明してください。"""
    res = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=2048,
        messages=[{"role": "user", "content": prompt}],
    )
    return res.content[0].text


# ─── AI 設定 ─────────────────────────────────────────────────────────────────

AI_CONFIG = [
    ("MELCHIOR·1",  "ChatGPT", "m", ask_chatgpt),
    ("BALTHASAR·2", "Gemini",  "b", ask_gemini),
    ("CASPAR·3",    "Claude",  "c", ask_claude),
]


# ─── HTML レンダラー ──────────────────────────────────────────────────────────

def panel_html(cls: str, computer: str, ai_name: str, body: str) -> str:
    esc = html_lib.escape(body)
    return f"""
<div class="magi-panel p-{cls}">
  <div class="panel-topbar">
    <span class="panel-led"></span>
    <span class="panel-computer">{computer}</span>
    <span class="panel-ai">/ {ai_name}</span>
    <span class="panel-tag">ONLINE</span>
  </div>
  <div class="panel-body">{esc}</div>
</div>"""


def judge_html(body: str) -> str:
    esc = html_lib.escape(body)
    return f"""
<div class="magi-judge">
  <div class="judge-topbar">
    <span class="judge-led"></span>
    <span class="judge-label">◈ &nbsp;JUDGMENT SYSTEM — EVALUATION COMPLETE</span>
  </div>
  <div class="judge-body">{esc}</div>
</div>"""


# ─── セッション状態 ───────────────────────────────────────────────────────────

if "results" not in st.session_state:
    st.session_state.results = {}
if "judge" not in st.session_state:
    st.session_state.judge = ""


# ─── ヘッダー ────────────────────────────────────────────────────────────────

st.markdown("""
<div class="magi-header">
  <div class="nerv-badge">NERV — GEHIRN ADVANCED COMPUTING DIVISION</div>
  <div class="magi-title">MAGI</div>
  <div class="magi-sub">SUPER COMPUTER NETWORK &nbsp;·&nbsp; MULTI-AI QUERY &amp; JUDGMENT SYSTEM</div>
  <div class="magi-nodes">MELCHIOR-1 &nbsp;·&nbsp; BALTHASAR-2 &nbsp;·&nbsp; CASPAR-3</div>
</div>
""", unsafe_allow_html=True)


# ─── 入力エリア ──────────────────────────────────────────────────────────────

st.markdown('<div class="input-section">', unsafe_allow_html=True)

col_q, col_img = st.columns([3, 1], gap="medium")
with col_q:
    question = st.text_area(
        "QUERY INPUT",
        height=108,
        placeholder="質問を入力してください…",
        label_visibility="visible",
    )
with col_img:
    st.markdown('<p style="font-family:Orbitron,sans-serif;font-size:0.68rem;color:#1a6644;letter-spacing:0.18em;margin-bottom:4px">IMAGE ATTACHMENT</p>', unsafe_allow_html=True)
    uploaded = st.file_uploader(
        "image",
        type=["png", "jpg", "jpeg", "webp"],
        label_visibility="collapsed",
    )

st.markdown('</div>', unsafe_allow_html=True)

_, btn_col, _ = st.columns([1.5, 1, 1.5])
with btn_col:
    execute = st.button("▶  EXECUTE QUERY", use_container_width=True)


# ─── 実行 ────────────────────────────────────────────────────────────────────

if execute and question.strip():
    image_bytes = uploaded.getvalue() if uploaded else None
    image_mime  = uploaded.type       if uploaded else None

    with st.spinner("MAGI SYSTEM PROCESSING…"):
        responses: dict[str, str] = {}

        def _call(computer: str, ai_name: str, fn) -> tuple[str, str]:
            try:
                return ai_name, fn(question, image_bytes, image_mime)
            except Exception as e:
                return ai_name, f"[エラー]\n{e}"

        with ThreadPoolExecutor(max_workers=3) as ex:
            futs = [ex.submit(_call, computer, ai_name, fn)
                    for computer, ai_name, _, fn in AI_CONFIG]
            for f in as_completed(futs):
                name, text = f.result()
                responses[name] = text

        try:
            verdict = judge_responses(question, responses, has_image=image_bytes is not None)
        except Exception as e:
            verdict = f"[ジャッジエラー]\n{e}"

        st.session_state.results = responses
        st.session_state.judge = verdict


# ─── 結果表示 ────────────────────────────────────────────────────────────────

if st.session_state.results:
    cols = st.columns(3, gap="small")
    for col, (computer, ai_name, cls, _) in zip(cols, AI_CONFIG):
        body = st.session_state.results.get(ai_name, "—")
        col.markdown(panel_html(cls, computer, ai_name, body), unsafe_allow_html=True)

    if st.session_state.judge:
        st.markdown(judge_html(st.session_state.judge), unsafe_allow_html=True)
