import streamlit as st
from datetime import datetime, date, timedelta
import random
import time

# ---------------------------
# OOP Classes
# ---------------------------

class Milestone:
    def __init__(self, name):
        self.name = name
        self.completed = False
        self.created_at = datetime.now()

    def mark_complete(self):
        self.completed = True

    def update_name(self, new_name):
        self.name = new_name

class Goal:
    def __init__(self, title, description, deadline, category, priority="Medium"):
        self.title = title
        self.description = description
        self.deadline = deadline
        self.category = category
        self.priority = priority
        self.created_at = datetime.now()
        self.milestones = []

    def add_milestone(self, milestone):
        self.milestones.append(milestone)

    def delete_milestone(self, index):
        if 0 <= index < len(self.milestones):
            self.milestones.pop(index)

    def get_progress(self):
        if not self.milestones:
            return 0
        completed = sum(1 for m in self.milestones if m.completed)
        return int((completed / len(self.milestones)) * 100)

    def is_deadline_near(self):
        return self.deadline <= date.today() + timedelta(days=3)

    def is_overdue(self):
        return self.deadline < date.today()
    
    def days_remaining(self):
        return (self.deadline - date.today()).days

class Motivation:
    quotes = [
        "Keep going, you're doing great!",
        "Success is a series of small wins.",
        "Believe in yourself.",
        "Push yourself, because no one else will do it for you.",
        "Stay positive, work hard, make it happen.",
        "Hard work beats talent when talent doesn't work hard.",
        "The secret of getting ahead is getting started.",
        "Small steps every day lead to big results.",
        "You're capable of amazing things.",
        "Progress, not perfection.",
        "Don't watch the clock; do what it does. Keep going.",
        "The expert in anything was once a beginner.",
        "You don't have to be great to start, but you have to start to be great."
    ]

    @classmethod
    def get_quote(cls):
        return random.choice(cls.quotes)

# ---------------------------
# Streamlit App Configuration
# ---------------------------

st.set_page_config(
    page_title="Goal Tracker",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS with additional improvements
st.markdown("""
    <style>
    /* Base styles */
    .goal-card {
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 4px 12px 0 rgba(0,0,0,0.1);
        transition: all 0.3s ease;
        background-color: white;
    }
    .goal-card:hover {
        box-shadow: 0 8px 16px 0 rgba(0,0,0,0.15);
        transform: translateY(-2px);
    }
    
    /* Priority indicators */
    .urgent { border-left: 6px solid #FF4B4B; background-color: #fff0f0; }
    .high { border-left: 6px solid #FFA500; background-color: #fff8e6; }
    .medium { border-left: 6px solid #1C83E1; background-color: #f0f7ff; }
    .low { border-left: 6px solid #00D100; background-color: #f0fff0; }
    .completed { border-left: 6px solid #00D100; background-color: #f0fff0; opacity: 0.8; }
    
    /* Milestone styles */
    .milestone-completed {
        text-decoration: line-through;
        color: #808080;
        opacity: 0.7;
    }
    .milestone-item {
        padding: 8px 0;
        border-bottom: 1px solid #f0f0f0;
    }
    
    /* Progress bar customization */
    .stProgress > div > div > div {
        background-color: #4CAF50 !important;
    }
    
    /* Button styles */
    .stButton > button {
        border-radius: 8px !important;
        transition: all 0.2s;
    }
    .stButton > button:hover {
        transform: scale(1.02);
    }
    
    /* Timer styles */
    .timer-display {
        font-size: 3em;
        font-weight: bold;
        text-align: center;
        margin: 20px 0;
        font-family: monospace;
    }
    .work-mode { color: #4CAF50; }
    .break-mode { color: #FFA500; }
    
    /* Responsive adjustments */
    @media (max-width: 768px) {
        .goal-card {
            padding: 15px;
        }
    }
    
    /* Tooltip improvements */
    .stTooltip {
        font-size: 14px !important;
    }
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    ::-webkit-scrollbar-track {
        background: #f1f1f1;
    }
    ::-webkit-scrollbar-thumb {
        background: #888;
        border-radius: 4px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: #555;
    }
    </style>
    """, unsafe_allow_html=True)

# ---------------------------
# Main App
# ---------------------------

# Sidebar with enhanced features
with st.sidebar:
    st.title("🚀 Goal Tracker Pro+")
    st.markdown("🌟 Your personal productivity companion")
    
    # Quick Stats with icons
    if 'goals' in st.session_state and st.session_state.goals:
        total_goals = len(st.session_state.goals)
        completed_goals = sum(1 for g in st.session_state.goals if g.get_progress() == 100)
        overdue_goals = sum(1 for g in st.session_state.goals if g.is_overdue())
        active_goals = total_goals - completed_goals
        
        st.subheader("📊 Your Stats")
        st.metric("Active Goals", active_goals, help="Goals not yet completed")
        st.metric("Completed", completed_goals, f"{int(completed_goals/total_goals*100)}%" if total_goals else "0%")
        st.metric("Overdue", overdue_goals, "⚠️ Immediate attention needed" if overdue_goals else "All good!")
    
    # Enhanced Motivation Section
    st.subheader("💪 Motivation Boost")
    with st.expander("Get Inspired"):
        quote = Motivation.get_quote()
        st.markdown(f'<div style="font-style: italic; font-size: 16px;">"{quote}"</div>', unsafe_allow_html=True)
        if st.button("Another Quote"):
            st.rerun()
    
    # Quick Actions
    st.subheader("⚡ Quick Actions")
    if st.button("Create New Goal", use_container_width=True):
        st.session_state.expand_creator = True
    if st.button("View All Goals", use_container_width=True):
        if 'selected_goal_index' in st.session_state:
            st.session_state.selected_goal_index = None
        st.rerun()
    
    # Help Section
    st.markdown("---")
    with st.expander("❓ Help & Tips"):
        st.markdown("""
        **Tips for effective goal tracking:**
        1. Break big goals into smaller milestones
        2. Set realistic deadlines
        3. Prioritize your goals
        4. Review progress regularly
        
        **Timer Features:**
        - Pomodoro: Work 25min, Break 5min
        - Custom: Set any duration
        
        **Priority Guide:**
        - 🔥 Urgent: Critical, needs immediate attention
        - ⚠️ High: Important but not urgent
        - 📌 Medium: Normal priority
        - 🌱 Low: Nice to have
        """)

# Main Content with better organization
st.title("🚀 My Goals Dashboard")

# ---------------------------
# Enhanced Goal Creation
# ---------------------------

# Auto-expand if coming from quick action
expanded = st.session_state.get('expand_creator', False)
with st.expander("➕ Create New Goal", expanded=expanded):
    if expanded:
        st.session_state.expand_creator = False  # Reset after expansion
    
    # Initialize suggested deadline in session state
    if 'suggested_deadline' not in st.session_state:
        st.session_state.suggested_deadline = None
    
    cols = st.columns([2, 1])
    title = cols[0].text_input("Goal Title*", placeholder="e.g., Learn Python Basics", help="Be specific about what you want to achieve")
    category = cols[1].selectbox("Category*", ["Study", "Health", "Finance", "Personal", "Work", "Other"], 
                               help="Category helps with organization")
    
    description = st.text_area("Description", placeholder="Why is this goal important? What does success look like?", 
                             help="Detailed descriptions increase commitment")
    
    cols = st.columns([1, 1, 1, 1])
    deadline = cols[0].date_input("Deadline*", min_value=date.today(), 
                                help="Set a realistic but challenging deadline")
    priority = cols[1].selectbox("Priority*", ["Urgent", "High", "Medium", "Low"], 
                               index=2, help="Helps with prioritization")
    
    # Smart deadline suggestions based on priority - now outside form
    with cols[2]:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Suggest Deadline", help="Get smart deadline suggestions"):
            days_to_add = {"Urgent": 7, "High": 14, "Medium": 30, "Low": 60}
            suggested_date = date.today() + timedelta(days=days_to_add[priority])
            st.session_state.suggested_deadline = suggested_date
            st.rerun()
    
    if st.session_state.suggested_deadline:
        with cols[3]:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button(f"Use {st.session_state.suggested_deadline.strftime('%b %d')}"):
                deadline = st.session_state.suggested_deadline
                st.session_state.suggested_deadline = None
                st.rerun()
    
    # Main add goal button - now outside form
    if st.button("✨ Add Goal", use_container_width=True):
        if title:  # Basic validation
            new_goal = Goal(title, description, deadline, category, priority)
            st.session_state.goals.append(new_goal)
            st.success(f"Goal '{title}' added successfully!")
            st.balloons()
            st.session_state.suggested_deadline = None
            st.rerun()
        else:
            st.error("Please enter a goal title")

# ---------------------------
# Enhanced Goals Display
# ---------------------------

if 'goals' not in st.session_state:
    st.session_state.goals = []

if st.session_state.goals:
    # Improved Filtering System
    st.subheader("🔍 Find Your Goals")
    with st.expander("Filter & Sort Options", expanded=True):
        cols = st.columns([2, 2, 1, 1])
        selected_category = cols[0].selectbox("By Category", ["All"] + list(sorted(set(g.category for g in st.session_state.goals))))
        selected_priority = cols[1].selectbox("By Priority", ["All", "Urgent", "High", "Medium", "Low"])
        show_completed = cols[2].checkbox("Show Completed", value=False)
        show_overdue = cols[3].checkbox("Show Overdue Only", value=False)
        
        sort_cols = st.columns([3, 1])
        sort_option = sort_cols[0].selectbox("Sort By", [
            "Priority (Urgent first)",
            "Deadline (Closest first)",
            "Deadline (Farthest first)",
            "Progress (Most complete)",
            "Progress (Least complete)",
            "Recently Added",
            "Alphabetical"
        ])
        
        # Apply filters
        filtered_goals = st.session_state.goals
        
        if selected_category != "All":
            filtered_goals = [g for g in filtered_goals if g.category == selected_category]
        
        if selected_priority != "All":
            filtered_goals = [g for g in filtered_goals if g.priority == selected_priority]
        
        if not show_completed:
            filtered_goals = [g for g in filtered_goals if g.get_progress() < 100]
        
        if show_overdue:
            filtered_goals = [g for g in filtered_goals if g.is_overdue()]
        
        # Apply sorting
        if sort_option == "Priority (Urgent first)":
            priority_order = {"Urgent": 0, "High": 1, "Medium": 2, "Low": 3}
            filtered_goals.sort(key=lambda x: priority_order.get(x.priority, 4))
        elif sort_option == "Deadline (Closest first)":
            filtered_goals.sort(key=lambda x: x.deadline)
        elif sort_option == "Deadline (Farthest first)":
            filtered_goals.sort(key=lambda x: x.deadline, reverse=True)
        elif sort_option == "Progress (Most complete)":
            filtered_goals.sort(key=lambda x: x.get_progress(), reverse=True)
        elif sort_option == "Progress (Least complete)":
            filtered_goals.sort(key=lambda x: x.get_progress())
        elif sort_option == "Recently Added":
            filtered_goals.sort(key=lambda x: x.created_at, reverse=True)
        elif sort_option == "Alphabetical":
            filtered_goals.sort(key=lambda x: x.title.lower())
    
    # Goals Display with Enhanced Cards
    if not filtered_goals:
        st.info("🌟 No goals match your filters. Try adjusting your criteria or create a new goal!")
    else:
        for i, goal in enumerate(filtered_goals):
            # Determine card styling
            card_class = ""
            if goal.get_progress() == 100:
                card_class = "completed"
            elif goal.priority == "Urgent":
                card_class = "urgent"
            elif goal.priority == "High":
                card_class = "high"
            elif goal.priority == "Medium":
                card_class = "medium"
            elif goal.priority == "Low":
                card_class = "low"
            
            with st.container():
                st.markdown(f'<div class="goal-card {card_class}">', unsafe_allow_html=True)
                
                # Main goal info
                cols = st.columns([4, 1, 1])
                with cols[0]:
                    # Visual priority indicator
                    priority_icon = {
                        "Urgent": "🔥",
                        "High": "⚠️",
                        "Medium": "📌",
                        "Low": "🌱"
                    }.get(goal.priority, "")
                    
                    st.markdown(f"### {priority_icon} {goal.title}")
                    
                    # Category and deadline info
                    days_left = goal.days_remaining()
                    deadline_status = ""
                    if goal.is_overdue():
                        deadline_status = f"<span style='color:red'>Overdue by {-days_left} days</span>"
                    elif goal.is_deadline_near():
                        deadline_status = f"<span style='color:orange'>Due in {days_left} days</span>"
                    else:
                        deadline_status = f"Due in {days_left} days"
                    
                    st.markdown(f"""
                        <div style="margin-bottom:10px">
                            <span style="background:#f0f0f0; padding:3px 8px; border-radius:12px; font-size:0.8em">
                                {goal.category}
                            </span>
                            <span style="margin-left:10px; font-size:0.9em">
                                {deadline_status}
                            </span>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    # Progress bar with percentage inside
                    progress = goal.get_progress()
                    st.markdown(f"""
                        <div style="margin:10px 0; position:relative; height:24px; background:#f0f0f0; border-radius:12px">
                            <div style="width:{progress}%; height:100%; background:#4CAF50; border-radius:12px; display:flex; align-items:center; justify-content:center; color:white; font-weight:bold; font-size:0.8em">
                                {progress}%
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    # Description preview
                    if goal.description:
                        with st.expander("📝 View Details"):
                            st.write(goal.description)
                
                # Action buttons
                with cols[1]:
                    if st.button("✏️ Edit", key=f"edit_{i}", use_container_width=True):
                        st.session_state.selected_goal_index = st.session_state.goals.index(goal)
                
                with cols[2]:
                    if st.button("🗑️ Delete", key=f"delete_{i}", use_container_width=True):
                        st.session_state.goals.remove(goal)
                        st.rerun()
                
                st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------
# Goal Management Section
# ---------------------------

if 'selected_goal_index' in st.session_state and st.session_state.selected_goal_index is not None:
    selected_goal = st.session_state.goals[st.session_state.selected_goal_index]
    
    st.subheader(f"📝 Managing Goal: {selected_goal.title}")
    
    with st.expander("Goal Details", expanded=True):
        cols = st.columns(2)
        with cols[0]:
            new_title = st.text_input("Title", value=selected_goal.title, key="edit_title")
            new_description = st.text_area("Description", value=selected_goal.description, key="edit_desc")
        
        with cols[1]:
            new_deadline = st.date_input("Deadline", value=selected_goal.deadline, key="edit_deadline")
            new_priority = st.selectbox("Priority", ["Urgent", "High", "Medium", "Low"], 
                                     index=["Urgent", "High", "Medium", "Low"].index(selected_goal.priority),
                                     key="edit_priority")
        
        if st.button("Update Goal"):
            selected_goal.title = new_title
            selected_goal.description = new_description
            selected_goal.deadline = new_deadline
            selected_goal.priority = new_priority
            st.success("Goal updated successfully!")
            st.session_state.selected_goal_index = None
            st.rerun()
    
    # Milestone Management
    st.subheader("📋 Milestones")
    
    # Add Milestone - using form submit button which is allowed
    with st.form("add_milestone"):
        cols = st.columns([4, 1])
        milestone_name = cols[0].text_input("New Milestone", placeholder="What's the next step?", key="new_milestone")
        add_milestone = cols[1].form_submit_button("➕ Add", use_container_width=True)
        
        if add_milestone and milestone_name:
            selected_goal.add_milestone(Milestone(milestone_name))
            st.rerun()
    
    # Display Milestones
    if selected_goal.milestones:
        for i, milestone in enumerate(selected_goal.milestones):
            cols = st.columns([1, 6, 1, 1])
            with cols[0]:
                completed = st.checkbox("", value=milestone.completed, key=f"complete_{i}", label_visibility="hidden")
                if completed:
                    milestone.mark_complete()
                else:
                    milestone.completed = False
            
            with cols[1]:
                if milestone.completed:
                    st.markdown(f'<div class="milestone-completed">{milestone.name}</div>', unsafe_allow_html=True)
                else:
                    new_name = st.text_input("", value=milestone.name, key=f"name_{i}", label_visibility="hidden")
                    milestone.update_name(new_name)
            
            with cols[2]:
                st.caption(milestone.created_at.strftime("%b %d"))
            
            with cols[3]:
                if st.button("❌", key=f"delete_milestone_{i}"):
                    selected_goal.delete_milestone(i)
                    st.rerun()
    else:
        st.info("No milestones added yet. Break your goal into smaller steps to make progress!")
    
    # Back button
    if st.button("← Back to All Goals"):
        st.session_state.selected_goal_index = None
        st.rerun()

# ---------------------------
# Pomodoro Timer Section
# ---------------------------

st.markdown("---")
st.subheader("⏰ Productivity Timer")

tab1, tab2 = st.tabs(["🍅 Pomodoro Timer", "⏱️ Custom Timer"])

with tab1:
    if "pomo_start_time" not in st.session_state:
        st.session_state.pomo_start_time = None
        st.session_state.pomo_state = "idle"  # idle, work, break
        st.session_state.pomo_cycles = 0
    
    cols = st.columns(2)
    work_min = cols[0].number_input("Work Duration (minutes)", min_value=1, value=25, help="Traditional Pomodoro is 25 minutes")
    break_min = cols[1].number_input("Break Duration (minutes)", min_value=1, value=5, help="Traditional break is 5 minutes")
    
    cols = st.columns(3)
    start_pomo = cols[0].button("▶️ Start Work", use_container_width=True)
    pause_pomo = cols[1].button("⏸️ Pause", use_container_width=True)
    reset_pomo = cols[2].button("🔄 Reset", use_container_width=True)
    
    if start_pomo and st.session_state.pomo_state == "idle":
        st.session_state.pomo_start_time = datetime.now()
        st.session_state.pomo_state = "work"
        st.session_state.pomo_cycles += 1
    
    if pause_pomo and st.session_state.pomo_state in ["work", "break"]:
        st.session_state.pomo_state = "paused"
        st.session_state.pomo_pause_time = datetime.now()
    
    if reset_pomo:
        st.session_state.pomo_state = "idle"
        st.session_state.pomo_start_time = None
    
    # Timer Display
    timer_placeholder = st.empty()
    
    if st.session_state.pomo_state != "idle":
        if st.session_state.pomo_state == "paused":
            elapsed = st.session_state.pomo_pause_time - st.session_state.pomo_start_time
            timer_placeholder.markdown(f"""
                <div class="timer-display">
                    ⏸️ Paused | Session {st.session_state.pomo_cycles}
                </div>
            """, unsafe_allow_html=True)
        else:
            elapsed = datetime.now() - st.session_state.pomo_start_time
            
            if st.session_state.pomo_state == "work":
                total_seconds = work_min * 60
                if elapsed.total_seconds() < total_seconds:
                    remaining = total_seconds - elapsed.total_seconds()
                    mins = int(remaining // 60)
                    secs = int(remaining % 60)
                    timer_placeholder.markdown(f"""
                        <div class="timer-display work-mode">
                            🍅 {mins:02}:{secs:02} | Work Session {st.session_state.pomo_cycles}
                        </div>
                    """, unsafe_allow_html=True)
                else:
                    st.session_state.pomo_state = "break"
                    st.session_state.pomo_start_time = datetime.now()
                    st.balloons()
                    st.success("Work session complete! Time for a break.")
            elif st.session_state.pomo_state == "break":
                total_seconds = break_min * 60
                if elapsed.total_seconds() < total_seconds:
                    remaining = total_seconds - elapsed.total_seconds()
                    mins = int(remaining // 60)
                    secs = int(remaining % 60)
                    timer_placeholder.markdown(f"""
                        <div class="timer-display break-mode">
                            ☕ {mins:02}:{secs:02} | Break Time
                        </div>
                    """, unsafe_allow_html=True)
                else:
                    st.session_state.pomo_state = "work"
                    st.session_state.pomo_start_time = datetime.now()
                    st.session_state.pomo_cycles += 1
                    st.balloons()
                    st.success("Break over! Time to get back to work.")
    else:
        timer_placeholder.markdown("""
            <div class="timer-display">
                ⏱️ Ready to start your Pomodoro session!
            </div>
        """, unsafe_allow_html=True)

with tab2:
    custom_min = st.number_input("Timer Duration (minutes)", min_value=1, value=30)
    
    if "custom_start_time" not in st.session_state:
        st.session_state.custom_start_time = None
        st.session_state.custom_state = "idle"
    
    cols = st.columns(3)
    start_custom = cols[0].button("▶️ Start Timer", use_container_width=True)
    pause_custom = cols[1].button("⏸️ Pause Timer", use_container_width=True)
    reset_custom = cols[2].button("🔄 Reset Timer", use_container_width=True)
    
    if start_custom and st.session_state.custom_state == "idle":
        st.session_state.custom_start_time = datetime.now()
        st.session_state.custom_state = "running"
    
    if pause_custom and st.session_state.custom_state == "running":
        st.session_state.custom_state = "paused"
        st.session_state.custom_pause_time = datetime.now()
    
    if reset_custom:
        st.session_state.custom_state = "idle"
        st.session_state.custom_start_time = None
    
    # Timer Display
    custom_timer_placeholder = st.empty()
    
    if st.session_state.custom_state != "idle":
        if st.session_state.custom_state == "paused":
            elapsed = st.session_state.custom_pause_time - st.session_state.custom_start_time
            custom_timer_placeholder.markdown("""
                <div class="timer-display">
                    ⏸️ Timer Paused
                </div>
            """, unsafe_allow_html=True)
        else:
            elapsed = datetime.now() - st.session_state.custom_start_time
            total_seconds = custom_min * 60
            
            if elapsed.total_seconds() < total_seconds:
                remaining = total_seconds - elapsed.total_seconds()
                mins = int(remaining // 60)
                secs = int(remaining % 60)
                custom_timer_placeholder.markdown(f"""
                    <div class="timer-display">
                        ⏱️ {mins:02}:{secs:02} remaining
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.session_state.custom_state = "idle"
                custom_timer_placeholder.markdown("""
                    <div class="timer-display">
                        ✅ Timer Complete!
                    </div>
                """, unsafe_allow_html=True)
                st.balloons()
    else:
        custom_timer_placeholder.markdown("""
            <div class="timer-display">
                ⏱️ Set your custom timer duration
            </div>
        """, unsafe_allow_html=True)

# ---------------------------
# Footer
# ---------------------------
st.markdown("---")
st.markdown("""
    <div style="text-align: center; color: grey; padding: 10px; font-size: 0.9em;">
    Goal Tracker Pro+ © 2023 | Stay Productive and Achieve Your Dreams!
    </div>
    """, unsafe_allow_html=True)