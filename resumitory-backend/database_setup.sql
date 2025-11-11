-- ============================================
-- Resumitory Database Setup Script
-- Run this in Supabase SQL Editor
-- ============================================

-- Step 1: Create Storage Bucket for Resumes
-- (Note: This might fail if bucket already exists, that's okay)
INSERT INTO storage.buckets (id, name, public)
VALUES ('resumes', 'resumes', true)
ON CONFLICT (id) DO NOTHING;

-- Step 2: Set up Storage Policies for Resumes Bucket
-- Allow authenticated users to upload files
CREATE POLICY "Users can upload own resumes"
ON storage.objects FOR INSERT
TO authenticated
WITH CHECK (
  bucket_id = 'resumes' AND
  (storage.foldername(name))[1] = auth.uid()::text
);

-- Allow users to read their own files
CREATE POLICY "Users can read own resumes"
ON storage.objects FOR SELECT
TO authenticated
USING (
  bucket_id = 'resumes' AND
  (storage.foldername(name))[1] = auth.uid()::text
);

-- Allow users to delete their own files
CREATE POLICY "Users can delete own resumes"
ON storage.objects FOR DELETE
TO authenticated
USING (
  bucket_id = 'resumes' AND
  (storage.foldername(name))[1] = auth.uid()::text
);

-- Allow public access to files (for viewing resumes)
CREATE POLICY "Public can view resumes"
ON storage.objects FOR SELECT
TO public
USING (bucket_id = 'resumes');

-- Step 3: Create Resumes Table
CREATE TABLE IF NOT EXISTS resumes (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE NOT NULL,
  name TEXT NOT NULL,
  notes TEXT,
  pdf_url TEXT NOT NULL,
  tex_url TEXT,
  tags TEXT[],
  created_at TIMESTAMP DEFAULT NOW() NOT NULL,
  updated_at TIMESTAMP DEFAULT NOW() NOT NULL
);

-- Step 4: Create Applications Table
CREATE TABLE IF NOT EXISTS applications (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE NOT NULL,
  company TEXT NOT NULL,
  role TEXT NOT NULL,
  date_applied DATE NOT NULL,
  status TEXT NOT NULL CHECK (status IN ('applied', 'interview', 'offer', 'rejected', 'archived')),
  notes TEXT,
  resume_id UUID REFERENCES resumes(id) ON DELETE SET NULL,
  follow_up_date DATE,
  last_updated TIMESTAMP DEFAULT NOW() NOT NULL,
  created_at TIMESTAMP DEFAULT NOW() NOT NULL
);

-- Step 5: Create Interview Rounds Table (V1.1)
CREATE TABLE IF NOT EXISTS interview_rounds (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  application_id UUID REFERENCES applications(id) ON DELETE CASCADE NOT NULL,
  round_number INTEGER NOT NULL,
  round_type TEXT NOT NULL,
  scheduled_date DATE,
  completed_date DATE,
  notes TEXT,
  status TEXT CHECK (status IN ('scheduled', 'completed', 'cancelled')),
  created_at TIMESTAMP DEFAULT NOW() NOT NULL
);

-- Step 6: Create Indexes for Performance
CREATE INDEX IF NOT EXISTS idx_resumes_user_id ON resumes(user_id);
CREATE INDEX IF NOT EXISTS idx_resumes_created ON resumes(user_id, created_at DESC);

CREATE INDEX IF NOT EXISTS idx_applications_user_id ON applications(user_id);
CREATE INDEX IF NOT EXISTS idx_applications_status ON applications(user_id, status);
CREATE INDEX IF NOT EXISTS idx_applications_date ON applications(user_id, date_applied DESC);
CREATE INDEX IF NOT EXISTS idx_applications_company ON applications(user_id, company);
CREATE INDEX IF NOT EXISTS idx_applications_follow_up ON applications(follow_up_date) 
  WHERE follow_up_date IS NOT NULL AND status NOT IN ('rejected', 'archived');

CREATE INDEX IF NOT EXISTS idx_rounds_application ON interview_rounds(application_id);

-- Step 7: Enable Row Level Security (RLS)
ALTER TABLE resumes ENABLE ROW LEVEL SECURITY;
ALTER TABLE applications ENABLE ROW LEVEL SECURITY;
ALTER TABLE interview_rounds ENABLE ROW LEVEL SECURITY;

-- Step 8: RLS Policies for Resumes
DROP POLICY IF EXISTS "Users can view own resumes" ON resumes;
CREATE POLICY "Users can view own resumes" ON resumes
  FOR SELECT USING (auth.uid() = user_id);

DROP POLICY IF EXISTS "Users can insert own resumes" ON resumes;
CREATE POLICY "Users can insert own resumes" ON resumes
  FOR INSERT WITH CHECK (auth.uid() = user_id);

DROP POLICY IF EXISTS "Users can update own resumes" ON resumes;
CREATE POLICY "Users can update own resumes" ON resumes
  FOR UPDATE USING (auth.uid() = user_id);

DROP POLICY IF EXISTS "Users can delete own resumes" ON resumes;
CREATE POLICY "Users can delete own resumes" ON resumes
  FOR DELETE USING (auth.uid() = user_id);

-- Step 9: RLS Policies for Applications
DROP POLICY IF EXISTS "Users can view own applications" ON applications;
CREATE POLICY "Users can view own applications" ON applications
  FOR SELECT USING (auth.uid() = user_id);

DROP POLICY IF EXISTS "Users can insert own applications" ON applications;
CREATE POLICY "Users can insert own applications" ON applications
  FOR INSERT WITH CHECK (auth.uid() = user_id);

DROP POLICY IF EXISTS "Users can update own applications" ON applications;
CREATE POLICY "Users can update own applications" ON applications
  FOR UPDATE USING (auth.uid() = user_id);

DROP POLICY IF EXISTS "Users can delete own applications" ON applications;
CREATE POLICY "Users can delete own applications" ON applications
  FOR DELETE USING (auth.uid() = user_id);

-- Step 10: RLS Policies for Interview Rounds
DROP POLICY IF EXISTS "Users can view rounds for own applications" ON interview_rounds;
CREATE POLICY "Users can view rounds for own applications" ON interview_rounds
  FOR SELECT USING (
    EXISTS (
      SELECT 1 FROM applications 
      WHERE applications.id = interview_rounds.application_id 
      AND applications.user_id = auth.uid()
    )
  );

DROP POLICY IF EXISTS "Users can insert rounds for own applications" ON interview_rounds;
CREATE POLICY "Users can insert rounds for own applications" ON interview_rounds
  FOR INSERT WITH CHECK (
    EXISTS (
      SELECT 1 FROM applications 
      WHERE applications.id = interview_rounds.application_id 
      AND applications.user_id = auth.uid()
    )
  );

DROP POLICY IF EXISTS "Users can update rounds for own applications" ON interview_rounds;
CREATE POLICY "Users can update rounds for own applications" ON interview_rounds
  FOR UPDATE USING (
    EXISTS (
      SELECT 1 FROM applications 
      WHERE applications.id = interview_rounds.application_id 
      AND applications.user_id = auth.uid()
    )
  );

DROP POLICY IF EXISTS "Users can delete rounds for own applications" ON interview_rounds;
CREATE POLICY "Users can delete rounds for own applications" ON interview_rounds
  FOR DELETE USING (
    EXISTS (
      SELECT 1 FROM applications 
      WHERE applications.id = interview_rounds.application_id 
      AND applications.user_id = auth.uid()
    )
  );

-- Step 11: Create Updated_At Trigger Function
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Step 12: Add Triggers for Auto-Updating updated_at
DROP TRIGGER IF EXISTS update_resumes_updated_at ON resumes;
CREATE TRIGGER update_resumes_updated_at
BEFORE UPDATE ON resumes
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();

DROP TRIGGER IF EXISTS update_applications_last_updated ON applications;
CREATE TRIGGER update_applications_last_updated
BEFORE UPDATE ON applications
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();

-- ============================================
-- Setup Complete!
-- ============================================

-- Verify tables were created
SELECT 
  'resumes' as table_name, 
  COUNT(*) as row_count 
FROM resumes
UNION ALL
SELECT 
  'applications' as table_name, 
  COUNT(*) as row_count 
FROM applications
UNION ALL
SELECT 
  'interview_rounds' as table_name, 
  COUNT(*) as row_count 
FROM interview_rounds;

-- Verify storage bucket was created
SELECT * FROM storage.buckets WHERE id = 'resumes';
