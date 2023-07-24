import pandas as pd
import streamlit as st

from App import load_fanfare

st.set_page_config(page_title="Quiz :: Problem Set Generator", page_icon="📝")

if "problem_set" not in st.session_state:
    st.error("**No problem set found!** Please generate a problem set first.", icon="❗")
    st.stop()

pset = st.session_state["problem_set"]

if "index" not in st.session_state:
    st.session_state["index"] = 0

def set_question(setmode):
    if setmode == "next":
        if st.session_state["index"] < (len(pset) - 1):
            st.session_state["index"] = pset.index[pset["QNum"] == question].tolist()[0] + 1
        else:
            st.session_state["index"] = 0
    elif setmode == "prev":
        if st.session_state["index"] > 0:
            st.session_state["index"] = pset.index[pset["QNum"] == question].tolist()[0] - 1
        else:
            st.session_state["index"] = (len(pset) - 1)
    else:
        st.session_state["index"] = pset.index[pset["QNum"] == setmode].tolist()[0]


st.progress(value=(sum(pset["Done"])) / len(pset), text=f"**Progress:&ensp;:blue[{sum(pset['Done'])}] / {len(pset)}**")

nav1, _fill1, nav2, _fill2, nav3 = st.columns([1, 1, 3, 1, 1])

question = pset.iloc[st.session_state["index"]]["QNum"]

# Create navigation buttons



with nav1:
    if st.button("< Prev"):
        set_question("prev")

with nav3:
    if st.button("Next >"):
        set_question("next")

with nav2:
    question = st.selectbox("Question", pset["QNum"].values, index=st.session_state["index"])
    set_question(question)

correct_answer = pset.loc[pset["QNum"] == question, "Answer"].values[0].strip()

with st.form("Question Form"):

    st.subheader(question.replace("Q-", "Question #"))
    st.markdown(pset.loc[pset["QNum"] == question, "Question"].values[0])
    # st.markdown(
    #     f"""
    #     <details><summary style='font-size: 1.2em'>Reveal Answer</summary>
    #     <br>

    #     <div style='font-size: 1.25em;'><b>
        
    #     ##### :green[{pset.loc[pset["QNum"] == question, "Answer"].values[0]}]
    #     </b></div>
    #     </details>
    #     """,
    #     unsafe_allow_html=True
    # )

    answer = st.radio("**Select Answer**:", pset.loc[pset["QNum"] == question, "Choices"].values[0])
    done_status = pset.loc[pset["QNum"] == question, "Done"].values[0]

    if st.form_submit_button("Submit Answer", disabled=done_status):
        if answer == correct_answer:
            pset.loc[pset["QNum"] == question, "Correct"] = True
        else:
            pset.loc[pset["QNum"] == question, "Correct"] = False
        pset.loc[pset["QNum"] == question, "Done"] = True
        st.session_state["problem_set"] = pset.copy()

        set_question("next")
        st.experimental_rerun()

    if done_status:
        st.info("&emsp;**You have already answered this question. Proceed to the next question.**", icon="ℹ️")


if pset["Done"].all():
    if (sum(pset["Correct"]) == len(pset)): #and (len(pset) > 50):
        st.markdown(load_fanfare(9999), unsafe_allow_html=True)
    else:
        st.markdown(st.session_state["fanfare"], unsafe_allow_html=True)
    st.balloons()
    st.toast("**NICE JOB!**  \nYou completed the problem set!", icon="🎉")
    

with st.sidebar:
    st.info("If it does not navigate properly,  \npress **R** to REFRESH.")
    st.dataframe(pset[["QNum", "Done"]].rename(columns={"QNum": "Question", "Done": "Done?"}).set_index("Question"), width=150)


# pset