\# Data Dictionary



This page outlines the mapping from the raw TradingView data frame attributes to our cleaned JSON target metrics.



| Raw Attribute | Cleaned Target Field | Data Type | Description |

| :--- | :--- | :--- | :--- |

| `name` | `Ticker` | String | Financial instrument tracking symbol (e.g., BTCUSD) |

| `close` | `Closing\_Price` | Float | The final evaluation price of the current matrix loop |

| `volume` | `Volume` | Float | Total market transactional volume traded |

| `market\_cap\_basic`| `Market\_Cap` | Float | Net basic valuation of the asset |

| `change` | `Price\_Change\_Percent` | Float | 24-hour delta shifting tracking percentage |

| \*Calculated\* | `Risk\_Profile` | String | Evaluation flags: `High Volatility` (>4% shift) or `Stable` |

