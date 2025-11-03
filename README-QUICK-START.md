# 🚀 QUICK START GUIDE

## ⚡ FASTEST WAY TO RUN (3 Steps)

### 1️⃣ Make sure MySQL is running
```powershell
net start MySQL80
```

### 2️⃣ Run the startup script
```powershell
cd D:\Know-Where-You-Lack
.\START-ALL.ps1
```

### 3️⃣ Wait for browser to open
- Frontend: http://localhost:5173
- Backend: http://localhost:8082

---

## ✅ WHAT'S BEEN INTEGRATED

| Feature | Status | Description |
|---------|--------|-------------|
| **Notes** | ✅ | Create/Edit/Delete notes saved to MySQL |
| **Quiz Results** | ✅ | All quiz scores saved to database |
| **Dashboard** | ✅ | Real-time analytics from database |
| **Timer** | ✅ | Study sessions tracked |
| **Chatbot** | ✅ | Skilli AI with GROQ API |
| **Floating Avatar** | ✅ | Animated Skilli button |
| **Dark Mode** | ✅ | Theme toggle with persistence |
| **Resources** | ✅ | Learning materials library |
| **Profile** | ✅ | User stats and history |

---

## 🧪 TEST THE INTEGRATION

### Test 1: Notes
1. Click "My Notes" (diamond button)
2. Create a new note
3. **Refresh the page**
4. ✅ Note is still there (saved to backend!)

### Test 2: Quiz
1. Take any quiz
2. Complete it
3. Go to Dashboard
4. ✅ See updated quiz count and stats

### Test 3: Dashboard
1. Open Dashboard
2. Check browser console (F12)
3. ✅ See: "Dashboard data loaded from backend"

### Test 4: Timer
1. Click Timer button
2. Set 1 minute
3. Wait for completion
4. Check backend terminal
5. ✅ See: "📚 Study session saved"

### Test 5: Chatbot
1. Click Floating Skilli
2. Ask: "Explain Newton's laws"
3. ✅ Get educational response

---

## 🆘 IF SOMETHING DOESN'T WORK

### Backend Issues
```powershell
# Delete conflicting files
Remove-Item "D:\Know-Where-You-Lack\java-backend\src\main\java\com\knowwhereyoulack\model\Quiz.java" -ErrorAction SilentlyContinue

# Rebuild
cd D:\Know-Where-You-Lack\java-backend
mvn clean install -DskipTests
java -jar target/backend-1.0.0.jar
```

### Frontend Issues
```powershell
cd D:\Know-Where-You-Lack\frontend
npm install
npm run dev
```

### Database Issues
```sql
-- Create database if not exists
CREATE DATABASE IF NOT EXISTS knowwhereyoulack;

-- Check tables
SHOW TABLES;
```

---

## 📊 CHECK DATABASE

```sql
-- Connect to MySQL
mysql -u root -p

-- Use database
USE knowwhereyoulack;

-- See all notes
SELECT * FROM notes;

-- See all quiz results
SELECT * FROM quiz_results;

-- Count total quizzes
SELECT COUNT(*) FROM quiz_results WHERE user_id = 1;

-- Get average score
SELECT AVG(accuracy) FROM quiz_results WHERE user_id = 1;
```

---

## 🎯 KEY FEATURES TO DEMO

1. **Create a Note** → It persists after refresh
2. **Take 3 Quizzes** → Dashboard updates automatically
3. **Check Weak Topics** → Shows subjects < 80%
4. **Use Timer** → Sessions logged in backend
5. **Ask Skilli** → AI responds to educational questions

---

## 📁 FILES MODIFIED

### Frontend (1 file)
- `frontend/src/App.tsx` - Added backend API calls

### Backend (5 files)
- `AnalyticsController.java` - Added quiz result endpoint
- `AnalyticsService.java` - Added saveQuizResult method
- `StudySessionController.java` - NEW - Timer sessions
- `NotesController.java` - Already existed
- `NoteService.java` - Already existed

---

## 🔥 EVERYTHING IS READY!

**Your app now has:**
- ✅ Full backend integration
- ✅ Real database persistence
- ✅ Live analytics
- ✅ AI chatbot
- ✅ All features working together

**Just run `.\START-ALL.ps1` and you're good to go!**

---

Need help? Check `INTEGRATION-COMPLETE.md` for detailed documentation.
