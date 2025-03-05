import streamlit as st

from pathlib import Path

from src.common.common import page_setup, save_params
from src.mzmlfileworkflow import result_section, run_workflow
from src.queue_1 import add_process_to_queue
from rq import Queue
from redis import Redis
from rq_scheduler import Scheduler
from datetime import datetime, timedelta
# from tasks2 import simple_job

# Page name "workflow" will show mzML file selector in sidebar
params = page_setup()

st.title("Workflow")
st.markdown(
    """
More complex workflow with mzML files and input form.
             
Changing widgets within the form will not trigger the execution of the script immediatly.
This is great for large parameter sections.
"""
)


# def run():
#     print('running? 2')
#     mzmlfileworkflow.run_workflow(params, result_dir)

with st.form("workflow-with-mzML-form"):
    st.markdown("**Parameters**")
    
    file_options = [f.stem for f in Path(st.session_state.workspace, "mzML-files").glob("*.mzML") if "external_files.txt" not in f.name]
    
    # Check if local files are available
    external_files = Path(Path(st.session_state.workspace, "mzML-files"), "external_files.txt")
    if external_files.exists():
        with open(external_files, "r") as f_handle:
            external_files = f_handle.readlines()
            external_files = [str(Path(f.strip()).with_suffix('')) for f in external_files]
            file_options += external_files

    st.multiselect(
        "**input mzML files**",
        file_options,
        params["example-workflow-selected-mzML-files"],
        key="example-workflow-selected-mzML-files",
    )

    c1, _, c3 = st.columns(3)
    if c1.form_submit_button(
        "Save Parameters", help="Save changes made to parameter section."
    ):
        params = save_params(params)
    run_workflow_button = c3.form_submit_button("Run Workflow", type="primary")

result_dir = Path(st.session_state["workspace"], "mzML-workflow-results")

if run_workflow_button:
    params = save_params(params)
    if params["example-workflow-selected-mzML-files"]:
        queue = Queue(connection=Redis())
        job = queue.enqueue(run_workflow, params, result_dir)
        # st.success(f"Workflow queued with job ID: {job.id} {job.get_status()} {len(list(queue.get_jobs()))}")
    else:
        st.warning("Select some mzML files.")



result_section(result_dir)