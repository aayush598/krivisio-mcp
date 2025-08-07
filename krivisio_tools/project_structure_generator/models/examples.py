from typing import List, Dict

def get_example_repos() -> List[Dict]:
    """
    Return hardcoded example repository structures for similarity matching.
    
    Each example contains:
        - description: Project summary
        - tech_stack: List of technologies
        - structure: Directory structure in JSON format
    """
    return [
        {
            "description": "React TypeScript frontend with Node.js backend",
            "tech_stack": ["React", "TypeScript", "Node.js", "Express"],
            "structure": {
                "name": "fullstack-app",
                "structure": [
                    {"type": "file", "name": "README.md"},
                    {"type": "file", "name": ".gitignore"},
                    {"type": "file", "name": "package.json"},
                    {"type": "folder", "name": "frontend", "children": [
                        {"type": "file", "name": "package.json"},
                        {"type": "folder", "name": "src", "children": [
                            {"type": "folder", "name": "components", "children": []},
                            {"type": "folder", "name": "pages", "children": []},
                            {"type": "folder", "name": "utils", "children": []},
                            {"type": "file", "name": "App.tsx"},
                            {"type": "file", "name": "index.tsx"}
                        ]},
                        {"type": "folder", "name": "public", "children": []}
                    ]},
                    {"type": "folder", "name": "backend", "children": [
                        {"type": "file", "name": "package.json"},
                        {"type": "folder", "name": "src", "children": [
                            {"type": "folder", "name": "routes", "children": []},
                            {"type": "folder", "name": "models", "children": []},
                            {"type": "folder", "name": "middleware", "children": []},
                            {"type": "file", "name": "server.js"}
                        ]}
                    ]},
                    {"type": "folder", "name": "tests", "children": []},
                    {"type": "folder", "name": "docs", "children": []}
                ]
            }
        },
        {
            "description": "Python Django REST API with PostgreSQL",
            "tech_stack": ["Python", "Django", "PostgreSQL", "Redis"],
            "structure": {
                "name": "django-api",
                "structure": [
                    {"type": "file", "name": "README.md"},
                    {"type": "file", "name": ".gitignore"},
                    {"type": "file", "name": "requirements.txt"},
                    {"type": "file", "name": "manage.py"},
                    {"type": "folder", "name": "app", "children": [
                        {"type": "file", "name": "__init__.py"},
                        {"type": "file", "name": "settings.py"},
                        {"type": "file", "name": "urls.py"},
                        {"type": "file", "name": "wsgi.py"}
                    ]},
                    {"type": "folder", "name": "api", "children": [
                        {"type": "file", "name": "__init__.py"},
                        {"type": "file", "name": "models.py"},
                        {"type": "file", "name": "views.py"},
                        {"type": "file", "name": "serializers.py"},
                        {"type": "file", "name": "urls.py"}
                    ]},
                    {"type": "folder", "name": "tests", "children": []},
                    {"type": "folder", "name": "docs", "children": []}
                ]
            }
        }
    ]
