"""
Simple Task Manager - Practice DevOps Project
A basic command-line task management application
"""

import json
import os
from datetime import datetime


class TaskManager:
    """Simple task manager with file persistence"""
    
    def __init__(self, filename="tasks.json"):
        self.filename = filename
        self.tasks = self.load_tasks()
    
    def load_tasks(self):
        """Load tasks from file"""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r') as f:
                    return json.load(f)
            except:
                return []
        return []
    
    def save_tasks(self):
        """Save tasks to file"""
        with open(self.filename, 'w') as f:
            json.dump(self.tasks, f, indent=2)
    
    def add_task(self, title, description=""):
        """Add a new task"""
        if not title:
            raise ValueError("Task title cannot be empty")
        
        task = {
            "id": len(self.tasks) + 1,
            "title": title,
            "description": description,
            "completed": False,
            "created_at": datetime.now().isoformat()
        }
        self.tasks.append(task)
        self.save_tasks()
        return task
    
    def list_tasks(self, show_completed=True):
        """List all tasks"""
        if show_completed:
            return self.tasks
        return [task for task in self.tasks if not task["completed"]]
    
    def complete_task(self, task_id):
        """Mark a task as completed"""
        for task in self.tasks:
            if task["id"] == task_id:
                task["completed"] = True
                task["completed_at"] = datetime.now().isoformat()
                self.save_tasks()
                return task
        raise ValueError(f"Task with id {task_id} not found")
    
    def delete_task(self, task_id):
        """Delete a task"""
        for i, task in enumerate(self.tasks):
            if task["id"] == task_id:
                deleted_task = self.tasks.pop(i)
                self.save_tasks()
                return deleted_task
        raise ValueError(f"Task with id {task_id} not found")
    
    def get_task_count(self):
        """Get total number of tasks"""
        return len(self.tasks)
    
    def get_completed_count(self):
        """Get number of completed tasks"""
        return sum(1 for task in self.tasks if task["completed"])


def main():
    """Main CLI interface"""
    tm = TaskManager()
    
    print("=" * 50)
    print("📝 Simple Task Manager")
    print("=" * 50)
    
    while True:
        print("\nOptions:")
        print("1. Add task")
        print("2. List tasks")
        print("3. Complete task")
        print("4. Delete task")
        print("5. Statistics")
        print("6. Exit")
        
        choice = input("\nEnter choice (1-6): ").strip()
        
        if choice == "1":
            title = input("Task title: ").strip()
            description = input("Description (optional): ").strip()
            try:
                task = tm.add_task(title, description)
                print(f"✓ Added task #{task['id']}: {task['title']}")
            except ValueError as e:
                print(f"✗ Error: {e}")
        
        elif choice == "2":
            tasks = tm.list_tasks()
            if not tasks:
                print("No tasks found.")
            else:
                print("\n📋 Your Tasks:")
                for task in tasks:
                    status = "✓" if task["completed"] else " "
                    print(f"  [{status}] #{task['id']}: {task['title']}")
                    if task["description"]:
                        print(f"      {task['description']}")
        
        elif choice == "3":
            try:
                task_id = int(input("Task ID to complete: "))
                task = tm.complete_task(task_id)
                print(f"✓ Completed: {task['title']}")
            except ValueError as e:
                print(f"✗ Error: {e}")
        
        elif choice == "4":
            try:
                task_id = int(input("Task ID to delete: "))
                task = tm.delete_task(task_id)
                print(f"✓ Deleted: {task['title']}")
            except ValueError as e:
                print(f"✗ Error: {e}")
        
        elif choice == "5":
            total = tm.get_task_count()
            completed = tm.get_completed_count()
            pending = total - completed
            print(f"\n📊 Statistics:")
            print(f"   Total tasks: {total}")
            print(f"   Completed: {completed}")
            print(f"   Pending: {pending}")
        
        elif choice == "6":
            print("Goodbye! 👋")
            break
        
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()