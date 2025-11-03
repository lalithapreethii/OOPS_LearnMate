# ========================================
# QUICK START - KnowWhereYouLack with Difficulty Slider
# ========================================

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   KnowWhereYouLack - Quick Start" -ForegroundColor Cyan
Write-Host "   Difficulty Slider Integration" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

# Step 1: Check MySQL
Write-Host "[1/5] Checking MySQL..." -ForegroundColor Yellow
$mysqlProcess = Get-Process mysqld -ErrorAction SilentlyContinue
if ($mysqlProcess) {
    Write-Host "✓ MySQL is running" -ForegroundColor Green
} else {
    Write-Host "✗ MySQL is NOT running. Please start MySQL first." -ForegroundColor Red
    Write-Host "   Run: net start MySQL80" -ForegroundColor Yellow
    exit 1
}

# Step 2: Setup Database
Write-Host "`n[2/5] Setting up database..." -ForegroundColor Yellow
Write-Host "   Please run these SQL commands manually:" -ForegroundColor Cyan
Write-Host "   mysql -u root -p" -ForegroundColor White
Write-Host "   USE knowwhereyoulack;" -ForegroundColor White
Write-Host "   SOURCE D:/Know-Where-You-Lack/database/setup_topics.sql;" -ForegroundColor White
Write-Host "   SOURCE D:/Know-Where-You-Lack/database/insert_quiz_questions.sql;" -ForegroundColor White
Write-Host "`n   Press ENTER when database setup is complete..." -ForegroundColor Yellow
$null = Read-Host

# Step 3: Build Backend
Write-Host "`n[3/5] Building Java Backend..." -ForegroundColor Yellow
cd D:\Know-Where-You-Lack\java-backend
Write-Host "   Running: mvn clean install -DskipTests" -ForegroundColor Cyan
mvn clean install -DskipTests

if ($LASTEXITCODE -ne 0) {
    Write-Host "✗ Backend build failed!" -ForegroundColor Red
    exit 1
}
Write-Host "✓ Backend built successfully" -ForegroundColor Green

# Step 4: Start Backend (in background)
Write-Host "`n[4/5] Starting Backend Server..." -ForegroundColor Yellow
Write-Host "   Starting on http://localhost:8082" -ForegroundColor Cyan
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd D:\Know-Where-You-Lack\java-backend; mvn spring-boot:run"

# Wait for backend to start
Write-Host "   Waiting for backend to start..." -ForegroundColor Yellow
$maxAttempts = 30
$attempt = 0
$backendReady = $false

while ($attempt -lt $maxAttempts) {
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:8082/api/quiz/topics" -Method GET -TimeoutSec 2 -ErrorAction Stop
        if ($response.StatusCode -eq 200) {
            $backendReady = $true
            break
        }
    } catch {
        # Backend not ready yet
    }
    Start-Sleep -Seconds 2
    $attempt++
    Write-Host "   Attempt $attempt/$maxAttempts..." -ForegroundColor Gray
}

if ($backendReady) {
    Write-Host "✓ Backend is ready!" -ForegroundColor Green
} else {
    Write-Host "⚠ Backend taking longer than expected. Please check manually." -ForegroundColor Yellow
}

# Step 5: Start Frontend
Write-Host "`n[5/5] Starting Frontend..." -ForegroundColor Yellow
cd D:\Know-Where-You-Lack\frontend
Write-Host "   Starting on http://localhost:5173" -ForegroundColor Cyan
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd D:\Know-Where-You-Lack\frontend; npm run dev"

# Wait a bit for frontend to start
Start-Sleep -Seconds 5

# Open browser
Write-Host "`n✓ Opening browser..." -ForegroundColor Green
Start-Process "http://localhost:5173"

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "   ✓ ALL SERVICES STARTED!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "`nServices Running:" -ForegroundColor Yellow
Write-Host "   • Backend:  http://localhost:8082" -ForegroundColor White
Write-Host "   • Frontend: http://localhost:5173" -ForegroundColor White
Write-Host "   • MySQL:    localhost:3306" -ForegroundColor White

Write-Host "`n🎯 Quick Test:" -ForegroundColor Yellow
Write-Host "   1. Go to Quizzes page" -ForegroundColor White
Write-Host "   2. Use the difficulty slider" -ForegroundColor White
Write-Host "   3. Select a topic (OOP, DSA, or Physics)" -ForegroundColor White
Write-Host "   4. Start quiz and see 10 questions!" -ForegroundColor White

Write-Host "`n📊 Test API Endpoints:" -ForegroundColor Yellow
Write-Host "   curl http://localhost:8082/api/quiz/topics" -ForegroundColor White
Write-Host "   curl http://localhost:8082/api/quiz/1/difficulty/EASY" -ForegroundColor White

Write-Host "`n📖 Documentation:" -ForegroundColor Yellow
Write-Host "   See: DIFFICULTY-SLIDER-IMPLEMENTATION.md" -ForegroundColor White

Write-Host "`nPress any key to exit this window..." -ForegroundColor Gray
$null = Read-Host
