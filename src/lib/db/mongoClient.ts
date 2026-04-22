import { Db, MongoClient } from "mongodb";

import type { RuntimeConfig } from "../../config";
import { getSecretValue } from "./secretManager";

let clientPromise: Promise<MongoClient> | null = null;

async function resolveMongoUri(config: RuntimeConfig): Promise<string> {
  if (config.mongoUri) {
    return config.mongoUri;
  }
  return getSecretValue(config.mongoSecretName);
}

export async function connectMongo(config: RuntimeConfig): Promise<Db> {
  if (!clientPromise) {
    clientPromise = (async () => {
      const uri = await resolveMongoUri(config);
      const client = new MongoClient(uri);
      await client.connect();
      return client;
    })();
  }

  const client = await clientPromise;
  return client.db(config.mongoDbName);
}

export async function closeMongo() {
  if (!clientPromise) {
    return;
  }

  const client = await clientPromise;
  await client.close();
  clientPromise = null;
}
