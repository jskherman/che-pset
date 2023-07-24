import pandas as pd
import streamlit as st

st.set_page_config(page_title="QnA", page_icon="📚")
# st.title("QnA")

@st.cache_data
def get_data():
    qna_csv = st.secrets["QNA_CSV"]
    df = pd.read_csv(qna_csv)
    df.dropna(inplace=True, axis=0, subset=["Question", "Answer"])
    for index, row in df.iterrows():
        row["Choices"] = [item.strip() for item in row["Choices"].split(";")]
        row["Tags"] = [item.strip() for item in row["Tags"].split(";")]
        df["Choices"][index] = row["Choices"]
        df["Tags"][index] = row["Tags"]
    return df

@st.cache_data
def get_tag_list(df: pd.DataFrame) -> list:
    tags = {x for l in df["Tags"] for x in l}
    return list(tags)

def load_fanfare():
    import base64

    fanfare_file = open("assets/fanfare.mp3", "rb")
    fanfare_html = f'\n<audio autoplay class="stAudio">\n<source src="data:audio/ogg;base64,{(base64.b64encode(fanfare_file.read()).decode())}" type="audio/mp3">\nYour browser does not support the audio element.\n</audio>'
    return fanfare_html

def generate_50_set(df, tags):
    filtered_df = df[df["Tags"].apply(lambda x: any(item in x for item in selected_tags))].copy()
    filtered_df.sort_values(by="ID").reset_index(inplace=True, drop=True)
    filtered_df = filtered_df.sample(n=50, replace=False).sort_values(by="ID")
    filtered_df.reset_index(inplace=True, drop=True)
    for index, row in filtered_df.iterrows():
        # Create Question Number
        filtered_df.loc[index, "QNum"] = f"Q-{index + 1}"
    filtered_df["Correct"] = False
    filtered_df["Done"] = False
    filtered_df = filtered_df[["ID", "QNum", "Correct", "Done", "Question", "Choices", "Answer", "Tags"]]
    return filtered_df.copy()


df = get_data()
tags = get_tag_list(df)

with st.expander("**Problem Set Generator** ⚙", expanded=True):
    selected_tags = st.multiselect("Select Tags", tags, default=["PCP"])
    filtered_df = df[df["Tags"].apply(lambda x: any(item in x for item in selected_tags))].copy()
    filtered_df.sort_values(by="ID").reset_index(inplace=True, drop=True)

    if len(filtered_df) == 0:
        st.error("**No questions found!** Please select some tags.", icon="❗")
        # st.button("Generate Problem Set", disabled=True)
    else:
        if len(filtered_df) > 1:
            num_questions = st.slider("Number of questions to generate:", min_value=1, max_value=len(filtered_df), value=len(filtered_df))
            filtered_df = filtered_df.sample(n=num_questions, replace=False).sort_values(by="ID")
        else:
            st.info("&emsp;**Only _:red[one]_ question found.**", icon="ℹ️")

        filtered_df.reset_index(inplace=True, drop=True)
        for index, row in filtered_df.iterrows():
            # Create Question Number
            filtered_df.loc[index, "QNum"] = f"Q-{index + 1}"
        filtered_df["Correct"] = False
        filtered_df["Done"] = False
        filtered_df = filtered_df[["ID", "QNum", "Correct", "Done", "Question", "Choices", "Answer", "Tags"]]

        # st.divider()
        if st.button("Generate!", type="primary"):
            st.session_state["problem_set"] = filtered_df.copy()
            st.balloons()
            st.toast(f"**:blue[{str(len(filtered_df)).zfill(1)} Questions] generated.**  \nProblem Set ready!", icon="🎉")

# st.divider()

# st.subheader("Quick Configs")

# acol1, acol2, _fill1 = st.columns(3)
# with acol1:
#     set_pcp = st.button("Generate **50 PCP Problems**", key="pcp")
#     set_gen = st.button("Generate **50 GEN Problems**", key="gen")

# with acol2:
#     set_che = st.button("Generate **50 CHE Problems**", key="che")
#     set_mix = st.button("Generate **50 MIX Problems**", key="mix")

# if set_pcp:
#     set_tags = ["PCP"]
#     st.session_state["problem_set"] = generate_50_set(df, set_tags)
#     st.balloons()
#     st.toast("**:blue[50 Questions] generated.**  \nProblem Set ready!", icon="🎉")
# elif set_gen:
#     set_tags = ["GEN"]
#     st.session_state["problem_set"] = generate_50_set(df, set_tags)
#     st.balloons()
#     st.toast("**:blue[50 Questions] generated.**  \nProblem Set ready!", icon="🎉")
# elif set_che:
#     set_tags = ["CHE"]
#     st.session_state["problem_set"] = generate_50_set(df, set_tags)
#     st.balloons()
#     st.toast("**:blue[50 Questions] generated.**  \nProblem Set ready!", icon="🎉")
# elif set_mix:
#     set_tags = ["PCP", "GEN", "CHE"]
#     st.session_state["problem_set"] = generate_50_set(df, set_tags)
#     st.balloons()
#     st.toast("**:blue[50 Questions] generated.**  \nProblem Set ready!", icon="🎉")

# st.session_state["problem_set"]

# Secret Settings

st.subheader("Secret Settings")

password = st.text_input("Enter Password:", type="password")


# Sidebar settings
with st.sidebar:
    with st.expander("**Other Settings** ⚙", expanded=True):
        audio_on = st.checkbox("🔊 **Enable Fanfare?**", value=True)

if audio_on:
    st.session_state["fanfare"] = load_fanfare()
else:
    st.session_state["fanfare"] = ""
st.session_state["playsound"] = audio_on