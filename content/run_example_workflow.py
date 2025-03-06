import streamlit as st

from pathlib import Path

from src.common.common import page_setup, save_params
from src import mzmlfileworkflow, stats
from rq import Queue
from redis import Redis
import time

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

def get_workflow_progress_logs(job_id):
    r = Redis()
    return r.lrange(f"workflow_progress_logs:{job_id}", 0, -1)

if run_workflow_button:
    params = save_params(params)
    if params["example-workflow-selected-mzML-files"]:
        queue = Queue('mzml_workflow_run', connection=Redis())
        job = queue.enqueue(mzmlfileworkflow.run_workflow, params, result_dir, st.session_state["workspace"])
        with st.status("Workflow in progress...", expanded=True) as status:
            last_len = 0
            # read logs till job is running
            while not job.is_finished:
                logs = get_workflow_progress_logs(job.id)

                if len(logs) > last_len:
                    # read from the last read log
                    for log in logs[last_len:]:
                        st.write(log.decode('utf-8'))
                    last_len = len(logs)

                time.sleep(1)
            
            if job.is_finished:
                status.update(label="Workflow complete!", expanded=False, state='complete')
            else:
                status.update(label="Workflow stopped!", expanded=False, state='error')

    else:
        st.warning("Select some mzML files.")


mzmlfileworkflow.result_section(result_dir)