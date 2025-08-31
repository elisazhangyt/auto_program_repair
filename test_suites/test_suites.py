import test_suites_helpers as tsh
import os
import subprocess
from ..context_retrieval import retrieval_utils as cr

def run_defects4j_test(project_name: str, version: str, working_dir: str, java_patch_files: dict[str, str]) -> list:
    '''
    Run the test suite for a given project and version.
    
    Parameters:
    - project_name: Project name (e.g., 'Chart', 'Closure', 'Math')
    - version: Bug version (e.g., '2', '3', '4')
    - working_dir: Absolute path to the project directory
    - java_patch_files: Dict containing entries in the form of {modified source name: path to java patch file}
    '''
    if not tsh.checkout_defects4j_project(project_name, version, working_dir):
        return {'error': 'Failed to checkout project'}
    
    results = []

    modified_sources = tsh.get_modified_sources(project_name, version)
    for modified_source in modified_sources:
        full_source_path = tsh.get_full_source_path(project_name, working_dir, modified_source)
        
        try:
            if not tsh.apply_java_file_patch(java_patch_files[modified_source], full_source_path):
                return {'error': 'Failed to apply Java file patch'}
        
            # Run the test command
            result = subprocess.run(
                ['defects4j', 'test', '-w', working_dir],
                capture_output=True,
                text=True,
                cwd=working_dir
            )
        
            # Parse the output to extract test results
            output = result.stdout
            return_code = result.returncode
            
                # Parse failing test names
            failing_tests = []
            lines = output.split('\n')

            for line in lines:
                if line.strip().startswith('- '):
                    # Remove the "  - " prefix and get the test name
                    test_name = line.strip()[2:].strip()
                    failing_tests.append(test_name)

            results.append({
            'success': return_code == 0,
            'failing_tests': failing_tests,
            'return_code': return_code
            })
        
        except Exception as e:
            print(f"Error occurred: {e}")
            return {'error': str(e)}

    return results


# Call this function if success code is 0
def get_failing_test_info(working_dir: str, project_name: str, failing_tests: list[str]) -> list[dict[str]]:
    """
    Extract detailed information about failing tests.

    Return:
    list of failing tests, each containing: a dict of strings identifying the exception name, entire buggy
    function, and the exact failing line
    """
    all_info = []

    # get failing_tests_info
    failing_tests_path = os.path.join(working_dir, 'failing_tests')
    failing_tests_info = subprocess.run(['cat', failing_tests_path], capture_output=True, text=True).stdout
    info_for_each_test = tsh.get_each_failing_test_info(failing_tests, failing_tests_info)

    for test_identifier in failing_tests:
        test_info = info_for_each_test.get(test_identifier)
        failure_message = tsh.get_failure_message(test_info)

        buggy_method = "not found"
        buggy_line = "not found"

        package_path, method_name, line_number = tsh.get_failing_test_method_and_line(test_identifier, test_info)
        if (line_number != -1):
            test_path = tsh.get_full_test_path(project_name, working_dir, package_path)

            with open(test_path, 'rb') as f:
                code = f.read()
            buggy_method = cr.get_node_text(cr.retrieve_method_by_name(test_path, method_name), code)

            buggy_line = cr.retrieve_code_by_line_number(test_path, [(line_number, line_number)])

        test_info = {
            'failing test': test_identifier,
            'failure message': failure_message,
            'buggy method': buggy_method,
            'buggy line': buggy_line
        }
        all_info.append(test_info)
    
    return all_info