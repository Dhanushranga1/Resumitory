# 📚 Resumitory

> **Resume chaos, solved.** Track every version. Remember every application. Finally organized.

[![MIT License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![TypeScript](https://img.shields.io/badge/typescript-5.0+-blue.svg)](https://www.typescriptlang.org/)

---

## 🎯 What is Resumitory?

Resumitory is a **resume version control and job application tracker** built for people who create multiple resume versions and apply to 100+ jobs. It's the only tool that explicitly links each application to the exact resume version you sent.

### Core Features

- 📚 **Resume Library** — Store all versions (PDF + LaTeX source) with notes
- 🧾 **Application Tracker** — Manage every submission with status tracking
- 🔗 **Smart Linking** — Connect exact resume to each application (our differentiator!)
- 🔔 **Follow-Up System** — Never miss critical follow-ups
- 📊 **Interview Rounds** — Track multi-stage interview processes
- 🧭 **Clean Dashboard** — See everything at a glance

### What Resumitory is NOT

❌ Not an AI resume builder  
❌ Not an ATS optimization tool  
❌ Not a job board aggregator  

We focus on **organization clarity** over feature bloat.

---

## 🚀 Tech Stack

**Frontend:**
- React 18 + TypeScript
- Vite (build tool)
- Tailwind CSS + shadcn/ui
- React Query (server state)
- Zustand (client state)

**Backend:**
- FastAPI (Python 3.11+)
- SQLModel (ORM)
- Supabase (PostgreSQL + Auth + Storage)
- JWT authentication

**Infrastructure:**
- Supabase (database + auth + file storage)
- Railway/Render (backend hosting)
- Vercel (frontend hosting)

---

## 📂 Project Structure

```
Resumitory/
├── resumitory-backend/          # FastAPI backend
│   ├── app/
│   │   ├── main.py             # FastAPI app entry
│   │   ├── config.py           # Environment config
│   │   ├── database.py         # Database session
│   │   ├── auth/               # Authentication
│   │   ├── resumes/            # Resume management
│   │   ├── applications/       # Application tracking
│   │   └── rounds/             # Interview rounds (V1.1)
│   ├── requirements.txt
│   └── README.md
│
├── resumitory-frontend/         # React frontend
│   ├── src/
│   │   ├── lib/                # API clients
│   │   ├── components/         # UI components
│   │   ├── pages/              # Page components
│   │   └── features/           # Feature modules
│   ├── package.json
│   └── README.md
│
├── .github/
│   └── copilot-instructions.md # AI agent guidelines
├── ACTION_PLAN.md              # Detailed development plan
├── kickoff.md                  # Project blueprint
└── README.md                   # This file
```

---

## 🛠️ Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+
- Git
- Supabase account (free tier)

### 1. Clone Repository

```bash
git clone https://github.com/Dhanushranga1/Resumitory.git
cd Resumitory
```

### 2. Backend Setup

```bash
cd resumitory-backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Create .env file (see backend/README.md)
cp .env.example .env
# Edit .env with your Supabase credentials

# Run backend
uvicorn app.main:app --reload --port 8000
```

Backend will run at: http://localhost:8000  
API docs: http://localhost:8000/docs

### 3. Frontend Setup

```bash
cd resumitory-frontend
npm install

# Create .env file (see frontend/README.md)
cp .env.example .env
# Edit .env with API URL and Supabase credentials

# Run frontend
npm run dev
```

Frontend will run at: http://localhost:5173

---

## 📖 Documentation

- [Action Plan](ACTION_PLAN.md) - Detailed 8-week development roadmap
- [Backend README](resumitory-backend/README.md) - Backend setup and API docs
- [Frontend README](resumitory-frontend/README.md) - Frontend setup guide
- [Project Blueprint](kickoff.md) - Complete project research and design
- [AI Agent Instructions](.github/copilot-instructions.md) - Guidelines for AI assistants

---

## 🎯 Development Phases

### ✅ Phase 1: Backend Foundation (Week 1-2)
- FastAPI setup with Supabase
- Authentication with JWT
- Resume CRUD with file upload
- Application CRUD with search/filter

### ⏳ Phase 2: Frontend Foundation (Week 3-4)
- React setup with TypeScript
- Auth pages (Login/Signup)
- Dashboard with stats
- Resume Library UI
- Application Tracker UI

### 🔜 Phase 3: V1.1 Features (Week 5-6)
- Interview round tracking
- Follow-up reminder system
- Resume cloning
- Quick-add modal
- Enhanced search/filter

### 🔜 Phase 4: Testing & Launch (Week 7-8)
- End-to-end testing
- Performance optimization
- Documentation
- Production deployment

---

## 🤝 Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details.

### Development Workflow

1. Create a feature branch: `git checkout -b feat/your-feature`
2. Make changes with clear commits (use conventional commits)
3. Test thoroughly
4. Submit pull request

### Commit Convention

```
feat: Add new feature
fix: Fix bug
docs: Update documentation
style: Format code
refactor: Refactor code
test: Add tests
chore: Update build process
```

---

## 📊 Success Metrics

### Activation
- 80%+ users upload ≥1 resume
- 60%+ users add ≥3 applications
- 70%+ users link resumes to applications (proves core value!)

### Retention
- 50%+ Day 7 retention
- 40%+ Day 30 retention
- 30%+ Day 90 retention

---

## 🙏 Acknowledgments

Built for job seekers who are tired of losing track of their applications. Special thanks to the r/cscareerquestions community for validating the need.

---

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

---

## 🔗 Links

- **Live Demo:** Coming soon!
- **Documentation:** [Read the docs](https://github.com/Dhanushranga1/Resumitory/wiki)
- **Report Bug:** [Create an issue](https://github.com/Dhanushranga1/Resumitory/issues)
- **Feature Request:** [Create an issue](https://github.com/Dhanushranga1/Resumitory/issues)

---

**Made with ❤️ for job seekers everywhere**

*Remember: Perfect is the enemy of done. Ship fast, iterate faster.* 🚀
