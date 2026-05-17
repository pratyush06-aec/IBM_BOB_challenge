# Firebase Authentication Setup Guide

## Prerequisites

1. **Create a Firebase Project**
   - Go to [Firebase Console](https://console.firebase.google.com/)
   - Click "Add project" or select existing project
   - Follow the setup wizard

2. **Enable Authentication**
   - In Firebase Console, go to "Authentication"
   - Click "Get Started"
   - Enable "Email/Password" sign-in method

3. **Get Firebase Configuration**
   
   **For Frontend (Web App):**
   - Go to Project Settings > General
   - Scroll to "Your apps" section
   - Click "Add app" > Web (</>) icon
   - Register your app
   - Copy the Firebase configuration object

   **For Backend (Admin SDK):**
   - Go to Project Settings > Service Accounts
   - Click "Generate new private key"
   - Download the JSON file
   - Save it as `firebase-service-account.json` in `backend/` directory

## Environment Variables

### Frontend (.env.local)
Create `frontend/.env.local` with your Firebase config:

```env
NEXT_PUBLIC_FIREBASE_API_KEY=your_api_key
NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN=your_project.firebaseapp.com
NEXT_PUBLIC_FIREBASE_PROJECT_ID=your_project_id
NEXT_PUBLIC_FIREBASE_STORAGE_BUCKET=your_project.appspot.com
NEXT_PUBLIC_FIREBASE_MESSAGING_SENDER_ID=your_sender_id
NEXT_PUBLIC_FIREBASE_APP_ID=your_app_id
```

### Backend (.env)
Add to `backend/.env`:

```env
FIREBASE_SERVICE_ACCOUNT_PATH=./firebase-service-account.json
```

## Installation

### Frontend
```bash
cd frontend
npm install firebase
```

### Backend
```bash
cd backend
pip install firebase-admin
```

## Security Notes

- **NEVER** commit `firebase-service-account.json` to version control
- Add it to `.gitignore`
- Keep your API keys secure
- Use environment variables for all sensitive data

## Testing

After setup, you can:
1. Register a new user with email/password
2. Sign in with registered credentials
3. Access protected routes with Firebase token