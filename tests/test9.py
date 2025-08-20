from krivisio_tools.github.utils.classify_repo_features import classify_features_and_tech_stack

# Example: Combined features + tech stack from multiple repos
repos_data = {
    "repo1": {
        "features": ["User authentication", "Basic CRUD operations", "REST API"],
        "tech_stack": ["Python", "Flask", "SQLite"]
    },
    "repo2": {
        "features": ["Real-time chat", "WebSocket communication", "Docker deployment"],
        "tech_stack": ["Node.js", "Socket.IO", "Docker"]
    },
    "repo3": {
        "features": ["Machine learning model training", "Data preprocessing", "GPU acceleration"],
        "tech_stack": ["Python", "TensorFlow", "CUDA"]
    }
}

classified = classify_features_and_tech_stack(repos_data)
print(classified)

print("\nClassified Features and Tech Stack:"
      "\nBasic Features:", classified["Basic"]["features"],
      "\nBasic Tech Stack:", classified["Basic"]["tech_stack"],
      "\nIntermediate Features:", classified["Intermediate"]["features"],
      "\nIntermediate Tech Stack:", classified["Intermediate"]["tech_stack"],
      "\nAdvanced Features:", classified["Advanced"]["features"],
      "\nAdvanced Tech Stack:", classified["Advanced"]["tech_stack"])