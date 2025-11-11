# Resumitory - Detailed Action Plan

## 🎯 Project Timeline: 8 Weeks to V1.1

---

## Phase 1: Backend Foundation (Week 1-2)

### Week 1: Core Backend Setup

#### Day 1: Project Initialization
- [ ] Create `resumitory-backend` directory structure
- [ ] Initialize Python virtual environment
- [ ] Create `requirements.txt` with dependencies
- [ ] Set up `.env.example` for configuration
- [ ] Initialize git and make first commit: `feat: Initialize backend project structure`

**Commit Message:** `feat: Initialize FastAPI project with basic structure`

#### Day 2: Database & Auth Setup
- [ ] Create Supabase project (database + auth + storage)
- [ ] Set up `app/config.py` with pydantic_settings
- [ ] Create `app/database.py` with SQLModel session
- [ ] Implement `app/auth/dependencies.py` with JWT verification
- [ ] Create `app/auth/router.py` with `/auth/me` endpoint
- [ ] Test authentication with Supabase token

**Commit Message:** `feat: Add Supabase authentication with JWT verification`

#### Day 3: Resume Models & Storage
- [ ] Create `app/resumes/models.py` with Resume SQLModel
- [ ] Implement `app/resumes/storage.py` for Supabase Storage
- [ ] Add file upload helpers (PDF + .tex support)
- [ ] Add file deletion helpers
- [ ] Test file upload/download locally

**Commit Message:** `feat: Add Resume models and Supabase Storage integration`

#### Day 4: Resume CRUD Endpoints
- [ ] Create `app/resumes/router.py`
- [ ] Implement POST `/resumes/` (upload with multipart form-data)
- [ ] Implement GET `/resumes/` (list user resumes)
- [ ] Implement GET `/resumes/{id}` (get specific resume)
- [ ] Implement PATCH `/resumes/{id}` (update metadata)
- [ ] Implement DELETE `/resumes/{id}` (delete resume + files)
- [ ] Test all endpoints via `/docs`

**Commit Message:** `feat: Add Resume CRUD endpoints with file upload`

#### Day 5: Application Models
- [ ] Create `app/applications/models.py` with Application SQLModel
- [ ] Add StatusEnum (applied, interview, offer, rejected, archived)
- [ ] Add ApplicationCreate, ApplicationUpdate, ApplicationResponse schemas
- [ ] Add resume_id foreign key to resumes table
- [ ] Test model relationships

**Commit Message:** `feat: Add Application models with resume linking`

#### Day 6-7: Application CRUD Endpoints
- [ ] Create `app/applications/router.py`
- [ ] Implement POST `/applications/` (create)
- [ ] Implement GET `/applications/` (list with filters)
- [ ] Implement GET `/applications/{id}` (get specific)
- [ ] Implement PATCH `/applications/{id}` (update)
- [ ] Implement DELETE `/applications/{id}` (delete)
- [ ] Add search functionality (company/role)
- [ ] Add status filter
- [ ] Test all endpoints thoroughly

**Commit Message:** `feat: Add Application CRUD with search and filters`

**Week 1 Deliverable:** ✅ Working REST API with authentication, resume management, and application tracking

---

### Week 2: API Polish & Testing

#### Day 8: Resume Cloning Feature
- [ ] Implement POST `/resumes/{id}/clone` endpoint
- [ ] Clone logic: copy metadata, keep file URLs
- [ ] Append " (Copy)" to cloned resume name
- [ ] Test cloning with multiple resumes

**Commit Message:** `feat: Add resume cloning functionality`

#### Day 9: Quick Add Endpoint
- [ ] Implement POST `/applications/quick` endpoint
- [ ] Minimal fields: company, role, resume_id
- [ ] Auto-set date_applied to today
- [ ] Default status to "applied"
- [ ] Test quick add flow

**Commit Message:** `feat: Add quick-add endpoint for applications`

#### Day 10: Main FastAPI App
- [ ] Complete `app/main.py` with all routers
- [ ] Configure CORS for frontend (localhost:5173)
- [ ] Add root endpoint with API info
- [ ] Add health check endpoint
- [ ] Test complete API via Swagger UI

**Commit Message:** `feat: Complete main FastAPI app with CORS and routing`

#### Day 11-12: Database Schema in Supabase
- [ ] Create users table (or use Supabase auth.users)
- [ ] Create resumes table with indexes
- [ ] Create applications table with indexes
- [ ] Set up Row Level Security (RLS) policies
- [ ] Test RLS with different user tokens

**Commit Message:** `feat: Set up database schema with RLS policies`

#### Day 13-14: Backend Testing & Documentation
- [ ] Create `resumitory-backend/README.md`
- [ ] Document setup steps
- [ ] Document environment variables
- [ ] Document API endpoints
- [ ] Create `.env.example`
- [ ] Test complete backend flow end-to-end

**Commit Message:** `docs: Add comprehensive backend documentation`

**Week 2 Deliverable:** ✅ Production-ready backend API with documentation

---

## Phase 2: Frontend Foundation (Week 3-4)

### Week 3: React Setup & Auth

#### Day 15: Frontend Initialization
- [ ] Create `resumitory-frontend` directory
- [ ] Initialize Vite + React + TypeScript project
- [ ] Install Tailwind CSS
- [ ] Install shadcn/ui CLI
- [ ] Configure `tailwind.config.js`
- [ ] Set up `src/` directory structure
- [ ] Create `.env.example` for API URL

**Commit Message:** `feat: Initialize React frontend with Vite and Tailwind`

#### Day 16: Supabase & API Client Setup
- [ ] Create `src/lib/supabase.ts` with Supabase client
- [ ] Create `src/lib/api.ts` with Axios instance
- [ ] Add JWT interceptor to Axios
- [ ] Create `src/types/index.ts` for TypeScript types
- [ ] Test API connection

**Commit Message:** `feat: Set up Supabase client and API integration`

#### Day 17: Auth Pages
- [ ] Install shadcn/ui components (Button, Input, Card)
- [ ] Create `src/pages/auth/Login.tsx`
- [ ] Create `src/pages/auth/Signup.tsx`
- [ ] Implement Supabase authentication flow
- [ ] Add form validation
- [ ] Test login/signup

**Commit Message:** `feat: Add authentication pages with Supabase`

#### Day 18: Protected Routes & Layout
- [ ] Create `src/components/ProtectedRoute.tsx`
- [ ] Create `src/components/Layout.tsx`
- [ ] Create `src/components/Navbar.tsx`
- [ ] Set up React Router with protected routes
- [ ] Test authentication flow with route protection

**Commit Message:** `feat: Add protected routes and navigation layout`

#### Day 19: React Query Setup
- [ ] Install @tanstack/react-query
- [ ] Set up QueryClient in `src/main.tsx`
- [ ] Create `src/features/resumes/useResumes.ts` hook
- [ ] Create `src/features/applications/useApplications.ts` hook
- [ ] Test query hooks with API

**Commit Message:** `feat: Set up React Query for server state management`

#### Day 20-21: Dashboard Page
- [ ] Create `src/pages/Dashboard.tsx`
- [ ] Fetch resume and application counts
- [ ] Display recent activity
- [ ] Add loading states
- [ ] Add error handling
- [ ] Style with Tailwind

**Commit Message:** `feat: Add dashboard with stats and recent activity`

**Week 3 Deliverable:** ✅ Functional frontend with auth and dashboard

---

### Week 4: Resume & Application UI

#### Day 22-23: Resume Library Page
- [ ] Create `src/pages/ResumeLibrary.tsx`
- [ ] Create `src/features/resumes/ResumeCard.tsx`
- [ ] Create `src/features/resumes/UploadModal.tsx`
- [ ] Implement file upload with drag-and-drop
- [ ] Support PDF and .tex files
- [ ] Display resume list with metadata
- [ ] Add delete confirmation
- [ ] Test upload/delete flows

**Commit Message:** `feat: Add Resume Library with upload functionality`

#### Day 24-25: Application Tracker Page
- [ ] Create `src/pages/ApplicationTracker.tsx`
- [ ] Create `src/features/applications/ApplicationTable.tsx`
- [ ] Install shadcn/ui Table components
- [ ] Display applications in table format
- [ ] Add status badges with color coding
- [ ] Show linked resume names
- [ ] Test table rendering

**Commit Message:** `feat: Add Application Tracker with table view`

#### Day 26: Application Form
- [ ] Create `src/features/applications/ApplicationForm.tsx`
- [ ] Add all form fields (company, role, date, status, notes)
- [ ] Add resume selection dropdown
- [ ] Implement form validation
- [ ] Add create/update logic
- [ ] Test form submission

**Commit Message:** `feat: Add application form with resume linking`

#### Day 27: Quick Add Modal
- [ ] Create `src/features/applications/QuickAddModal.tsx`
- [ ] Minimal form: company, role, resume
- [ ] Quick save with default values
- [ ] Test quick add flow

**Commit Message:** `feat: Add quick-add modal for fast application entry`

#### Day 28: Search & Filter UI
- [ ] Add search input to ApplicationTracker
- [ ] Add status filter dropdown
- [ ] Implement debounced search
- [ ] Update React Query to use filters
- [ ] Test search/filter combinations

**Commit Message:** `feat: Add search and filter to application tracker`

**Week 4 Deliverable:** ✅ Complete MVP frontend with all core features

---

## Phase 3: V1.1 Features (Week 5-6)

### Week 5: Interview Rounds & Follow-Ups

#### Day 29-30: Interview Rounds Backend
- [ ] Create `app/rounds/models.py` with InterviewRound model
- [ ] Create `app/rounds/router.py` with CRUD endpoints
- [ ] Add round_type enum (phone, technical, onsite, final)
- [ ] Add status enum (scheduled, completed, cancelled)
- [ ] Link rounds to applications via application_id FK
- [ ] Test all round endpoints

**Commit Message:** `feat: Add interview rounds tracking (backend)`

#### Day 31-32: Interview Rounds Frontend
- [ ] Create `src/pages/ApplicationDetail.tsx`
- [ ] Add interview rounds section
- [ ] Display rounds chronologically
- [ ] Add "Add Round" button and form
- [ ] Edit/delete round functionality
- [ ] Test complete round workflow

**Commit Message:** `feat: Add interview rounds tracking (frontend)`

#### Day 33-34: Follow-Up System Backend
- [ ] Add `follow_up_date` field to Application model
- [ ] Create `app/reminders/tasks.py` for cron jobs
- [ ] Implement daily reminder check logic
- [ ] Integrate SendGrid or Resend for emails
- [ ] Create email template
- [ ] Test reminder emails locally

**Commit Message:** `feat: Add follow-up reminder system with email notifications`

#### Day 35: Follow-Up System Frontend
- [ ] Add follow-up date picker to application form
- [ ] Add "Set Reminder" button in ApplicationDetail
- [ ] Display upcoming reminders on dashboard
- [ ] Add reminder preset buttons (3 days, 1 week, 2 weeks)
- [ ] Test reminder setting flow

**Commit Message:** `feat: Add follow-up reminder UI`

**Week 5 Deliverable:** ✅ Interview tracking and reminder system functional

---

### Week 6: Advanced Features & Polish

#### Day 36: Resume Cloning Frontend
- [ ] Add "Clone" button to ResumeCard
- [ ] Implement clone mutation with React Query
- [ ] Show success toast on clone
- [ ] Test cloning workflow

**Commit Message:** `feat: Add resume cloning in UI`

#### Day 37-38: Enhanced Search & Filters
- [ ] Add date range filter
- [ ] Add "My Applications" vs "All" toggle
- [ ] Add sort options (date, company, status)
- [ ] Implement URL query params for filters
- [ ] Test all filter combinations

**Commit Message:** `feat: Add advanced search and filtering options`

#### Day 39-40: Dashboard Enhancements
- [ ] Add status breakdown chart
- [ ] Add timeline view of recent applications
- [ ] Add follow-up reminders widget
- [ ] Add quick actions (Quick Add, Upload Resume)
- [ ] Polish UI/UX

**Commit Message:** `feat: Enhance dashboard with charts and widgets`

#### Day 41-42: UI Polish & Responsiveness
- [ ] Add loading skeletons
- [ ] Add error boundaries
- [ ] Add toast notifications (success/error)
- [ ] Make all pages mobile-responsive
- [ ] Add empty states with helpful messages
- [ ] Polish spacing and typography

**Commit Message:** `feat: Add loading states, toasts, and mobile responsiveness`

**Week 6 Deliverable:** ✅ Feature-complete V1.1 with polished UI

---

## Phase 4: Testing & Documentation (Week 7-8)

### Week 7: Testing & Bug Fixes

#### Day 43-44: End-to-End Testing
- [ ] Test complete user journey (signup → upload → apply → track)
- [ ] Test edge cases (empty states, large files, long text)
- [ ] Test error scenarios (network errors, auth failures)
- [ ] Create test checklist document
- [ ] Fix identified bugs

**Commit Message:** `test: Add comprehensive E2E testing and fix bugs`

#### Day 45-46: Beta Testing
- [ ] Deploy to staging environment
- [ ] Recruit 10-20 beta testers
- [ ] Collect feedback via Google Form
- [ ] Implement high-priority feedback
- [ ] Fix critical bugs

**Commit Message:** `fix: Address beta tester feedback and critical bugs`

#### Day 47-48: Performance Optimization
- [ ] Optimize API response times
- [ ] Add pagination to applications list
- [ ] Optimize image loading
- [ ] Add lazy loading for routes
- [ ] Test performance with 100+ applications

**Commit Message:** `perf: Optimize API and frontend performance`

#### Day 49: Security Audit
- [ ] Review RLS policies in Supabase
- [ ] Test authorization for all endpoints
- [ ] Add rate limiting to API
- [ ] Sanitize user inputs
- [ ] Review file upload security

**Commit Message:** `security: Add rate limiting and enhance security measures`

**Week 7 Deliverable:** ✅ Thoroughly tested and optimized application

---

### Week 8: Documentation & Launch

#### Day 50-51: Comprehensive Documentation
- [ ] Write main `README.md` for repository
- [ ] Update `resumitory-backend/README.md` with setup guide
- [ ] Update `resumitory-frontend/README.md` with setup guide
- [ ] Create `CONTRIBUTING.md` for contributors
- [ ] Create `docs/API.md` with all endpoints
- [ ] Create `docs/DEPLOYMENT.md` with deployment guide
- [ ] Add inline code comments

**Commit Message:** `docs: Add comprehensive documentation for all components`

#### Day 52: Landing Page
- [ ] Create simple landing page
- [ ] Add hero section with value proposition
- [ ] Add features section
- [ ] Add screenshots/demo video
- [ ] Add signup CTA
- [ ] Deploy landing page

**Commit Message:** `feat: Add landing page for public launch`

#### Day 53-54: Deployment
- [ ] Set up Railway/Render for backend
- [ ] Set up Vercel for frontend
- [ ] Configure environment variables
- [ ] Set up custom domain
- [ ] Set up SSL certificates
- [ ] Test production deployment

**Commit Message:** `deploy: Set up production infrastructure`

#### Day 55: Analytics & Monitoring
- [ ] Add Plausible/PostHog analytics
- [ ] Set up error tracking (Sentry)
- [ ] Set up uptime monitoring
- [ ] Create admin dashboard for stats
- [ ] Test analytics tracking

**Commit Message:** `feat: Add analytics and error monitoring`

#### Day 56: Launch Preparation
- [ ] Create launch post for Product Hunt
- [ ] Prepare Reddit posts for r/cscareerquestions
- [ ] Write Twitter/X thread
- [ ] Prepare Hacker News "Show HN" post
- [ ] Create press kit with screenshots
- [ ] Schedule launch for optimal time

**Commit Message:** `docs: Prepare launch materials and marketing content`

**Week 8 Deliverable:** ✅ Production deployment with documentation and launch materials

---

## Post-Launch: Continuous Improvement

### Week 9-10: Monitor & Iterate
- [ ] Monitor user feedback and bug reports
- [ ] Respond to support requests within 24 hours
- [ ] Ship hotfixes for critical bugs
- [ ] Collect feature requests
- [ ] Plan V1.2 features based on feedback

### Week 11-12: V1.2 Planning
- [ ] CSV export functionality
- [ ] Application timeline view
- [ ] Rejection archive
- [ ] Status change log
- [ ] Resume tags and categories

---

## Git Commit Conventions

Use conventional commits format:
- `feat:` New features
- `fix:` Bug fixes
- `docs:` Documentation changes
- `style:` Code style changes (formatting)
- `refactor:` Code refactoring
- `test:` Adding tests
- `chore:` Build process or auxiliary tool changes
- `perf:` Performance improvements
- `security:` Security fixes

**Example:**
```
feat: Add resume upload with LaTeX support

- Implement file upload to Supabase Storage
- Support both PDF and .tex files
- Add file validation and error handling
```

---

## Success Metrics to Track

### Activation Metrics
- [ ] 80%+ users upload ≥1 resume
- [ ] 60%+ users add ≥3 applications
- [ ] 70%+ users link resumes to applications

### Engagement Metrics
- [ ] 50%+ weekly active users
- [ ] Average 3+ resumes per user
- [ ] Average 20+ applications per user

### Retention Metrics
- [ ] 50%+ Day 7 retention
- [ ] 40%+ Day 30 retention
- [ ] 30%+ Day 90 retention

---

## Risk Mitigation

### Technical Risks
- **Supabase free tier limits:** Monitor usage, upgrade if needed
- **File storage costs:** Implement file size limits (5MB PDF, 1MB .tex)
- **Email deliverability:** Use verified domain with SendGrid/Resend

### Product Risks
- **Low adoption:** Focus on Reddit/HN launch, iterate based on feedback
- **Competitor copying:** Ship fast, build brand, focus on user experience
- **Scope creep:** Stick to action plan, say no to non-critical features

---

## Next Steps

1. **Review this action plan** and adjust timeline if needed
2. **Set up development environment** (Python, Node.js, Git)
3. **Create Supabase project** and note credentials
4. **Start with Backend Day 1** and follow plan sequentially
5. **Commit frequently** with meaningful messages
6. **Document as you build** to maintain clarity

Let's build Resumitory! 🚀
