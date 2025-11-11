# Resumitory Backend

FastAPI backend for Resumitory - Resume version control and job application tracker.

## 🚀 Quick Start

### Prerequisites

- Python 3.11 or higher
- pip (Python package manager)
- Supabase account (free tier)

### Installation

1. **Create virtual environment:**

```bash
python -m venv venv
```

2. **Activate virtual environment:**

```bash
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

3. **Install dependencies:**

```bash
pip install -r requirements.txt
```

4. **Set up environment variables:**

```bash
# Copy example env file
cp .env.example .env

# Edit .env with your Supabase credentials
```

Required environment variables:
- `SUPABASE_URL`: Your Supabase project URL
- `SUPABASE_KEY`: Your Supabase anon key
- `SUPABASE_JWT_SECRET`: Your Supabase JWT secret (from Project Settings > API)

5. **Run the development server:**

```bash
uvicorn app.main:app --reload --port 8000
```

The API will be available at:
- **API**: http://localhost:8000
- **Interactive docs**: http://localhost:8000/docs
- **Alternative docs**: http://localhost:8000/redoc

---

## 📁 Project Structure

```
resumitory-backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI app entry point
│   ├── config.py               # Configuration settings
│   ├── database.py             # Database session management
│   ├── auth/
│   │   ├── __init__.py
│   │   ├── dependencies.py     # JWT verification
│   │   └── router.py           # Auth endpoints
│   ├── resumes/
│   │   ├── __init__.py
│   │   ├── models.py           # Resume SQLModel
│   │   ├── router.py           # Resume CRUD endpoints
│   │   └── storage.py          # Supabase Storage helpers
│   ├── applications/
│   │   ├── __init__.py
│   │   ├── models.py           # Application SQLModel
│   │   └── router.py           # Application CRUD endpoints
│   └── rounds/                 # Interview rounds (V1.1)
│       ├── __init__.py
│       ├── models.py
│       └── router.py
├── tests/                      # Unit tests
├── requirements.txt            # Python dependencies
├── .env.example                # Example environment variables
└── README.md                   # This file
```

---

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the `resumitory-backend` directory:

```env
# Supabase Configuration
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-key-here
SUPABASE_JWT_SECRET=your-jwt-secret-here

# API Configuration (optional)
API_HOST=0.0.0.0
API_PORT=8000
```

### Getting Supabase Credentials

1. Go to [Supabase Dashboard](https://app.supabase.com)
2. Select your project
3. Go to **Project Settings** > **API**
4. Copy:
   - **Project URL** → `SUPABASE_URL`
   - **anon public** key → `SUPABASE_KEY`
   - **JWT Secret** → `SUPABASE_JWT_SECRET`

---

## 📚 API Endpoints

### Authentication

```
GET  /auth/me              # Get current user (requires JWT token)
```

### Resumes

```
GET    /resumes/           # List user's resumes
POST   /resumes/           # Upload new resume (multipart/form-data)
GET    /resumes/{id}       # Get specific resume
PATCH  /resumes/{id}       # Update resume metadata
DELETE /resumes/{id}       # Delete resume and files
POST   /resumes/{id}/clone # Clone resume (creates copy)
```

### Applications

```
GET    /applications/                # List applications (with filters)
POST   /applications/                # Create application
POST   /applications/quick           # Quick add (minimal fields)
GET    /applications/{id}            # Get application details
PATCH  /applications/{id}            # Update application
DELETE /applications/{id}            # Delete application
GET    /applications/stats/summary   # Get stats and upcoming follow-ups
```

**Query Parameters for GET /applications/:**
- `status_filter` - Filter by status (applied, interview, offer, rejected, archived)
- `search` - Search in company name or role (case-insensitive)
- `resume_id` - Filter by specific resume
GET    /applications/{id}            # Get application
PATCH  /applications/{id}            # Update application
DELETE /applications/{id}            # Delete application
POST   /applications/quick           # Quick add application
GET    /applications/search?q={query} # Search applications
```

### Interview Rounds - V1.1 (Coming Soon)

```
GET    /applications/{id}/rounds     # List rounds
POST   /applications/{id}/rounds     # Add round
PATCH  /rounds/{id}                  # Update round
DELETE /rounds/{id}                  # Delete round
```

### Utility

```
GET  /                     # Root endpoint with API info
GET  /health               # Health check
```

---

## 🧪 Testing

### Manual Testing with Swagger UI

1. Start the server: `uvicorn app.main:app --reload`
2. Go to http://localhost:8000/docs
3. Click "Authorize" button
4. Get a JWT token from frontend Supabase auth
5. Enter token in format: `Bearer <your-token>`
6. Test endpoints

### Running Tests (Coming Soon)

```bash
pytest tests/
```

---

## 🗄️ Database Schema

The database is managed by Supabase (PostgreSQL). See `docs/DATABASE.md` for complete schema.

### Key Tables

**resumes**
- id (UUID, PK)
- user_id (UUID, FK → users.id)
- name (String)
- notes (Text, nullable)
- pdf_url (String)
- tex_url (String, nullable)
- tags (String[], nullable)
- created_at, updated_at (Timestamp)

**applications**
- id (UUID, PK)
- user_id (UUID, FK → users.id)
- company (String)
- role (String)
- date_applied (Date)
- status (Enum: applied, interview, offer, rejected, archived)
- notes (Text, nullable)
- resume_id (UUID, FK → resumes.id, nullable)
- follow_up_date (Date, nullable)
- last_updated, created_at (Timestamp)

**interview_rounds** (V1.1)
- id (UUID, PK)
- application_id (UUID, FK → applications.id)
- round_number (Integer)
- round_type (String)
- scheduled_date, completed_date (Date, nullable)
- notes (Text, nullable)
- status (Enum: scheduled, completed, cancelled)
- created_at (Timestamp)

---

## 🔐 Authentication

Authentication is handled by **Supabase Auth**. The backend verifies JWT tokens.

### How it Works

1. Frontend authenticates users via Supabase Auth
2. Supabase returns JWT token
3. Frontend sends token in `Authorization` header: `Bearer <token>`
4. Backend verifies token using `get_current_user()` dependency
5. `user_id` is extracted from JWT and used for data access

### Protected Endpoints

All endpoints except `/` and `/health` require authentication.

---

## 🚀 Deployment

### Railway

1. Create new project on [Railway](https://railway.app)
2. Connect GitHub repository
3. Add environment variables
4. Deploy!

### Render

1. Create new Web Service on [Render](https://render.com)
2. Connect GitHub repository
3. Build command: `pip install -r requirements.txt`
4. Start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. Add environment variables
6. Deploy!

---

## 📝 Development Guidelines

### Code Style

- Use type hints everywhere
- Follow PEP 8
- Use SQLModel (not raw SQLAlchemy)
- Snake_case for Python variables/functions
- Clear docstrings for functions

### Commit Messages

Use conventional commits:
- `feat:` New features
- `fix:` Bug fixes
- `docs:` Documentation
- `refactor:` Code refactoring
- `test:` Tests

Example:
```
feat: Add resume upload with LaTeX support

- Implement file upload to Supabase Storage
- Support both PDF and .tex files
- Add file validation
```

---

## 🐛 Troubleshooting

### Common Issues

**Issue: `ModuleNotFoundError: No module named 'app'`**
- Make sure you're in the `resumitory-backend` directory
- Ensure virtual environment is activated
- Run: `pip install -r requirements.txt`

**Issue: Database connection error**
- Check Supabase credentials in `.env`
- Ensure Supabase project is active
- Verify `SUPABASE_URL` format (should include https://)

**Issue: JWT verification fails**
- Check `SUPABASE_JWT_SECRET` is correct
- Get fresh token from frontend
- Ensure token format: `Bearer <token>`

**Issue: CORS errors**
- Check frontend URL in `app/main.py` CORS config
- Ensure frontend is running on expected port (5173)

---

## 📚 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLModel Documentation](https://sqlmodel.tiangolo.com/)
- [Supabase Documentation](https://supabase.com/docs)
- [Action Plan](../ACTION_PLAN.md)

---

## 📄 License

MIT License - see [LICENSE](../LICENSE) file for details.
