# 🚀 QUICK START GUIDE - Difficulty Slider Feature

## ⚡ 3-STEP STARTUP

### **Step 1: Database Setup (2 minutes)**
```bash
mysql -u root -p
```
```sql
USE knowwhereyoulack;
SOURCE D:/Know-Where-You-Lack/database/setup_topics.sql;
SOURCE D:/Know-Where-You-Lack/database/insert_quiz_questions.sql;
```

### **Step 2: Start Backend (1 minute)**
```powershell
cd D:\Know-Where-You-Lack\java-backend
mvn clean install -DskipTests
mvn spring-boot:run
```
Wait for: `Started KnowWhereYouLackApplication`

### **Step 3: Start Frontend (30 seconds)**
```powershell
cd D:\Know-Where-You-Lack\frontend
npm run dev
```
Open: http://localhost:5173

---

## 🎯 NEW FEATURES

### **✨ Difficulty Slider**
- Beautiful animated slider
- 3 levels: EASY 🟢 | MEDIUM 🟠 | HARD 🔴
- Drag to select or click buttons
- Real-time color feedback

### **🔌 Backend Integration**
- New endpoint: `GET /api/quiz/{topicId}/difficulty/{difficulty}`
- Returns 10 random questions per quiz
- Filters by difficulty level
- Automatic fallback to mock data

---

## 🧪 QUICK TEST

1. **Go to Quizzes** → See slider
2. **Select EASY** → Click OOP → Start Quiz
3. **Answer 10 questions** → Submit
4. **Check Dashboard** → Stats updated!

---

## 📊 TEST COMMANDS

```powershell
# Test topics
curl http://localhost:8082/api/quiz/topics

# Test difficulties
curl http://localhost:8082/api/quiz/1/difficulty/EASY
curl http://localhost:8082/api/quiz/1/difficulty/MEDIUM
curl http://localhost:8082/api/quiz/1/difficulty/HARD
```

---

## 📁 FILES CHANGED

### Backend (Java)
- ✅ `QuestionRepository.java` - Added difficulty filtering
- ✅ `QuizService.java` - Added new method
- ✅ `QuizServiceImpl.java` - Implemented logic
- ✅ `QuizController.java` - New endpoint

### Frontend (React)
- ✅ `DifficultySlider.tsx` - NEW component
- ✅ `App.tsx` - Integrated slider + backend API

### Database
- ✅ `setup_topics.sql` - NEW topics setup
- ✅ `insert_quiz_questions.sql` - Existing (90 questions)

---

## 🎨 SLIDER COLORS

| Difficulty | Color | Hex Code |
|------------|-------|----------|
| EASY | Green 🟢 | #4CAF50 |
| MEDIUM | Orange 🟠 | #FF9800 |
| HARD | Red 🔴 | #F44336 |

---

## ✅ SUCCESS INDICATORS

- ✓ Slider changes color when dragging
- ✓ Backend returns exactly 10 questions
- ✓ Questions match selected difficulty
- ✓ Quiz completes without errors
- ✓ Dashboard updates after submission

---

## 🐛 COMMON ISSUES

**Backend not starting?**
```powershell
mvn clean install -DskipTests
```

**No questions found?**
```sql
-- Run in MySQL
SOURCE D:/Know-Where-You-Lack/database/insert_quiz_questions.sql;
```

**CORS error?**
- Check backend is running on port 8082
- Check frontend is on port 5173

---

## 📖 FULL DOCUMENTATION

See: `DIFFICULTY-SLIDER-IMPLEMENTATION.md`

---

## 🎊 YOU'RE READY!

Everything is set up. Just run the 3 steps above and enjoy your enhanced quiz system with difficulty filtering! 🚀
