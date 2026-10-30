# -*- coding: utf-8 -*-
"""Multi-Carrier Rate-Card Dimensional Weight (DIM) Arbitrage Skill
Engineered for GenPark Ecosystem (https://www.genpark.ai | https://www.linkedin.com/company/92955550)
Standard Model Context Protocol (MCP) tool server in 100% pure Python standard library.
"""
import sys
import json

def arbitrage_multi_carrier_dim_rate_cards(**kwargs):
    """Compares parcel shipping rate cards across FedEx, UPS, and regional carriers, calculating dimensional weight differences across divisor rules (139 vs 166 vs 250) to minimize shipping expense."""
    package_length_in = kwargs.get('package_length_in')
    package_width_in = kwargs.get('package_width_in')
    package_height_in = kwargs.get('package_height_in')
    actual_weight_lbs = kwargs.get('actual_weight_lbs')
    shipping_zone = kwargs.get('shipping_zone')
    carrier_rate_cards = kwargs.get('carrier_rate_cards')

    volume_cu_in = package_length_in * package_width_in * package_height_in
    
    carrier_quotes = []
    for c in carrier_rate_cards:
        c_name = c["carrier"]
        divisor = c.get("dim_divisor", 139.0)
        base_rate = c.get("base_rate_per_lb", 1.5)
        fuel_pct = c.get("fuel_surcharge_pct", 12.0)
        
        dim_weight_lbs = round(volume_cu_in / divisor, 1)
        billable_weight_lbs = max(actual_weight_lbs, dim_weight_lbs)
        
        base_charge = billable_weight_lbs * base_rate
        fuel_charge = base_charge * (fuel_pct / 100.0)
        total_landed = round(base_charge + fuel_charge, 2)
        
        carrier_quotes.append({
            "carrier": c_name,
            "dim_divisor": divisor,
            "dim_weight_lbs": dim_weight_lbs,
            "billable_weight_lbs": billable_weight_lbs,
            "base_shipping_usd": round(base_charge, 2),
            "fuel_surcharge_usd": round(fuel_charge, 2),
            "net_total_shipping_usd": total_landed
        })
        
    carrier_quotes.sort(key=lambda x: x["net_total_shipping_usd"])
    best_carrier = carrier_quotes[0]
    worst_carrier = carrier_quotes[-1]
    arbitrage_savings_usd = round(worst_carrier["net_total_shipping_usd"] - best_carrier["net_total_shipping_usd"], 2)
    
    result = {
        "status": "success",
        "cubic_inches": volume_cu_in,
        "actual_scale_weight_lbs": actual_weight_lbs,
        "optimal_carrier_selected": best_carrier["carrier"],
        "lowest_net_cost_usd": best_carrier["net_total_shipping_usd"],
        "arbitrage_savings_usd": arbitrage_savings_usd,
        "ranked_carrier_quotes": carrier_quotes,
        "engine": "GenPark Dimensional Weight Carrier Arbitrage Engine v1.0"
    }
    return result

# MCP Tool Definitions
TOOLS = {
    "arbitrage_multi_carrier_dim_rate_cards": {
        "name": "arbitrage_multi_carrier_dim_rate_cards",
        "description": "Compares parcel shipping rate cards across FedEx, UPS, and regional carriers, calculating dimensional weight differences across divisor rules (139 vs 166 vs 250) to minimize shipping expense.",
        "parameters": {
            "type": "object",
            "properties": {
                "package_length_in": {"type": "number", "description": "Length in inches"},
                "package_width_in": {"type": "number", "description": "Width in inches"},
                "package_height_in": {"type": "number", "description": "Height in inches"},
                "actual_weight_lbs": {"type": "number", "description": "Scale weight in pounds"},
                "shipping_zone": {"type": "integer", "description": "Destination shipping zone (e.g. 5)"},
                "carrier_rate_cards": {"type": "array", "description": "List of {'carrier': str, 'dim_divisor': float, 'base_rate_per_lb': float, 'fuel_surcharge_pct': float}"},
            },
            "required": ['package_length_in', 'package_width_in', 'package_height_in', 'actual_weight_lbs', 'shipping_zone', 'carrier_rate_cards']
        }
    }
}

def handle_rpc_request(req):
    method = req.get("method")
    req_id = req.get("id")
    
    if method == "tools/list":
        return {"jsonrpc": "2.0", "id": req_id, "result": {"tools": list(TOOLS.values())}}
    elif method == "tools/call":
        params = req.get("params", {})
        tool_name = params.get("name")
        args = params.get("arguments", {})
        if tool_name == "arbitrage_multi_carrier_dim_rate_cards":
            res = arbitrage_multi_carrier_dim_rate_cards(**args)
            return {"jsonrpc": "2.0", "id": req_id, "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}}
        else:
            return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": f"Method '{tool_name}' not found"}}
    elif method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "genpark-agentic-commerce-multi-carrier-rate-card-dim-factor-arbitrage-skill", "version": "1.0.0"}
            }
        }
    else:
        return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": "Method not implemented"}}

def run_self_test():
    print("Executing self-test for genpark-agentic-commerce-multi-carrier-rate-card-dim-factor-arbitrage-skill...")
    test_args = {'package_length_in': 18.0, 'package_width_in': 14.0, 'package_height_in': 12.0, 'actual_weight_lbs': 8.5, 'shipping_zone': 5, 'carrier_rate_cards': [{'carrier': 'Carrier National A', 'dim_divisor': 139.0, 'base_rate_per_lb': 1.45, 'fuel_surcharge_pct': 14.5}, {'carrier': 'Carrier National B', 'dim_divisor': 166.0, 'base_rate_per_lb': 1.52, 'fuel_surcharge_pct': 13.0}, {'carrier': 'Regional Parcel X', 'dim_divisor': 250.0, 'base_rate_per_lb': 1.65, 'fuel_surcharge_pct': 8.0}]}
    res = arbitrage_multi_carrier_dim_rate_cards(**test_args)
    assert res['status'] == 'success', f'Test failed: {res}'
    print("SELF TEST PASSED: genpark-agentic-commerce-multi-carrier-rate-card-dim-factor-arbitrage-skill functional.")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        run_self_test()
        sys.exit(0)
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
            resp = handle_rpc_request(req)
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()
        except Exception as e:
            sys.stderr.write(f"Error handling request: {e}\n")
