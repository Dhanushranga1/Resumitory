# Resumitory - AI Agent Instructions

## Project Overview
**Resumitory** is a resume version control and job application tracker. Core differentiator: explicit linking between resume versions and applications (no competitor does this well).

**Stack:** FastAPI (Python) + React/TypeScript + Supabase (PostgreSQL + Auth + Storage)  
**Goal:** Ship MVP in 4 weeks, V1.1 in 8 weeks

## Architecture

### Backend Structure (`resumitory-backend/`)
```
app/
├── main.py              # FastAPI app with CORS, router registration
├── config.py            # Supabase credentials from .env (use pydantic_settings)
├── database.py          # SQLModel session management
├── auth/
│   ├── router.py        # Auth endpoints (Supabase handles auth)
│   └── dependencies.py  # JWT verification via get_current_user()
├── resumes/
│   ├── models.py        # Resume SQLModel with pdf_url, tex_url, tags
│   ├── router.py        # CRUD + clone endpoint
│   └── storage.py       # Supabase Storage helpers (upload_file, delete_file)
├── applications/
│   ├── models.py        # Application with status enum, resume_id FK
│   └── router.py        # CRUD + quick-add endpoint + search/filter
└── rounds/              # V1.1: Interview round tracking
```

### Frontend Structure (`resumitory-frontend/`)
```
src/
├── lib/
│   ├── supabase.ts      # Supabase client for auth
│   └── api.ts           # Axios instance with JWT interceptor
├── components/ui/       # shadcn/ui components (install as needed)
├── pages/
│   ├── auth/            # Login.tsx, Signup.tsx
│   ├── Dashboard.tsx    # Stats overview
│   ├── ResumeLibrary.tsx
│   └── ApplicationTracker.tsx
└── features/
    ├── resumes/         # ResumeCard, UploadModal, useResumes hook
    └── applications/    # ApplicationTable, useApplications hook
```

## Critical Patterns

### 1. Authentication Flow
- **Backend:** Verify Supabase JWT via `get_current_user()` dependency
- **Frontend:** Store session in Supabase client, add token to axios interceptor
- Never store tokens in localStorage manually; use Supabase's built-in session management

### 2. Resume-to-Application Linking
- Applications have `resume_id` FK (nullable) to `resumes.id`
- UI must show resume name in application list/detail
- Dropdown in application form to select from user's resumes
- This is the **core differentiator** - surface it prominently

### 3. File Upload Pattern
```python
# Backend: resumes/storage.py
- Use Supabase Storage with user-scoped paths: f"resumes/{user_id}/{unique_id}_{filename}"
- Support both PDF (required) and .tex (optional)
- Return public URLs for storage
```

### 4. State Management
- **Server State:** React Query (`@tanstack/react-query`) for all API calls
- **Client State:** Zustand for UI state (modals, filters)
- Always invalidate queries after mutations: `queryClient.invalidateQueries(['resumes'])`

### 5. Status Enum Handling
```python
# Backend: applications/models.py
status: Enum('applied', 'interview', 'offer', 'rejected', 'archived')
```
- Frontend dropdowns must match backend enum exactly
- Use color coding: blue (applied), yellow (interview), green (offer), red (rejected)

## Development Workflows

### Starting Dev Servers
```bash
# Backend (from project root)
cd resumitory-backend
uvicorn app.main:app --reload --port 8000

# Frontend (from project root)
cd resumitory-frontend
npm run dev
```

### Database Migrations
- Use Supabase SQL Editor or Alembic
- Schema defined in `kickoff.md` - follow it exactly
- Critical indexes: `applications.user_id`, `applications.status`, `applications.follow_up_date`

### Testing Endpoints
- Use `/docs` (Swagger UI) for API testing
- Obtain Supabase token from frontend auth, paste in "Authorize" button
- Test authentication first before CRUD endpoints

## Project-Specific Conventions

### 1. Minimal Form Pattern (Quick Add)
```typescript
// Quick add requires only: company, role, resume_id
// Full form includes: notes, follow_up_date, status
```
- Ship quick-add modal for bulk apply sessions
- Reduce friction during job search (users apply to 100+ jobs)

### 2. Resume Cloning
```python
# POST /resumes/{id}/clone
# Creates copy with name += " (Copy)"
```
- Users tweak existing versions frequently
- Clone should duplicate file URLs (not re-upload)

### 3. Follow-Up System (V1.1)
- `applications.follow_up_date` triggers email reminders
- Backend cron: daily check for `follow_up_date <= today AND status != 'rejected'`
- Email includes resume name to help user prepare

### 4. Search Implementation
```python
# GET /applications/?search={query}
# Search both company AND role fields (case-insensitive)
statement.where(or_(
    Application.company.ilike(f"%{search}%"),
    Application.role.ilike(f"%{search}%")
))
```

## V1.1 Critical Features (Week 5-8)
1. **Interview Rounds:** Track multi-stage interviews (phone → technical → onsite)
2. **Follow-Up Reminders:** Email notifications when `follow_up_date` arrives
3. **Search & Filter:** Essential at 50+ applications
4. **Quick Add Modal:** Fast entry during bulk apply
5. **Resume Cloning:** Tweak from existing versions

## Key Files to Reference
- **Schema:** See `kickoff.md` lines 220-290 for exact database structure
- **API Endpoints:** See `kickoff.md` lines 540-590 for all routes
- **UI Patterns:** See `copilotinstructions.md` lines 750-850 for component examples
- **Tech Stack Rationale:** See `kickoff.md` lines 345-370

## Common Gotchas
- **LaTeX Support:** Must handle `.tex` uploads separately from PDFs (store `tex_url`)
- **CORS:** Frontend runs on `:5173`, backend on `:8000` - configure properly
- **Row Level Security:** Supabase RLS must match `user_id` from JWT
- **File Size Limits:** Supabase free tier = 500MB total; validate uploads
- **Enum Case:** Backend uses lowercase enums ('applied' not 'Applied')

## What NOT to Build
❌ AI resume generation  
❌ ATS optimization tools  
❌ Job board scrapers  
❌ Mobile apps (web-first)  

Focus on **organization clarity** over feature bloat.

## Success Criteria
- User uploads ≥1 resume: **80%+**
- User adds ≥3 applications: **60%+**
- Resume-to-app linking rate: **70%+** (proves core value)

## Code Style
- **Backend:** Use SQLModel (not raw SQLAlchemy), type hints everywhere
- **Frontend:** Strict TypeScript, no `any` types
- **UI:** Tailwind utility classes, shadcn/ui components (no custom CSS)
- **Naming:** Snake_case (Python), camelCase (TypeScript)

## When Stuck
1. Check existing patterns in `copilotinstructions.md` (lines 200-650)
2. Verify schema against `kickoff.md` database design
3. Supabase issues: Check RLS policies and JWT claims
4. CRUD patterns: All follow same structure (list, get, create, update, delete)
