import subprocess
import os
import shutil
import sys

########################
# HELPER FUNCTION FOR WORKING DIRECTORY AND PACKAGE PATHS
########################

def connect_paths(project_name: str, working_dir: str, paths: dict[str, str], package_path: str):
    connecting_path = paths.get(project_name.lower())
    file_path = package_path.replace('.', '/') + '.java'
    full_path = os.path.join(working_dir, connecting_path, file_path)
    return full_path


########################
# HELPER FUNCTIONS FOR RUN_DEFECTS4J_TEST
########################

def checkout_defects4j_project(project_name: str, version: str, working_dir: str):
    """Checkout a Defects4J project to create the working directory with buggy code.
    
    Parameters:
    - project_name (str): Project name (e.g., 'Chart', 'Closure', 'Lang')
    - version (str): Bug version (e.g., '2b', '3f', '1b')
    - working_dir (str): Absolute path where to create the project
    
    Returns:
    - bool: True if checkout successful, False otherwise
    """
    try:
        # Run the checkout command
        result = subprocess.run(
            ['defects4j', 'checkout', '-p', project_name, '-v', version + 'b', '-w', working_dir],
            capture_output=True,
            text=True,
        )
        
        if result.returncode == 0:
            return True
        else:
            print(f"Failed to checkout project: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"Error during checkout: {e}")
        return False


# Replace a buggy file (target_file_path) with the patched program (java_file)
def apply_java_file_patch(java_file: str, target_file_path: str):
    try:
        # Copy the Java file to the target location
        shutil.copy2(java_file, target_file_path)
        return True
    except Exception as e:
        print(f"Error applying Java file patch: {e}")
        return False


def get_modified_sources(project_name: str, bug_id: str) -> list[str]:
    """Get the list of modified sources for a specific bug.
    
    Parameters:
    - project_name: Project name (e.g., 'Chart', 'Closure', 'Math')
    - bug_id: Bug ID (e.g., '2', '3', '4')
    
    Returns:
    - list[str]: List of modified source packages (e.g., ['com.google.javascript.jscomp.TypeCheck'])
    """
    try:
        # Run the info command for specific bug
        result = subprocess.run(
            ['defects4j', 'info', '-p', project_name, '-b', bug_id],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            output = result.stdout
            modified_sources = []
            
            # Parse the output to find "List of modified sources:"
            lines = output.split('\n')
            in_modified_sources = False
            
            for line in lines:
                line = line.strip()
                
                # Check if we've reached the modified sources section
                if line == "List of modified sources:":
                    in_modified_sources = True
                    continue
                
                # If we're in the modified sources section and see a dash, extract the source
                if in_modified_sources and line.startswith('- '):
                    source = line[2:].strip()  # Remove the "- " prefix
                    modified_sources.append(source)
                elif in_modified_sources and line == "":
                    # Empty line indicates end of modified sources section
                    break
            
            return modified_sources
        else:
            print(f"Failed to get bug info: {result.stderr}")
            return []
            
    except Exception as e:
        print(f"Error getting modified sources: {e}")
        return []


def get_full_source_path(project_name: str, working_dir: str, package_path: str):
    """Construct the target_java_path by combining connecting path with modified source.
    
    Parameters:
    - project_name: Project name (e.g., 'Chart', 'Closure', 'Math')
    - modified_source: Modified source from Defects4J (e.g., 'org.apache.commons.math3.dfp.Dfp')
    
    Returns:
    - str: Full target_java_path relative to working_dir
    """

    # Get the connecting path for this project
    paths = {
        'chart': 'source',
        'closure': 'src',
        'mockito': 'src', 
        'math': 'src/main/java',
        'lang': 'src/main/java',
        'time': 'src/main/java'
    }

    # Combine connecting path with file path
    full_source_path = connect_paths(project_name, working_dir, paths, package_path)
    return full_source_path


########################
# HELPER FUNCTIONS FOR GET_FAILING_TEST_INFO
########################

def get_each_failing_test_info(failing_tests: list[str], failing_tests_info: str) -> dict[str, str]:
    info_for_each_test = {}

    for test_identifier in failing_tests:
        # Find the start of this test's info (starts with "--- test_identifier")
        start_marker = f"--- {test_identifier}"
        start_index = failing_tests_info.find(start_marker)
        
        if start_index == -1:
            # Test info not found, add empty dict
            all_info.append({test_identifier: ""})
            continue
        
        # Find the end of this test's info (next "---" or end of string)
        next_start = failing_tests_info.find("---", start_index + 1)
        
        if next_start == -1:
            # This is the last test, take everything to the end
            test_info = failing_tests_info[start_index:]
        else:
            # Take everything up to the next test
            test_info = failing_tests_info[start_index:next_start]
        
        info_for_each_test[test_identifier] = test_info

    return info_for_each_test


def get_failure_message(test_info: str) -> str:
    """
    Extract the failure message from the failing test info for a specific test.
    
    Args:
        test_info (str): The failing test info for a specific test
        
    Returns:
        str: The complete failure message from the second line
    """
    lines = test_info.split('\n')
    
    # Return the second line (index 1) if it exists
    if len(lines) > 1:
        return lines[1].strip()
    
    return ""  # Return empty string if not found


def get_full_test_path(project_name: str, working_dir: str, test_identifier_without_method: str) -> str:
        # Get the connecting path for this project
    paths = {
        'chart': 'tests',
        'closure': 'tests',
        'mockito': 'test', 
        'math': 'src/test/java',
        'lang': 'src/test/java',
        'time': 'src/test/java'
    }

    # Combine connecting path with file path
    full_test_path = connect_paths(project_name, working_dir, paths, test_identifier_without_method)
    return full_test_path


def get_failing_test_method_and_line(test_identifier: str, failing_test_info: str) -> tuple[str, str, int]:
    """
    Extract the method name, and line number from the failing test info for a specific test.
    
    Parameters:
    - test_identifier: The specific test identifier to look for
    - failing_tests_info: String containing the failing test information
    
    Returns:
    - tuple[str, int]: (package_path, method_name, line_number)
    """
    
    # Split the test identifier to get package path and method name
    parts = test_identifier.split('::')
    if len(parts) != 2:
        return ("", "", 0)
    
    package_path = parts[0]  # org.mockito.internal.util.TimerTest
    method_name = parts[1]   # should_throw_friendly_reminder_exception_when_duration_is_negative
    
    # Convert :: to . for searching in stack trace
    test_identifier_with_dots = test_identifier.replace('::', '.')
    
    # Search for the test identifier in the "at..." lines
    lines = failing_test_info.split('\n')
    for line in lines:
        if line.strip().startswith('at ') and test_identifier_with_dots in line:
            # Extract line number from parentheses
            # Format: "at org.mockito.internal.util.TimerTest.should_throw_friendly_reminder_exception_when_duration_is_negative(TimerTest.java:42)"
            if '(' in line and ')' in line:
                file_line_part = line.split('(')[1].split(')')[0]
                if ':' in file_line_part:
                    line_number = int(file_line_part.split(':')[1])
                    return (package_path, method_name, line_number)
    
    return (package_path, method_name, -1)  # Return -1 if line number not found