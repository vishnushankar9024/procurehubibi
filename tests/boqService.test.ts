import { describe, expect, it } from "vitest";

import { MockProvider } from "../src/lib/ai/mockProvider";
import { BoqService } from "../src/services/boqService";
import { InMemoryRepository } from "./helpers/inMemoryRepository";

describe("BoqService", () => {
  it("parses and stores BOQ items in POMI format", async () => {
    const repository = new InMemoryRepository();
    const service = new BoqService(repository, new MockProvider(), 3000);

    const result = await service.uploadBoq({
      projectId: "project-1",
      fileName: "boq.txt",
      mimeType: "text/plain",
      content: "Excavation and concrete line items",
    });

    expect(result.projectId).toBe("project-1");
    expect(result.standard).toBe("POMI");
    expect(result.items.length).toBeGreaterThan(0);
    expect(repository.boqRecords.size).toBe(1);
  });
});
