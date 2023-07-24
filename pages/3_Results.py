import datetime as dt

import altair as alt
import gspread
import pandas as pd
import streamlit as st


@st.cache_data
def generate_plot_data(df):
    df = df[["ID", "QNum", "Correct", "Streak"]]
    for row, index in df.iterrows():
        df.loc[row, "Correct"] = "Correct" if index["Correct"] else "Incorrect"
        df.loc[row, "QNum"] = index["QNum"].replace("Q-", "")
    return df

@st.cache_data
def generate_streak_info(results, col:str = "Correct"):
    
    data = results[col].to_frame()
    data["start_of_streak"] = data[col].ne(data[col].shift())
    data["streak_id"] = data.start_of_streak.cumsum()
    data["Streak"] = data.groupby("streak_id").cumcount() + 1
    df = pd.concat([results, data["Streak"]], axis=1)
    for index, row in df.iterrows():
        if row[col]:
            df.loc[index, "Streak"] = row["Streak"]
        else:
            df.loc[index, "Streak"] = 0
    return df

@st.cache_data
def generate_runchart(runchartdf):
    runchart = alt.Chart(runchartdf).mark_point(filled=True, size=400).encode(
        x=alt.X("QNum", title="Question Number", axis=alt.Axis(labelAngle=0)),
        y=alt.Y("Correct", title=""),
        color=alt.Color("Correct", scale=alt.Scale(domain=["Correct", "Incorrect"], range=["green", "red"]), legend=None),
        tooltip=[alt.Tooltip("QNum", title="Question No"), alt.Tooltip("Correct", title="Status"), alt.Tooltip("Streak", title="Streak")],
        shape=alt.Shape("Correct", scale=alt.Scale(domain=["Correct", "Incorrect"], range=['circle', 'triangle-up'])),
    ).properties(
        height=200
    ).interactive()

    return runchart

@st.cache_data
def write_incorrect_questions(incorrect):
    incorrect_strings = []
    if st.session_state["auth"]:
        for index, row in incorrect.iterrows():
            string = (
                f"""
<details><summary style='font-size: 1.2em;'>{row["QNum"].replace("Q-", "Question #")}</summary>
<br>

[#{row["ID"]}]({st.secrets["GSHEETS_URL"]}{row["ID"]+1}) {row["Question"]}

|            |                               |
| :--------- | :---------------------------- |
| **Answer** | {row["Answer"]}               |
| **Tags**   | {',&ensp;'.join(row["Tags"])} |
<hr>
</details>
                """
            )
            incorrect_strings.append(string)
    else:
        for index, row in incorrect.iterrows():
            string = (
                f"""
<details><summary style='font-size: 1.2em;'>{row["QNum"].replace("Q-", "Question #")}</summary>
<br>

{row["Question"]}

|            |                               |
| :--------- | :---------------------------- |
| **Answer** | {row["Answer"]}               |
| **Tags**   | {',&ensp;'.join(row["Tags"])} |
<hr>
</details>
                """
            )
            incorrect_strings.append(string)
    return incorrect_strings

if "problem_set" not in st.session_state:
    st.error("**No problem set found!** Please generate a problem set first.", icon="❗")
    st.stop()
if not st.session_state["problem_set"]["Done"].all():
    st.error("**Please complete the quiz first!**", icon="❗")
    st.stop()

st.set_page_config(page_title="Results :: Problem Set Generator", page_icon="🏆")

gc = gspread.service_account_from_dict(st.secrets["GSHEETS_CREDS"])
sh = gc.open("Board Review")
ws = sh.worksheet("PS Data")

results = generate_streak_info(st.session_state["problem_set"].copy(), col="Correct")
# results
runchartdf = generate_plot_data(results)

with st.expander("Result Summary", expanded=True):
    rs1, rs2, rs3 = st.columns(3)

    with rs1:
        st.metric("Score", f"{sum(results['Correct'])} / {len(results)}")
    with rs2:
        st.metric("Accuracy", f"{round(sum(results['Correct']) / len(results) * 100, 2)}%")
    with rs3:
        # Show metric for highest streak of correct questions from cumulative sum of correct answers column
        st.metric("Highest Streak", f"{max(results['Streak'])}")
        

# Generate altair scatter plot of correct and incorrect items vs question number, change symbol to checkmark or cross
st.markdown("#### Run Chart")
runchart = generate_runchart(runchartdf)

st.altair_chart(runchart, use_container_width=True)

st.divider()

#  Generate list of questions that were answered incorrectly
st.markdown(f"#### Incorrect Questions: :red[{len(results) - sum(results['Correct'])}]")
incorrect = results[results["Correct"] == False]
incorrect = incorrect[["ID", "QNum", "Question", "Answer", "Tags"]]
incorrect_qid_list = [str(id) for id in incorrect["ID"].tolist()].copy()
incorrect_qid_list.sort()
incorrect_qid_list = '; '.join(incorrect_qid_list)
incorrect_tags_list = '; '.join(list(set([item for sublist in incorrect["Tags"].tolist() for item in sublist])))
incorrect_strings = write_incorrect_questions(incorrect)
for q_string in incorrect_strings:
    st.markdown(q_string, unsafe_allow_html=True)

with st.sidebar:
    if st.session_state["auth"]:
        with st.form("Save Results"):
            duration = st.number_input("Run Duration (secs)", min_value=1, step=1)
            run_tags = '; '.join(list(set([item for sublist in results["Tags"].tolist() for item in sublist])))

            result_list = [
                dt.datetime.now().strftime("%Y-%m-%d"),
                sum(results['Correct']),
                len(results),
                duration,
                '=(INDIRECT("RC[-3]",FALSE))/INDIRECT("RC[-2]",FALSE)',
                '=(INDIRECT("RC[-4]",FALSE)+1)/(INDIRECT("RC[-3]",FALSE)+2)',
                max(results['Streak']),
                run_tags,
                incorrect_qid_list,
                incorrect_tags_list
            ]

            if st.form_submit_button("Save Results"):
                ws.append_rows([result_list], value_input_option="USER_ENTERED")
                st.balloons()
                st.toast("**Results saved!**", icon="🎉")

