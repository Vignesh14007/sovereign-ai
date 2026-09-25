import streamlit as st

from app.knowledge.service import (
    get_dashboard_stats,
    list_documents,
    upload_document,
    archive_document,
    activate_document,
    delete_document,
)
from app.admin.employee_management import (
    render_employee_management,
)

def render_admin_panel():
    """
    Render the Sovereign AI Admin Panel.

    The panel manages local company knowledge records.
    """

    st.markdown(
        """
        <div style="
            padding: 10px 0 25px 0;
        ">
            <div style="
                font-size: 32px;
                font-weight: 700;
            ">
                🔐 Admin Panel
            </div>

            <div style="
                color: #888;
                font-size: 15px;
                margin-top: 5px;
            ">
                Knowledge & Records Management
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ========================================================
    # DASHBOARD
    # ========================================================

    stats = get_dashboard_stats()

    st.subheader("Knowledge Base")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Documents",
            stats["total"],
        )

    with col2:
        st.metric(
            "Active",
            stats["active"],
        )

    with col3:
        st.metric(
            "Archived",
            stats["archived"],
        )

    with col4:
        st.metric(
            "Processing",
            stats["processing"],
        )

    st.divider()

    # ========================================================
    # EMPLOYEE MANAGEMENT
    # ========================================================

    render_employee_management(
        admin_id="ADM001"
    )

    st.divider()

    # ========================================================
    # UPLOAD
    # ========================================================

    st.subheader("📤 Add Company Document")

    uploaded_file = st.file_uploader(
        "Upload a company document",
        type=[
            "pdf",
            "txt",
            "docx",
        ],
        key="admin_document_uploader",
    )

    category = st.selectbox(
        "Category",
        [
            "SOP",
            "Maintenance",
            "Inspection",
            "Safety",
            "Technical Manual",
            "Policy",
            "Company Report",
            "Other",
        ],
        key="admin_category",
    )

    department = st.text_input(
        "Department",
        placeholder="Example: Maintenance",
        key="admin_department",
    )

    equipment = st.text_input(
        "Equipment",
        placeholder="Example: Compressor C-204",
        key="admin_equipment",
    )

    description = st.text_area(
        "Description",
        placeholder="Short description of the document...",
        height=90,
        key="admin_description",
    )

    version = st.text_input(
        "Version",
        value="1.0",
        key="admin_version",
    )

    upload_button = st.button(
        "Process & Add to Knowledge Base",
        type="primary",
        use_container_width=True,
    )

    if upload_button:

        if uploaded_file is None:

            st.warning(
                "Please select a document first."
            )

        else:

            try:

                # Store the uploaded file temporarily.
                temp_dir = (
                    "data/knowledge/admin_uploads"
                )

                from pathlib import Path

                temp_path = (
                    Path(temp_dir)
                    / uploaded_file.name
                )

                temp_path.parent.mkdir(
                    parents=True,
                    exist_ok=True,
                )

                temp_path.write_bytes(
                    uploaded_file.getbuffer()
                )

                with st.spinner(
                    "Processing document..."
                ):

                    result = upload_document(
                        file_path=temp_path,
                        category=category,
                        department=department.strip()
                        or None,
                        equipment=equipment.strip()
                        or None,
                        description=description.strip()
                        or None,
                        uploaded_by="admin",
                        version=version.strip()
                        or "1.0",
                    )

                st.success(
                    f"Document added successfully: "
                    f"{result['document_id']}"
                )

                st.info(
                    f"Created {result['chunk_count']} "
                    f"searchable knowledge chunks."
                )

                st.rerun()

            except Exception as error:

                st.error(
                    "Document processing failed."
                )

                st.exception(error)

    st.divider()

    # ========================================================
    # DOCUMENT MANAGEMENT
    # ========================================================

    st.subheader("📚 Managed Documents")

    documents = list_documents(
        include_archived=True
    )

    if not documents:

        st.info(
            "No company documents have been added yet."
        )

    else:

        for document in documents:

            document_id = document["document_id"]

            status = document["status"]

            with st.container(
                border=True
            ):

                col1, col2 = st.columns(
                    [4, 1]
                )

                with col1:

                    st.markdown(
                        f"### {document['name']}"
                    )

                    st.caption(
                        f"ID: {document_id}"
                    )

                    st.write(
                        f"**Category:** "
                        f"{document['category']}"
                    )

                    if document["department"]:

                        st.write(
                            f"**Department:** "
                            f"{document['department']}"
                        )

                    if document["equipment"]:

                        st.write(
                            f"**Equipment:** "
                            f"{document['equipment']}"
                        )

                    st.write(
                        f"**Version:** "
                        f"{document['version']}"
                    )

                    st.write(
                        f"**Chunks:** "
                        f"{document['chunk_count']}"
                    )

                    st.write(
                        f"**Status:** "
                        f"{status}"
                    )

                    st.caption(
                        f"Updated: "
                        f"{document['updated_at']}"
                    )

                with col2:

                    if status == "active":

                        if st.button(
                            "Archive",
                            key=f"archive_{document_id}",
                        ):

                            try:

                                archive_document(
                                    document_id
                                )

                                st.success(
                                    "Document archived."
                                )

                                st.rerun()

                            except Exception as error:

                                st.error(
                                    str(error)
                                )

                    elif status == "archived":

                        if st.button(
                            "Activate",
                            key=f"activate_{document_id}",
                        ):

                            try:

                                activate_document(
                                    document_id
                                )

                                st.success(
                                    "Document activated."
                                )

                                st.rerun()

                            except Exception as error:

                                st.error(
                                    str(error)
                                )

                    st.write("")

                    if st.button(
                        "Delete",
                        key=f"delete_{document_id}",
                    ):

                        st.session_state[
                            f"confirm_delete_{document_id}"
                        ] = True

                    if st.session_state.get(
                        f"confirm_delete_{document_id}",
                        False,
                    ):

                        st.warning(
                            "This permanently removes "
                            "the document and its chunks."
                        )

                        confirm = st.button(
                            "Confirm Delete",
                            key=f"confirm_{document_id}",
                        )

                        cancel = st.button(
                            "Cancel",
                            key=f"cancel_{document_id}",
                        )

                        if confirm:

                            try:

                                delete_document(
                                    document_id
                                )

                                st.session_state.pop(
                                    f"confirm_delete_{document_id}",
                                    None,
                                )

                                st.success(
                                    "Document deleted."
                                )

                                st.rerun()

                            except Exception as error:

                                st.error(
                                    str(error)
                                )

                        if cancel:

                            st.session_state.pop(
                                f"confirm_delete_{document_id}",
                                None,
                            )

                            st.rerun()
