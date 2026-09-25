import streamlit as st

from app.auth.database import (
    create_employee,
    get_all_employees,
    update_employee_status,
    update_employee_permissions,
)


# ============================================================
# EMPLOYEE MANAGEMENT
# ============================================================

def render_employee_management(admin_id):
    """
    Admin-only employee management interface.

    Allows administrators to:
    - Create employee accounts
    - View employee details
    - Update permissions
    - Activate/deactivate accounts
    """

    st.subheader("👥 Employee Management")

    st.write(
        "Create and manage employee accounts, "
        "permissions and account status."
    )

    # ========================================================
    # DASHBOARD
    # ========================================================

    employees = get_all_employees()

    total_employees = len(employees)

    active_employees = sum(
        1
        for employee in employees
        if employee["status"] == "active"
    )

    pending_employees = sum(
        1
        for employee in employees
        if employee["status"] == "pending"
    )

    inactive_employees = sum(
        1
        for employee in employees
        if employee["status"] == "inactive"
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Total Employees",
            total_employees,
        )

    with col2:
        st.metric(
            "Active",
            active_employees,
        )

    with col3:
        st.metric(
            "Pending",
            pending_employees,
        )

    with col4:
        st.metric(
            "Inactive",
            inactive_employees,
        )

    st.divider()

    # ========================================================
    # ADD EMPLOYEE
    # ========================================================

    with st.expander(
        "➕ Add New Employee",
        expanded=False,
    ):

        with st.form(
            "add_employee_form",
            clear_on_submit=True,
        ):

            col1, col2 = st.columns(2)

            with col1:

                employee_id = st.text_input(
                    "Employee ID *",
                    placeholder="Example: EMP002",
                )

                employee_name = st.text_input(
                    "Full Name *",
                    placeholder="Example: Arun Kumar",
                )

                employee_email = st.text_input(
                    "Email *",
                    placeholder="employee@company.local",
                )

            with col2:

                department = st.text_input(
                    "Department",
                    placeholder="Example: Maintenance",
                )

                designation = st.text_input(
                    "Designation",
                    placeholder="Example: Engineer",
                )

                st.markdown(
                    "**Initial Permissions**"
                )

                permission_ai = st.checkbox(
                    "AI Workbench",
                    value=True,
                )

                permission_documents = st.checkbox(
                    "Documents",
                    value=False,
                )

                permission_reports = st.checkbox(
                    "Reports",
                    value=False,
                )

                permission_code_execution = st.checkbox(
                    "Code Execution",
                    value=False,
                )

                permission_sensitive_documents = st.checkbox(
                    "Sensitive Documents",
                    value=False,
                )

            submitted = st.form_submit_button(
                "Create Employee Account",
                type="primary",
                use_container_width=True,
            )

        if submitted:

            if not employee_id.strip():

                st.error(
                    "Employee ID is required."
                )

            elif not employee_name.strip():

                st.error(
                    "Employee name is required."
                )

            elif not employee_email.strip():

                st.error(
                    "Employee email is required."
                )

            else:

                try:

                    result = create_employee(
                        employee_id=employee_id.strip(),
                        name=employee_name.strip(),
                        email=employee_email.strip(),
                        department=(
                            department.strip()
                            or None
                        ),
                        designation=(
                            designation.strip()
                            or None
                        ),
                        created_by=admin_id,
                        permission_ai=permission_ai,
                        permission_documents=(
                            permission_documents
                        ),
                        permission_reports=(
                            permission_reports
                        ),
                        permission_code_execution=(
                            permission_code_execution
                        ),
                        permission_sensitive_documents=(
                            permission_sensitive_documents
                        ),
                    )

                    if result:

                        st.success(
                            f"Employee {employee_id.strip()} "
                            "created successfully."
                        )

                        st.info(
                            "The employee account is pending "
                            "first-time activation. The employee "
                            "will create their own password."
                        )

                        st.rerun()

                    else:

                        st.error(
                            "Employee account could not be created."
                        )

                except Exception as error:

                    error_message = str(error)

                    if "UNIQUE" in error_message.upper():

                        st.error(
                            "Employee ID or email already exists."
                        )

                    else:

                        st.error(
                            "Failed to create employee account."
                        )

                        st.exception(error)

    # ========================================================
    # EMPLOYEE LIST
    # ========================================================

    st.subheader(
        "📋 Employee Directory"
    )

    employees = get_all_employees()

    if not employees:

        st.info(
            "No employee accounts have been created yet."
        )

        return

    search = st.text_input(
        "🔎 Search employees",
        placeholder=(
            "Search by employee ID, name, email "
            "or department..."
        ),
        key="employee_search",
    )

    filtered_employees = employees

    if search.strip():

        search_text = search.strip().lower()

        filtered_employees = [
            employee
            for employee in employees
            if (
                search_text
                in str(
                    employee["employee_id"]
                ).lower()
                or search_text
                in str(
                    employee["name"]
                ).lower()
                or search_text
                in str(
                    employee["email"]
                ).lower()
                or search_text
                in str(
                    employee["department"] or ""
                ).lower()
            )
        ]

    if not filtered_employees:

        st.info(
            "No employees match your search."
        )

        return

    # ========================================================
    # EMPLOYEE RECORDS
    # ========================================================

    for employee in filtered_employees:

        employee_id = employee["employee_id"]

        status = employee["status"]

        with st.container(
            border=True
        ):

            col1, col2 = st.columns(
                [4, 1]
            )

            with col1:

                st.markdown(
                    f"### 👤 {employee['name']}"
                )

                st.caption(
                    f"Employee ID: {employee_id}"
                )

                st.write(
                    f"**Email:** {employee['email']}"
                )

                if employee["department"]:

                    st.write(
                        f"**Department:** "
                        f"{employee['department']}"
                    )

                if employee["designation"]:

                    st.write(
                        f"**Designation:** "
                        f"{employee['designation']}"
                    )

                st.write(
                    f"**Status:** `{status}`"
                )

                if employee["last_login"]:

                    st.caption(
                        f"Last login: "
                        f"{employee['last_login']}"
                    )

                else:

                    st.caption(
                        "Last login: Never"
                    )

            with col2:

                if status == "active":

                    if st.button(
                        "Deactivate",
                        key=f"deactivate_{employee_id}",
                    ):

                        update_employee_status(
                            employee_id,
                            "inactive",
                        )

                        st.success(
                            "Employee deactivated."
                        )

                        st.rerun()

                elif status == "inactive":

                    if st.button(
                        "Activate",
                        key=f"activate_employee_{employee_id}",
                    ):

                        update_employee_status(
                            employee_id,
                            "active",
                        )

                        st.success(
                            "Employee activated."
                        )

                        st.rerun()

                else:

                    st.info(
                        "Pending activation"
                    )

            # ==================================================
            # PERMISSIONS
            # ==================================================

            st.markdown(
                "#### 🛂 Permissions"
            )

            permission_columns = st.columns(5)

            current_ai = bool(
                employee["permission_ai"]
            )

            current_documents = bool(
                employee["permission_documents"]
            )

            current_reports = bool(
                employee["permission_reports"]
            )

            current_code = bool(
                employee["permission_code_execution"]
            )

            current_sensitive = bool(
                employee[
                    "permission_sensitive_documents"
                ]
            )

            with permission_columns[0]:

                new_ai = st.checkbox(
                    "AI",
                    value=current_ai,
                    key=f"perm_ai_{employee_id}",
                )

            with permission_columns[1]:

                new_documents = st.checkbox(
                    "Documents",
                    value=current_documents,
                    key=f"perm_documents_{employee_id}",
                )

            with permission_columns[2]:

                new_reports = st.checkbox(
                    "Reports",
                    value=current_reports,
                    key=f"perm_reports_{employee_id}",
                )

            with permission_columns[3]:

                new_code = st.checkbox(
                    "Code",
                    value=current_code,
                    key=f"perm_code_{employee_id}",
                )

            with permission_columns[4]:

                new_sensitive = st.checkbox(
                    "Sensitive",
                    value=current_sensitive,
                    key=f"perm_sensitive_{employee_id}",
                )

            if st.button(
                "💾 Save Permissions",
                key=f"save_permissions_{employee_id}",
            ):

                update_employee_permissions(
                    employee_id=employee_id,
                    permission_ai=new_ai,
                    permission_documents=new_documents,
                    permission_reports=new_reports,
                    permission_code_execution=new_code,
                    permission_sensitive_documents=(
                        new_sensitive
                    ),
                )

                st.success(
                    "Permissions updated."
                )

                st.rerun()
