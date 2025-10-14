#!/usr/bin/env python3
"""
Bucket Management Implementation Verification Script

Validates that all bucket management components are properly implemented.
"""

import os
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))


def check_file_exists(filepath: str, description: str) -> bool:
    """Check if a file exists"""
    path = project_root / filepath
    exists = path.exists()
    status = "✓" if exists else "✗"
    print(f"{status} {description}: {filepath}")
    return exists


def check_function_exists(module_path: str, function_name: str, description: str) -> bool:
    """Check if a function exists in a module"""
    try:
        module_parts = module_path.split(".")
        module = __import__(module_path)
        for part in module_parts[1:]:
            module = getattr(module, part)

        has_function = hasattr(module, function_name)
        status = "✓" if has_function else "✗"
        print(f"{status} {description}: {module_path}.{function_name}")
        return has_function
    except ImportError as e:
        print(f"✗ {description}: Import error - {e}")
        return False


def main():
    """Run all verification checks"""
    print("=" * 60)
    print("Bucket Management Implementation Verification")
    print("=" * 60)

    results = []

    # Documentation
    print("\n📄 Documentation Files:")
    results.append(check_file_exists("0-docs/bucket-management/001-context.md", "Context doc"))
    results.append(check_file_exists("0-docs/bucket-management/002-decisions.md", "Decisions doc"))
    results.append(check_file_exists("0-docs/bucket-management/003-spec.md", "Spec doc"))
    results.append(check_file_exists("0-docs/bucket-management/README.md", "README"))

    # Core Python Modules
    print("\n🐍 Core Python Modules:")
    results.append(check_file_exists("planner_lib/bucket_create.py", "Bucket create module"))
    results.append(check_file_exists("planner_lib/bucket_delete.py", "Bucket delete module"))
    results.append(check_file_exists("planner_lib/bucket_update.py", "Bucket update module"))
    results.append(check_file_exists("planner_lib/bucket_move.py", "Bucket move module"))
    results.append(check_file_exists("planner_lib/cli_bucket_commands.py", "CLI commands module"))

    # Functions in modules
    print("\n🔧 Core Functions:")
    results.append(check_function_exists("planner_lib.bucket_create", "create_bucket_op", "Create function"))
    results.append(check_function_exists("planner_lib.bucket_delete", "delete_bucket_op", "Delete function"))
    results.append(check_function_exists("planner_lib.bucket_update", "update_bucket_op", "Update function"))
    results.append(check_function_exists("planner_lib.bucket_move", "move_bucket_tasks_op", "Move function"))
    results.append(check_function_exists("planner_lib.graph_client", "delete_json", "Graph delete_json"))

    # CLI Registration
    print("\n⌨️  CLI Commands:")
    results.append(check_function_exists("planner_lib.cli_bucket_commands", "create_bucket_cmd", "Create command"))
    results.append(check_function_exists("planner_lib.cli_bucket_commands", "delete_bucket_cmd", "Delete command"))
    results.append(check_function_exists("planner_lib.cli_bucket_commands", "rename_bucket_cmd", "Rename command"))
    results.append(check_function_exists("planner_lib.cli_bucket_commands", "move_bucket_tasks_cmd", "Move command"))
    results.append(check_function_exists("planner_lib.cli_bucket_commands", "register_bucket_commands", "Register function"))

    # MCP Server Files
    print("\n🌐 MCP Server Files:")
    results.append(check_file_exists("src/server/handlers-buckets.ts", "Bucket handlers"))
    results.append(check_file_exists("src/server/tools.ts", "Tools definitions"))
    results.append(check_file_exists("src/server/handlers.ts", "Main handlers"))

    # Test Files
    print("\n🧪 Test Files:")
    results.append(check_file_exists("tests/test_bucket_operations/__init__.py", "Test module init"))
    results.append(check_file_exists("tests/test_bucket_operations/test_bucket_create.py", "Create tests"))
    results.append(check_file_exists("tests/test_bucket_operations/test_bucket_delete.py", "Delete tests"))
    results.append(check_file_exists("tests/test_bucket_operations/test_bucket_update.py", "Update tests"))
    results.append(check_file_exists("tests/test_bucket_operations/test_bucket_move.py", "Move tests"))
    results.append(check_file_exists("tests/test_cli_bucket_operations.py", "CLI integration tests"))

    # Summary
    print("\n" + "=" * 60)
    total = len(results)
    passed = sum(results)
    failed = total - passed

    print(f"Results: {passed}/{total} checks passed")

    if failed > 0:
        print(f"❌ {failed} checks failed")
        return 1
    else:
        print("✅ All checks passed!")
        print("\n📋 Manual Testing Checklist:")
        print("  1. Run unit tests: pytest tests/test_bucket_operations/")
        print("  2. Run CLI integration tests: pytest tests/test_cli_bucket_operations.py")
        print("  3. Test CLI commands manually (after authentication)")
        print("  4. Test MCP tools via Cursor")
        print("  5. Build TypeScript: npm run build")
        return 0


if __name__ == "__main__":
    sys.exit(main())
