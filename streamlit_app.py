import streamlit as st
import pandas as pd
import random
from datetime import datetime
import time

# Page configuration
st.set_page_config(
    page_title="Bốc Thăm Ghép Cặp",
    page_icon="💛",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for yellow-gold and blue theme
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Quicksand:wght@400;500;600;700&display=swap');
    
    /* Global Styles */
    * {
        font-family: 'Quicksand', sans-serif !important;
    }
    
    /* Main background with gradient */
    .stApp {
        background: linear-gradient(135deg, #FFE5B4 0%, #E0F7FF 100%);
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #FFD700 0%, #FFA500 100%);
        border-right: 3px solid #1E90FF;
    }
    
    [data-testid="stSidebar"] .stMarkdown {
        color: #1a1a1a;
    }
    
    /* Headers */
    h1 {
        background: linear-gradient(90deg, #FFD700 0%, #FFA500 50%, #1E90FF 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700 !important;
        text-align: center;
        font-size: 3rem !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    
    h2 {
        color: #FF8C00;
        font-weight: 600 !important;
        border-bottom: 3px solid #1E90FF;
        padding-bottom: 10px;
    }
    
    h3 {
        color: #1E90FF;
        font-weight: 600 !important;
    }
    
    /* Hide keyboard double arrow right icon */
    [data-testid="stExpanderToggleIcon"] {
        display: none !important;
    }
    
    .streamlit-expanderHeader::before {
        display: none !important;
    }
    
    /* Cards for lists */
    .list-card {
        background: white;
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 8px 16px rgba(0,0,0,0.1);
        margin: 10px 0;
        border: 3px solid;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .list-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 24px rgba(0,0,0,0.15);
    }
    
    .list-card-a {
        border-color: #FFD700;
        background: linear-gradient(135deg, #FFFACD 0%, #FFFFFF 100%);
    }
    
    .list-card-b {
        border-color: #1E90FF;
        background: linear-gradient(135deg, #E0F7FF 0%, #FFFFFF 100%);
    }
    
    .list-header-a {
        color: #FF8C00;
        font-size: 1.5rem;
        font-weight: 700;
        text-align: center;
        margin-bottom: 15px;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
    }
    
    .list-header-b {
        color: #1E90FF;
        font-size: 1.5rem;
        font-weight: 700;
        text-align: center;
        margin-bottom: 15px;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
    }
    
    /* Pairing cards */
    .pair-card {
        background: white;
        border-radius: 20px;
        padding: 25px;
        margin: 15px 0;
        box-shadow: 0 10px 20px rgba(0,0,0,0.15);
        border: 3px solid transparent;
        background-image: linear-gradient(white, white), 
                          linear-gradient(90deg, #FFD700, #1E90FF);
        background-origin: border-box;
        background-clip: padding-box, border-box;
        animation: slideIn 0.5s ease;
    }
    
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .pair-content {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 20px;
    }
    
    .pair-name-a {
        flex: 1;
        text-align: right;
        color: #FF8C00;
        font-size: 1.3rem;
        font-weight: 600;
        padding: 15px;
        background: linear-gradient(135deg, #FFFACD 0%, #FFE5B4 100%);
        border-radius: 10px;
        border: 2px solid #FFD700;
    }
    
    .pair-heart {
        font-size: 2.5rem;
        animation: heartBeat 1.5s infinite;
        filter: drop-shadow(0 0 10px rgba(255,215,0,0.5));
    }
    
    @keyframes heartBeat {
        0%, 100% { transform: scale(1); }
        25% { transform: scale(1.2); }
        50% { transform: scale(1); }
    }
    
    .pair-name-b {
        flex: 1;
        text-align: left;
        color: #1E90FF;
        font-size: 1.3rem;
        font-weight: 600;
        padding: 15px;
        background: linear-gradient(135deg, #E0F7FF 0%, #B0E0E6 100%);
        border-radius: 10px;
        border: 2px solid #1E90FF;
    }
    
    /* Confetti animation */
    .confetti {
        position: fixed;
        width: 10px;
        height: 10px;
        background: #FFD700;
        animation: confettiFall 3s linear;
        z-index: 1000;
    }
    
    @keyframes confettiFall {
        to {
            transform: translateY(100vh) rotate(360deg);
            opacity: 0;
        }
    }
    
    /* Buttons */
    .stButton > button {
        border-radius: 25px;
        font-weight: 600;
        border: 2px solid;
        transition: all 0.3s ease;
        font-size: 1.1rem !important;
        padding: 12px 24px;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 16px rgba(0,0,0,0.2);
    }
    
    /* Success message */
    .celebration {
        background: linear-gradient(90deg, #FFD700, #1E90FF, #FFD700);
        background-size: 200% 200%;
        animation: gradientShift 2s ease infinite;
        color: white;
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        font-size: 1.5rem;
        font-weight: 700;
        box-shadow: 0 8px 16px rgba(0,0,0,0.2);
    }
    
    @keyframes gradientShift {
        0%, 100% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
    }
    
    /* DataFrames */
    .dataframe {
        border-radius: 10px;
        overflow: hidden;
    }
    
    /* Info boxes */
    .stAlert {
        border-radius: 15px;
        border-width: 2px;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background: linear-gradient(90deg, #FFE5B4 0%, #E0F7FF 100%);
        border-radius: 10px;
        font-weight: 600;
        padding-left: 15px !important;
    }
    
    /* Number badge */
    .number-badge {
        display: inline-block;
        background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%);
        color: white;
        padding: 5px 15px;
        border-radius: 20px;
        font-weight: 700;
        margin-right: 10px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
</style>
""", unsafe_allow_html=True)

# Confetti effect function
def show_confetti():
    confetti_html = """
    <script>
    function createConfetti() {
        const colors = ['#FFD700', '#FFA500', '#1E90FF', '#4169E1', '#FF69B4'];
        for(let i = 0; i < 50; i++) {
            setTimeout(() => {
                const confetti = document.createElement('div');
                confetti.className = 'confetti';
                confetti.style.left = Math.random() * 100 + '%';
                confetti.style.background = colors[Math.floor(Math.random() * colors.length)];
                confetti.style.animationDelay = Math.random() * 2 + 's';
                document.body.appendChild(confetti);
                setTimeout(() => confetti.remove(), 3000);
            }, i * 50);
        }
    }
    createConfetti();
    </script>
    """
    st.components.v1.html(confetti_html, height=0)

# Initialize session state
if 'list_a' not in st.session_state:
    st.session_state.list_a = []
if 'list_b' not in st.session_state:
    st.session_state.list_b = []
if 'current_pairs' not in st.session_state:
    st.session_state.current_pairs = []
if 'revealed_index' not in st.session_state:
    st.session_state.revealed_index = 0
if 'pairing_history' not in st.session_state:
    st.session_state.pairing_history = []
if 'pairing_mode' not in st.session_state:
    st.session_state.pairing_mode = None
if 'show_confetti' not in st.session_state:
    st.session_state.show_confetti = False

# Title with emoji
st.markdown("<h1>💛 BỐC THĂM GHÉP CẶP NGẪU NHIÊN 💙</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 1.2rem; color: #555;'>✨ Hệ thống ghép cặp tự động ✨</p>", unsafe_allow_html=True)
st.markdown("---")

# Sidebar for input
with st.sidebar:
    st.markdown("### 📝 NHẬP DANH SÁCH")
    
    st.markdown("#### 🟡 Danh Sách A")
    list_a_input = st.text_area(
        "",
        height=200,
        key="input_a",
        placeholder="Nguyễn Văn A\nTrần Thị B\nLê Văn C\n...",
        label_visibility="collapsed"
    )
    
    st.markdown("#### 🔵 Danh Sách B")
    list_b_input = st.text_area(
        "",
        height=200,
        key="input_b",
        placeholder="Phạm Văn X\nHoàng Thị Y\nĐỗ Văn Z\n...",
        label_visibility="collapsed"
    )
    
    if st.button("✅ XÁC NHẬN DANH SÁCH", use_container_width=True, type="primary"):
        # Parse lists
        st.session_state.list_a = [line.strip() for line in list_a_input.split('\n') if line.strip()]
        st.session_state.list_b = [line.strip() for line in list_b_input.split('\n') if line.strip()]
        
        # Reset pairing state
        st.session_state.current_pairs = []
        st.session_state.revealed_index = 0
        st.session_state.pairing_mode = None
        st.session_state.show_confetti = False
        
        if len(st.session_state.list_a) == 0 or len(st.session_state.list_b) == 0:
            st.error("❌ Vui lòng nhập cả hai danh sách!")
        elif len(st.session_state.list_a) != len(st.session_state.list_b):
            st.warning(f"⚠️ Danh sách không cân bằng:\n\n🟡 A: {len(st.session_state.list_a)} mục\n\n🔵 B: {len(st.session_state.list_b)} mục")
        else:
            st.success(f"✅ Đã tải {len(st.session_state.list_a)} mục từ mỗi danh sách!")
            st.balloons()
    
    st.markdown("---")
    
    # Display current lists info
    if st.session_state.list_a and st.session_state.list_b:
        st.markdown(f"""
        <div style='background: white; padding: 15px; border-radius: 10px; border: 2px solid #FFD700;'>
            <p style='margin: 5px 0; color: #FF8C00; font-weight: 600;'>🟡 Danh sách A: <span class='number-badge'>{len(st.session_state.list_a)}</span></p>
            <p style='margin: 5px 0; color: #1E90FF; font-weight: 600;'>🔵 Danh sách B: <span class='number-badge'>{len(st.session_state.list_b)}</span></p>
        </div>
        """, unsafe_allow_html=True)

# Main content
col1, col2 = st.columns(2)

with col1:
    st.markdown("<h2>📋 DANH SÁCH HIỆN TẠI</h2>", unsafe_allow_html=True)
    
    if st.session_state.list_a and st.session_state.list_b:
        # Display both lists side by side
        list_col1, list_col2 = st.columns(2)
        
        with list_col1:
            st.markdown("""
            <div class='list-card list-card-a'>
                <div class='list-header-a'>🟡 DANH SÁCH A</div>
            </div>
            """, unsafe_allow_html=True)
            
            df_a = pd.DataFrame(st.session_state.list_a, columns=['Tên'])
            df_a.index = df_a.index + 1
            st.dataframe(df_a, use_container_width=True, height=400)
        
        with list_col2:
            st.markdown("""
            <div class='list-card list-card-b'>
                <div class='list-header-b'>🔵 DANH SÁCH B</div>
            </div>
            """, unsafe_allow_html=True)
            
            df_b = pd.DataFrame(st.session_state.list_b, columns=['Tên'])
            df_b.index = df_b.index + 1
            st.dataframe(df_b, use_container_width=True, height=400)
    else:
        st.info("👈 Vui lòng nhập danh sách ở thanh bên trái")

with col2:
    st.markdown("<h2>🎯 CHẾ ĐỘ GHÉP CẶP</h2>", unsafe_allow_html=True)
    
    if st.session_state.list_a and st.session_state.list_b:
        if len(st.session_state.list_a) == len(st.session_state.list_b):
            
            mode_col1, mode_col2 = st.columns(2)
            
            with mode_col1:
                if st.button("🎲 GHÉP TỪNG CẶP", use_container_width=True, type="primary"):
                    if not st.session_state.current_pairs:
                        # Generate pairs
                        list_a_copy = st.session_state.list_a.copy()
                        list_b_copy = st.session_state.list_b.copy()
                        random.shuffle(list_b_copy)
                        
                        st.session_state.current_pairs = list(zip(list_a_copy, list_b_copy))
                        st.session_state.revealed_index = 0
                        st.session_state.pairing_mode = "sequential"
                        st.session_state.show_confetti = False
                    
                    st.rerun()
            
            with mode_col2:
                if st.button("⚡ GHÉP TỰ ĐỘNG", use_container_width=True, type="secondary"):
                    # Generate pairs
                    list_a_copy = st.session_state.list_a.copy()
                    list_b_copy = st.session_state.list_b.copy()
                    random.shuffle(list_b_copy)
                    
                    st.session_state.current_pairs = list(zip(list_a_copy, list_b_copy))
                    st.session_state.revealed_index = len(st.session_state.current_pairs)
                    st.session_state.pairing_mode = "auto"
                    st.session_state.show_confetti = True
                    
                    st.rerun()
            
            st.markdown("---")
            
            # Show confetti effect
            if st.session_state.show_confetti:
                show_confetti()
                st.session_state.show_confetti = False
            
            # Display pairing results
            if st.session_state.current_pairs:
                
                if st.session_state.pairing_mode == "sequential":
                    st.markdown("<h3>🎁 BỐC THĂM TỪNG CẶP</h3>", unsafe_allow_html=True)
                    
                    # Show revealed pairs with hearts
                    if st.session_state.revealed_index > 0:
                        for idx in range(st.session_state.revealed_index):
                            pair = st.session_state.current_pairs[idx]
                            st.markdown(f"""
                            <div class='pair-card'>
                                <div style='text-align: center; margin-bottom: 10px;'>
                                    <span class='number-badge'>Cặp {idx + 1}</span>
                                </div>
                                <div class='pair-content'>
                                    <div class='pair-name-a'>{pair[0]}</div>
                                    <div class='pair-heart'>💕</div>
                                    <div class='pair-name-b'>{pair[1]}</div>
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
                    
                    # Next pair button
                    if st.session_state.revealed_index < len(st.session_state.current_pairs):
                        if st.button(f"🎲 BỐC CẶP TIẾP THEO ({st.session_state.revealed_index + 1}/{len(st.session_state.current_pairs)})", 
                                   use_container_width=True, type="primary"):
                            st.session_state.revealed_index += 1
                            
                            if st.session_state.revealed_index == len(st.session_state.current_pairs):
                                # Save to history when complete
                                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                                st.session_state.pairing_history.append({
                                    'timestamp': timestamp,
                                    'pairs': st.session_state.current_pairs.copy(),
                                    'mode': 'Ghép Từng Cặp'
                                })
                                st.session_state.show_confetti = True
                            
                            st.rerun()
                    else:
                        st.markdown("""
                        <div class='celebration'>
                            🎉 HOÀN THÀNH BỐC THĂM TẤT CẢ CÁC CẶP! 🎉
                        </div>
                        """, unsafe_allow_html=True)
                        st.balloons()
                
                elif st.session_state.pairing_mode == "auto":
                    st.markdown("<h3>⚡ KẾT QUẢ GHÉP TỰ ĐỘNG</h3>", unsafe_allow_html=True)
                    
                    # Display all pairs with hearts
                    for idx, pair in enumerate(st.session_state.current_pairs):
                        st.markdown(f"""
                        <div class='pair-card'>
                            <div style='text-align: center; margin-bottom: 10px;'>
                                <span class='number-badge'>Cặp {idx + 1}</span>
                            </div>
                            <div class='pair-content'>
                                <div class='pair-name-a'>{pair[0]}</div>
                                <div class='pair-heart'>💕</div>
                                <div class='pair-name-b'>{pair[1]}</div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    # Save to history
                    if st.session_state.current_pairs:
                        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        
                        # Check if this pairing is already in history
                        is_duplicate = False
                        for history_item in st.session_state.pairing_history:
                            if history_item['pairs'] == st.session_state.current_pairs:
                                is_duplicate = True
                                break
                        
                        if not is_duplicate:
                            st.session_state.pairing_history.append({
                                'timestamp': timestamp,
                                'pairs': st.session_state.current_pairs.copy(),
                                'mode': 'Ghép Tự Động'
                            })
                
                # Reset and Save buttons
                st.markdown("<br>", unsafe_allow_html=True)
                btn_col1, btn_col2 = st.columns(2)
                with btn_col1:
                    if st.button("🔄 LÀM LẠI", use_container_width=True):
                        st.session_state.current_pairs = []
                        st.session_state.revealed_index = 0
                        st.session_state.pairing_mode = None
                        st.session_state.show_confetti = False
                        st.rerun()
                
                with btn_col2:
                    if st.button("💾 LƯU KẾT QUẢ", use_container_width=True, type="primary"):
                        if st.session_state.current_pairs:
                            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            
                            # Check for duplicates
                            is_duplicate = False
                            for history_item in st.session_state.pairing_history:
                                if history_item['pairs'] == st.session_state.current_pairs:
                                    is_duplicate = True
                                    break
                            
                            if not is_duplicate:
                                st.session_state.pairing_history.append({
                                    'timestamp': timestamp,
                                    'pairs': st.session_state.current_pairs.copy(),
                                    'mode': st.session_state.pairing_mode
                                })
                                st.success("✅ Đã lưu kết quả!")
                                st.balloons()
                            else:
                                st.info("ℹ️ Kết quả này đã được lưu trước đó")
        else:
            st.warning("⚠️ Hai danh sách phải có cùng số lượng mục để ghép cặp!")
    else:
        st.info("👈 Vui lòng nhập và xác nhận danh sách trước")

# History and Export section
st.markdown("---")
st.markdown("<h2>📊 LỊCH SỬ & XUẤT BÁO CÁO</h2>", unsafe_allow_html=True)

if st.session_state.pairing_history:
    st.markdown(f"<h3>🗂️ Có {len(st.session_state.pairing_history)} kết quả đã lưu</h3>", unsafe_allow_html=True)
    
    # Display history
    for idx, history_item in enumerate(reversed(st.session_state.pairing_history)):
        with st.expander(f"📅 Lần {len(st.session_state.pairing_history) - idx}: {history_item['timestamp']} - {history_item['mode']}"):
            # Display pairs with hearts in expander
            for pair_idx, pair in enumerate(history_item['pairs']):
                st.markdown(f"""
                <div class='pair-card'>
                    <div style='text-align: center; margin-bottom: 10px;'>
                        <span class='number-badge'>Cặp {pair_idx + 1}</span>
                    </div>
                    <div class='pair-content'>
                        <div class='pair-name-a'>{pair[0]}</div>
                        <div class='pair-heart'>💕</div>
                        <div class='pair-name-b'>{pair[1]}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            # Export individual result
            df_history = pd.DataFrame(history_item['pairs'], columns=['Danh Sách A', 'Danh Sách B'])
            df_history.index = df_history.index + 1
            csv = df_history.to_csv(index=True, encoding='utf-8-sig').encode('utf-8-sig')
            st.download_button(
                label="📥 Tải CSV",
                data=csv,
                file_name=f"ghep_cap_{history_item['timestamp'].replace(':', '-').replace(' ', '_')}.csv",
                mime="text/csv",
                key=f"download_{idx}",
                use_container_width=True
            )
    
    # Export all results
    st.markdown("---")
    
    export_col1, export_col2 = st.columns(2)
    
    with export_col1:
        # Combine all history into one dataframe
        all_pairs_data = []
        for idx, history_item in enumerate(st.session_state.pairing_history):
            for pair_idx, pair in enumerate(history_item['pairs']):
                all_pairs_data.append({
                    'Lần Ghép': idx + 1,
                    'Thời Gian': history_item['timestamp'],
                    'Chế Độ': history_item['mode'],
                    'STT Cặp': pair_idx + 1,
                    'Danh Sách A': pair[0],
                    'Danh Sách B': pair[1]
                })
        
        df_all = pd.DataFrame(all_pairs_data)
        csv_all = df_all.to_csv(index=False, encoding='utf-8-sig').encode('utf-8-sig')
        
        st.download_button(
            label="📥 TẢI TOÀN BỘ LỊCH SỬ (CSV)",
            data=csv_all,
            file_name=f"lich_su_ghep_cap_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
            use_container_width=True,
            type="primary"
        )
    
    with export_col2:
        if st.button("🗑️ XÓA TOÀN BỘ LỊCH SỬ", use_container_width=True):
            st.session_state.pairing_history = []
            st.rerun()

else:
    st.info("📭 Chưa có kết quả ghép cặp nào được lưu")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; padding: 20px; background: linear-gradient(90deg, #FFE5B4 0%, #E0F7FF 100%); border-radius: 15px; margin-top: 30px;'>
    <p style='font-size: 1.2rem; font-weight: 600; margin: 0; background: linear-gradient(90deg, #FFD700 0%, #1E90FF 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>
        💛 Ứng dụng Bốc Thăm Ghép Cặp Ngẫu Nhiên 💙
    </p>
    <p style='font-size: 0.9rem; color: #666; margin: 5px 0 0 0;'>
        ✨ Phiên bản 2.0 - Ban Chuyển đổi số và Công nghệ ✨
    </p>
</div>
""", unsafe_allow_html=True)
