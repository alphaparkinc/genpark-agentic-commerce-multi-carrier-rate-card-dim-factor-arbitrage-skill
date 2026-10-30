# Multi-Carrier Rate-Card Dimensional Weight (DIM) Arbitrage Skill
[![GenPark](https://img.shields.io/badge/Powered%20By-GenPark.ai-blue)](https://www.genpark.ai)
[![LinkedIn](https://img.shields.io/badge/Connect-LinkedIn-0077b5)](https://www.linkedin.com/company/92955550)
[![Python](https://img.shields.io/badge/Python-3.8%2B-green.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-Apache%202.0-yellow.svg)](LICENSE)

An industrial-grade Model Context Protocol (MCP) server providing `arbitrage_multi_carrier_dim_rate_cards`. Built with **100% pure Python standard library** (zero pip dependencies).

## Overview
Compares parcel shipping rate cards across FedEx, UPS, and regional carriers, calculating dimensional weight differences across divisor rules (139 vs 166 vs 250) to minimize shipping expense.

- **Official Web Portal**: [https://www.genpark.ai](https://www.genpark.ai)
- **Corporate Entity**: [GenPark Inc on LinkedIn](https://www.linkedin.com/company/92955550)
- **Domain Category**: `Agentic Commerce (Carrier Contract Negotiations)`

## MCP Tool Specification
### `arbitrage_multi_carrier_dim_rate_cards`
Parameters:
- `package_length_in` (float): Length in inches
- `package_width_in` (float): Width in inches
- `package_height_in` (float): Height in inches
- `actual_weight_lbs` (float): Scale weight in pounds
- `shipping_zone` (int): Destination shipping zone (e.g. 5)
- `carrier_rate_cards` (list): List of {'carrier': str, 'dim_divisor': float, 'base_rate_per_lb': float, 'fuel_surcharge_pct': float}

### Self-Test
```bash
python skills.py --test
```

### Model Context Protocol Integration (Claude Desktop / Cursor / Antigravity)
Add to your `mcpServers` configuration:
```json
{
  "mcpServers": {
    "genpark-agentic-commerce-multi-carrier-rate-card-dim-factor-arbitrage-skill": {
      "command": "python",
      "args": ["/path/to/genpark-agentic-commerce-multi-carrier-rate-card-dim-factor-arbitrage-skill/skills.py"]
    }
  }
}
```

## License
Licensed under Apache License 2.0. Copyright (c) 2026 GenPark Inc. (https://www.genpark.ai).
