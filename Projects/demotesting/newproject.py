import os

def create_project_structure():
    """
    Creates the specified project structure for a backend/frontend application.
    """
    # Define the root directory
    project_root = '.'
    
    # Define the directories and files in a nested dictionary
    structure = {
        'backend': ['astra_client.py', 'ingest.py', 'llm_client.py'],
        'frontend': ['streamlit_app.py'],
        'docker-compose.yml': '',
        'README.md': ''
    }

    def create_elements(base_path, elements):
        for name, content in elements.items():
            path = os.path.join(base_path, name)
            if isinstance(content, list):
                # It's a directory containing files
                os.makedirs(path, exist_ok=True)
                for file_name in content:
                    with open(os.path.join(path, file_name), 'w') as f:
                        f.write('')
            elif isinstance(content, str):
                # It's a file
                with open(path, 'w') as f:
                    f.write('')

    # Create the top-level directories and files
    create_elements(project_root, structure)

    print("Project structure created successfully.")

if __name__ == "__main__":
    create_project_structure()