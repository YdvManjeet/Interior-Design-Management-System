import os
import pandas as pd
import matplotlib.pyplot as plt
from IPython.display import display


def load_data():
    global designers, projects

    if os.path.exists("designers.csv"):
        designers = pd.read_csv("designers.csv").to_dict('records')
    else:
        designers = []

    if os.path.exists("projects.csv"):
        projects = pd.read_csv("projects.csv").to_dict('records')
    else:
        projects = []

    # Ensure each designer has an 'id'
    max_id = 0
    for d in designers:
        if 'id' in d and pd.notna(d['id']):
            try:
                val = int(d['id'])
                if val > max_id:
                    max_id = val
            except:
                pass
    next_id = max_id + 1
    for d in designers:
        if 'id' not in d or pd.isna(d['id']):
            d['id'] = next_id
            next_id += 1

    # Ensure each project has a 'project_id'
    max_pid = 0
    for p in projects:
        if 'project_id' in p and pd.notna(p['project_id']):
            try:
                val = int(p['project_id'])
                if val > max_pid:
                    max_pid = val
            except:
                pass
    next_pid = max_pid + 1
    for p in projects:
        if 'project_id' not in p or pd.isna(p['project_id']):
            p['project_id'] = next_pid
            next_pid += 1


# Call loader at start
load_data()


def save_to_csv():
    pd.DataFrame(designers).to_csv("designers.csv", index=False)
    pd.DataFrame(projects).to_csv("projects.csv", index=False)
    print("✔ Data saved successfully!\n")


def input_int(prompt, min_val=None):
    while True:
        value = input(prompt)
        try:
            num = int(value)
            if min_val is not None and num < min_val:
                print(f"Value must be at least {min_val}. Try again.")
                continue
            return num
        except ValueError:
            print("Please enter a valid integer.")

def input_float(prompt, min_val=None):
    while True:
        value = input(prompt)
        try:
            num = float(value)
            if min_val is not None and num < min_val:
                print(f"Value must be at least {min_val}. Try again.")
                continue
            return num
        except ValueError:
            print("Please enter a valid number.")


def get_next_designer_id():
    if not designers:
        return 1
    return max(int(d.get("id", 0)) for d in designers) + 1

def get_next_project_id():
    if not projects:
        return 1
    return max(int(p.get("project_id", 0)) for p in projects) + 1

def add_designer():
    print("\n--- Add Designer ---")
    name = input("Enter designer name: ")
    experience = input_int("Enter experience (years): ", min_val=0)
    specialization = input("Enter specialization (Modern/Classic/etc): ")

    designer = {
        "id": get_next_designer_id(),
        "name": name,
        "experience": experience,
        "specialization": specialization
    }
    designers.append(designer)
    save_to_csv()
    print("✔ Designer added!\n")

def add_project():
    print("\n--- Add Project ---")
    project_name = input("Project name: ")
    client = input("Client name: ")
    designer_name = input("Designer name: ")
    budget = input_float("Enter budget: ", min_val=0)

    project = {
        "project_id": get_next_project_id(),
        "project_name": project_name,
        "client": client,
        "designer": designer_name,
        "budget": budget
    }
    projects.append(project)
    save_to_csv()
    print("✔ Project added!\n")

def view_designers():
    print("\n--- Designers List ---")
    if designers:
        df = pd.DataFrame(designers)
        df = df[["id", "name", "experience", "specialization"]]
        display(df)
    else:
        print("⚠ No designers found!\n")

def view_projects():
    print("\n--- Projects List ---")
    if projects:
        df = pd.DataFrame(projects)
        df = df[["project_id", "project_name", "client", "designer", "budget"]]
        display(df)
    else:
        print("⚠ No projects found!\n")

def search_project_by_designer():
    print("\n--- Search Project by Designer ---")
    name = input("Enter designer name: ").strip().lower()
    df = pd.DataFrame(projects)
    if df.empty:
        print("⚠ No projects found!\n")
        return
    result = df[df['designer'].str.lower() == name]
    if not result.empty:
        display(result[["project_id", "project_name", "client", "designer", "budget"]])
    else:
        print("⚠ No projects found for this designer!\n")

def delete_project():
    print("\n--- Delete Project ---")
    global projects  # must be at top

    if not projects:
        print("⚠ No projects to delete!\n")
        return

    view_projects()
    pid = input_int("Enter Project ID to delete: ", min_val=1)

    before = len(projects)
    projects = [p for p in projects if int(p.get("project_id", -1)) != pid]
    after = len(projects)

    if before == after:
        print("⚠ Project not found!\n")
    else:
        save_to_csv()
        print("✔ Project deleted!\n")



def find_designer_by_id(did):
    for d in designers:
        try:
            if int(d.get("id", -1)) == did:
                return d
        except:
            continue
    return None

def find_project_by_id(pid):
    for p in projects:
        try:
            if int(p.get("project_id", -1)) == pid:
                return p
        except:
            continue
    return None

def update_designer():
    print("\n--- Update Designer ---")
    if not designers:
        print("⚠ No designers to update!\n")
        return

    view_designers()
    did = input_int("Enter Designer ID to update: ", min_val=1)

    designer = find_designer_by_id(did)
    if not designer:
        print("⚠ Designer not found!\n")
        return

    print("Press Enter to keep existing value.")

    new_name = input(f"New name (current: {designer['name']}): ").strip()
    if new_name:
        designer['name'] = new_name

    exp_input = input(f"New experience (current: {designer['experience']}): ").strip()
    if exp_input:
        try:
            designer['experience'] = int(exp_input)
        except ValueError:
            print("Invalid experience entered. Keeping old value.")

    new_spec = input(f"New specialization (current: {designer['specialization']}): ").strip()
    if new_spec:
        designer['specialization'] = new_spec

    save_to_csv()
    print("✔ Designer updated!\n")

def update_project():
    print("\n--- Update Project ---")
    if not projects:
        print("⚠ No projects to update!\n")
        return

    view_projects()
    pid = input_int("Enter Project ID to update: ", min_val=1)

    project = find_project_by_id(pid)
    if not project:
        print("⚠ Project not found!\n")
        return

    print("Press Enter to keep existing value.")

    new_name = input(f"New project name (current: {project['project_name']}): ").strip()
    if new_name:
        project['project_name'] = new_name

    new_client = input(f"New client name (current: {project['client']}): ").strip()
    if new_client:
        project['client'] = new_client

    new_designer = input(f"New designer name (current: {project['designer']}): ").strip()
    if new_designer:
        project['designer'] = new_designer

    budget_input = input(f"New budget (current: {project['budget']}): ").strip()
    if budget_input:
        try:
            project['budget'] = float(budget_input)
        except ValueError:
            print("Invalid budget entered. Keeping old value.")

    save_to_csv()
    print("✔ Project updated!\n")

def sort_designers_by_experience():
    print("\n--- Sort Designers by Experience ---")
    if not designers:
        print("⚠ No designers to sort!\n")
        return

    designers.sort(key=lambda d: int(d.get("experience", 0)))
    save_to_csv()
    print("✔ Designers sorted by experience (ascending).")
    view_designers()

def sort_projects_by_budget():
    print("\n--- Sort Projects by Budget ---")
    if not projects:
        print("⚠ No projects to sort!\n")
        return

    projects.sort(key=lambda p: float(p.get("budget", 0)))
    save_to_csv()
    print("✔ Projects sorted by budget (ascending).")
    view_projects()


def plot_budget_bar_chart():
    print("\n--- Budget Bar Chart ---")
    if not projects:
        print("⚠ No projects available for chart!\n")
        return

    df = pd.DataFrame(projects)
    plt.figure(figsize=(9, 5))
    plt.bar(df['project_name'], df['budget'])
    plt.xlabel("Project Name")
    plt.ylabel("Budget")
    plt.title("Interior Design Project Budgets")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def plot_budget_pie_chart():
    print("\n--- Budget Share Pie Chart (by Designer) ---")
    if not projects:
        print("⚠ No projects available for chart!\n")
        return

    df = pd.DataFrame(projects)
    grouped = df.groupby('designer')['budget'].sum()

    plt.figure(figsize=(7, 7))
    plt.pie(grouped.values, labels=grouped.index, autopct='%1.1f%%', startangle=90)
    plt.title("Budget Share by Designer")
    plt.tight_layout()
    plt.show()

def plot_projects_per_designer():
    print("\n--- Projects per Designer Chart ---")
    if not projects:
        print("⚠ No projects available for chart!\n")
        return

    df = pd.DataFrame(projects)
    counts = df['designer'].value_counts()

    plt.figure(figsize=(8, 5))
    plt.bar(counts.index, counts.values)
    plt.xlabel("Designer")
    plt.ylabel("Number of Projects")
    plt.title("Projects per Designer")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def plot_budget_histogram():
    print("\n--- Budget Distribution Histogram ---")
    if not projects:
        print("⚠ No projects available for chart!\n")
        return

    df = pd.DataFrame(projects)
    plt.figure(figsize=(8, 5))
    plt.hist(df['budget'], bins=5)
    plt.xlabel("Budget")
    plt.ylabel("Number of Projects")
    plt.title("Distribution of Project Budgets")
    plt.tight_layout()
    plt.show()

def plot_top_n_projects_by_budget():
    print("\n--- Top N Projects by Budget ---")
    if not projects:
        print("⚠ No projects available for chart!\n")
        return

    n = input_int("Enter N (how many top projects): ", min_val=1)
    df = pd.DataFrame(projects)
    df_sorted = df.sort_values(by='budget', ascending=False).head(n)

    plt.figure(figsize=(9, 5))
    plt.bar(df_sorted['project_name'], df_sorted['budget'])
    plt.xlabel("Project Name")
    plt.ylabel("Budget")
    plt.title(f"Top {len(df_sorted)} Projects by Budget")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def plot_experience_vs_total_budget():
    print("\n--- Designer Experience vs Total Budget ---")
    if not projects or not designers:
        print("⚠ Need both designers and projects for this chart!\n")
        return

    df_proj = pd.DataFrame(projects)
    budgets_by_designer = df_proj.groupby('designer')['budget'].sum().reset_index()

    df_des = pd.DataFrame(designers)
    merged = pd.merge(df_des, budgets_by_designer, left_on='name', right_on='designer', how='inner')

    if merged.empty:
        print("⚠ No matching designer names between designers.csv and projects.csv\n")
        return

    plt.figure(figsize=(8, 5))
    plt.scatter(merged['experience'], merged['budget'])
    for idx, row in merged.iterrows():
        plt.text(row['experience'], row['budget'], row['name'], fontsize=8)
    plt.xlabel("Designer Experience (years)")
    plt.ylabel("Total Project Budget")
    plt.title("Experience vs Total Budget Managed")
    plt.tight_layout()
    plt.show()



def menu():
    while True:
        print("""
=========== INTERIOR DESIGN MANAGEMENT SYSTEM ===========
1.  Add Designer
2.  Add Project
3.  View All Designers
4.  View All Projects
5.  Search Project by Designer
6.  Delete Project
7.  Show Budget Bar Chart (per project)
8.  Show Budget Share Pie Chart (by designer)
9.  Show Projects per Designer Bar Chart
10. Update Designer
11. Update Project
12. Sort Designers by Experience
13. Sort Projects by Budget
14. Budget Distribution Histogram
15. Top N Projects by Budget
16. Experience vs Total Budget (scatter)
17. Exit
""")
        choice = input("Enter your choice: ").strip()

        if choice == '1':
            add_designer()
        elif choice == '2':
            add_project()
        elif choice == '3':
            view_designers()
        elif choice == '4':
            view_projects()
        elif choice == '5':
            search_project_by_designer()
        elif choice == '6':
            delete_project()
        elif choice == '7':
            plot_budget_bar_chart()
        elif choice == '8':
            plot_budget_pie_chart()
        elif choice == '9':
            plot_projects_per_designer()
        elif choice == '10':
            update_designer()
        elif choice == '11':
            update_project()
        elif choice == '12':
            sort_designers_by_experience()
        elif choice == '13':
            sort_projects_by_budget()
        elif choice == '14':
            plot_budget_histogram()
        elif choice == '15':
            plot_top_n_projects_by_budget()
        elif choice == '16':
            plot_experience_vs_total_budget()
        elif choice == '17':
            print("👋 Exiting program... Goodbye!")
            break
        else:
            print("❌ Invalid choice! Try again.\n")



menu()
