# Resumitory - AI Agent Build Instructions

> **Project**: Resumitory - Resume version control + job application tracker  
> **Stack**: FastAPI (Backend) + React/TypeScript (Frontend) + Supabase (Database/Auth/Storage)  
> **Goal**: Ship MVP in 4 weeks, V1.1 in 8 weeks

---

## 🎯 Project Overview

**What We're Building:**
A web app that helps job seekers:
1. Store multiple resume versions (PDF + LaTeX source files)
2. Track job applications
3. Link each application to the exact resume version used
4. Set follow-up reminders
5. Track multi-stage interviews

**What We're NOT Building:**
- AI resume generation
- ATS optimization tools
- Job board scrapers
- Social features
- Mobile apps (web-first)

**Core Differentiator:** Resume versioning + explicit linking to applications (no competitor does this well)

---

## 📐 Technical Architecture

### Backend (FastAPI)
```
resumitory-backend/
├── app/
│   ├── main.py                 # FastAPI app entry
│   ├── config.py               # Environment variables
│   ├── database.py             # SQLModel/Supabase setup
│   ├── auth/
│   │   ├── __init__.py
│   │   ├── router.py           # Auth endpoints
│   │   └── dependencies.py     # JWT verification
│   ├── resumes/
│   │   ├── __init__.py
│   │   ├── router.py           # Resume CRUD
│   │   ├── models.py           # Resume SQLModel
│   │   └── storage.py          # Supabase Storage helpers
│   ├── applications/
│   │   ├── __init__.py
│   │   ├── router.py           # Application CRUD
│   │   └── models.py           # Application SQLModel
│   ├── rounds/                 # Interview rounds (V1.1)
│   │   ├── __init__.py
│   │   ├── router.py
│   │   └── models.py
│   └── reminders/              # Follow-up system (V1.1)
│       ├── __init__.py
│       ├── router.py
│       └── tasks.py            # Background jobs
├── tests/
├── requirements.txt
├── .env.example
└── README.md
```

### Frontend (React + TypeScript)
```
resumitory-frontend/
├── src/
│   ├── main.tsx
│   ├── App.tsx
│   ├── lib/
│   │   ├── supabase.ts         # Supabase client
│   │   ├── api.ts              # API client (Axios)
│   │   └── utils.ts
│   ├── components/
│   │   ├── ui/                 # shadcn/ui components
│   │   ├── Layout.tsx
│   │   ├── Navbar.tsx
│   │   └── ProtectedRoute.tsx
│   ├── pages/
│   │   ├── auth/
│   │   │   ├── Login.tsx
│   │   │   └── Signup.tsx
│   │   ├── Dashboard.tsx
│   │   ├── ResumeLibrary.tsx
│   │   ├── ApplicationTracker.tsx
│   │   └── ApplicationDetail.tsx
│   ├── features/
│   │   ├── resumes/
│   │   │   ├── ResumeCard.tsx
│   │   │   ├── UploadModal.tsx
│   │   │   └── useResumes.ts   # React Query hooks
│   │   └── applications/
│   │       ├── ApplicationTable.tsx
│   │       ├── ApplicationForm.tsx
│   │       ├── QuickAddModal.tsx
│   │       └── useApplications.ts
│   ├── types/
│   │   └── index.ts            # TypeScript types
│   └── styles/
│       └── globals.css
├── package.json
├── tsconfig.json
├── vite.config.ts
└── tailwind.config.js
```

### Database Schema (Supabase/PostgreSQL)

```sql
-- Users (managed by Supabase Auth)
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  email TEXT UNIQUE NOT NULL,
  name TEXT,
  created_at TIMESTAMP DEFAULT NOW()
);

-- Resumes
CREATE TABLE resumes (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID REFERENCES users(id) ON DELETE CASCADE,
  name TEXT NOT NULL,
  notes TEXT,
  pdf_url TEXT NOT NULL,
  tex_url TEXT,
  tags TEXT[],
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

-- Applications
CREATE TABLE applications (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID REFERENCES users(id) ON DELETE CASCADE,
  company TEXT NOT NULL,
  role TEXT NOT NULL,
  date_applied DATE NOT NULL,
  status TEXT NOT NULL CHECK (status IN ('applied', 'interview', 'offer', 'rejected', 'archived')),
  notes TEXT,
  resume_id UUID REFERENCES resumes(id) ON DELETE SET NULL,
  follow_up_date DATE,
  last_updated TIMESTAMP DEFAULT NOW(),
  created_at TIMESTAMP DEFAULT NOW()
);

-- Interview Rounds (V1.1)
CREATE TABLE interview_rounds (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  application_id UUID REFERENCES applications(id) ON DELETE CASCADE,
  round_number INTEGER NOT NULL,
  round_type TEXT NOT NULL,
  scheduled_date DATE,
  completed_date DATE,
  notes TEXT,
  status TEXT CHECK (status IN ('scheduled', 'completed', 'cancelled')),
  created_at TIMESTAMP DEFAULT NOW()
);

-- Indexes
CREATE INDEX idx_resumes_user_id ON resumes(user_id);
CREATE INDEX idx_applications_user_id ON applications(user_id);
CREATE INDEX idx_applications_status ON applications(user_id, status);
CREATE INDEX idx_applications_follow_up ON applications(follow_up_date) WHERE follow_up_date IS NOT NULL;
CREATE INDEX idx_rounds_application ON interview_rounds(application_id);
```

---

## 🚀 Phase-by-Phase Build Instructions

---

## **PHASE 1: Backend Foundation (Week 1)**

### Day 1-2: Project Setup & Auth

**Tasks:**
1. Initialize FastAPI project
2. Set up Supabase project (database + auth + storage)
3. Implement authentication endpoints

**Code to Generate:**

**File: `app/main.py`**
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.auth.router import router as auth_router
from app.resumes.router import router as resumes_router
from app.applications.router import router as applications_router

app = FastAPI(title="Resumitory API", version="1.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(resumes_router, prefix="/resumes", tags=["resumes"])
app.include_router(applications_router, prefix="/applications", tags=["applications"])

@app.get("/")
def root():
    return {"message": "Resumitory API"}
```

**File: `app/config.py`**
```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SUPABASE_URL: str
    SUPABASE_KEY: str
    SUPABASE_JWT_SECRET: str
    
    class Config:
        env_file = ".env"

settings = Settings()
```

**File: `app/auth/dependencies.py`**
```python
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from app.config import settings

security = HTTPBearer()

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        payload = jwt.decode(
            token, 
            settings.SUPABASE_JWT_SECRET, 
            algorithms=["HS256"],
            audience="authenticated"
        )
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
        return user_id
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
```

**File: `app/auth/router.py`**
```python
from fastapi import APIRouter, Depends
from app.auth.dependencies import get_current_user

router = APIRouter()

@router.get("/me")
async def get_me(user_id: str = Depends(get_current_user)):
    # Supabase handles auth, so we just return user_id from JWT
    return {"user_id": user_id}
```

**Testing Criteria:**
- [ ] FastAPI runs on `http://localhost:8000`
- [ ] `/docs` shows Swagger UI
- [ ] `/auth/me` returns 401 without token
- [ ] `/auth/me` returns user_id with valid Supabase token

---

### Day 3-4: Resume CRUD

**Tasks:**
1. Create Resume SQLModel
2. Implement resume CRUD endpoints
3. Set up Supabase Storage integration

**File: `app/resumes/models.py`**
```python
from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

class ResumeBase(SQLModel):
    name: str
    notes: Optional[str] = None
    tags: Optional[list[str]] = None

class Resume(ResumeBase, table=True):
    __tablename__ = "resumes"
    
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="users.id")
    pdf_url: str
    tex_url: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class ResumeCreate(ResumeBase):
    pass

class ResumeResponse(ResumeBase):
    id: UUID
    pdf_url: str
    tex_url: Optional[str]
    created_at: datetime
    updated_at: datetime
```

**File: `app/resumes/storage.py`**
```python
from supabase import create_client
from app.config import settings
import uuid

supabase = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)

async def upload_file(file_content: bytes, filename: str, user_id: str, file_type: str) -> str:
    """Upload file to Supabase Storage and return public URL"""
    bucket_name = "resumes"
    file_ext = filename.split(".")[-1]
    unique_filename = f"{user_id}/{uuid.uuid4()}.{file_ext}"
    
    supabase.storage.from_(bucket_name).upload(unique_filename, file_content)
    
    # Get public URL
    url = supabase.storage.from_(bucket_name).get_public_url(unique_filename)
    return url

async def delete_file(file_url: str):
    """Delete file from Supabase Storage"""
    # Extract path from URL
    bucket_name = "resumes"
    path = file_url.split(f"{bucket_name}/")[-1]
    supabase.storage.from_(bucket_name).remove([path])
```

**File: `app/resumes/router.py`**
```python
from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from sqlmodel import Session, select
from app.database import get_session
from app.auth.dependencies import get_current_user
from app.resumes.models import Resume, ResumeCreate, ResumeResponse
from app.resumes.storage import upload_file, delete_file
from typing import Optional

router = APIRouter()

@router.post("/", response_model=ResumeResponse)
async def create_resume(
    name: str = Form(...),
    notes: Optional[str] = Form(None),
    pdf_file: UploadFile = File(...),
    tex_file: Optional[UploadFile] = File(None),
    session: Session = Depends(get_session),
    user_id: str = Depends(get_current_user)
):
    # Upload PDF
    pdf_content = await pdf_file.read()
    pdf_url = await upload_file(pdf_content, pdf_file.filename, user_id, "pdf")
    
    # Upload TEX if provided
    tex_url = None
    if tex_file:
        tex_content = await tex_file.read()
        tex_url = await upload_file(tex_content, tex_file.filename, user_id, "tex")
    
    # Create resume record
    resume = Resume(
        user_id=user_id,
        name=name,
        notes=notes,
        pdf_url=pdf_url,
        tex_url=tex_url
    )
    session.add(resume)
    session.commit()
    session.refresh(resume)
    
    return resume

@router.get("/", response_model=list[ResumeResponse])
async def list_resumes(
    session: Session = Depends(get_session),
    user_id: str = Depends(get_current_user)
):
    statement = select(Resume).where(Resume.user_id == user_id)
    resumes = session.exec(statement).all()
    return resumes

@router.get("/{resume_id}", response_model=ResumeResponse)
async def get_resume(
    resume_id: str,
    session: Session = Depends(get_session),
    user_id: str = Depends(get_current_user)
):
    resume = session.get(Resume, resume_id)
    if not resume or resume.user_id != user_id:
        raise HTTPException(status_code=404, detail="Resume not found")
    return resume

@router.delete("/{resume_id}")
async def delete_resume(
    resume_id: str,
    session: Session = Depends(get_session),
    user_id: str = Depends(get_current_user)
):
    resume = session.get(Resume, resume_id)
    if not resume or resume.user_id != user_id:
        raise HTTPException(status_code=404, detail="Resume not found")
    
    # Delete files from storage
    await delete_file(resume.pdf_url)
    if resume.tex_url:
        await delete_file(resume.tex_url)
    
    # Delete record
    session.delete(resume)
    session.commit()
    
    return {"message": "Resume deleted"}

@router.post("/{resume_id}/clone", response_model=ResumeResponse)
async def clone_resume(
    resume_id: str,
    session: Session = Depends(get_session),
    user_id: str = Depends(get_current_user)
):
    original = session.get(Resume, resume_id)
    if not original or original.user_id != user_id:
        raise HTTPException(status_code=404, detail="Resume not found")
    
    # Create clone (same files, new name)
    clone = Resume(
        user_id=user_id,
        name=f"{original.name} (Copy)",
        notes=original.notes,
        pdf_url=original.pdf_url,  # Reuse same file
        tex_url=original.tex_url,
        tags=original.tags
    )
    session.add(clone)
    session.commit()
    session.refresh(clone)
    
    return clone
```

**Testing Criteria:**
- [ ] POST `/resumes/` uploads PDF and creates record
- [ ] GET `/resumes/` returns user's resumes
- [ ] DELETE `/resumes/{id}` removes resume and files
- [ ] POST `/resumes/{id}/clone` creates copy

---

### Day 5-7: Application CRUD

**Tasks:**
1. Create Application SQLModel
2. Implement application CRUD endpoints
3. Add resume linking functionality

**File: `app/applications/models.py`**
```python
from sqlmodel import SQLModel, Field
from datetime import datetime, date
from typing import Optional
from uuid import UUID, uuid4
from enum import Enum

class StatusEnum(str, Enum):
    applied = "applied"
    interview = "interview"
    offer = "offer"
    rejected = "rejected"
    archived = "archived"

class ApplicationBase(SQLModel):
    company: str
    role: str
    date_applied: date
    status: StatusEnum
    notes: Optional[str] = None
    resume_id: Optional[UUID] = None
    follow_up_date: Optional[date] = None

class Application(ApplicationBase, table=True):
    __tablename__ = "applications"
    
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="users.id")
    last_updated: datetime = Field(default_factory=datetime.utcnow)
    created_at: datetime = Field(default_factory=datetime.utcnow)

class ApplicationCreate(ApplicationBase):
    pass

class ApplicationUpdate(SQLModel):
    status: Optional[StatusEnum] = None
    notes: Optional[str] = None
    follow_up_date: Optional[date] = None
    resume_id: Optional[UUID] = None

class ApplicationResponse(ApplicationBase):
    id: UUID
    created_at: datetime
    last_updated: datetime
```

**File: `app/applications/router.py`**
```python
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlmodel import Session, select, or_
from app.database import get_session
from app.auth.dependencies import get_current_user
from app.applications.models import Application, ApplicationCreate, ApplicationUpdate, ApplicationResponse

router = APIRouter()

@router.post("/", response_model=ApplicationResponse)
async def create_application(
    application: ApplicationCreate,
    session: Session = Depends(get_session),
    user_id: str = Depends(get_current_user)
):
    db_application = Application(**application.dict(), user_id=user_id)
    session.add(db_application)
    session.commit()
    session.refresh(db_application)
    return db_application

@router.get("/", response_model=list[ApplicationResponse])
async def list_applications(
    status: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    session: Session = Depends(get_session),
    user_id: str = Depends(get_current_user)
):
    statement = select(Application).where(Application.user_id == user_id)
    
    # Filter by status
    if status:
        statement = statement.where(Application.status == status)
    
    # Search by company or role
    if search:
        search_pattern = f"%{search}%"
        statement = statement.where(
            or_(
                Application.company.ilike(search_pattern),
                Application.role.ilike(search_pattern)
            )
        )
    
    applications = session.exec(statement.order_by(Application.date_applied.desc())).all()
    return applications

@router.get("/{application_id}", response_model=ApplicationResponse)
async def get_application(
    application_id: str,
    session: Session = Depends(get_session),
    user_id: str = Depends(get_current_user)
):
    application = session.get(Application, application_id)
    if not application or application.user_id != user_id:
        raise HTTPException(status_code=404, detail="Application not found")
    return application

@router.patch("/{application_id}", response_model=ApplicationResponse)
async def update_application(
    application_id: str,
    update: ApplicationUpdate,
    session: Session = Depends(get_session),
    user_id: str = Depends(get_current_user)
):
    application = session.get(Application, application_id)
    if not application or application.user_id != user_id:
        raise HTTPException(status_code=404, detail="Application not found")
    
    update_data = update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(application, key, value)
    
    application.last_updated = datetime.utcnow()
    session.add(application)
    session.commit()
    session.refresh(application)
    
    return application

@router.delete("/{application_id}")
async def delete_application(
    application_id: str,
    session: Session = Depends(get_session),
    user_id: str = Depends(get_current_user)
):
    application = session.get(Application, application_id)
    if not application or application.user_id != user_id:
        raise HTTPException(status_code=404, detail="Application not found")
    
    session.delete(application)
    session.commit()
    
    return {"message": "Application deleted"}

@router.post("/quick", response_model=ApplicationResponse)
async def quick_add_application(
    company: str,
    role: str,
    session: Session = Depends(get_session),
    user_id: str = Depends(get_current_user)
):
    """Quick add with minimal fields"""
    application = Application(
        user_id=user_id,
        company=company,
        role=role,
        date_applied=date.today(),
        status="applied"
    )
    session.add(application)
    session.commit()
    session.refresh(application)
    return application
```

**Testing Criteria:**
- [ ] POST `/applications/` creates application
- [ ] GET `/applications/` lists user's applications
- [ ] GET `/applications/?status=interview` filters by status
- [ ] GET `/applications/?search=Google` searches company/role
- [ ] PATCH `/applications/{id}` updates fields
- [ ] POST `/applications/quick` creates minimal entry

---

## **PHASE 2: Frontend Foundation (Week 2)**

### Day 8-9: Auth Pages

**Tasks:**
1. Set up React + TypeScript + Vite
2. Configure Tailwind + shadcn/ui
3. Create auth pages (Login/Signup)

**File: `src/lib/supabase.ts`**
```typescript
import { createClient } from '@supabase/supabase-js'

const supabaseUrl = import.meta.env.VITE_SUPABASE_URL
const supabaseAnonKey = import.meta.env.VITE_SUPABASE_ANON_KEY

export const supabase = createClient(supabaseUrl, supabaseAnonKey)
```

**File: `src/lib/api.ts`**
```typescript
import axios from 'axios'
import { supabase } from './supabase'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000',
})

// Add auth token to requests
api.interceptors.request.use(async (config) => {
  const { data: { session } } = await supabase.auth.getSession()
  if (session?.access_token) {
    config.headers.Authorization = `Bearer ${session.access_token}`
  }
  return config
})

export default api
```

**File: `src/pages/auth/Login.tsx`**
```typescript
import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { supabase } from '@/lib/supabase'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'

export default function Login() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [loading, setLoading] = useState(false)
  const navigate = useNavigate()

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    
    const { error } = await supabase.auth.signInWithPassword({ email, password })
    
    if (error) {
      alert(error.message)
    } else {
      navigate('/dashboard')
    }
    
    setLoading(false)
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50">
      <Card className="w-full max-w-md">
        <CardHeader>
          <CardTitle>Login to Resumitory</CardTitle>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleLogin} className="space-y-4">
            <Input
              type="email"
              placeholder="Email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
            <Input
              type="password"
              placeholder="Password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
            <Button type="submit" className="w-full" disabled={loading}>
              {loading ? 'Loading...' : 'Login'}
            </Button>
          </form>
        </CardContent>
      </Card>
    </div>
  )
}
```

**Testing Criteria:**
- [ ] Login page renders
- [ ] Successful login redirects to dashboard
- [ ] Invalid credentials show error
- [ ] Protected routes require auth

---

### Day 10-11: Dashboard & Resume Library

**File: `src/pages/Dashboard.tsx`**
```typescript
import { useQuery } from '@tanstack/react-query'
import api from '@/lib/api'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'

export default function Dashboard() {
  const { data: resumes } = useQuery({
    queryKey: ['resumes'],
    queryFn: async () => {
      const { data } = await api.get('/resumes/')
      return data
    }
  })

  const { data: applications } = useQuery({
    queryKey: ['applications'],
    queryFn: async () => {
      const { data } = await api.get('/applications/')
      return data
    }
  })

  return (
    <div className="p-8">
      <h1 className="text-3xl font-bold mb-8">Dashboard</h1>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
        <Card>
          <CardHeader>
            <CardTitle>Resumes</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-4xl font-bold">{resumes?.length || 0}</p>
          </CardContent>
        </Card>
        
        <Card>
          <CardHeader>
            <CardTitle>Applications</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-4xl font-bold">{applications?.length || 0}</p>
          </CardContent>
        </Card>
      </div>
      
      {/* Add follow-up reminders widget in V1.1 */}
    </div>
  )
}
```

**File: `src/pages/ResumeLibrary.tsx`**
```typescript
import { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import api from '@/lib/api'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from '@/components/ui/dialog'
import { Input } from '@/components/ui/input'
import { Textarea } from '@/components/ui/textarea'

export default function ResumeLibrary() {
  const queryClient = useQueryClient()
  const [uploadOpen, setUploadOpen] = useState(false)
  
  const { data: resumes, isLoading } = useQuery({
    queryKey: ['resumes'],
    queryFn: async () => {
      const { data } = await api.get('/resumes/')
      return data
    }
  })

  const uploadMutation = useMutation({
    mutationFn: async (formData: FormData) => {
      await api.post('/resumes/', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      })
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['resumes'] })
      setUploadOpen(false)
    }
  })

  const deleteMutation = useMutation({
    mutationFn: async (id: string) => {
      await api.delete(`/resumes/${id}`)
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['resumes'] })
    }
  })

  const handleUpload = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    const formData = new FormData(e.currentTarget)
    uploadMutation.mutate(formData)
  }

  if (isLoading) return <div>Loading...</div>

  return (
    <div className="p-8">
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-3xl font-bold">Resume Library</h1>
        <Dialog open={uploadOpen} onOpenChange={setUploadOpen}>
          <DialogTrigger asChild>
            <Button>+ Upload Resume</Button>
          </DialogTrigger>
          <DialogContent>
            <DialogHeader>
              <DialogTitle>Upload Resume</DialogTitle>
            </DialogHeader>
            <form onSubmit={handleUpload} className="space-y-4">
              <Input name="name" placeholder="Resume name (e.g., SWE Resume v3)" required />
              <Textarea name="notes" placeholder="Notes (optional)" />
              <Input name="pdf_file" type="file" accept=".pdf" required />
              <Input name="tex_file" type="file" accept=".tex" />
              <Button type="submit" className="w-full">Upload</Button>
            </form>
          </DialogContent>
        </Dialog>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {resumes?.map((resume: any) => (
          <Card key={resume.id}>
            <CardHeader>
              <CardTitle>{resume.name}</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-gray-500 mb-4">{resume.notes}</p>
              <div className="flex gap-2">
                <Button size="sm" variant="outline" onClick={() => window.open(resume.pdf_url)}>
                  View
                </Button>
                <Button 
                  size="sm" 
                  variant="destructive"
                  onClick={() => deleteMutation.mutate(resume.id)}
                >
                  Delete
                </Button>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  )
}
```

**Testing Criteria:**
- [ ] Dashboard shows resume/application counts
- [ ] Resume Library displays uploaded resumes
- [ ] Upload modal works
- [ ] Delete removes resume

---

### Day 12-14: Application Tracker

**File: `src/pages/ApplicationTracker.tsx`**
```typescript
import { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import api from '@/lib/api'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Select } from '@/components/ui/select'
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table'

export default function ApplicationTracker() {
  const queryClient = useQueryClient()
  const [search, setSearch] = useState('')
  const [statusFilter, setStatusFilter] = useState('')

  const { data: applications } = useQuery({
    queryKey: ['applications', search, statusFilter],
    queryFn: async () => {
      const params = new URLSearchParams()
      if (search) params.append('search', search)
      if (statusFilter) params.append('status', statusFilter)
      
      const { data } = await api.get(`/applications/?${params}`)
      return data
    }
  })

  const { data: resumes } = useQuery({
    queryKey: ['resumes'],
    queryFn: async () => {
      const { data } = await api.get('/resumes/')
      return data
    }
  })

  return (
    <div className="p-8">
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-3xl font-bold">Application Tracker</h1>
        <Button>+ Add Application</Button>
      </div>

      <div className="flex gap-4 mb-6">
        <Input
          placeholder="Search company or role..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          className="max-w-xs"
        />
        <Select value={statusFilter} onValueChange={setStatusFilter}>
          <option value="">All Statuses</option>
          <option value="applied">Applied</option>
          <option value="interview">Interview</option>
          <option value="offer">Offer</option>
          <option value="rejected">Rejected</option>
        </Select>
      </div>

      <Table>
        <TableHeader>
          <TableRow>
            <TableHead>Company</TableHead>
            <TableHead>Role</TableHead>
            <TableHead>Date Applied</TableHead>
            <TableHead>Status</TableHead>
            <TableHead>Resume</TableHead>
            <TableHead>Actions</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {applications?.map((app: any) => (
            <TableRow key={app.id}>
              <TableCell>{app.company}</TableCell>
              <TableCell>{app.role}</TableCell>
              <TableCell>{new Date(app.date_applied).toLocaleDateString()}</TableCell>
              <TableCell>
                <span className={`px-2 py-1 rounded text-xs ${
                  app.status === 'offer' ? 'bg-green-100 text-green-800' :
                  app.status === 'interview' ? 'bg-blue-100 text-blue-800' :
                  app.status === 'rejected' ? 'bg-red-100 text-red-800' :
                  'bg-gray-100 text-gray-800'
                }`}>
                  {app.status}
                </span>
              </TableCell>
              <TableCell>
                {resumes?.find((r: any) => r.id === app.resume_id)?.name || 'None'}
              </TableCell>
              <TableCell>
                <Button size="sm" variant="outline">View</Button>
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </div>
  )
}
```

**Testing Criteria:**
- [ ] Table displays applications
- [ ] Search filters by company/role
- [ ] Status filter works
- [ ] Resume name shows if linked

---

## **PHASE 3: V1.1 Features (Week 3-4)**

### Day 15-17: Interview Rounds

**Backend: `app/rounds/models.py` & `app/rounds/router.py`**
Follow same pattern as applications - create model, CRUD endpoints.

**Frontend: Add rounds section to ApplicationDetail page**

---

### Day 18-21: Follow-Up Reminders

**Backend: `app/reminders/tasks.py`**
```python
from fastapi import BackgroundTasks
from sqlmodel import Session, select
from datetime import date
from app.applications.models import Application
from app.database import get_session
import smtplib
from email.mime.text import MIMEText

async def send_reminder_emails():
    """Cron job to send follow-up reminders"""
    session = next(get_session())
    
    # Get applications with follow-up due today
    statement = select(Application).where(
        Application.follow_up_date == date.today(),
        Application.status != 'rejected'
    )
    applications = session.exec(statement).all()
    
    for app in applications:
        # Send email (integrate SendGrid/Resend)
        send_email(
            to=app.user.email,
            subject=f"Follow-up due: {app.company}",
            body=f"Reminder to follow up on your {app.role} application at {app.company}"
        )
```

---

### Day 22-24: Quick Add & Clone Features

Implement:
- Quick Add modal (minimal form)
- Resume clone button
- Search/filter improvements

---

## **PHASE 4: Polish & Deploy (Week 4)**

### Day 25-26: UI Polish
- Loading states
- Error handling
- Toast notifications
- Responsive design

### Day 27-28: Testing
- Manual testing all flows
- Beta user testing
- Bug fixes

### Day 29-30: Deploy
- Deploy backend to Railway/Render
- Deploy frontend to Vercel
- Set up domain
- Launch!

---

## 🎨 Design Guidelines

**Colors:**
```css
--primary: #3B82F6;
--success: #10B981;
--warning: #F59E0B;
--danger: #EF4444;
--gray-50: #F9FAFB;
--gray-900: #111827;
```

**Typography:**
- Headers: Inter/Geist
- Body: System fonts

**Spacing:**
- Use Tailwind's 4px scale (p-4, p-8, etc.)
- Generous whitespace

---

## 🚨 Critical Rules

**DO:**
- Keep it simple - minimal features
- Use TypeScript strictly
- Handle errors gracefully
- Add loading states everywhere
- Make resume-to-app linking obvious
- Support LaTeX files properly

**DON'T:**
- Add AI features
- Build ATS optimization
- Overcomplicate UI
- Skip error handling
- Forget to invalidate React Query cache
- Ignore mobile responsiveness

---

## 🧪 Testing Checklist

Before each phase completion:
- [ ] All endpoints return expected data
- [ ] Authentication works
- [ ] File uploads succeed
- [ ] Search/filter functions correctly
- [ ] UI is responsive
- [ ] No console errors
- [ ] Loading states show
- [ ] Errors display properly

---

## 📦 Dependencies

**Backend (`requirements.txt`):**
```
fastapi==0.104.1
uvicorn[standard]==0.24.0
sqlmodel==0.0.14
supabase==2.0.0
pyjwt==2.8.0
python-multipart==0.0.6
python-dotenv==1.0.0
```

**Frontend (`package.json`):**
```json
{
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.20.0",
    "@tanstack/react-query": "^5.12.0",
    "@supabase/supabase-js": "^2.38.0",
    "axios": "^1.6.2",
    "tailwindcss": "^3.3.0",
    "@radix-ui/react-dialog": "^1.0.5",
    "@radix-ui/react-select": "^2.0.0"
  }
}
```

---

## 🎯 Success Metrics

Track these after launch:
- Users who upload ≥1 resume: **80%+**
- Users who add ≥3 applications: **60%+**
- Users who link resumes to apps: **70%+**
- 7-day retention: **50%+**
- 30-day retention: **40%+**

---

## 💡 Quick Commands

**Start Backend:**
```bash
cd resumitory-backend
uvicorn app.main:app --reload
```

**Start Frontend:**
```bash
cd resumitory-frontend
npm run dev
```

**Database Migrations:**
```bash
# Use Supabase SQL editor or Alembic
```

---

## 📞 When You're Stuck

Ask me for:
1. Specific code implementations
2. Bug fixes
3. Database queries
4. UI component code
5. Deployment help
6. Feature clarifications

**Remember:** Ship fast, iterate faster. Perfect is the enemy of done.

Now go build! 🚀