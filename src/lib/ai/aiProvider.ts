export type AiMessage = {
  role: "system" | "user" | "assistant";
  content: string;
};

export type AiGenerateInput = {
  task: string;
  messages: AiMessage[];
  responseSchemaHint?: string;
  maxTokens?: number;
};

export type AiGenerateOutput = {
  content: string;
  confidence: number;
  model: string;
  traces: string[];
};

export interface AiProvider {
  readonly name: string;
  generate(input: AiGenerateInput): Promise<AiGenerateOutput>;
}
