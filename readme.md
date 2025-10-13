Building a Fintech Support Chatbot with OpenAI Agent Builder, ChatKit, and FAISS

Introduction

Financial technology companies are increasingly adopting AI chatbots to assist customers with investment platform queries and support FAQs. Using OpenAI’s new AgentKit tools (Agent Builder and ChatKit) makes it much easier to create such an AI assistant, without weeks of custom orchestration or UI coding ￼ ￼. In this solution, we outline a customer support chatbot for a fintech (investment platform) that can answer user questions by pulling information from company policies, internal procedures, and FAQs stored in a vector database, and by using external tools like web search and code execution when needed. Notably, Klarna has already built a similar AI support agent that now handles two-thirds of customer tickets ￼, demonstrating the practical value of this approach.

Our chatbot will use a Retrieval-Augmented Generation (RAG) strategy combined with agent tools. In simple terms, the agent will retrieve relevant knowledge from a vector store (using FAISS) and generate answers with GPT-4 based on that context ￼. Additionally, the agent can invoke tools (like a web search API or a code interpreter) for information beyond the internal knowledge base or for performing calculations. We will also leverage OpenAI’s ChatKit widget to embed a ready-made chat UI on a web page, enabling an interactive experience with minimal frontend work ￼. The end result is a customer support chatbot that can answer policy questions, guide users through procedures, fetch up-to-date financial info via web search, and even perform on-the-fly computations – all without requiring user logins or session tracking on our side.

Architecture of the AI Support Chatbot

Agent Builder Workflow and Tools

OpenAI’s Agent Builder provides a visual or code-based way to design the chatbot’s reasoning workflow. We can define a custom workflow (or “agent”) with specific instructions and attach tools (functions) for the agent to use ￼. The core tools in our fintech support scenario include:
	•	Knowledge Base Search (FAISS vector store) – a function that searches the company’s internal docs for relevant information. This tool uses vector embeddings to find semantic matches in policy documents or FAQs.
	•	Web Search Tool – a function that performs a web search (e.g. via an API) to retrieve external information, like current stock prices or news, if the user’s query is not answered by internal data.
	•	Code Interpreter Tool – a function that executes code (e.g. Python) in a sandboxed environment, allowing the agent to perform calculations or data analysis. This is akin to ChatGPT’s Code Interpreter, enabling tasks like computing investment returns, parsing a CSV of transactions, or generating a quick chart if needed.

By integrating these tools, the agent can take actions step-by-step to solve the user’s query ￼. For example, the agent might first call the knowledge-base search; if that doesn’t yield an answer, it could invoke the web search for up-to-date info; or if the user provided a data file (ChatKit supports file uploads ￼), the agent could run code to analyze it. This flexible “agentic” workflow means the chatbot isn’t limited to pre-written answers – it can dynamically gather information and compute results as needed. Notably, ChatKit’s interface will even display the agent’s tool usage and chain-of-thought (for debugging or transparency) if configured ￼.

Internal Knowledge Base with FAISS

At the heart of the chatbot is the company’s internal knowledge base – documents like support FAQs, product guides, compliance policies, etc. We use OpenAI embeddings to convert each document (or paragraph) into a numerical vector, and store these vectors in a FAISS index for similarity search ￼. FAISS (Facebook AI Similarity Search) is an efficient vector database that can quickly find which stored text pieces are semantically closest to a new query vector ￼.

When a user asks a question, the agent’s first step is to retrieve relevant content from this vector store. The process is:
	1.	Embed the query: The user’s question is turned into an embedding vector using an OpenAI model (e.g. text-embedding-ada or similar).
	2.	Vector search: Using the FAISS index, find the top N documents or snippets whose embeddings are closest to the query vector (meaning they likely contain information related to the question). FAISS returns, say, the top 3–5 matches in milliseconds ￼.
	3.	Use retrieved context: The agent then has those relevant snippets as context. It will incorporate them into its prompt or reasoning to generate an accurate answer. Essentially, we augment the model’s input with company-specific knowledge so it can answer in a company-approved way.

This Retrieval-Augmented Generation approach ensures the chatbot’s answers are grounded in the latest company information (without needing the model to have seen these in training). It also means the bot’s knowledge can be easily updated – update the documents and re-index, and the bot is up-to-date. In our agent, the search_knowledge_base tool encapsulates this logic. For example, in code it might look like:

def search_knowledge_base(query: str) -> str:
    """Search internal knowledge base via FAISS and return relevant text."""
    # (Pseudo-code for embedding the query and searching FAISS index)
    embedding = openai.Embedding.create(input=query, model="text-embedding-ada-002")
    top_docs = faiss_index.search(embedding, k=5)  # find top 5 similar docs
    results_text = "\n".join([doc.text for doc in top_docs])
    return results_text  # return concatenated relevant snippets

We register this function as a tool in the Agent Builder so the agent can call search_knowledge_base() when needed ￼. (In Agent Builder’s visual interface, this might be a node that takes the user query and outputs retrieved info.) The agent’s instructions would include guidance like “First, search the knowledge base for relevant information, then draft an answer using that”.

Web Search Integration

For questions that go beyond the internal knowledge (for example, “What’s the current price of Bitcoin?” or “What are today’s market trends?”), the chatbot can fall back to an external web search tool. We can implement a custom function search_web(query: str) that calls an external API (such as a search engine API or a financial data API) and returns the results. This tool would also be added to the agent’s tool list. The agent’s logic might be: if the knowledge base search doesn’t find what it needs (or if the query explicitly asks for live data), then use search_web.

Using a browser/search tool ensures the AI assistant can provide up-to-date information, which is crucial in finance (markets move quickly!). For example, if a user asks, “What’s the latest NASDAQ index level?”, the agent might call search_web, get the latest figure, and then respond with that data. From the user’s perspective, it feels seamless – the bot just answers the question – but under the hood the agent intelligently chose to use an external resource. (This approach is similar to how ChatGPT with browsing works, but here you control the search API and parsing.)

We will have to implement search_web carefully to parse results into a concise answer. In an Agent Builder workflow, this could be a node that takes the query and returns a snippet of text (e.g. “NASDAQ is at 14,500 as of today”). The Agent Connector Registry can help manage API keys or endpoints for such tools if needed ￼ ￼, or we simply call the API directly in our tool function.

Code Interpreter for Calculations

The third tool, a code interpreter, brings powerful analytical capabilities. In a support context, this might be used less frequently, but it’s very useful for certain requests. For instance:
	•	If a customer asks, “Can you calculate the compound interest on $5,000 over 2 years at 5% APR?”, the agent can use a code tool to do the math and return an accurate result instead of relying on the language model’s arithmetic (which might be error-prone).
	•	If a user uploads a file (e.g. a CSV of their transactions or a PDF statement) and asks questions about it, the agent could run Python code to parse the file and generate an answer (ChatKit natively supports file uploads and attachments in the chat UI ￼, which the agent can then access as input).

To enable this, we add a tool like run_python(code: str) or more constrained versions (e.g. a calculate function that takes parameters). In practice, implementing a full sandboxed code interpreter requires care – one might use a restricted execution environment or an API like OpenAI’s own Code Interpreter if it were exposed. In our architecture, we assume we have a safe way to execute Python code snippets. The agent can then do things like generate a table, perform data analysis, or produce a quick chart if needed, and send the result back to the user. This greatly increases the insightfulness of the support bot, allowing it to not just recall information but also analyze and compute on the fly.

Agent Workflow Logic

With all these tools, the workflow in Agent Builder might look like this:
	1.	User query -> (Agent input node)
	2.	Knowledge Base Search -> Agent calls search_knowledge_base(query).
	•	If results are found (the tool returns relevant text), proceed. If no results or the query is out-of-domain, the agent can decide to use search_web next.
	3.	Optional Web Search -> If needed, call search_web(query) and get external info.
	4.	Optional Code Tool -> If the query involves calculation or file data, call run_python (or a similar tool) with the appropriate code or parameters.
	5.	Compose Answer -> Using the information gathered from the tools (internal docs context, web data, and/or calculation results), the agent formulates a final answer. This happens in the agent’s output node, leveraging GPT-4 to generate a friendly, precise response that cites policy if relevant.
	6.	Output to user -> The answer is streamed back to the ChatKit UI, where the user sees the chatbot’s answer appear.

Throughout this process, the agent can loop or make multiple tool calls if the first attempt didn’t yield a satisfactory answer. We do, however, apply some guardrails – for example, we instruct the agent not to keep searching forever. If after a few attempts the answer is still not found, the agent should either provide a generic fallback or advise contacting human support. (Agent Builder lets us set such guardrails; e.g., “After 3 failed search attempts, stop and escalate” ￼.) This prevents infinite loops or irrelevant digressions.

Importantly, because we do not track user sessions or require login, each chat session is independent. The agent treats each new conversation without persistent memory of previous sessions (aside from the conversation history within the session itself). This is fine for a support bot answering general questions. If a user asks a follow-up in the same chat, the history is maintained by ChatKit’s session, so the agent will remember what was already discussed in that conversation. But once the page is refreshed or a new chat started, it’s a clean slate. (ChatKit and OpenAI’s Conversations API manage the chat history on the backend for the duration of a session, so we don’t have to store it ourselves ￼.)

Implementation Outline

Building this system involves a few key components. Below is a high-level outline with some code snippets to illustrate the approach:
	1.	Prepare the Knowledge Base and Vector Store (FAISS): Gather company support documents, policies, and FAQs. Split them into reasonably sized chunks (e.g. paragraphs), generate embeddings for each chunk using OpenAI’s embedding API, and index them in a FAISS vector database. This step can be done offline or at startup. For example:

import faiss, numpy as np
from openai import Embedding

# Assume docs_chunks is a list of text segments from internal docs
embeddings = []
for text in docs_chunks:
    emb = Embedding.create(input=[text], model="text-embedding-ada-002")["data"][0]["embedding"]
    embeddings.append(emb)
embeddings = np.array(embeddings, dtype="float32")
index = faiss.IndexFlatL2(len(embeddings[0]))  # L2 or cosine similarity index
index.add(embeddings)
# (Save index to disk if needed for persistence)

This creates a FAISS index of our knowledge base, enabling fast similarity search ￼. We also keep a mapping of index positions to the original document text, so we can retrieve the actual content when we get search hits.

	2.	Define Agent Tools (Functions): Using OpenAI’s Agents SDK or the Agent Builder UI, define the tools the agent can use, and how they work. For example, in code form (for clarity):

from openai import ChatCompletion

def search_kb_tool(query: str) -> str:
    # Embed the query and search FAISS for top result
    q_emb = Embedding.create(input=[query], model="text-embedding-ada-002")["data"][0]["embedding"]
    D, I = index.search(np.array([q_emb], dtype="float32"), k=3)
    # Retrieve the top 3 matched texts
    top_texts = [docs_chunks[i] for i in I[0]]
    return "\n".join(top_texts) if top_texts else "No relevant info found."

def search_web_tool(query: str) -> str:
    # Call external API (pseudo-code)
    results = call_search_api(query)
    summary = parse_and_summarize(results)
    return summary[:1000]  # return a trimmed summary to stay within token limits

def run_python_tool(code: str) -> str:
    # Execute Python code in a safe environment (pseudo)
    try:
        output = safe_execute_code(code)
        return str(output)
    except Exception as e:
        return f"Error: {e}"

In the Agent Builder (visual or via SDK), we register these as tools the agent can invoke ￼. Each tool should have a name and description; for instance, search_kb_tool might be described as “Search the internal knowledge base for relevant information.” During a conversation, the agent can decide to call these functions. (Under the hood, OpenAI’s function-calling mechanism will pass the query string to our function and get back the result for the model to use.)

	3.	Design the Agent’s Workflow/Prompt: We give the agent a role description and strategy. For example: “You are an AI customer support assistant for FinTechCo. You have access to the company knowledge base via the search_kb_tool. Use it to answer questions about policies, procedures, accounts, etc. If the question is about external market data or something not in the docs, use search_web_tool. You also have a run_python_tool for calculations. Always provide clear, helpful answers. If you can’t find an answer, apologize and suggest contacting support.” We also include any relevant system instructions or persona (e.g. a friendly but professional tone). This becomes the basis for the agent’s behavior, combined with the tool usage logic above. The Agent Builder interface allows creating such a workflow with nodes: an input node, tool nodes (which can be conditional), and an output node for the final answer. We might start from a template (OpenAI provides a “Customer Support” agent template) and then customize it ￼. Using a template can save time and enforce best practices (e.g., avoiding infinite loops ￼).
	4.	FastAPI Backend Setup: We will create a simple FastAPI server to serve two purposes: (a) provide an API endpoint for ChatKit to obtain a session token (client secret) to connect to our agent, and (b) serve the static HTML/JS for the chat interface. For simplicity, we won’t implement user auth; everyone gets a new session. Here’s a minimal FastAPI example:

from fastapi import FastAPI
import openai

app = FastAPI()
openai.api_key = "sk-..."  # Your OpenAI API key (project-specific)

WORKFLOW_ID = "wf_12345abcde"  # your published Agent workflow ID from OpenAI [oai_citation:22‡medium.com](https://medium.com/@mcraddock/getting-started-with-openai-chatkit-the-one-setup-step-you-cant-skip-7d4c0110404a#:~:text=OPENAI_API_KEY%3Dsk)

@app.get("/chatkit/session")
async def create_session():
    # Create a new chat session for the agent workflow
    response = openai.ChatCompletion.create(workflow_id=WORKFLOW_ID)  # Pseudo API call
    # In practice, use the appropriate method to create a ChatKit session and get client_secret
    client_secret = response["client_secret"]
    return {"client_secret": client_secret}

In the above, workflow_id (starting with “wf_”) refers to the agent you built and published in the OpenAI platform ￼. When the front-end requests /chatkit/session, the backend calls OpenAI to initiate a new session for that agent and returns a client_secret token. (The actual OpenAI Python SDK call may differ – for example, there might be a dedicated openai.chatkit.sessions.create() function – but the idea is the same: the server obtains a session token using your API key and agent ID ￼.) This token is what allows the ChatKit widget on the client side to securely connect to your agent without exposing your API key. We do not store any session info in a database – the token itself identifies the session to OpenAI’s servers, which maintain the conversation state.

	5.	Front-End Integration with ChatKit Widget: Finally, we create a simple HTML page that includes OpenAI’s ChatKit widget script. This widget will present the chat interface to the user and communicate with the OpenAI-hosted backend (our agent) using the session token from our FastAPI service. An example embed code could look like:

<!DOCTYPE html>
<html>
<head><title>FinTechCo Support Chat</title></head>
<body>
  <!-- Container for the chat widget -->
  <div id="chat-container"></div>

  <!-- Include OpenAI ChatKit script -->
  <script src="https://cdn.openai.com/chatkit/v1/chatkit.js" async></script>
  <script>
    // Initialize ChatKit after the custom element is defined
    (async () => {
      await customElements.whenDefined('openai-chatkit');
      const chatEl = document.getElementById('chat-container');

      // Fetch a new client token from our FastAPI backend
      const res = await fetch('/chatkit/session');
      const data = await res.json();
      if (!data.client_secret) {
        console.error("Failed to get ChatKit client token");
        return;
      }

      // Mount the ChatKit widget
      chatEl.setAttribute('agent-id', 'wf_12345abcde');      // Agent workflow ID
      chatEl.setAttribute('client-secret', data.client_secret);  // Session token for auth
      chatEl.setAttribute('user-id', '');  // No user auth, so this can be blank or omitted
      // (We could also use ChatKit.init({...}) instead of setting attributes directly)
    })();
  </script>
</body>
</html>

In this snippet, the <openai-chatkit> web component (referenced by chatEl) is configured with our agent’s ID and the obtained client_secret for the session. We leave user-id blank since we are not tracking individual users (ChatKit can use a userId for analytics or personalization, but here every session is anonymous). The ChatKit widget automatically handles connecting to OpenAI, streaming messages, and displaying the chat UI. It supports customization of theme and other options as well ￼ ￼, but we can start with the defaults for simplicity.
Important: We must ensure our domain (or localhost for testing) is added to the OpenAI domain allowlist for ChatKit, otherwise the widget will refuse to connect ￼. This security feature prevents others from hijacking your agent. In development, we’d allowlist http://localhost (with port if needed), and in production the real domain (e.g. support.fintechco.com) ￼. Once allowlisted, the widget’s network calls (to OpenAI’s servers for session creation and message exchange) will succeed, and our chatbot will be live on the page ￼.

With those steps, the AI support chatbot is operational. A user visits the support page, sees a chat box, and can ask questions like “How do I withdraw funds from my investment account?”. The chatbot (Agent) will retrieve the relevant policy from FAISS (e.g. “Withdrawal procedure”) and answer with the steps, perhaps also linking to the full policy. If asked “What’s the interest rate on the savings account?”, it will find that info from the knowledge base. If asked something like “What’s the latest price of Bitcoin?”, it might use the web search tool to fetch the current price before responding. For a question like “Can you analyze my investment performance?”, the user could upload a CSV of their portfolio history; the agent’s code tool could crunch the numbers and give a summary. All of this happens within a single, user-friendly chat interface.

Conclusion

By combining OpenAI’s Agent Builder (for workflow logic and tool use) with a vector database (FAISS) and the ChatKit UI toolkit, we can create a powerful fintech customer support chatbot with relatively little code. The agent-centric approach ensures the AI can both retrieve factual information from internal data and perform actions (like web queries or calculations) to enhance its answers. This leads to more accurate and context-aware responses, addressing customer inquiries in real-time. The entire pipeline – from query to answer – is automated, enabling 24/7 support availability. And thanks to ChatKit’s plug-and-play widget, deploying the chatbot on a website or app is straightforward (just a few lines of HTML/JS, after proper setup).

In summary, the practical workflow we’ve outlined uses retrieval augmented generation for domain-specific knowledge, augmented with tool usage for external info and computations, all orchestrated by OpenAI’s agent framework. This design can significantly improve customer experience on an investment platform, answering users’ questions with the combined knowledge of company policies and the latest data. With no need for users to log in and no manual session handling required, the solution is both user-friendly and developer-friendly. By following these steps and best practices, a fintech company can stand up an insightful AI support agent that delivers quick, accurate answers – from simple FAQs to complex financial queries – at scale.

Sources:
	•	OpenAI DevDay announcements on AgentKit and ChatKit ￼ ￼
	•	Mark Craddock, “Getting Started with OpenAI ChatKit: The One Setup Step You Can’t Skip” ￼ ￼
	•	SmartScope Blog – AgentKit Implementation Guide (ChatKit integration snippet and agent workflow tips) ￼ ￼ ￼
	•	Medium article on Agentic RAG (Jay Kim, Apr 2025) ￼
	•	Medium article on AI Sales Assistant with RAG & FAISS (K. Singh, Apr 2025) ￼ ￼
	•	OpenAI “Introducing AgentKit” news (Oct 2025) – example use cases like Klarna support agent ￼.