import streamlit as st
from google import genai
from google.genai import types
from google.genai.errors import APIError

# 페이지 설정
st.set_page_config(page_title="신비로운 타로 챗봇", page_icon="🔮")
st.title("🔮 AI 타로 마스터")
st.caption("고민을 말씀하시면 타로 카드의 리딩을 통해 조언을 해드립니다.")

# 1. Secrets에서 API 키 불러오기
try:
    api_key = st.secrets["GEMINI_API_KEY"]
except KeyError:
    st.error("🔑 API 키를 찾을 수 없습니다. Streamlit Secrets 설정을 확인해주세요.")
    st.stop()

# 2. 세션 상태(채팅 기록 및 클라이언트) 초기화
# ★ 핵심: client와 chat_session을 세션 상태에 함께 묶어서 유지합니다.
if "client" not in st.session_state:
    st.session_state.client = genai.Client(api_key=api_key)

if "messages" not in st.session_state:
    st.session_state.messages = []
    
if "chat_session" not in st.session_state:
    system_instruction = (
        "당신은 신비롭고 공감 능력이 뛰어난 전문 타로 카드 마스터입니다. "
        "사용자가 고민을 이야기하면, 타로 카드를 스프레드(뽑기)하여 그 의미를 "
        "현재 상황, 조언, 미래의 가능성으로 나누어 친절하고 깊이 있게 설명해주세요. "
        "신비로운 분위기를 풍기는 말투를 사용하되, 지나치게 부정적인 예언보다는 "
        "사용자에게 위로와 통찰을 줄 수 있는 방향으로 리딩해야 합니다."
    )
    
    # 세션에 저장된 client를 사용하여 chat 생성
    st.session_state.chat_session = st.session_state.client.chats.create(
        model="gemini-2.5-flash-lite",
        config=types.GenerateContentConfig(
            system_instruction=system_instruction,
            temperature=0.7,
        )
    )

# 3. 기존 대화 기록 화면에 표시
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. 사용자 입력 처리
if user_input := st.chat_input("오늘 어떤 고민에 대해 타로를 보고 싶으신가요?"):
    # 사용자 메시지 표시 및 기록
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    # AI 응답 생성 및 오류 처리
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        with st.spinner("타로 카드를 섞고 리딩하는 중... 🃏"):
            try:
                # 대화 기록이 연동된 세션을 통해 메시지 전송
                response = st.session_state.chat_session.send_message(user_input)
                ai_response = response.text
                
                # 결과 출력 및 기록
                message_placeholder.markdown(ai_response)
                st.session_state.messages.append({"role": "assistant", "content": ai_response})
                
            except APIError as e:
                st.error(f"Gemini API 오류가 발생했습니다: {e.message}")
            except Exception as e:
                st.error(f"알 수 없는 오류가 발생했습니다: {str(e)}")
