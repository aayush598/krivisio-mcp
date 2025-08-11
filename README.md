# cocomo2 estimation
## INPUT
```
{
  "model_name": "cocomo2",
  "data": {
    "function_points": {
      "fp_items": [
        {"fp_type": "EI", "det": 8, "ftr_or_ret": 1},
        {"fp_type": "EO", "det": 10, "ftr_or_ret": 2},
        {"fp_type": "ILF", "det": 18, "ftr_or_ret": 3}
      ],
      "language": "Java"
    },
    "reuse": {
      "asloc": 3500,
      "dm": 20,
      "cm": 10,
      "im": 10,
      "su_rating": "L",
      "aa_rating": "2",
      "unfm_rating": "CF",
      "at": 15
    },
    "revl": {
      "new_sloc": 8500,
      "adapted_esloc": 2500,
      "revl_percent": 25
    },
    "effort_schedule": {
      "sloc_ksloc": 7.5,
      "sced_rating": "L"
    }
  }
}
```

## OUTPUT
```
{
  "model": "cocomo2",
  "result": {
    "function_point_sizing": {
      "ufp": 15,
      "sloc": 795
    },
    "reuse": {
      "esloc": 4025
    },
    "revl_adjustment": {
      "sloc_total": 11000,
      "sloc_after_revl": 13750
    },
    "estimation": {
      "person_months": 26.96,
      "development_time_months": 8.53,
      "avg_team_size": 3.16
    }
  }
}
```

# spec sheet generation 

## INPUT
```
{
  "module": "onboarding",
  "doc_type": "proposal",
  "input_data": {
    "project_name": "SmartEdu LMS",
    "complexity_level": "Intermediate",
    "features": [
      "User authentication and role management",
      "Interactive course modules with quizzes",
      "Progress tracking and analytics",
      "Live video conferencing integration",
      "Admin dashboard for content management"
    ],
    "cocomo_results": {
      "results": {
        "function_points": {
          "sloc": 18000
        },
        "reuse": {
          "esloc": 14500
        },
        "revl": {
          "sloc_after_revl": 16000
        },
        "effort_schedule": {
          "person_months": 24.5,
          "development_time_months": 5.5,
          "avg_team_size": 4.45
        }
      }
    }
  }
}
```

OUTPUT 

```
{
  "document": "# SmartEdu LMS Project Specification Document\n\n## 1. Executive Summary\n\nThe SmartEdu LMS project aims to develop a comprehensive learning management system tailored for educational institutions, designed to enhance learning experiences through interactive modules and seamless administration. The project has an intermediate complexity level, requiring a dedicated team to deliver key features such as user authentication, course modules with quizzes, progress tracking, live video conferencing, and an admin dashboard.\n\n## 2. Project Overview\n\n### Purpose\nThe purpose of the SmartEdu LMS is to provide an efficient platform for managing educational content and facilitating interactive learning experiences for students and teachers.\n\n### Background\nWith the increasing demand for digital education solutions, SmartEdu LMS intends to offer a robust platform that addresses key challenges faced by educators, including content management, student engagement, and performance tracking.\n\n### Goals\n- Develop a user-friendly LMS with essential features for both learners and educators.\n- Integrate advanced tools such as live video conferencing to support remote learning.\n- Provide analytics and progress tracking to improve learning outcomes.\n\n## 3. Functional Requirements\n\n### User Authentication and Role Management\n- Secure login system with roles: Administrator, Instructor, Student.\n- Password recovery and two-factor authentication.\n\n### Interactive Course Modules with Quizzes\n- Creation of multimedia-rich courses by instructors.\n- Self-paced learning with embedded quizzes for assessment.\n\n### Progress Tracking and Analytics\n- Dashboard displaying individual progress reports.\n- Analytics on course completion rates and student performance.\n\n### Live Video Conferencing Integration\n- Real-time video classes using third-party integration (e.g., Zoom or Microsoft Teams).\n- Recording sessions for later review.\n\n### Admin Dashboard for Content Management\n- Manage courses, users, assessments.\n- Generate reports on platform usage statistics.\n\n## 4. Non-Functional Requirements\n\n### Performance\n- System response time should be under 2 seconds for any action.\n  \n### Scalability\n- Support up to 10,000 concurrent users without performance degradation.\n\n### Reliability\n- System uptime should be at least 99.5%.\n\n## 5. Technical Architecture\n\n### System Diagrams\n![System Architecture Diagram](link_to_diagram)\n\n### Services\n- Authentication Service: Manages user roles and access control.\n- Course Management Service: Handles course creation and updates.\n- Analytics Service: Aggregates data for reporting purposes.\n  \n### Tech Stack\n- Frontend: React.js\n- Backend: Node.js with Express.js\n- Database: PostgreSQL\n- Video Conferencing: Integration via Zoom API/Microsoft Teams API\n\n## 6. Development Estimation\n\nBased on COCOMO-II estimation:\n\n| Metric | Estimate |\n|--------|----------|\n| Estimated SLOC | 18,000 |\n| Equivalent SLOC (with reuse) | 14,500 |\n| Total SLOC (after REVL) | 16,000 |\n| Estimated Effort | 24.5 person-months |\n| Development Time | 5.5 months |\n| Average Team Size | 4.45 members |\n\n## 7. Risk Assessment\n\n**Project Risks**\n1. **Integration Failure**: Potential issues in integrating third-party video conferencing tools.\n   - *Mitigation*: Conduct thorough testing in early stages; have backup solutions ready.\n\n2. **Data Security**: Risk of unauthorized access to sensitive information.\n   - *Mitigation*: Implement robust encryption protocols; regular security audits.\n\n3. **Scope Creep**: Addition of requirements beyond initial scope can delay the project.\n   - *Mitigation*: Establish clear project scope; adhere strictly unless changes are critical.\n\n## 8. Deliverables & Milestones\n\n**Phases**\n\n1. **Phase 1**: Requirements Gathering & Design (Month 1)\n   - Deliverable: Requirements Specification Document\n  \n2. **Phase 2**: Development (Months 2 - 4)\n   - Deliverable: Beta Release\n  \n3. **Phase 3**: Testing & Integration (Month 4 - Month 5"
}
```


# Talent matching
## INPUT
```
{
  "specsheet": {
    "project_description": "We need a frontend + backend team for an ecommerce platform using React and Node.",
    "preferred_team_size": 4,
    "minimum_manager_score": 4.2
  },
  "candidates": [
    {
      "name": "Alice",
      "domain": "frontend",
      "skills": ["React", "TypeScript"],
      "manager_score": 4.5,
      "availability": true
    },
    {
      "name": "Bob",
      "domain": "backend",
      "skills": ["Node.js", "Express"],
      "manager_score": 4.3,
      "availability": true
    }
  ]
}
```

## OUTPUT
```
{
  "selected_team": [
    {
      "name": "Alice",
      "domain": "frontend",
      "skills": [
        "React",
        "TypeScript"
      ],
      "manager_score": 4.5
    },
    {
      "name": "Bob",
      "domain": "backend",
      "skills": [
        "Node.js",
        "Express"
      ],
      "manager_score": 4.3
    }
  ]
}
```
----------

# Folder structure generation 
## INPUT
```
{
  "description": "Chatbot project for customer service",
  "tech_stack": ["html", "css", "javascript"],
  "preferences": {
    "include_docs": true,
    "include_tests": true,
    "include_docker": true,
    "include_ci_cd": false,
    "custom_folders": ["assets", "utils"],
    "framework_specific": false
  }
}
```
## OUTPUT
```
{
  "structure": {
    "name": "chatbot-project",
    "type": "folder",
    "children": [
      {
        "name": "assets",
        "type": "folder",
        "children": []
      },
      {
        "name": "utils",
        "type": "folder",
        "children": []
      },
      {
        "name": "src",
        "type": "folder",
        "children": [
          {
            "name": "index.html",
            "type": "file"
          },
          {
            "name": "styles.css",
            "type": "file"
          },
          {
            "name": "app.js",
            "type": "file"
          }
        ]
      },
      {
        "name": "docs",
        "type": "folder",
        "children": [
          {
            "name": "README.md",
            "type": "file"
          }
        ]
      },
      {
        "name": "__tests__",
        "type": "folder",
        "children": [
          {
            "name": "app.test.js",
            "type": "file"
          }
        ]
      },
      {
        "name": ".dockerignore",
        "type": "file"
      },
      {
        "name": ".gitignore",
        "type": "file"
      },
      {
        "name": ".eslintrc.json",
        "type": "file"
      },
      {
        "name": ".prettierrc.json",
        "type": "file"
      },
      {
        "name": ".dockerignore",
        "type": "file"
      },
      {
        "name": "Dockerfile",
        "type": "file"
      }
    ]
  }
}
```


# Github tool

## INPUT (Repo initialization)
```
{
  "function": "init_repo",
  "data": {
    "token": "ghp_abc123",
    "repo_name": "my-new-repo-52",
    "private": true,
    "description": "Test repo"
  }
}
```

## OUTPUT (Repo initialization)
```
{
  "result": "https://github.com/aayush598/my-new-repo-52"
}
```

## INPUT (Branch creation)
```
{
  "function": "create_branch",
  "data": {
    "token": "ghp_abc123",
    "repo_name": "aayush598/my-new-repo-52",
    "new_branch": "dev",
    "source_branch": "main"
  }
}
```

## OUTPUT (Branch creation)
```
{
  "result": "refs/heads/dev"
}
```

## INPUT (Code update)
```
{
  "function": "update_repo",
  "data": {
    "token": "ghp_abc123",
    "git_url": "https://github.com/aayush598/my-new-repo-52.git",
    "branch": "main",
    "files_to_update": [
      ["README.md", "# Updated README"],
      ["src/index.py", "print('Hello world')"]
    ],
    "commit_message": "Initial code push"
  }
}
```

## OUTPUT (Code update)
```
{
  "result": "a2e3ffa2eb14089d5f299eaaf75d8eab52d955bf"
}
```


## INPUT (Feature generation)
```
{
  "function": "process_document",
  "data": {
    "document_input": "I need a Python web scraper project with more than 500 stars.",
    "document_type": "text",
    "github_token": "your_github_token_here"
  }
}
```

## OUTPUT (Feature generation)
```
{
  "result": {
    "search_params": {
      "query": "Python web scraper",
      "stars": ">500",
      "token": "your_github_token_here"
    },
    "repos": [
      {
        "name": "autoscraper",
        "full_name": "alirezamika/autoscraper",
        "description": "A Smart, Automatic, Fast and Lightweight Web Scraper for Python",
        "stars": 6887,
        "language": "Python",
        "html_url": "https://github.com/alirezamika/autoscraper"
      },
      {
        "name": "crawlee-python",
        "full_name": "apify/crawlee-python",
        "description": "Crawlee—A web scraping and browser automation library for Python to build reliable crawlers. Extract data for AI, LLMs, RAG, or GPTs. Download HTML, PDF, JPG, PNG, and other files from websites. Works with BeautifulSoup, Playwright, and raw HTTP. Both headful and headless mode. With proxy rotation.",
        "stars": 6148,
        "language": "Python",
        "html_url": "https://github.com/apify/crawlee-python"
      },
      {
        "name": "Automatic-Udemy-Course-Enroller-GET-PAID-UDEMY-COURSES-for-FREE",
        "full_name": "aapatre/Automatic-Udemy-Course-Enroller-GET-PAID-UDEMY-COURSES-for-FREE",
        "description": "Do you want to LEARN NEW STUFF for FREE? Don't worry, with the power of web-scraping and automation, this script will find the necessary Udemy coupons & enroll you for PAID UDEMY COURSES, ABSOLUTELY FREE!",
        "stars": 3228,
        "language": "Python",
        "html_url": "https://github.com/aapatre/Automatic-Udemy-Course-Enroller-GET-PAID-UDEMY-COURSES-for-FREE"
      },
      {
        "name": "scrapfly-scrapers",
        "full_name": "scrapfly/scrapfly-scrapers",
        "description": "Scalable Python web scraping scripts for +40 popular domains",
        "stars": 594,
        "language": "Python",
        "html_url": "https://github.com/scrapfly/scrapfly-scrapers"
      },
      {
        "name": "quick-start-guide",
        "full_name": "oxylabs/quick-start-guide",
        "description": "Python quick start guides to get the most out of Oxylabs' Web Scraper API free trial.",
        "stars": 517,
        "language": null,
        "html_url": "https://github.com/oxylabs/quick-start-guide"
      }
    ],
    "repo_features": {
      "alirezamika/autoscraper": {
        "features": [
          "Automatic web scraping",
          "Learns scraping rules automatically",
          "Extracts similar elements from new URLs",
          "Supports getting exact results",
          "Supports custom requests parameters like proxies and headers",
          "Can save and load the scraping model"
        ],
        "tech_stack": [
          "Python",
          "requests"
        ]
      },
      "apify/crawlee-python": {
        "features": [
          "Unified interface for HTTP & headless browser crawling",
          "Automatic parallel crawling based on available system resources",
          "Written in Python with type hints",
          "Automatic retries on errors or getting blocked",
          "Integrated proxy rotation and session management",
          "Configurable request routing",
          "Persistent queue for URLs to crawl",
          "Pluggable storage of both tabular data and files",
          "Robust error handling"
        ],
        "tech_stack": [
          "Python",
          "BeautifulSoup",
          "Playwright",
          "HttpxHttpClient",
          "Asyncio"
        ]
      },
      "aapatre/Automatic-Udemy-Course-Enroller-GET-PAID-UDEMY-COURSES-for-FREE": {
        "features": [
          "Grab FREE Udemy Coupons",
          "Enroll in paid Udemy courses for free",
          "Web scraping for coupon links from multiple sources",
          "Automated script to handle course enrollment process",
          "CLI with various options for customization",
          "Docker support for running the script"
        ],
        "tech_stack": [
          "Python 3.8+",
          "Selenium",
          "REST API requests",
          "Docker"
        ]
      },
      "scrapfly/scrapfly-scrapers": {
        "features": [
          "Educational example scrapers for popular web scraping targets",
          "Uses ScrapFly web scraping API and Python",
          "Includes guides and sample datasets for each scraper",
          "Regular updates and improvements by Scrapfly team"
        ],
        "tech_stack": [
          "Python 3.10+",
          "Scrapfly's Python SDK",
          "Parsel",
          "asyncio",
          "JMESPath",
          "nested-lookup",
          "loguru"
        ]
      },
      "oxylabs/quick-start-guide": {
        "features": [
          "One-week free trial of Web Scraper API",
          "Setup guides for various types of websites",
          "Basic code samples in Python",
          "Web-based interface for testing API capabilities",
          "AI-powered OxyCopilot feature for generating scraping and parsing codes"
        ],
        "tech_stack": [
          "Python"
        ]
      }
    },
    "classified_features": {
      "Basic": {
        "features": [
          "Educational example scrapers for popular web scraping targets",
          "Includes guides and sample datasets for each scraper",
          "Regular updates and improvements by Scrapfly team",
          "One-week free trial of Web Scraper API",
          "Setup guides for various types of websites",
          "Basic code samples in Python",
          "Web-based interface for testing API capabilities"
        ],
        "tech_stack": [
          "Python"
        ]
      },
      "Intermediate": {
        "features": [
          "Automatic web scraping",
          "Learns scraping rules automatically",
          "Extracts similar elements from new URLs",
          "Supports getting exact results",
          "Supports custom requests parameters like proxies and headers",
          "Can save and load the scraping model",
          "Grab FREE Udemy Coupons",
          "Enroll in paid Udemy courses for free",
          "Web scraping for coupon links from multiple sources",
          "Automated script to handle course enrollment process",
          "CLI with various options for customization",
          "Docker support for running the script"
        ],
        "tech_stack": [
          "Python 3.8+",
          "Selenium",
          "REST API requests",
          "Docker"
        ]
      },
      "Advanced": {
        "features": [
          "Unified interface for HTTP & headless browser crawling",
          "Automatic parallel crawling based on available system resources",
          "Written in Python with type hints",
          "Automatic retries on errors or getting blocked",
          "Integrated proxy rotation and session management",
          "Configurable request routing",
          "Persistent queue for URLs to crawl",
          "Pluggable storage of both tabular data and files",
          "Robust error handling"
        ],
        "tech_stack": [
          "Python 3.10+",
          "'Scrapfly's Python SDK'",
          "'Parsel'",
          "'asyncio'",
          "'JMESPath'",
          "'nested-lookup'",
          "'loguru'",
          "BeautifulSoup",
          "Playwright",
          "HttpxHttpClient",
          "Asyncio"
        ]
      }
    }
  }
}
```


# Side tool
## INPUT (cocomo2 parameters generation)
```
{
  "tool": "cocomo2_parameters",
  "data": {
      "project_idea": "E-commerce site with AI recommendations",
      "level": "intermediate",
      "features": ["Login", "Shopping cart", "Payment gateway", "AI recommendations"],
      "tech_stacks": ["Python", "Django", "React"]
  }
}
```

## OUTPUT (cocomo2 parameters generation)
```
{
  "result": {
    "function_points": {
      "fp_items": [
        {
          "fp_type": "EI",
          "det": 8,
          "ftr_or_ret": 3
        },
        {
          "fp_type": "EO",
          "det": 10,
          "ftr_or_ret": 5
        },
        {
          "fp_type": "EQ",
          "det": 7,
          "ftr_or_ret": 4
        },
        {
          "fp_type": "ILF",
          "det": 15,
          "ftr_or_ret": 1
        },
        {
          "fp_type": "EIF",
          "det": 12,
          "ftr_or_ret": 2
        }
      ],
      "language": "Python"
    },
    "reuse": {
      "asloc": 2000,
      "dm": 30,
      "cm": 20,
      "im": 15,
      "su_rating": "N",
      "aa_rating": "3",
      "unfm_rating": "MF",
      "at": 25
    },
    "revl": {
      "new_sloc": 10000,
      "adapted_esloc": 3000,
      "revl_percent": 30
    },
    "effort_schedule": {
      "sloc_ksloc": 10.5,
      "sced_rating": "N"
    }
  }
}
```
