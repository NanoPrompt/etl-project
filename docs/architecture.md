\# System Architecture



The pipeline uses a \*\*Universal Distribution Network\*\* pattern. Instead of using standard git remotes to push to two places, the python environment directly acts as a hub using runtime API tokens.



\## Data Flow Diagram

\* \*\*Source:\*\* TradingView Screener API (Crypto)

\* \*\*Processing Hub:\*\* Local Engine (Pandas Engine)

\* \*\*Target A:\*\* Local JSON System filesystem (for GitHub Sync)

\* \*\*Target B:\*\* GitLab REST Commits Endpoints (Direct Cloud Injection)



\## Security Architecture

Credentials are explicitly barred from code storage. The system pulls `GITLAB\_COMMON\_TOKEN` from the host OS user-level environment space at application initialization.

