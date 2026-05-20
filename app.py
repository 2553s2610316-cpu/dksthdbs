import streamlit as st
st.title('졸려용')
st.write('소유닝')
import streamlit as range_app  # 기본 라이브러리 임포트
import streamlit as st
import pandas as pd
from datetime import datetime

# 1. 페이지 기본 설정 (웹앱 타이틀 및 아이콘)
st.set_page_config(
    page_title="하루 관리 스케줄러",
    page_icon="📅",
    layout="centered"
)

# 2. 데이터 저장소 초기화 (새로고침해도 데이터 유지)
if "todo_list" not in st.session_state:
    st.session_state.todo_list = [
        {"일정": "스트림릿 앱 만들기 🚀", "기한": "2026-05-20", "중요도": "🚨 높음", "완료": False},
        {"일정": "맛있는 저녁 먹기 🍕", "기한": "2026-05-20", "중요도": "🌱 보통", "완료": True}
    ]

# --- 프론트엔드 UI 시작 ---

# 3. 헤더 섹션
st.title("📅 하루 관리 스케줄러")
st.markdown("오늘의 할 일을 기록하고 멋지게 하루를 관리해보세요!")
st.write("---")

# 4. 사이드바 - 새로운 일정 추가 폼
with st.sidebar:
    st.header("➕ 새 일정 추가")
    
    with st.form(key="todo_form", clear_on_submit=True):
        new_task = st.text_input("📝 할 일을 입력하세요", placeholder="예: 운동하기, 독서하기")
        due_date = st.date_input("📅 기한 선택", datetime.now())
        priority = st.selectbox("🔥 중요도", ["🚨 높음", "🌱 보통", "💤 낮음"])
        
        submit_button = st.form_submit_button(label="추가하기")
        
        if submit_button:
            if new_task.strip() != "":
                # 새로운 일정을 세션 상태에 추가
                st.session_state.todo_list.append({
                    "일정": new_task,
                    "기한": due_date.strftime("%Y-%m-%d"),
                    "중요도": priority,
                    "완료": False
                })
                st.success("일정이 추가되었습니다!")
                st.rerun()  # 화면 즉시 갱신
            else:
                st.warning("할 일을 입력해주세요!")

# 5. 메인 화면 - 진행 상황 대시보드
todos = st.session_state.todo_list
total_tasks = len(todos)
completed_tasks = sum(1 for t in todos if t["완료"])

col1, col2, col3 = st.columns(3)
col1.metric(label="총 일정", value=f"{total_tasks}개")
col2.metric(label="완료됨", value=f"{completed_tasks}개")
col3.metric(label="남은 할 일", value=f"{total_tasks - completed_tasks}개")

st.write("")

# 6. 메인 화면 - 일정 목록 및 관리
st.subheader("📌 나의 스케줄 리스트")

if not todos:
    st.info("등록된 일정이 없습니다. 사이드바에서 일정을 추가해보세요!")
else:
    # 각 일정을 루프 돌며 체크박스와 삭제 버튼 배치
    for index, task in enumerate(todos):
        # 완료 여부에 따라 스타일 적용 (가독성을 위한 이모지 구분)
        status_emoji = "✅" if task["완료"] else "⏳"
        
        # 가로 레이아웃 배치
        col_check, col_text, col_date, col_priority, col_del = st.columns([0.5, 3, 1.5, 1, 1])
        
        # 완료 체크박스
        with col_check:
            is_completed = st.checkbox("", value=task["완료"], key=f"check_{index}")
            if is_completed != task["완료"]:
                st.session_state.todo_list[index]["완료"] = is_completed
                st.rerun()
                
        # 일정 내용 (완료 시 취소선 효과 대신 텍스트 색상 등으로 구분 가능)
        with col_text:
            if task["완료"]:
                st.markdown(f"~~{task['일정']}~~")
            else:
                st.markdown(f"**{task['일정']}**")
                
        # 기한 및 중요도 표시
        with col_date:
            st.caption(f"📅 {task['기한']}")
        with col_priority:
            st.caption(task["중요도"])
            
        # 삭제 버튼
        with col_del:
            if st.button("🗑️", key=f"del_{index}"):
                st.session_state.todo_list.pop(index)
                st.rerun()
                
    # 7. 전체 데이터 테이블 보기 (접기/펼치기 기능)
    with st.expander("📊 한눈에 데이터 모아보기"):
        df = pd.DataFrame(st.session_state.todo_list)
        if not df.empty:
            st.dataframe(df, use_container_width=True)
