import type { AiGenerateInput, AiGenerateOutput, AiProvider } from "./aiProvider";

export class OpenAiProvider implements AiProvider {
  readonly name = "openai";

  constructor(private readonly apiKey: string, private readonly model: string) {}

  async generate(input: AiGenerateInput): Promise<AiGenerateOutput> {
    if (!this.apiKey) {
      throw new Error("OPENAI_API_KEY is required for openai provider.");
    }

    const response = await fetch("https://api.openai.com/v1/responses", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${this.apiKey}`,
      },
      body: JSON.stringify({
        model: this.model,
        input: input.messages.map((message) => ({
          role: message.role,
          content: [{ type: "input_text", text: message.content }],
        })),
        temperature: 0.1,
        max_output_tokens: input.maxTokens ?? 1200,
      }),
    });

    if (!response.ok) {
      const details = await response.text();
      throw new Error(`OpenAI API error ${response.status}: ${details}`);
    }

    const body = (await response.json()) as {
      output_text?: string;
      usage?: {
        input_tokens?: number;
        output_tokens?: number;
      };
    };

    return {
      content: body.output_text ?? "",
      confidence: 0.75,
      model: this.model,
      traces: [
        `provider:openai`,
        `task:${input.task}`,
        `inputTokens:${body.usage?.input_tokens ?? 0}`,
        `outputTokens:${body.usage?.output_tokens ?? 0}`,
      ],
    };
  }
}
