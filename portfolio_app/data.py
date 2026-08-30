"""Static data used to render the portfolio content."""

RECENT_PROJECTS = [
    {
        "title": "EdgeHarness",
        "image_src": "/assets/edgeharness.svg",
        "image_alt": "EdgeHarness routed local model evaluation pipeline",
        "live_url": None,
        "demo_url": None,
        "github_url": "https://github.com/EdgeHarness",
        "context": "Open-source agent infrastructure",
        "stack": ["Python", "Llama 3.1", "llama.cpp"],
        "image_fit": "contain",
        "description": (
            "An open-source harness and evaluation workspace for reliable, auditable tool-using "
            "business agents, with a locally tuned Llama 3.1 8B office-agent runtime."
        ),
    },
    {
        "title": "Ekua autonomous agent outreach platform",
        "image_src": "/assets/ekua-outreach.png",
        "image_alt": "Ekua Outreach dashboard showing active company outreach sessions",
        "image_position": "center top",
        "live_url": None,
        "demo_url": None,
        "github_url": "https://github.com/22joshlee/ekua-outreach",
        "context": "Agentic outreach system",
        "stack": ["Python", "FastAPI", "Supabase"],
        "description": (
            "A human-in-the-loop outreach system that researches companies, drafts grounded "
            "messages, manages replies, and schedules calls with operator approval before every send."
        ),
    },
    {
        "title": "Temporal Roadside Calibration",
        "image_src": "/assets/temporal-calibration.webp",
        "image_alt": "Roadside intersection frame with homography calibration overlay",
        "live_url": None,
        "demo_url": None,
        "github_url": "https://github.com/samkwak188/CATS-Lab----temporal-roadside-calibration",
        "context": "CATS Lab research",
        "stack": ["Python", "OpenCV", "Reproducible research"],
        "description": (
            "A reproducible pipeline for measuring fixed-camera drift and its effect on "
            "world-coordinate vehicle tracks, speed estimates, and behavior analysis."
        ),
    },
    {
        "title": "SwipeLease",
        "image_src": "/assets/swipelease.webp",
        "image_alt": "SwipeLease mobile sublease discovery interface",
        "live_url": None,
        "demo_url": None,
        "github_url": "https://github.com/samkwak188/SwipeLease",
        "context": "Campus housing product",
        "stack": ["Expo", "FastAPI", "Supabase"],
        "description": (
            "A campus sublease matching product with swipe discovery, verified student "
            "accounts, likes, matches, and in-app chat."
        ),
    },
    {
        "title": "Clawmsy",
        "image_src": "/assets/clawmsy.jpg",
        "image_alt": "Clawmsy desktop assistant repository and project documentation",
        "live_url": None,
        "demo_url": None,
        "github_url": "https://github.com/samkwak188/Clawmsy---AI-Agent-for-Students",
        "context": "Desktop software",
        "stack": ["Electron", "React", "TypeScript"],
        "description": (
            "A screen-aware desktop study assistant with live visual context, multimodal chat, "
            "provider switching, screenshot analysis, and capture-safety controls."
        ),
    },
    {
        "title": "LiveClaw",
        "image_src": "/assets/liveclaw.png",
        "image_alt": "LiveClaw desktop control application mark",
        "live_url": None,
        "demo_url": None,
        "github_url": "https://github.com/samkwak188/LiveClaw",
        "context": "Desktop automation",
        "stack": ["Rust", "Python", "Tauri"],
        "description": (
            "A voice-controlled desktop agent with visual grounding, step verification, "
            "interrupt handling, input-conflict detection, and confirmation for risky actions."
        ),
    },
]

CODING_PROJECTS = [
    {
        "title": "Husk",
        "image_src": "/assets/husk.png",
        "image_alt": "Husk dependency security CLI repository preview",
        "detail_url": "https://github.com/samkwak188/Husk-Agentic-dependency-security-CLI",
        "live_url": None,
        "demo_url": None,
        "github_url": "https://github.com/samkwak188/Husk-Agentic-dependency-security-CLI",
        "accent": "#f0efe9",
        "context": "Dependency security",
        "stack": ["Python", "npm", "PyPI"],
        "description": (
            "An install-time npm and PyPI security gate that reached 97.3% precision and "
            "82.8% F1 on a 100-package benchmark. It won Best Technical Depth in 2026."
        ),
    },
    {
        "title": "Meta Winterfell Contribution",
        "image_src": "/assets/winterfell.png",
        "image_alt": "Meta Winterfell open-source repository preview",
        "detail_url": "https://github.com/facebook/winterfell/pull/407",
        "live_url": None,
        "demo_url": None,
        "github_url": "https://github.com/facebook/winterfell/pull/407",
        "accent": "#f0efe9",
        "context": "Open-source contribution",
        "stack": ["Rust", "Winterfell", "ZK proofs"],
        "description": (
            "A Rust contribution that rejects mismatched AIR LDE and FRI domain sizes before "
            "proof validation, with a typed error for the invalid state."
        ),
    },
    {
        "title": "TableUs",
        "image_src": "/assets/tableus-latest.png",
        "image_alt": "Location-Aware Restaurant Planner",
        "detail_url": "https://github.com/samkwak188/Tableus-ai-agent",
        "live_url": None,
        "demo_url": None,
        "github_url": "https://github.com/samkwak188/Tableus-ai-agent",
        "accent": "#1f3a5f",
        "context": "Cursor Hackathon",
        "stack": ["Next.js", "FastAPI", "Google Maps"],
        "description": (
            "A group dining app that ranks nearby restaurants from preferences, reviews, "
            "dietary needs, and live Google Maps data. It won 2nd place at Cursor Hackathon 2026."
        ),
    },
    {
        "title": "AI Hub V2",
        "image_src": "/assets/aihub.png",
        "image_alt": "Multi-Model AI Chrome Extension",
        "detail_url": "https://github.com/samkwak188/AI-Hub-v2",
        "live_url": None,
        "demo_url": None,
        "github_url": "https://github.com/samkwak188/AI-Hub-v2",
        "accent": "#24324d",
        "context": "Browser tooling",
        "stack": ["Chrome Extensions", "Streaming", "Model routing"],
        "description": (
            "A Chrome side panel that sends a question and the current page context to four "
            "models, then streams their responses into one final answer."
        ),
    },
    {
        "title": "Polymarket Automation",
        "image_src": "/assets/polymarket.jpg",
        "image_alt": "AI Prediction Market Trading Bot",
        "detail_url": "https://github.com/samkwak188/Polymarket-Automation",
        "live_url": None,
        "demo_url": None,
        "github_url": "https://github.com/samkwak188/Polymarket-Automation",
        "accent": "#1f2b45",
        "context": "Market research automation",
        "stack": ["Python", "Risk controls", "Telemetry"],
        "description": (
            "A Polymarket research bot that combines news classification, probability estimates, "
            "Kelly sizing, risk limits, and live run telemetry."
        ),
    },
    {
        "title": "MediMenu",
        "image_src": "/assets/medimenu.png",
        "image_alt": "AI Dietary Safety Platform",
        "detail_url": "https://github.com/samkwak188/MediMenu",
        "live_url": "https://medimenu-frontend.onrender.com",
        "demo_url": None,
        "github_url": "https://github.com/samkwak188/MediMenu",
        "accent": "#3b2f47",
        "context": "Dietary safety product",
        "stack": ["Full stack", "QR workflows", "Structured data"],
        "description": (
            "A menu tool that flags possible conflicts with allergies, medications, and dietary "
            "restrictions. Restaurants can digitize a menu and share the result by QR code."
        ),
    },
    {
        "title": "TrustRent Platform",
        "image_src": "/assets/trustrent.jpg",
        "image_alt": "Enterprise Inspection Workflow",
        "detail_url": "https://github.com/samkwak188/TrustRent---Madhacks2025",
        "live_url": None,
        "demo_url": None,
        "github_url": "https://github.com/samkwak188/TrustRent---Madhacks2025",
        "accent": "#1a3a4a",
        "context": "Inspection workflow",
        "stack": ["Full stack", "Image evidence", "Records"],
        "description": (
            "A rental inspection workflow for collecting verified photos, storing structured "
            "records, and reviewing inspections across a property portfolio."
        ),
    },
    {
        "title": "ClearMove Evidence Kit",
        "image_src": "/assets/clearmove.jpeg",
        "image_alt": "Property Management Solution",
        "detail_url": "https://github.com/samkwak188/ClearMove-Final----Madhacks2025",
        "live_url": "https://cleanmove.onrender.com",
        "demo_url": None,
        "github_url": "https://github.com/samkwak188/ClearMove-Final----Madhacks2025",
        "accent": "#1a3f6f",
        "context": "Badger Build",
        "stack": ["Full stack", "Evidence capture", "Cloud"],
        "description": (
            "A rental inspection app that creates timestamped move-in and move-out evidence "
            "packets. It won 3rd place out of 92 teams at Badger Build 2025."
        ),
    },
    {
        "title": "MadLuv Matchmaking",
        "image_src": "/assets/madluv.png",
        "image_alt": "Data-Driven Social Platform",
        "detail_url": "https://github.com/samkwak188/MadLuv---MadData-Hackathon-2025-Project",
        "live_url": None,
        "demo_url": None,
        "github_url": "https://github.com/samkwak188/MadLuv---MadData-Hackathon-2025-Project",
        "accent": "#5c1a3a",
        "context": "MadData Hackathon",
        "stack": ["Recommendations", "University auth", "Data"],
        "description": (
            "A student matchmaking app with verified university sign-in and a recommendation "
            "pipeline built from profile and preference data."
        ),
    },
    {
        "title": "Autonomous Perception",
        "image_src": "https://raw.githubusercontent.com/samkwak188/Wisconsin-Autonomous-Perception-Coding-Challenge/main/sample.png",
        "image_alt": "Autonomous Navigation System",
        "detail_url": "https://github.com/samkwak188/Wisconsin-Autonomous-Perception-Coding-Challenge",
        "live_url": None,
        "demo_url": None,
        "github_url": "https://github.com/samkwak188/Wisconsin-Autonomous-Perception-Coding-Challenge",
        "accent": "#2a3a1a",
        "context": "Computer vision",
        "stack": ["Python", "OpenCV", "RANSAC"],
        "description": (
            "A lane perception exercise using HSV segmentation, geometric filters, and RANSAC "
            "to recover a usable road boundary from a sample driving image."
        ),
    },
    {
        "title": "Intelligent Image Crawler",
        "image_src": "/assets/imagecrawler.png",
        "image_alt": "Data Acquisition Tool",
        "detail_url": "https://github.com/samkwak188/Image-Crawler-with-Face-detection",
        "live_url": None,
        "demo_url": None,
        "github_url": "https://github.com/samkwak188/Image-Crawler-with-Face-detection",
        "accent": "#1a2a4a",
        "context": "Vision data tooling",
        "stack": ["Python", "Web crawling", "Face detection"],
        "description": (
            "A crawler that collects images and filters them with face detection, reducing the "
            "manual cleanup needed before building a small vision dataset."
        ),
    },
    {
        "title": "AI Face Type Analyzer",
        "image_src": "/assets/aifaceanalyze.png",
        "image_alt": "Computer Vision Analysis",
        "detail_url": "https://myfacetype.netlify.app",
        "live_url": "https://myfacetype.netlify.app",
        "demo_url": None,
        "github_url": "https://github.com/samkwak188/AI-Face-Type-Analyzer",
        "accent": "#3a1a5a",
        "context": "Browser machine learning",
        "stack": ["TensorFlow.js", "Responsive web", "Vision"],
        "description": (
            "A web app that runs a small image classifier and returns a simple face-shape result "
            "through a responsive browser interface."
        ),
    },
    {
        "title": "Story Video Automation",
        "image_src": "/assets/faketextstory.png",
        "image_alt": "Text Story Generator",
        "detail_url": "https://my-service-662964498291.us-central1.run.app",
        "live_url": None,
        "demo_url": None,
        "github_url": "https://github.com/samkwak188/Fake-Text-Story-Video-Generator---Complete-Version",
        "accent": "#1a3050",
        "context": "Media automation",
        "stack": ["Cloud Run", "FFmpeg", "Rendering"],
        "description": (
            "A cloud service that turns a text conversation into a captioned short video, "
            "including layout, timing, and server-side rendering."
        ),
    },
    {
        "title": "Viral Video Generator",
        "image_src": "/assets/youtubeshorts.png",
        "image_alt": "Automated Content Pipeline",
        "detail_url": "https://www.youtube.com/watch?v=VhmSVoiDHdU",
        "demo_url": "https://www.youtube.com/watch?v=VhmSVoiDHdU",
        "live_url": None,
        "github_url": "https://github.com/samkwak188/GoViral-Wizard---youtube-shorts-tiktok-video-creator",
        "accent": "#6a2a1a",
        "context": "GoViral",
        "stack": ["FFmpeg", "Voice", "Publishing"],
        "description": (
            "A short-video workflow that combines voiceover, captions, background media, FFmpeg "
            "rendering, and publishing in one tool."
        ),
    },
    {
        "title": "EPL Match Result Predictor",
        "image_src": "/assets/epl.png",
        "image_alt": "Predictive Analytics Dashboard",
        "detail_url": "https://epl-match-result-predictor-3.onrender.com",
        "live_url": None,
        "demo_url": None,
        "github_url": "https://github.com/samkwak188/EPL-Match-Result-Predictor",
        "accent": "#1a1a3a",
        "context": "Predictive analytics",
        "stack": ["Python", "Machine learning", "Dash"],
        "description": (
            "A match prediction app that cleans football data, runs a trained model, and presents "
            "English Premier League forecasts in a browser dashboard."
        ),
    },
]

ENGINEERING_PROJECTS = [
    {
        "id": "engineering-card-1",
        "title": "Kitchen Wastewater Purifier",
        "image_src": "/assets/kitchen.png",
        "image_alt": "Environmental Engineering Prototype",
        "accent": "#2a3a2a",
        "context": "Mechanical prototype",
        "stack": ["Filtration", "Fabrication", "Testing"],
        "description": (
            "A working multi-stage purifier that separates oil and food particles from kitchen "
            "wastewater using mechanical filtration and absorbent media."
        ),
    },
    {
        "id": "engineering-card-2",
        "title": "4D Home Cinema Helmet",
        "image_src": "/assets/4dhelmet.png",
        "image_alt": "Embedded Systems Project",
        "accent": "#3a2a1a",
        "context": "World Robot Olympiad",
        "stack": ["Embedded control", "CAD", "Fabrication"],
        "description": (
            "A home cinema helmet that synchronizes motion, mist, light, and scent with video. "
            "The project won first place at World Robot Olympiad Korea."
        ),
    },
    {
        "id": "engineering-card-3",
        "title": "Humanoid Robotics Control",
        "image_src": "/assets/humanoids.png",
        "image_alt": "Robotics Control System",
        "accent": "#1a2a3a",
        "context": "Robotics control",
        "stack": ["C", "Servo control", "3D printing"],
        "description": (
            "A set of small humanoid robots programmed in C to perform synchronized movement. "
            "I tuned servo sequences and fabricated replacement parts with a 3D printer."
        ),
    },
]

ALL_PROJECTS = RECENT_PROJECTS + CODING_PROJECTS

IMPACT_METRICS = [
    {"label": "Years Building", "value": "3+"},
    {"label": "Projects Shipped", "value": "20+"},
    {"label": "Domains", "value": "AI / Full Stack"},
]

TECH_STACK = [
    {
        "category": "Languages",
        "items": [
            "Python",
            "Java",
            "C/C++",
            "SQL",
            "TypeScript/JavaScript",
            "R",
            "Three.js",
            "Swift",
            "Rust",
            "Bash",
        ],
    },
    {
        "category": "Frameworks & Databases",
        "items": [
            "Next.js",
            "Node.js",
            "React",
            "Dash",
            "React Native",
            "FastAPI",
            "Flask",
            "PostgreSQL",
            "MySQL",
            "MongoDB",
            "Firebase",
        ],
    },
    {
        "category": "ML, AI & Data",
        "items": [
            "PyTorch",
            "TensorFlow.js",
            "YOLO",
            "OpenCV",
            "scikit-learn",
            "Pandas",
            "NumPy",
            "LightFM",
            "Word2Vec",
            "Random Forest",
            "SVD",
        ],
    },
    {
        "category": "Cloud, DevOps & Tools",
        "items": [
            "Google Cloud Platform (GCP)",
            "Azure",
            "Google Cloud Run",
            "Render",
            "Vercel",
            "Docker",
            "GitHub Actions",
            "Git",
            "Linux",
            "Fusion 360",
            "Eclipse",
            "VS Code",
            "Cypress",
            "Jenkins",
            "Angular",
            "Vue",
            "Figma",
            "REST APIs",
        ],
    },
]


# Employer-facing content. The complete project archive above remains available in
# the coverflow section; these records provide a focused first read.
CONTACT = {
    "email": "mailto:ckwak7@wisc.edu",
    "linkedin": "https://www.linkedin.com/in/changyong-kwak/",
    "github": "https://github.com/samkwak188",
    "resume": "/assets/changyong-kwak-resume.pdf",
}

FEATURED_WORK = [
    {
        "title": "Robot control platform",
        "context": "Contoro Robotics",
        "summary": (
            "A browser-to-robot control service for three Isaac Sim robots. I built the "
            "React and TypeScript interface and the FastAPI service that carried commands "
            "through ROS 2, then tested cancellation, timeouts, and concurrent requests."
        ),
        "flow": ["React + TypeScript", "FastAPI", "ROS 2", "Isaac Sim"],
        "link_label": "See the experience",
        "link": "#experience",
        "external": False,
    },
    {
        "title": "Brick Agent Harness",
        "context": "N+1 Institute at UW-Madison",
        "summary": (
            "A local evaluation platform for tool-using agents. It keeps model behavior "
            "separate from typed tools, graders, and immutable run evidence so experiments "
            "can be repeated and audited."
        ),
        "flow": ["Domain packs", "Typed executor", "Strict graders", "Run evidence"],
        "link_label": "View the repository",
        "link": "https://github.com/EdgeHarness/Brick-Agent-Harness",
        "external": True,
    },
    {
        "title": "LiveClaw",
        "context": "Independent project",
        "summary": (
            "A desktop control loop that observes the screen, takes an action, and checks "
            "the result. The Rust and Python stack pauses for input conflicts and blocks "
            "or confirms risky actions."
        ),
        "flow": ["Observe", "Plan", "Act", "Verify"],
        "link_label": "View the repository",
        "link": "https://github.com/samkwak188/LiveClaw",
        "external": True,
    },
]

EXPERIENCE = [
    {
        "company": "Contoro Robotics",
        "role": "Software Engineering Intern",
        "dates": "Feb 2026 - Jul 2026",
        "description": (
            "Built a browser-based robot control service across React, FastAPI, ROS 2, "
            "and Isaac Sim. Focused on concurrency, cancellation, timeout recovery, and "
            "repeatable CI checks."
        ),
    },
    {
        "company": "N+1 Institute at UW-Madison",
        "role": "AI Research and Software Engineering Intern",
        "dates": "Jun 2026 - Aug 2026",
        "description": (
            "Built Brick, a local evaluation harness for tool-using agents, while working "
            "with Brix Coworking and technical mentors from Qualcomm. Qualified 528 "
            "synthetic cases and hardened evidence recovery on Windows ARM64."
        ),
    },
    {
        "company": "CATS Lab at UW-Madison",
        "role": "Undergraduate Researcher",
        "dates": "May 2026 - Present",
        "description": (
            "Researching how fixed-camera drift changes downstream traffic measurements. "
            "Also reproduced an upstream PyTorch Transformer on 97,499 observations and "
            "documented a session-label confound before making a generalization claim."
        ),
    },
    {
        "company": "GoViral",
        "role": "Creator and Full-Stack Developer",
        "dates": "Oct 2024 - Feb 2026",
        "description": (
            "Built and ran a cloud video workflow used by 40+ beta users. Automated rendering, "
            "captions, voiceover, and publishing to cut a typical workflow from about two "
            "hours to under ten minutes."
        ),
    },
]

SKILL_GROUPS = [
    {
        "id": "systems",
        "label": "Systems",
        "icon": "ph:terminal-window",
        "description": (
            "I design boundaries, cancellation paths, evidence, and failure behavior before "
            "optimizing the happy path."
        ),
        "items": ["Python", "Rust", "C / C++", "FastAPI", "Linux", "PostgreSQL"],
    },
    {
        "id": "product",
        "label": "Product",
        "icon": "ph:browser",
        "description": (
            "I carry product work from interaction design through APIs, persistence, and "
            "deployment, with the interface kept close to real system state."
        ),
        "items": ["TypeScript", "React", "Next.js", "Expo", "Supabase", "Dash"],
    },
    {
        "id": "robotics",
        "label": "Robotics",
        "icon": "ph:robot",
        "description": (
            "I connect browser controls to simulated or physical machines with explicit "
            "timeouts, interruption, and repeatable integration checks."
        ),
        "items": ["ROS 2", "Isaac Sim", "OpenCV", "Servo control", "Fusion 360", "3D printing"],
    },
    {
        "id": "intelligence",
        "label": "ML and data",
        "icon": "ph:graph",
        "description": (
            "I treat models as measurable system components: grounded inputs, honest claims, "
            "strict evaluation, and traceable outputs."
        ),
        "items": ["PyTorch", "scikit-learn", "Pandas", "NumPy", "Computer vision", "Evaluation"],
    },
    {
        "id": "delivery",
        "label": "Delivery",
        "icon": "ph:cloud-check",
        "description": (
            "I make builds reproducible and observable across local development, CI, cloud "
            "services, and production recovery paths."
        ),
        "items": ["Docker", "GitHub Actions", "GCP", "Vercel", "Render", "Cypress"],
    },
]
