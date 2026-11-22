from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Preformatted, PageBreak

out = Path(__file__).with_name('spring-ai-ollam-project-guide.pdf')
styles = getSampleStyleSheet()
navy = colors.HexColor('#17324D')
blue = colors.HexColor('#176B87')
pale = colors.HexColor('#EEF4F7')
muted = colors.HexColor('#52616B')
styles.add(ParagraphStyle(name='Title2', parent=styles['Title'], fontName='Helvetica-Bold', fontSize=24, leading=29, textColor=navy, alignment=0, spaceAfter=6))
styles.add(ParagraphStyle(name='Sub2', parent=styles['Normal'], fontSize=10.5, leading=15, textColor=muted, spaceAfter=12))
styles.add(ParagraphStyle(name='H12', parent=styles['Heading1'], fontName='Helvetica-Bold', fontSize=16, leading=20, textColor=navy, spaceBefore=6, spaceAfter=7))
styles.add(ParagraphStyle(name='H22', parent=styles['Heading2'], fontName='Helvetica-Bold', fontSize=11, leading=14, textColor=blue, spaceBefore=6, spaceAfter=4))
styles.add(ParagraphStyle(name='Body2', parent=styles['BodyText'], fontSize=9, leading=13, spaceAfter=5))
styles.add(ParagraphStyle(name='Small2', parent=styles['BodyText'], fontSize=7.8, leading=10, textColor=muted, spaceAfter=4))
styles.add(ParagraphStyle(name='Bullet2', parent=styles['BodyText'], fontSize=8.8, leading=12, leftIndent=12, firstLineIndent=-8, spaceAfter=3))
styles.add(ParagraphStyle(name='Code2', fontName='Courier', fontSize=7.1, leading=9.3, backColor=pale, borderColor=colors.HexColor('#D6E1E8'), borderWidth=.5, borderPadding=6, leftIndent=3, rightIndent=3, spaceBefore=3, spaceAfter=6))
styles.add(ParagraphStyle(name='TH2', parent=styles['BodyText'], fontName='Helvetica-Bold', fontSize=8, leading=9.5, textColor=colors.white))
styles.add(ParagraphStyle(name='TC2', parent=styles['BodyText'], fontSize=7.8, leading=10.3))

def p(text, style='Body2'):
    return Paragraph(text, styles[style])
def b(text):
    return Paragraph('&bull; ' + text, styles['Bullet2'])
def c(text):
    return Preformatted(text.strip('\n'), styles['Code2'])
def tab(rows, widths):
    data = [[Paragraph(str(x), styles['TH2'] if i == 0 else styles['TC2']) for x in row] for i, row in enumerate(rows)]
    t = Table(data, colWidths=widths, repeatRows=1, hAlign='LEFT')
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),navy),('GRID',(0,0),(-1,-1),.35,colors.HexColor('#CFD9DF')),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),5),('RIGHTPADDING',(0,0),(-1,-1),5),('TOPPADDING',(0,0),(-1,-1),4),('BOTTOMPADDING',(0,0),(-1,-1),4),('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,pale])]))
    return t
def footer(canvas, doc):
    canvas.saveState()
    w, _ = A4
    canvas.setStrokeColor(colors.HexColor('#D5DEE4'))
    canvas.line(18*mm,15*mm,w-18*mm,15*mm)
    canvas.setFont('Helvetica',8)
    canvas.setFillColor(muted)
    canvas.drawString(18*mm,10*mm,'Spring AI with Ollama - Project Guide')
    canvas.drawRightString(w-18*mm,10*mm,f'Page {doc.page}')
    canvas.restoreState()

doc = SimpleDocTemplate(str(out), pagesize=A4, rightMargin=18*mm, leftMargin=18*mm, topMargin=16*mm, bottomMargin=21*mm, title='Spring AI with Ollama - Project Guide')
st = []
st += [p('Spring AI with Ollama','Title2'),p('Project guide | Spring Boot, Java, Spring AI, local LLM','Sub2')]
st += [p('1. Project overview','H12'),p('A Java REST API that receives a question over HTTP and uses Spring AI’s <b>ChatClient</b> to send it to a locally running Ollama model. The controller handles HTTP input, a service handles the chat operation, and the AI response is returned as plain text.'),tab([['Item','Details'],['Framework','Spring Boot 3.5.5'],['Java target','Java 21'],['Spring AI','1.0.1 with Ollama model starter'],['Default Ollama URL','http://localhost:11434'],['Default model','llama3.2'],['API port','8081'],['External API key','Not required; Ollama runs locally or on a configured server']],[43*mm,125*mm]),p('Request flow','H22'),c('HTTP GET /chat?q=... -> ChatController validates q -> ChatService\n-> ChatServiceImpl builds a ChatClient prompt -> Ollama generates an answer\n-> Controller returns plain-text response')]
st += [PageBreak(),p('2. Folder structure','H12'),p('The project follows the standard Spring Initializr Maven convention and contains a single <b>src</b> directory:'),c('spring-ai-ollam/\n|-- pom.xml\n|-- mvnw, mvnw.cmd\n|-- .mvn/wrapper/maven-wrapper.properties\n|-- README.md\n|-- src/\n    |-- main/\n    |   |-- java/com/spring/ollama/\n    |   |   |-- SpringAiOllamApplication.java\n    |   |   |-- controller/ChatController.java\n    |   |   |-- service/ChatService.java\n    |   |   |-- service/ChatServiceImpl.java\n    |   |-- resources/application.properties\n    |-- test/java/com/spring/ollama/\n        |-- SpringAiOllamApplicationTests.java'),tab([['File','Purpose'],['SpringAiOllamApplication.java','Starts the Spring Boot application.'],['controller/ChatController.java','Maps GET /chat, validates q, delegates to service.'],['service/ChatService.java','Declares the chat operation.'],['service/ChatServiceImpl.java','Uses ChatClient to call configured Ollama model.'],['application.properties','Server port, Ollama endpoint/model, temperature.'],['SpringAiOllamApplicationTests.java','Mocked controller tests; does not need Ollama.'],['pom.xml','Maven dependencies, Spring Boot and Spring AI versions.']],[63*mm,105*mm]),p('Maven creates target/ during builds; it is generated build output, not a second source root.','Small2')]
st += [PageBreak(),p('3. Install, configure, and run','H12'),p('Requirements','H22'),b('JDK 21 or newer.'),b('Ollama installed and running locally, or a reachable Ollama server.'),b('A model downloaded to Ollama. The default is llama3.2.'),p('Download the default model','H22'),c('ollama pull llama3.2\nollama list'),p('Start the application from the project directory','H22'),p('Windows PowerShell','H22'),c(r'.\mvnw.cmd spring-boot:run'),p('macOS / Linux / Git Bash','H22'),c('./mvnw spring-boot:run'),p('The server listens on http://localhost:8081. Ollama is normally available at http://localhost:11434.'),p('Optional environment overrides','H22'),p('Windows PowerShell','H22'),c('$env:OLLAMA_BASE_URL = "http://localhost:11434"\n$env:OLLAMA_CHAT_MODEL = "llama3.2"'),p('macOS / Linux / Git Bash','H22'),c('export OLLAMA_BASE_URL="http://localhost:11434"\nexport OLLAMA_CHAT_MODEL="llama3.2"'),p('The model name must exist on the Ollama server. These settings default in application.properties to localhost:11434 and llama3.2.')]
st += [PageBreak(),p('4. API, testing, and interview summary','H12'),p('Ask a question','H22'),c('GET http://localhost:8081/chat?q=Explain%20Java%20records'),p('Example curl request','H22'),c('curl --get "http://localhost:8081/chat" --data-urlencode "q=Explain Java records"'),p('The endpoint returns the response as plain text. Missing or blank q returns HTTP 400.'),p('Run tests','H22'),c(r'.\mvnw.cmd clean test    # Windows PowerShell'+'\n'+'./mvnw clean test        # macOS / Linux / Git Bash'),p('The test suite mocks ChatService and covers a successful request, missing q, and blank q. Latest clean run: <b>3 tests, 0 failures</b>. The tests do not make a real Ollama request.'),p('What it demonstrates','H22'),b('Spring dependency injection and separation of web/controller and service layers.'),b('Spring AI ChatClient prompt construction and synchronous local-model invocation.'),b('Externalized local endpoint and model configuration.'),b('Controller testing without network calls or an external model server.'),p('Limitations','H22'),b('No chat history, streaming, authentication, rate limiting, frontend, or production-grade provider failure handling.'),b('A real answer requires Ollama to be running and the configured model to be available.'),p('Interview explanation','H22'),p('“This project is a Spring Boot REST API that demonstrates connecting to a local language model using Spring AI and Ollama. The controller validates a question and delegates it to a service, which builds a prompt through ChatClient and returns the model response. I made the Ollama URL and model configurable and wrote controller tests with a mocked service, so tests do not depend on Ollama being online.”'),p('Attribution: Based on LearnCodeWithDurgesh/spring-ai-yt-series/spring-ai-ollam. Review the original repository’s licensing and attribution terms before redistribution.','Small2'),p('Source: https://github.com/LearnCodeWithDurgesh/spring-ai-yt-series/tree/main/spring-ai-ollam','Small2')]
doc.build(st,onFirstPage=footer,onLaterPages=footer)
print(out.resolve())
print(out.stat().st_size,'bytes')
