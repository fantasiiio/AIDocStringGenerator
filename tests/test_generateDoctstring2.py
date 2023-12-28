
   

import unittest
from unittest.mock import MagicMock, patch, ANY, mock_open
import sys
import os
import tempfile
import shutil
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(f"{parent}")
from pathlib import Path

from DocStringGenerator.APICommunicator import *
from DocStringGenerator.DocstringProcessor import DocstringProcessor
from DocStringGenerator.FileProcessor import FileProcessor
from DocStringGenerator.ConfigManager import ConfigManager
from dotenv import load_dotenv

class TestAPICommunicator(unittest.TestCase):
    def setUp(self):
        load_dotenv()
        ConfigManager(initial_config={"keep_responses": False, "bot": "file", 'verbose': False, "model": "classTest"})        
        self.communicator_manager: CommunicatorManager = dependencies.resolve("CommunicatorManager")
        if self.communicator_manager.bot_communicator:
            self.bot_communicator: BaseBotCommunicator = self.communicator_manager.bot_communicator

    @patch('requests.post')
    def test_send_request(self, mock_post):
        # Mocking the post request to return a predefined response
        mock_response = MagicMock()
        mock_response.iter_lines.return_value = iter([
            b'header or metadata', 
            b'data: {"completion": "mocked completion"}'
        ])
        mock_post.return_value = mock_response

        response = self.bot_communicator.ask_for_docstrings('test code')
        self.assertIn('mocked completion', response.content) 

    @patch('requests.post')
    def test_error_handling(self, mock_post):
        # Simulate an exception during the request
        mock_post.side_effect = Exception("Connection error")

        response = self.bot_communicator.ask_for_docstrings('test code')
        self.assertIn('Error during Claude API call', response.content)

    @patch('requests.post')
    def test_response_parsing(self, mock_post):
        # Testing parsing of a valid response
        valid_response = iter([
            b'header or metadata', 
            b'data: {"completion": "test docstring"}'
        ])
        mock_response = MagicMock()
        mock_response.iter_lines.return_value = valid_response
        mock_post.return_value = mock_response

        response = self.bot_communicator.ask_for_docstrings('test code')
        self.assertIn('test docstring', response.content)


class TestDocstringProcessor(unittest.TestCase):
    def setUp(self):
        load_dotenv()

        self.processor = dependencies.resolve("DocstringProcessor")
        self.mock_file_path = MagicMock()
        self.mock_file_path.read_text.return_value = "def test_function():\n    pass"


    def test_extract_docstrings2(self):
        # Test validation of a JSON response
        valid_response = '{"docstrings": {"MyClass": {"exemple": "example code", "docstring": "Class docstring", "methods": {"my_method": "Method docstring"}}}}'        
        self.assertTrue(self.processor.extract_docstrings([valid_response]))


class TestFileProcessor(unittest.TestCase):
    def setUp(self):
        load_dotenv()
        ConfigManager(initial_config={"keep_responses": False, "bot": "file", 'verbose': False, "model": "classTest"})
        self.file_processor: FileProcessor = dependencies.resolve("FileProcessor")

    def test_process_file(self):
        classTest_file_path = Path('./tests/classTest_orig.py')
        temp_dir = tempfile.mkdtemp()  # Create a temporary directory
        temp_file_path = Path(temp_dir, 'classTest_temp.py')

        # Copy the original file to the temporary file
        shutil.copy2(str(classTest_file_path), str(temp_file_path))

        # Create a FileProcessor instance and call process_file on the temp file
        file_processor: FileProcessor = dependencies.resolve("FileProcessor")
        success = file_processor.process_file(temp_file_path)

        # Assert that the process was successful
        self.assertTrue(success)

        # Read the contents of the temporary file after processing
        with open(str(temp_file_path), 'r') as file:
            processed_content = file.read()

        # Read the expected contents from the result file
        result_file_path = Path('./tests/classTest-result.py')
        with open(str(result_file_path), 'r') as file:
            expected_docstrings = file.read()

        # Assert that the processed content matches the expected content
        self.assertEqual(expected_docstrings, processed_content)

        # Remove the temporary file first
        os.remove(str(temp_file_path))

        # Check if the directory is empty, and remove if possible
        if not os.listdir(temp_dir):
            os.rmdir(temp_dir)  # Directory is empty, safe to remove
        else:
            # Directory is not empty, proceed with recursive deletion
            try:
                shutil.rmtree(temp_dir)  # Recursively delete all contents
                print("Temporary directory and its contents have been removed.")
            except OSError as e:
                print("Error removing temporary directory:", e)
                # Handle potential errors, such as permission issues


    @patch('DocStringGenerator.FileProcessor.FileProcessor.process_file')
    def test_process_directory(self, mock_process_file):
        # Mocking the process_file method to simulate file processing
        mock_process_file.return_value = True

        file_processor = dependencies.resolve("FileProcessor")

        file_processor.process_file("tests/classTest_orig.py")

        # Assuming the directory contains two Python files
        self.assertEqual(mock_process_file.call_count, 1)


    def test_process_file2(self):            
        new_test_script_content = """class Calculator:
    def add(self, x, y):
        return x + y

    def subtract(self, x, y):
        return x - y

    def multiply(self, x, y):
        return x * y

    def divide(self, x, y):
        if y == 0:
            raise ValueError("Cannot divide by zero.")
        return x / y"""

        # New content for the JSON file (docstrings_response.json)
        new_docstrings_response_content = """{
    "docstrings": {
        "Calculator":{
            "docstring": "Class to perform basic arithmetic operations.",
            "example": "calc = Calculator()\\nresult = calc.add(5, 3)\\nprint(result)",
            "methods": {
                "add": "Adds two numbers.",
                "subtract": "Subtracts the second number from the first.",
                "multiply": "Multiplies two numbers.",
                "divide": "Divides the first number by the second."
            }
        }
    }  
}
"""

        final_script_with_comments = """class Calculator:
    \"\"\"Class to perform basic arithmetic operations.\"\"\"
    def add(self, x, y):
        \"\"\"Adds two numbers.\"\"\"
        return x + y

    def subtract(self, x, y):
        \"\"\"Subtracts the second number from the first.\"\"\"
        return x - y

    def multiply(self, x, y):
        \"\"\"Multiplies two numbers.\"\"\"
        return x * y

    def divide(self, x, y):
        \"\"\"Divides the first number by the second.\"\"\"
        if y == 0:
            raise ValueError("Cannot divide by zero.")
        return x / y

    def example_function_Calculator(self):
        calc = Calculator()
        result = calc.add(5, 3)
        print(result)"""
        
        # New file paths
        with tempfile.TemporaryDirectory() as tmpdir:  
            new_test_script_file_path = Path(tmpdir, "new_test_script.py")  
            new_docstrings_response_file_path = Path(tmpdir, "new_docstrings.response.json")  

            # Writing the new contents to the files
            with open(new_test_script_file_path, 'w') as file:
                file.write(new_test_script_content.strip())

            with open(new_docstrings_response_file_path, 'w') as file:
                file.write(new_docstrings_response_content.strip())
            stem = Path(new_docstrings_response_file_path).stem

            directory_path = new_docstrings_response_file_path.parent
            ConfigManager().set_config('model', str(Path(directory_path, stem).absolute()))

            response = self.file_processor.process_file(new_test_script_file_path)
            self.assertTrue(response.is_valid)

            self.assertEqual(response.content, final_script_with_comments)  
            dependencies.resolve("FileProcessor").removed_from_processed_log(new_test_script_file_path)


if __name__ == '__main__':
    unittest.main()
