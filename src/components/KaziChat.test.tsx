import { describe, it, expect, vi, beforeEach } from "vitest";
import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { KaziChat, sendChatMessage } from "./KaziChat";

function mockFetchOnce(body: unknown, ok = true, status = 200) {
  const fn = vi.fn().mockResolvedValue({
    ok,
    status,
    json: async () => body,
  } as Response);
  (globalThis as unknown as { fetch: typeof fetch }).fetch =
    fn as unknown as typeof fetch;
  return fn;
}

describe("sendChatMessage", () => {
  it("posts user_id + message and returns response", async () => {
    const fetchImpl = vi.fn().mockResolvedValue({
      ok: true,
      status: 200,
      json: async () => ({ response: "hello there" }),
    } as Response);

    const result = await sendChatMessage({
      url: "http://api.test/chat",
      userId: "employee_1",
      message: "hi",
      fetchImpl: fetchImpl as unknown as typeof fetch,
    });

    expect(result).toBe("hello there");
    expect(fetchImpl).toHaveBeenCalledWith(
      "http://api.test/chat",
      expect.objectContaining({
        method: "POST",
        body: JSON.stringify({ user_id: "employee_1", message: "hi" }),
      }),
    );
  });

  it("throws on non-ok response", async () => {
    const fetchImpl = vi.fn().mockResolvedValue({
      ok: false,
      status: 500,
      json: async () => ({}),
    } as Response);

    await expect(
      sendChatMessage({
        url: "x",
        userId: "u",
        message: "m",
        fetchImpl: fetchImpl as unknown as typeof fetch,
      }),
    ).rejects.toThrow(/500/);
  });
});

describe("<KaziChat />", () => {
  beforeEach(() => {
    window.localStorage.clear();
  });

  it("renders welcome message and composer", () => {
    mockFetchOnce({ response: "" });
    render(<KaziChat />);
    expect(screen.getByRole("heading", { name: /kazi/i })).toBeInTheDocument();
    expect(screen.getByLabelText(/message/i)).toBeInTheDocument();
    expect(screen.getByText(/your hr assistant/i)).toBeInTheDocument();
  });

  it("sends a message and renders the assistant reply", async () => {
    mockFetchOnce({ response: "Your leave balance is 12 days." });
    const user = userEvent.setup();
    render(<KaziChat />);

    await user.type(screen.getByLabelText(/message/i), "How many leave days?");
    await user.click(screen.getByRole("button", { name: /send message/i }));

    expect(await screen.findByTestId("msg-user")).toHaveTextContent(
      "How many leave days?",
    );

    await waitFor(() => {
      const replies = screen.getAllByTestId("msg-assistant");
      expect(replies[replies.length - 1]).toHaveTextContent(
        "Your leave balance is 12 days.",
      );
    });
  });

  it("renders an error message when the request fails", async () => {
    (globalThis as unknown as { fetch: typeof fetch }).fetch = vi
      .fn()
      .mockRejectedValue(new Error("Network down")) as unknown as typeof fetch;
    const user = userEvent.setup();
    render(<KaziChat />);

    await user.type(screen.getByLabelText(/message/i), "hello");
    await user.click(screen.getByRole("button", { name: /send message/i }));

    const err = await screen.findByTestId("error");
    expect(err).toHaveTextContent(/network down/i);
  });
});