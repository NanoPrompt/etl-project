\# Troubleshooting \& Operational Guide



\### 1. Issue: GitLab Destination Skipped

\* \*\*Symptom:\*\* Logs report `⚠ Destination GitLab: Skipped (Token missing...)`

\* \*\*Resolution:\*\* Your active terminal session cannot access your token variable. Open PowerShell as an administrator and re-run your environment variable assignment command, then restart your terminal completely.



\### 2. Issue: Network Failures (404 / 401 Unauthorized)

\* \*\*Symptom:\*\* Cloud Upload Failed (404 or 401)

\* \*\*Resolution:\*\* Verify that your explicit `GITLAB\_PROJECT\_ID` inside the configuration header match exactly with your target GitLab project numbers found on your cloud homepage.

