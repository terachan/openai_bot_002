
import streamlit as st
import openai

# Streamlit Community Cloudの「Secrets」からOpenAI API keyを取得
openai.api_key = st.secrets.OpenAIAPI.openai_api_key

system_prompt = """
あなたは東京都内のレストランを熟知した食通です。
20人くらいで立食ディナー(一人あたり予算5000円から8000円)ができる都内のレストランを提案することができます。
特にアクセンチュアオフィス近郊の赤坂や麻布、六本木近辺のレストランを優先的に紹介してください。
飲み放題コースがあることは必須の条件としてください。
あなたの役割はレストランを薦めることなので、例えば以下のようなレストラン以外ことを聞かれても、絶対に答えないでください。

* 旅行
* 芸能人
* 映画
* 科学
* 歴史
* 医療

また東京都以外のレストランを聞かれても絶対に答えないで下さい。
"""

# st.session_stateを使いメッセージのやりとりを保存
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": system_prompt}
        ]

# チャットボットとやりとりする関数
def communicate():
    messages = st.session_state["messages"]

    user_message = {"role": "user", "content": st.session_state["user_input"]}
    messages.append(user_message)

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )  

    bot_message = response["choices"][0]["message"]
    messages.append(bot_message)

    st.session_state["user_input"] = ""  # 入力欄を消去


# ユーザーインターフェイスの構築
st.title("都内のレストランを薦めてくれるチャットボット")
st.image("01_recipe.png")
st.write("どんなレストランが良いですか？")

user_input = st.text_input("メッセージを入力してください。", key="user_input", on_change=communicate)

if st.session_state["messages"]:
    messages = st.session_state["messages"]

    for message in reversed(messages[1:]):  # 直近のメッセージを上に
        speaker = "🙂"
        if message["role"]=="assistant":
            speaker="🤖"

        st.write(speaker + ": " + message["content"])
