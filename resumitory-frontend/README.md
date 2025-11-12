# Resumitory Frontend

React + TypeScript frontend for Resumitory - Resume version control and job application tracker.

## 🚀 Quick Start

### Prerequisites

- Node.js 18+ 
- npm or yarn
- Backend API running on `http://localhost:8000`

### Installation

1. **Install dependencies:**

```bash
npm install
```

2. **Set up environment variables:**

```bash
# Copy example env file
cp .env.example .env

# Edit .env with your Supabase credentials
```

Required environment variables:
- `VITE_SUPABASE_URL`: Your Supabase project URL
- `VITE_SUPABASE_ANON_KEY`: Your Supabase anon key
- `VITE_API_URL`: Backend API URL (default: http://localhost:8000)

3. **Run the development server:**

```bash
npm run dev
```

The app will be available at: **http://localhost:5173**

---

## 📁 Project Structure

```
resumitory-frontend/
├── src/
│   ├── lib/
│   │   ├── supabase.ts         # Supabase client
│   │   ├── api.ts              # Axios client with JWT interceptor
│   │   ├── query.tsx           # React Query provider
│   │   └── store.ts            # Zustand state management
│   ├── pages/
│   │   ├── Login.tsx           # Login page
│   │   ├── Signup.tsx          # Signup page
│   │   └── Dashboard.tsx       # Dashboard page
│   ├── components/             # Reusable components
│   ├── features/               # Feature-specific components
│   ├── App.tsx                 # Main app with routing
│   ├── main.tsx                # Entry point
│   └── index.css               # Tailwind CSS
├── .env                        # Environment variables
└── README.md                   # This file
```

---

## 🛠️ Tech Stack

- **React 18** + **TypeScript**
- **Vite**: Fast build tool
- **React Router**: Routing
- **Tailwind CSS**: Styling
- **React Query**: Server state
- **Zustand**: Client state
- **Axios**: HTTP client
- **Supabase**: Authentication

---

## 📚 Current Features

- ✅ Authentication (Login/Signup)
- ✅ Dashboard with stats
- 🚧 Resume Library (coming soon)
- 🚧 Application Tracker (coming soon)

---

## 🔑 Authentication Flow

1. User signs up/logs in via Supabase Auth
2. JWT token stored in Supabase session
3. Axios interceptor adds token to all API requests
4. On 401 error, redirect to login

---

## 🚀 Deployment

Build for production:
```bash
npm run build
```

Deploy to Vercel, Netlify, or any static host.
