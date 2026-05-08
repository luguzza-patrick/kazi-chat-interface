import { useEffect, useRef, useState, type FormEvent } from "react";
import { Send, Settings, Loader2, Sparkles, AlertCircle, LogOut } from "lucide-react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import { Login } from "./Login";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@/components/ui/popover";
import { Label } from "@/components/ui/label";
import { Badge } from "@/components/ui/badge";
import { cn } from "@/lib/utils";

export type ChatRole = "user" | "assistant";

export interface ChatMessage {
  id: string;
  role: ChatRole;
  content: string;
}

export interface KaziUser {
  id: string;
  name: string;
  role: "Employee" | "HR" | "CEO";
}

export const STORAGE_USER_KEY = "kazi:user";

const DEFAULT_BACKEND_URL =
  (import.meta.env.VITE_KAZI_BACKEND_URL as string | undefined) ??
  "/api/v1/chat";

const STORAGE_KEY = "kazi:backend-url";

export interface SendChatArgs {
  url: string;
  userId: string;
  message: string;
  fetchImpl?: typeof fetch;
}

export async function sendChatMessage({
  url,
  userId,
  message,
  fetchImpl = fetch,
}: SendChatArgs): Promise<string> {
  const res = await fetchImpl(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ user_id: userId, message }),
  });
  if (!res.ok) {
    throw new Error(`Request failed (${res.status})`);
  }
  const data = (await res.json()) as { response?: string };
  if (typeof data.response !== "string") {
    throw new Error("Malformed response from server");
  }
  return data.response;
}

function roleBadgeClass(role: KaziUser["role"]) {
  switch (role) {
    case "CEO":
      return "border-transparent bg-[oklch(0.45_0.12_265)] text-white";
    case "HR":
      return "border-transparent bg-[oklch(0.55_0.12_220)] text-white";
    default:
      return "border-transparent bg-secondary text-secondary-foreground";
  }
}

export function KaziChat() {
  const [user, setUser] = useState<any>(null);
  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      id: "welcome",
      role: "assistant",
      content:
        "Hi, I'm Kazi — your HR assistant. Ask me about policies, leave, payroll, or anything HR-related.",
    },
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [backendUrl, setBackendUrl] = useState<string>(DEFAULT_BACKEND_URL);
  const scrollRef = useRef<HTMLDivElement>(null);



  useEffect(() => {
    if (typeof window === "undefined") return;
    const savedUrl = window.localStorage.getItem(STORAGE_KEY);
    if (savedUrl) setBackendUrl(savedUrl);
    
    const savedUser = window.localStorage.getItem(STORAGE_USER_KEY);
    if (savedUser) setUser(JSON.parse(savedUser));
  }, []);

  useEffect(() => {
    const el = scrollRef.current;
    if (!el || typeof el.scrollTo !== "function") return;
    el.scrollTo({ top: el.scrollHeight, behavior: "smooth" });
  }, [messages, loading]);

  const handleLogin = (authenticatedUser: any) => {
    setUser(authenticatedUser);
    if (typeof window !== "undefined") {
      window.localStorage.setItem(STORAGE_USER_KEY, JSON.stringify(authenticatedUser));
    }
  };

  const handleLogout = () => {
    setUser(null);
    if (typeof window !== "undefined") {
      window.localStorage.removeItem(STORAGE_USER_KEY);
    }
  };

  const persistUrl = (url: string) => {
    setBackendUrl(url);
    if (typeof window !== "undefined") {
      window.localStorage.setItem(STORAGE_KEY, url);
    }
  };

  async function handleSubmit(e: FormEvent) {
    e.preventDefault();
    const text = input.trim();
    if (!text || loading) return;

    const userMsg: ChatMessage = {
      id: `${Date.now()}-u`,
      role: "user",
      content: text,
    };
    setMessages((m) => [...m, userMsg]);
    setInput("");
    setLoading(true);
    setError(null);

    try {
      const response = await sendChatMessage({
        url: backendUrl,
        userId: user.id.toString(),
        message: text,
      });
      setMessages((m) => [
        ...m,
        { id: `${Date.now()}-a`, role: "assistant", content: response },
      ]);
    } catch (err) {
      const msg =
        err instanceof Error ? err.message : "Something went wrong";
      setError(msg);
    } finally {
      setLoading(false);
    }
  }

  if (!user) {
    return <Login onLogin={handleLogin} />;
  }

  return (
    <div className="mx-auto flex h-[100dvh] w-full max-w-3xl flex-col bg-background">
      {/* Header */}
      <header className="flex items-center justify-between gap-3 border-b border-border bg-card/80 px-5 py-3 backdrop-blur">
        <div className="flex items-center gap-3">
          <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-primary text-primary-foreground shadow-sm">
            <Sparkles className="h-4 w-4" />
          </div>
          <div className="leading-tight">
            <h1 className="text-sm font-semibold tracking-tight">Kazi</h1>
            <p className="text-xs text-muted-foreground">AI HR assistant</p>
          </div>
        </div>

        <div className="flex items-center gap-2">
          <Button
            variant="ghost"
            size="sm"
            onClick={handleLogout}
            className="text-muted-foreground hover:text-foreground gap-2 h-9"
          >
            <LogOut className="h-4 w-4" />
            <span className="hidden sm:inline">Sign Out</span>
          </Button>

          <Popover>
            <PopoverTrigger asChild>
              <Button
                variant="outline"
                size="icon"
                className="h-9 w-9"
                aria-label="Settings"
              >
                <Settings className="h-4 w-4" />
              </Button>
            </PopoverTrigger>
            <PopoverContent align="end" className="w-80">
              <div className="space-y-3">
                <div>
                  <h3 className="text-sm font-semibold">Backend settings</h3>
                  <p className="text-xs text-muted-foreground">
                    Endpoint Kazi will POST messages to.
                  </p>
                </div>
                <div className="space-y-1.5">
                  <Label htmlFor="backend-url" className="text-xs">
                    Backend URL
                  </Label>
                  <Input
                    id="backend-url"
                    value={backendUrl}
                    onChange={(e) => persistUrl(e.target.value)}
                    placeholder="http://localhost:8000/chat"
                  />
                </div>
              </div>
            </PopoverContent>
          </Popover>
        </div>
      </header>

      {/* Role bar */}
      <div className="flex items-center justify-between border-b border-border bg-muted/40 px-5 py-2">
        <div className="flex items-center gap-2 text-xs text-muted-foreground">
          <span>Signed in as</span>
          <span className="font-medium text-foreground">{user.name}</span>
          <Badge className={roleBadgeClass(user.role.toUpperCase() as any)}>
            {user.role}
          </Badge>
        </div>
      </div>

      {/* Messages */}
      <div
        ref={scrollRef}
        data-testid="chat-scroll"
        className="flex-1 overflow-y-auto px-5 py-6"
      >
        <ul className="space-y-4">
          {messages.map((m) => (
            <li
              key={m.id}
              data-testid={`msg-${m.role}`}
              className={cn(
                "flex w-full",
                m.role === "user" ? "justify-end" : "justify-start",
              )}
            >
              <div
                className={cn(
                  "max-w-[80%] rounded-2xl px-4 py-2.5 text-sm leading-relaxed shadow-sm",
                  m.role === "user"
                    ? "rounded-br-sm bg-primary text-primary-foreground"
                    : "rounded-bl-sm bg-card text-card-foreground border border-border",
                )}
              >
                <div className="markdown-content">
                  <ReactMarkdown remarkPlugins={[remarkGfm]}>
                    {m.content}
                  </ReactMarkdown>
                </div>
              </div>
            </li>
          ))}

          {loading && (
            <li
              data-testid="loading"
              className="flex justify-start"
            >
              <div className="flex items-center gap-2 rounded-2xl rounded-bl-sm border border-border bg-card px-4 py-2.5 text-sm text-muted-foreground">
                <Loader2 className="h-3.5 w-3.5 animate-spin" />
                Kazi is thinking…
              </div>
            </li>
          )}

          {error && (
            <li data-testid="error" className="flex justify-start">
              <div className="flex items-start gap-2 rounded-xl border border-destructive/30 bg-destructive/10 px-4 py-2.5 text-sm text-destructive">
                <AlertCircle className="mt-0.5 h-4 w-4 shrink-0" />
                <span>{error}</span>
              </div>
            </li>
          )}
        </ul>
      </div>

      {/* Composer */}
      <form
        onSubmit={handleSubmit}
        className="border-t border-border bg-card/80 px-5 py-3 backdrop-blur"
      >
        <div className="flex items-end gap-2">
          <Input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder={`Message Kazi as ${user.role}…`}
            aria-label="Message"
            disabled={loading}
            className="h-11"
          />
          <Button
            type="submit"
            size="icon"
            className="h-11 w-11 shrink-0"
            disabled={loading || !input.trim()}
            aria-label="Send message"
          >
            {loading ? (
              <Loader2 className="h-4 w-4 animate-spin" />
            ) : (
              <Send className="h-4 w-4" />
            )}
          </Button>
        </div>
        <p className="mt-2 text-[11px] text-muted-foreground">
          Kazi may make mistakes. Verify important HR information.
        </p>
      </form>
    </div>
  );
}
