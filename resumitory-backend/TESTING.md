# Testing Guide for Resumitory Backend

## Prerequisites

Before testing, ensure you have:
- ✅ Supabase project created
- ✅ Database tables created (run `database_setup.sql`)
- ✅ `.env` file configured
- ✅ Virtual environment activated
- ✅ Dependencies installed

## Quick Start

```bash
# Navigate to backend
cd resumitory-backend

# Activate virtual environment
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux

# Install dependencies (if not done)
pip install -r requirements.txt

# Run the server
uvicorn app.main:app --reload --port 8000
```

Server will start at: **http://localhost:8000**  
API docs at: **http://localhost:8000/docs**

---

## Testing Workflow

### 1. Create a Test User in Supabase

1. Go to Supabase Dashboard → **Authentication** → **Users**
2. Click **"Add user"** → **"Create new user"**
3. Enter:
   - Email: test@resumitory.com
   - Password: TestPass123!
4. Click **"Create user"**

### 2. Get Authentication Token

**Option A: Via Supabase Dashboard**
1. Go to **Authentication** → **Users**
2. Click on the test user
3. Copy the **Access Token** (JWT)

**Option B: Via API (Coming in Frontend)**
- Use Supabase Auth SDK to login
- Extract JWT token from session

### 3. Authorize in Swagger UI

1. Go to **http://localhost:8000/docs**
2. Click **"Authorize"** button (top right, 🔒 icon)
3. Paste your JWT token
4. Click **"Authorize"**
5. Close the modal

### 4. Test Authentication

**Endpoint:** `GET /auth/me`

**Expected Response:**
```json
{
  "user_id": "your-uuid-here",
  "message": "Authentication successful"
}
```

---

## Testing Resume Endpoints

### Test 1: Upload Resume

**Endpoint:** `POST /resumes/`

**Steps:**
1. In Swagger UI, find `POST /resumes/`
2. Click **"Try it out"**
3. Fill in:
   - **name**: "Software Engineer Resume v1"
   - **notes**: "Tailored for backend roles"
   - **tags**: "python,backend,api"
   - **pdf_file**: Upload a PDF file (max 5MB)
   - **tex_file**: (Optional) Upload a .tex file
4. Click **"Execute"**

**Expected Response (201 Created):**
```json
{
  "id": "uuid-here",
  "user_id": "your-user-id",
  "name": "Software Engineer Resume v1",
  "notes": "Tailored for backend roles",
  "pdf_url": "https://xxx.supabase.co/storage/v1/object/public/resumes/...",
  "tex_url": null,
  "tags": ["python", "backend", "api"],
  "created_at": "2025-11-12T...",
  "updated_at": "2025-11-12T..."
}
```

### Test 2: List All Resumes

**Endpoint:** `GET /resumes/`

**Expected Response (200 OK):**
```json
[
  {
    "id": "uuid-here",
    "user_id": "your-user-id",
    "name": "Software Engineer Resume v1",
    ...
  }
]
```

### Test 3: Get Specific Resume

**Endpoint:** `GET /resumes/{resume_id}`

**Steps:**
1. Copy `id` from previous response
2. Paste into `resume_id` parameter
3. Execute

**Expected Response (200 OK):**
- Same structure as single resume

### Test 4: Update Resume Metadata

**Endpoint:** `PATCH /resumes/{resume_id}`

**Request Body:**
```json
{
  "name": "Software Engineer Resume v2",
  "notes": "Updated for senior roles",
  "tags": ["python", "backend", "senior", "distributed"]
}
```

**Expected Response (200 OK):**
- Updated resume with new metadata
- `updated_at` timestamp changed

### Test 5: Clone Resume

**Endpoint:** `POST /resumes/{resume_id}/clone`

**Expected Response (201 Created):**
```json
{
  "id": "new-uuid-here",
  "name": "Software Engineer Resume v1 (Copy)",
  "pdf_url": "same-as-original",
  ...
}
```

### Test 6: Delete Resume

**Endpoint:** `DELETE /resumes/{resume_id}`

**Expected Response (204 No Content):**
- Empty response
- Resume and files deleted from database and storage

---

## Common Issues & Solutions

### Issue: "401 Unauthorized"
**Solution:** 
- Check that JWT token is not expired (expires after 1 hour)
- Re-authorize in Swagger UI
- Get fresh token from Supabase

### Issue: "403 Forbidden"
**Solution:**
- Ensure you're accessing your own resources
- Check that `user_id` in token matches resource owner

### Issue: "File upload failed"
**Solution:**
- Check file size (PDF max 5MB, .tex max 1MB)
- Verify file type (only .pdf and .tex allowed)
- Ensure Supabase storage bucket exists (run `database_setup.sql`)

### Issue: "Database connection error"
**Solution:**
- Verify `.env` credentials are correct
- Check `DATABASE_PASSWORD` is set
- Ensure Supabase project is active
- Test connection: `psql postgresql://postgres:[PASSWORD]@db.[PROJECT_REF].supabase.co:5432/postgres`

### Issue: "Import errors" (sqlmodel, supabase)
**Solution:**
```bash
pip install -r requirements.txt
```

---

## Testing Checklist

### Authentication ✅
- [ ] GET /auth/me returns user_id
- [ ] Invalid token returns 401
- [ ] Missing token returns 401

### Resume Upload ✅
- [ ] Upload PDF only (no .tex)
- [ ] Upload PDF + .tex
- [ ] Upload with tags
- [ ] Validate file size limits
- [ ] Validate file types

### Resume CRUD ✅
- [ ] List all resumes (ordered by date)
- [ ] Get specific resume by ID
- [ ] Update resume metadata (name, notes, tags)
- [ ] Delete resume (removes from DB and storage)

### Resume Cloning ✅
- [ ] Clone resume creates copy
- [ ] Clone appends " (Copy)" to name
- [ ] Clone references same files

### Error Handling ✅
- [ ] 404 for non-existent resume
- [ ] 403 for accessing other user's resume
- [ ] 400 for invalid file types
- [ ] 400 for oversized files

---

## Next Steps

Once Resume endpoints are verified:
1. Create Application models and endpoints
2. Link applications to resumes
3. Test application tracking workflow
4. Build frontend UI

---

## Performance Testing

### Load Test (Optional)

```python
# test_load.py
import asyncio
import aiohttp

async def upload_resume(session, token):
    url = "http://localhost:8000/resumes/"
    headers = {"Authorization": f"Bearer {token}"}
    
    data = aiohttp.FormData()
    data.add_field('name', 'Load Test Resume')
    data.add_field('pdf_file', open('test.pdf', 'rb'))
    
    async with session.post(url, headers=headers, data=data) as response:
        return response.status

async def main():
    token = "your-jwt-token"
    async with aiohttp.ClientSession() as session:
        tasks = [upload_resume(session, token) for _ in range(10)]
        results = await asyncio.gather(*tasks)
        print(f"Completed: {len([r for r in results if r == 201])}/10")

asyncio.run(main())
```

---

## Database Verification

### Check Data in Supabase

1. Go to Supabase Dashboard → **Table Editor**
2. Select `resumes` table
3. Verify:
   - Resumes are being created
   - `user_id` matches your test user
   - URLs are valid Supabase Storage links
   - `created_at` and `updated_at` timestamps are correct

### Check Files in Storage

1. Go to Supabase Dashboard → **Storage**
2. Select `resumes` bucket
3. Navigate to your `user_id` folder
4. Verify files are uploaded and accessible

---

**Happy Testing! 🚀**

If you encounter issues not covered here, check:
- Backend logs in terminal
- Supabase logs in Dashboard → **Logs**
- Network tab in browser DevTools
