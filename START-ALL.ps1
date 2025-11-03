# ========================================
# KNOW WHERE YOU LACK - COMPLETE STARTUP
# ========================================

Write-Host "🚀 Starting Know-Where-You-Lack Application..." -ForegroundColor Cyan
Write-Host ""

# Check if MySQL is running
Write-Host "📊 Checking MySQL..." -ForegroundColor Yellow
$mysqlRunning = Get-Process -Name "mysqld" -ErrorAction SilentlyContinue
if (!$mysqlRunning) {
    Write-Host "❌ MySQL is not running! Please start MySQL first." -ForegroundColor Red
    Write-Host "   Run: net start MySQL80" -ForegroundColor Gray
    exit 1
}
Write-Host "✅ MySQL is running" -ForegroundColor Green
Write-Host ""

# Start Backend
Write-Host "🔧 Starting Backend (Spring Boot)..." -ForegroundColor Yellow
Write-Host "   This will take 30-60 seconds..." -ForegroundColor Gray
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PSScriptRoot\java-backend'; Write-Host '🔧 Building and starting backend...' -ForegroundColor Cyan; mvn clean install -DskipTests; Write-Host '✅ Backend built! Starting server...' -ForegroundColor Green; java -jar target/backend-1.0.0.jar"

# Wait for backend to start
Write-Host "⏳ Waiting for backend to start on port 8082..." -ForegroundColor Yellow
$maxAttempts = 30
$attempt = 0
$backendReady = $false

while ($attempt -lt $maxAttempts -and !$backendReady) {
    Start-Sleep -Seconds 2
    $connection = Test-NetConnection -ComputerName localhost -Port 8082 -WarningAction SilentlyContinue -ErrorAction SilentlyContinue
    if ($connection.TcpTestSucceeded) {
        $backendReady = $true
    }
    $attempt++
    Write-Host "." -NoNewline
}

Write-Host ""
if ($backendReady) {
    Write-Host "✅ Backend is ready on http://localhost:8082" -ForegroundColor Green
} else {
    Write-Host "⚠️  Backend taking longer than expected. Check the backend terminal." -ForegroundColor Yellow
}
Write-Host ""

# Start Frontend
Write-Host "🎨 Starting Frontend (Vite)..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PSScriptRoot\frontend'; Write-Host '🎨 Starting frontend dev server...' -ForegroundColor Cyan; npm run dev"

# Wait a bit for frontend to start
Start-Sleep -Seconds 5

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "✅ APPLICATION STARTED!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "📱 Frontend:  http://localhost:5173" -ForegroundColor White
Write-Host "🔧 Backend:   http://localhost:8082" -ForegroundColor White
Write-Host "💾 Database:  MySQL on localhost:3306" -ForegroundColor White
Write-Host ""
Write-Host "🔥 FEATURES INTEGRATED:" -ForegroundColor Yellow
Write-Host "  ✅ Notes with backend API" -ForegroundColor White
Write-Host "  ✅ Quiz results saved to database" -ForegroundColor White
Write-Host "  ✅ Dashboard with real analytics" -ForegroundColor White
Write-Host "  ✅ Timer sessions tracked" -ForegroundColor White
Write-Host "  ✅ Skilli chatbot with GROQ AI" -ForegroundColor White
Write-Host ""
Write-Host "Press Enter to open the application in your browser..." -ForegroundColor Cyan
Read-Host

Start-Process "http://localhost:5173"

Write-Host ""
Write-Host "🎉 All set! Happy learning!" -ForegroundColor Green
Write-Host ""
