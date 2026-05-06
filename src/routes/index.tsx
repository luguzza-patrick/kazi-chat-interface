import { createFileRoute } from "@tanstack/react-router";
import { KaziChat } from "@/components/KaziChat";

export const Route = createFileRoute("/")({
  component: Index,
  head: () => ({
    meta: [
      { title: "Kazi — AI HR Assistant" },
      {
        name: "description",
        content:
          "Chat with Kazi, your AI HR assistant for policies, payroll, leave and more.",
      },
    ],
  }),
});

function Index() {
  return <KaziChat />;
}
