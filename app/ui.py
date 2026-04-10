import streamlit as st
from app.matcher import ResumeMatcher


def show_results(matcher: ResumeMatcher, job_desc: str):
    with st.spinner("Ranking resumes..."):
        ranked = matcher.rank_resumes(job_desc)
    if not ranked:
        st.warning("No resumes found.")
        return
    st.success(f"Found {len(ranked)} relevant candidates")
    for idx, candidate in enumerate(ranked, 1):
        with st.expander(
            f"#{idx} – {candidate['resume'].split('/')[-1]} (Score: {candidate['score']:.2f})"
        ):
            st.markdown("Preview:")
            st.write(candidate["content"])
            if st.button(f"Summarise {idx}", key=f"sum_{idx}"):
                summary = matcher.generate_summary(candidate["content"])
                st.info(summary)
