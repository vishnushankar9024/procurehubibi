import { SecretManagerServiceClient } from "@google-cloud/secret-manager";

import { getConfig } from "../../config";

let client: SecretManagerServiceClient | null = null;

function getClient() {
  if (!client) {
    client = new SecretManagerServiceClient();
  }
  return client;
}

export async function getSecretValue(secretName: string): Promise<string> {
  const config = getConfig();
  if (!config.gcpProject && !config.mongoSecretResource) {
    throw new Error(
      "GOOGLE_CLOUD_PROJECT or MONGODB_URI_SECRET_RESOURCE is required when loading secret.",
    );
  }
  const secretResource =
    config.mongoSecretResource ??
    `projects/${config.gcpProject}/secrets/${secretName}/versions/${config.mongoSecretVersion}`;

  if (!secretResource.includes("/secrets/")) {
    throw new Error("Invalid secret resource configuration.");
  }

  const [version] = await getClient().accessSecretVersion({
    name: secretResource,
  });

  const payload = version.payload?.data?.toString("utf8")?.trim();
  if (!payload) {
    throw new Error(`Secret payload for ${secretName} is empty.`);
  }
  return payload;
}
