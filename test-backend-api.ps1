# Test Backend Quiz API
# This script tests the difficulty-based quiz endpoints

Write-Host "`n" -NoNewline
Write-Host "========================================" -ForegroundColor Cyan
Write-Host " TESTING BACKEND QUIZ API" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$baseUrl = "http://localhost:8082/api/quiz"

# Test 1: Get All Topics
Write-Host "TEST 1: Get All Topics" -ForegroundColor Yellow
Write-Host "URL: $baseUrl/topics" -ForegroundColor Gray
try {
    $response = Invoke-RestMethod -Uri "$baseUrl/topics" -Method Get
    Write-Host "✅ SUCCESS: Got $($response.Count) topics" -ForegroundColor Green
    $response | ForEach-Object {
        Write-Host "   - Topic $($_.topicId): $($_.topicName) ($($_.questionCount) questions)" -ForegroundColor White
    }
} catch {
    Write-Host "❌ FAILED: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""

# Test 2: Get EASY Questions for Topic 1
Write-Host "TEST 2: Get EASY Questions (Topic 1)" -ForegroundColor Yellow
Write-Host "URL: $baseUrl/1/difficulty/EASY" -ForegroundColor Gray
try {
    $response = Invoke-RestMethod -Uri "$baseUrl/1/difficulty/EASY" -Method Get
    $questionCount = $response.questions.Count
    Write-Host "✅ SUCCESS: Got $questionCount questions" -ForegroundColor Green
    Write-Host "   Topic ID: $($response.topicId)" -ForegroundColor White
    Write-Host "   Topic Name: $($response.topicName)" -ForegroundColor White
    
    if ($questionCount -eq 10) {
        Write-Host "   ✅ CORRECT: Exactly 10 questions returned" -ForegroundColor Green
    } else {
        Write-Host "   ⚠️  WARNING: Expected 10 questions, got $questionCount" -ForegroundColor Yellow
    }
    
    # Show first question
    if ($response.questions.Count -gt 0) {
        Write-Host "   First Question: $($response.questions[0].questionText)" -ForegroundColor Cyan
    }
} catch {
    Write-Host "❌ FAILED: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""

# Test 3: Get MEDIUM Questions for Topic 1
Write-Host "TEST 3: Get MEDIUM Questions (Topic 1)" -ForegroundColor Yellow
Write-Host "URL: $baseUrl/1/difficulty/MEDIUM" -ForegroundColor Gray
try {
    $response = Invoke-RestMethod -Uri "$baseUrl/1/difficulty/MEDIUM" -Method Get
    $questionCount = $response.questions.Count
    Write-Host "✅ SUCCESS: Got $questionCount questions" -ForegroundColor Green
    
    if ($questionCount -eq 10) {
        Write-Host "   ✅ CORRECT: Exactly 10 questions returned" -ForegroundColor Green
    } else {
        Write-Host "   ⚠️  WARNING: Expected 10 questions, got $questionCount" -ForegroundColor Yellow
    }
} catch {
    Write-Host "❌ FAILED: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""

# Test 4: Get HARD Questions for Topic 1
Write-Host "TEST 4: Get HARD Questions (Topic 1)" -ForegroundColor Yellow
Write-Host "URL: $baseUrl/1/difficulty/HARD" -ForegroundColor Gray
try {
    $response = Invoke-RestMethod -Uri "$baseUrl/1/difficulty/HARD" -Method Get
    $questionCount = $response.questions.Count
    Write-Host "✅ SUCCESS: Got $questionCount questions" -ForegroundColor Green
    
    if ($questionCount -eq 10) {
        Write-Host "   ✅ CORRECT: Exactly 10 questions returned" -ForegroundColor Green
    } else {
        Write-Host "   ⚠️  WARNING: Expected 10 questions, got $questionCount" -ForegroundColor Yellow
    }
} catch {
    Write-Host "❌ FAILED: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host " TEST COMPLETE" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "NEXT STEPS:" -ForegroundColor Magenta
Write-Host "1. If all tests passed with 10 questions: ✅ Backend is working correctly" -ForegroundColor Green
Write-Host "2. If fewer than 10 questions: ⚠️  Check database for question count" -ForegroundColor Yellow
Write-Host "3. If tests failed: ❌ Make sure backend is running on port 8082" -ForegroundColor Red
Write-Host ""
