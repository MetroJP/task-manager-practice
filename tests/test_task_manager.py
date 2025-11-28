"""
Tests for Task Manager
"""
import pytest
import sys
import os
import json
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from task_manager import TaskManager


@pytest.fixture
def tm():
    """Create a temporary task manager for testing"""
    # Use a test file that gets cleaned up
    tm = TaskManager("test_tasks.json")
    yield tm
    # Cleanup
    if os.path.exists("test_tasks.json"):
        os.remove("test_tasks.json")


def test_add_task(tm):
    """Test adding a task"""
    task = tm.add_task("Test task", "Test description")
    assert task["title"] == "Test task"
    assert task["description"] == "Test description"
    assert task["completed"] == False
    assert task["id"] == 1


def test_add_task_without_title(tm):
    """Test that adding task without title raises error"""
    with pytest.raises(ValueError):
        tm.add_task("")


def test_list_tasks(tm):
    """Test listing tasks"""
    tm.add_task("Task 1")
    tm.add_task("Task 2")
    tasks = tm.list_tasks()
    assert len(tasks) == 2


def test_complete_task(tm):
    """Test completing a task"""
    task = tm.add_task("Test task")
    completed = tm.complete_task(task["id"])
    assert completed["completed"] == True
    assert "completed_at" in completed


def test_complete_nonexistent_task(tm):
    """Test completing a task that doesn't exist"""
    with pytest.raises(ValueError):
        tm.complete_task(999)


def test_delete_task(tm):
    """Test deleting a task"""
    task = tm.add_task("Test task")
    deleted = tm.delete_task(task["id"])
    assert deleted["id"] == task["id"]
    assert len(tm.list_tasks()) == 0


def test_delete_nonexistent_task(tm):
    """Test deleting a task that doesn't exist"""
    with pytest.raises(ValueError):
        tm.delete_task(999)


def test_get_task_count(tm):
    """Test getting task count"""
    assert tm.get_task_count() == 0
    tm.add_task("Task 1")
    tm.add_task("Task 2")
    assert tm.get_task_count() == 2


def test_get_completed_count(tm):
    """Test getting completed task count"""
    task1 = tm.add_task("Task 1")
    task2 = tm.add_task("Task 2")
    assert tm.get_completed_count() == 0
    
    tm.complete_task(task1["id"])
    assert tm.get_completed_count() == 1
    
    tm.complete_task(task2["id"])
    assert tm.get_completed_count() == 2


def test_persistence(tm):
    """Test that tasks are saved and loaded correctly"""
    tm.add_task("Persistent task")
    
    # Create new instance with same file
    tm2 = TaskManager("test_tasks.json")
    tasks = tm2.list_tasks()
    assert len(tasks) == 1
    assert tasks[0]["title"] == "Persistent task"


def test_list_tasks_filter_completed(tm):
    """Test filtering completed tasks"""
    task1 = tm.add_task("Task 1")
    task2 = tm.add_task("Task 2")
    tm.complete_task(task1["id"])
    
    # Show all
    all_tasks = tm.list_tasks(show_completed=True)
    assert len(all_tasks) == 2
    
    # Show only pending
    pending_tasks = tm.list_tasks(show_completed=False)
    assert len(pending_tasks) == 1
    assert pending_tasks[0]["id"] == task2["id"]