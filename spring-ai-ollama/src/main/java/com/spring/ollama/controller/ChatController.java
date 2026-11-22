package com.spring.ollama.controller;

import com.spring.ollama.service.ChatService;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

/** HTTP endpoint for asking the configured Ollama model a question. */
@RestController
@RequestMapping
public class ChatController {

    private final ChatService chatService;

    // Constructor injection keeps the web layer independent of the AI client implementation.
    public ChatController(ChatService chatService) {
        this.chatService = chatService;
    }

    /** Example: GET /chat?q=Explain%20Java%20records */
    @GetMapping("/chat")
    public ResponseEntity<String> chat(@RequestParam("q") String query) {
        if (query.isBlank()) {
            return ResponseEntity.badRequest().body("Query parameter 'q' must not be blank.");
        }
        return ResponseEntity.ok(chatService.chat(query));
    }
}
