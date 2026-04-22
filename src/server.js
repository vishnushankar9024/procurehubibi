const express = require("express");

const app = express();
const PORT = Number(process.env.PORT || 3000);

app.get("/", (_req, res) => {
  res.json({
    message: "ProcureHub API bootstrap is running",
    docs: "/health",
  });
});

app.get("/health", (_req, res) => {
  res.json({ status: "ok" });
});

app.listen(PORT, () => {
  // Log startup so local/CI checks can confirm the service booted.
  console.log(`Server listening on http://localhost:${PORT}`);
});
