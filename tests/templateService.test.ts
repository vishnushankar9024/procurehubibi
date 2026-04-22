import { describe, expect, it } from "vitest";

import { MockProvider } from "../src/lib/ai/mockProvider";
import { TemplateService } from "../src/services/templateService";
import { InMemoryRepository } from "./helpers/inMemoryRepository";

describe("TemplateService", () => {
  it("creates template with qualitative and quantitative sections", async () => {
    const repository = new InMemoryRepository();
    const service = new TemplateService(repository, new MockProvider());

    const result = await service.createTemplate({
      projectId: "P-1001",
      projectType: "high-rise residential",
      requirements: {
        safetyClass: "A",
      },
    });

    expect(result.projectId).toBe("P-1001");
    expect(result.qualitative.length).toBeGreaterThan(0);
    expect(result.quantitative.length).toBeGreaterThan(0);
    expect(repository.templates.size).toBe(1);
  });
});
