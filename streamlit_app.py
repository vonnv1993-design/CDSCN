import streamlit as st
import pandas as pd
import random
from datetime import datetime
import io

# Page configuration
st.set_page_config(
    page_title="Bốc Thăm Ghép Cặp",
    page_icon="🎲",
    layout="wide"
)

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

# Title
st.title("🎲 Bốc Thăm Ghép Cặp Ngẫu Nhiên")
st.markdown("---")

# Sidebar for input
with st.sidebar:
    st.header("📝 Nhập Danh Sách")
    
    st.subheader("Danh Sách A")
    list_a_input = st.text_area(
        "Nhập hoặc paste danh sách A (mỗi tên một dòng):",
        height=200,
        key="input_a",
        placeholder="Nguyễn Văn A\nTrần Thị B\nLê Văn C"
    )
    
    st.subheader("Danh Sách B")
    list_b_input = st.text_area(
        "Nhập hoặc paste danh sách B (mỗi tên một dòng):",
        height=200,
        key="input_b",
        placeholder="Phạm Văn X\nHoàng Thị Y\nĐỗ Văn Z"
    )
    
    if st.button("✅ Xác Nhận Danh Sách", use_container_width=True):
        # Parse lists
        st.session_state.list_a = [line.strip() for line in list_a_input.split('\n') if line.strip()]
        st.session_state.list_b = [line.strip() for line in list_b_input.split('\n') if line.strip()]
        
        # Reset pairing state
        st.session_state.current_pairs = []
        st.session_state.revealed_index = 0
        st.session_state.pairing_mode = None
        
        if len(st.session_state.list_a) == 0 or len(st.session_state.list_b) == 0:
            st.error("❌ Vui lòng nhập cả hai danh sách!")
        elif len(st.session_state.list_a) != len(st.session_state.list_b):
            st.warning(f"⚠️ Danh sách không cân bằng: A ({len(st.session_state.list_a)}) - B ({len(st.session_state.list_b)})")
        else:
            st.success(f"✅ Đã tải {len(st.session_state.list_a)} mục từ mỗi danh sách!")
    
    st.markdown("---")
    
    # Display current lists info
    if st.session_state.list_a and st.session_state.list_b:
        st.info(f"📊 Danh sách A: {len(st.session_state.list_a)} mục\n\n📊 Danh sách B: {len(st.session_state.list_b)} mục")

# Main content
col1, col2 = st.columns(2)

with col1:
    st.header("📋 Danh Sách Hiện Tại")
    
    if st.session_state.list_a and st.session_state.list_b:
        tab1, tab2 = st.tabs(["Danh Sách A", "Danh Sách B"])
        
        with tab1:
            df_a = pd.DataFrame(st.session_state.list_a, columns=['Tên'])
            df_a.index = df_a.index + 1
            st.dataframe(df_a, use_container_width=True)
        
        with tab2:
            df_b = pd.DataFrame(st.session_state.list_b, columns=['Tên'])
            df_b.index = df_b.index + 1
            st.dataframe(df_b, use_container_width=True)
    else:
        st.info("👈 Vui lòng nhập danh sách ở thanh bên trái")

with col2:
    st.header("🎯 Chế Độ Ghép Cặp")
    
    if st.session_state.list_a and st.session_state.list_b:
        if len(st.session_state.list_a) == len(st.session_state.list_b):
            
            mode_col1, mode_col2 = st.columns(2)
            
            with mode_col1:
                if st.button("🎲 Ghép Từng Cặp", use_container_width=True, type="primary"):
                    if not st.session_state.current_pairs:
                        # Generate pairs
                        list_a_copy = st.session_state.list_a.copy()
                        list_b_copy = st.session_state.list_b.copy()
                        random.shuffle(list_b_copy)
                        
                        st.session_state.current_pairs = list(zip(list_a_copy, list_b_copy))
                        st.session_state.revealed_index = 0
                        st.session_state.pairing_mode = "sequential"
                    
                    st.rerun()
            
            with mode_col2:
                if st.button("⚡ Ghép Tự Động", use_container_width=True, type="secondary"):
                    # Generate pairs
                    list_a_copy = st.session_state.list_a.copy()
                    list_b_copy = st.session_state.list_b.copy()
                    random.shuffle(list_b_copy)
                    
                    st.session_state.current_pairs = list(zip(list_a_copy, list_b_copy))
                    st.session_state.revealed_index = len(st.session_state.current_pairs)
                    st.session_state.pairing_mode = "auto"
                    
                    st.rerun()
            
            st.markdown("---")
            
            # Display pairing results
            if st.session_state.current_pairs:
                
                if st.session_state.pairing_mode == "sequential":
                    st.subheader("🎁 Bốc Thăm Từng Cặp")
                    
                    # Show revealed pairs
                    if st.session_state.revealed_index > 0:
                        revealed_pairs = st.session_state.current_pairs[:st.session_state.revealed_index]
                        df_revealed = pd.DataFrame(revealed_pairs, columns=['Danh Sách A', 'Danh Sách B'])
                        df_revealed.index = df_revealed.index + 1
                        st.dataframe(df_revealed, use_container_width=True)
                    
                    # Next pair button
                    if st.session_state.revealed_index < len(st.session_state.current_pairs):
                        if st.button(f"🎲 Bốc Cặp Tiếp Theo ({st.session_state.revealed_index + 1}/{len(st.session_state.current_pairs)})", 
                                   use_container_width=True):
                            st.session_state.revealed_index += 1
                            
                            if st.session_state.revealed_index == len(st.session_state.current_pairs):
                                # Save to history when complete
                                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                                st.session_state.pairing_history.append({
                                    'timestamp': timestamp,
                                    'pairs': st.session_state.current_pairs.copy(),
                                    'mode': 'Ghép Từng Cặp'
                                })
                            
                            st.rerun()
                    else:
                        st.success("🎉 Đã hoàn thành bốc thăm tất cả các cặp!")
                
                elif st.session_state.pairing_mode == "auto":
                    st.subheader("⚡ Kết Quả Ghép Tự Động")
                    
                    df_pairs = pd.DataFrame(st.session_state.current_pairs, columns=['Danh Sách A', 'Danh Sách B'])
                    df_pairs.index = df_pairs.index + 1
                    st.dataframe(df_pairs, use_container_width=True)
                    
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
                btn_col1, btn_col2 = st.columns(2)
                with btn_col1:
                    if st.button("🔄 Làm Lại", use_container_width=True):
                        st.session_state.current_pairs = []
                        st.session_state.revealed_index = 0
                        st.session_state.pairing_mode = None
                        st.rerun()
                
                with btn_col2:
                    if st.button("💾 Lưu Kết Quả", use_container_width=True):
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
                            else:
                                st.info("ℹ️ Kết quả này đã được lưu trước đó")
        else:
            st.warning("⚠️ Hai danh sách phải có cùng số lượng mục để ghép cặp!")
    else:
        st.info("👈 Vui lòng nhập và xác nhận danh sách trước")

# History and Export section
st.markdown("---")
st.header("📊 Lịch Sử & Xuất Báo Cáo")

if st.session_state.pairing_history:
    st.subheader(f"🗂️ Có {len(st.session_state.pairing_history)} kết quả đã lưu")
    
    # Display history
    for idx, history_item in enumerate(reversed(st.session_state.pairing_history)):
        with st.expander(f"Lần {len(st.session_state.pairing_history) - idx}: {history_item['timestamp']} - {history_item['mode']}"):
            df_history = pd.DataFrame(history_item['pairs'], columns=['Danh Sách A', 'Danh Sách B'])
            df_history.index = df_history.index + 1
            st.dataframe(df_history, use_container_width=True)
            
            # Export individual result
            csv = df_history.to_csv(index=True, encoding='utf-8-sig').encode('utf-8-sig')
            st.download_button(
                label="📥 Tải CSV",
                data=csv,
                file_name=f"ghep_cap_{history_item['timestamp'].replace(':', '-')}.csv",
                mime="text/csv",
                key=f"download_{idx}"
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
            label="📥 Tải Toàn Bộ Lịch Sử (CSV)",
            data=csv_all,
            file_name=f"lich_su_ghep_cap_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
            use_container_width=True
        )
    
    with export_col2:
        if st.button("🗑️ Xóa Toàn Bộ Lịch Sử", use_container_width=True, type="secondary"):
            st.session_state.pairing_history = []
            st.rerun()

else:
    st.info("📭 Chưa có kết quả ghép cặp nào được lưu")

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: gray;'>
    <p>🎲 Ứng dụng Bốc Thăm Ghép Cặp Ngẫu Nhiên | Phiên bản 1.0</p>
    </div>
    """,
    unsafe_allow_html=True
)
