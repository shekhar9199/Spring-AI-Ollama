package com.spring.ollama;

import com.spring.ollama.controller.ChatController;
import com.spring.ollama.service.ChatService;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.test.web.servlet.MockMvc;

import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.content;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;
import static org.springframework.test.web.servlet.setup.MockMvcBuilders.standaloneSetup;

/** Controller tests use a mocked service, so Ollama does not need to be running. */
class SpringAiOllamApplicationTests {

    private ChatService chatService;
    private MockMvc mockMvc;

    @BeforeEach
    void setUp() {
        chatService = mock(ChatService.class);
        mockMvc = standaloneSetup(new ChatController(chatService)).build();
    }

    @Test
    void chatEndpointReturnsTheServiceAnswer() throws Exception {
        when(chatService.chat("Explain Java records"))
                .thenReturn("A record is a concise class for immutable data carriers.");

        mockMvc.perform(get("/chat").param("q", "Explain Java records"))
                .andExpect(status().isOk())
                .andExpect(content().string("A record is a concise class for immutable data carriers."));

        verify(chatService).chat("Explain Java records");
    }

    @Test
    void chatEndpointRequiresAQuestion() throws Exception {
        mockMvc.perform(get("/chat"))
                .andExpect(status().isBadRequest());
    }

    @Test
    void chatEndpointRejectsBlankQuestions() throws Exception {
        mockMvc.perform(get("/chat").param("q", "   "))
                .andExpect(status().isBadRequest())
                .andExpect(content().string("Query parameter 'q' must not be blank."));
    }
}
