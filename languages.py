# languages.py

SUPPORTED_LANGUAGES = {
    "Python": {
        "extension": ".py",
        "compile_cmd": None,
        "run_cmd": ["python3", "{file}"],
        "version_cmd": ["python3", "--version"]
    },
    "JavaScript": {
        "extension": ".js",
        "compile_cmd": None,
        "run_cmd": ["node", "{file}"],
        "version_cmd": ["node", "--version"]
    },
    "C": {
        "extension": ".c",
        "compile_cmd": ["gcc", "{file}", "-o", "{dir}/a.out"],
        "run_cmd": ["{dir}/a.out"],
        "version_cmd": ["gcc", "--version"]
    },
    "C++": {
        "extension": ".cpp",
        "compile_cmd": ["g++", "{file}", "-o", "{dir}/a.out"],
        "run_cmd": ["{dir}/a.out"],
        "version_cmd": ["g++", "--version"]
    },
    "Java": {
        "extension": ".java",
        "compile_cmd": ["javac", "{file}"],
        "run_cmd": ["java", "-cp", "{dir}", "Main"], # Java requires strict class naming
        "version_cmd": ["javac", "--version"]
    }
}

def get_language_config(language_name):
    return SUPPORTED_LANGUAGES.get(language_name)