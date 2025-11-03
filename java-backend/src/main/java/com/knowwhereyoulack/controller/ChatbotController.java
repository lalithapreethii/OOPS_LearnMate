package com.knowwhereyoulack.controller;

import java.io.IOException;
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.time.Duration;
import java.util.Arrays;
import java.util.List;
import java.util.Map;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.google.gson.Gson;
import com.google.gson.JsonArray;
import com.google.gson.JsonElement;
import com.google.gson.JsonObject;
import com.google.gson.JsonParser;

@RestController
@RequestMapping("/api/chatbot")
@CrossOrigin(origins = "http://localhost:5173")
public class ChatbotController {

    private static final Logger logger = LoggerFactory.getLogger(ChatbotController.class);

    @Value("${groq.api.key:}")
    private String groqApiKey;

    @Value("${groq.api.url:https://api.groq.com/openai/v1/chat/completions}")
    private String groqApiUrl;

    @Value("${groq.model:llama-3.1-8b-instant}")
    private String groqModel;

    private final HttpClient httpClient = HttpClient.newBuilder()
            .connectTimeout(Duration.ofSeconds(15))
            .build();

    private final Gson gson = new Gson();

    // ========================================
    // EDUCATION FILTERING SYSTEM
    // ========================================

    private static final List<String> EDUCATIONAL_KEYWORDS = Arrays.asList(
        // Core subjects
        "math", "mathematics", "science", "physics", "chemistry", "biology",
        "history", "geography", "english", "literature", "grammar", "writing",
        "computer", "programming", "coding", "algorithm", "data structure",
        // Programming languages
        "java", "python", "javascript", "react", "html", "css", "sql", "c++",
        // Math topics
        "calculus", "algebra", "geometry", "statistics", "probability", "trigonometry",
        "derivative", "integral", "function", "variable", "theorem", "proof",
        // General academic
        "study", "learn", "education", "quiz", "test", "exam", "homework",
        "assignment", "research", "essay", "problem", "solution", "concept",
        "theory", "practice", "tutorial", "lesson", "course", "subject", "topic",
        // Action words
        "explain", "understand", "help", "question", "answer", "teach", "show",
        // Science terms
        "photosynthesis", "cell", "atom", "molecule", "equation", "formula",
        // CS terms
        "array", "loop", "class", "object", "method", "recursion", "api"
    );

    private static final List<String> BLACKLISTED_KEYWORDS = Arrays.asList(
        "movie", "film", "song", "music", "game", "gaming", "sport", "football",
        "cricket", "recipe", "cooking", "fashion", "celebrity", "gossip",
        "politics", "election", "dating", "relationship", "joke", "meme",
        "weather", "news", "stocks", "cryptocurrency", "shopping"
    );

    /**
     * Check if a message is education-related
     * LENIENT FILTER: Only reject obvious non-educational topics
     */
    private boolean isEducationalQuery(String message) {
        String lowerMessage = message.toLowerCase();
        
        // Reject only very obvious blacklisted topics (entertainment/social)
        for (String blacklisted : BLACKLISTED_KEYWORDS) {
            if (lowerMessage.contains(blacklisted)) {
                logger.info("Message rejected: Contains blacklisted keyword '{}'", blacklisted);
                return false;
            }
        }
        
        // Accept if contains educational keywords
        for (String educational : EDUCATIONAL_KEYWORDS) {
            if (lowerMessage.contains(educational)) {
                logger.info("Message approved: Contains educational keyword '{}'", educational);
                return true;
            }
        }
        
        // Accept questions (very permissive)
        if (lowerMessage.matches(".*(\\?|what|how|why|when|where|who|explain|define|describe|teach|show|tell|give|provide|can you).*")) {
            logger.info("Message approved: Question format detected");
            return true;
        }
        
        // Accept if message contains common academic words (law, theory, rule, formula, etc.)
        String[] academicPatterns = {
            "law", "theory", "rule", "principle", "formula", "equation", "concept",
            "compound", "element", "force", "energy", "motion", "reaction", "process",
            "structure", "system", "method", "technique", "solution", "definition",
            "analysis", "theorem", "proof", "axiom", "property", "characteristic"
        };
        
        for (String pattern : academicPatterns) {
            if (lowerMessage.contains(pattern)) {
                logger.info("Message approved: Contains academic pattern '{}'", pattern);
                return true;
            }
        }
        
        // If message is longer than 5 words, likely a genuine question - accept it
        if (message.split("\\s+").length >= 5) {
            logger.info("Message approved: Long enough to be a genuine educational query");
            return true;
        }
        
        logger.info("Message rejected: No educational indicators found");
        return false;
    }

    // ========================================
    // MAIN ENDPOINT
    // ========================================

    @PostMapping("/message")
    public ResponseEntity<?> message(@RequestBody Map<String, Object> payload) {
        logger.info("=== CHATBOT REQUEST RECEIVED ===");
        logger.debug("Payload: {}", payload);
        
        // Step 1: Validate API key
        if (groqApiKey == null || groqApiKey.isBlank() || groqApiKey.equals("YOUR_GROQ_API_KEY_HERE")) {
            logger.error("Groq API key not configured!");
            return ResponseEntity.ok(Map.of(
                "reply", "⚠️ The AI tutor is currently unavailable. Please contact the administrator to configure the Groq API key."
            ));
        }

        logger.info("Groq API configured - Key: {}..., Model: {}, URL: {}", 
            groqApiKey.substring(0, Math.min(15, groqApiKey.length())), 
            groqModel, 
            groqApiUrl
        );

        // Step 2: Extract user message
        Object messageObj = payload.get("message");
        String userMessage = messageObj == null ? "" : messageObj.toString().trim();

        if (userMessage.isEmpty()) {
            logger.warn("Empty message received");
            return ResponseEntity.ok(Map.of(
                "reply", "Please ask me a question about your studies!"
            ));
        }

        logger.info("User message: '{}'", userMessage);

        // Step 3: Education domain check
        if (!isEducationalQuery(userMessage)) {
            return ResponseEntity.ok(Map.of(
                "reply", "🎓 I'm Skilli, your educational AI tutor! I can only help with academic topics like mathematics, science, programming, languages, and other educational subjects.\n\n" +
                        "Please ask me questions related to:\n" +
                        "• Math, Science, or Programming\n" +
                        "• Study tips and learning strategies\n" +
                        "• Subject explanations and concepts\n" +
                        "• Homework or assignment help\n\n" +
                        "How can I help you learn today? 📚"
            ));
        }

        // Step 4: Call Groq API
        try {
            return callGroqAPI(userMessage);
        } catch (Exception e) {
            logger.error("Unexpected error in chatbot controller", e);
            return ResponseEntity.ok(Map.of(
                "reply", "⚠️ An unexpected error occurred. Please try again."
            ));
        }
    }

    // ========================================
    // GROQ API CALL
    // ========================================

    private ResponseEntity<?> callGroqAPI(String userMessage) {
        try {
            logger.info("Calling Groq API...");

            // Build request body
            JsonObject requestBody = new JsonObject();
            requestBody.addProperty("model", groqModel);

            // Messages array with system instruction
            JsonArray messages = new JsonArray();

            // System message - strict education-only instruction
            JsonObject systemMessage = new JsonObject();
            systemMessage.addProperty("role", "system");
            systemMessage.addProperty("content", buildSystemPrompt());
            messages.add(systemMessage);

            // User message
            JsonObject userMsg = new JsonObject();
            userMsg.addProperty("role", "user");
            userMsg.addProperty("content", userMessage);
            messages.add(userMsg);

            requestBody.add("messages", messages);

            // Parameters (optimized for free tier)
            requestBody.addProperty("temperature", 0.7);
            requestBody.addProperty("max_tokens", 800);
            requestBody.addProperty("top_p", 0.9);
            requestBody.addProperty("stream", false);

            String requestBodyJson = gson.toJson(requestBody);
            logger.debug("Request body: {}", requestBodyJson);

            // Send HTTP request
            HttpRequest request = HttpRequest.newBuilder()
                    .uri(URI.create(groqApiUrl))
                    .timeout(Duration.ofSeconds(30))
                    .header("Content-Type", "application/json")
                    .header("Authorization", "Bearer " + groqApiKey)
                    .POST(HttpRequest.BodyPublishers.ofString(requestBodyJson))
                    .build();

            HttpResponse<String> response = httpClient.send(request, HttpResponse.BodyHandlers.ofString());

            logger.info("Groq API response status: {}", response.statusCode());
            logger.debug("Response body: {}", response.body());

            // Handle response
            return handleGroqResponse(response);

        } catch (IOException ex) {
            logger.error("IO error calling Groq API", ex);
            return ResponseEntity.ok(Map.of(
                "reply", "⚠️ Network error. Please check your connection and try again."
            ));
        } catch (InterruptedException ex) {
            Thread.currentThread().interrupt();
            logger.error("Request interrupted", ex);
            return ResponseEntity.ok(Map.of(
                "reply", "⚠️ Request was interrupted. Please try again."
            ));
        } catch (Exception ex) {
            logger.error("Unexpected error calling Groq API", ex);
            return ResponseEntity.ok(Map.of(
                "reply", "⚠️ An error occurred. Please try again."
            ));
        }
    }

    // ========================================
    // RESPONSE HANDLER (FIXED)
    // ========================================

    private ResponseEntity<?> handleGroqResponse(HttpResponse<String> response) {
        int statusCode = response.statusCode();
        String responseBody = response.body();

        // Success (200-299)
        if (statusCode >= 200 && statusCode < 300) {
            try {
                // Parse JSON response
                JsonElement jsonElement = JsonParser.parseString(responseBody);
                
                if (!jsonElement.isJsonObject()) {
                    logger.error("Response is not a JSON object");
                    return ResponseEntity.ok(Map.of(
                        "reply", "I received an unexpected response format. Please try again."
                    ));
                }
                
                JsonObject json = jsonElement.getAsJsonObject();
                
                // Extract reply from choices
                if (json.has("choices")) {
                    JsonArray choices = json.getAsJsonArray("choices");
                    if (choices != null && choices.size() > 0) {
                        JsonObject firstChoice = choices.get(0).getAsJsonObject();
                        if (firstChoice.has("message")) {
                            JsonObject message = firstChoice.getAsJsonObject("message");
                            if (message.has("content")) {
                                String replyText = message.get("content").getAsString().trim();
                                logger.info("AI reply received ({} chars)", replyText.length());
                                logger.debug("AI reply: {}", replyText);
                                return ResponseEntity.ok(Map.of("reply", replyText));
                            }
                        }
                    }
                }

                // Check for error field
                if (json.has("error")) {
                    JsonObject error = json.getAsJsonObject("error");
                    String errorMsg = error.has("message") ? error.get("message").getAsString() : "Unknown error";
                    logger.error("Groq API returned error: {}", errorMsg);
                    return ResponseEntity.ok(Map.of(
                        "reply", "🤖 API Error: " + errorMsg
                    ));
                }

            } catch (Exception e) {
                logger.error("Error parsing Groq response", e);
                logger.error("Response body was: {}", responseBody);
            }
            
            return ResponseEntity.ok(Map.of(
                "reply", "I'm having trouble understanding the response. Could you rephrase your question?"
            ));
        }

        // Authentication error (401)
        if (statusCode == 401) {
            logger.error("Groq API authentication failed - invalid API key");
            return ResponseEntity.ok(Map.of(
                "reply", "⚠️ API authentication failed. Please check the API key configuration."
            ));
        }

        // Rate limit (429)
        if (statusCode == 429) {
            logger.warn("Groq API rate limit exceeded");
            return ResponseEntity.ok(Map.of(
                "reply", "⚠️ Rate limit reached. Please wait a moment and try again."
            ));
        }

        // Bad Request (400)
        if (statusCode == 400) {
            logger.error("Bad request to Groq API: {}", responseBody);
            return ResponseEntity.ok(Map.of(
                "reply", "⚠️ Invalid request format. Please try again."
            ));
        }

        // Other errors
        logger.error("Groq API error: {} - {}", statusCode, responseBody);
        return ResponseEntity.ok(Map.of(
            "reply", "🤖 I'm experiencing technical difficulties (Error " + statusCode + "). Please try again in a moment."
        ));
    }

    // ========================================
    // SYSTEM PROMPT
    // ========================================

    private String buildSystemPrompt() {
        return "You are Skilli, an AI educational tutor for the KnowWhereYouLack platform. " +
               "Your ONLY purpose is to help students learn academic subjects.\n\n" +
               "STRICT RULES:\n" +
               "1. ONLY answer questions about education, academics, studying, and learning\n" +
               "2. Subjects you can help with: Math, Science, Programming, Languages, History, Literature, etc.\n" +
               "3. You MUST refuse to discuss: entertainment, sports, politics, gossip, recipes, dating, or any non-educational topics\n" +
               "4. If asked about non-educational topics, politely redirect to educational content\n" +
               "5. Keep responses concise, clear, and student-friendly (2-3 paragraphs max)\n" +
               "6. Use examples and analogies to explain concepts\n" +
               "7. Encourage critical thinking and problem-solving\n" +
               "8. Break down complex topics into simple steps\n" +
               "9. Use emojis sparingly for engagement (📚, 💡, ✨)\n\n" +
               "Your goal: Help students UNDERSTAND concepts, not just provide answers.";
    }
}
