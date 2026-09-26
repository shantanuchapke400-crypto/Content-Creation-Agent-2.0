import streamlit as st

from dotenv import load_dotenv

from frontend.api_client import APIClient


# ============================================================
# Configuration
# ============================================================

load_dotenv()

st.set_page_config(
    page_title="CreatorOS AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ============================================================
# Session State
# ============================================================

if "token" not in st.session_state:
    st.session_state.token = None

if "user" not in st.session_state:
    st.session_state.user = None

if "projects" not in st.session_state:
    st.session_state.projects = []

if "active_project" not in st.session_state:
    st.session_state.active_project = None

if "last_generation" not in st.session_state:
    st.session_state.last_generation = None

if "generation_history" not in st.session_state:
    st.session_state.generation_history = []

if "generation_history_project_id" not in st.session_state:
    st.session_state.generation_history_project_id = None

if "selected_history_generation" not in st.session_state:
    st.session_state.selected_history_generation = None


# ============================================================
# Styling
# ============================================================

def load_css():
    try:
        with open("style.css", encoding="utf-8") as file:
            st.markdown(
                f"<style>{file.read()}</style>",
                unsafe_allow_html=True,
            )
    except FileNotFoundError:
        pass


# ============================================================
# Authentication
# ============================================================

def logout():
    st.session_state.token = None
    st.session_state.user = None
    st.session_state.projects = []
    st.session_state.active_project = None
    st.session_state.last_generation = None
    st.session_state.generation_history = []
    st.session_state.generation_history_project_id = None
    st.session_state.selected_history_generation = None
    st.rerun()


def login_page():
    st.title("🤖 CreatorOS AI")

    st.markdown(
        """
        <div style="
            text-align:center;
            color:#CBD5E1;
            font-size:18px;
            margin-bottom:30px;
        ">
            Your AI Content Creation Workspace
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.subheader("Login")

    username = st.text_input(
        "Username",
        key="login_username",
    )

    password = st.text_input(
        "Password",
        type="password",
        key="login_password",
    )

    if st.button(
        "Login",
        use_container_width=True,
        type="primary",
    ):
        if not username.strip() or not password:
            st.warning("Please enter username and password.")
            return

        api_client = APIClient()

        with st.spinner("Signing you in..."):
            response = api_client.login(
                username=username.strip(),
                password=password,
            )

        if response.status_code == 200:
            data = response.json()

            st.session_state.token = data["access_token"]
            st.session_state.user = data["user"]
            st.session_state.projects = []
            st.session_state.active_project = None
            st.session_state.last_generation = None
            st.session_state.generation_history = []
            st.session_state.generation_history_project_id = None
            st.session_state.selected_history_generation = None

            st.rerun()

        else:
            try:
                detail = response.json().get(
                    "detail",
                    "Login failed.",
                )
            except Exception:
                detail = "Login failed."

            st.error(detail)


# ============================================================
# Project Management
# ============================================================

def load_projects():
    api_client = APIClient(
        token=st.session_state.token,
    )

    try:
        response = api_client.get_projects()
    except Exception as error:
        st.error(f"Unable to connect to CreatorOS API: {error}")
        return False

    if response.status_code == 200:
        data = response.json()

        st.session_state.projects = data.get(
            "projects",
            [],
        )

        return True

    if response.status_code == 401:
        logout()
        return False

    st.error(
        f"Unable to load projects: {response.text}"
    )

    return False


def create_project():
    project_name = st.session_state.get(
        "new_project_name",
        "",
    ).strip()

    project_description = st.session_state.get(
        "new_project_description",
        "",
    ).strip()

    if not project_name:
        st.warning("Please enter a project name.")
        return

    api_client = APIClient(
        token=st.session_state.token,
    )

    try:
        response = api_client.create_project(
            name=project_name,
            description=project_description,
        )
    except Exception as error:
        st.error(f"Unable to connect to CreatorOS API: {error}")
        return

    if response.status_code in (200, 201):
        project = response.json()

        st.session_state.projects.append(project)
        st.session_state.active_project = project

        st.success(
            f"Project '{project['name']}' created successfully!"
        )

        st.session_state.new_project_name = ""
        st.session_state.new_project_description = ""

        st.rerun()

    elif response.status_code == 401:
        logout()

    else:
        st.error(
            f"Unable to create project: {response.text}"
        )


def delete_active_project():
    project = st.session_state.active_project

    if not project:
        st.warning("Please select a project first.")
        return

    api_client = APIClient(token=st.session_state.token)

    try:
        response = api_client.delete_project(project["id"])
    except Exception as error:
        st.error(f"Unable to connect to CreatorOS API: {error}")
        return

    if response.status_code in (200, 204):
        deleted_name = project.get("name", "Project")
        st.session_state.projects = [
            item for item in st.session_state.projects
            if item.get("id") != project.get("id")
        ]
        st.session_state.active_project = None
        st.session_state.last_generation = None
        st.session_state.generation_history = []
        st.session_state.generation_history_project_id = None
        st.session_state.selected_history_generation = None
        st.success(f"Project '{deleted_name}' deleted successfully.")
        st.rerun()

    elif response.status_code == 401:
        logout()

    else:
        st.error(f"Unable to delete project: {response.text}")


def project_workspace():
    st.subheader("📁 Your Projects")

    if not st.session_state.projects:
        st.info(
            "You don't have any projects yet. "
            "Create your first project to get started."
        )

    with st.expander("➕ Create New Project"):
        st.text_input(
            "Project name",
            placeholder="e.g. AI Content Studio",
            key="new_project_name",
        )

        st.text_area(
            "Description",
            placeholder="What will you create with this project?",
            key="new_project_description",
        )

        st.button(
            "Create Project",
            type="primary",
            use_container_width=True,
            on_click=create_project,
        )

    if not st.session_state.projects:
        return

    project_names = [
        project["name"]
        for project in st.session_state.projects
    ]

    active_project_id = None

    if st.session_state.active_project:
        active_project_id = st.session_state.active_project.get("id")

    default_index = 0

    for index, project in enumerate(st.session_state.projects):
        if project["id"] == active_project_id:
            default_index = index
            break

    selected_name = st.selectbox(
        "Active Project",
        project_names,
        index=default_index,
        key="active_project_selector",
    )

    selected_project = next(
        project
        for project in st.session_state.projects
        if project["name"] == selected_name
    )

    previous_project_id = (
        st.session_state.active_project.get("id")
        if st.session_state.active_project
        else None
    )

    if previous_project_id != selected_project["id"]:
        st.session_state.selected_history_generation = None

    st.session_state.active_project = selected_project

    st.caption(
        f"Active Project ID: {selected_project['id']}"
    )

    with st.expander("⚙️ Project Settings"):
        st.warning(
            "Deleting this project also removes its saved generations "
            "when the backend cascade is configured."
        )
        confirm_delete = st.checkbox(
            "I understand that this action cannot be undone.",
            key=f"confirm_delete_project_{selected_project['id']}",
        )
        if st.button(
            "🗑️ Delete Active Project",
            disabled=not confirm_delete,
            use_container_width=True,
        ):
            delete_active_project()


# ============================================================
# Generation History
# ============================================================

def load_generation_history(force=False):
    project = st.session_state.active_project

    if not project:
        st.session_state.generation_history = []
        st.session_state.generation_history_project_id = None
        return False

    project_id = project["id"]

    if (
        not force
        and st.session_state.generation_history_project_id == project_id
    ):
        return True

    api_client = APIClient(token=st.session_state.token)

    try:
        response = api_client.get_generations(project_id)
    except Exception as error:
        st.error(f"Unable to load generation history: {error}")
        return False

    if response.status_code == 200:
        data = response.json()

        if isinstance(data, list):
            generations = data
        else:
            generations = data.get("generations", [])

        generations.sort(
            key=lambda item: item.get("created_at", ""),
            reverse=True,
        )

        st.session_state.generation_history = generations
        st.session_state.generation_history_project_id = project_id
        return True

    if response.status_code == 401:
        logout()
        return False

    st.error(f"Unable to load generation history: {response.text}")
    return False


def open_generation(generation_id):
    project = st.session_state.active_project

    if not project:
        return

    api_client = APIClient(token=st.session_state.token)

    try:
        response = api_client.get_generation(
            project["id"],
            generation_id,
        )
    except Exception as error:
        st.error(f"Unable to open generation: {error}")
        return

    if response.status_code == 200:
        data = response.json()
        generation = data.get("generation", data)
        st.session_state.selected_history_generation = generation
        return

    if response.status_code == 401:
        logout()
        return

    st.error(f"Unable to open generation: {response.text}")


def delete_generation(generation_id):
    project = st.session_state.active_project

    if not project:
        return

    api_client = APIClient(token=st.session_state.token)

    try:
        response = api_client.delete_generation(
            project["id"],
            generation_id,
        )
    except Exception as error:
        st.error(f"Unable to delete generation: {error}")
        return

    if response.status_code in (200, 204):
        selected = st.session_state.selected_history_generation
        if selected and selected.get("id") == generation_id:
            st.session_state.selected_history_generation = None

        st.success("Generation deleted successfully.")
        load_generation_history(force=True)
        return

    if response.status_code == 401:
        logout()
        return

    st.error(f"Unable to delete generation: {response.text}")


def _generation_label(generation):
    content_type = generation.get("content_type", "Content")
    topic = generation.get("topic") or "Untitled generation"
    return f"{content_type.replace('_', ' ').title()} · {topic}"


def display_generation_history():
    project = st.session_state.active_project

    if not project:
        return

    load_generation_history()

    st.divider()
    st.subheader("📚 Generation History")

    history = st.session_state.generation_history

    if not history:
        st.info("No saved generations in this project yet.")
        return

    filter_col, search_col, refresh_col = st.columns([1.3, 2.7, 1])

    with filter_col:
        content_types = sorted({
            item.get("content_type", "unknown")
            for item in history
        })
        filter_options = ["All types"] + [
            value.replace("_", " ").title()
            for value in content_types
        ]
        selected_filter = st.selectbox(
            "Filter",
            filter_options,
            key="history_type_filter",
        )

    with search_col:
        search_term = st.text_input(
            "Search",
            placeholder="Search by topic or content type...",
            key="history_search",
        ).strip().lower()

    with refresh_col:
        st.write("")
        if st.button("🔄 Refresh", use_container_width=True):
            load_generation_history(force=True)
            st.rerun()

    filtered_history = []

    for generation in history:
        type_label = generation.get("content_type", "unknown").replace("_", " ").title()
        topic = (generation.get("topic") or "").lower()

        matches_filter = (
            selected_filter == "All types"
            or type_label == selected_filter
        )
        matches_search = (
            not search_term
            or search_term in topic
            or search_term in type_label.lower()
        )

        if matches_filter and matches_search:
            filtered_history.append(generation)

    st.caption(
        f"Showing {len(filtered_history)} of {len(history)} saved generation(s)."
    )

    if not filtered_history:
        st.warning("No generations match your current search/filter.")
        return

    for generation in filtered_history:
        generation_id = generation.get("id")
        label = _generation_label(generation)

        with st.container(border=True):
            meta_col, action_col = st.columns([5, 1])

            with meta_col:
                st.markdown(f"**{label}**")
                tone = generation.get("tone")
                if tone:
                    st.caption(f"Tone: {tone}")

            with action_col:
                if generation_id is not None:
                    if st.button(
                        "👁️ Open",
                        key=f"open_generation_{generation_id}",
                        use_container_width=True,
                    ):
                        open_generation(generation_id)
                        st.rerun()

            if generation_id is not None:
                delete_col, download_col = st.columns(2)

                with delete_col:
                    if st.button(
                        "🗑️ Delete",
                        key=f"delete_generation_{generation_id}",
                        use_container_width=True,
                    ):
                        delete_generation(generation_id)
                        st.rerun()

                with download_col:
                    output = generation.get("output_content", "")
                    st.download_button(
                        "📥 Download",
                        data=output,
                        file_name=f"generation_{generation_id}.txt",
                        mime="text/plain",
                        key=f"download_generation_{generation_id}",
                        use_container_width=True,
                    )

    selected = st.session_state.selected_history_generation

    if selected:
        st.divider()
        st.markdown(
            f"### 👁️ {_generation_label(selected)}"
        )
        st.caption(
            f"Tone: {selected.get('tone', 'Not specified')}"
        )
        st.markdown(
            "<div class='card'>",
            unsafe_allow_html=True,
        )
        st.write(selected.get("output_content", ""))
        st.markdown("</div>", unsafe_allow_html=True)

        if st.button("✖ Close generation", key="close_selected_generation"):
            st.session_state.selected_history_generation = None
            st.rerun()


# ============================================================
# Content Generation
# ============================================================

CONTENT_TYPE_MAP = {
    "Blog": "blog",
    "LinkedIn Post": "linkedin",
    "YouTube Script": "youtube",
    "Instagram Caption": "instagram",
    "Twitter/X Thread": "twitter",
    "Newsletter": "newsletter",
    "Email": "email",
    "Rewrite Content": "rewrite",
    "Summarize Content": "summarize",
    "Expand Content": "expand",
    "Humanize Content": "humanize",
    "SEO Title": "seo_title",
    "Meta Description": "meta_description",
}


def generate_project_content():
    active_project = st.session_state.active_project

    if not active_project:
        st.warning("Please create or select a project first.")
        return

    topic = st.session_state.get(
        "generation_topic",
        "",
    ).strip()

    content_type = st.session_state.get(
        "generation_content_type",
        "Blog",
    )

    tone = st.session_state.get(
        "generation_tone",
        "Professional",
    )

    input_content = st.session_state.get(
        "generation_input_content",
        "",
    ).strip()

    if not topic and content_type not in {
        "Rewrite Content",
        "Summarize Content",
        "Expand Content",
        "Humanize Content",
    }:
        st.warning("Please enter a topic.")
        return

    if content_type in {
        "Rewrite Content",
        "Summarize Content",
        "Expand Content",
        "Humanize Content",
    } and not input_content:
        st.warning("Please enter the content you want to process.")
        return

    api_content_type = CONTENT_TYPE_MAP.get(content_type)

    if not api_content_type:
        st.error(
            f"Unsupported content type: {content_type}"
        )
        return

    api_client = APIClient(
        token=st.session_state.token,
    )

    with st.spinner("✨ Creating your content..."):
        try:
            response = api_client.generate_content(
                project_id=active_project["id"],
                content_type=api_content_type,
                topic=topic,
                tone=tone,
                input_content=input_content,
            )
        except Exception as error:
            st.error(
                f"Unable to connect to CreatorOS API: {error}"
            )
            return

    if response.status_code == 200:
        data = response.json()

        st.session_state.last_generation = data["generation"]
        load_generation_history(force=True)

        st.success("Content generated successfully! 🎉")

    elif response.status_code == 401:
        logout()

    elif response.status_code == 400:
        try:
            detail = response.json().get(
                "detail",
                "Invalid generation request.",
            )
        except Exception:
            detail = "Invalid generation request."

        st.warning(detail)

    elif response.status_code == 503:
        st.error(
            "Gemini is temporarily unavailable. "
            "Please try again in a moment."
        )

    elif response.status_code == 429:
        st.error(
            "Gemini API quota has been exceeded."
        )

    else:
        st.error(
            f"Generation failed: {response.text}"
        )


def generation_workspace():
    st.subheader("✨ AI Content Studio")

    if not st.session_state.active_project:
        st.info(
            "Create or select a project above before generating content."
        )
        return

    st.caption(
        f"Generating inside: "
        f"**{st.session_state.active_project['name']}**"
    )

    topic = st.text_input(
        "📝 Topic",
        placeholder="e.g. Future of Artificial Intelligence",
        key="generation_topic",
    )

    col1, col2 = st.columns(2)

    with col1:
        st.selectbox(
            "📄 Content Type",
            list(CONTENT_TYPE_MAP.keys()),
            key="generation_content_type",
        )

    with col2:
        st.selectbox(
            "🎯 Writing Tone",
            [
                "Professional",
                "Friendly",
                "Educational",
                "Storytelling",
                "Marketing",
            ],
            key="generation_tone",
        )

    content_type = st.session_state.generation_content_type

    if content_type in {
        "Rewrite Content",
        "Summarize Content",
        "Expand Content",
        "Humanize Content",
    }:
        st.text_area(
            "📄 Content to process",
            placeholder="Paste your existing content here...",
            height=220,
            key="generation_input_content",
        )

    st.write("")

    st.button(
        "🚀 Generate Content",
        use_container_width=True,
        type="primary",
        on_click=generate_project_content,
    )


# ============================================================
# Generation Result
# ============================================================

def display_generation():
    generation = st.session_state.last_generation

    if not generation:
        return

    st.divider()

    st.subheader("✨ Generated Content")

    st.markdown(
        "<div class='card'>",
        unsafe_allow_html=True,
    )

    st.write(
        generation.get(
            "output_content",
            "",
        )
    )

    st.markdown(
        "</div>",
        unsafe_allow_html=True,
    )

    st.download_button(
        label="📥 Download Content",
        data=generation.get(
            "output_content",
            "",
        ),
        file_name=(
            f"{generation.get('content_type', 'content')}.txt"
        ),
        mime="text/plain",
    )


# ============================================================
# Main Application
# ============================================================

def main():
    load_css()

    if not st.session_state.token:
        login_page()
        return

    # Header
    header_col1, header_col2 = st.columns(
        [5, 1],
        vertical_alignment="center",
    )

    with header_col1:
        st.title("🤖 CreatorOS AI")

    with header_col2:
        username = (
            st.session_state.user.get("username", "User")
            if isinstance(st.session_state.user, dict)
            else "User"
        )

        st.caption(f"👤 {username}")

        if st.button("Logout"):
            logout()

    st.markdown(
        """
        <div style="
            text-align:center;
            color:#CBD5E1;
            font-size:18px;
            margin-top:-10px;
            margin-bottom:30px;
        ">
            Your AI Content Creation Workspace
            <br><br>
            Generate content with
            <span style="color:#60A5FA;font-weight:600;">
                Gemini
            </span>
            through the CreatorOS API
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.divider()

    # Load projects after authentication.
    if not st.session_state.projects:
        load_projects()

    # Project workspace.
    project_workspace()

    st.divider()

    # Content workspace.
    generation_workspace()

    # Latest generated content.
    display_generation()

    # Saved generations for the active project.
    display_generation_history()


if __name__ == "__main__":
    main()