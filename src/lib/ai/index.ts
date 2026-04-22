import type { AIProviderName } from "../../types";
import { getConfig } from "../../config";
import type { AiProvider } from "./aiProvider";
import { GeminiProvider } from "./geminiProvider";
import { MockProvider } from "./mockProvider";
import { OpenAiProvider } from "./openAiProvider";

export function createAiProvider(providerName?: AIProviderName): AiProvider {
  const config = getConfig();
  const selected = providerName ?? config.aiProvider;

  if (selected === "openai") {
    return new OpenAiProvider(config.openAiApiKey ?? "", config.openAiModel);
  }

  if (selected === "gemini") {
    return new GeminiProvider(config.geminiApiKey ?? "", config.geminiModel);
  }

  return new MockProvider();
}
