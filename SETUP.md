# Resumitory - Quick Setup Guide

This guide will help you get Resumitory up and running locally in **15 minutes**.

---

## 📋 Prerequisites

Before you begin, make sure you have:

- ✅ **Python 3.11+** installed ([Download](https://www.python.org/downloads/))
- ✅ **Git** installed ([Download](https://git-scm.com/downloads))
- ✅ **Node.js 18+** installed ([Download](https://nodejs.org/)) - *for frontend (coming soon)*
- ✅ **Supabase account** (free tier) - [Sign up](https://supabase.com)

---

## 🚀 Step-by-Step Setup

### Step 1: Clone the Repository

```bash
git clone https://github.com/Dhanushranga1/Resumitory.git
cd Resumitory
```

### Step 2: Set Up Supabase Project

1. Go to [Supabase Dashboard](https://app.supabase.com)
2. Click **"New Project"**
3. Fill in:
   - **Project Name:** Resumitory
   - **Database Password:** (save this securely)
   - **Region:** Choose closest to you
   - **Pricing Plan:** Free
4. Click **"Create Project"** (takes ~2 minutes)

### Step 3: Create Database Tables

1. In Supabase Dashboard, go to **SQL Editor**
2. Click **"New Query"**
3. Copy and paste this SQL:

```sql
-- Users table (Supabase Auth handles this automatically)
-- We just need to reference auth.users

-- Resumes table
CREATE TABLE resumes (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
  name TEXT NOT NULL,
  notes TEXT,
  pdf_url TEXT NOT NULL,
  tex_url TEXT,
  tags TEXT[],
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

-- Applications table
CREATE TABLE applications (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
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

-- Interview rounds table (V1.1)
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

-- Create indexes for performance
CREATE INDEX idx_resumes_user_id ON resumes(user_id);
CREATE INDEX idx_applications_user_id ON applications(user_id);
CREATE INDEX idx_applications_status ON applications(user_id, status);
CREATE INDEX idx_applications_follow_up ON applications(follow_up_date) WHERE follow_up_date IS NOT NULL;
CREATE INDEX idx_rounds_application ON interview_rounds(application_id);

-- Enable Row Level Security (RLS)
ALTER TABLE resumes ENABLE ROW LEVEL SECURITY;
ALTER TABLE applications ENABLE ROW LEVEL SECURITY;
ALTER TABLE interview_rounds ENABLE ROW LEVEL SECURITY;

-- RLS Policies for resumes
CREATE POLICY "Users can view own resumes" ON resumes
  FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own resumes" ON resumes
  FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own resumes" ON resumes
  FOR UPDATE USING (auth.uid() = user_id);

CREATE POLICY "Users can delete own resumes" ON resumes
  FOR DELETE USING (auth.uid() = user_id);

-- RLS Policies for applications
CREATE POLICY "Users can view own applications" ON applications
  FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own applications" ON applications
  FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own applications" ON applications
  FOR UPDATE USING (auth.uid() = user_id);

CREATE POLICY "Users can delete own applications" ON applications
  FOR DELETE USING (auth.uid() = user_id);

-- RLS Policies for interview_rounds
CREATE POLICY "Users can view rounds for own applications" ON interview_rounds
  FOR SELECT USING (
    EXISTS (
      SELECT 1 FROM applications 
      WHERE applications.id = interview_rounds.application_id 
      AND applications.user_id = auth.uid()
    )
  );

CREATE POLICY "Users can insert rounds for own applications" ON interview_rounds
  FOR INSERT WITH CHECK (
    EXISTS (
      SELECT 1 FROM applications 
      WHERE applications.id = interview_rounds.application_id 
      AND applications.user_id = auth.uid()
    )
  );

CREATE POLICY "Users can update rounds for own applications" ON interview_rounds
  FOR UPDATE USING (
    EXISTS (
      SELECT 1 FROM applications 
      WHERE applications.id = interview_rounds.application_id 
      AND applications.user_id = auth.uid()
    )
  );

CREATE POLICY "Users can delete rounds for own applications" ON interview_rounds
  FOR DELETE USING (
    EXISTS (
      SELECT 1 FROM applications 
      WHERE applications.id = interview_rounds.application_id 
      AND applications.user_id = auth.uid()
    )
  );
```

4. Click **"Run"** to execute the SQL

### Step 4: Get Supabase Credentials

1. In Supabase Dashboard, go to **Project Settings** (gear icon)
2. Click **API** in the left sidebar
3. Copy these values:
   - **Project URL** (e.g., `https://xxxxx.supabase.co`)
   - **anon public** key
   - **JWT Secret** (from "JWT Settings" section)

### Step 5: Set Up Backend

1. **Navigate to backend directory:**
   ```bash
   cd resumitory-backend
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   ```

3. **Activate virtual environment:**
   ```bash
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Create `.env` file:**
   ```bash
   # Windows
   copy .env.example .env
   
   # macOS/Linux
   cp .env.example .env
   ```

6. **Edit `.env` file** with your Supabase credentials:
   ```env
   SUPABASE_URL=https://your-project.supabase.co
   SUPABASE_KEY=your-anon-key-here
   SUPABASE_JWT_SECRET=your-jwt-secret-here
   ```

7. **Run the backend:**
   ```bash
   uvicorn app.main:app --reload --port 8000
   ```

8. **Verify backend is running:**
   - Open http://localhost:8000
   - You should see: `{"message": "Resumitory API", ...}`
   - Open http://localhost:8000/docs for API documentation

### Step 6: Test Authentication (Optional)

1. In Supabase Dashboard, go to **Authentication** > **Users**
2. Click **"Add user"** > **"Create new user"**
3. Enter email and password
4. Click **"Create user"**
5. In Supabase, go to **Authentication** > **Users** > click the user
6. Copy the **Access Token** (JWT)
7. Go to http://localhost:8000/docs
8. Click **"Authorize"** button (top right)
9. Paste token and click **"Authorize"**
10. Try the `/auth/me` endpoint - should return your user_id

---

## ✅ You're Done! (Backend)

Your backend is now running at:
- **API:** http://localhost:8000
- **Docs:** http://localhost:8000/docs

---

## 🎯 Next Steps

### Current Status
- ✅ Backend structure set up
- ✅ Authentication working
- ⏳ Resume endpoints (coming soon)
- ⏳ Application endpoints (coming soon)
- ⏳ Frontend (coming in Week 3)

### What to Do Next

1. **Follow the development progress** in `PROGRESS.md`
2. **Check the action plan** in `ACTION_PLAN.md` for upcoming features
3. **Read the backend README** in `resumitory-backend/README.md` for API details

---

## 🐛 Troubleshooting

### "ModuleNotFoundError: No module named 'app'"
- Make sure you're in `resumitory-backend` directory
- Ensure virtual environment is activated
- Run: `pip install -r requirements.txt`

### "Database connection error"
- Check Supabase credentials in `.env`
- Ensure Supabase project is active
- Verify `SUPABASE_URL` includes `https://`

### "Port 8000 already in use"
- Stop other processes using port 8000
- Or use a different port: `uvicorn app.main:app --reload --port 8001`

### "Cannot activate virtual environment"
- Windows: Ensure execution policy allows scripts
  ```powershell
  Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
  ```
- macOS/Linux: Check that `venv` directory exists

---

## 📚 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Supabase Documentation](https://supabase.com/docs)
- [Backend README](resumitory-backend/README.md)
- [Action Plan](ACTION_PLAN.md)
- [Contributing Guide](CONTRIBUTING.md)

---

## 💬 Need Help?

- Create an issue on [GitHub](https://github.com/Dhanushranga1/Resumitory/issues)
- Check [PROGRESS.md](PROGRESS.md) for current development status

---

**Happy coding! 🚀**
