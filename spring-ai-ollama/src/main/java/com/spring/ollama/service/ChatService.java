package com.spring.ollama.service;

/** Application operation for sending a question to the configured Ollama model. */
public interface ChatService {

    /** Sends a question and returns the model's response. */
    String chat(String query);
}
