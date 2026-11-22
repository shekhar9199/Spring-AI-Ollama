package com.spring.ollama.service;

import org.springframework.ai.chat.client.ChatClient;
import org.springframework.stereotype.Service;

/** Uses Spring AI's fluent ChatClient API to communicate with Ollama. */
@Service
public class ChatServiceImpl implements ChatService {

    private final ChatClient chatClient;

    public ChatServiceImpl(ChatClient.Builder builder) {
        // Spring AI auto-configures this builder from the spring.ai.ollama.* properties.
        this.chatClient = builder.build();
    }

    @Override
    public String chat(String query) {
        // Build a user prompt, call the local model, and return its text response.
        return chatClient.prompt()
                .user(query)
                .call()
                .content();
    }
}
