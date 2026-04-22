import type { AiGenerateInput, AiGenerateOutput, AiProvider } from "./aiProvider";

export class GeminiProvider implements AiProvider {
  readonly name = "gemini";

  constructor(private readonly apiKey: string, private readonly model = "gemini-2.0-flash") {}

  async generate(input: AiGenerateInput): Promise<AiGenerateOutput> {
    if (!this.apiKey) {
      throw new Error("GEMINI_API_KEY is required for gemini provider.");
    }

    const prompt = input.messages.map((message) => `${message.role.toUpperCase()}: ${message.content}`).join("\n\n");

    const contents = [{ role: "user", parts: [{ text: prompt }] }];

    const response = await fetch(
      `https://generativelanguage.googleapis.com/v1beta/models/${this.model}:generateContent?key=${this.apiKey}`,
      {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          contents,
          generationConfig: {
            temperature: 0.1,
            maxOutputTokens: input.maxTokens ?? 1200,
          },
        }),
      },
    );

    if (!response.ok) {
      const message = await response.text();
      throw new Error(`Gemini API error: ${response.status} ${message}`);
    }

    const body = (await response.json()) as {
      candidates?: Array<{
        content?: { parts?: Array<{ text?: string }> };
      }>;
    };

    const text = body.candidates?.[0]?.content?.parts?.map((part) => part.text ?? "").join("") ?? "";

    return {
      content: text,
      confidence: 0.74,
      model: this.model,
      traces: [`provider:gemini`, `task:${input.task}`],
    };
  }
}
