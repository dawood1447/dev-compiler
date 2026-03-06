# languages.py

"""
Configuration for supported programming languages.
Each language maps to its file extension and the base command used to run it.
"""

SUPPORTED_LANGUAGES = {
    "Python": {
        "extension": ".py",
        # Using python3 for Linux/Mac. If on Windows, you might just use "python"
        "command": "python3" 
    },
    "JavaScript": {
        "extension": ".js",
        "command": "node"
    }
}

def get_language_config(language_name):
    """Returns the configuration dictionary for a given language."""
    return SUPPORTED_LANGUAGES.get(language_name)