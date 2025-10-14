#!/usr/bin/env python3
"""
Verification script for find task enhancements
Demonstrates that new functions are importable and have correct signatures.
"""

import inspect
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))


def verify_imports():
    """Verify functions can be imported"""
    print("✓ Testing imports...")
    
    try:
        from planner_lib import get_task_details, find_task_by_title
        print("  ✓ Direct import from planner_lib works")
    except ImportError as e:
        print(f"  ✗ Failed to import from planner_lib: {e}")
        return False
    
    try:
        from planner_lib.task_operations import get_task_details, find_task_by_title
        print("  ✓ Direct import from task_operations works")
    except ImportError as e:
        print(f"  ✗ Failed to import from task_operations: {e}")
        return False
    
    return True


def verify_signatures():
    """Verify function signatures are correct"""
    print("\n✓ Testing function signatures...")
    
    from planner_lib.task_operations import get_task_details, find_task_by_title
    
    # Check get_task_details signature
    sig = inspect.signature(get_task_details)
    params = list(sig.parameters.keys())
    
    if params == ['task_id', 'token']:
        print("  ✓ get_task_details signature correct: (task_id, token)")
    else:
        print(f"  ✗ get_task_details signature wrong: {params}")
        return False
    
    # Check find_task_by_title signature
    sig = inspect.signature(find_task_by_title)
    params = list(sig.parameters.keys())
    
    if params == ['title', 'plan_id', 'token']:
        print("  ✓ find_task_by_title signature correct: (title, plan_id, token)")
    else:
        print(f"  ✗ find_task_by_title signature wrong: {params}")
        return False
    
    return True


def verify_docstrings():
    """Verify functions have proper documentation"""
    print("\n✓ Testing docstrings...")
    
    from planner_lib.task_operations import get_task_details, find_task_by_title
    
    if get_task_details.__doc__ and "Fetch task details by task ID" in get_task_details.__doc__:
        print("  ✓ get_task_details has proper docstring")
    else:
        print("  ✗ get_task_details missing or incorrect docstring")
        return False
    
    if find_task_by_title.__doc__ and "Find task by title within a plan" in find_task_by_title.__doc__:
        print("  ✓ find_task_by_title has proper docstring")
    else:
        print("  ✗ find_task_by_title missing or incorrect docstring")
        return False
    
    return True


def verify_exports():
    """Verify functions are exported in __all__"""
    print("\n✓ Testing module exports...")
    
    from planner_lib import task_management
    
    if 'get_task_details' in task_management.__all__:
        print("  ✓ get_task_details in task_management.__all__")
    else:
        print("  ✗ get_task_details not in task_management.__all__")
        return False
    
    if 'find_task_by_title' in task_management.__all__:
        print("  ✓ find_task_by_title in task_management.__all__")
    else:
        print("  ✗ find_task_by_title not in task_management.__all__")
        return False
    
    return True


def verify_backward_compatibility():
    """Verify existing functions still work"""
    print("\n✓ Testing backward compatibility...")
    
    try:
        from planner_lib.task_operations import resolve_task, list_tasks
        print("  ✓ resolve_task still importable")
        print("  ✓ list_tasks still importable")
    except ImportError as e:
        print(f"  ✗ Backward compatibility broken: {e}")
        return False
    
    return True


def main():
    """Run all verification checks"""
    print("=" * 60)
    print("Find Task Enhancements - Implementation Verification")
    print("=" * 60)
    
    checks = [
        verify_imports,
        verify_signatures,
        verify_docstrings,
        verify_exports,
        verify_backward_compatibility
    ]
    
    results = []
    for check in checks:
        results.append(check())
    
    print("\n" + "=" * 60)
    if all(results):
        print("✅ ALL CHECKS PASSED")
        print("=" * 60)
        return 0
    else:
        print("❌ SOME CHECKS FAILED")
        print("=" * 60)
        return 1


if __name__ == "__main__":
    sys.exit(main())

