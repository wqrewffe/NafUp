"""
🌟 Enhanced Personal Manager - Company Edition 🌟
Save this file as **app.py** and run with: streamlit run app.py
Features: User Management, Company/Group Management, Employee Task Assignment, Team Analytics, and much more!
"""

import streamlit as st
import json
import os
import datetime
from pathlib import Path
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from typing import Dict, List, Any, Optional, Tuple
import hashlib
import secrets
import uuid
import base64
import io
import time
import threading

# Configure page
st.set_page_config(
    page_title="Nafup - Personal & Team Manager 🏢",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for beautiful styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Dark mode styles */
    [data-testid="stAppViewContainer"] {
        background: var(--background-color, #ffffff);
        color: var(--text-color, #000000);
    }
    
    .dark-mode {
        --background-color: #1a1a1a;
        --text-color: #ffffff;
        --card-background: #2d2d2d;
        --border-color: #404040;
    }
    
    .light-mode {
        --background-color: #ffffff;
        --text-color: #000000;
        --card-background: #ffffff;
        --border-color: #e0e0e0;
    }
    
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 3rem 2rem;
        border-radius: 20px;
        text-align: center;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 20px 40px rgba(102, 126, 234, 0.3);
    }
    
    .login-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 4rem 3rem;
        border-radius: 25px;
        color: white;
        text-align: center;
        margin: 2rem auto;
        max-width: 600px;
        box-shadow: 0 25px 50px rgba(0,0,0,0.3);
        backdrop-filter: blur(10px);
    }
    
    .login-form {
        background: rgba(255,255,255,0.95);
        padding: 3rem;
        border-radius: 20px;
        margin: 2rem 0;
        box-shadow: 0 15px 35px rgba(0,0,0,0.1);
        backdrop-filter: blur(20px);
    }
    
    .welcome-header {
        text-align: center;
        padding: 3rem 2rem;
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        border-radius: 20px;
        margin-bottom: 2rem;
        box-shadow: 0 15px 35px rgba(102, 126, 234, 0.3);
    }
    
    .role-badge {
        display: inline-block;
        padding: 0.5rem 1rem;
        border-radius: 25px;
        font-size: 0.8rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .admin-badge {
        background: linear-gradient(45deg, #ff6b6b, #ee5a24);
        color: white;
    }
    
    .manager-badge {
        background: linear-gradient(45deg, #4834d4, #686de0);
        color: white;
    }
    
    .employee-badge {
        background: linear-gradient(45deg, #00d2d3, #01a3a4);
        color: white;
    }
    
    .personal-badge {
        background: linear-gradient(45deg, #2ed573, #1e90ff);
        color: white;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        padding: 2rem;
        border-radius: 15px;
        border-left: 5px solid #667eea;
        margin: 1rem 0;
        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
        transition: transform 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
    }
    
    .task-card {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        margin: 1rem 0;
        border-left: 5px solid #28a745;
        transition: all 0.3s ease;
    }
    
    .task-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 15px 40px rgba(0,0,0,0.15);
    }
    
    .high-priority {
        border-left-color: #ff4757 !important;
        background: linear-gradient(135deg, #fff5f5 0%, #ffe6e6 100%);
    }
    
    .medium-priority {
        border-left-color: #ffa726 !important;
        background: linear-gradient(135deg, #fffbf0 0%, #fff3e0 100%);
    }
    
    .low-priority {
        border-left-color: #26c6da !important;
        background: linear-gradient(135deg, #f0fdff 0%, #e0f7ff 100%);
    }
    
    .assigned-task {
        border-left-color: #9c27b0 !important;
        background: linear-gradient(135deg, #faf4ff 0%, #f3e5f5 100%);
    }
    
    .sidebar-section {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        padding: 2rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    }
    
    .company-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 20px;
        margin: 1rem 0;
        box-shadow: 0 15px 35px rgba(102, 126, 234, 0.3);
    }
    
    .employee-card {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
        border-left: 5px solid #667eea;
    }
    
    .notification-card {
        background: linear-gradient(135deg, #74b9ff 0%, #0984e3 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 10px 25px rgba(116, 185, 255, 0.3);
    }
    
    .success-message {
        background: linear-gradient(135deg, #00b894 0%, #00a085 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 10px 25px rgba(0, 184, 148, 0.3);
    }
    
    .warning-message {
        background: linear-gradient(135deg, #fdcb6e 0%, #e17055 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 10px 25px rgba(253, 203, 110, 0.3);
    }
    
    .error-message {
        background: linear-gradient(135deg, #ff7675 0%, #d63031 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 10px 25px rgba(255, 118, 117, 0.3);
    }
    
    .animated-button {
        background: linear-gradient(45deg, #667eea, #764ba2);
        color: white;
        border: none;
        padding: 1rem 2rem;
        border-radius: 25px;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .animated-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 15px 35px rgba(102, 126, 234, 0.4);
    }
    
    .stats-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 2rem;
        margin: 2rem 0;
    }
    
    .gradient-text {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-weight: 700;
    }
    
    .floating-card {
        background: white;
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 20px 40px rgba(0,0,0,0.1);
        margin: 1rem 0;
        position: relative;
        overflow: hidden;
    }
    
    .floating-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #667eea, #764ba2);
    }
    
    .team-header {
        background: linear-gradient(135deg, #a8e6cf 0%, #7fcdcd 100%);
        color: #2d3436;
        padding: 2rem;
        border-radius: 20px;
        text-align: center;
        margin: 2rem 0;
        box-shadow: 0 15px 35px rgba(168, 230, 207, 0.3);
    }
</style>
""", unsafe_allow_html=True)

# File paths
DATA_FILE = Path("users.json")
AUTH_FILE = Path("auth.json")
COMPANIES_FILE = Path("companies.json")
NOTIFICATIONS_FILE = Path("notifications.json")
CHAT_FILE = Path("chat_messages.json")
PRIVATE_CHAT_FILE = Path("private_chats.json")
FILES_FILE = Path("shared_files.json")
PRIVATE_FILES_FILE = Path("private_files.json")
CALENDAR_FILE = Path("calendar_events.json")
POLLS_FILE = Path("polls.json")
USER_STATUS_FILE = Path("user_status.json")
TASK_COMMENTS_FILE = Path("task_comments.json")
PINNED_MESSAGES_FILE = Path("pinned_messages.json")
TASK_ATTACHMENTS_FILE = Path("task_attachments.json")
PROJECTS_FILE = Path("projects.json")
DEPARTMENTS_FILE = Path("departments.json")
PERFORMANCE_FILE = Path("performance_reviews.json")
BUDGET_FILE = Path("budget_tracking.json")
REPORTS_FILE = Path("reports.json")
WORKFLOWS_FILE = Path("workflows.json")
KNOWLEDGE_BASE_FILE = Path("knowledge_base.json")
INTEGRATIONS_FILE = Path("integrations.json")

# -------------------------------------------------------------
# Enhanced Authentication Functions
# -------------------------------------------------------------
def hash_password(password: str) -> str:
    """Hash a password using SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()

def generate_company_code():
    """Generate a unique company code."""
    return str(uuid.uuid4())[:8].upper()

def load_auth_data():
    """Load authentication data."""
    if not AUTH_FILE.exists():
        AUTH_FILE.write_text("{}", encoding="utf-8")
    
    with AUTH_FILE.open("r", encoding="utf-8") as f:
        return json.load(f)

def save_auth_data(auth_data: dict):
    """Save authentication data."""
    with AUTH_FILE.open("w", encoding="utf-8") as f:
        json.dump(auth_data, f, indent=2, ensure_ascii=False)

def load_companies_data():
    """Load companies data."""
    if not COMPANIES_FILE.exists():
        COMPANIES_FILE.write_text("{}", encoding="utf-8")
    
    with COMPANIES_FILE.open("r", encoding="utf-8") as f:
        return json.load(f)

def save_companies_data(companies_data: dict):
    """Save companies data."""
    with COMPANIES_FILE.open("w", encoding="utf-8") as f:
        json.dump(companies_data, f, indent=2, ensure_ascii=False)

def load_notifications_data():
    """Load notifications data."""
    if not NOTIFICATIONS_FILE.exists():
        NOTIFICATIONS_FILE.write_text("{}", encoding="utf-8")
    
    with NOTIFICATIONS_FILE.open("r", encoding="utf-8") as f:
        return json.load(f)

def save_notifications_data(notifications_data: dict):
    """Save notifications data."""
    with NOTIFICATIONS_FILE.open("w", encoding="utf-8") as f:
        json.dump(notifications_data, f, indent=2, ensure_ascii=False)

def load_chat_data():
    """Load chat messages data."""
    if not CHAT_FILE.exists():
        CHAT_FILE.write_text("{}", encoding="utf-8")
    
    with CHAT_FILE.open("r", encoding="utf-8") as f:
        return json.load(f)

def save_chat_data(chat_data: dict):
    """Save chat messages data."""
    with CHAT_FILE.open("w", encoding="utf-8") as f:
        json.dump(chat_data, f, indent=2, ensure_ascii=False)

def load_private_chat_data():
    """Load private chat messages data."""
    if not PRIVATE_CHAT_FILE.exists():
        PRIVATE_CHAT_FILE.write_text("{}", encoding="utf-8")
    
    with PRIVATE_CHAT_FILE.open("r", encoding="utf-8") as f:
        return json.load(f)

def save_private_chat_data(private_chat_data: dict):
    """Save private chat messages data."""
    with PRIVATE_CHAT_FILE.open("w", encoding="utf-8") as f:
        json.dump(private_chat_data, f, indent=2, ensure_ascii=False)

def load_files_data():
    """Load shared files data."""
    if not FILES_FILE.exists():
        FILES_FILE.write_text("{}", encoding="utf-8")
    
    with FILES_FILE.open("r", encoding="utf-8") as f:
        return json.load(f)

def save_files_data(files_data: dict):
    """Save shared files data."""
    with FILES_FILE.open("w", encoding="utf-8") as f:
        json.dump(files_data, f, indent=2, ensure_ascii=False)

def load_private_files_data():
    """Load private files data."""
    if not PRIVATE_FILES_FILE.exists():
        PRIVATE_FILES_FILE.write_text("{}", encoding="utf-8")
    
    with PRIVATE_FILES_FILE.open("r", encoding="utf-8") as f:
        return json.load(f)

def save_private_files_data(private_files_data: dict):
    """Save private files data."""
    with PRIVATE_FILES_FILE.open("w", encoding="utf-8") as f:
        json.dump(private_files_data, f, indent=2, ensure_ascii=False)

def load_calendar_data():
    """Load calendar events data."""
    if not CALENDAR_FILE.exists():
        CALENDAR_FILE.write_text("{}", encoding="utf-8")
    
    with CALENDAR_FILE.open("r", encoding="utf-8") as f:
        return json.load(f)

def save_calendar_data(calendar_data: dict):
    """Save calendar events data."""
    with CALENDAR_FILE.open("w", encoding="utf-8") as f:
        json.dump(calendar_data, f, indent=2, ensure_ascii=False)

def load_polls_data():
    """Load polls data."""
    if not POLLS_FILE.exists():
        POLLS_FILE.write_text("{}", encoding="utf-8")
    
    with POLLS_FILE.open("r", encoding="utf-8") as f:
        return json.load(f)

def save_polls_data(polls_data: dict):
    """Save polls data."""
    with POLLS_FILE.open("w", encoding="utf-8") as f:
        json.dump(polls_data, f, indent=2, ensure_ascii=False)

def load_user_status_data():
    """Load user status data."""
    if not USER_STATUS_FILE.exists():
        USER_STATUS_FILE.write_text("{}", encoding="utf-8")
    
    with USER_STATUS_FILE.open("r", encoding="utf-8") as f:
        return json.load(f)

def save_user_status_data(user_status_data: dict):
    """Save user status data."""
    with USER_STATUS_FILE.open("w", encoding="utf-8") as f:
        json.dump(user_status_data, f, indent=2, ensure_ascii=False)

def load_task_comments_data():
    """Load task comments data."""
    if not TASK_COMMENTS_FILE.exists():
        TASK_COMMENTS_FILE.write_text("{}", encoding="utf-8")
    
    with TASK_COMMENTS_FILE.open("r", encoding="utf-8") as f:
        return json.load(f)

def save_task_comments_data(task_comments_data: dict):
    """Save task comments data."""
    with TASK_COMMENTS_FILE.open("w", encoding="utf-8") as f:
        json.dump(task_comments_data, f, indent=2, ensure_ascii=False)

def load_pinned_messages_data():
    """Load pinned messages data."""
    if not PINNED_MESSAGES_FILE.exists():
        PINNED_MESSAGES_FILE.write_text("{}", encoding="utf-8")
    
    with PINNED_MESSAGES_FILE.open("r", encoding="utf-8") as f:
        return json.load(f)

def save_pinned_messages_data(pinned_messages_data: dict):
    """Save pinned messages data."""
    with PINNED_MESSAGES_FILE.open("w", encoding="utf-8") as f:
        json.dump(pinned_messages_data, f, indent=2, ensure_ascii=False)

def load_task_attachments_data():
    """Load task attachments data."""
    if not TASK_ATTACHMENTS_FILE.exists():
        TASK_ATTACHMENTS_FILE.write_text("{}", encoding="utf-8")
    
    with TASK_ATTACHMENTS_FILE.open("r", encoding="utf-8") as f:
        return json.load(f)

def save_task_attachments_data(task_attachments_data: dict):
    """Save task attachments data."""
    with TASK_ATTACHMENTS_FILE.open("w", encoding="utf-8") as f:
        json.dump(task_attachments_data, f, indent=2, ensure_ascii=False)

# -------------------------------------------------------------
# Advanced Management Functions
# -------------------------------------------------------------
def load_projects_data():
    """Load projects data."""
    if not PROJECTS_FILE.exists():
        PROJECTS_FILE.write_text("{}", encoding="utf-8")
    
    with PROJECTS_FILE.open("r", encoding="utf-8") as f:
        return json.load(f)

def save_projects_data(projects_data: dict):
    """Save projects data."""
    with PROJECTS_FILE.open("w", encoding="utf-8") as f:
        json.dump(projects_data, f, indent=2, ensure_ascii=False)

def load_departments_data():
    """Load departments data."""
    if not DEPARTMENTS_FILE.exists():
        DEPARTMENTS_FILE.write_text("{}", encoding="utf-8")
    
    with DEPARTMENTS_FILE.open("r", encoding="utf-8") as f:
        return json.load(f)

def save_departments_data(departments_data: dict):
    """Save departments data."""
    with DEPARTMENTS_FILE.open("w", encoding="utf-8") as f:
        json.dump(departments_data, f, indent=2, ensure_ascii=False)

def load_performance_data():
    """Load performance reviews data."""
    if not PERFORMANCE_FILE.exists():
        PERFORMANCE_FILE.write_text("{}", encoding="utf-8")
    
    with PERFORMANCE_FILE.open("r", encoding="utf-8") as f:
        return json.load(f)

def save_performance_data(performance_data: dict):
    """Save performance reviews data."""
    with PERFORMANCE_FILE.open("w", encoding="utf-8") as f:
        json.dump(performance_data, f, indent=2, ensure_ascii=False)

def load_budget_data():
    """Load budget tracking data."""
    if not BUDGET_FILE.exists():
        BUDGET_FILE.write_text("{}", encoding="utf-8")
    
    with BUDGET_FILE.open("r", encoding="utf-8") as f:
        return json.load(f)

def save_budget_data(budget_data: dict):
    """Save budget tracking data."""
    with BUDGET_FILE.open("w", encoding="utf-8") as f:
        json.dump(budget_data, f, indent=2, ensure_ascii=False)

def load_reports_data():
    """Load reports data."""
    if not REPORTS_FILE.exists():
        REPORTS_FILE.write_text("{}", encoding="utf-8")
    
    with REPORTS_FILE.open("r", encoding="utf-8") as f:
        return json.load(f)

def save_reports_data(reports_data: dict):
    """Save reports data."""
    with REPORTS_FILE.open("w", encoding="utf-8") as f:
        json.dump(reports_data, f, indent=2, ensure_ascii=False)

def load_workflows_data():
    """Load workflows data."""
    if not WORKFLOWS_FILE.exists():
        WORKFLOWS_FILE.write_text("{}", encoding="utf-8")
    
    with WORKFLOWS_FILE.open("r", encoding="utf-8") as f:
        return json.load(f)

def save_workflows_data(workflows_data: dict):
    """Save workflows data."""
    with WORKFLOWS_FILE.open("w", encoding="utf-8") as f:
        json.dump(workflows_data, f, indent=2, ensure_ascii=False)

def load_knowledge_base_data():
    """Load knowledge base data."""
    if not KNOWLEDGE_BASE_FILE.exists():
        KNOWLEDGE_BASE_FILE.write_text("{}", encoding="utf-8")
    
    with KNOWLEDGE_BASE_FILE.open("r", encoding="utf-8") as f:
        return json.load(f)

def save_knowledge_base_data(knowledge_base_data: dict):
    """Save knowledge base data."""
    with KNOWLEDGE_BASE_FILE.open("w", encoding="utf-8") as f:
        json.dump(knowledge_base_data, f, indent=2, ensure_ascii=False)

def load_integrations_data():
    """Load integrations data."""
    if not INTEGRATIONS_FILE.exists():
        INTEGRATIONS_FILE.write_text("{}", encoding="utf-8")
    
    with INTEGRATIONS_FILE.open("r", encoding="utf-8") as f:
        return json.load(f)

def save_integrations_data(integrations_data: dict):
    """Save integrations data."""
    with INTEGRATIONS_FILE.open("w", encoding="utf-8") as f:
        json.dump(integrations_data, f, indent=2, ensure_ascii=False)

def register_user(username: str, password: str, email: str, full_name: str, role: str = "personal", company_code: Optional[str] = None) -> Tuple[bool, str]:
    """Register a new user with enhanced role support."""
    auth_data = load_auth_data()
    
    # Check if username already exists
    if username in auth_data:
        return False, "Username already exists!"
    
    # Check if email already exists
    for user_data in auth_data.values():
        if user_data.get("email") == email:
            return False, "Email already registered!"
    
    # Validate company code if provided
    if company_code:
        companies_data = load_companies_data()
        if company_code not in companies_data:
            return False, "Invalid company code!"
    
    # Create new user
    user_id = str(uuid.uuid4())
    auth_data[username] = {
        "user_id": user_id,
        "password_hash": hash_password(password),
        "email": email,
        "full_name": full_name,
        "role": role,
        "company_code": company_code,
        "created_at": get_current_timestamp(),
        "last_login": None,
        "active": True
    }
    
    save_auth_data(auth_data)
    
    # Add user to company if company code provided
    if company_code:
        companies_data = load_companies_data()
        if "employees" not in companies_data[company_code]:
            companies_data[company_code]["employees"] = []
        companies_data[company_code]["employees"].append({
            "username": username,
            "user_id": user_id,
            "full_name": full_name,
            "email": email,
            "role": role,
            "joined_at": get_current_timestamp(),
            "active": True
        })
        save_companies_data(companies_data)
    
    # Create user data file
    user_data = {
        "tasks": [],
        "notes": [],
        "contacts": [],
        "goals": [],
        "assigned_tasks": [],
        "team_notifications": [],
        "categories": ["Work", "Personal", "Health", "Learning", "Finance", "Team"],
        "settings": {
            "theme": "light",
            "notifications": True,
            "notification_sound": True,
            "notification_popup": True,
            "default_priority": "medium",
            "show_team_tasks": True
        }
    }
    
    user_file = Path(f"user_{username}.json")
    with user_file.open("w", encoding="utf-8") as f:
        json.dump(user_data, f, indent=2, ensure_ascii=False)
    
    return True, "Registration successful!"

def create_company(company_name: str, description: str, admin_username: str) -> tuple[bool, str]:
    """Create a new company."""
    companies_data = load_companies_data()
    company_code = generate_company_code()
    
    # Ensure unique company code
    while company_code in companies_data:
        company_code = generate_company_code()
    
    companies_data[company_code] = {
        "name": company_name,
        "description": description,
        "admin_username": admin_username,
        "created_at": get_current_timestamp(),
        "employees": [],
        "departments": ["General", "HR", "IT", "Sales", "Marketing", "Finance"],
        "company_settings": {
            "allow_self_registration": True,
            "require_approval": False,
            "default_employee_role": "employee"
        }
    }
    
    save_companies_data(companies_data)
    return True, company_code

def authenticate_user(username: str, password: str) -> tuple[bool, str]:
    """Authenticate a user."""
    auth_data = load_auth_data()
    
    if username not in auth_data:
        return False, "Username not found!"
    
    user_data = auth_data[username]
    if not user_data.get("active", True):
        return False, "Account is deactivated!"
    
    if user_data["password_hash"] != hash_password(password):
        return False, "Invalid password!"
    
    # Update last login
    auth_data[username]["last_login"] = get_current_timestamp()
    save_auth_data(auth_data)
    
    return True, "Login successful!"

def get_user_info(username: str) -> dict:
    """Get user information."""
    auth_data = load_auth_data()
    return auth_data.get(username, {})

def get_user_company_info(username: str) -> dict:
    """Get user's company information."""
    user_info = get_user_info(username)
    company_code = user_info.get("company_code")
    
    if not company_code:
        return {}
    
    companies_data = load_companies_data()
    company_data = companies_data.get(company_code, {})
    
    # Add the company code to the returned data
    if company_data:
        company_data["code"] = company_code
    
    return company_data

def get_company_employees(company_code: str) -> list:
    """Get all employees of a company."""
    companies_data = load_companies_data()
    company_data = companies_data.get(company_code, {})
    return company_data.get("employees", [])

def is_admin_or_manager(username: str) -> bool:
    """Check if user is admin or manager."""
    user_info = get_user_info(username)
    return user_info.get("role") in ["admin", "manager"]

def can_create_tasks(username: str) -> bool:
    """Check if user can create new tasks (only admins)."""
    user_info = get_user_info(username)
    company_info = get_user_company_info(username)
    
    # Only company admin can create tasks
    if company_info.get("admin_username") == username:
        return True
    
    # Check if user has admin role
    if user_info.get("role", "").lower() == "admin":
        return True
    
    return False

def can_assign_tasks(username: str) -> bool:
    """Check if user can assign tasks to others (seniors can assign to juniors)."""
    user_info = get_user_info(username)
    company_info = get_user_company_info(username)
    
    # Company admin can assign tasks
    if company_info.get("admin_username") == username:
        return True
    
    # Check if user has admin role
    if user_info.get("role", "").lower() == "admin":
        return True
    
    # Senior roles can assign tasks to juniors
    user_role = user_info.get("role", "employee")
    user_level = get_role_level(user_role)
    
    # Allow assignment if user has a senior role (level 3 and above)
    if user_level >= 3:
        return True
    
    return False

def can_assign_task_to_user(assigner_username: str, target_username: str) -> bool:
    """Check if a user can assign tasks to a specific target user."""
    assigner_info = get_user_info(assigner_username)
    target_info = get_user_info(target_username)
    
    if not assigner_info or not target_info:
        return False
    
    assigner_role = assigner_info.get("role", "employee")
    target_role = target_info.get("role", "employee")
    
    # Admin can assign to anyone
    if assigner_role.lower() == "admin":
        return True
    
    # Check if assigner can manage the target's role (hierarchy-based)
    return can_manage_role(assigner_role, target_role)

# -------------------------------------------------------------
# Enhanced Notification Functions
# -------------------------------------------------------------

def get_notification_sound(notification_type: str) -> int:
    """Get the appropriate sound frequency for notification type."""
    # Different frequencies for different notification types
    frequencies = {
        "task": 800,      # Higher pitch for tasks
        "file": 600,      # Medium pitch for files
        "poll": 1000,     # High pitch for polls
        "calendar": 400,  # Lower pitch for calendar
        "chat": 1200,     # Highest pitch for chat
        "project": 700,   # Medium-high for projects
        "performance": 500,  # Medium for performance
        "success": 900,   # High for success
        "warning": 300,   # Low for warnings
        "error": 200,     # Very low for errors
        "info": 600       # Default medium pitch
    }
    return frequencies.get(notification_type, 600)

def get_notification_icon(notification_type: str) -> str:
    """Get the appropriate icon for notification type."""
    icons = {
        "task": "📋",
        "file": "📁",
        "poll": "📊",
        "calendar": "📅",
        "chat": "💬",
        "project": "📈",
        "performance": "📊",
        "success": "✅",
        "warning": "⚠️",
        "error": "❌",
        "info": "ℹ️"
    }
    return icons.get(notification_type, "🔔")

def get_notification_color(notification_type: str) -> str:
    """Get the appropriate color for notification type."""
    colors = {
        "task": "#4CAF50",
        "file": "#2196F3",
        "poll": "#FF9800",
        "calendar": "#9C27B0",
        "chat": "#00BCD4",
        "project": "#607D8B",
        "performance": "#795548",
        "success": "#4CAF50",
        "warning": "#FF9800",
        "error": "#F44336",
        "info": "#2196F3"
    }
    return colors.get(notification_type, "#2196F3")

def show_notification_popup(notification: dict):
    """Show a notification popup with sound."""
    notification_type = notification.get("type", "info")
    title = notification.get("title", "Notification")
    message = notification.get("message", "No message")
    icon = get_notification_icon(notification_type)
    color = get_notification_color(notification_type)
    frequency = get_notification_sound(notification_type)
    
    # Check if sound should be disabled
    sound_disabled = notification.get("_disable_sound", False)
    
    # Create popup HTML with Web Audio API sound
    popup_html = f"""
    <div id="notification-popup" style="
        position: fixed;
        top: 20px;
        right: 20px;
        background: white;
        border-left: 4px solid {color};
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        border-radius: 8px;
        padding: 16px;
        max-width: 350px;
        z-index: 10000;
        animation: slideIn 0.3s ease-out;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    ">
        <div style="display: flex; align-items: flex-start; gap: 12px;">
            <div style="font-size: 24px;">{icon}</div>
            <div style="flex: 1;">
                <h4 style="margin: 0 0 8px 0; color: #333; font-size: 16px; font-weight: 600;">{title}</h4>
                <p style="margin: 0; color: #666; font-size: 14px; line-height: 1.4;">{message}</p>
                <small style="color: #999; font-size: 12px;">{notification.get('created_at', 'Now')}</small>
            </div>
            <button onclick="this.parentElement.parentElement.remove()" style="
                background: none;
                border: none;
                font-size: 18px;
                cursor: pointer;
                color: #999;
                padding: 0;
                margin: 0;
            ">×</button>
        </div>
    </div>
    
    <style>
    @keyframes slideIn {{
        from {{
            transform: translateX(100%);
            opacity: 0;
        }}
        to {{
            transform: translateX(0);
            opacity: 1;
        }}
    }}
    
    @keyframes slideOut {{
        from {{
            transform: translateX(0);
            opacity: 1;
        }}
        to {{
            transform: translateX(100%);
            opacity: 0;
        }}
    }}
    </style>
    
    <script>
    {f'''
    // Play notification sound using Web Audio API
    (function() {{
        try {{
            // Create audio context
            var audioContext = new (window.AudioContext || window.webkitAudioContext)();
            
            // Create oscillator for notification sound
            var oscillator = audioContext.createOscillator();
            var gainNode = audioContext.createGain();
            
            // Configure sound
            oscillator.frequency.setValueAtTime({frequency}, audioContext.currentTime);
            oscillator.type = 'sine';
            
            // Configure volume envelope
            gainNode.gain.setValueAtTime(0, audioContext.currentTime);
            gainNode.gain.linearRampToValueAtTime(0.3, audioContext.currentTime + 0.01);
            gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.3);
            
            // Connect nodes
            oscillator.connect(gainNode);
            gainNode.connect(audioContext.destination);
            
            // Play sound
            oscillator.start(audioContext.currentTime);
            oscillator.stop(audioContext.currentTime + 0.3);
            
        }} catch (error) {{
            console.log('Audio playback failed:', error);
        }}
    }})();
    ''' if not sound_disabled else '// Sound disabled for this notification'}
    
    // Auto-hide popup after 5 seconds
    setTimeout(function() {{
        var popup = document.getElementById('notification-popup');
        if (popup) {{
            popup.style.animation = 'slideOut 0.3s ease-in';
            setTimeout(function() {{
                if (popup && popup.parentNode) {{
                    popup.parentNode.removeChild(popup);
                }}
            }}, 300);
        }}
    }}, 5000);
    </script>
    """
    
    st.markdown(popup_html, unsafe_allow_html=True)

def check_and_show_new_notifications(username: str):
    """Check for new notifications and show popups."""
    if "last_notification_check" not in st.session_state:
        st.session_state["last_notification_check"] = {}
    
    if "shown_notifications" not in st.session_state:
        st.session_state["shown_notifications"] = set()
    
    notifications = get_user_notifications(username)
    unread_notifications = [n for n in notifications if not n.get("read", False)]
    
    # Get user settings
    user_data = load_data()
    settings = user_data.get("settings", {})
    notifications_enabled = settings.get("notifications", True)
    sound_enabled = settings.get("notification_sound", True)
    popup_enabled = settings.get("notification_popup", True)
    
    if not notifications_enabled:
        return
    
    # Show popups for new unread notifications
    for notification in unread_notifications:
        notification_id = notification.get("id")
        if notification_id not in st.session_state["shown_notifications"]:
            if popup_enabled:
                # Create a modified notification that respects sound settings
                notification_with_sound = notification.copy()
                if not sound_enabled:
                    # Set frequency to 0 to disable sound
                    notification_with_sound["_disable_sound"] = True
                show_notification_popup(notification_with_sound)
            st.session_state["shown_notifications"].add(notification_id)

def enhanced_send_notification(to_username: str, title: str, message: str, notification_type: str = "info", from_username: Optional[str] = None, priority: str = "normal"):
    """Enhanced notification function with priority and better categorization."""
    notifications_data = load_notifications_data()
    
    if to_username not in notifications_data:
        notifications_data[to_username] = []
    
    notification = {
        "id": str(uuid.uuid4()),
        "title": title,
        "message": message,
        "type": notification_type,
        "from_username": from_username,
        "created_at": get_current_timestamp(),
        "read": False,
        "priority": priority,
        "timestamp": time.time()
    }
    
    notifications_data[to_username].append(notification)
    save_notifications_data(notifications_data)
    
    # Show popup immediately if user is currently logged in
    if "username" in st.session_state and st.session_state["username"] == to_username:
        user_data = load_data()
        settings = user_data.get("settings", {})
        if settings.get("notifications", True) and settings.get("notification_popup", True):
            # Create a modified notification that respects sound settings
            notification_with_sound = notification.copy()
            if not settings.get("notification_sound", True):
                notification_with_sound["_disable_sound"] = True
            show_notification_popup(notification_with_sound)

# -------------------------------------------------------------
# Enhanced Notification Functions for Different Types
# -------------------------------------------------------------

def send_task_notification(to_username: str, task_title: str, action: str, from_username: Optional[str] = None, priority: str = "normal"):
    """Send task-related notification."""
    title = f"Task {action.title()}"
    message = f"Task '{task_title}' has been {action}"
    if from_username:
        message += f" by {get_user_info(from_username).get('full_name', from_username)}"
    
    enhanced_send_notification(to_username, title, message, "task", from_username, priority)

def send_file_notification(to_username: str, file_name: str, action: str, from_username: Optional[str] = None, priority: str = "normal"):
    """Send file-related notification."""
    title = f"File {action.title()}"
    message = f"File '{file_name}' has been {action}"
    if from_username:
        message += f" by {get_user_info(from_username).get('full_name', from_username)}"
    
    enhanced_send_notification(to_username, title, message, "file", from_username, priority)

def send_poll_notification(to_username: str, poll_question: str, action: str, from_username: Optional[str] = None, priority: str = "normal"):
    """Send poll-related notification."""
    title = f"Poll {action.title()}"
    message = f"Poll '{poll_question[:50]}{'...' if len(poll_question) > 50 else ''}' has been {action}"
    if from_username:
        message += f" by {get_user_info(from_username).get('full_name', from_username)}"
    
    enhanced_send_notification(to_username, title, message, "poll", from_username, priority)

def send_calendar_notification(to_username: str, event_title: str, action: str, from_username: Optional[str] = None, priority: str = "normal"):
    """Send calendar-related notification."""
    title = f"Calendar Event {action.title()}"
    message = f"Event '{event_title}' has been {action}"
    if from_username:
        message += f" by {get_user_info(from_username).get('full_name', from_username)}"
    
    enhanced_send_notification(to_username, title, message, "calendar", from_username, priority)

def send_chat_notification(to_username: str, sender_name: str, message_preview: str, priority: str = "normal"):
    """Send chat-related notification."""
    title = f"New Message from {sender_name}"
    message = f"{message_preview[:100]}{'...' if len(message_preview) > 100 else ''}"
    
    enhanced_send_notification(to_username, title, message, "chat", None, priority)

def send_project_notification(to_username: str, project_name: str, action: str, from_username: Optional[str] = None, priority: str = "normal"):
    """Send project-related notification."""
    title = f"Project {action.title()}"
    message = f"Project '{project_name}' has been {action}"
    if from_username:
        message += f" by {get_user_info(from_username).get('full_name', from_username)}"
    
    enhanced_send_notification(to_username, title, message, "project", from_username, priority)

def send_performance_notification(to_username: str, action: str, from_username: Optional[str] = None, priority: str = "normal"):
    """Send performance-related notification."""
    title = f"Performance Review {action.title()}"
    message = f"Your performance review has been {action}"
    if from_username:
        message += f" by {get_user_info(from_username).get('full_name', from_username)}"
    
    enhanced_send_notification(to_username, title, message, "performance", from_username, priority)

def send_notification(to_username: str, title: str, message: str, notification_type: str = "info", from_username: Optional[str] = None):
    """Send a notification to a user."""
    # Use enhanced notification function
    enhanced_send_notification(to_username, title, message, notification_type, from_username, "normal")

def get_user_notifications(username: str) -> list:
    """Get notifications for a user."""
    notifications_data = load_notifications_data()
    return notifications_data.get(username, [])

def mark_notification_read(username: str, notification_id: str):
    """Mark a notification as read."""
    notifications_data = load_notifications_data()
    user_notifications = notifications_data.get(username, [])
    
    for notification in user_notifications:
        if notification.get("id") == notification_id:
            notification["read"] = True
            break
    
    save_notifications_data(notifications_data)

# Role hierarchy for company positions
ROLE_HIERARCHY = {
    "admin": 11,  # Admin has highest level
    "ceo": 10,
    "cfo": 9,
    "cto": 9,
    "vp": 8,
    "director": 7,
    "senior_manager": 6,
    "manager": 5,
    "team_lead": 4,
    "senior_employee": 3,
    "employee": 2,
    "intern": 1
}

def get_role_level(role: str) -> int:
    """Get the hierarchy level of a role."""
    return ROLE_HIERARCHY.get(role.lower(), 0)

def can_manage_role(manager_role: str, target_role: str) -> bool:
    """Check if a manager can change the role of a target user."""
    manager_level = get_role_level(manager_role)
    target_level = get_role_level(target_role)
    # Admin can manage any role
    if manager_role.lower() == "admin":
        return True
    # Any higher role can manage any lower role
    return manager_level > target_level

def send_chat_message(company_code: str, from_username: str, message: str, message_type: str = "text"):
    """Send a chat message to company chat."""
    # Validate message content
    message_valid, message_error = validate_content(message)
    if not message_valid:
        return False, message_error
    
    chat_data = load_chat_data()
    
    if company_code not in chat_data:
        chat_data[company_code] = []
    
    user_info = get_user_info(from_username)
    
    chat_message = {
        "id": str(uuid.uuid4()),
        "from_username": from_username,
        "from_name": user_info.get("full_name", from_username),
        "from_role": user_info.get("role", "employee"),
        "message": message,
        "message_type": message_type,
        "timestamp": get_current_timestamp(),
        "edited": False,
        "deleted": False
    }
    
    chat_data[company_code].append(chat_message)
    save_chat_data(chat_data)
    return True, "Message sent successfully"
    
    # Send enhanced chat notifications to all company members
    employees = get_company_employees(company_code)
    for employee in employees:
        if employee.get("username") != from_username:
            send_chat_notification(
                employee.get("username"),
                user_info.get('full_name', from_username),
                message,
                "normal"
            )

def get_company_chat_messages(company_code: str, limit: int = 50) -> List[Dict[str, Any]]:
    """Get recent chat messages for a company."""
    chat_data = load_chat_data()
    messages = chat_data.get(company_code, [])
    
    # Filter out deleted messages and return recent ones
    active_messages = [msg for msg in messages if not msg.get("deleted", False)]
    return active_messages[-limit:]

def edit_chat_message(company_code: str, message_id: str, new_message: str, editor_username: str) -> bool:
    """Edit a chat message (only by original author)."""
    chat_data = load_chat_data()
    messages = chat_data.get(company_code, [])
    
    for message in messages:
        if message.get("id") == message_id:
            # Only original author can edit their own message
            if message.get("from_username") == editor_username:
                message["message"] = new_message
                message["edited"] = True
                message["edited_by"] = editor_username
                message["edited_at"] = get_current_timestamp()
                save_chat_data(chat_data)
                return True
            return False
    
    return False

def delete_chat_message(company_code: str, message_id: str, deleter_username: str) -> bool:
    """Delete a chat message (only by original author)."""
    chat_data = load_chat_data()
    messages = chat_data.get(company_code, [])
    
    for message in messages:
        if message.get("id") == message_id:
            # Only original author can delete their own message
            if message.get("from_username") == deleter_username:
                message["deleted"] = True
                message["deleted_by"] = deleter_username
                message["deleted_at"] = get_current_timestamp()
                save_chat_data(chat_data)
                return True
            return False
    
    return False

def change_user_role(company_code: str, target_username: str, new_role: str, changer_username: str) -> Tuple[bool, str]:
    """Change a user's role in the company."""
    # Check if changer has permission
    changer_info = get_user_info(changer_username)
    target_info = get_user_info(target_username)
    
    if not changer_info or not target_info:
        return False, "User not found!"
    
    changer_role = changer_info.get("role", "employee")
    target_role = target_info.get("role", "employee")
    
    # Check if changer can manage the target's role
    if not can_manage_role(changer_role, target_role):
        return False, "You don't have permission to change this user's role!"
    
    # Update user role
    auth_data = load_auth_data()
    if target_username in auth_data:
        auth_data[target_username]["role"] = new_role
        save_auth_data(auth_data)
        
        # Update in company data
        companies_data = load_companies_data()
        if company_code in companies_data:
            for employee in companies_data[company_code].get("employees", []):
                if employee.get("username") == target_username:
                    employee["role"] = new_role
                    break
            save_companies_data(companies_data)
        
        # Send enhanced role change notification
        enhanced_send_notification(
            target_username,
            "Role Changed",
            f"Your role has been changed to {new_role.title()} by {changer_info.get('full_name', changer_username)}",
            "info",
            changer_username,
            "high"
        )
        
        return True, f"Role changed successfully to {new_role.title()}!"
    
    return False, "Failed to update user role!"

def add_custom_role(company_code: str, role_name: str, role_level: int, creator_username: str) -> Tuple[bool, str]:
    """Add a custom role to the company."""
    # Only admins can add custom roles
    creator_info = get_user_info(creator_username)
    if not creator_info or creator_info.get("role") not in ["admin", "ceo", "cfo", "cto"]:
        return False, "Only admins can add custom roles!"
    
    companies_data = load_companies_data()
    if company_code in companies_data:
        if "custom_roles" not in companies_data[company_code]:
            companies_data[company_code]["custom_roles"] = {}
        
        companies_data[company_code]["custom_roles"][role_name.lower()] = {
            "name": role_name,
            "level": role_level,
            "created_by": creator_username,
            "created_at": get_current_timestamp()
        }
        
        save_companies_data(companies_data)
        return True, f"Custom role '{role_name}' added successfully!"
    
    return False, "Company not found!"

# -------------------------------------------------------------
# Private Chat Functions
# -------------------------------------------------------------
def get_chat_pair_key(user1: str, user2: str) -> str:
    """Get a consistent key for a chat pair (sorted alphabetically)."""
    return "|".join(sorted([user1, user2]))

def send_private_message(from_username: str, to_username: str, message: str, message_type: str = "text") -> bool:
    """Send a private message between two users."""
    # Validate message content
    message_valid, message_error = validate_content(message)
    if not message_valid:
        return False
    
    # Check if both users are in the same company
    from_user_info = get_user_info(from_username)
    to_user_info = get_user_info(to_username)
    
    if not from_user_info or not to_user_info:
        return False
    
    from_company = from_user_info.get("company_code")
    to_company = to_user_info.get("company_code")
    
    if from_company != to_company:
        return False  # Users must be in the same company
    
    private_chat_data = load_private_chat_data()
    pair_key = get_chat_pair_key(from_username, to_username)
    
    if pair_key not in private_chat_data:
        private_chat_data[pair_key] = []
    
    chat_message = {
        "id": str(uuid.uuid4()),
        "from_username": from_username,
        "from_name": from_user_info.get("full_name", from_username),
        "to_username": to_username,
        "message": message,
        "message_type": message_type,
        "timestamp": get_current_timestamp(),
        "read": False,
        "edited": False,
        "deleted": False
    }
    
    private_chat_data[pair_key].append(chat_message)
    save_private_chat_data(private_chat_data)
    
    # Send enhanced private message notification
    send_chat_notification(
        to_username,
        from_user_info.get('full_name', from_username),
        message,
        "normal"
    )
    
    return True

def get_private_messages(user1: str, user2: str, limit: int = 50) -> List[Dict[str, Any]]:
    """Get private messages between two users."""
    private_chat_data = load_private_chat_data()
    pair_key = get_chat_pair_key(user1, user2)
    messages = private_chat_data.get(pair_key, [])
    
    # Filter out deleted messages and return recent ones
    active_messages = [msg for msg in messages if not msg.get("deleted", False)]
    return active_messages[-limit:]

def mark_private_message_read(user1: str, user2: str, message_id: str):
    """Mark a private message as read."""
    private_chat_data = load_private_chat_data()
    pair_key = get_chat_pair_key(user1, user2)
    
    if pair_key in private_chat_data:
        for message in private_chat_data[pair_key]:
            if message.get("id") == message_id and message.get("to_username") == user1:
                message["read"] = True
                break
        save_private_chat_data(private_chat_data)

def get_user_private_chats(username: str) -> List[Dict[str, Any]]:
    """Get all private chat conversations for a user."""
    private_chat_data = load_private_chat_data()
    user_chats = []
    
    for pair_key, messages in private_chat_data.items():
        if username in pair_key.split("|"):
            # Get the other user in the conversation
            users = pair_key.split("|")
            other_user = users[1] if users[0] == username else users[0]
            
            # Get the last message
            if messages:
                last_message = messages[-1]
                if not last_message.get("deleted", False):
                    user_chats.append({
                        "other_user": other_user,
                        "other_user_name": get_user_info(other_user).get("full_name", other_user),
                        "last_message": last_message.get("message", ""),
                        "last_timestamp": last_message.get("timestamp", ""),
                        "unread_count": len([m for m in messages if not m.get("read", False) and m.get("to_username") == username])
                    })
    
    # Sort by last message timestamp
    user_chats.sort(key=lambda x: x.get("last_timestamp", ""), reverse=True)
    return user_chats

# -------------------------------------------------------------
# File Sharing Functions
# -------------------------------------------------------------
def upload_file(company_code: str, uploaded_by: str, file_name: str, file_content: bytes, file_type: str = "unknown") -> bool:
    """Upload a file to company storage."""
    files_data = load_files_data()
    
    if company_code not in files_data:
        files_data[company_code] = []
    
    file_info = {
        "id": str(uuid.uuid4()),
        "name": file_name,
        "type": file_type,
        "size": len(file_content),
        "uploaded_by": uploaded_by,
        "uploaded_at": get_current_timestamp(),
        "downloads": 0,
        "content": file_content.hex()  # Store as hex string
    }
    
    files_data[company_code].append(file_info)
    save_files_data(files_data)
    
    # Send enhanced file notifications to company members
    employees = get_company_employees(company_code)
    for employee in employees:
        if employee.get("username") != uploaded_by:
            send_file_notification(
                employee.get("username"),
                file_name,
                "shared",
                uploaded_by,
                "normal"
            )
    
    return True

def get_company_files(company_code: str) -> List[Dict[str, Any]]:
    """Get all files for a company."""
    files_data = load_files_data()
    return files_data.get(company_code, [])

def download_file(company_code: str, file_id: str) -> Optional[bytes]:
    """Download a file."""
    files_data = load_files_data()
    company_files = files_data.get(company_code, [])
    
    for file_info in company_files:
        if file_info.get("id") == file_id:
            # Increment download count
            file_info["downloads"] = file_info.get("downloads", 0) + 1
            save_files_data(files_data)
            
            # Return file content
            return bytes.fromhex(file_info.get("content", ""))
    
    return None

# -------------------------------------------------------------
# Private File Functions
# -------------------------------------------------------------
def upload_private_file(from_username: str, to_username: str, file_name: str, file_content: bytes, file_type: str = "unknown") -> bool:
    """Upload a private file between two users."""
    # Check if both users are in the same company
    from_user_info = get_user_info(from_username)
    to_user_info = get_user_info(to_username)
    
    if not from_user_info or not to_user_info:
        return False
    
    from_company = from_user_info.get("company_code")
    to_company = to_user_info.get("company_code")
    
    if from_company != to_company:
        return False  # Users must be in the same company
    
    private_files_data = load_private_files_data()
    pair_key = get_chat_pair_key(from_username, to_username)
    
    if pair_key not in private_files_data:
        private_files_data[pair_key] = []
    
    file_info = {
        "id": str(uuid.uuid4()),
        "name": file_name,
        "type": file_type,
        "size": len(file_content),
        "uploaded_by": from_username,
        "uploaded_to": to_username,
        "uploaded_at": get_current_timestamp(),
        "downloads": 0
    }
    
    private_files_data[pair_key].append(file_info)
    save_private_files_data(private_files_data)
    
    # Send enhanced private file notification
    send_file_notification(to_username, file_name, "shared privately", from_username, "normal")
    
    return True

def get_private_files(user1: str, user2: str) -> List[Dict[str, Any]]:
    """Get private files shared between two users."""
    private_files_data = load_private_files_data()
    pair_key = get_chat_pair_key(user1, user2)
    return private_files_data.get(pair_key, [])

def download_private_file(user1: str, user2: str, file_id: str) -> Optional[bytes]:
    """Download a private file."""
    private_files_data = load_private_files_data()
    pair_key = get_chat_pair_key(user1, user2)
    files = private_files_data.get(pair_key, [])
    
    for file_info in files:
        if file_info.get("id") == file_id:
            # Update download count
            file_info["downloads"] = file_info.get("downloads", 0) + 1
            save_private_files_data(private_files_data)
            
            # In a real app, you'd store files in a proper file system
            # For now, we'll return a placeholder
            return b"Private file content placeholder"
    
    return None

def delete_private_file(user1: str, user2: str, file_id: str, deleter_username: str) -> bool:
    """Delete a private file (only by uploader)."""
    private_files_data = load_private_files_data()
    pair_key = get_chat_pair_key(user1, user2)
    files = private_files_data.get(pair_key, [])
    
    for i, file_info in enumerate(files):
        if file_info.get("id") == file_id:
            # Only uploader can delete the file
            if file_info.get("uploaded_by") == deleter_username:
                files.pop(i)
                save_private_files_data(private_files_data)
                return True
            return False
    
    return False

def get_user_private_files(username: str) -> List[Dict[str, Any]]:
    """Get all private files for a user (both sent and received)."""
    private_files_data = load_private_files_data()
    user_files = []
    
    for pair_key, files in private_files_data.items():
        user1, user2 = pair_key.split("|")
        if username in [user1, user2]:
            for file_info in files:
                # Add pair info to file info
                file_info_copy = file_info.copy()
                file_info_copy["pair_key"] = pair_key
                file_info_copy["other_user"] = user2 if username == user1 else user1
                user_files.append(file_info_copy)
    
    return user_files

# -------------------------------------------------------------
# Calendar Functions
# -------------------------------------------------------------
def create_calendar_event(company_code: str, created_by: str, title: str, description: str, 
                         start_date: str, end_date: str, event_type: str = "meeting", 
                         attendees: Optional[List[str]] = None) -> bool:
    """Create a calendar event."""
    calendar_data = load_calendar_data()
    
    if company_code not in calendar_data:
        calendar_data[company_code] = []
    
    event = {
        "id": str(uuid.uuid4()),
        "title": title,
        "description": description,
        "start_date": start_date,
        "end_date": end_date,
        "event_type": event_type,
        "created_by": created_by,
        "attendees": attendees or [],
        "created_at": get_current_timestamp(),
        "status": "active"
    }
    
    calendar_data[company_code].append(event)
    save_calendar_data(calendar_data)
    
    # Send enhanced calendar notifications to attendees
    if attendees:
        for attendee in attendees:
            if attendee != created_by:
                send_calendar_notification(
                    attendee,
                    title,
                    "created",
                    created_by,
                    "normal"
                )
    
    return True

def get_company_events(company_code: str, start_date: Optional[str] = None, end_date: Optional[str] = None) -> List[Dict[str, Any]]:
    """Get all events for a company with optional date filtering."""
    calendar_data = load_calendar_data()
    events = calendar_data.get(company_code, [])
    
    if start_date and end_date:
        # Filter events by date range with proper validation
        filtered_events = []
        for event in events:
            event_start = event.get("start_date", "")
            event_end = event.get("end_date", "")
            
            # Only include events where both dates are valid strings
            if isinstance(event_start, str) and isinstance(event_end, str) and event_start and event_end:
                if event_start >= start_date and event_end <= end_date:
                    filtered_events.append(event)
        events = filtered_events
    
    return sorted(events, key=lambda x: x.get("start_date", ""))

def get_user_events(username: str, company_code: str) -> List[Dict[str, Any]]:
    """Get events where user is an attendee or creator."""
    events = get_company_events(company_code)
    user_events = []
    
    for event in events:
        if (event.get("created_by") == username or 
            username in event.get("attendees", [])):
            user_events.append(event)
    
    return user_events

# -------------------------------------------------------------
# Polls Functions
# -------------------------------------------------------------
def create_poll(company_code: str, created_by: str, question: str, options: List[str], 
                allow_multiple: bool = False, duration_hours: int = 24) -> bool:
    """Create a poll."""
    polls_data = load_polls_data()
    
    if company_code not in polls_data:
        polls_data[company_code] = []
    
    poll = {
        "id": str(uuid.uuid4()),
        "question": question,
        "options": options,
        "allow_multiple": allow_multiple,
        "created_by": created_by,
        "created_at": get_current_timestamp(),
        "expires_at": (datetime.datetime.now() + datetime.timedelta(hours=duration_hours)).strftime("%Y-%m-%d %H:%M:%S"),
        "votes": {},
        "status": "active"
    }
    
    polls_data[company_code].append(poll)
    save_polls_data(polls_data)
    
    # Send enhanced poll notifications to company members
    employees = get_company_employees(company_code)
    for employee in employees:
        if employee.get("username") != created_by:
            send_poll_notification(
                employee.get("username"),
                question,
                "created",
                created_by,
                "normal"
            )
    
    return True

def vote_poll(company_code: str, poll_id: str, username: str, selected_options: List[int]) -> bool:
    """Vote on a poll."""
    try:
        polls_data = load_polls_data()
        company_polls = polls_data.get(company_code, [])
        
        for poll in company_polls:
            if poll.get("id") == poll_id:
                if poll.get("status") != "active":
                    return False  # Poll is closed
                
                # Check if user already voted
                if username in poll.get("votes", {}):
                    return False  # Already voted
                
                # Convert selected_options to integers and validate
                try:
                    selected_options = [int(opt) for opt in selected_options]
                except (ValueError, TypeError):
                    return False  # Invalid option format
                
                # Validate options
                if not poll.get("allow_multiple", False) and len(selected_options) > 1:
                    return False  # Multiple votes not allowed
                
                if not selected_options or max(selected_options) >= len(poll.get("options", [])):
                    return False  # Invalid option
                
                # Record vote
                if "votes" not in poll:
                    poll["votes"] = {}
                poll["votes"][username] = selected_options
                save_polls_data(polls_data)
                return True
        
        return False  # Poll not found
    except Exception as e:
        print(f"Error in vote_poll: {e}")
        return False

def get_company_polls(company_code: str) -> List[Dict[str, Any]]:
    """Get all polls for a company."""
    polls_data = load_polls_data()
    polls = polls_data.get(company_code, [])
    
    # Update expired polls
    current_time = datetime.datetime.now()
    for poll in polls:
        if poll.get("status") == "active":
            expires_at = datetime.datetime.strptime(poll.get("expires_at", ""), "%Y-%m-%d %H:%M:%S")
            if current_time > expires_at:
                poll["status"] = "expired"
    
    save_polls_data(polls_data)
    return polls

# -------------------------------------------------------------
# User Status Functions
# -------------------------------------------------------------
def update_user_status(username: str, status: str = "online", custom_status: str = ""):
    """Update user's online status."""
    user_status_data = load_user_status_data()
    
    user_status_data[username] = {
        "status": status,  # online, away, busy, offline
        "custom_status": custom_status,
        "last_seen": get_current_timestamp(),
        "updated_at": get_current_timestamp()
    }
    
    save_user_status_data(user_status_data)

def get_user_status(username: str) -> Dict[str, Any]:
    """Get user's current status."""
    user_status_data = load_user_status_data()
    return user_status_data.get(username, {
        "status": "offline",
        "custom_status": "",
        "last_seen": "",
        "updated_at": ""
    })

def get_online_users(company_code: str) -> List[Dict[str, Any]]:
    """Get all online users in a company."""
    employees = get_company_employees(company_code)
    online_users = []
    
    for employee in employees:
        username = employee.get("username")
        status = get_user_status(username)
        if status.get("status") == "online":
            online_users.append({
                "username": username,
                "full_name": employee.get("full_name", username),
                "status": status.get("status"),
                "custom_status": status.get("custom_status"),
                "last_seen": status.get("last_seen")
            })
    
    return online_users

# -------------------------------------------------------------
# Task Comments Functions
# -------------------------------------------------------------
def add_task_comment(task_id: str, username: str, comment: str) -> bool:
    """Add a comment to a task."""
    task_comments_data = load_task_comments_data()
    
    if task_id not in task_comments_data:
        task_comments_data[task_id] = []
    
    comment_obj = {
        "id": str(uuid.uuid4()),
        "username": username,
        "user_name": get_user_info(username).get("full_name", username),
        "comment": comment,
        "timestamp": get_current_timestamp(),
        "edited": False,
        "deleted": False
    }
    
    task_comments_data[task_id].append(comment_obj)
    save_task_comments_data(task_comments_data)
    
    return True

def get_task_comments(task_id: str) -> List[Dict[str, Any]]:
    """Get all comments for a task."""
    task_comments_data = load_task_comments_data()
    comments = task_comments_data.get(task_id, [])
    
    # Filter out deleted comments
    active_comments = [c for c in comments if not c.get("deleted", False)]
    return sorted(active_comments, key=lambda x: x.get("timestamp", ""))

# -------------------------------------------------------------
# Pinned Messages Functions
# -------------------------------------------------------------
def pin_message(company_code: str, message_id: str, pinned_by: str, message_type: str = "company") -> bool:
    """Pin a message in company or private chat."""
    pinned_messages_data = load_pinned_messages_data()
    
    if company_code not in pinned_messages_data:
        pinned_messages_data[company_code] = []
    
    # Check if message is already pinned
    for pinned in pinned_messages_data[company_code]:
        if pinned.get("message_id") == message_id:
            return False  # Already pinned
    
    pinned_message = {
        "id": str(uuid.uuid4()),
        "message_id": message_id,
        "message_type": message_type,  # company, private
        "pinned_by": pinned_by,
        "pinned_at": get_current_timestamp()
    }
    
    pinned_messages_data[company_code].append(pinned_message)
    save_pinned_messages_data(pinned_messages_data)
    
    return True

def unpin_message(company_code: str, message_id: str, unpinned_by: str) -> bool:
    """Unpin a message."""
    pinned_messages_data = load_pinned_messages_data()
    
    if company_code in pinned_messages_data:
        pinned_messages_data[company_code] = [
            p for p in pinned_messages_data[company_code] 
            if p.get("message_id") != message_id
        ]
        save_pinned_messages_data(pinned_messages_data)
        return True
    
    return False

def get_pinned_messages(company_code: str) -> List[Dict[str, Any]]:
    """Get all pinned messages for a company."""
    pinned_messages_data = load_pinned_messages_data()
    return pinned_messages_data.get(company_code, [])

# -------------------------------------------------------------
# Task Attachments Functions
# -------------------------------------------------------------
def add_task_attachment(task_id: str, username: str, file_name: str, file_content: bytes, 
                       file_type: str = "unknown", attachment_type: str = "file") -> bool:
    """Add an attachment to a task."""
    task_attachments_data = load_task_attachments_data()
    
    if task_id not in task_attachments_data:
        task_attachments_data[task_id] = []
    
    attachment = {
        "id": str(uuid.uuid4()),
        "file_name": file_name,
        "file_type": file_type,
        "attachment_type": attachment_type,  # file, code, image, document
        "size": len(file_content),
        "uploaded_by": username,
        "uploaded_at": get_current_timestamp(),
        "content": file_content.hex()  # Store as hex string
    }
    
    task_attachments_data[task_id].append(attachment)
    save_task_attachments_data(task_attachments_data)
    
    return True

def get_task_attachments(task_id: str) -> List[Dict[str, Any]]:
    """Get all attachments for a task."""
    task_attachments_data = load_task_attachments_data()
    return task_attachments_data.get(task_id, [])

def download_task_attachment(task_id: str, attachment_id: str) -> Optional[bytes]:
    """Download a task attachment."""
    task_attachments_data = load_task_attachments_data()
    task_attachments = task_attachments_data.get(task_id, [])
    
    for attachment in task_attachments:
        if attachment.get("id") == attachment_id:
            return bytes.fromhex(attachment.get("content", ""))
    
    return None

def delete_task_attachment(task_id: str, attachment_id: str, username: str) -> bool:
    """Delete a task attachment (only by uploader)."""
    task_attachments_data = load_task_attachments_data()
    task_attachments = task_attachments_data.get(task_id, [])
    
    for attachment in task_attachments:
        if attachment.get("id") == attachment_id:
            if attachment.get("uploaded_by") == username:
                task_attachments_data[task_id] = [a for a in task_attachments if a.get("id") != attachment_id]
                save_task_attachments_data(task_attachments_data)
                return True
            return False
    
    return False

# -------------------------------------------------------------
# Project Management Functions
# -------------------------------------------------------------
def create_project(company_code: str, created_by: str, name: str, description: str, 
                  start_date: str, end_date: str, budget: float = 0.0, 
                  project_manager: str = "", team_members: Optional[List[str]] = None) -> Tuple[bool, str]:
    """Create a new project."""
    projects_data = load_projects_data()
    
    if company_code not in projects_data:
        projects_data[company_code] = []
    
    project = {
        "id": str(uuid.uuid4()),
        "name": name,
        "description": description,
        "start_date": start_date,
        "end_date": end_date,
        "budget": budget,
        "project_manager": project_manager,
        "team_members": team_members or [],
        "created_by": created_by,
        "created_at": get_current_timestamp(),
        "status": "planning",  # planning, active, on_hold, completed, cancelled
        "progress": 0,
        "tasks": [],
        "milestones": [],
        "risks": [],
        "documents": []
    }
    
    projects_data[company_code].append(project)
    save_projects_data(projects_data)
    
    # Send enhanced project notifications to team members
    if team_members:
        for member in team_members:
            if member != created_by:
                send_project_notification(
                    member,
                    name,
                    "assigned",
                    created_by,
                    "normal"
                )
    
    return True, f"Project '{name}' created successfully!"

def get_company_projects(company_code: str) -> List[Dict[str, Any]]:
    """Get all projects for a company."""
    projects_data = load_projects_data()
    return projects_data.get(company_code, [])

def update_project_progress(company_code: str, project_id: str, progress: int, 
                          updated_by: str) -> bool:
    """Update project progress."""
    projects_data = load_projects_data()
    company_projects = projects_data.get(company_code, [])
    
    for project in company_projects:
        if project.get("id") == project_id:
            project["progress"] = max(0, min(100, progress))
            project["updated_at"] = get_current_timestamp()
            project["updated_by"] = updated_by
            save_projects_data(projects_data)
            return True
    
    return False

def add_project_milestone(company_code: str, project_id: str, title: str, 
                         description: str, due_date: str, created_by: str) -> bool:
    """Add a milestone to a project."""
    projects_data = load_projects_data()
    company_projects = projects_data.get(company_code, [])
    
    for project in company_projects:
        if project.get("id") == project_id:
            milestone = {
                "id": str(uuid.uuid4()),
                "title": title,
                "description": description,
                "due_date": due_date,
                "created_by": created_by,
                "created_at": get_current_timestamp(),
                "status": "pending",  # pending, completed, overdue
                "completed_at": None
            }
            
            if "milestones" not in project:
                project["milestones"] = []
            project["milestones"].append(milestone)
            save_projects_data(projects_data)
            return True
    
    return False

# -------------------------------------------------------------
# Department Management Functions
# -------------------------------------------------------------
def create_department(company_code: str, name: str, description: str, 
                     manager_username: str, created_by: str) -> Tuple[bool, str]:
    """Create a new department."""
    departments_data = load_departments_data()
    
    if company_code not in departments_data:
        departments_data[company_code] = []
    
    department = {
        "id": str(uuid.uuid4()),
        "name": name,
        "description": description,
        "manager_username": manager_username,
        "created_by": created_by,
        "created_at": get_current_timestamp(),
        "employees": [],
        "budget": 0.0,
        "goals": [],
        "performance_metrics": {}
    }
    
    departments_data[company_code].append(department)
    save_departments_data(departments_data)
    
    return True, f"Department '{name}' created successfully!"

def get_company_departments(company_code: str) -> List[Dict[str, Any]]:
    """Get all departments for a company."""
    departments_data = load_departments_data()
    return departments_data.get(company_code, [])

def assign_employee_to_department(company_code: str, department_id: str, 
                                employee_username: str) -> bool:
    """Assign an employee to a department."""
    departments_data = load_departments_data()
    company_departments = departments_data.get(company_code, [])
    
    for department in company_departments:
        if department.get("id") == department_id:
            if employee_username not in department.get("employees", []):
                if "employees" not in department:
                    department["employees"] = []
                department["employees"].append(employee_username)
                save_departments_data(departments_data)
                return True
    
    return False

# -------------------------------------------------------------
# Performance Management Functions
# -------------------------------------------------------------
def create_performance_review(company_code: str, employee_username: str, 
                            reviewer_username: str, review_period: str,
                            goals_achieved: List[str], areas_improvement: List[str],
                            overall_rating: int, comments: str) -> Tuple[bool, str]:
    """Create a performance review."""
    performance_data = load_performance_data()
    
    if company_code not in performance_data:
        performance_data[company_code] = []
    
    review = {
        "id": str(uuid.uuid4()),
        "employee_username": employee_username,
        "reviewer_username": reviewer_username,
        "review_period": review_period,
        "goals_achieved": goals_achieved,
        "areas_improvement": areas_improvement,
        "overall_rating": max(1, min(5, overall_rating)),  # 1-5 scale
        "comments": comments,
        "created_at": get_current_timestamp(),
        "status": "submitted"  # submitted, approved, rejected
    }
    
    performance_data[company_code].append(review)
    save_performance_data(performance_data)
    
    # Send enhanced performance notification
    send_performance_notification(
        employee_username,
        "submitted",
        reviewer_username,
        "high"
    )
    
    return True, "Performance review created successfully!"

def get_employee_performance_reviews(company_code: str, employee_username: str) -> List[Dict[str, Any]]:
    """Get performance reviews for an employee."""
    performance_data = load_performance_data()
    company_reviews = performance_data.get(company_code, [])
    
    return [review for review in company_reviews if review.get("employee_username") == employee_username]

# -------------------------------------------------------------
# Budget Management Functions
# -------------------------------------------------------------
def create_budget_item(company_code: str, category: str, description: str,
                      amount: float, budget_type: str, created_by: str,
                      department: str = "", project: str = "") -> Tuple[bool, str]:
    """Create a budget item."""
    budget_data = load_budget_data()
    
    if company_code not in budget_data:
        budget_data[company_code] = []
    
    budget_item = {
        "id": str(uuid.uuid4()),
        "category": category,  # income, expense, investment
        "description": description,
        "amount": amount,
        "budget_type": budget_type,  # planned, actual
        "department": department,
        "project": project,
        "created_by": created_by,
        "created_at": get_current_timestamp(),
        "date": get_current_timestamp().split()[0]
    }
    
    budget_data[company_code].append(budget_item)
    save_budget_data(budget_data)
    
    return True, "Budget item created successfully!"

def get_company_budget(company_code: str, start_date: Optional[str] = None, end_date: Optional[str] = None) -> List[Dict[str, Any]]:
    """Get budget items for a company."""
    budget_data = load_budget_data()
    budget_items = budget_data.get(company_code, [])
    
    if start_date and end_date:
        budget_items = [item for item in budget_items 
                       if start_date <= item.get("date", "") <= end_date]
    
    return budget_items

def calculate_budget_summary(company_code: str) -> Dict[str, Any]:
    """Calculate budget summary."""
    budget_items = get_company_budget(company_code)
    
    total_income = sum(item.get("amount", 0) for item in budget_items 
                      if item.get("category") == "income")
    total_expenses = sum(item.get("amount", 0) for item in budget_items 
                        if item.get("category") == "expense")
    total_investments = sum(item.get("amount", 0) for item in budget_items 
                           if item.get("category") == "investment")
    
    return {
        "total_income": total_income,
        "total_expenses": total_expenses,
        "total_investments": total_investments,
        "net_balance": total_income - total_expenses - total_investments,
        "total_items": len(budget_items)
    }

# -------------------------------------------------------------
# Advanced Reporting Functions
# -------------------------------------------------------------
def generate_comprehensive_report(company_code: str, report_type: str, 
                                start_date: Optional[str] = None, end_date: Optional[str] = None) -> Dict[str, Any]:
    """Generate comprehensive reports."""
    reports_data = load_reports_data()
    
    if company_code not in reports_data:
        reports_data[company_code] = []
    
    report = {
        "id": str(uuid.uuid4()),
        "type": report_type,
        "start_date": start_date,
        "end_date": end_date,
        "generated_at": get_current_timestamp(),
        "data": {}
    }
    
    if report_type == "team_performance":
        # Team performance report
        employees = get_company_employees(company_code)
        performance_data = []
        
        for employee in employees:
            username = employee.get("username")
            user_file = Path(f"user_{username}.json")
            
            if user_file.exists():
                with user_file.open("r", encoding="utf-8") as f:
                    user_data = json.load(f)
                    assigned_tasks = user_data.get("assigned_tasks", [])
                    
                    total_tasks = len(assigned_tasks)
                    completed_tasks = len([t for t in assigned_tasks if t.get("completed", False)])
                    completion_rate = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
                    
                    performance_data.append({
                        "employee": employee.get("full_name", username),
                        "username": username,
                        "role": employee.get("role", "employee"),
                        "total_tasks": total_tasks,
                        "completed_tasks": completed_tasks,
                        "completion_rate": completion_rate
                    })
        
        report["data"] = {
            "performance_data": performance_data,
            "summary": {
                "total_employees": len(employees),
                "average_completion_rate": sum(p["completion_rate"] for p in performance_data) / len(performance_data) if performance_data else 0
            }
        }
    
    elif report_type == "project_status":
        # Project status report
        projects = get_company_projects(company_code)
        report["data"] = {
            "projects": projects,
            "summary": {
                "total_projects": len(projects),
                "active_projects": len([p for p in projects if p.get("status") == "active"]),
                "completed_projects": len([p for p in projects if p.get("status") == "completed"]),
                "average_progress": sum(p.get("progress", 0) for p in projects) / len(projects) if projects else 0
            }
        }
    
    elif report_type == "financial_summary":
        # Financial summary report
        budget_summary = calculate_budget_summary(company_code)
        report["data"] = budget_summary
    
    reports_data[company_code].append(report)
    save_reports_data(reports_data)
    
    return report

# -------------------------------------------------------------
# Workflow Management Functions
# -------------------------------------------------------------
def create_workflow(company_code: str, name: str, description: str, 
                   steps: List[Dict[str, Any]], created_by: str) -> Tuple[bool, str]:
    """Create a workflow."""
    workflows_data = load_workflows_data()
    
    if company_code not in workflows_data:
        workflows_data[company_code] = []
    
    workflow = {
        "id": str(uuid.uuid4()),
        "name": name,
        "description": description,
        "steps": steps,
        "created_by": created_by,
        "created_at": get_current_timestamp(),
        "status": "active",  # active, inactive
        "instances": []
    }
    
    workflows_data[company_code].append(workflow)
    save_workflows_data(workflows_data)
    
    return True, f"Workflow '{name}' created successfully!"

def get_company_workflows(company_code: str) -> List[Dict[str, Any]]:
    """Get all workflows for a company."""
    workflows_data = load_workflows_data()
    return workflows_data.get(company_code, [])

def start_workflow_instance(company_code: str, workflow_id: str, 
                           initiator_username: str, data: Dict[str, Any]) -> Tuple[bool, str]:
    """Start a workflow instance."""
    workflows_data = load_workflows_data()
    company_workflows = workflows_data.get(company_code, [])
    
    for workflow in company_workflows:
        if workflow.get("id") == workflow_id:
            instance = {
                "id": str(uuid.uuid4()),
                "workflow_id": workflow_id,
                "initiator": initiator_username,
                "started_at": get_current_timestamp(),
                "status": "running",  # running, completed, cancelled
                "current_step": 0,
                "data": data,
                "history": []
            }
            
            if "instances" not in workflow:
                workflow["instances"] = []
            workflow["instances"].append(instance)
            save_workflows_data(workflows_data)
            return True, f"Workflow instance started successfully!"
    
    return False, "Workflow not found!"

# -------------------------------------------------------------
# Knowledge Base Functions
# -------------------------------------------------------------
def create_knowledge_article(company_code: str, title: str, content: str,
                           category: str, author_username: str, 
                           tags: Optional[List[str]] = None) -> Tuple[bool, str]:
    """Create a knowledge base article."""
    knowledge_base_data = load_knowledge_base_data()
    
    if company_code not in knowledge_base_data:
        knowledge_base_data[company_code] = []
    
    article = {
        "id": str(uuid.uuid4()),
        "title": title,
        "content": content,
        "category": category,
        "author": author_username,
        "tags": tags or [],
        "created_at": get_current_timestamp(),
        "updated_at": get_current_timestamp(),
        "views": 0,
        "rating": 0,
        "status": "published"  # draft, published, archived
    }
    
    knowledge_base_data[company_code].append(article)
    save_knowledge_base_data(knowledge_base_data)
    
    return True, f"Knowledge article '{title}' created successfully!"

def get_knowledge_articles(company_code: str, category: Optional[str] = None) -> List[Dict[str, Any]]:
    """Get knowledge base articles."""
    knowledge_base_data = load_knowledge_base_data()
    articles = knowledge_base_data.get(company_code, [])
    
    if category:
        articles = [article for article in articles if article.get("category") == category]
    
    return articles

def search_knowledge_base(company_code: str, query: str) -> List[Dict[str, Any]]:
    """Search knowledge base articles."""
    articles = get_knowledge_articles(company_code)
    results = []
    
    for article in articles:
        if (query.lower() in article.get("title", "").lower() or
            query.lower() in article.get("content", "").lower() or
            any(query.lower() in tag.lower() for tag in article.get("tags", []))):
            results.append(article)
    
    return results

# -------------------------------------------------------------
# Integration Management Functions
# -------------------------------------------------------------
def create_integration(company_code: str, name: str, integration_type: str,
                      config: Dict[str, Any], created_by: str) -> Tuple[bool, str]:
    """Create an integration."""
    integrations_data = load_integrations_data()
    
    if company_code not in integrations_data:
        integrations_data[company_code] = []
    
    integration = {
        "id": str(uuid.uuid4()),
        "name": name,
        "type": integration_type,  # slack, email, calendar, crm, etc.
        "config": config,
        "created_by": created_by,
        "created_at": get_current_timestamp(),
        "status": "active",  # active, inactive, error
        "last_sync": None
    }
    
    integrations_data[company_code].append(integration)
    save_integrations_data(integrations_data)
    
    return True, f"Integration '{name}' created successfully!"

def get_company_integrations(company_code: str) -> List[Dict[str, Any]]:
    """Get all integrations for a company."""
    integrations_data = load_integrations_data()
    return integrations_data.get(company_code, [])

# -------------------------------------------------------------
# Search Functions
# -------------------------------------------------------------
def search_messages(company_code: str, query: str, search_type: str = "all") -> List[Dict[str, Any]]:
    """Search through chat messages."""
    results = []
    
    if search_type in ["all", "company"]:
        # Search company chat
        chat_data = load_chat_data()
        messages = chat_data.get(company_code, [])
        
        for message in messages:
            if (query.lower() in message.get("message", "").lower() or
                query.lower() in message.get("from_name", "").lower()):
                results.append({
                    "type": "company_chat",
                    "message": message,
                    "context": "Company Chat"
                })
    
    if search_type in ["all", "private"]:
        # Search private chats
        private_chat_data = load_private_chat_data()
        
        for pair_key, messages in private_chat_data.items():
            if company_code in pair_key:  # Only search within company
                for message in messages:
                    if query.lower() in message.get("message", "").lower():
                        results.append({
                            "type": "private_chat",
                            "message": message,
                            "context": f"Private Chat with {message.get('from_name', 'Unknown')}"
                        })
    
    return results

def search_tasks(username: str, query: str) -> List[Dict[str, Any]]:
    """Search through user's tasks."""
    results = []
    
    # Search personal tasks
    user_file = Path(f"user_{username}.json")
    if user_file.exists():
        with user_file.open("r", encoding="utf-8") as f:
            user_data = json.load(f)
            
            tasks = user_data.get("tasks", [])
            for task in tasks:
                if (query.lower() in task.get("title", "").lower() or
                    query.lower() in task.get("description", "").lower()):
                    results.append({
                        "type": "personal_task",
                        "task": task,
                        "context": "Personal Tasks"
                    })
            
            # Search assigned tasks
            assigned_tasks = user_data.get("assigned_tasks", [])
            for task in assigned_tasks:
                if (query.lower() in task.get("title", "").lower() or
                    query.lower() in task.get("description", "").lower()):
                    results.append({
                        "type": "assigned_task",
                        "task": task,
                        "context": "Assigned Tasks"
                    })
    
    return results

# -------------------------------------------------------------
# Dark Mode and Theme Functions
# -------------------------------------------------------------
def get_user_theme(username: str) -> str:
    """Get user's preferred theme."""
    user_file = Path(f"user_{username}.json")
    if user_file.exists():
        with user_file.open("r", encoding="utf-8") as f:
            user_data = json.load(f)
            return user_data.get("settings", {}).get("theme", "light")
    return "light"

def update_user_theme(username: str, theme: str):
    """Update user's theme preference."""
    user_file = Path(f"user_{username}.json")
    if user_file.exists():
        with user_file.open("r", encoding="utf-8") as f:
            user_data = json.load(f)
        
        if "settings" not in user_data:
            user_data["settings"] = {}
        user_data["settings"]["theme"] = theme
        
        with user_file.open("w", encoding="utf-8") as f:
            json.dump(user_data, f, indent=2, ensure_ascii=False)

def show_login_page():
    """Display enhanced login/register page."""
    st.markdown("""
    <div class="login-container">
        <h1>🏢 Nafup</h1>
        <p>Professional Productivity Suite for Individuals & Teams</p>
        <div style="margin: 2rem 0;">
            <span class="role-badge admin-badge">Admin</span>
            <span class="role-badge manager-badge">Manager</span>
            <span class="role-badge employee-badge">Employee</span>
            <span class="role-badge personal-badge">Personal</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Login/Register tabs
    tab1, tab2, tab3 = st.tabs(["🔐 Login", "📝 Register", "🏢 Create Company"])
    
    with tab1:
        st.markdown('<div class="login-form">', unsafe_allow_html=True)
        st.markdown('<h3 class="gradient-text">👋 Welcome Back!</h3>', unsafe_allow_html=True)
        
        with st.form("login_form"):
            username = st.text_input("Username", placeholder="Enter your username")
            password = st.text_input("Password", type="password", placeholder="Enter your password")
            
            login_button = st.form_submit_button("🔐 Login", use_container_width=True)
            
            if login_button:
                if not username or not password:
                    st.error("Please fill in all fields!")
                else:
                    success, message = authenticate_user(username, password)
                    if success:
                        st.session_state["authenticated"] = True
                        st.session_state["username"] = username
                        st.session_state["session_timestamp"] = get_session_timestamp()
                        save_session_data()  # Save session data on login
                        st.success(message)
                        st.rerun()
                    else:
                        st.error(message)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab2:
        st.markdown('<div class="login-form">', unsafe_allow_html=True)
        st.markdown('<h3 class="gradient-text">🎯 Join Our Platform!</h3>', unsafe_allow_html=True)
        
        with st.form("register_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                reg_username = st.text_input("Username*", placeholder="Choose a username")
                reg_email = st.text_input("Email*", placeholder="your@email.com")
                reg_full_name = st.text_input("Full Name*", placeholder="Your full name")
            
            with col2:
                reg_password = st.text_input("Password*", type="password", placeholder="Choose a strong password")
                reg_confirm_password = st.text_input("Confirm Password*", type="password", placeholder="Confirm your password")
                reg_role = st.selectbox("Role", ["personal", "employee", "manager"])
            
            reg_company_code = st.text_input("Company Code (Optional)", placeholder="Enter company code if joining a company")
            
            register_button = st.form_submit_button("📝 Create Account", use_container_width=True)
            
            if register_button:
                if not all([reg_username, reg_email, reg_full_name, reg_password, reg_confirm_password]):
                    st.error("Please fill in all required fields!")
                elif reg_password != reg_confirm_password:
                    st.error("Passwords do not match!")
                elif len(reg_password) < 6:
                    st.error("Password must be at least 6 characters long!")
                else:
                    success, message = register_user(reg_username, reg_password, reg_email, reg_full_name, reg_role, reg_company_code)
                    if success:
                        st.success(message)
                        st.info("You can now login with your credentials!")
                    else:
                        st.error(message)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab3:
        st.markdown('<div class="login-form">', unsafe_allow_html=True)
        st.markdown('<h3 class="gradient-text">🏢 Create Your Company</h3>', unsafe_allow_html=True)
        
        st.info("⚠️ You must be logged in to create a company. Please login first, then access Company Management from the sidebar.")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Feature showcase
    st.markdown("---")
    st.markdown("""
    <div class="floating-card">
        <h3 class="gradient-text">🚀 Platform Features</h3>
        <div class="stats-grid">
            <div>
                <h4>👤 Personal Mode</h4>
                <p>✅ Task Management<br>📝 Note Taking<br>👥 Contact Management<br>🎯 Goal Tracking</p>
            </div>
            <div>
                <h4>🏢 Company Mode</h4>
                <p>👥 Employee Management<br>📋 Task Assignment<br>📊 Team Analytics<br>🔔 Notifications</p>
            </div>
            <div>
                <h4>📈 Analytics</h4>
                <p>📊 Personal Dashboard<br>🏆 Team Performance<br>📈 Progress Tracking<br>📋 Detailed Reports</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# -------------------------------------------------------------
# Helper Functions
# -------------------------------------------------------------
def load_data():
    """Load user data."""
    if "username" not in st.session_state:
        return {}
    
    username = st.session_state["username"]
    user_file = Path(f"user_{username}.json")
    
    if not user_file.exists():
        initial_data = {
            "tasks": [],
            "notes": [],
            "contacts": [],
            "goals": [],
            "assigned_tasks": [],
            "team_notifications": [],
            "categories": ["Work", "Personal", "Health", "Learning", "Finance", "Team"],
            "settings": {
                "theme": "light",
                "notifications": True,
                "notification_sound": True,
                "notification_popup": True,
                "default_priority": "medium",
                "show_team_tasks": True
            }
        }
        user_file.write_text(json.dumps(initial_data, indent=2), encoding="utf-8")
    
    with user_file.open("r", encoding="utf-8") as f:
        return json.load(f)

def save_data(data: dict):
    """Save user data."""
    if "username" not in st.session_state:
        return
    
    username = st.session_state["username"]
    user_file = Path(f"user_{username}.json")
    
    with user_file.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def get_current_timestamp():
    """Get current timestamp."""
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def get_session_timestamp():
    """Get current timestamp for session management."""
    return datetime.datetime.now().timestamp()

def is_session_valid(session_timestamp: float, timeout_hours: int = 48) -> bool:
    """Check if session is still valid based on timestamp and timeout."""
    if not session_timestamp:
        return False
    
    current_time = datetime.datetime.now().timestamp()
    session_age_hours = (current_time - session_timestamp) / 3600
    
    return session_age_hours < timeout_hours

def refresh_session():
    """Refresh the session timestamp for active users."""
    if "authenticated" in st.session_state and st.session_state["authenticated"]:
        st.session_state["session_timestamp"] = get_session_timestamp()
        save_session_data()

def save_session_data():
    """Save session data to persistent storage."""
    if "authenticated" in st.session_state and st.session_state["authenticated"]:
        session_data = {
            "username": st.session_state.get("username", ""),
            "session_timestamp": st.session_state.get("session_timestamp"),
            "current_page": st.session_state.get("current_page", "dashboard")
        }
        
        session_file = Path("session_data.json")
        with session_file.open("w", encoding="utf-8") as f:
            json.dump(session_data, f, indent=2, ensure_ascii=False)

def load_session_data():
    """Load session data from persistent storage."""
    session_file = Path("session_data.json")
    if session_file.exists():
        try:
            with session_file.open("r", encoding="utf-8") as f:
                session_data = json.load(f)
            
            # Check if session is still valid
            session_timestamp = session_data.get("session_timestamp")
            if session_timestamp and is_session_valid(session_timestamp, timeout_hours=48):
                return session_data
            else:
                # Session expired, remove the file
                session_file.unlink(missing_ok=True)
        except Exception as e:
            # If there's any error reading the file, remove it
            session_file.unlink(missing_ok=True)
    
    return None

def clear_session_data():
    """Clear persistent session data."""
    session_file = Path("session_data.json")
    session_file.unlink(missing_ok=True)

def validate_content(content: str) -> tuple[bool, str]:
    """Validate content for inappropriate language."""
    inappropriate_words = [
        "fuck", "shit", "bitch", "ass", "dick", "pussy", "cock", "cunt", "whore", "slut",
        "nigger", "faggot", "retard", "idiot", "stupid", "dumb", "moron"
    ]
    
    content_lower = content.lower()
    for word in inappropriate_words:
        if word in content_lower:
            return False, f"Content contains inappropriate language: '{word}'"
    
    return True, "Content is appropriate"

def assign_task_to_user(from_username: str, to_username: str, task_data: dict):
    """Assign a task to another user."""
    # Load target user's data
    target_user_file = Path(f"user_{to_username}.json")
    if not target_user_file.exists():
        return False, "Target user not found!"
    
    with target_user_file.open("r", encoding="utf-8") as f:
        target_data = json.load(f)
    
    # Create assigned task
    assigned_task = {
        "id": str(uuid.uuid4()),
        "title": task_data["title"],
        "description": task_data.get("description", ""),
        "category": task_data.get("category", "Work"),
        "priority": task_data.get("priority", "medium"),
        "due_date": task_data.get("due_date"),
        "assigned_by": from_username,
        "assigned_to": to_username,
        "assigned_at": get_current_timestamp(),
        "status": "assigned",
        "completed": False,
        "feedback": "",
        "tags": task_data.get("tags", [])
    }
    
    # Add to target user's assigned tasks
    if "assigned_tasks" not in target_data:
        target_data["assigned_tasks"] = []
    target_data["assigned_tasks"].append(assigned_task)
    
    # Save target user's data
    with target_user_file.open("w", encoding="utf-8") as f:
        json.dump(target_data, f, indent=2, ensure_ascii=False)
    
    # Send enhanced task notification
    send_task_notification(to_username, task_data['title'], "assigned", from_username, "high")
    
    return True, "Task assigned successfully!"

def get_role_display(role: str) -> str:
    """Get role display with badge."""
    role_badges = {
        "admin": '<span class="role-badge admin-badge">Admin</span>',
        "manager": '<span class="role-badge manager-badge">Manager</span>',
        "employee": '<span class="role-badge employee-badge">Employee</span>',
        "personal": '<span class="role-badge personal-badge">Personal</span>'
    }
    return role_badges.get(role, f'<span class="role-badge">{role.title()}</span>')

def calculate_team_stats(company_code: str) -> dict:
    """Calculate team statistics."""
    employees = get_company_employees(company_code)
    
    total_employees = len(employees)
    active_employees = len([e for e in employees if e.get("active", True)])
    
    # Calculate task statistics across all employees
    total_tasks = 0
    completed_tasks = 0
    
    for employee in employees:
        username = employee.get("username")
        user_file = Path(f"user_{username}.json")
        
        if user_file.exists():
            with user_file.open("r", encoding="utf-8") as f:
                user_data = json.load(f)
                
                # Count assigned tasks
                assigned_tasks = user_data.get("assigned_tasks", [])
                total_tasks += len(assigned_tasks)
                completed_tasks += len([t for t in assigned_tasks if t.get("completed", False)])
    
    completion_rate = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
    
    return {
        "total_employees": total_employees,
        "active_employees": active_employees,
        "total_tasks": total_tasks,
        "completed_tasks": completed_tasks,
        "completion_rate": completion_rate
    }

# -------------------------------------------------------------
# Main Application
# -------------------------------------------------------------
# -------------------------------------------------------------
# Main Application
# -------------------------------------------------------------
def main():
    # Add custom CSS for notifications
    st.markdown("""
    <style>
    /* Notification popup styles */
    .notification-popup {
        position: fixed;
        top: 20px;
        right: 20px;
        background: white;
        border-radius: 8px;
        padding: 16px;
        max-width: 350px;
        z-index: 10000;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        animation: slideIn 0.3s ease-out;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    }
    
    @keyframes slideIn {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
    
    /* Enhanced notification card styles */
    .notification-card {
        background: white;
        border-radius: 8px;
        padding: 16px;
        margin-bottom: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
    }
    
    .notification-card:hover {
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        transform: translateY(-2px);
    }
    
    .notification-card.unread {
        border-left: 4px solid #ff4444;
        background: #f8f9fa;
    }
    
    /* Priority indicators */
    .priority-high {
        border-left-color: #ff4444 !important;
    }
    
    .priority-normal {
        border-left-color: #2196F3 !important;
    }
    
    .priority-low {
        border-left-color: #4CAF50 !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Initialize session state
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False
    if "username" not in st.session_state:
        st.session_state["username"] = ""
    if "current_page" not in st.session_state:
        st.session_state["current_page"] = "dashboard"
    if "session_timestamp" not in st.session_state:
        st.session_state["session_timestamp"] = None
    
    # Try to restore session from persistent storage if not authenticated
    if not st.session_state["authenticated"]:
        saved_session = load_session_data()
        if saved_session:
            st.session_state["authenticated"] = True
            st.session_state["username"] = saved_session.get("username", "")
            st.session_state["session_timestamp"] = saved_session.get("session_timestamp")
            st.session_state["current_page"] = saved_session.get("current_page", "dashboard")
            st.success("🔄 Session restored successfully!")
    
    # Session validation and automatic login
    if st.session_state["authenticated"]:
        session_timestamp = st.session_state.get("session_timestamp")
        if session_timestamp is None or not is_session_valid(session_timestamp, timeout_hours=48):
            # Session expired
            st.session_state["authenticated"] = False
            st.session_state["username"] = ""
            st.session_state["session_timestamp"] = None
            st.session_state["current_page"] = "dashboard"
            clear_session_data()  # Clear persistent session data
            st.warning("⚠️ Your session has expired. Please login again.")
            show_login_page()
            return
    
    # Authentication check
    if not st.session_state["authenticated"]:
        show_login_page()
        return
    
    # Load user data
    username = st.session_state["username"]
    user_info = get_user_info(username)
    company_info = get_user_company_info(username)
    data = load_data()
    
    # Sidebar navigation
    with st.sidebar:
        # Session status
        session_timestamp = st.session_state.get("session_timestamp")
        if session_timestamp:
            session_age_hours = (datetime.datetime.now().timestamp() - session_timestamp) / 3600
            remaining_hours = max(0, 48 - session_age_hours)
            session_status = f"🟢 Session Active ({remaining_hours:.1f}h remaining)"
        else:
            session_status = "🔴 Session Expired"
        
        st.markdown(f"""
        <div class="sidebar-section">
            <h3>👋 Welcome!</h3>
            <p><strong>{user_info.get('full_name', username)}</strong></p>
            {get_role_display(user_info.get('role', 'personal'))}
            <p style="font-size: 0.8em; margin-top: 8px; color: #666;">{session_status}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Company info
        if company_info:
            st.markdown(f"""
            <div class="company-card">
                <h4>🏢 {company_info.get('name', 'Unknown Company')}</h4>
                <p>{company_info.get('description', 'No description available')}</p>
                <small>Code: {user_info.get('company_code', 'N/A')}</small>
            </div>
            """, unsafe_allow_html=True)
        
        # Navigation menu
        st.markdown("### 🧭 Navigation")
        
        # Personal features
        if st.button("🏠 Dashboard", use_container_width=True):
            st.session_state["current_page"] = "dashboard"
            save_session_data()
        
        if st.button("📋 My Tasks", use_container_width=True):
            st.session_state["current_page"] = "tasks"
            save_session_data()
        
        if st.button("📝 Notes", use_container_width=True):
            st.session_state["current_page"] = "notes"
            save_session_data()
        
        if st.button("👥 Contacts", use_container_width=True):
            st.session_state["current_page"] = "contacts"
            save_session_data()
        
        if st.button("🎯 Goals", use_container_width=True):
            st.session_state["current_page"] = "goals"
            save_session_data()
        
        # Company features
        if company_info and company_info.get("name"):
            st.markdown("### 🏢 Company Features")
            
            if st.button("👥 Team Members", use_container_width=True):
                st.session_state["current_page"] = "team"
                save_session_data()
            
            if can_assign_tasks(username):
                if st.button("📋 Assign Tasks", use_container_width=True):
                    st.session_state["current_page"] = "assign_tasks"
                    save_session_data()
            
            if st.button("📊 Team Analytics", use_container_width=True):
                st.session_state["current_page"] = "analytics"
                save_session_data()
            
            # Chat features for company members
            if st.button("💬 Company Chat", use_container_width=True):
                st.session_state["current_page"] = "company_chat"
                save_session_data()
            
            if st.button("💬 Private Chat", use_container_width=True):
                st.session_state["current_page"] = "private_chat"
                save_session_data()
            
            # File sharing
            if st.button("📁 File Sharing", use_container_width=True):
                st.session_state["current_page"] = "file_sharing"
                save_session_data()
            
            # Calendar
            if st.button("📅 Calendar", use_container_width=True):
                st.session_state["current_page"] = "calendar"
                save_session_data()
            
            # Polls
            if st.button("📊 Polls", use_container_width=True):
                st.session_state["current_page"] = "polls"
                save_session_data()
            
            # Search
            if st.button("🔍 Search", use_container_width=True):
                st.session_state["current_page"] = "search"
                save_session_data()
            
            if user_info.get("role") in ["admin", "manager", "ceo", "cfo", "cto", "vp", "director"]:
                if st.button("👥 Role Management", use_container_width=True):
                    st.session_state["current_page"] = "role_management"
                    save_session_data()
            
            if user_info.get("role") in ["admin", "manager"]:
                if st.button("⚙️ Company Settings", use_container_width=True):
                    st.session_state["current_page"] = "company_settings"
                    save_session_data()
        
        # Advanced Management Features (Upper Level)
        if user_info.get("role") in ["admin", "manager", "ceo", "cfo", "cto", "vp", "director", "senior_manager"]:
            st.markdown("### 🚀 Advanced Management")
            
            if st.button("📊 Project Management", use_container_width=True):
                st.session_state["current_page"] = "project_management"
                save_session_data()
            
            if st.button("🏢 Department Management", use_container_width=True):
                st.session_state["current_page"] = "department_management"
                save_session_data()
            
            if st.button("📈 Performance Reviews", use_container_width=True):
                st.session_state["current_page"] = "performance_reviews"
                save_session_data()
            
            if st.button("💰 Budget Management", use_container_width=True):
                st.session_state["current_page"] = "budget_management"
                save_session_data()
            
            if st.button("📋 Advanced Reports", use_container_width=True):
                st.session_state["current_page"] = "advanced_reports"
                save_session_data()
            
            if st.button("🔄 Workflow Management", use_container_width=True):
                st.session_state["current_page"] = "workflow_management"
                save_session_data()
            
            if st.button("📚 Knowledge Base", use_container_width=True):
                st.session_state["current_page"] = "knowledge_base"
                save_session_data()
            
            if st.button("🔗 Integrations", use_container_width=True):
                st.session_state["current_page"] = "integrations"
                save_session_data()
    
        # Company creation for users without a company
        if not company_info:
            st.markdown("### 🏢 Company Management")
            if st.button("🏢 Create Company", use_container_width=True):
                st.session_state["current_page"] = "create_company"
                save_session_data()
        
        # Notifications with enhanced counter
        notifications = get_user_notifications(username)
        unread_count = len([n for n in notifications if not n.get("read", False)])
        
        # Show notification button with badge
        if unread_count > 0:
            notification_text = f"🔔 Notifications ({unread_count})"
            button_style = "background-color: #ff4444; color: white; border: none; border-radius: 8px; padding: 8px 16px; font-weight: bold;"
        else:
            notification_text = "🔔 Notifications"
            button_style = ""
        
        if st.button(notification_text, use_container_width=True, key="notifications_button"):
            st.session_state["current_page"] = "notifications"
            save_session_data()
        
        # Settings and logout
        st.markdown("---")
        if st.button("⚙️ Settings", use_container_width=True):
            st.session_state["current_page"] = "settings"
            save_session_data()
        
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state["authenticated"] = False
            st.session_state["username"] = ""
            st.session_state["session_timestamp"] = None
            st.session_state["current_page"] = "dashboard"
            clear_session_data()  # Clear persistent session data on logout
            st.rerun()
    
    # Check for new notifications and show popups
    check_and_show_new_notifications(username)
    
    # Main content area
    current_page = st.session_state.get("current_page", "dashboard")
    
    if current_page == "dashboard":
        show_dashboard(username, user_info, company_info, data)
    elif current_page == "tasks":
        show_tasks_page(data)
    elif current_page == "notes":
        show_notes_page(data)
    elif current_page == "contacts":
        show_contacts_page(data)
    elif current_page == "goals":
        show_goals_page(data)
    elif current_page == "team":
        show_team_page(company_info)
    elif current_page == "assign_tasks":
        show_assign_tasks_page(username, company_info)
    elif current_page == "analytics":
        show_analytics_page(company_info)
    elif current_page == "company_settings":
        show_company_settings_page(username, company_info)
    elif current_page == "company_chat":
        show_company_chat_page(username, company_info)
    elif current_page == "role_management":
        show_role_management_page(username, company_info)
    elif current_page == "private_chat":
        show_private_chat_page(username, company_info)
    elif current_page == "file_sharing":
        show_file_sharing_page(username, company_info)
    elif current_page == "calendar":
        show_calendar_page(username, company_info)
    elif current_page == "polls":
        show_polls_page(username, company_info)
    elif current_page == "search":
        show_search_page(username, company_info)
    elif current_page == "create_company":
        show_create_company_page(username)
    elif current_page == "notifications":
        show_notifications_page(username)
    elif current_page == "settings":
        show_settings_page(data)
    # Advanced Management Pages
    elif current_page == "project_management":
        show_project_management_page(username, company_info)
    elif current_page == "department_management":
        show_department_management_page(username, company_info)
    elif current_page == "performance_reviews":
        show_performance_reviews_page(username, company_info)
    elif current_page == "budget_management":
        show_budget_management_page(username, company_info)
    elif current_page == "advanced_reports":
        show_advanced_reports_page(username, company_info)
    elif current_page == "workflow_management":
        show_workflow_management_page(username, company_info)
    elif current_page == "knowledge_base":
        show_knowledge_base_page(username, company_info)
    elif current_page == "integrations":
        show_integrations_page(username, company_info)

def show_dashboard(username: str, user_info: dict, company_info: dict, data: dict):
    """Show main dashboard."""
    st.markdown(f"""
    <div class="welcome-header">
        <h1>🏠 Welcome to Your Dashboard</h1>
        <p>Hello, <strong>{user_info.get('full_name', username)}</strong>! Here's your productivity overview.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Quick stats
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_tasks = len(data.get("tasks", []))
        st.markdown(f"""
        <div class="metric-card">
            <h3>📋 Total Tasks</h3>
            <h2>{total_tasks}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        completed_tasks = len([t for t in data.get("tasks", []) if t.get("completed", False)])
        st.markdown(f"""
        <div class="metric-card">
            <h3>✅ Completed</h3>
            <h2>{completed_tasks}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        pending_tasks = total_tasks - completed_tasks
        st.markdown(f"""
        <div class="metric-card">
            <h3>⏳ Pending</h3>
            <h2>{pending_tasks}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        total_notes = len(data.get("notes", []))
        st.markdown(f"""
        <div class="metric-card">
            <h3>📝 Notes</h3>
            <h2>{total_notes}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    # Recent tasks and assigned tasks
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📋 Recent Active Tasks")
        tasks = data.get("tasks", [])
        incomplete_tasks = [t for t in tasks if not t.get("completed", False)]
        recent_incomplete_tasks = sorted(incomplete_tasks, key=lambda x: x.get("created_at", ""), reverse=True)[:5]
        
        if recent_incomplete_tasks:
            for task in recent_incomplete_tasks:
                priority_class = f"{task.get('priority', 'medium')}-priority"
                
                st.markdown(f"""
                <div class="task-card {priority_class}">
                    <h4>⏳ {task.get('title', 'Untitled')}</h4>
                    <p><strong>Category:</strong> {task.get('category', 'General')}</p>
                    <p><strong>Priority:</strong> {task.get('priority', 'medium').title()}</p>
                    {f"<p><strong>Due:</strong> {task.get('due_date', 'No due date')}</p>" if task.get('due_date') else ""}
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No active tasks. Create your first task!")
    
    with col2:
        st.markdown("### 📋 Active Assigned Tasks")
        assigned_tasks = data.get("assigned_tasks", [])
        incomplete_assigned_tasks = [t for t in assigned_tasks if not t.get("completed", False)]
        
        if incomplete_assigned_tasks:
            for task in incomplete_assigned_tasks[-5:]:  # Show last 5
                st.markdown(f"""
                <div class="task-card assigned-task">
                    <h4>⏳ {task.get('title', 'Untitled')}</h4>
                    <p><strong>Assigned by:</strong> {task.get('assigned_by', 'Unknown')}</p>
                    <p><strong>Priority:</strong> {task.get('priority', 'medium').title()}</p>
                    <p><strong>Status:</strong> {task.get('status', 'assigned').title()}</p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No active assigned tasks.")
    
    # Team dashboard (if part of company)
    if company_info:
        st.markdown("---")
        st.markdown(f"""
        <div class="team-header">
            <h2>🏢 Team Dashboard - {company_info.get('name', 'Unknown Company')}</h2>
        </div>
        """, unsafe_allow_html=True)
        
        company_code = user_info.get("company_code")
        if company_code:
            team_stats = calculate_team_stats(company_code)
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.markdown(f"""
                <div class="metric-card">
                    <h3>👥 Team Members</h3>
                    <h2>{team_stats['total_employees']}</h2>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div class="metric-card">
                    <h3>📋 Team Tasks</h3>
                    <h2>{team_stats['total_tasks']}</h2>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown(f"""
                <div class="metric-card">
                    <h3>✅ Completed</h3>
                    <h2>{team_stats['completed_tasks']}</h2>
                </div>
                """, unsafe_allow_html=True)
            
            with col4:
                st.markdown(f"""
                <div class="metric-card">
                    <h3>📊 Completion Rate</h3>
                    <h2>{team_stats['completion_rate']:.1f}%</h2>
                </div>
                """, unsafe_allow_html=True)

def show_tasks_page(data: dict):
    """Show tasks management page."""
    st.markdown("""
    <div class="main-header">
        <h1>📋 Task Management</h1>
        <p>Organize and track your tasks efficiently</p>
    </div>
    """, unsafe_allow_html=True)
    
    current_user = st.session_state.get("username", "")
    
    # Task creation form - allow all users to create personal tasks
    with st.expander("➕ Create New Task", expanded=False):
        with st.form("create_task"):
            col1, col2 = st.columns(2)
            
            with col1:
                task_title = st.text_input("Task Title*", placeholder="Enter task title")
                task_category = st.selectbox("Category", data.get("categories", ["Work", "Personal", "Health"]))
                task_priority = st.selectbox("Priority", ["low", "medium", "high"])
            
            with col2:
                task_description = st.text_area("Description", placeholder="Task description (optional)")
                task_due_date = st.date_input("Due Date (Optional)")
                task_tags = st.text_input("Tags (comma-separated)", placeholder="urgent, meeting, review")
            
            submit_task = st.form_submit_button("🚀 Create Task", use_container_width=True)
            
            if submit_task:
                if not task_title.strip():
                    st.error("Please enter a task title!")
                else:
                    # Validate content
                    title_valid, title_error = validate_content(task_title.strip())
                    desc_valid, desc_error = validate_content(task_description.strip())
                    
                    if not title_valid:
                        st.error(f"Task title: {title_error}")
                    elif not desc_valid:
                        st.error(f"Task description: {desc_error}")
                    else:
                        new_task = {
                            "id": str(uuid.uuid4()),
                            "title": task_title.strip(),
                            "description": task_description.strip(),
                            "category": task_category,
                            "priority": task_priority,
                            "due_date": task_due_date.strftime("%Y-%m-%d") if task_due_date else None,
                            "tags": [tag.strip() for tag in task_tags.split(",") if tag.strip()],
                            "completed": False,
                            "created_at": get_current_timestamp(),
                            "updated_at": get_current_timestamp()
                        }
                        
                        data["tasks"].append(new_task)
                        save_data(data)
                        refresh_session()  # Refresh session on task creation
                        st.success("Task created successfully!")
                        st.rerun()
    
    # Task listing section
    st.markdown("---")
    
    # Personal tasks - Only show incomplete tasks
    st.markdown("### 📋 Your Active Tasks")
    tasks = data.get("tasks", [])
    incomplete_tasks = [t for t in tasks if not t.get("completed", False)]
    
    if incomplete_tasks:
        # Filter and sort options for incomplete tasks
        col1, col2 = st.columns(2)
        
        with col1:
            filter_priority = st.selectbox("Filter by Priority", ["all", "high", "medium", "low"], key="personal_priority_filter")
        
        with col2:
            filter_category = st.selectbox("Filter by Category", ["all"] + data.get("categories", []), key="personal_category_filter")
        
        # Apply filters to incomplete tasks
        filtered_tasks = incomplete_tasks
        
        if filter_priority != "all":
            filtered_tasks = [t for t in filtered_tasks if t.get("priority") == filter_priority]
        
        if filter_category != "all":
            filtered_tasks = [t for t in filtered_tasks if t.get("category") == filter_category]
        
        # Sort tasks by priority and due date
        filtered_tasks = sorted(filtered_tasks, key=lambda x: (
            {"high": 0, "medium": 1, "low": 2}.get(x.get("priority", "medium"), 1),
            x.get("due_date", "9999-12-31")
        ))
        
        for task in filtered_tasks:
            priority_class = f"{task.get('priority', 'medium')}-priority"
            status = "✅" if task.get("completed", False) else "⏳"
            
            with st.container():
                st.markdown(f"""
                <div class="task-card {priority_class}">
                    <h4>{status} {task.get('title', 'Untitled')}</h4>
                    <p><strong>Category:</strong> {task.get('category', 'General')}</p>
                    <p><strong>Priority:</strong> {task.get('priority', 'medium').title()}</p>
                    {f"<p><strong>Due:</strong> {task.get('due_date', 'No due date')}</p>" if task.get('due_date') else ""}
                    {f"<p><strong>Description:</strong> {task.get('description', 'No description')}</p>" if task.get('description') else ""}
                    {f"<p><strong>Tags:</strong> {', '.join(task.get('tags', []))}</p>" if task.get('tags') else ""}
                    <p><strong>Created:</strong> {task.get('created_at', 'Unknown')}</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Show attachments if they exist
                if task.get("attachments"):
                    with st.expander(f"📎 Attachments ({len(task['attachments'])})"):
                        for attachment in task["attachments"]:
                            col1, col2 = st.columns([3, 1])
                            with col1:
                                st.write(f"📄 {attachment['name']} ({attachment['size']} bytes)")
                                st.write(f"Uploaded by: {attachment['uploaded_by']} on {attachment['uploaded_at']}")
                            with col2:
                                if st.button("📥 Download", key=f"download_{attachment['id']}"):
                                    st.download_button(
                                        label="Download File",
                                        data=attachment['content'],
                                        file_name=attachment['name'],
                                        mime=attachment['type']
                                    )
                
                # Show code snippets if they exist
                if task.get("code_snippets"):
                    with st.expander(f"💻 Code Snippets ({len(task['code_snippets'])})"):
                        for i, snippet in enumerate(task["code_snippets"]):
                            st.markdown(f"**Code by {snippet['user']} on {snippet['timestamp']}:**")
                            st.code(snippet['code'], language='python')
                
                # Show incomplete comments if they exist
                if task.get("incomplete_comments"):
                    with st.expander(f"💬 Incomplete Comments ({len(task['incomplete_comments'])})"):
                        for comment in task["incomplete_comments"]:
                            st.markdown(f"**{comment['user']} on {comment['timestamp']}:**")
                            st.write(comment['comment'])
                
                # Task actions
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    if not task.get("completed", False):
                        if st.button("✅ Mark Complete", key=f"complete_task_{task['id']}"):
                            task["completed"] = True
                            task["completed_at"] = get_current_timestamp()
                            task["updated_at"] = get_current_timestamp()
                            save_data(data)
                            refresh_session()  # Refresh session on task completion
                            st.success("Task marked as complete!")
                            st.rerun()
                    else:
                        if st.button("🔄 Mark Incomplete", key=f"incomplete_task_{task['id']}"):
                            st.session_state[f"mark_incomplete_{task['id']}"] = True
                
                with col2:
                    if st.button("✏️ Edit", key=f"edit_task_{task['id']}"):
                        st.session_state[f"edit_task_{task['id']}"] = True
                
                with col3:
                    if st.button("🗑️ Delete", key=f"delete_task_{task['id']}"):
                        if st.session_state.get(f"confirm_delete_task_{task['id']}"):
                            data["tasks"] = [t for t in data["tasks"] if t["id"] != task["id"]]
                            save_data(data)
                            refresh_session()  # Refresh session on task deletion
                            st.success("Task deleted!")
                            st.rerun()
                        else:
                            st.session_state[f"confirm_delete_task_{task['id']}"] = True
                            st.warning("Click delete again to confirm!")
                
                # Edit task form
                if st.session_state.get(f"edit_task_{task['id']}"):
                    with st.form(f"edit_task_form_{task['id']}"):
                        st.markdown("#### Edit Task")
                        
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            edit_title = st.text_input("Title", value=task.get("title", ""))
                            edit_category = st.selectbox("Category", data.get("categories", []), 
                                                       index=data.get("categories", []).index(task.get("category", "Work")) if task.get("category") in data.get("categories", []) else 0)
                            edit_priority = st.selectbox("Priority", ["low", "medium", "high"], 
                                                       index=["low", "medium", "high"].index(task.get("priority", "medium")))
                        
                        with col2:
                            edit_description = st.text_area("Description", value=task.get("description", ""))
                            edit_due_date = st.date_input("Due Date", 
                                                       value=datetime.datetime.strptime(task.get("due_date", "2024-12-31"), "%Y-%m-%d").date() if task.get("due_date") else None)
                            edit_tags = st.text_input("Tags", value=", ".join(task.get("tags", [])))
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            if st.form_submit_button("💾 Save Changes"):
                                for t in data["tasks"]:
                                    if t["id"] == task["id"]:
                                        t["title"] = edit_title
                                        t["description"] = edit_description
                                        t["category"] = edit_category
                                        t["priority"] = edit_priority
                                        t["due_date"] = edit_due_date.strftime("%Y-%m-%d") if edit_due_date else None
                                        t["tags"] = [tag.strip() for tag in edit_tags.split(",") if tag.strip()]
                                        t["updated_at"] = get_current_timestamp()
                                        break
                                save_data(data)
                                st.session_state[f"edit_task_{task['id']}"] = False
                                st.success("Task updated!")
                                st.rerun()
                        
                        with col2:
                            if st.form_submit_button("❌ Cancel"):
                                st.session_state[f"edit_task_{task['id']}"] = False
                                st.rerun()
                
                # Mark incomplete with attachments form
                if st.session_state.get(f"mark_incomplete_{task['id']}"):
                    with st.form(f"mark_incomplete_form_{task['id']}"):
                        st.markdown("#### 🔄 Mark Task as Incomplete")
                        st.info("You can add files or code snippets when marking this task as incomplete.")
                        
                        # File upload
                        uploaded_files = st.file_uploader(
                            "Upload files (optional)", 
                            type=['txt', 'pdf', 'doc', 'docx', 'py', 'js', 'html', 'css', 'json', 'xml', 'csv', 'md'],
                            accept_multiple_files=True,
                            key=f"files_{task['id']}"
                        )
                        
                        # Code snippet
                        code_snippet = st.text_area(
                            "Add code snippet (optional)", 
                            placeholder="Paste your code here...",
                            height=150,
                            key=f"code_{task['id']}"
                        )
                        
                        # Comments
                        comments = st.text_area(
                            "Add comments (optional)", 
                            placeholder="Why is this task being marked as incomplete?",
                            key=f"comments_{task['id']}"
                        )
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            if st.form_submit_button("✅ Mark Incomplete"):
                                # Mark task as incomplete
                                task["completed"] = False
                                task["updated_at"] = get_current_timestamp()
                                if "completed_at" in task:
                                    del task["completed_at"]
                                
                                # Add comments if provided
                                if comments.strip():
                                    if "incomplete_comments" not in task:
                                        task["incomplete_comments"] = []
                                    task["incomplete_comments"].append({
                                        "comment": comments.strip(),
                                        "timestamp": get_current_timestamp(),
                                        "user": st.session_state.get("username", "Unknown")
                                    })
                                
                                # Add code snippet if provided
                                if code_snippet.strip():
                                    if "code_snippets" not in task:
                                        task["code_snippets"] = []
                                    task["code_snippets"].append({
                                        "code": code_snippet.strip(),
                                        "timestamp": get_current_timestamp(),
                                        "user": st.session_state.get("username", "Unknown")
                                    })
                                
                                # Handle file uploads
                                if uploaded_files:
                                    if "attachments" not in task:
                                        task["attachments"] = []
                                    
                                    for uploaded_file in uploaded_files:
                                        file_content = uploaded_file.read()
                                        attachment = {
                                            "id": str(uuid.uuid4()),
                                            "name": uploaded_file.name,
                                            "type": uploaded_file.type or "unknown",
                                            "size": len(file_content),
                                            "uploaded_at": get_current_timestamp(),
                                            "uploaded_by": st.session_state.get("username", "Unknown"),
                                            "content": file_content
                                        }
                                        task["attachments"].append(attachment)
                                
                                save_data(data)
                                st.session_state[f"mark_incomplete_{task['id']}"] = False
                                st.success("Task marked as incomplete with attachments!")
                                st.rerun()
                        
                        with col2:
                            if st.form_submit_button("❌ Cancel"):
                                st.session_state[f"mark_incomplete_{task['id']}"] = False
                                st.rerun()
                
                st.markdown("---")
    else:
        st.info("No active tasks. Create your first task!")
    
    # Completed tasks section
    completed_tasks = [t for t in tasks if t.get("completed", False)]
    if completed_tasks:
        st.markdown("### ✅ Completed Tasks")
        st.info(f"You have {len(completed_tasks)} completed tasks. They are archived here for reference.")
        
        # Show completed tasks in a compact format
        for task in completed_tasks[-10:]:  # Show last 10 completed tasks
            completed_date = task.get("completed_at", "Unknown")
            st.markdown(f"""
            <div class="task-card completed-task" style="opacity: 0.7;">
                <h5>✅ {task.get('title', 'Untitled')}</h5>
                <p><strong>Completed:</strong> {completed_date}</p>
                <p><strong>Category:</strong> {task.get('category', 'General')} | <strong>Priority:</strong> {task.get('priority', 'medium').title()}</p>
            </div>
            """, unsafe_allow_html=True)
        
        if len(completed_tasks) > 10:
            st.info(f"Showing last 10 of {len(completed_tasks)} completed tasks")
        
        # Option to view all completed tasks
        if st.button("📋 View All Completed Tasks", key="view_all_completed"):
            st.session_state["show_all_completed"] = True
        
        if st.session_state.get("show_all_completed"):
            st.markdown("#### 📋 All Completed Tasks")
            for task in completed_tasks:
                completed_date = task.get("completed_at", "Unknown")
                st.markdown(f"""
                <div class="task-card completed-task" style="opacity: 0.7;">
                    <h5>✅ {task.get('title', 'Untitled')}</h5>
                    <p><strong>Completed:</strong> {completed_date}</p>
                    <p><strong>Category:</strong> {task.get('category', 'General')} | <strong>Priority:</strong> {task.get('priority', 'medium').title()}</p>
                    {f"<p><strong>Description:</strong> {task.get('description', 'No description')}</p>" if task.get('description') else ""}
                </div>
                """, unsafe_allow_html=True)
            
            if st.button("🔽 Hide All Completed Tasks", key="hide_all_completed"):
                st.session_state["show_all_completed"] = False
                st.rerun()
    
    # Assigned tasks - Only show incomplete assigned tasks
    st.markdown("### 📋 Active Assigned Tasks")
    assigned_tasks = data.get("assigned_tasks", [])
    incomplete_assigned_tasks = [t for t in assigned_tasks if not t.get("completed", False)]
    
    if incomplete_assigned_tasks:
        for task in incomplete_assigned_tasks:
            status = "✅" if task.get("completed", False) else "⏳"
            
            with st.container():
                st.markdown(f"""
                <div class="task-card assigned-task">
                    <h4>{status} {task.get('title', 'Untitled')}</h4>
                    <p><strong>Assigned by:</strong> {task.get('assigned_by', 'Unknown')}</p>
                    <p><strong>Category:</strong> {task.get('category', 'General')}</p>
                    <p><strong>Priority:</strong> {task.get('priority', 'medium').title()}</p>
                    <p><strong>Status:</strong> {task.get('status', 'assigned').title()}</p>
                    {f"<p><strong>Due:</strong> {task.get('due_date', 'No due date')}</p>" if task.get('due_date') else ""}
                    {f"<p><strong>Description:</strong> {task.get('description', 'No description')}</p>" if task.get('description') else ""}
                    <p><strong>Assigned on:</strong> {task.get('assigned_at', 'Unknown')}</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Show attachments if they exist
                if task.get("attachments"):
                    with st.expander(f"📎 Attachments ({len(task['attachments'])})"):
                        for attachment in task["attachments"]:
                            col1, col2 = st.columns([3, 1])
                            with col1:
                                st.write(f"📄 {attachment['name']} ({attachment['size']} bytes)")
                                st.write(f"Uploaded by: {attachment['uploaded_by']} on {attachment['uploaded_at']}")
                            with col2:
                                if st.button("📥 Download", key=f"download_assigned_{attachment['id']}"):
                                    st.download_button(
                                        label="Download File",
                                        data=attachment['content'],
                                        file_name=attachment['name'],
                                        mime=attachment['type']
                                    )
                
                # Show code snippets if they exist
                if task.get("code_snippets"):
                    with st.expander(f"💻 Code Snippets ({len(task['code_snippets'])})"):
                        for i, snippet in enumerate(task["code_snippets"]):
                            st.markdown(f"**Code by {snippet['user']} on {snippet['timestamp']}:**")
                            st.code(snippet['code'], language='python')
                
                # Show incomplete comments if they exist
                if task.get("incomplete_comments"):
                    with st.expander(f"💬 Incomplete Comments ({len(task['incomplete_comments'])})"):
                        for comment in task["incomplete_comments"]:
                            st.markdown(f"**{comment['user']} on {comment['timestamp']}:**")
                            st.write(comment['comment'])
                
                # Assigned task actions
                col1, col2 = st.columns(2)
                
                with col1:
                    if not task.get("completed", False):
                        if st.button("✅ Mark Complete", key=f"complete_assigned_{task['id']}"):
                            task["completed"] = True
                            task["completed_at"] = get_current_timestamp()
                            task["updated_at"] = get_current_timestamp()
                            save_data(data)
                            st.success("Task marked as complete!")
                            st.rerun()
                    else:
                        if st.button("🔄 Mark Incomplete", key=f"incomplete_assigned_{task['id']}"):
                            st.session_state[f"mark_incomplete_assigned_{task['id']}"] = True
                
                with col2:
                    if st.button("💬 Add Feedback", key=f"feedback_{task['id']}"):
                        st.session_state[f"add_feedback_{task['id']}"] = True
                
                # Add feedback form
                if st.session_state.get(f"add_feedback_{task['id']}"):
                    with st.form(f"feedback_form_{task['id']}"):
                        feedback = st.text_area("Add feedback or comments", value=task.get("feedback", ""))
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            if st.form_submit_button("💾 Save Feedback"):
                                task["feedback"] = feedback
                                task["updated_at"] = get_current_timestamp()
                                save_data(data)
                                st.session_state[f"add_feedback_{task['id']}"] = False
                                st.success("Feedback added!")
                                st.rerun()
                        
                        with col2:
                            if st.form_submit_button("❌ Cancel"):
                                st.session_state[f"add_feedback_{task['id']}"] = False
                                st.rerun()
                
                # Mark incomplete with attachments form for assigned tasks
                if st.session_state.get(f"mark_incomplete_assigned_{task['id']}"):
                    with st.form(f"mark_incomplete_assigned_form_{task['id']}"):
                        st.markdown("#### 🔄 Mark Assigned Task as Incomplete")
                        st.info("You can add files or code snippets when marking this task as incomplete.")
                        
                        # File upload
                        uploaded_files = st.file_uploader(
                            "Upload files (optional)", 
                            type=['txt', 'pdf', 'doc', 'docx', 'py', 'js', 'html', 'css', 'json', 'xml', 'csv', 'md'],
                            accept_multiple_files=True,
                            key=f"assigned_files_{task['id']}"
                        )
                        
                        # Code snippet
                        code_snippet = st.text_area(
                            "Add code snippet (optional)", 
                            placeholder="Paste your code here...",
                            height=150,
                            key=f"assigned_code_{task['id']}"
                        )
                        
                        # Comments
                        comments = st.text_area(
                            "Add comments (optional)", 
                            placeholder="Why is this task being marked as incomplete?",
                            key=f"assigned_comments_{task['id']}"
                        )
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            if st.form_submit_button("✅ Mark Incomplete"):
                                # Mark task as incomplete
                                task["completed"] = False
                                task["updated_at"] = get_current_timestamp()
                                if "completed_at" in task:
                                    del task["completed_at"]
                                
                                # Add comments if provided
                                if comments.strip():
                                    if "incomplete_comments" not in task:
                                        task["incomplete_comments"] = []
                                    task["incomplete_comments"].append({
                                        "comment": comments.strip(),
                                        "timestamp": get_current_timestamp(),
                                        "user": st.session_state.get("username", "Unknown")
                                    })
                                
                                # Add code snippet if provided
                                if code_snippet.strip():
                                    if "code_snippets" not in task:
                                        task["code_snippets"] = []
                                    task["code_snippets"].append({
                                        "code": code_snippet.strip(),
                                        "timestamp": get_current_timestamp(),
                                        "user": st.session_state.get("username", "Unknown")
                                    })
                                
                                # Handle file uploads
                                if uploaded_files:
                                    if "attachments" not in task:
                                        task["attachments"] = []
                                    
                                    for uploaded_file in uploaded_files:
                                        file_content = uploaded_file.read()
                                        attachment = {
                                            "id": str(uuid.uuid4()),
                                            "name": uploaded_file.name,
                                            "type": uploaded_file.type or "unknown",
                                            "size": len(file_content),
                                            "uploaded_at": get_current_timestamp(),
                                            "uploaded_by": st.session_state.get("username", "Unknown"),
                                            "content": file_content
                                        }
                                        task["attachments"].append(attachment)
                                
                                save_data(data)
                                st.session_state[f"mark_incomplete_assigned_{task['id']}"] = False
                                st.success("Task marked as incomplete with attachments!")
                                st.rerun()
                        
                        with col2:
                            if st.form_submit_button("❌ Cancel"):
                                st.session_state[f"mark_incomplete_assigned_{task['id']}"] = False
                                st.rerun()
                
                st.markdown("---")
    else:
        st.info("No active assigned tasks.")
    
    # Completed assigned tasks section
    completed_assigned_tasks = [t for t in assigned_tasks if t.get("completed", False)]
    if completed_assigned_tasks:
        st.markdown("### ✅ Completed Assigned Tasks")
        st.info(f"You have {len(completed_assigned_tasks)} completed assigned tasks.")
        
        # Show completed assigned tasks in a compact format
        for task in completed_assigned_tasks[-5:]:  # Show last 5 completed assigned tasks
            completed_date = task.get("completed_at", "Unknown")
            st.markdown(f"""
            <div class="task-card assigned-task" style="opacity: 0.7;">
                <h5>✅ {task.get('title', 'Untitled')}</h5>
                <p><strong>Assigned by:</strong> {task.get('assigned_by', 'Unknown')}</p>
                <p><strong>Completed:</strong> {completed_date}</p>
                <p><strong>Category:</strong> {task.get('category', 'General')} | <strong>Priority:</strong> {task.get('priority', 'medium').title()}</p>
            </div>
            """, unsafe_allow_html=True)
        
        if len(completed_assigned_tasks) > 5:
            st.info(f"Showing last 5 of {len(completed_assigned_tasks)} completed assigned tasks")
        
        # Option to view all completed assigned tasks
        if st.button("📋 View All Completed Assigned Tasks", key="view_all_completed_assigned"):
            st.session_state["show_all_completed_assigned"] = True
        
        if st.session_state.get("show_all_completed_assigned"):
            st.markdown("#### 📋 All Completed Assigned Tasks")
            for task in completed_assigned_tasks:
                completed_date = task.get("completed_at", "Unknown")
                st.markdown(f"""
                <div class="task-card assigned-task" style="opacity: 0.7;">
                    <h5>✅ {task.get('title', 'Untitled')}</h5>
                    <p><strong>Assigned by:</strong> {task.get('assigned_by', 'Unknown')}</p>
                    <p><strong>Completed:</strong> {completed_date}</p>
                    <p><strong>Category:</strong> {task.get('category', 'General')} | <strong>Priority:</strong> {task.get('priority', 'medium').title()}</p>
                    {f"<p><strong>Description:</strong> {task.get('description', 'No description')}</p>" if task.get('description') else ""}
                    {f"<p><strong>Feedback:</strong> {task.get('feedback', 'No feedback')}</p>" if task.get('feedback') else ""}
                </div>
                """, unsafe_allow_html=True)
            
            if st.button("🔽 Hide All Completed Assigned Tasks", key="hide_all_completed_assigned"):
                st.session_state["show_all_completed_assigned"] = False
                st.rerun()

def show_notes_page(data: dict):
    """Show notes management page."""
    st.markdown("""
    <div class="main-header">
        <h1>📝 Notes</h1>
        <p>Capture and organize your thoughts</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Note creation form
    with st.expander("➕ Create New Note", expanded=False):
        with st.form("create_note"):
            note_title = st.text_input("Note Title*", placeholder="Enter note title")
            note_content = st.text_area("Content*", placeholder="Write your note here...", height=150)
            note_category = st.selectbox("Category", data.get("categories", ["Work", "Personal", "Health"]))
            note_tags = st.text_input("Tags (comma-separated)", placeholder="important, meeting, idea")
            
            submit_note = st.form_submit_button("📝 Create Note", use_container_width=True)
            
            if submit_note:
                if not note_title.strip() or not note_content.strip():
                    st.error("Please enter both title and content!")
                else:
                    new_note = {
                        "id": str(uuid.uuid4()),
                        "title": note_title.strip(),
                        "content": note_content.strip(),
                        "category": note_category,
                        "tags": [tag.strip() for tag in note_tags.split(",") if tag.strip()],
                        "created_at": get_current_timestamp(),
                        "updated_at": get_current_timestamp()
                    }
                    
                    if "notes" not in data:
                        data["notes"] = []
                    data["notes"].append(new_note)
                    save_data(data)
                    refresh_session()  # Refresh session on note creation
                    st.success("Note created successfully!")
                    st.rerun()
    
    # Notes list
    notes = data.get("notes", [])
    
    if notes:
        st.markdown(f"### 📝 Your Notes ({len(notes)})")
        
        # Sort notes by creation date (newest first)
        notes = sorted(notes, key=lambda x: x.get("created_at", ""), reverse=True)
        
        for note in notes:
            with st.container():
                st.markdown(f"""
                <div class="floating-card">
                    <h4>📝 {note.get('title', 'Untitled')}</h4>
                    <p><strong>Category:</strong> {note.get('category', 'General')}</p>
                    <p><strong>Created:</strong> {note.get('created_at', 'Unknown')}</p>
                    {f"<p><strong>Tags:</strong> {', '.join(note.get('tags', []))}</p>" if note.get('tags') else ""}
                    <hr>
                    <p>{note.get('content', 'No content')}</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Note actions
                col1, col2 = st.columns(2)
                
                with col1:
                    if st.button("✏️ Edit", key=f"edit_note_{note['id']}"):
                        st.session_state[f"edit_note_{note['id']}"] = True
                
                with col2:
                    if st.button("🗑️ Delete", key=f"delete_note_{note['id']}"):
                        if st.session_state.get(f"confirm_delete_note_{note['id']}"):
                            # Remove note
                            data["notes"] = [n for n in data["notes"] if n["id"] != note["id"]]
                            save_data(data)
                            st.success("Note deleted!")
                            st.rerun()
                        else:
                            st.session_state[f"confirm_delete_note_{note['id']}"] = True
                            st.warning("Click delete again to confirm!")
                
                # Edit note form
                if st.session_state.get(f"edit_note_{note['id']}"):
                    with st.form(f"edit_note_form_{note['id']}"):
                        st.markdown("#### Edit Note")
                        
                        edit_title = st.text_input("Title", value=note.get("title", ""))
                        edit_content = st.text_area("Content", value=note.get("content", ""), height=150)
                        edit_category = st.selectbox("Category", data.get("categories", []), 
                                                   index=data.get("categories", []).index(note.get("category", "Work")) if note.get("category") in data.get("categories", []) else 0)
                        edit_tags = st.text_input("Tags", value=", ".join(note.get("tags", [])))
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            if st.form_submit_button("💾 Save Changes"):
                                # Update note
                                for n in data["notes"]:
                                    if n["id"] == note["id"]:
                                        n["title"] = edit_title
                                        n["content"] = edit_content
                                        n["category"] = edit_category
                                        n["tags"] = [tag.strip() for tag in edit_tags.split(",") if tag.strip()]
                                        n["updated_at"] = get_current_timestamp()
                                        break
                                save_data(data)
                                st.session_state[f"edit_note_{note['id']}"] = False
                                st.success("Note updated!")
                                st.rerun()
                        
                        with col2:
                            if st.form_submit_button("❌ Cancel"):
                                st.session_state[f"edit_note_{note['id']}"] = False
                                st.rerun()
                
                st.markdown("---")
    else:
        st.info("No notes yet. Create your first note!")

def show_contacts_page(data: dict):
    """Show contacts management page."""
    st.markdown("""
    <div class="main-header">
        <h1>👥 Contacts</h1>
        <p>Manage your professional and personal contacts</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Contact creation form
    with st.expander("➕ Add New Contact", expanded=False):
        with st.form("create_contact"):
            col1, col2 = st.columns(2)
            
            with col1:
                contact_name = st.text_input("Full Name*", placeholder="Enter full name")
                contact_email = st.text_input("Email", placeholder="contact@example.com")
                contact_phone = st.text_input("Phone", placeholder="+1234567890")
            
            with col2:
                contact_company = st.text_input("Company", placeholder="Company name")
                contact_position = st.text_input("Position", placeholder="Job title")
                contact_category = st.selectbox("Category", ["Work", "Personal", "Client", "Vendor", "Other"])
            
            contact_notes = st.text_area("Notes", placeholder="Additional information about this contact")
            
            submit_contact = st.form_submit_button("👥 Add Contact", use_container_width=True)
            
            if submit_contact:
                if not contact_name.strip():
                    st.error("Please enter a contact name!")
                else:
                    new_contact = {
                        "id": str(uuid.uuid4()),
                        "name": contact_name.strip(),
                        "email": contact_email.strip(),
                        "phone": contact_phone.strip(),
                        "company": contact_company.strip(),
                        "position": contact_position.strip(),
                        "category": contact_category,
                        "notes": contact_notes.strip(),
                        "created_at": get_current_timestamp(),
                        "updated_at": get_current_timestamp()
                    }
                    
                    if "contacts" not in data:
                        data["contacts"] = []
                    data["contacts"].append(new_contact)
                    save_data(data)
                    st.success("Contact added successfully!")
                    st.rerun()
    
    # Contacts list
    contacts = data.get("contacts", [])
    
    if contacts:
        st.markdown(f"### 👥 Your Contacts ({len(contacts)})")
        
        # Search functionality
        search_query = st.text_input("🔍 Search contacts", placeholder="Search by name, email, or company")
        
        if search_query:
            contacts = [c for c in contacts if 
                       search_query.lower() in c.get("name", "").lower() or
                       search_query.lower() in c.get("email", "").lower() or
                       search_query.lower() in c.get("company", "").lower()]
        
        # Sort contacts alphabetically
        contacts = sorted(contacts, key=lambda x: x.get("name", "").lower())
        
        for contact in contacts:
            with st.container():
                st.markdown(f"""
                <div class="floating-card">
                    <h4>👤 {contact.get('name', 'Unknown')}</h4>
                    <p><strong>Email:</strong> {contact.get('email', 'Not provided')}</p>
                    <p><strong>Phone:</strong> {contact.get('phone', 'Not provided')}</p>
                    <p><strong>Company:</strong> {contact.get('company', 'Not provided')}</p>
                    <p><strong>Position:</strong> {contact.get('position', 'Not provided')}</p>
                    <p><strong>Category:</strong> {contact.get('category', 'Other')}</p>
                    {f"<p><strong>Notes:</strong> {contact.get('notes', 'No notes')}</p>" if contact.get('notes') else ""}
                </div>
                """, unsafe_allow_html=True)
                
                # Contact actions
                col1, col2 = st.columns(2)
                
                with col1:
                    if st.button("✏️ Edit", key=f"edit_contact_{contact['id']}"):
                        st.session_state[f"edit_contact_{contact['id']}"] = True
                
                with col2:
                    if st.button("🗑️ Delete", key=f"delete_contact_{contact['id']}"):
                        if st.session_state.get(f"confirm_delete_contact_{contact['id']}"):
                            data["contacts"] = [c for c in data["contacts"] if c["id"] != contact["id"]]
                            save_data(data)
                            st.success("Contact deleted!")
                            st.rerun()
                        else:
                            st.session_state[f"confirm_delete_contact_{contact['id']}"] = True
                            st.warning("Click delete again to confirm!")
                
                # Edit contact form
                if st.session_state.get(f"edit_contact_{contact['id']}"):
                    with st.form(f"edit_contact_form_{contact['id']}"):
                        st.markdown("#### Edit Contact")
                        
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            edit_name = st.text_input("Name", value=contact.get("name", ""))
                            edit_email = st.text_input("Email", value=contact.get("email", ""))
                            edit_phone = st.text_input("Phone", value=contact.get("phone", ""))
                        
                        with col2:
                            edit_company = st.text_input("Company", value=contact.get("company", ""))
                            edit_position = st.text_input("Position", value=contact.get("position", ""))
                            edit_category = st.selectbox("Category", ["Work", "Personal", "Client", "Vendor", "Other"],
                                                       index=["Work", "Personal", "Client", "Vendor", "Other"].index(contact.get("category", "Other")))
                        
                        edit_notes = st.text_area("Notes", value=contact.get("notes", ""))
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            if st.form_submit_button("💾 Save Changes"):
                                for c in data["contacts"]:
                                    if c["id"] == contact["id"]:
                                        c["name"] = edit_name
                                        c["email"] = edit_email
                                        c["phone"] = edit_phone
                                        c["company"] = edit_company
                                        c["position"] = edit_position
                                        c["category"] = edit_category
                                        c["notes"] = edit_notes
                                        c["updated_at"] = get_current_timestamp()
                                        break
                                save_data(data)
                                st.session_state[f"edit_contact_{contact['id']}"] = False
                                st.success("Contact updated!")
                                st.rerun()
                        
                        with col2:
                            if st.form_submit_button("❌ Cancel"):
                                st.session_state[f"edit_contact_{contact['id']}"] = False
                                st.rerun()
                
                st.markdown("---")
    else:
        st.info("No contacts yet. Add your first contact!")

def show_goals_page(data: dict):
    """Show goals management page."""
    st.markdown("""
    <div class="main-header">
        <h1>🎯 Goals</h1>
        <p>Set and track your personal and professional goals</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Goal creation form
    with st.expander("➕ Create New Goal", expanded=False):
        with st.form("create_goal"):
            col1, col2 = st.columns(2)
            
            with col1:
                goal_title = st.text_input("Goal Title*", placeholder="Enter goal title")
                goal_category = st.selectbox("Category", ["Career", "Health", "Personal", "Financial", "Learning", "Other"])
                goal_priority = st.selectbox("Priority", ["low", "medium", "high"])
            
            with col2:
                goal_target_date = st.date_input("Target Date")
                goal_status = st.selectbox("Status", ["not_started", "in_progress", "completed", "on_hold"])
                goal_progress = st.slider("Progress (%)", 0, 100, 0)
            
            goal_description = st.text_area("Description", placeholder="Describe your goal and how you plan to achieve it")
            
            submit_goal = st.form_submit_button("🎯 Create Goal", use_container_width=True)
            
            if submit_goal:
                if not goal_title.strip():
                    st.error("Please enter a goal title!")
                else:
                    new_goal = {
                        "id": str(uuid.uuid4()),
                        "title": goal_title.strip(),
                        "description": goal_description.strip(),
                        "category": goal_category,
                        "priority": goal_priority,
                        "target_date": goal_target_date.strftime("%Y-%m-%d") if goal_target_date else None,
                        "status": goal_status,
                        "progress": goal_progress,
                        "created_at": get_current_timestamp(),
                        "updated_at": get_current_timestamp()
                    }
                    
                    if "goals" not in data:
                        data["goals"] = []
                    data["goals"].append(new_goal)
                    save_data(data)
                    st.success("Goal created successfully!")
                    st.rerun()
    
    # Goals list
    goals = data.get("goals", [])
    
    if goals:
        st.markdown(f"### 🎯 Your Goals ({len(goals)})")
        
        # Filter goals
        filter_status = st.selectbox("Filter by Status", ["all", "not_started", "in_progress", "completed", "on_hold"])
        
        if filter_status != "all":
            goals = [g for g in goals if g.get("status") == filter_status]
        
        # Sort goals by priority and target date
        goals = sorted(goals, key=lambda x: (
            {"high": 0, "medium": 1, "low": 2}.get(x.get("priority", "medium"), 1),
            x.get("target_date", "9999-12-31")
        ))
        
        for goal in goals:
            priority_class = f"{goal.get('priority', 'medium')}-priority"
            status_emoji = {
                "not_started": "⏳",
                "in_progress": "🔄",
                "completed": "✅",
                "on_hold": "⏸️"
            }.get(goal.get("status", "not_started"), "⏳")
            
            with st.container():
                st.markdown(f"""
                <div class="goal-card {priority_class}">
                    <h4>{status_emoji} {goal.get('title', 'Untitled')}</h4>
                    <p><strong>Category:</strong> {goal.get('category', 'Other')}</p>
                    <p><strong>Priority:</strong> {goal.get('priority', 'medium').title()}</p>
                    <p><strong>Status:</strong> {goal.get('status', 'not_started').replace('_', ' ').title()}</p>
                    <p><strong>Progress:</strong> {goal.get('progress', 0)}%</p>
                    {f"<p><strong>Target Date:</strong> {goal.get('target_date', 'No target date')}</p>" if goal.get('target_date') else ""}
                    {f"<p><strong>Description:</strong> {goal.get('description', 'No description')}</p>" if goal.get('description') else ""}
                </div>
                """, unsafe_allow_html=True)
                
                # Progress bar
                st.progress(goal.get("progress", 0) / 100)
                
                # Goal actions
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    if st.button("📈 Update Progress", key=f"update_progress_{goal['id']}"):
                        st.session_state[f"update_progress_{goal['id']}"] = True
                
                with col2:
                    if st.button("✏️ Edit", key=f"edit_goal_{goal['id']}"):
                        st.session_state[f"edit_goal_{goal['id']}"] = True
                
                with col3:
                    if st.button("🗑️ Delete", key=f"delete_goal_{goal['id']}"):
                        if st.session_state.get(f"confirm_delete_goal_{goal['id']}"):
                            data["goals"] = [g for g in data["goals"] if g["id"] != goal["id"]]
                            save_data(data)
                            st.success("Goal deleted!")
                            st.rerun()
                        else:
                            st.session_state[f"confirm_delete_goal_{goal['id']}"] = True
                            st.warning("Click delete again to confirm!")
                
                # Update progress form
                if st.session_state.get(f"update_progress_{goal['id']}"):
                    with st.form(f"update_progress_form_{goal['id']}"):
                        st.markdown("#### Update Progress")
                        
                        new_progress = st.slider("Progress (%)", 0, 100, goal.get("progress", 0))
                        new_status = st.selectbox("Status", ["not_started", "in_progress", "completed", "on_hold"],
                                                index=["not_started", "in_progress", "completed", "on_hold"].index(goal.get("status", "not_started")))
                        progress_note = st.text_area("Progress Note", placeholder="What did you accomplish?")
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            if st.form_submit_button("💾 Save Progress"):
                                for g in data["goals"]:
                                    if g["id"] == goal["id"]:
                                        g["progress"] = new_progress
                                        g["status"] = new_status
                                        g["updated_at"] = get_current_timestamp()
                                        if progress_note:
                                            if "progress_notes" not in g:
                                                g["progress_notes"] = []
                                            g["progress_notes"].append({
                                                "note": progress_note,
                                                "timestamp": get_current_timestamp(),
                                                "progress": new_progress
                                            })
                                        break
                                save_data(data)
                                st.session_state[f"update_progress_{goal['id']}"] = False
                                st.success("Progress updated!")
                                st.rerun()
                        
                        with col2:
                            if st.form_submit_button("❌ Cancel"):
                                st.session_state[f"update_progress_{goal['id']}"] = False
                                st.rerun()
                
                # Edit goal form
                if st.session_state.get(f"edit_goal_{goal['id']}"):
                    with st.form(f"edit_goal_form_{goal['id']}"):
                        st.markdown("#### Edit Goal")
                        
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            edit_title = st.text_input("Title", value=goal.get("title", ""))
                            edit_category = st.selectbox("Category", ["Career", "Health", "Personal", "Financial", "Learning", "Other"],
                                                       index=["Career", "Health", "Personal", "Financial", "Learning", "Other"].index(goal.get("category", "Other")))
                            edit_priority = st.selectbox("Priority", ["low", "medium", "high"],
                                                       index=["low", "medium", "high"].index(goal.get("priority", "medium")))
                        
                        with col2:
                            edit_target_date = st.date_input("Target Date", 
                                                           value=datetime.datetime.strptime(goal.get("target_date", "2024-12-31"), "%Y-%m-%d").date() if goal.get("target_date") else None)
                            edit_status = st.selectbox("Status", ["not_started", "in_progress", "completed", "on_hold"],
                                                     index=["not_started", "in_progress", "completed", "on_hold"].index(goal.get("status", "not_started")))
                            edit_progress = st.slider("Progress (%)", 0, 100, goal.get("progress", 0))
                        
                        edit_description = st.text_area("Description", value=goal.get("description", ""))
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            if st.form_submit_button("💾 Save Changes"):
                                for g in data["goals"]:
                                    if g["id"] == goal["id"]:
                                        g["title"] = edit_title
                                        g["category"] = edit_category
                                        g["priority"] = edit_priority
                                        g["target_date"] = edit_target_date.strftime("%Y-%m-%d") if edit_target_date else None
                                        g["status"] = edit_status
                                        g["progress"] = edit_progress
                                        g["description"] = edit_description
                                        g["updated_at"] = get_current_timestamp()
                                        break
                                save_data(data)
                                st.session_state[f"edit_goal_{goal['id']}"] = False
                                st.success("Goal updated!")
                                st.rerun()
                        
                        with col2:
                            if st.form_submit_button("❌ Cancel"):
                                st.session_state[f"edit_goal_{goal['id']}"] = False
                                st.rerun()
                
                st.markdown("---")
    else:
        st.info("No goals yet. Create your first goal!")

def show_team_page(company_info: dict):
    """Show team members page."""
    st.markdown("""
    <div class="main-header">
        <h1>👥 Team Members</h1>
        <p>View and manage your team</p>
    </div>
    """, unsafe_allow_html=True)
    
    if not company_info:
        st.error("You need to be part of a company to view team members.")
        return
    
    company_code = company_info.get("code")
    if not company_code:
        st.error("Invalid company information.")
        return
    
    # Get all team members
    team_members = get_team_members(company_code)
    
    if team_members:
        st.markdown(f"### 👥 Team Members ({len(team_members)})")
        
        # Search functionality
        search_query = st.text_input("🔍 Search team members", placeholder="Search by name or role")
        
        if search_query:
            team_members = [m for m in team_members if 
                          search_query.lower() in m.get("full_name", "").lower() or
                          search_query.lower() in m.get("role", "").lower()]
        
        # Display team members
        for member in team_members:
            with st.container():
                st.markdown(f"""
                <div class="team-member-card">
                    <h4>👤 {member.get('full_name', 'Unknown')}</h4>
                    <p><strong>Username:</strong> {member.get('username', 'Unknown')}</p>
                    <p><strong>Role:</strong> {member.get('role', 'employee').title()}</p>
                    <p><strong>Department:</strong> {member.get('department', 'Not specified')}</p>
                    <p><strong>Email:</strong> {member.get('email', 'Not provided')}</p>
                    <p><strong>Joined:</strong> {member.get('created_at', 'Unknown')}</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Member actions (for managers and admins)
                current_user = st.session_state.get("username")
                if current_user:
                    current_user_info = get_user_info(current_user)
                else:
                    current_user_info = None
                
                if current_user_info and current_user_info.get("role") in ["admin", "manager"]:
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        if st.button("📋 Assign Task", key=f"assign_to_{member['username']}"):
                            st.session_state["assign_to_user"] = member["username"]
                            st.session_state["current_page"] = "assign_tasks"
                            st.rerun()
                    
                    with col2:
                        if member.get("role") != "admin":  # Can't remove admins
                            if st.button("🚫 Remove from Team", key=f"remove_{member['username']}"):
                                if st.session_state.get(f"confirm_remove_{member['username']}"):
                                    # Remove user from company
                                    remove_user_from_company(member["username"])
                                    st.success(f"Removed {member.get('full_name', 'User')} from team!")
                                    st.rerun()
                                else:
                                    st.session_state[f"confirm_remove_{member['username']}"] = True
                                    st.warning("Click remove again to confirm!")
                
                st.markdown("---")
    else:
        st.info("No team members found.")

def show_assign_tasks_page(username: str, company_info: dict):
    """Show assign tasks page."""
    st.markdown("""
    <div class="main-header">
        <h1>📋 Assign Tasks</h1>
        <p>Assign tasks to team members</p>
    </div>
    """, unsafe_allow_html=True)
    
    if not company_info:
        st.error("You need to be part of a company to assign tasks.")
        return
    
    # Check if user can assign tasks
    if not can_assign_tasks(username):
        st.error("You don't have permission to assign tasks.")
        return
    
    company_code = company_info.get("code")
    if not company_code:
        st.error("Invalid company information.")
        return
    
    team_members = get_team_members(company_code)
    
    # Filter out the current user
    team_members = [m for m in team_members if m["username"] != username]
    
    # Filter to only juniors (those the user can assign to)
    team_members = [m for m in team_members if can_assign_task_to_user(username, m["username"])]
    
    if not team_members:
        st.info("No juniors available to assign tasks to.")
        return
    
    # Task assignment form
    with st.form("assign_task"):
        st.markdown("### 📝 Create and Assign Task")
        
        col1, col2 = st.columns(2)
        
        with col1:
            task_title = st.text_input("Task Title*", placeholder="Enter task title")
            task_priority = st.selectbox("Priority", ["low", "medium", "high"])
            task_due_date = st.date_input("Due Date (Optional)")
        
        with col2:
            # Pre-select user if coming from team page
            default_user = st.session_state.get("assign_to_user", "")
            if default_user:
                member_names = [f"{m['full_name']} ({m['username']})" for m in team_members]
                default_index = next((i for i, m in enumerate(team_members) if m["username"] == default_user), 0)
            else:
                member_names = [f"{m['full_name']} ({m['username']})" for m in team_members]
                default_index = 0
            
            selected_member = st.selectbox("Assign to", member_names, index=default_index)
            task_category = st.selectbox("Category", ["Work", "Project", "Meeting", "Review", "Other"])
            task_status = st.selectbox("Status", ["assigned", "urgent", "important"])
        
        task_description = st.text_area("Task Description", placeholder="Describe what needs to be done...")
        
        submit_assignment = st.form_submit_button("🎯 Assign Task", use_container_width=True)
        
        if submit_assignment:
            if not task_title.strip():
                st.error("Please enter a task title!")
            elif not selected_member:
                st.error("Please select a team member!")
            else:
                # Validate content
                title_valid, title_error = validate_content(task_title.strip())
                desc_valid, desc_error = validate_content(task_description.strip())
                
                if not title_valid:
                    st.error(f"Task title: {title_error}")
                elif not desc_valid:
                    st.error(f"Task description: {desc_error}")
                else:
                    # Get selected member username
                    selected_username = selected_member.split("(")[1].split(")")[0]
                    # Double check permission
                    if not can_assign_task_to_user(username, selected_username):
                        st.error("You can only assign tasks to juniors.")
                        return
                    # Create assigned task
                    assigned_task = {
                        "id": str(uuid.uuid4()),
                        "title": task_title.strip(),
                        "description": task_description.strip(),
                        "category": task_category,
                        "priority": task_priority,
                        "due_date": task_due_date.strftime("%Y-%m-%d") if task_due_date else None,
                        "assigned_by": username,
                        "assigned_to": selected_username,
                        "status": task_status,
                        "completed": False,
                        "created_at": get_current_timestamp(),
                        "updated_at": get_current_timestamp()
                    }
                    # Add to assigned user's data
                    success, message = assign_task_to_user(username, selected_username, assigned_task)
                    # Send enhanced task notification
                    send_task_notification(
                        selected_username,
                        task_title,
                        "assigned",
                        username,
                        "high"
                    )
                    st.success(f"Task assigned to {selected_member.split('(')[0].strip()} successfully!")
                    # Clear the pre-selected user
                    if "assign_to_user" in st.session_state:
                        del st.session_state["assign_to_user"]
                    st.rerun()
    # Show assigned tasks history
    st.markdown("### 📋 Recently Assigned Tasks")
    # Get all assigned tasks by this user
    assigned_tasks_history = get_assigned_tasks_by_user(username)
    if assigned_tasks_history:
        for task in assigned_tasks_history[-10:]:  # Show last 10
            status_emoji = "✅" if task.get("completed", False) else "⏳"
            st.markdown(f"""
            <div class="task-card assigned-task">
                <h4>{status_emoji} {task.get('title', 'Untitled')}</h4>
                <p><strong>Assigned to:</strong> {task.get('assigned_to', 'Unknown')}</p>
                <p><strong>Priority:</strong> {task.get('priority', 'medium').title()}</p>
                <p><strong>Status:</strong> {task.get('status', 'assigned').title()}</p>
                <p><strong>Assigned on:</strong> {task.get('created_at', 'Unknown')}</p>
                {f"<p><strong>Due:</strong> {task.get('due_date', 'No due date')}</p>" if task.get('due_date') else ""}
                {f"<p><strong>Feedback:</strong> {task.get('feedback', 'No feedback')}</p>" if task.get('feedback') else ""}
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No tasks assigned yet.")

def show_analytics_page(company_info: dict):
    """Show team analytics page."""
    st.markdown("""
    <div class="main-header">
        <h1>📊 Team Analytics</h1>
        <p>Insights and performance metrics</p>
    </div>
    """, unsafe_allow_html=True)
    
    if not company_info:
        st.error("You need to be part of a company to view analytics.")
        return
    
    company_code = company_info.get("code")
    if not company_code:
        st.error("Invalid company information.")
        return
    
    # Get team statistics
    team_stats = calculate_team_stats(company_code)
    
    # Overview metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <h3>👥 Team Size</h3>
            <h2>{team_stats['total_employees']}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <h3>📋 Total Tasks</h3>
            <h2>{team_stats['total_tasks']}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <h3>✅ Completed</h3>
            <h2>{team_stats['completed_tasks']}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <h3>📊 Completion Rate</h3>
            <h2>{team_stats['completion_rate']:.1f}%</h2>
        </div>
        """, unsafe_allow_html=True)
    
    # Detailed analytics
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📈 Task Distribution by Priority")
        
        # Get task priority distribution
        priority_data = get_task_priority_distribution(company_code)
        
        if priority_data:
            import plotly.express as px
            import pandas as pd
            
            df = pd.DataFrame(priority_data)
            fig = px.pie(df, values='count', names='priority', title='Task Priority Distribution')
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No task data available for analysis.")
    
    with col2:
        st.markdown("### 📊 Team Performance")
        
        # Get individual performance data
        performance_data = get_team_performance_data(company_code)
        
        if performance_data:
            import pandas as pd
            
            df = pd.DataFrame(performance_data)
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No performance data available.")
    
    # Task completion trends
    st.markdown("### 📈 Task Completion Trends")
    
    completion_trends = get_task_completion_trends(company_code)
    
    if completion_trends and len(completion_trends) > 0:
        import plotly.express as px
        import pandas as pd
        
        df = pd.DataFrame(completion_trends)
        if not df.empty:
            fig = px.line(df, x='date', y='completed_tasks', title='Daily Task Completion Trends')
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No completion trend data available.")
    else:
        st.info("No completion trend data available.")
    
    # Department wise analytics
    st.markdown("### 🏢 Department Analytics")
    
    dept_analytics = get_department_analytics(company_code)
    
    if dept_analytics and dept_analytics.get('department_distribution') and dept_analytics.get('department_performance'):
        col1, col2 = st.columns(2)
        
        with col1:
            # Department distribution
            import plotly.express as px
            import pandas as pd
            
            dept_dist = dept_analytics['department_distribution']
            if dept_dist:  # Check if not empty
                df = pd.DataFrame(dept_dist)
                fig = px.bar(df, x='department', y='employee_count', title='Employees by Department')
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No department distribution data available.")
        
        with col2:
            # Department performance
            dept_perf = dept_analytics['department_performance']
            if dept_perf:  # Check if not empty
                df_perf = pd.DataFrame(dept_perf)
                fig = px.bar(df_perf, x='department', y='completion_rate', title='Completion Rate by Department')
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No department performance data available.")
    else:
        st.info("No department analytics available.")
    
    # Recent activity
    st.markdown("### 📅 Recent Team Activity")
    
    recent_activities = get_recent_team_activities(company_code)
    
    if recent_activities:
        for activity in recent_activities[:10]:  # Show last 10 activities
            activity_type = activity.get('type', 'activity')
            activity_icon = {
                'task_completed': '✅',
                'task_assigned': '📋',
                'task_created': '➕',
                'user_joined': '👋',
                'user_left': '👋',
                'goal_achieved': '🎯',
                'deadline_missed': '⚠️'
            }.get(activity_type, '📝')
            
            st.markdown(f"""
            <div class="activity-item">
                <span class="activity-icon">{activity_icon}</span>
                <div class="activity-content">
                    <p><strong>{activity.get('user', 'Unknown')}</strong> {activity.get('action', 'performed an action')}</p>
                    <small>{activity.get('timestamp', 'Unknown time')}</small>
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No recent activities found.")
    
    # Export analytics
    st.markdown("### 📊 Export Analytics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📊 Export Team Report", use_container_width=True):
            # Generate and download team report
            report_data = generate_team_report(company_code)
            if report_data:
                st.download_button(
                    label="📥 Download Report",
                    data=report_data,
                    file_name=f"team_report_{company_code}_{get_current_timestamp()}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
            else:
                st.error("Failed to generate report.")
    
    with col2:
        if st.button("📈 Export Analytics Data", use_container_width=True):
            # Generate and download analytics data
            analytics_data = export_analytics_data(company_code)
            if analytics_data:
                st.download_button(
                    label="📥 Download Analytics",
                    data=analytics_data,
                    file_name=f"analytics_{company_code}_{get_current_timestamp()}.json",
                    mime="application/json",
                    use_container_width=True
                )
            else:
                st.error("Failed to export analytics data.")
    
    # Refresh button
    if st.button("🔄 Refresh Analytics", use_container_width=True):
        st.rerun()
        
# -------------------------------------------------------------
# Missing Functions Implementation
# -------------------------------------------------------------

def get_team_members(company_code: str) -> List[Dict[str, Any]]:
    """Get all team members of a company."""
    companies_data = load_companies_data()
    company_data = companies_data.get(company_code, {})
    return company_data.get("employees", [])

def remove_user_from_company(username: str):
    """Remove a user from a company."""
    auth_data = load_auth_data()
    companies_data = load_companies_data()
    
    if username in auth_data:
        company_code = auth_data[username].get("company_code")
        if company_code and company_code in companies_data:
            # Remove from company employees list
            companies_data[company_code]["employees"] = [
                emp for emp in companies_data[company_code]["employees"] 
                if emp.get("username") != username
            ]
            save_companies_data(companies_data)
            
            # Remove company code from user
            auth_data[username]["company_code"] = None
            save_auth_data(auth_data)

def get_assigned_tasks_by_user(username: str) -> List[Dict[str, Any]]:
    """Get all tasks assigned by a specific user."""
    companies_data = load_companies_data()
    all_assigned_tasks = []
    
    for company_code, company_data in companies_data.items():
        employees = company_data.get("employees", [])
        for employee in employees:
            emp_username = employee.get("username")
            if emp_username:
                user_file = Path(f"user_{emp_username}.json")
                if user_file.exists():
                    with user_file.open("r", encoding="utf-8") as f:
                        user_data = json.load(f)
                        assigned_tasks = user_data.get("assigned_tasks", [])
                        # Filter tasks assigned by the specified user
                        user_assigned_tasks = [task for task in assigned_tasks if task.get("assigned_by") == username]
                        all_assigned_tasks.extend(user_assigned_tasks)
    
    return all_assigned_tasks

def get_task_priority_distribution(company_code: str) -> List[Dict[str, Any]]:
    """Get task priority distribution for a company."""
    employees = get_company_employees(company_code)
    priority_counts = {"low": 0, "medium": 0, "high": 0}
    
    for employee in employees:
        username = employee.get("username")
        user_file = Path(f"user_{username}.json")
        
        if user_file.exists():
            with user_file.open("r", encoding="utf-8") as f:
                user_data = json.load(f)
                assigned_tasks = user_data.get("assigned_tasks", [])
                
                for task in assigned_tasks:
                    priority = task.get("priority", "medium")
                    priority_counts[priority] = priority_counts.get(priority, 0) + 1
    
    return [{"priority": k.title(), "count": v} for k, v in priority_counts.items() if v > 0]

def get_team_performance_data(company_code: str) -> List[Dict[str, Any]]:
    """Get individual team member performance data."""
    employees = get_company_employees(company_code)
    performance_data = []
    
    for employee in employees:
        username = employee.get("username")
        user_file = Path(f"user_{username}.json")
        
        if user_file.exists():
            with user_file.open("r", encoding="utf-8") as f:
                user_data = json.load(f)
                assigned_tasks = user_data.get("assigned_tasks", [])
                
                total_tasks = len(assigned_tasks)
                completed_tasks = len([t for t in assigned_tasks if t.get("completed", False)])
                completion_rate = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
                
                performance_data.append({
                    "Employee": employee.get("full_name", username),
                    "Total Tasks": total_tasks,
                    "Completed": completed_tasks,
                    "Completion Rate (%)": round(completion_rate, 1)
                })
    
    return performance_data

def get_task_completion_trends(company_code: str) -> List[Dict[str, Any]]:
    """Get task completion trends over time."""
    employees = get_company_employees(company_code)
    completion_dates = {}
    
    for employee in employees:
        username = employee.get("username")
        user_file = Path(f"user_{username}.json")
        
        if user_file.exists():
            with user_file.open("r", encoding="utf-8") as f:
                user_data = json.load(f)
                assigned_tasks = user_data.get("assigned_tasks", [])
                
                for task in assigned_tasks:
                    if task.get("completed", False) and task.get("completed_at"):
                        date = task.get("completed_at").split()[0]  # Get just the date part
                        completion_dates[date] = completion_dates.get(date, 0) + 1
    
    # Convert to list and sort by date
    trends = [{"date": date, "completed_tasks": count} for date, count in completion_dates.items()]
    trends.sort(key=lambda x: x["date"])
    
    return trends

def get_department_analytics(company_code: str) -> Dict[str, Any]:
    """Get department-wise analytics."""
    employees = get_company_employees(company_code)
    dept_data = {}
    
    for employee in employees:
        dept = employee.get("department", "General")
        if dept not in dept_data:
            dept_data[dept] = {"employees": [], "tasks": []}
        dept_data[dept]["employees"].append(employee)
    
    # Calculate department statistics
    dept_distribution = []
    dept_performance = []
    
    for dept, data in dept_data.items():
        employee_count = len(data["employees"])
        dept_distribution.append({"department": dept, "employee_count": employee_count})
        
        # Calculate completion rate for department
        total_tasks = 0
        completed_tasks = 0
        
        for emp in data["employees"]:
            username = emp.get("username")
            user_file = Path(f"user_{username}.json")
            
            if user_file.exists():
                with user_file.open("r", encoding="utf-8") as f:
                    user_data = json.load(f)
                    assigned_tasks = user_data.get("assigned_tasks", [])
                    total_tasks += len(assigned_tasks)
                    completed_tasks += len([t for t in assigned_tasks if t.get("completed", False)])
        
        completion_rate = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
        dept_performance.append({"department": dept, "completion_rate": round(completion_rate, 1)})
    
    return {
        "department_distribution": dept_distribution,
        "department_performance": dept_performance
    }

def get_recent_team_activities(company_code: str) -> List[Dict[str, Any]]:
    """Get recent team activities."""
    employees = get_company_employees(company_code)
    activities = []
    
    for employee in employees:
        username = employee.get("username")
        user_file = Path(f"user_{username}.json")
        
        if user_file.exists():
            with user_file.open("r", encoding="utf-8") as f:
                user_data = json.load(f)
                
                # Get recent task completions
                assigned_tasks = user_data.get("assigned_tasks", [])
                for task in assigned_tasks:
                    if task.get("completed", False):
                        activities.append({
                            "type": "task_completed",
                            "user": employee.get("full_name", username),
                            "action": f"completed task '{task.get('title', 'Untitled')}'",
                            "timestamp": task.get("completed_at", "Unknown")
                        })
                
                # Get recent task assignments
                for task in assigned_tasks:
                    activities.append({
                        "type": "task_assigned",
                        "user": employee.get("full_name", username),
                        "action": f"was assigned task '{task.get('title', 'Untitled')}'",
                        "timestamp": task.get("assigned_at", "Unknown")
                    })
    
    # Sort by timestamp (most recent first)
    activities.sort(key=lambda x: x.get("timestamp", ""), reverse=True)
    return activities[:50]  # Return last 50 activities

def generate_team_report(company_code: str) -> Optional[str]:
    """Generate a CSV team report."""
    try:
        team_stats = calculate_team_stats(company_code)
        performance_data = get_team_performance_data(company_code)
        
        # Create CSV content
        csv_lines = ["Employee,Total Tasks,Completed,Completion Rate (%)"]
        
        for data in performance_data:
            csv_lines.append(f"{data['Employee']},{data['Total Tasks']},{data['Completed']},{data['Completion Rate (%)']}")
        
        csv_lines.append("")
        csv_lines.append("Team Summary")
        csv_lines.append(f"Total Employees,{team_stats['total_employees']}")
        csv_lines.append(f"Total Tasks,{team_stats['total_tasks']}")
        csv_lines.append(f"Completed Tasks,{team_stats['completed_tasks']}")
        csv_lines.append(f"Overall Completion Rate,{team_stats['completion_rate']:.1f}%")
        
        return "\n".join(csv_lines)
    except Exception as e:
        st.error(f"Error generating report: {str(e)}")
        return None

def export_analytics_data(company_code: str) -> Optional[str]:
    """Export analytics data as JSON."""
    try:
        analytics_data = {
            "team_stats": calculate_team_stats(company_code),
            "performance_data": get_team_performance_data(company_code),
            "priority_distribution": get_task_priority_distribution(company_code),
            "completion_trends": get_task_completion_trends(company_code),
            "department_analytics": get_department_analytics(company_code),
            "recent_activities": get_recent_team_activities(company_code),
            "exported_at": get_current_timestamp()
        }
        
        return json.dumps(analytics_data, indent=2, ensure_ascii=False)
    except Exception as e:
        st.error(f"Error exporting analytics: {str(e)}")
        return None

def show_company_settings_page(username: str, company_info: dict):
    """Show company settings page."""
    st.markdown("""
    <div class="main-header">
        <h1>⚙️ Company Settings</h1>
        <p>Manage your company configuration</p>
    </div>
    """, unsafe_allow_html=True)
    
    if not company_info:
        st.error("You need to be part of a company to access settings.")
        return
    
    company_code = company_info.get("code")
    if not company_code:
        st.error("Invalid company information.")
        return
    
    # Check if user is admin
    user_info = get_user_info(username)
    if company_info.get("admin_username") != username and user_info.get("role") != "admin":
        st.error("Only company admins can access company settings.")
        return
    
    companies_data = load_companies_data()
    company_data = companies_data.get(company_code, {})
    
    st.markdown("### 🏢 Company Information")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.info(f"**Company Name:** {company_data.get('name', 'Unknown')}")
        st.info(f"**Company Code:** {company_code}")
        st.info(f"**Admin:** {company_data.get('admin_username', 'Unknown')}")
    
    with col2:
        st.info(f"**Created:** {company_data.get('created_at', 'Unknown')}")
        st.info(f"**Total Employees:** {len(company_data.get('employees', []))}")
        st.info(f"**Description:** {company_data.get('description', 'No description')}")
    
    # Company settings form
    st.markdown("### ⚙️ Company Configuration")
    
    with st.form("company_settings"):
        allow_self_registration = st.checkbox("Allow Self Registration", 
                                            value=company_data.get("company_settings", {}).get("allow_self_registration", True))
        require_approval = st.checkbox("Require Approval for New Members", 
                                     value=company_data.get("company_settings", {}).get("require_approval", False))
        default_role = st.selectbox("Default Employee Role", 
                                  ["employee", "manager"], 
                                  index=0 if company_data.get("company_settings", {}).get("default_employee_role", "employee") == "employee" else 1)
        
        if st.form_submit_button("💾 Save Settings"):
            if "company_settings" not in company_data:
                company_data["company_settings"] = {}
            
            company_data["company_settings"]["allow_self_registration"] = allow_self_registration
            company_data["company_settings"]["require_approval"] = require_approval
            company_data["company_settings"]["default_employee_role"] = default_role
            
            companies_data[company_code] = company_data
            save_companies_data(companies_data)
            st.success("Company settings updated successfully!")
    
    # Department management
    st.markdown("### 🏢 Department Management")
    
    departments = company_data.get("departments", ["General", "HR", "IT", "Sales", "Marketing", "Finance"])
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Current Departments")
        for dept in departments:
            st.write(f"• {dept}")
    
    with col2:
        with st.form("add_department"):
            new_dept = st.text_input("New Department Name")
            if st.form_submit_button("➕ Add Department"):
                if new_dept.strip() and new_dept not in departments:
                    departments.append(new_dept.strip())
                    company_data["departments"] = departments
                    companies_data[company_code] = company_data
                    save_companies_data(companies_data)
                    st.success(f"Department '{new_dept}' added!")
                    st.rerun()
                elif new_dept in departments:
                    st.error("Department already exists!")
    
    # Employee management
    st.markdown("### 👥 Employee Management")
    
    employees = company_data.get("employees", [])
    
    if employees:
        for employee in employees:
            with st.container():
                col1, col2, col3 = st.columns([2, 1, 1])
                
                with col1:
                    st.write(f"**{employee.get('full_name', 'Unknown')}** ({employee.get('username', 'Unknown')})")
                    st.write(f"Role: {employee.get('role', 'employee').title()}")
                
                with col2:
                    if employee.get("role") != "admin":
                        if st.button("🚫 Remove", key=f"remove_emp_{employee['username']}"):
                            if st.session_state.get(f"confirm_remove_emp_{employee['username']}"):
                                remove_user_from_company(employee["username"])
                                st.success(f"Removed {employee.get('full_name', 'User')} from company!")
                                st.rerun()
                            else:
                                st.session_state[f"confirm_remove_emp_{employee['username']}"] = True
                                st.warning("Click remove again to confirm!")
                
                with col3:
                    if employee.get("role") != "admin":
                        if st.button("👑 Make Admin", key=f"make_admin_{employee['username']}"):
                            # Update user role to admin
                            auth_data = load_auth_data()
                            if employee["username"] in auth_data:
                                auth_data[employee["username"]]["role"] = "admin"
                                save_auth_data(auth_data)
                                
                                # Update in company data
                                for emp in company_data["employees"]:
                                    if emp["username"] == employee["username"]:
                                        emp["role"] = "admin"
                                        break
                                companies_data[company_code] = company_data
                                save_companies_data(companies_data)
                                
                                st.success(f"Made {employee.get('full_name', 'User')} an admin!")
                                st.rerun()
                
                st.markdown("---")
    else:
        st.info("No employees found.")

def show_create_company_page(username: str):
    """Show create company page."""
    st.markdown("""
    <div class="main-header">
        <h1>🏢 Create Company</h1>
        <p>Start your own company and invite team members</p>
    </div>
    """, unsafe_allow_html=True)
    
    with st.form("create_company_form"):
        company_name = st.text_input("Company Name*", placeholder="Enter your company name")
        company_description = st.text_area("Description", placeholder="Describe your company...")
        
        col1, col2 = st.columns(2)
        
        with col1:
            allow_self_registration = st.checkbox("Allow Self Registration", value=True)
            require_approval = st.checkbox("Require Approval for New Members", value=False)
        
        with col2:
            default_role = st.selectbox("Default Employee Role", ["employee", "manager"])
            departments = st.multiselect("Departments", 
                                       ["General", "HR", "IT", "Sales", "Marketing", "Finance", "Operations", "Support"],
                                       default=["General", "HR", "IT", "Sales", "Marketing", "Finance"])
        
        submit_company = st.form_submit_button("🏢 Create Company", use_container_width=True)
        
        if submit_company:
            if not company_name.strip():
                st.error("Please enter a company name!")
            else:
                success, result = create_company(company_name.strip(), company_description.strip(), username)
                
                if success:
                    company_code = result
                    
                    # Update company settings
                    companies_data = load_companies_data()
                    if company_code in companies_data:
                        companies_data[company_code]["company_settings"] = {
                            "allow_self_registration": allow_self_registration,
                            "require_approval": require_approval,
                            "default_employee_role": default_role
                        }
                        companies_data[company_code]["departments"] = departments
                        save_companies_data(companies_data)
                    
                    # Update user's company code
                    auth_data = load_auth_data()
                    if username in auth_data:
                        auth_data[username]["company_code"] = company_code
                        auth_data[username]["role"] = "admin"
                        save_auth_data(auth_data)
                    
                    st.success(f"Company '{company_name}' created successfully!")
                    st.info(f"Your company code is: **{company_code}**")
                    st.info("Share this code with your team members so they can join your company!")
                    
                    # Show next steps
                    st.markdown("### 🎉 Next Steps")
                    st.markdown("""
                    1. **Share the company code** with your team members
                    2. **Invite employees** to register with your company code
                    3. **Start assigning tasks** to your team
                    4. **Monitor team performance** through analytics
                    """)
                    
                    st.rerun()
                else:
                    st.error(f"Failed to create company: {result}")

def show_notifications_page(username: str):
    """Show notifications page."""
    st.markdown("""
    <div class="main-header">
        <h1>🔔 Notifications</h1>
        <p>Stay updated with your latest notifications</p>
    </div>
    """, unsafe_allow_html=True)
    
    notifications = get_user_notifications(username)
    
    if notifications:
        # Filter options
        col1, col2 = st.columns(2)
        
        with col1:
            filter_type = st.selectbox("Filter by Type", ["all", "info", "success", "warning", "error", "task", "file", "poll", "calendar", "chat", "project", "performance"])
        
        with col2:
            filter_read = st.selectbox("Filter by Status", ["all", "unread", "read"])
        
        # Apply filters
        filtered_notifications = notifications
        
        if filter_type != "all":
            filtered_notifications = [n for n in filtered_notifications if n.get("type") == filter_type]
        
        if filter_read != "all":
            if filter_read == "unread":
                filtered_notifications = [n for n in filtered_notifications if not n.get("read", False)]
            else:
                filtered_notifications = [n for n in filtered_notifications if n.get("read", False)]
        
        # Display notifications
        st.markdown(f"### 📋 Notifications ({len(filtered_notifications)})")
        
        for notification in filtered_notifications:
            notification_type = notification.get("type", "info")
            is_read = notification.get("read", False)
            
            # Determine notification style with enhanced icons and colors
            icon = get_notification_icon(notification_type)
            color = get_notification_color(notification_type)
            
            if notification_type == "success":
                style_class = "success-message"
            elif notification_type == "warning":
                style_class = "warning-message"
            elif notification_type == "error":
                style_class = "error-message"
            else:
                style_class = "notification-card"
            
            # Add read/unread indicator
            if not is_read:
                style_class += " unread"
                icon += " 🔴"
            
            st.markdown(f"""
            <div class="{style_class}" style="border-left: 4px solid {color};">
                <h4>{icon} {notification.get('title', 'Notification')}</h4>
                <p>{notification.get('message', 'No message')}</p>
                <small>
                    <strong>From:</strong> {notification.get('from_username', 'System')} | 
                    <strong>Time:</strong> {notification.get('created_at', 'Unknown')}
                    {f" | <strong>Priority:</strong> {notification.get('priority', 'normal').title()}" if notification.get('priority') else ""}
                </small>
            </div>
            """, unsafe_allow_html=True)
            
            # Notification actions
            col1, col2 = st.columns(2)
            
            with col1:
                if not is_read:
                    if st.button("✅ Mark as Read", key=f"read_{notification['id']}"):
                        mark_notification_read(username, notification["id"])
                        st.success("Marked as read!")
                        st.rerun()
            
            with col2:
                if st.button("🗑️ Delete", key=f"delete_notif_{notification['id']}"):
                    # Remove notification
                    notifications_data = load_notifications_data()
                    if username in notifications_data:
                        notifications_data[username] = [n for n in notifications_data[username] if n.get("id") != notification["id"]]
                        save_notifications_data(notifications_data)
                        st.success("Notification deleted!")
                        st.rerun()
            
            st.markdown("---")
        
        # Bulk actions
        st.markdown("### 🔧 Bulk Actions")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("✅ Mark All as Read", use_container_width=True):
                notifications_data = load_notifications_data()
                if username in notifications_data:
                    for notification in notifications_data[username]:
                        notification["read"] = True
                    save_notifications_data(notifications_data)
                    st.success("All notifications marked as read!")
                    st.rerun()
        
        with col2:
            if st.button("🗑️ Delete All Read", use_container_width=True):
                notifications_data = load_notifications_data()
                if username in notifications_data:
                    notifications_data[username] = [n for n in notifications_data[username] if not n.get("read", False)]
                    save_notifications_data(notifications_data)
                    st.success("All read notifications deleted!")
                    st.rerun()
        
        with col3:
            if st.button("🗑️ Delete All", use_container_width=True):
                if st.session_state.get("confirm_delete_all_notifications"):
                    notifications_data = load_notifications_data()
                    if username in notifications_data:
                        notifications_data[username] = []
                        save_notifications_data(notifications_data)
                        st.success("All notifications deleted!")
                        st.rerun()
                else:
                    st.session_state["confirm_delete_all_notifications"] = True
                    st.warning("Click delete again to confirm!")
    else:
        st.info("No notifications found.")

def show_settings_page(data: dict):
    """Show user settings page."""
    st.markdown("""
    <div class="main-header">
        <h1>⚙️ Settings</h1>
        <p>Customize your experience</p>
    </div>
    """, unsafe_allow_html=True)
    
    # User profile section
    st.markdown("### 👤 User Profile")
    
    username = st.session_state.get("username")
    if not username:
        st.error("User not found.")
        return
    
    user_info = get_user_info(username)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.info(f"**Username:** {username}")
        st.info(f"**Full Name:** {user_info.get('full_name', 'Not set')}")
        st.info(f"**Email:** {user_info.get('email', 'Not set')}")
    
    with col2:
        st.info(f"**Role:** {user_info.get('role', 'personal').title()}")
        st.info(f"**Company:** {user_info.get('company_code', 'None')}")
        st.info(f"**Member Since:** {user_info.get('created_at', 'Unknown')}")
    
    # Session management section
    st.markdown("### 🔐 Session Management")
    
    session_timestamp = st.session_state.get("session_timestamp")
    if session_timestamp:
        session_age_hours = (datetime.datetime.now().timestamp() - session_timestamp) / 3600
        remaining_hours = max(0, 48 - session_age_hours)
        session_start = datetime.datetime.fromtimestamp(session_timestamp).strftime("%Y-%m-%d %H:%M:%S")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.info(f"**Session Started:** {session_start}")
            st.info(f"**Session Age:** {session_age_hours:.1f} hours")
        
        with col2:
            st.info(f"**Time Remaining:** {remaining_hours:.1f} hours")
            st.info(f"**Session Status:** {'🟢 Active' if remaining_hours > 0 else '🔴 Expired'}")
        
        if st.button("🔄 Refresh Session", use_container_width=True):
            refresh_session()
            st.success("Session refreshed! You now have 48 hours remaining.")
            st.rerun()
    else:
        st.warning("No active session found.")
    
    # App settings
    st.markdown("### ⚙️ Application Settings")
    
    settings = data.get("settings", {})
    
    with st.form("app_settings"):
        theme = st.selectbox("Theme", ["light", "dark"], 
                           index=0 if settings.get("theme", "light") == "light" else 1)
        notifications_enabled = st.checkbox("Enable Notifications", 
                                          value=settings.get("notifications", True))
        notification_sound = st.checkbox("Enable Notification Sounds", 
                                       value=settings.get("notification_sound", True))
        notification_popup = st.checkbox("Enable Notification Popups", 
                                       value=settings.get("notification_popup", True))
        default_priority = st.selectbox("Default Task Priority", 
                                      ["low", "medium", "high"],
                                      index=["low", "medium", "high"].index(settings.get("default_priority", "medium")))
        show_team_tasks = st.checkbox("Show Team Tasks in Dashboard", 
                                    value=settings.get("show_team_tasks", True))
        
        if st.form_submit_button("💾 Save Settings"):
            data["settings"] = {
                "theme": theme,
                "notifications": notifications_enabled,
                "notification_sound": notification_sound,
                "notification_popup": notification_popup,
                "default_priority": default_priority,
                "show_team_tasks": show_team_tasks
            }
            save_data(data)
            update_user_theme(username, theme)
            refresh_session()  # Refresh session on settings save
            st.success("Settings saved successfully!")
    
    # Notification sound test
    st.markdown("### 🔊 Notification Sound Test")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔊 Test Task Sound"):
            test_notification = {
                "type": "task",
                "title": "Test Task Notification",
                "message": "This is a test task notification sound",
                "created_at": "Now"
            }
            show_notification_popup(test_notification)
    
    with col2:
        if st.button("🔊 Test File Sound"):
            test_notification = {
                "type": "file",
                "title": "Test File Notification",
                "message": "This is a test file notification sound",
                "created_at": "Now"
            }
            show_notification_popup(test_notification)
    
    with col3:
        if st.button("🔊 Test Chat Sound"):
            test_notification = {
                "type": "chat",
                "title": "Test Chat Notification",
                "message": "This is a test chat notification sound",
                "created_at": "Now"
            }
            show_notification_popup(test_notification)
    
    st.markdown("---")
    
    # Test notifications
    st.markdown("### 🧪 Test Notifications")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📋 Test Task Notification"):
            send_task_notification(username, "Test Task", "created", None, "high")
            st.success("Task notification sent!")
    
    with col2:
        if st.button("📁 Test File Notification"):
            send_file_notification(username, "test_file.pdf", "uploaded", None, "normal")
            st.success("File notification sent!")
    
    with col3:
        if st.button("📊 Test Poll Notification"):
            send_poll_notification(username, "Test Poll Question", "created", None, "normal")
            st.success("Poll notification sent!")
    
    col4, col5, col6 = st.columns(3)
    
    with col4:
        if st.button("📅 Test Calendar Notification"):
            send_calendar_notification(username, "Test Event", "created", None, "normal")
            st.success("Calendar notification sent!")
    
    with col5:
        if st.button("💬 Test Chat Notification"):
            send_chat_notification(username, "Test User", "This is a test message", "normal")
            st.success("Chat notification sent!")
    
    with col6:
        if st.button("📈 Test Project Notification"):
            send_project_notification(username, "Test Project", "assigned", None, "high")
            st.success("Project notification sent!")
    
    st.markdown("---")
    
    # Category management
    st.markdown("### 📂 Category Management")
    
    categories = data.get("categories", ["Work", "Personal", "Health", "Learning", "Finance", "Team"])
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Current Categories")
        for category in categories:
            st.write(f"• {category}")
    
    with col2:
        with st.form("add_category"):
            new_category = st.text_input("New Category Name")
            if st.form_submit_button("➕ Add Category"):
                if new_category.strip() and new_category not in categories:
                    categories.append(new_category.strip())
                    data["categories"] = categories
                    save_data(data)
                    st.success(f"Category '{new_category}' added!")
                    st.rerun()
                elif new_category in categories:
                    st.error("Category already exists!")
    
    # Data management
    st.markdown("### 💾 Data Management")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📊 Export Data", use_container_width=True):
            # Export user data
            export_data = {
                "user_info": user_info,
                "tasks": data.get("tasks", []),
                "notes": data.get("notes", []),
                "contacts": data.get("contacts", []),
                "goals": data.get("goals", []),
                "assigned_tasks": data.get("assigned_tasks", []),
                "exported_at": get_current_timestamp()
            }
            
            st.download_button(
                label="📥 Download Data",
                data=json.dumps(export_data, indent=2, ensure_ascii=False),
                file_name=f"user_data_{username}_{get_current_timestamp()}.json",
                mime="application/json",
                use_container_width=True
            )
    
    with col2:
        if st.button("🗑️ Clear All Data", use_container_width=True):
            if st.session_state.get("confirm_clear_data"):
                # Clear all user data
                data = {
                    "tasks": [],
                    "notes": [],
                    "contacts": [],
                    "goals": [],
                    "assigned_tasks": [],
                    "team_notifications": [],
                    "categories": ["Work", "Personal", "Health", "Learning", "Finance", "Team"],
                    "settings": {
                        "theme": "light",
                        "notifications": True,
                        "default_priority": "medium",
                        "show_team_tasks": True
                    }
                }
                save_data(data)
                st.success("All data cleared!")
                st.rerun()
            else:
                st.session_state["confirm_clear_data"] = True
                st.warning("Click clear again to confirm!")
    
    with col3:
        if st.button("🔄 Reset Settings", use_container_width=True):
            if st.session_state.get("confirm_reset_settings"):
                # Reset to default settings
                data["settings"] = {
                    "theme": "light",
                    "notifications": True,
                    "default_priority": "medium",
                    "show_team_tasks": True
                }
                save_data(data)
                st.success("Settings reset to defaults!")
                st.rerun()
            else:
                st.session_state["confirm_reset_settings"] = True
                st.warning("Click reset again to confirm!")
    
    # Account management
    st.markdown("### 🔐 Account Management")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔑 Change Password", use_container_width=True):
            st.session_state["show_change_password"] = True
    
    with col2:
        if st.button("🚪 Deactivate Account", use_container_width=True):
            if st.session_state.get("confirm_deactivate"):
                # Deactivate account
                auth_data = load_auth_data()
                if username in auth_data:
                    auth_data[username]["active"] = False
                    save_auth_data(auth_data)
                    st.success("Account deactivated!")
                    st.session_state["authenticated"] = False
                    st.session_state["username"] = ""
                    st.rerun()
            else:
                st.session_state["confirm_deactivate"] = True
                st.warning("Click deactivate again to confirm!")
    
    # Change password form
    if st.session_state.get("show_change_password"):
        with st.form("change_password"):
            st.markdown("#### 🔑 Change Password")
            
            current_password = st.text_input("Current Password", type="password")
            new_password = st.text_input("New Password", type="password")
            confirm_password = st.text_input("Confirm New Password", type="password")
            
            col1, col2 = st.columns(2)
            
            with col1:
                if st.form_submit_button("💾 Change Password"):
                    if not all([current_password, new_password, confirm_password]):
                        st.error("Please fill in all fields!")
                    elif new_password != confirm_password:
                        st.error("New passwords do not match!")
                    elif len(new_password) < 6:
                        st.error("Password must be at least 6 characters long!")
                    else:
                        # Verify current password
                        auth_data = load_auth_data()
                        if username in auth_data:
                            if auth_data[username]["password_hash"] == hash_password(current_password):
                                # Update password
                                auth_data[username]["password_hash"] = hash_password(new_password)
                                save_auth_data(auth_data)
                                st.success("Password changed successfully!")
                                st.session_state["show_change_password"] = False
                                st.rerun()
                            else:
                                st.error("Current password is incorrect!")
                        else:
                            st.error("User not found!")
            
            with col2:
                if st.form_submit_button("❌ Cancel"):
                    st.session_state["show_change_password"] = False
                    st.rerun()

def show_company_chat_page(username: str, company_info: dict):
    """Show company chat page."""
    st.markdown("""
    <div class="main-header">
        <h1>💬 Company Chat</h1>
        <p>Real-time communication with your team</p>
    </div>
    """, unsafe_allow_html=True)
    
    if not company_info or not company_info.get("name"):
        st.error("You need to be part of a company to access the chat.")
        return
    
    company_code = company_info.get("code")
    if not company_code:
        st.error("Invalid company information.")
        return
    
    # Chat interface
    st.markdown("### 💬 Team Chat")
    
    # Display chat messages
    messages = get_company_chat_messages(company_code, limit=100)
    
    # Chat container with scrollable area
    chat_container = st.container()
    
    with chat_container:
        # Display messages
        for message in messages:
            is_own_message = message.get("from_username") == username
            message_style = "background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white;" if is_own_message else "background: white; border: 1px solid #e0e0e0;"
            
            st.markdown(f"""
            <div style="margin: 10px 0; padding: 15px; border-radius: 15px; {message_style}">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 5px;">
                    <strong>{message.get('from_name', 'Unknown')}</strong>
                    <small>{message.get('timestamp', 'Unknown')}</small>
                </div>
                <div style="margin-bottom: 5px;">
                    <span style="background: rgba(255,255,255,0.2); padding: 2px 8px; border-radius: 10px; font-size: 0.8em;">
                        {message.get('from_role', 'employee').title()}
                    </span>
                </div>
                <p style="margin: 0;">{message.get('message', '')}</p>
                {f"<small style='opacity: 0.7;'>Edited by {message.get('edited_by', 'Unknown')}</small>" if message.get('edited') else ""}
            </div>
            """, unsafe_allow_html=True)
            
            # Message actions (edit/delete) - only for own messages
            if is_own_message:
                col1, col2 = st.columns(2)
                
                with col1:
                    if st.button("✏️ Edit", key=f"edit_msg_{message['id']}"):
                        st.session_state[f"edit_message_{message['id']}"] = True
                
                with col2:
                    if st.button("🗑️ Delete", key=f"delete_msg_{message['id']}"):
                        if delete_chat_message(company_code, message["id"], username):
                            st.success("Message deleted!")
                            st.rerun()
                        else:
                            st.error("Failed to delete message!")
                
                # Edit message form
                if st.session_state.get(f"edit_message_{message['id']}"):
                    with st.form(f"edit_form_{message['id']}"):
                        new_message = st.text_area("Edit Message", value=message.get("message", ""))
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            if st.form_submit_button("💾 Save"):
                                if new_message and new_message.strip():
                                    if edit_chat_message(company_code, message["id"], new_message.strip(), username):
                                        st.success("Message updated!")
                                        st.session_state[f"edit_message_{message['id']}"] = False
                                        st.rerun()
                                    else:
                                        st.error("Failed to update message!")
                                else:
                                    st.error("Please enter a message!")
                        
                        with col2:
                            if st.form_submit_button("❌ Cancel"):
                                st.session_state[f"edit_message_{message['id']}"] = False
                                st.rerun()
    
    # Send new message
    st.markdown("---")
    st.markdown("### 📝 Send Message")
    
    with st.form("send_message"):
        new_message = st.text_area("Your message", placeholder="Type your message here...", height=100)
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            if st.form_submit_button("💬 Send Message", use_container_width=True):
                if new_message.strip():
                    send_chat_message(company_code, username, new_message.strip())
                    st.success("Message sent!")
                    st.rerun()
                else:
                    st.error("Please enter a message!")
        
        with col2:
            if st.form_submit_button("🔄 Refresh", use_container_width=True):
                st.rerun()

def show_role_management_page(username: str, company_info: dict):
    """Show role management page."""
    st.markdown("""
    <div class="main-header">
        <h1>👥 Role Management</h1>
        <p>Manage team roles and permissions</p>
    </div>
    """, unsafe_allow_html=True)
    
    if not company_info or not company_info.get("name"):
        st.error("You need to be part of a company to access role management.")
        return
    
    company_code = company_info.get("code")
    if not company_code:
        st.error("Invalid company information.")
        return
    
    # Check if user has permission
    user_info = get_user_info(username)
    user_role = user_info.get("role", "employee")
    
    # Check if user has permission to manage roles
    if user_role.lower() != "admin" and not can_manage_role(user_role, "employee"):
        st.error("You don't have permission to manage roles.")
        return
    
    # Role hierarchy display
    st.markdown("### 🏗️ Role Hierarchy")
    
    st.markdown("""
    **Role Hierarchy (from highest to lowest):**
    - **Admin** (Level 11) - System Administrator
    - **CEO** (Level 10) - Company Chief Executive Officer
    - **CFO/CTO** (Level 9) - Chief Financial/Technology Officer  
    - **VP** (Level 8) - Vice President
    - **Director** (Level 7) - Director
    - **Senior Manager** (Level 6) - Senior Manager
    - **Manager** (Level 5) - Manager
    - **Team Lead** (Level 4) - Team Leader
    - **Senior Employee** (Level 3) - Senior Employee
    - **Employee** (Level 2) - Regular Employee
    - **Intern** (Level 1) - Intern
    
    **Role Management Rules:**
    - **Admins** can manage any role
    - **Higher-level roles** can manage any role below them in the hierarchy
    - Example: Level 6 (Senior Manager) can manage Level 5, 4, 3, 2, 1 roles
    """)
    
    # Get all employees
    employees = get_company_employees(company_code)
    
    if employees:
        st.markdown("### 👥 Manage Team Roles")
        
        # Filter employees that current user can manage
        manageable_employees = []
        for employee in employees:
            if user_role.lower() == "admin" or can_manage_role(user_role, employee.get("role", "employee")):
                manageable_employees.append(employee)
        
        if manageable_employees:
            for employee in manageable_employees:
                with st.container():
                    col1, col2, col3 = st.columns([2, 2, 1])
                    
                    with col1:
                        st.write(f"**{employee.get('full_name', 'Unknown')}**")
                        st.write(f"Username: {employee.get('username', 'Unknown')}")
                    
                    with col2:
                        current_role = employee.get("role", "employee")
                        st.write(f"**Current Role:** {current_role.title()}")
                        st.write(f"**Level:** {get_role_level(current_role)}")
                    
                    with col3:
                        if st.button("Change Role", key=f"change_role_{employee['username']}"):
                            st.session_state[f"show_role_change_{employee['username']}"] = True
                    
                    # Role change form
                    if st.session_state.get(f"show_role_change_{employee['username']}"):
                        with st.form(f"role_change_form_{employee['username']}"):
                            st.markdown(f"#### Change Role for {employee.get('full_name', 'Unknown')}")
                            
                            # Available roles (all roles for admins, lower roles for others)
                            available_roles = []
                            for role, level in ROLE_HIERARCHY.items():
                                if user_role.lower() == "admin" or level < get_role_level(user_role):
                                    available_roles.append(role)
                            
                            new_role = st.selectbox("New Role", available_roles, 
                                                   index=available_roles.index(current_role) if current_role in available_roles else 0)
                            
                            col1, col2 = st.columns(2)
                            with col1:
                                if st.form_submit_button("💾 Change Role"):
                                    if new_role:
                                        success, message = change_user_role(company_code, employee["username"], new_role, username)
                                        if success:
                                            st.success(message)
                                            st.session_state[f"show_role_change_{employee['username']}"] = False
                                            st.rerun()
                                        else:
                                            st.error(message)
                                    else:
                                        st.error("Please select a role!")
                            
                            with col2:
                                if st.form_submit_button("❌ Cancel"):
                                    st.session_state[f"show_role_change_{employee['username']}"] = False
                                    st.rerun()
                    
                    st.markdown("---")
        else:
            st.info("No employees found that you can manage.")
    else:
        st.info("No employees found in the company.")
    
    # Add custom roles (for admins only)
    if user_info.get("role") in ["admin", "ceo", "cfo", "cto"]:
        st.markdown("### ➕ Add Custom Role")
        
        with st.form("add_custom_role"):
            role_name = st.text_input("Role Name", placeholder="e.g., Senior Developer, Product Manager")
            role_level = st.slider("Role Level", min_value=1, max_value=9, value=3, 
                                 help="Higher level = more permissions")
            
            if st.form_submit_button("➕ Add Custom Role"):
                if role_name.strip():
                    success, message = add_custom_role(company_code, role_name.strip(), role_level, username)
                    if success:
                        st.success(message)
                        st.rerun()
                    else:
                        st.error(message)
                else:
                    st.error("Please enter a role name!")
    
    # Role permissions info
    st.markdown("### ℹ️ Role Permissions")
    
    st.markdown("""
    **Permission Rules:**
    - **Admins** can manage any role
    - **Higher-level roles** can manage any role below them in the hierarchy
    - Higher-level roles have more permissions
    - **Chat restrictions:** Only original authors can edit/delete their own messages
    - **Task attachments:** Users can add files and code snippets when completing tasks
    """)

def show_private_chat_page(username: str, company_info: dict):
    """Show private chat page."""
    st.markdown("""
    <div class="main-header">
        <h1>💬 Private Chat</h1>
        <p>Direct messaging with team members</p>
    </div>
    """, unsafe_allow_html=True)
    
    if not company_info or not company_info.get("name"):
        st.error("You need to be part of a company to access private chat.")
        return
    
    company_code = company_info.get("code")
    if not company_code:
        st.error("Invalid company information.")
        return
    
    # Update user status to online
    update_user_status(username, "online")
    
    # Get user's private chats
    user_chats = get_user_private_chats(username)
    
    # Get all team members for starting new chats
    team_members = get_company_employees(company_code)
    team_members = [m for m in team_members if m.get("username") != username]
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("### 👥 Team Members")
        
        # Show online status for team members
        for member in team_members:
            member_username = member.get("username")
            member_status = get_user_status(member_username)
            status_emoji = {
                "online": "🟢",
                "away": "🟡", 
                "busy": "🔴",
                "offline": "⚫"
            }.get(member_status.get("status", "offline"), "⚫")
            
            if st.button(f"{status_emoji} {member.get('full_name', member_username)}", 
                        key=f"chat_with_{member_username}", use_container_width=True):
                st.session_state["selected_chat_user"] = member_username
                st.rerun()
        
        # Show existing chats
        if user_chats:
            st.markdown("### 💬 Recent Chats")
            for chat in user_chats:
                unread_badge = f" ({chat.get('unread_count', 0)})" if chat.get('unread_count', 0) > 0 else ""
                if st.button(f"💬 {chat.get('other_user_name', 'Unknown')}{unread_badge}", 
                           key=f"recent_chat_{chat['other_user']}", use_container_width=True):
                    st.session_state["selected_chat_user"] = chat.get("other_user")
                    st.rerun()
    
    with col2:
        selected_user = st.session_state.get("selected_chat_user")
        
        if selected_user:
            selected_user_info = get_user_info(selected_user)
            st.markdown(f"### 💬 Chat with {selected_user_info.get('full_name', selected_user)}")
            
            # Display chat messages
            messages = get_private_messages(username, selected_user, limit=100)
            
            chat_container = st.container()
            with chat_container:
                for message in messages:
                    is_own_message = message.get("from_username") == username
                    message_style = "background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white;" if is_own_message else "background: white; border: 1px solid #e0e0e0;"
                    read_indicator = "✅" if message.get("read", False) else "📤"
                    
                    st.markdown(f"""
                    <div style="margin: 10px 0; padding: 15px; border-radius: 15px; {message_style}">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 5px;">
                            <strong>{message.get('from_name', 'Unknown')}</strong>
                            <small>{message.get('timestamp', 'Unknown')} {read_indicator}</small>
                        </div>
                        <p style="margin: 0;">{message.get('message', '')}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Mark message as read if it's from the other user
                    if not is_own_message and not message.get("read", False):
                        message_id = message.get("id")
                        if message_id:
                            mark_private_message_read(username, selected_user, message_id)
            
            # Send new message
            st.markdown("---")
            with st.form("send_private_message"):
                new_message = st.text_area("Your message", placeholder="Type your message here...", height=100)
                
                col1, col2 = st.columns([3, 1])
                with col1:
                    if st.form_submit_button("💬 Send Message", use_container_width=True):
                        if new_message.strip():
                            if send_private_message(username, selected_user, new_message.strip()):
                                st.success("Message sent!")
                                st.rerun()
                            else:
                                st.error("Failed to send message!")
                        else:
                            st.error("Please enter a message!")
                
                with col2:
                    if st.form_submit_button("🔄 Refresh", use_container_width=True):
                        st.rerun()
        else:
            st.info("Select a team member to start chatting!")

def show_file_sharing_page(username: str, company_info: dict):
    """Show file sharing page."""
    st.markdown("""
    <div class="main-header">
        <h1>📁 File Sharing</h1>
        <p>Share and manage files with your team</p>
    </div>
    """, unsafe_allow_html=True)
    
    if not company_info or not company_info.get("name"):
        st.error("You need to be part of a company to access file sharing.")
        return
    
    company_code = company_info.get("code")
    if not company_code:
        st.error("Invalid company information.")
        return
    
    # Create tabs for different file sharing options
    tab1, tab2, tab3 = st.tabs(["📤 Upload Files", "📁 Shared Files", "🔒 Private Files"])
    
    with tab1:
        st.markdown("### 📤 Upload Files")
        
        # File sharing type selection
        share_type = st.radio("Share with:", ["Company", "Private"], horizontal=True)
        
        if share_type == "Company":
            # Company-wide file upload
            with st.form("upload_company_file"):
                uploaded_file = st.file_uploader("Choose a file", type=['txt', 'pdf', 'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx', 'jpg', 'jpeg', 'png', 'gif'], key="company_file")
                file_description = st.text_area("File Description (Optional)", placeholder="Describe what this file is for...")
                
                if st.form_submit_button("📤 Upload to Company", use_container_width=True):
                    if uploaded_file is not None:
                        file_content = uploaded_file.read()
                        if upload_file(company_code, username, uploaded_file.name, file_content, uploaded_file.type):
                            st.success(f"File '{uploaded_file.name}' uploaded to company successfully!")
                            st.rerun()
                        else:
                            st.error("Failed to upload file!")
                    else:
                        st.error("Please select a file to upload!")
        
        else:
            # Private file upload
            team_members = get_company_employees(company_code)
            team_members = [m for m in team_members if m.get("username") != username]
            
            if team_members:
                with st.form("upload_private_file"):
                    uploaded_file = st.file_uploader("Choose a file", type=['txt', 'pdf', 'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx', 'jpg', 'jpeg', 'png', 'gif'], key="private_file")
                    
                    # Select recipient
                    recipient_options = [f"{m.get('full_name', 'Unknown')} ({m.get('username', 'Unknown')})" for m in team_members]
                    selected_recipient = st.selectbox("Share with:", recipient_options)
                    
                    file_description = st.text_area("File Description (Optional)", placeholder="Describe what this file is for...")
                    
                    if st.form_submit_button("📤 Share Privately", use_container_width=True):
                        if uploaded_file is not None and selected_recipient:
                            file_content = uploaded_file.read()
                            recipient_username = selected_recipient.split("(")[1].split(")")[0]
                            
                            if upload_private_file(username, recipient_username, uploaded_file.name, file_content, uploaded_file.type):
                                st.success(f"File '{uploaded_file.name}' shared privately with {selected_recipient.split('(')[0].strip()}!")
                                st.rerun()
                            else:
                                st.error("Failed to share file!")
                        else:
                            st.error("Please select a file and recipient!")
            else:
                st.info("No team members available for private sharing.")
    
    with tab2:
        st.markdown("### 📁 Company Shared Files")
        
        files = get_company_files(company_code)
        
        if files:
            # Search and filter
            search_query = st.text_input("🔍 Search files", placeholder="Search by filename...", key="company_search")
            
            if search_query:
                files = [f for f in files if search_query.lower() in f.get("name", "").lower()]
            
            # Sort by upload date (newest first)
            files = sorted(files, key=lambda x: x.get("uploaded_at", ""), reverse=True)
            
            for file_info in files:
                with st.container():
                    col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
                    
                    with col1:
                        st.write(f"**📄 {file_info.get('name', 'Unknown')}**")
                        st.write(f"Uploaded by: {get_user_info(file_info.get('uploaded_by', '')).get('full_name', file_info.get('uploaded_by', 'Unknown'))}")
                        st.write(f"Size: {file_info.get('size', 0)} bytes")
                        st.write(f"Uploaded: {file_info.get('uploaded_at', 'Unknown')}")
                        if file_info.get('description'):
                            st.write(f"Description: {file_info.get('description')}")
                    
                    with col2:
                        st.write(f"Downloads: {file_info.get('downloads', 0)}")
                    
                    with col3:
                        if st.button("📥 Download", key=f"download_{file_info['id']}"):
                            file_content = download_file(company_code, file_info["id"])
                            if file_content:
                                st.download_button(
                                    label="📥 Download File",
                                    data=file_content,
                                    file_name=file_info.get("name", "file"),
                                    mime=file_info.get("type", "application/octet-stream"),
                                    use_container_width=True
                                )
                            else:
                                st.error("Failed to download file!")
                    
                    with col4:
                        if file_info.get("uploaded_by") == username or is_admin_or_manager(username):
                            if st.button("🗑️ Delete", key=f"delete_file_{file_info['id']}"):
                                # Delete file functionality would go here
                                st.warning("File deletion not implemented yet!")
                    
                    st.markdown("---")
        else:
            st.info("No files shared in the company yet.")
    
    with tab3:
        st.markdown("### 🔒 Private Files")
        
        # Get user's private files
        private_files = get_user_private_files(username)
        
        if private_files:
            # Search and filter
            search_query = st.text_input("🔍 Search private files", placeholder="Search by filename...", key="private_search")
            
            if search_query:
                private_files = [f for f in private_files if search_query.lower() in f.get("name", "").lower()]
            
            # Sort by upload date (newest first)
            private_files = sorted(private_files, key=lambda x: x.get("uploaded_at", ""), reverse=True)
            
            for file_info in private_files:
                with st.container():
                    col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
                    
                    with col1:
                        # Determine if user is sender or receiver
                        is_sender = file_info.get("uploaded_by") == username
                        other_user = file_info.get("other_user", "Unknown")
                        other_user_info = get_user_info(other_user)
                        other_user_name = other_user_info.get("full_name", other_user) if other_user_info else other_user
                        
                        direction_emoji = "📤" if is_sender else "📥"
                        direction_text = f"Sent to {other_user_name}" if is_sender else f"Received from {other_user_name}"
                        
                        st.write(f"**{direction_emoji} {file_info.get('name', 'Unknown')}**")
                        st.write(f"**{direction_text}**")
                        st.write(f"Size: {file_info.get('size', 0)} bytes")
                        st.write(f"Shared: {file_info.get('uploaded_at', 'Unknown')}")
                    
                    with col2:
                        st.write(f"Downloads: {file_info.get('downloads', 0)}")
                    
                    with col3:
                        if st.button("📥 Download", key=f"download_private_{file_info['id']}"):
                            file_content = download_private_file(username, other_user, file_info["id"])
                            if file_content:
                                st.download_button(
                                    label="📥 Download File",
                                    data=file_content,
                                    file_name=file_info.get("name", "file"),
                                    mime=file_info.get("type", "application/octet-stream"),
                                    use_container_width=True
                                )
                            else:
                                st.error("Failed to download file!")
                    
                    with col4:
                        # Only sender can delete
                        if file_info.get("uploaded_by") == username:
                            if st.button("🗑️ Delete", key=f"delete_private_{file_info['id']}"):
                                if delete_private_file(username, other_user, file_info["id"], username):
                                    st.success("File deleted successfully!")
                                    st.rerun()
                                else:
                                    st.error("Failed to delete file!")
                    
                    st.markdown("---")
        else:
                         st.info("No private files shared yet.")

def show_calendar_page(username: str, company_info: dict):
    """Show calendar page."""
    st.markdown("""
    <div class="main-header">
        <h1>📅 Team Calendar</h1>
        <p>Schedule and manage team events</p>
    </div>
    """, unsafe_allow_html=True)
    
    if not company_info or not company_info.get("name"):
        st.error("You need to be part of a company to access the calendar.")
        return
    
    company_code = company_info.get("code")
    if not company_code:
        st.error("Invalid company information.")
        return
    
    # Create new event
    st.markdown("### ➕ Create Event")
    
    with st.form("create_event"):
        col1, col2 = st.columns(2)
        
        with col1:
            event_title = st.text_input("Event Title*", placeholder="Enter event title")
            event_type = st.selectbox("Event Type", ["meeting", "deadline", "presentation", "workshop", "other"])
            start_date = st.date_input("Start Date*")
            start_time = st.time_input("Start Time*")
        
        with col2:
            event_description = st.text_area("Description", placeholder="Event description...")
            end_date = st.date_input("End Date*")
            end_time = st.time_input("End Time*")
        
        # Attendee selection
        team_members = get_company_employees(company_code)
        team_members = [m for m in team_members if m.get("username") != username]
        
        attendee_options = [f"{m.get('full_name', 'Unknown')} ({m.get('username', 'Unknown')})" for m in team_members]
        selected_attendees = st.multiselect("Invite Attendees", attendee_options)
        
        if st.form_submit_button("📅 Create Event", use_container_width=True):
            if not event_title.strip():
                st.error("Please enter an event title!")
            else:
                # Convert dates and times to strings
                start_datetime = f"{start_date.strftime('%Y-%m-%d')} {start_time.strftime('%H:%M')}"
                end_datetime = f"{end_date.strftime('%Y-%m-%d')} {end_time.strftime('%H:%M')}"
                
                # Extract usernames from selected attendees
                attendee_usernames = []
                for attendee in selected_attendees:
                    username_part = attendee.split("(")[1].split(")")[0]
                    attendee_usernames.append(username_part)
                
                if create_calendar_event(company_code, username, event_title.strip(), 
                                       event_description.strip(), start_datetime, end_datetime, 
                                       event_type, attendee_usernames):
                    st.success("Event created successfully!")
                    st.rerun()
                else:
                    st.error("Failed to create event!")
    
    # Display events
    st.markdown("### 📅 Upcoming Events")
    
    events = get_user_events(username, company_code)
    
    if events:
        # Filter upcoming events
        current_time = datetime.datetime.now()
        upcoming_events = []
        
        for event in events:
            try:
                event_start = datetime.datetime.strptime(event.get("start_date", ""), "%Y-%m-%d %H:%M")
                if event_start > current_time:
                    upcoming_events.append(event)
            except:
                continue
        
        upcoming_events = sorted(upcoming_events, key=lambda x: x.get("start_date", ""))
        
        if upcoming_events:
            for event in upcoming_events[:10]:  # Show next 10 events
                with st.container():
                    event_type_emoji = {
                        "meeting": "🤝",
                        "deadline": "⏰",
                        "presentation": "📊",
                        "workshop": "🔧",
                        "other": "📅"
                    }.get(event.get("event_type", "other"), "📅")
                    
                    st.markdown(f"""
                    <div class="floating-card">
                        <h4>{event_type_emoji} {event.get('title', 'Untitled')}</h4>
                        <p><strong>Type:</strong> {event.get('event_type', 'other').title()}</p>
                        <p><strong>Start:</strong> {event.get('start_date', 'Unknown')}</p>
                        <p><strong>End:</strong> {event.get('end_date', 'Unknown')}</p>
                        <p><strong>Created by:</strong> {get_user_info(event.get('created_by', '')).get('full_name', event.get('created_by', 'Unknown'))}</p>
                        {f"<p><strong>Description:</strong> {event.get('description', 'No description')}</p>" if event.get('description') else ""}
                        {f"<p><strong>Attendees:</strong> {', '.join([get_user_info(a).get('full_name', a) for a in event.get('attendees', [])])}</p>" if event.get('attendees') else ""}
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.markdown("---")
        else:
            st.info("No upcoming events found.")
    else:
        st.info("No events found. Create your first event!")

def show_polls_page(username: str, company_info: dict):
    """Show polls page."""
    st.markdown("""
    <div class="main-header">
        <h1>📊 Team Polls</h1>
        <p>Create and participate in team polls</p>
    </div>
    """, unsafe_allow_html=True)
    
    if not company_info or not company_info.get("name"):
        st.error("You need to be part of a company to access polls.")
        return
    
    company_code = company_info.get("code")
    if not company_code:
        st.error("Invalid company information.")
        return
    
    # Create new poll
    st.markdown("### ➕ Create Poll")
    
    with st.form("create_poll"):
        poll_question = st.text_input("Poll Question*", placeholder="What would you like to ask?")
        
        col1, col2 = st.columns(2)
        
        with col1:
            option1 = st.text_input("Option 1*", placeholder="First option")
            option2 = st.text_input("Option 2*", placeholder="Second option")
            option3 = st.text_input("Option 3", placeholder="Third option (optional)")
        
        with col2:
            option4 = st.text_input("Option 4", placeholder="Fourth option (optional)")
            option5 = st.text_input("Option 5", placeholder="Fifth option (optional)")
            allow_multiple = st.checkbox("Allow multiple votes")
        
        duration_hours = st.slider("Poll Duration (hours)", 1, 168, 24, help="How long should the poll be active?")
        
        if st.form_submit_button("📊 Create Poll", use_container_width=True):
            if not poll_question.strip() or not option1.strip() or not option2.strip():
                st.error("Please enter a question and at least 2 options!")
            else:
                options = [option1.strip(), option2.strip()]
                if option3.strip():
                    options.append(option3.strip())
                if option4.strip():
                    options.append(option4.strip())
                if option5.strip():
                    options.append(option5.strip())
                
                if create_poll(company_code, username, poll_question.strip(), options, allow_multiple, duration_hours):
                    st.success("Poll created successfully!")
                    st.rerun()
                else:
                    st.error("Failed to create poll!")
    
    # Display polls
    st.markdown("### 📊 Active Polls")
    
    polls = get_company_polls(company_code)
    active_polls = [p for p in polls if p.get("status") == "active"]
    
    if active_polls:
        for poll in active_polls:
            with st.container():
                st.markdown(f"""
                <div class="floating-card">
                    <h4>📊 {poll.get('question', 'Untitled')}</h4>
                    <p><strong>Created by:</strong> {get_user_info(poll.get('created_by', '')).get('full_name', poll.get('created_by', 'Unknown'))}</p>
                    <p><strong>Created:</strong> {poll.get('created_at', 'Unknown')}</p>
                    <p><strong>Expires:</strong> {poll.get('expires_at', 'Unknown')}</p>
                    <p><strong>Multiple votes:</strong> {'Yes' if poll.get('allow_multiple', False) else 'No'}</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Check if user has already voted
                has_voted = username in poll.get("votes", {})
                
                if not has_voted:
                    with st.form(f"vote_poll_{poll['id']}"):
                        st.markdown("#### Vote")
                        
                        if poll.get("allow_multiple", False):
                            selected_option_texts = st.multiselect("Select options", poll.get("options", []))
                            # Convert selected option texts to indices
                            selected_options = [poll.get("options", []).index(opt) for opt in selected_option_texts]
                        else:
                            selected_option = st.selectbox("Select option", poll.get("options", []))
                            selected_options = [poll.get("options", []).index(selected_option)] if selected_option else []
                        
                        if st.form_submit_button("🗳️ Vote", use_container_width=True):
                            if selected_options:
                                try:
                                    if vote_poll(company_code, poll["id"], username, selected_options):
                                        st.success("Vote recorded!")
                                        st.rerun()
                                    else:
                                        st.error("Failed to record vote! You may have already voted or the poll is closed.")
                                except Exception as e:
                                    st.error(f"Error recording vote: {str(e)}")
                            else:
                                st.error("Please select an option!")
                else:
                    st.info("You have already voted in this poll.")
                
                # Show results
                st.markdown("#### 📊 Results")
                votes = poll.get("votes", {})
                total_votes = len(votes)
                
                if total_votes > 0:
                    for i, option in enumerate(poll.get("options", [])):
                        option_votes = sum(1 for user_votes in votes.values() if i in user_votes)
                        percentage = (option_votes / total_votes * 100) if total_votes > 0 else 0
                        
                        st.write(f"**{option}:** {option_votes} votes ({percentage:.1f}%)")
                        st.progress(percentage / 100)
                else:
                    st.info("No votes yet.")
                
                st.markdown("---")
    else:
        st.info("No active polls. Create the first poll!")
    
    # Show expired polls
    expired_polls = [p for p in polls if p.get("status") == "expired"]
    
    if expired_polls:
        st.markdown("### 📊 Expired Polls")
        
        for poll in expired_polls[-5:]:  # Show last 5 expired polls
            with st.container():
                st.markdown(f"""
                <div class="floating-card">
                    <h4>📊 {poll.get('question', 'Untitled')} (Expired)</h4>
                    <p><strong>Created by:</strong> {get_user_info(poll.get('created_by', '')).get('full_name', poll.get('created_by', 'Unknown'))}</p>
                    <p><strong>Expired:</strong> {poll.get('expires_at', 'Unknown')}</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Show final results
                st.markdown("#### 📊 Final Results")
                votes = poll.get("votes", {})
                total_votes = len(votes)
                
                if total_votes > 0:
                    for i, option in enumerate(poll.get("options", [])):
                        option_votes = sum(1 for user_votes in votes.values() if i in user_votes)
                        percentage = (option_votes / total_votes * 100) if total_votes > 0 else 0
                        
                        st.write(f"**{option}:** {option_votes} votes ({percentage:.1f}%)")
                        st.progress(percentage / 100)
                else:
                    st.info("No votes recorded.")
                
                st.markdown("---")

def show_search_page(username: str, company_info: dict):
    """Show search page."""
    st.markdown("""
    <div class="main-header">
        <h1>🔍 Search</h1>
        <p>Search through messages, tasks, and more</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Search interface
    search_query = st.text_input("🔍 Enter your search query", placeholder="Search for messages, tasks, files...")
    search_type = st.selectbox("Search in", ["all", "messages", "tasks", "files"])
    
    if st.button("🔍 Search", use_container_width=True):
        if search_query.strip():
            st.markdown("### 📋 Search Results")
            
            results = []
            
            # Search messages
            if search_type in ["all", "messages"] and company_info:
                company_code = company_info.get("code")
                if company_code:
                    message_results = search_messages(company_code, search_query.strip())
                    results.extend(message_results)
            
            # Search tasks
            if search_type in ["all", "tasks"]:
                task_results = search_tasks(username, search_query.strip())
                results.extend(task_results)
            
            # Search files (if implemented)
            if search_type in ["all", "files"] and company_info:
                company_code = company_info.get("code")
                if company_code:
                    files = get_company_files(company_code)
                    for file_info in files:
                        if search_query.lower() in file_info.get("name", "").lower():
                            results.append({
                                "type": "file",
                                "file": file_info,
                                "context": "Shared Files"
                            })
            
            # Display results
            if results:
                st.markdown(f"Found **{len(results)}** results:")
                
                for result in results:
                    result_type = result.get("type", "unknown")
                    
                    if result_type == "company_chat":
                        message = result.get("message", {})
                        st.markdown(f"""
                        <div class="floating-card">
                            <h4>💬 Company Chat</h4>
                            <p><strong>From:</strong> {message.get('from_name', 'Unknown')}</p>
                            <p><strong>Message:</strong> {message.get('message', '')}</p>
                            <p><strong>Time:</strong> {message.get('timestamp', 'Unknown')}</p>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    elif result_type == "private_chat":
                        message = result.get("message", {})
                        st.markdown(f"""
                        <div class="floating-card">
                            <h4>💬 Private Chat</h4>
                            <p><strong>From:</strong> {message.get('from_name', 'Unknown')}</p>
                            <p><strong>Message:</strong> {message.get('message', '')}</p>
                            <p><strong>Time:</strong> {message.get('timestamp', 'Unknown')}</p>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    elif result_type in ["personal_task", "assigned_task"]:
                        task = result.get("task", {})
                        st.markdown(f"""
                        <div class="floating-card">
                            <h4>📋 {result.get('context', 'Task')}</h4>
                            <p><strong>Title:</strong> {task.get('title', 'Untitled')}</p>
                            <p><strong>Description:</strong> {task.get('description', 'No description')}</p>
                            <p><strong>Status:</strong> {'✅ Completed' if task.get('completed', False) else '⏳ Pending'}</p>
                            <p><strong>Priority:</strong> {task.get('priority', 'medium').title()}</p>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    elif result_type == "file":
                        file_info = result.get("file", {})
                        st.markdown(f"""
                        <div class="floating-card">
                            <h4>📁 Shared File</h4>
                            <p><strong>Name:</strong> {file_info.get('name', 'Unknown')}</p>
                            <p><strong>Uploaded by:</strong> {get_user_info(file_info.get('uploaded_by', '')).get('full_name', file_info.get('uploaded_by', 'Unknown'))}</p>
                            <p><strong>Size:</strong> {file_info.get('size', 0)} bytes</p>
                            <p><strong>Uploaded:</strong> {file_info.get('uploaded_at', 'Unknown')}</p>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    st.markdown("---")
            else:
                st.info("No results found. Try a different search term.")
        else:
            st.warning("Please enter a search query!")

def show_project_management_page(username: str, company_info: dict):
    st.markdown("""
    <div class='main-header'>
        <h1>📊 Project Management</h1>
        <p>Manage and track all company projects here. (Feature coming soon!)</p>
    </div>
    """, unsafe_allow_html=True)

def show_department_management_page(username: str, company_info: dict):
    st.markdown("""
    <div class='main-header'>
        <h1>🏢 Department Management</h1>
        <p>Manage company departments, assign managers, and set goals. (Feature coming soon!)</p>
    </div>
    """, unsafe_allow_html=True)

def show_performance_reviews_page(username: str, company_info: dict):
    st.markdown("""
    <div class='main-header'>
        <h1>📈 Performance Reviews</h1>
        <p>Conduct and review employee performance. (Feature coming soon!)</p>
    </div>
    """, unsafe_allow_html=True)

def show_budget_management_page(username: str, company_info: dict):
    st.markdown("""
    <div class='main-header'>
        <h1>💰 Budget Management</h1>
        <p>Track and manage company budgets. (Feature coming soon!)</p>
    </div>
    """, unsafe_allow_html=True)

def show_advanced_reports_page(username: str, company_info: dict):
    st.markdown("""
    <div class='main-header'>
        <h1>📋 Advanced Reports</h1>
        <p>Generate and view advanced company reports. (Feature coming soon!)</p>
    </div>
    """, unsafe_allow_html=True)

def show_workflow_management_page(username: str, company_info: dict):
    st.markdown("""
    <div class='main-header'>
        <h1>🔄 Workflow Management</h1>
        <p>Automate and manage company workflows. (Feature coming soon!)</p>
    </div>
    """, unsafe_allow_html=True)

def show_knowledge_base_page(username: str, company_info: dict):
    st.markdown("""
    <div class='main-header'>
        <h1>📚 Knowledge Base</h1>
        <p>Access and manage the company knowledge base. (Feature coming soon!)</p>
    </div>
    """, unsafe_allow_html=True)

def show_integrations_page(username: str, company_info: dict):
    st.markdown("""
    <div class='main-header'>
        <h1>🔗 Integrations</h1>
        <p>Connect and manage integrations with external services. (Feature coming soon!)</p>
    </div>
    """, unsafe_allow_html=True)

# -------------------------------------------------------------
# Main Application Entry Point
# -------------------------------------------------------------

if __name__ == "__main__":
    main()
