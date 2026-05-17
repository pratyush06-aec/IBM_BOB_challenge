# GraphMind AI - Integration Testing Guide

## Overview
This guide walks you through testing the complete integrated system with authentication, repository management, and graph visualization.

## Prerequisites

### 1. Backend Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### 2. Frontend Dependencies
```bash
cd frontend
npm install
```

### 3. Neo4j Database
Start Neo4j using Docker:
```bash
docker run -d --name neo4j \
  -p 7474:7474 -p 7687:7687 \
  -e NEO4J_AUTH=neo4j/password \
  neo4j:latest
```

Or use an existing Neo4j instance and update `.env` file.

### 4. Environment Configuration
Ensure `backend/.env` is properly configured:
```env
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=password
SECRET_KEY=your-secret-key-here
ACCESS_TOKEN_EXPIRE_MINUTES=30
UPLOAD_DIR=./uploads
MAX_UPLOAD_SIZE=52428800
```

## Testing Steps

### Phase 1: Backend Testing

#### 1.1 Start Backend Server
```bash
cd backend
python -m app.main
```

Expected output:
```
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

#### 1.2 Test Health Endpoint
```bash
curl http://localhost:8000/health
```

Expected response:
```json
{"status": "healthy"}
```

#### 1.3 Test Authentication

**Register a new user:**
```bash
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "testpass123"
  }'
```

Expected response:
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer"
}
```

**Login with demo user:**
```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=demo&password=demo123"
```

**Get user info:**
```bash
curl http://localhost:8000/api/auth/me \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

#### 1.4 Test Neo4j Connection
Check backend logs for:
```
INFO: Neo4j connection successful
```

If you see connection errors, verify:
- Neo4j is running
- Credentials in `.env` are correct
- Port 7687 is accessible

### Phase 2: Frontend Testing

#### 2.1 Start Frontend Server
```bash
cd frontend
npm run dev
```

Expected output:
```
  ▲ Next.js 15.1.0
  - Local:        http://localhost:3000
  - Ready in 2.3s
```

#### 2.2 Open Application
Navigate to: http://localhost:3000

You should see:
- ✅ 3D animated background with floating shapes
- ✅ Glassmorphism UI panels
- ✅ "Sign In" button in header
- ✅ Sample graph visualization (default data)

### Phase 3: Authentication Flow Testing

#### 3.1 Test Login
1. Click "Sign In" button
2. Modal should appear with glassmorphism effect
3. Use demo credentials:
   - Username: `demo`
   - Password: `demo123`
4. Click "Sign In"

**Expected Results:**
- ✅ Modal closes
- ✅ Header shows: "Repositories", "Upload", user menu
- ✅ User icon with username "demo"
- ✅ Logout button appears

#### 3.2 Test Registration
1. Click "Sign In" button
2. Click "Sign Up" toggle
3. Fill in:
   - Username: `newuser`
   - Email: `new@example.com`
   - Password: `newpass123`
   - Confirm Password: `newpass123`
4. Click "Create Account"

**Expected Results:**
- ✅ Account created successfully
- ✅ Automatically logged in
- ✅ Redirected to main view

#### 3.3 Test Logout
1. Click logout button (red icon) in user menu
2. Confirm logout

**Expected Results:**
- ✅ Logged out successfully
- ✅ Header shows only "Sign In" button
- ✅ Repository and Upload buttons hidden

### Phase 4: Repository Upload Testing

#### 4.1 Prepare Test Repository
Create a test repository:
```bash
mkdir test-repo
cd test-repo

# Create sample Python files
cat > main.py << 'EOF'
from utils import helper

class Application:
    def __init__(self):
        self.name = "Test App"
    
    def run(self):
        helper.process()
EOF

cat > utils.py << 'EOF'
class Helper:
    def process(self):
        print("Processing...")

helper = Helper()
EOF

# Create zip file
cd ..
zip -r test-repo.zip test-repo/
```

#### 4.2 Upload Repository
1. Ensure you're logged in
2. Click "Upload" button
3. Upload modal appears
4. Drag and drop `test-repo.zip` or click to browse
5. Repository name auto-fills: `test-repo`
6. Add description: "Test repository for integration testing"
7. Click "Upload Repository"

**Expected Results:**
- ✅ Progress bar shows upload progress
- ✅ "Repository uploaded successfully!" message
- ✅ Modal closes automatically
- ✅ Graph updates with new repository data

**Backend Processing:**
Check backend logs for:
```
INFO: Parsing repository: test-repo
INFO: Found 2 Python files
INFO: Extracted 2 classes, 2 functions
INFO: Created 4 nodes, 3 relationships
INFO: Stored in Neo4j successfully
```

#### 4.3 Verify Upload in Neo4j
Open Neo4j Browser: http://localhost:7474

Run query:
```cypher
MATCH (n:Repository {name: "test-repo"})
RETURN n
```

Expected: Repository node with metadata

```cypher
MATCH (n)-[r]->(m)
WHERE n.repository_id = "YOUR_REPO_ID"
RETURN n, r, m
LIMIT 25
```

Expected: Graph of code entities and relationships

### Phase 5: Repository Management Testing

#### 5.1 View Repository List
1. Click "Repositories" button
2. Sidebar slides in from right

**Expected Results:**
- ✅ List of uploaded repositories
- ✅ Each shows: name, description, node count, date
- ✅ Hover effects work
- ✅ View and Delete buttons appear on hover

#### 5.2 Select Repository
1. Click on a repository card
2. Or click the "View" (eye) icon

**Expected Results:**
- ✅ Sidebar closes
- ✅ Graph updates with repository data
- ✅ Stats overlay shows repository name
- ✅ Node and edge counts update

#### 5.3 Delete Repository
1. Open repository list
2. Hover over a repository
3. Click "Delete" (trash) icon
4. Confirm deletion

**Expected Results:**
- ✅ Confirmation dialog appears
- ✅ Repository removed from list
- ✅ Data deleted from Neo4j
- ✅ If currently viewing, switches to default graph

### Phase 6: Graph Visualization Testing

#### 6.1 Test Node Interaction
1. Click on any node in the graph
2. Node details panel opens on left

**Expected Results:**
- ✅ Panel slides in smoothly
- ✅ Shows node type, name, properties
- ✅ Lists connections
- ✅ Close button works

#### 6.2 Test Graph Controls
1. **Zoom:** Scroll mouse wheel
2. **Rotate:** Click and drag
3. **Pan:** Right-click and drag

**Expected Results:**
- ✅ Smooth camera movements
- ✅ No OrbitControls errors
- ✅ Nodes remain clickable
- ✅ Edges stay visible

#### 6.3 Test Workflow View
1. Click "Show Workflows" button
2. View switches to workflow visualization

**Expected Results:**
- ✅ Workflow view loads
- ✅ Toggle button updates to "Show Graph"
- ✅ Can switch back to graph view

### Phase 7: AI Chat Testing

#### 7.1 Test AI Interaction
1. Select a node
2. Type question in AI chat: "Explain this component"
3. Send message

**Expected Results:**
- ✅ Message appears in chat
- ✅ AI response generated (mock or real)
- ✅ Response formatted nicely
- ✅ Can continue conversation

#### 7.2 Test Context Awareness
1. Select different nodes
2. Ask similar questions
3. Verify responses are contextual

### Phase 8: Performance Testing

#### 8.1 Large Repository Test
Upload a larger repository (e.g., 50+ files):

**Expected Results:**
- ✅ Upload completes within reasonable time
- ✅ Parsing doesn't timeout
- ✅ Graph renders smoothly
- ✅ No memory leaks

#### 8.2 Multiple Users Test
1. Open multiple browser tabs
2. Login with different users
3. Upload different repositories

**Expected Results:**
- ✅ Each user sees only their repositories
- ✅ No data leakage between users
- ✅ Concurrent uploads work

### Phase 9: Error Handling Testing

#### 9.1 Test Invalid Upload
1. Try uploading a .txt file
2. Try uploading a file > 50MB

**Expected Results:**
- ✅ Error message displayed
- ✅ Upload rejected
- ✅ Clear error explanation

#### 9.2 Test Network Errors
1. Stop backend server
2. Try to upload repository

**Expected Results:**
- ✅ Error message displayed
- ✅ No crash
- ✅ Can retry after backend restarts

#### 9.3 Test Authentication Errors
1. Use invalid credentials
2. Try expired token

**Expected Results:**
- ✅ Clear error messages
- ✅ Redirected to login
- ✅ Can re-authenticate

### Phase 10: UI/UX Testing

#### 10.1 Visual Design
Verify:
- ✅ Glassmorphism effects visible
- ✅ Animations smooth (60fps)
- ✅ Colors high contrast
- ✅ Text readable
- ✅ Buttons have hover effects

#### 10.2 Responsive Design
Test at different screen sizes:
- ✅ Desktop (1920x1080)
- ✅ Laptop (1366x768)
- ✅ Tablet (768x1024)

#### 10.3 Accessibility
- ✅ Keyboard navigation works
- ✅ Focus indicators visible
- ✅ Color contrast sufficient
- ✅ Error messages clear

## Common Issues and Solutions

### Issue 1: OrbitControls Error
**Symptom:** "Cannot read properties of undefined (reading 'x')"

**Solution:**
- Already fixed with control patching
- Verify `Graph3D.tsx` has the patch
- Clear browser cache

### Issue 2: Neo4j Connection Failed
**Symptom:** "Failed to connect to Neo4j"

**Solutions:**
1. Check Neo4j is running: `docker ps`
2. Verify credentials in `.env`
3. Test connection: `curl http://localhost:7474`
4. Check firewall settings

### Issue 3: Upload Fails
**Symptom:** "Upload failed" error

**Solutions:**
1. Check file size < 50MB
2. Verify file format (.zip, .tar.gz, .tgz)
3. Check backend logs for details
4. Ensure `uploads/` directory exists

### Issue 4: Token Expired
**Symptom:** "Unauthorized" errors

**Solution:**
1. Logout and login again
2. Check `ACCESS_TOKEN_EXPIRE_MINUTES` in `.env`
3. Clear localStorage: `localStorage.clear()`

### Issue 5: Graph Not Rendering
**Symptom:** Blank screen or loading forever

**Solutions:**
1. Check browser console for errors
2. Verify backend is running
3. Check graph data format
4. Try different browser

## Performance Benchmarks

### Expected Performance:
- **Page Load:** < 2 seconds
- **Login:** < 500ms
- **Upload (10MB):** < 5 seconds
- **Graph Render (100 nodes):** < 1 second
- **Node Click Response:** < 100ms

### Memory Usage:
- **Frontend:** ~150MB
- **Backend:** ~200MB
- **Neo4j:** ~500MB

## Security Checklist

- ✅ Passwords hashed with bcrypt
- ✅ JWT tokens used for auth
- ✅ CORS configured properly
- ✅ File upload size limited
- ✅ User data isolated
- ✅ SQL injection prevented (using ORM)
- ✅ XSS protection enabled

## Production Deployment Checklist

Before deploying to production:

1. **Environment Variables:**
   - [ ] Change `SECRET_KEY` to strong random value
   - [ ] Update `NEO4J_PASSWORD`
   - [ ] Set `ACCESS_TOKEN_EXPIRE_MINUTES` appropriately
   - [ ] Configure production URLs

2. **Security:**
   - [ ] Enable HTTPS
   - [ ] Configure CORS for production domain
   - [ ] Set up rate limiting
   - [ ] Enable security headers

3. **Database:**
   - [ ] Backup Neo4j data
   - [ ] Set up monitoring
   - [ ] Configure persistence

4. **Monitoring:**
   - [ ] Set up logging
   - [ ] Configure error tracking
   - [ ] Add performance monitoring

5. **Testing:**
   - [ ] Run all integration tests
   - [ ] Load testing
   - [ ] Security audit

## Support

If you encounter issues:

1. Check backend logs: `backend/logs/`
2. Check browser console
3. Review Neo4j logs
4. Consult documentation:
   - `ADVANCED_FEATURES_GUIDE.md`
   - `TROUBLESHOOTING.md`
   - `API_SPECIFICATION.md`

## Success Criteria

All tests pass when:
- ✅ Users can register and login
- ✅ Repositories can be uploaded and parsed
- ✅ Graphs visualize correctly
- ✅ Node interactions work smoothly
- ✅ AI chat responds appropriately
- ✅ No console errors
- ✅ Performance meets benchmarks
- ✅ UI is responsive and beautiful

---

**Testing Complete!** 🎉

Your GraphMind AI platform is now fully integrated and ready for use.