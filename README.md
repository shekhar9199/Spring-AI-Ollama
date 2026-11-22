# Spring AI with Ollama

A small Spring Boot REST API that sends a question to a locally running Ollama model using Spring AI's `ChatClient`. It demonstrates the basic request flow from an HTTP controller to a service and then to a local language model.

## Features

- Synchronous responses through Spring AI `ChatClient`.
- Local model calls via Ollama; no cloud API key is required.
- Configurable Ollama server URL and model name.
- Blank-question validation.
- Controller tests that use a mocked service and do not require Ollama to be running.
- Maven Wrapper included.

## Technology

| Technology | Version / configuration |
| --- | --- |
| Java | 21 (Maven compiler target) |
| Spring Boot | 3.5.5 |
| Spring AI | 1.0.1 |
| Build | Maven Wrapper |
| Model server | Ollama at `http://localhost:11434` by default |
| Default model | `llama3.2` |
| HTTP port | `8081` |

## Project structure

The project uses the conventional Spring Initializr Maven layout with **one `src` directory**:

```text
spring-ai-ollam/
├── .mvn/wrapper/                    # Maven Wrapper configuration
├── src/
│   ├── main/
│   │   ├── java/com/spring/ollama/
│   │   │   ├── SpringAiOllamApplication.java # Spring Boot entry point
│   │   │   ├── controller/ChatController.java # HTTP route and validation
│   │   │   └── service/
│   │   │       ├── ChatService.java           # Service contract
│   │   │       └── ChatServiceImpl.java       # ChatClient integration
│   │   └── resources/application.properties   # Ollama URL, model, port
│   └── test/java/com/spring/ollama/
│       └── SpringAiOllamApplicationTests.java  # Controller tests
├── mvnw
├── mvnw.cmd
├── pom.xml
└── README.md
```

Maven creates `target/` during builds. It is generated output and is not another source directory.

## Requirements

- JDK 21 or newer.
- [Ollama](https://ollama.com/download) installed and running locally, or a reachable Ollama server.
- A model downloaded in Ollama. The default is `llama3.2`.

The Java tests do not require Ollama; only running the application and making a real chat request does.

## Set up Ollama

Start the Ollama application/service, then download the configured model:

```bash
ollama pull llama3.2
```

You can check that Ollama is available with:

```bash
ollama list
```

Ollama normally exposes its local API at `http://localhost:11434`. If you configure another model or server, set the environment variables below before starting Spring Boot.

## Run the application

From this project directory:

### Windows PowerShell

```powershell
.\mvnw.cmd spring-boot:run
```

### macOS / Linux / Git Bash

```bash
./mvnw spring-boot:run
```

The server starts at `http://localhost:8081`.

### Optional configuration overrides

Defaults are set in `src/main/resources/application.properties`. Override them with environment variables if needed:

**Windows PowerShell:**

```powershell
$env:OLLAMA_BASE_URL = "http://localhost:11434"
$env:OLLAMA_CHAT_MODEL = "llama3.2"
```

**macOS / Linux / Git Bash:**

```bash
export OLLAMA_BASE_URL="http://localhost:11434"
export OLLAMA_CHAT_MODEL="llama3.2"
```

The configured model must already be available to the Ollama server. No OpenAI key is used by this project.

## API

### Ask a question

```http
GET /chat?q=Explain%20Java%20records
```

Example with `curl`:

```bash
curl --get "http://localhost:8081/chat" \
  --data-urlencode "q=Explain Java records"
```

The endpoint returns the model's answer as plain text. A missing or blank `q` parameter returns `400 Bad Request`.

## How a request works

```text
HTTP request
    -> ChatController validates the query parameter
    -> ChatService defines the chat operation
    -> ChatServiceImpl builds a ChatClient prompt
    -> Spring AI sends it to the configured Ollama model
    -> The model response is returned as plain text
```

Spring AI auto-configures `ChatClient.Builder` from the `spring.ai.ollama.*` settings. The controller depends on the `ChatService` interface, keeping HTTP handling separate from the AI integration.

## Run tests

Tests mock the chat service, so they run without an Ollama installation or model download.

### Windows PowerShell

```powershell
.\mvnw.cmd clean test
```

### macOS / Linux / Git Bash

```bash
./mvnw clean test
```

The test suite covers a successful request, a missing question parameter, and a blank question. It does not send a real prompt to Ollama.

## Troubleshooting

- **Connection refused:** Make sure Ollama is installed and its service is running; confirm `OLLAMA_BASE_URL` is reachable.
- **Model not found:** Run `ollama pull llama3.2`, or set `OLLAMA_CHAT_MODEL` to a model already downloaded on the server.
- **Tests fail because Ollama is offline:** The tests should not require Ollama. Run `clean test` and check that only the controller tests are running; do not use a full Spring application context test for this external integration.

## Limitations

This is a compact learning example, not a production-ready chatbot. It does not currently implement conversation history, streaming, authentication, rate limiting, a frontend, or specialized handling for all model-server failures.
