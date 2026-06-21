"use client";

import { useEffect, useRef, useState } from "react";

type Source = {
  id: string;
  title: string;
  source: string;
};

type ChatMessage = {
  role: "user" | "assistant";
  content: string;
  urgency?: string;
  symptoms?: string[];
  sources?: Source[];
};

export default function Home() {
  const [sessionId, setSessionId] = useState(`session_${Date.now()}`);
  const [message, setMessage] = useState("");

  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      role: "assistant",
      content: "Hello 👋 Please describe your symptoms.",
    },
  ]);

  const [loading, setLoading] = useState(false);

  const messagesEndRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({
      behavior: "smooth",
    });
  }, [messages, loading]);

  const getUrgencyStyle = (urgency?: string) => {
    if (urgency === "EMERGENCY") {
      return "bg-red-100 text-red-700 border-red-200";
    }

    if (urgency === "HIGH") {
      return "bg-orange-100 text-orange-700 border-orange-200";
    }

    if (urgency === "MODERATE") {
      return "bg-yellow-100 text-yellow-700 border-yellow-200";
    }

    return "bg-green-100 text-green-700 border-green-200";
  };

  const sendMessage = async () => {
    if (!message.trim()) return;

    const userMessage = message;

    setMessages((prev) => [
      ...prev,
      {
        role: "user",
        content: userMessage,
      },
    ]);

    setMessage("");
    setLoading(true);

    try {
      const response = await fetch("http://127.0.0.1:8000/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          session_id: sessionId,
          message: userMessage,
        }),
      });

      const data = await response.json();

      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: data.reply,
          urgency: data.urgency,
          symptoms: data.symptoms,
          sources: data.sources,
        },
      ]);
    } catch {
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content:
            "Something went wrong. Please make sure the backend is running.",
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const startNewChat = async () => {
    try {
      await fetch(`http://127.0.0.1:8000/chat/${sessionId}`, {
        method: "DELETE",
      });
    } catch {
      // Start a new frontend session even if backend delete fails.
    }

    setSessionId(`session_${Date.now()}`);
    setMessage("");

    setMessages([
      {
        role: "assistant",
        content: "Hello 👋 Please describe your symptoms.",
      },
    ]);
  };

  return (
    <main className="h-screen w-full bg-slate-100 flex items-center justify-center px-4 py-6">
      <div className="w-full max-w-4xl h-full bg-white rounded-3xl shadow-xl flex flex-col overflow-hidden">
        <header className="border-b px-6 py-5 bg-white">
          <div className="flex flex-col items-center">
            <h1 className="text-3xl font-bold text-slate-900 text-center">
              MedGuide AI
            </h1>

            <p className="text-center text-slate-500 mt-1">
              Educational Medical Symptom Assistant
            </p>

            <button
              onClick={startNewChat}
              className="mt-3 text-sm bg-slate-200 hover:bg-slate-300 text-slate-800 px-4 py-2 rounded-xl"
            >
              New Chat
            </button>
          </div>
        </header>

        <section className="flex-1 overflow-y-auto bg-slate-50 p-6 space-y-4">
          {messages.map((chat, index) => (
            <div
              key={index}
              className={`p-4 rounded-2xl max-w-[80%] whitespace-pre-line text-sm leading-relaxed ${
                chat.role === "user"
                  ? "bg-blue-600 text-white ml-auto"
                  : "bg-white text-slate-800 border shadow-sm"
              }`}
            >
              <div>{chat.content}</div>

              {chat.role === "assistant" && chat.urgency && (
                <div className="mt-3">
                  <span
                    className={`inline-block rounded-full border px-3 py-1 text-xs font-semibold ${getUrgencyStyle(
                      chat.urgency
                    )}`}
                  >
                    Urgency: {chat.urgency}
                  </span>
                </div>
              )}

              {chat.role === "assistant" &&
                chat.symptoms &&
                chat.symptoms.length > 0 && (
                  <div className="mt-3 text-xs text-slate-500">
                    <strong>Detected symptoms:</strong>{" "}
                    {chat.symptoms.join(", ")}
                  </div>
                )}

              {chat.role === "assistant" &&
                chat.sources &&
                chat.sources.length > 0 && (
                  <div className="mt-3 text-xs text-slate-500">
                    <strong>Sources:</strong>
                    <ul className="list-disc ml-5 mt-1">
                      {chat.sources.map((source) => (
                        <li key={source.id}>
                          {source.title} — {source.source}
                        </li>
                      ))}
                    </ul>
                  </div>
                )}
            </div>
          ))}

          {loading && (
            <div className="bg-white text-slate-700 border shadow-sm p-4 rounded-2xl w-fit">
              Thinking...
            </div>
          )}

          <div ref={messagesEndRef} />
        </section>

        <footer className="border-t bg-white p-4">
          <div className="flex gap-3">
            <input
              type="text"
              placeholder="Describe your symptoms..."
              value={message}
              onChange={(event) => setMessage(event.target.value)}
              onKeyDown={(event) => {
                if (event.key === "Enter") {
                  sendMessage();
                }
              }}
              className="flex-1 border rounded-2xl px-4 py-3 outline-none focus:ring-2 focus:ring-blue-500 text-black placeholder:text-gray-400 bg-white"
            />

            <button
              onClick={sendMessage}
              disabled={loading}
              className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-2xl disabled:bg-slate-400"
            >
              Send
            </button>
          </div>

          <p className="text-xs text-slate-400 mt-3 text-center">
            This tool is for educational purposes only and is not a substitute
            for professional medical advice.
          </p>
        </footer>
      </div>
    </main>
  );
}