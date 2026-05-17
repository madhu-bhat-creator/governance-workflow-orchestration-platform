import streamlit as st
import pandas as pd
from openai import OpenAI

# OpenAI Client
client = OpenAI(
    api_key=st.secrets["OPENAI_API_KEY"]
)

# App Title
st.title("AI Prototype: Governance Workflow & Remediation Orchestration Platform")

st.write("""
This prototype explores AI-driven governance remediation,
workflow orchestration and human-in-the-loop approval simulation.
""")

# Upload CSV
uploaded_file = st.file_uploader(
    "Upload Governance Dataset",
    type=["csv"]
)

if uploaded_file:

    # Read CSV
    df = pd.read_csv(uploaded_file)

    st.subheader("Uploaded Governance Data")
    st.dataframe(df)

    findings = []

    # Governance analysis
    for index, row in df.iterrows():

        risk_score = 0
        issues = []

        # Ownership issue
        if row["owner_assigned"] == "no":
            risk_score += 30
            issues.append("Missing ownership")

        # Lineage issue
        if row["lineage_complete"] == "no":
            risk_score += 30
            issues.append("Lineage gap")

        # Stale controls
        if row["control_review_days"] > 365:
            risk_score += 20
            issues.append("Stale governance controls")

        # Duplicate datasets
        if row["duplicate_dataset"] == "yes":
            risk_score += 20
            issues.append("Duplicate dataset")

        # Regulatory criticality
        if row["regulatory_criticality"] == "high":
            risk_score += 40
            issues.append("High regulatory exposure")

        # Workflow routing
        workflow_status = "Open"

        if risk_score >= 60:
            workflow_status = "Pending Approval"

        # Automation eligibility
        automation_mode = "Auto-Remediate"

        if row["regulatory_criticality"] == "high":
            automation_mode = "Human Approval Required"

        findings.append({
            "dataset": row["dataset"],
            "risk_score": risk_score,
            "issues": ", ".join(issues),
            "workflow_status": workflow_status,
            "automation_mode": automation_mode
        })

    risk_df = pd.DataFrame(findings)

    # Display findings
    st.subheader("Governance Workflow Findings")

    st.dataframe(risk_df)

    # High risk issues
    high_risk = risk_df[risk_df["risk_score"] >= 60]

    st.subheader("High-Risk Governance Issues")

    st.dataframe(high_risk)

    # Metrics
    st.metric(
        "High-Risk Governance Issues",
        len(high_risk)
    )

    # Governance score
    avg_score = 100 - int(risk_df["risk_score"].mean())

    st.metric(
        "Governance Health Score",
        f"{avg_score}/100"
    )

    # Chart
    st.bar_chart(
        high_risk.set_index("dataset")["risk_score"]
    )

    # Workflow simulation
    st.subheader("Workflow Actions")

    selected_dataset = st.selectbox(
        "Select Dataset",
        risk_df["dataset"]
    )

    action = st.selectbox(
        "Select Workflow Action",
        [
            "Approve Remediation",
            "Escalate Issue",
            "Assign Steward",
            "Close Issue"
        ]
    )

    if st.button("Execute Workflow Action"):

        st.success(
            f"{action} executed successfully for {selected_dataset}"
        )

    # AI Governance Insights
    st.subheader("AI Governance Workflow Insights")

    summary = high_risk.to_string(index=False)

    prompt = f"""
    Analyze the following governance workflow findings.

    Identify:
    - governance weaknesses
    - ownership gaps
    - remediation bottlenecks
    - workflow inefficiencies
    - operational governance risks

    Recommend:
    - remediation priorities
    - governance workflow improvements
    - escalation strategies
    - ownership accountability enhancements
    - automation opportunities
    - human approval requirements

    Findings:
    {summary}
    """

    with st.spinner("Generating AI governance insights..."):

        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are a senior enterprise governance and remediation orchestration expert."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.3
        )

        output = response.choices[0].message.content

        st.write(output)
