package com.spring.ollama;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

/** Starts the Spring Boot application and its embedded HTTP server. */
@SpringBootApplication
public class SpringAiOllamApplication {

	public static void main(String[] args) {
		SpringApplication.run(SpringAiOllamApplication.class, args);
	}

}
