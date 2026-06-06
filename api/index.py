import os
import time
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from concurrent.futures import ThreadPoolExecutor, as_completed
from flask import Flask, request, jsonify

app = Flask(__name__)

# ── Resilient HTTP session (retry once on 429/5xx) ───────────────────────────
_session = requests.Session()
_session.mount("https://", HTTPAdapter(max_retries=Retry(
    total=1, backoff_factor=0.2, status_forcelist=[429, 500, 502, 503],
    allowed_methods=["GET", "POST"]
)))

# ── Config ────────────────────────────────────────────────────────────────────
TOKEN    = os.environ.get("BOT_TOKEN", "")
TG       = f"https://api.telegram.org/bot{TOKEN}"
BOT_NAME = "RPC Radar Bot"
BOT_EMOJI = "⚡"
GITHUB_REPO = "https://github.com/Lord1Egypt/rpc-radar-bot"

# ── Chain Registry ────────────────────────────────────────────────────────────
# All endpoints verified live against publicnode.com — 2026-06-07

EVM_CHAINS = {
    "ethereum":   {"name": "Ethereum",   "url": "https://ethereum-rpc.publicnode.com",         "chainId": 1,       "symbol": "ETH",   "explorer": "https://etherscan.io",                  "emoji": "🔵"},
    "bnb":        {"name": "BNB Chain",  "url": "https://bsc-rpc.publicnode.com",               "chainId": 56,      "symbol": "BNB",   "explorer": "https://bscscan.com",                   "emoji": "🟡"},
    "polygon":    {"name": "Polygon",    "url": "https://polygon-bor-rpc.publicnode.com",       "chainId": 137,     "symbol": "MATIC", "explorer": "https://polygonscan.com",               "emoji": "🟣"},
    "base":       {"name": "Base",       "url": "https://base-rpc.publicnode.com",              "chainId": 8453,    "symbol": "ETH",   "explorer": "https://basescan.org",                  "emoji": "🔷"},
    "arbitrum":   {"name": "Arbitrum",   "url": "https://arbitrum-one-rpc.publicnode.com",      "chainId": 42161,   "symbol": "ETH",   "explorer": "https://arbiscan.io",                   "emoji": "🌀"},
    "optimism":   {"name": "Optimism",   "url": "https://optimism-rpc.publicnode.com",          "chainId": 10,      "symbol": "ETH",   "explorer": "https://optimistic.etherscan.io",       "emoji": "🔴"},
    "avalanche":  {"name": "Avalanche",  "url": "https://avalanche-c-chain-rpc.publicnode.com", "chainId": 43114,   "symbol": "AVAX",  "explorer": "https://snowtrace.io",                  "emoji": "🔺"},
    "linea":      {"name": "Linea",      "url": "https://linea-rpc.publicnode.com",             "chainId": 59144,   "symbol": "ETH",   "explorer": "https://lineascan.build",               "emoji": "⬛"},
    "scroll":     {"name": "Scroll",     "url": "https://scroll-rpc.publicnode.com",            "chainId": 534352,  "symbol": "ETH",   "explorer": "https://scrollscan.com",                "emoji": "📜"},
    "blast":      {"name": "Blast",      "url": "https://blast-rpc.publicnode.com",             "chainId": 81457,   "symbol": "ETH",   "explorer": "https://blastscan.io",                  "emoji": "💥"},
    "gnosis":     {"name": "Gnosis",     "url": "https://gnosis-rpc.publicnode.com",            "chainId": 100,     "symbol": "xDAI",  "explorer": "https://gnosisscan.io",                 "emoji": "🦉"},
    "celo":       {"name": "Celo",       "url": "https://celo-rpc.publicnode.com",              "chainId": 42220,   "symbol": "CELO",  "explorer": "https://celoscan.io",                   "emoji": "🌿"},
    "moonbeam":   {"name": "Moonbeam",   "url": "https://moonbeam-rpc.publicnode.com",          "chainId": 1284,    "symbol": "GLMR",  "explorer": "https://moonscan.io",                   "emoji": "🌕"},
    "metis":      {"name": "Metis",      "url": "https://metis-rpc.publicnode.com",             "chainId": 1088,    "symbol": "METIS", "explorer": "https://andromeda-explorer.metis.io",   "emoji": "🏛"},
    "opbnb":      {"name": "opBNB",      "url": "https://opbnb-rpc.publicnode.com",             "chainId": 204,     "symbol": "BNB",   "explorer": "https://mainnet.opbnbscan.com",         "emoji": "🟨"},
    "pulsechain": {"name": "PulseChain", "url": "https://pulsechain-rpc.publicnode.com",        "chainId": 369,     "symbol": "PLS",   "explorer": "https://scan.pulsechain.com",           "emoji": "💓"},
    "mantle":     {"name": "Mantle",     "url": "https://mantle-rpc.publicnode.com",            "chainId": 5000,    "symbol": "MNT",   "explorer": "https://explorer.mantle.xyz",           "emoji": "⚙️"},
    "taiko":      {"name": "Taiko",      "url": "https://taiko-rpc.publicnode.com",             "chainId": 167000,  "symbol": "ETH",   "explorer": "https://taikoscan.io",                  "emoji": "🥁"},
    "berachain":  {"name": "Berachain",  "url": "https://berachain-rpc.publicnode.com",         "chainId": 80094,   "symbol": "BERA",  "explorer": "https://berascan.com",                  "emoji": "🐻"},
    "soneium":    {"name": "Soneium",    "url": "https://soneium-rpc.publicnode.com",           "chainId": 1868,    "symbol": "ETH",   "explorer": "https://soneium.blockscout.com",        "emoji": "🌊"},
    "unichain":   {"name": "Unichain",   "url": "https://unichain-rpc.publicnode.com",          "chainId": 130,     "symbol": "ETH",   "explorer": "https://unichain.blockscout.com",       "emoji": "🦄"},
    "fraxtal":    {"name": "Fraxtal",    "url": "https://fraxtal-rpc.publicnode.com",           "chainId": 252,     "symbol": "frxETH","explorer": "https://fraxscan.com",                  "emoji": "⬜"},
    "chiliz":     {"name": "Chiliz",     "url": "https://chiliz-rpc.publicnode.com",            "chainId": 88888,   "symbol": "CHZ",   "explorer": "https://scan.chiliz.com",               "emoji": "🌶"},
    "sonic":      {"name": "Sonic",      "url": "https://sonic-rpc.publicnode.com",             "chainId": 146,     "symbol": "S",     "explorer": "https://sonicscan.org",                 "emoji": "⚡"},
}

NON_EVM_CHAINS = {
    "solana":   {"name": "Solana",   "url": "https://solana-rpc.publicnode.com",   "type": "solana",   "symbol": "SOL",  "explorer": "https://solscan.io",                    "emoji": "🟣"},
    "bitcoin":  {"name": "Bitcoin",  "url": "https://bitcoin-rpc.publicnode.com",  "type": "bitcoin",  "symbol": "BTC",  "explorer": "https://mempool.space",                 "emoji": "🟠"},
    "ton":      {"name": "TON",      "url": "https://mainnet-v4.tonhubapi.com",    "type": "ton",      "symbol": "TON",  "explorer": "https://tonviewer.com",                 "emoji": "💎"},
    "starknet": {"name": "Starknet", "url": "https://starknet-rpc.publicnode.com", "type": "starknet", "symbol": "STRK", "explorer": "https://starkscan.co",                  "emoji": "⭐"},
    "sui":      {"name": "Sui",      "url": "https://sui-rpc.publicnode.com",      "type": "sui",      "symbol": "SUI",  "explorer": "https://suiscan.xyz",                   "emoji": "💧"},
    "cosmos":   {"name": "Cosmos",   "url": "https://cosmos-rest.publicnode.com",  "type": "cosmos",   "symbol": "ATOM", "explorer": "https://www.mintscan.io/cosmos",         "emoji": "⚛️"},
}

ALL_CHAINS = {**EVM_CHAINS, **{k: {**v, "is_evm": False} for k, v in NON_EVM_CHAINS.items()}}

# ── Aliases ───────────────────────────────────────────────────────────────────
ALIASES = {
    "eth": "ethereum", "ether": "ethereum", "mainnet": "ethereum",
    "bsc": "bnb", "binance": "bnb", "bnbchain": "bnb",
    "poly": "polygon", "matic": "polygon",
    "arb": "arbitrum", "arbone": "arbitrum",
    "op": "optimism",
    "avax": "avalanche", "ava": "avalanche",
    "xdai": "gnosis", "gno": "gnosis",
    "opbnb": "opbnb",
    "pulse": "pulsechain", "pls": "pulsechain",
    "mnt": "mantle",
    "bera": "berachain",
    "uni": "unichain",
    "frax": "fraxtal",
    "chz": "chiliz",
    "sol": "solana",
    "btc": "bitcoin", "bit": "bitcoin",
    "strk": "starknet", "stark": "starknet",
    "atom": "cosmos", "cosm": "cosmos",
    "sui": "sui",
}

def resolve_chain(name):
    name = name.lower().strip()
    if name in ALL_CHAINS:
        return name
    if name in ALIASES:
        return ALIASES[name]
    for key, chain in ALL_CHAINS.items():
        if chain["name"].lower() == name:
            return key
    return None

# ── Telegram helpers ──────────────────────────────────────────────────────────
def send(chat_id, text, parse_mode="Markdown"):
    _session.post(f"{TG}/sendMessage", json={
        "chat_id": chat_id, "text": text,
        "parse_mode": parse_mode, "disable_web_page_preview": True,
    }, timeout=10)

def action(chat_id, act="typing"):
    _session.post(f"{TG}/sendChatAction",
        json={"chat_id": chat_id, "action": act}, timeout=5)

# ── RPC callers ───────────────────────────────────────────────────────────────
def _evm_rpc(url, method, params=None, timeout=6):
    r = _session.post(url, json={"jsonrpc": "2.0", "id": 1, "method": method, "params": params or []}, timeout=timeout)
    d = r.json()
    if "error" in d:
        raise Exception(d["error"].get("message", str(d["error"])))
    return d["result"]

def fetch_evm(key, chain, timeout=5):
    t0 = time.time()
    try:
        block_hex = _evm_rpc(chain["url"], "eth_blockNumber", timeout=timeout)
        block = int(block_hex, 16)
        ms = int((time.time() - t0) * 1000)
        return key, {"ok": True, "block": block, "ms": ms}
    except Exception as e:
        ms = int((time.time() - t0) * 1000)
        return key, {"ok": False, "block": None, "ms": ms, "err": str(e)[:60]}

def fetch_evm_full(chain, timeout=6):
    t0 = time.time()
    block = int(_evm_rpc(chain["url"], "eth_blockNumber", timeout=timeout), 16)
    gas_hex = _evm_rpc(chain["url"], "eth_gasPrice", timeout=timeout)
    gas_gwei = int(gas_hex, 16) / 1e9
    ms = int((time.time() - t0) * 1000)
    return block, gas_gwei, ms

def fetch_solana(chain, timeout=6):
    t0 = time.time()
    r = _session.post(chain["url"], json={"jsonrpc": "2.0", "id": 1, "method": "getBlockHeight", "params": []}, timeout=timeout)
    height = r.json()["result"]
    r2 = _session.post(chain["url"], json={"jsonrpc": "2.0", "id": 2, "method": "getVersion", "params": []}, timeout=timeout)
    ver = r2.json()["result"].get("solana-core", "?")
    ms = int((time.time() - t0) * 1000)
    return height, ver, ms

def fetch_bitcoin(chain, timeout=6):
    t0 = time.time()
    r = _session.post(chain["url"], json={"jsonrpc": "1.0", "id": 1, "method": "getblockchaininfo", "params": []}, timeout=timeout)
    d = r.json()["result"]
    ms = int((time.time() - t0) * 1000)
    return d["blocks"], d.get("difficulty", 0), ms

def fetch_ton(chain, timeout=6):
    t0 = time.time()
    r = _session.get(f"{chain['url']}/block/latest", timeout=timeout)
    d = r.json()
    seqno = d["last"]["seqno"]
    ms = int((time.time() - t0) * 1000)
    return seqno, ms

def fetch_starknet(chain, timeout=6):
    t0 = time.time()
    r = _session.post(chain["url"], json={"jsonrpc": "2.0", "id": 1, "method": "starknet_blockNumber", "params": []}, timeout=timeout)
    block = r.json()["result"]
    ms = int((time.time() - t0) * 1000)
    return block, ms

def fetch_sui(chain, timeout=6):
    t0 = time.time()
    r = _session.post(chain["url"], json={"jsonrpc": "2.0", "id": 1, "method": "sui_getLatestCheckpointSequenceNumber", "params": []}, timeout=timeout)
    checkpoint = int(r.json()["result"])
    ms = int((time.time() - t0) * 1000)
    return checkpoint, ms

def fetch_cosmos(chain, timeout=6):
    t0 = time.time()
    r = _session.get(f"{chain['url']}/cosmos/base/tendermint/v1beta1/blocks/latest", timeout=timeout)
    h = r.json()["block"]["header"]
    height = int(h["height"])
    ms = int((time.time() - t0) * 1000)
    return height, ms

def fetch_non_evm_quick(key, chain, timeout=5):
    t0 = time.time()
    try:
        t = chain.get("type", "")
        if t == "solana":
            r = _session.post(chain["url"], json={"jsonrpc": "2.0", "id": 1, "method": "getBlockHeight", "params": []}, timeout=timeout)
            val = r.json()["result"]
        elif t == "bitcoin":
            r = _session.post(chain["url"], json={"jsonrpc": "1.0", "id": 1, "method": "getblockcount", "params": []}, timeout=timeout)
            val = r.json()["result"]
        elif t == "ton":
            r = _session.get(f"{chain['url']}/block/latest", timeout=timeout)
            val = r.json()["last"]["seqno"]
        elif t == "starknet":
            r = _session.post(chain["url"], json={"jsonrpc": "2.0", "id": 1, "method": "starknet_blockNumber", "params": []}, timeout=timeout)
            val = r.json()["result"]
        elif t == "sui":
            r = _session.post(chain["url"], json={"jsonrpc": "2.0", "id": 1, "method": "sui_getLatestCheckpointSequenceNumber", "params": []}, timeout=timeout)
            val = int(r.json()["result"])
        elif t == "cosmos":
            r = _session.get(f"{chain['url']}/cosmos/base/tendermint/v1beta1/blocks/latest", timeout=timeout)
            val = int(r.json()["block"]["header"]["height"])
        else:
            val = None
        ms = int((time.time() - t0) * 1000)
        return key, {"ok": val is not None, "val": val, "ms": ms}
    except Exception as e:
        ms = int((time.time() - t0) * 1000)
        return key, {"ok": False, "val": None, "ms": ms, "err": str(e)[:60]}

def fmt_num(n):
    if n >= 1_000_000_000: return f"{n/1_000_000_000:.2f}B"
    if n >= 1_000_000:     return f"{n/1_000_000:.2f}M"
    if n >= 1_000:         return f"{n/1_000:.1f}K"
    return str(n)

def ms_badge(ms):
    if ms < 200: return "🟢"
    if ms < 600: return "🟡"
    return "🔴"

# ── Command handlers ──────────────────────────────────────────────────────────
def cmd_evm(chat_id):
    action(chat_id)
    results = {}

    def _fetch(item):
        k, v = item
        return fetch_evm(k, v, timeout=5)

    with ThreadPoolExecutor(max_workers=len(EVM_CHAINS)) as ex:
        futures = [ex.submit(_fetch, item) for item in EVM_CHAINS.items()]
        for f in as_completed(futures, timeout=10):
            try:
                k, r = f.result()
                results[k] = r
            except Exception:
                pass

    lines = ["⚙️ *EVM Chains — Live Block Heights*\n"]
    for key, chain in EVM_CHAINS.items():
        r = results.get(key, {"ok": False, "block": None, "ms": 0})
        em = chain["emoji"]
        name = chain["name"]
        if r["ok"]:
            badge = ms_badge(r["ms"])
            lines.append(f"{badge} {em} *{name}* — block `#{r['block']:,}` ({r['ms']}ms)")
        else:
            lines.append(f"❌ {em} *{name}* — offline")

    online = sum(1 for r in results.values() if r.get("ok"))
    lines.append(f"\n✅ {online}/{len(EVM_CHAINS)} online  |  [publicnode.com](https://publicnode.com)")
    send(chat_id, "\n".join(lines))


def cmd_l1(chat_id):
    action(chat_id)
    results = {}

    def _fetch(item):
        k, v = item
        return fetch_non_evm_quick(k, v, timeout=6)

    with ThreadPoolExecutor(max_workers=len(NON_EVM_CHAINS)) as ex:
        futures = [ex.submit(_fetch, item) for item in NON_EVM_CHAINS.items()]
        for f in as_completed(futures, timeout=12):
            try:
                k, r = f.result()
                results[k] = r
            except Exception:
                pass

    labels = {
        "solana":   ("Block height", ""),
        "bitcoin":  ("Block height", ""),
        "ton":      ("Master seqno", ""),
        "starknet": ("Block",        ""),
        "sui":      ("Checkpoint",   ""),
        "cosmos":   ("Block",        ""),
    }

    lines = ["🌐 *Non-EVM Chains — Live Stats*\n"]
    for key, chain in NON_EVM_CHAINS.items():
        r = results.get(key, {"ok": False, "val": None, "ms": 0})
        em = chain["emoji"]
        name = chain["name"]
        symbol = chain["symbol"]
        label, _ = labels.get(key, ("Value", ""))
        if r["ok"]:
            badge = ms_badge(r["ms"])
            lines.append(f"{badge} {em} *{name}* (`{symbol}`) — {label} `{r['val']:,}` ({r['ms']}ms)")
        else:
            lines.append(f"❌ {em} *{name}* — offline")

    online = sum(1 for r in results.values() if r.get("ok"))
    lines.append(f"\n✅ {online}/{len(NON_EVM_CHAINS)} online  |  [publicnode.com](https://publicnode.com)")
    send(chat_id, "\n".join(lines))


def cmd_status(chat_id):
    action(chat_id)
    evm_results = {}
    l1_results  = {}

    def _evm(item):
        return fetch_evm(item[0], item[1], timeout=5)

    def _l1(item):
        return fetch_non_evm_quick(item[0], item[1], timeout=5)

    with ThreadPoolExecutor(max_workers=len(ALL_CHAINS)) as ex:
        evm_futures = [ex.submit(_evm, item) for item in EVM_CHAINS.items()]
        l1_futures  = [ex.submit(_l1,  item) for item in NON_EVM_CHAINS.items()]
        for f in as_completed(evm_futures + l1_futures, timeout=25):
            try:
                k, r = f.result()
                if k in EVM_CHAINS:
                    evm_results[k] = r
                else:
                    l1_results[k] = r
            except Exception:
                pass

    # Categorise EVM by latency
    fast, ok_ms, slow, down = [], [], [], []
    for key, chain in EVM_CHAINS.items():
        r = evm_results.get(key, {"ok": False, "ms": 0})
        name = f"{chain['emoji']}{chain['name']}"
        if not r.get("ok"):
            down.append(name)
        elif r["ms"] < 200:
            fast.append(name)
        elif r["ms"] < 600:
            ok_ms.append(name)
        else:
            slow.append(name)

    lines = ["🔍 *RPC Status — All 30 Chains*\n"]
    lines.append("*EVM Chains (24):*")
    if fast:  lines.append(f"🟢 Fast:  {', '.join(fast)}")
    if ok_ms: lines.append(f"🟡 OK:    {', '.join(ok_ms)}")
    if slow:  lines.append(f"🔴 Slow:  {', '.join(slow)}")
    if down:  lines.append(f"❌ Down:  {', '.join(down)}")

    lines.append("\n*Non-EVM Chains (6):*")
    for key, chain in NON_EVM_CHAINS.items():
        r = l1_results.get(key, {"ok": False, "ms": 0})
        if r.get("ok"):
            badge = ms_badge(r["ms"])
            lines.append(f"{badge} {chain['emoji']} {chain['name']} — `{r['ms']}ms`")
        else:
            lines.append(f"❌ {chain['emoji']} {chain['name']} — offline")

    evm_ok = sum(1 for r in evm_results.values() if r.get("ok"))
    l1_ok  = sum(1 for r in l1_results.values()  if r.get("ok"))
    total  = evm_ok + l1_ok
    lines.append(f"\n*{total}/30 nodes online*")
    send(chat_id, "\n".join(lines))


def cmd_balance(chat_id, addr):
    action(chat_id)
    addr = addr.strip().lower()
    if not addr.startswith("0x") or len(addr) != 42:
        send(chat_id,
            "❌ `/balance` checks EVM balances — needs a `0x` address (42 chars).\n\n"
            "📖 *Example:*\n"
            "`/balance 0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045` — Vitalik's address")
        return

    results = {}
    def fetch_bal(key, chain):
        t0 = time.time()
        try:
            r = _session.post(chain["url"],
                json={"jsonrpc":"2.0","id":1,"method":"eth_getBalance","params":[addr,"latest"]},
                timeout=5)
            bal = int(r.json()["result"], 16) / 1e18
            ms  = int((time.time() - t0) * 1000)
            return key, {"ok": True, "bal": bal, "ms": ms}
        except Exception:
            return key, {"ok": False, "bal": 0.0, "ms": int((time.time()-t0)*1000)}

    with ThreadPoolExecutor(max_workers=len(EVM_CHAINS)) as ex:
        futures = [ex.submit(fetch_bal, k, v) for k, v in EVM_CHAINS.items()]
        for f in as_completed(futures, timeout=12):
            try:
                k, r = f.result()
                results[k] = r
            except Exception:
                pass

    has_funds = [
        (key, EVM_CHAINS[key], r["bal"])
        for key, r in results.items()
        if r.get("ok") and r["bal"] > 0.000001
    ]
    has_funds.sort(key=lambda x: -x[2])

    short_addr = f"{addr[:8]}…{addr[-4:]}"
    lines = [f"💰 *Multi-Chain Balance*\n\n📬 `{addr}`\n"]

    if has_funds:
        lines.append(f"*Found on {len(has_funds)} chain(s):*")
        for key, chain, bal in has_funds:
            badge = ms_badge(results[key]["ms"])
            lines.append(f"{badge} {chain['emoji']} {chain['name']}: `{bal:.6f} {chain['symbol']}`")
    else:
        lines.append("_No EVM balance found on any of the 24 chains._")

    zero_chains = [EVM_CHAINS[k]["name"] for k, r in results.items() if r.get("ok") and r["bal"] <= 0.000001]
    if zero_chains and has_funds:
        lines.append(f"\n_Zero on: {', '.join(zero_chains[:6])}{'…' if len(zero_chains) > 6 else ''}_")

    send(chat_id, "\n".join(lines))


def cmd_node(chat_id, arg):
    action(chat_id)
    key = resolve_chain(arg)
    if not key:
        close = [c["name"] for c in ALL_CHAINS.values() if arg.lower() in c["name"].lower()]
        hint = f"\n\nDid you mean: {', '.join(close[:3])}?" if close else ""
        send(chat_id,
            f"❌ Chain `{arg}` not found.{hint}\n\n"
            f"Use `/chains` to see all supported chains.\n"
            f"Example: `/node ethereum`  or  `/node solana`")
        return

    if key in EVM_CHAINS:
        chain = EVM_CHAINS[key]
        try:
            block, gas_gwei, ms = fetch_evm_full(chain)
            badge = ms_badge(ms)
            msg = (
                f"{chain['emoji']} *{chain['name']}*\n\n"
                f"📦 Latest Block: `#{block:,}`\n"
                f"⛽ Gas Price: `{gas_gwei:.4f} Gwei`\n"
                f"🔢 Chain ID: `{chain['chainId']}`\n"
                f"💰 Native Token: `{chain['symbol']}`\n"
                f"🌐 RPC: `{chain['url']}`\n"
                f"{badge} Latency: `{ms}ms`\n\n"
                f"🔗 [Open Explorer]({chain['explorer']})"
            )
        except Exception as e:
            msg = (
                f"{chain['emoji']} *{chain['name']}*\n\n"
                f"❌ Node offline: `{str(e)[:100]}`\n"
                f"🌐 RPC: `{chain['url']}`"
            )

    else:
        chain = NON_EVM_CHAINS[key]
        ct = chain["type"]
        try:
            if ct == "solana":
                height, ver, ms = fetch_solana(chain)
                badge = ms_badge(ms)
                msg = (
                    f"{chain['emoji']} *Solana*\n\n"
                    f"📦 Block Height: `{height:,}`\n"
                    f"🔧 Version: `{ver}`\n"
                    f"💰 Token: `SOL`\n"
                    f"🌐 RPC: `{chain['url']}`\n"
                    f"{badge} Latency: `{ms}ms`\n\n"
                    f"🔗 [Solscan]({chain['explorer']})"
                )
            elif ct == "bitcoin":
                height, diff, ms = fetch_bitcoin(chain)
                badge = ms_badge(ms)
                msg = (
                    f"{chain['emoji']} *Bitcoin*\n\n"
                    f"📦 Block Height: `{height:,}`\n"
                    f"⚙️ Difficulty: `{diff:.2e}`\n"
                    f"💰 Token: `BTC`\n"
                    f"🌐 RPC: `{chain['url']}`\n"
                    f"{badge} Latency: `{ms}ms`\n\n"
                    f"🔗 [Mempool.space]({chain['explorer']})"
                )
            elif ct == "ton":
                seqno, ms = fetch_ton(chain)
                badge = ms_badge(ms)
                msg = (
                    f"{chain['emoji']} *TON*\n\n"
                    f"📦 Masterchain Seqno: `{seqno:,}`\n"
                    f"💰 Token: `TON`\n"
                    f"🌐 API: `{chain['url']}`\n"
                    f"{badge} Latency: `{ms}ms`\n\n"
                    f"🔗 [TON Viewer]({chain['explorer']})"
                )
            elif ct == "starknet":
                block, ms = fetch_starknet(chain)
                badge = ms_badge(ms)
                msg = (
                    f"{chain['emoji']} *Starknet*\n\n"
                    f"📦 Latest Block: `{block:,}`\n"
                    f"💰 Token: `STRK`\n"
                    f"🌐 RPC: `{chain['url']}`\n"
                    f"{badge} Latency: `{ms}ms`\n\n"
                    f"🔗 [Starkscan]({chain['explorer']})"
                )
            elif ct == "sui":
                checkpoint, ms = fetch_sui(chain)
                badge = ms_badge(ms)
                msg = (
                    f"{chain['emoji']} *Sui*\n\n"
                    f"📦 Latest Checkpoint: `{checkpoint:,}`\n"
                    f"💰 Token: `SUI`\n"
                    f"🌐 RPC: `{chain['url']}`\n"
                    f"{badge} Latency: `{ms}ms`\n\n"
                    f"🔗 [Suiscan]({chain['explorer']})"
                )
            elif ct == "cosmos":
                height, ms = fetch_cosmos(chain)
                badge = ms_badge(ms)
                msg = (
                    f"{chain['emoji']} *Cosmos*\n\n"
                    f"📦 Latest Block: `{height:,}`\n"
                    f"💰 Token: `ATOM`\n"
                    f"🌐 REST: `{chain['url']}`\n"
                    f"{badge} Latency: `{ms}ms`\n\n"
                    f"🔗 [Mintscan]({chain['explorer']})"
                )
            else:
                msg = f"❌ Unknown chain type: `{ct}`"
        except Exception as e:
            msg = (
                f"{chain['emoji']} *{chain['name']}*\n\n"
                f"❌ Node error: `{str(e)[:120]}`\n"
                f"🌐 URL: `{chain['url']}`"
            )

    send(chat_id, msg)


def cmd_ping(chat_id, arg):
    action(chat_id)
    key = resolve_chain(arg)
    if not key:
        send(chat_id, f"❌ Chain `{arg}` not found. Use `/chains` to see all chains.")
        return

    chain = ALL_CHAINS.get(key) or EVM_CHAINS.get(key) or NON_EVM_CHAINS.get(key)
    name = chain["name"]
    em   = chain["emoji"]
    url  = chain["url"]

    t0 = time.time()
    try:
        if key in EVM_CHAINS:
            _evm_rpc(url, "eth_blockNumber", timeout=6)
        elif chain.get("type") == "ton":
            _session.get(f"{url}/block/latest", timeout=6)
        elif chain.get("type") == "cosmos":
            _session.get(f"{url}/cosmos/base/tendermint/v1beta1/blocks/latest", timeout=6)
        elif chain.get("type") == "bitcoin":
            _session.post(url, json={"jsonrpc":"1.0","id":1,"method":"getblockcount","params":[]}, timeout=6)
        else:
            _session.post(url, json={"jsonrpc":"2.0","id":1,"method":"eth_blockNumber","params":[]}, timeout=6)
        ms = int((time.time() - t0) * 1000)
        badge = ms_badge(ms)
        speed = "Fast" if ms < 200 else ("OK" if ms < 600 else "Slow")
        send(chat_id,
            f"{badge} *Ping: {em} {name}*\n\n"
            f"🟢 Online — `{ms}ms` ({speed})\n"
            f"🌐 `{url}`"
        )
    except Exception as e:
        ms = int((time.time() - t0) * 1000)
        send(chat_id,
            f"❌ *Ping: {em} {name}*\n\n"
            f"🔴 Offline — `{ms}ms`\n"
            f"Error: `{str(e)[:80]}`\n"
            f"🌐 `{url}`"
        )


def cmd_chains(chat_id):
    lines = ["🌐 *All Supported Chains*\n"]
    lines.append("*EVM Chains (24):*")
    for key, chain in EVM_CHAINS.items():
        lines.append(f"{chain['emoji']} {chain['name']} — `/node {key}`  |  chainId `{chain['chainId']}`")
    lines.append("\n*Non-EVM Chains (6):*")
    for key, chain in NON_EVM_CHAINS.items():
        lines.append(f"{chain['emoji']} {chain['name']} (`{chain['symbol']}`) — `/node {key}`")
    lines.append(f"\n_Source: [publicnode.com](https://publicnode.com) + [TON Hub](https://tonhubapi.com)_")
    send(chat_id, "\n".join(lines))


def cmd_search(chat_id, query):
    query = query.lower().strip()
    matches = []
    for key, chain in ALL_CHAINS.items():
        if query in key or query in chain["name"].lower() or query in chain.get("symbol","").lower():
            matches.append((key, chain))
    if not matches:
        send(chat_id, f"❌ No chains found for `{query}`.\n\nUse `/chains` to browse all 30 chains.")
        return
    lines = [f"🔍 *Search results for '{query}':*\n"]
    for key, chain in matches[:8]:
        lines.append(f"{chain['emoji']} *{chain['name']}* (`{chain['symbol']}`) — `/node {key}`")
    send(chat_id, "\n".join(lines))


# ── Help text ─────────────────────────────────────────────────────────────────
HELP_TEXT = (
    f"{BOT_EMOJI} *RPC Radar Bot — Commands*\n\n"
    "`/evm` — Live block heights for all 24 EVM chains\n"
    "`/l1` — Non-EVM: Solana, Bitcoin, TON, Starknet, Sui, Cosmos\n"
    "`/status` — Health check (✅/❌ + latency) for all 30 chains\n"
    "`/node <chain>` — Full live stats for one chain\n"
    "`/ping <chain>` — Latency test for one node\n"
    "`/balance <0x...>` — ETH balance across all 24 EVM chains\n"
    "`/chains` — Browse all 30 supported chains\n"
    "`/search <name>` — Find a chain by name or symbol\n\n"
    "📖 *Examples:*\n"
    "• `/node ethereum` — Ethereum RPC stats\n"
    "• `/node solana` — Solana height + version\n"
    "• `/node bitcoin` — Bitcoin block height\n"
    "• `/node ton` — TON masterchain seqno\n"
    "• `/ping base` — Ping Base RPC\n"
    "• `/balance 0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045` — Vitalik's balances\n"
    "• `/search arb` — Find Arbitrum\n\n"
    "💡 *Shortcuts:* `eth`, `bnb`, `poly`, `arb`, `op`, `avax`, `sol`, `btc`, `atom`, `strk`\n\n"
    f"🔗 [publicnode.com](https://publicnode.com) — Free public RPC nodes, no key required"
)

WELCOME = (
    f"👋 Welcome to *{BOT_NAME}*!\n\n"
    f"Monitor 30 public blockchain RPC nodes in real-time — "
    f"24 EVM chains + Solana, Bitcoin, TON, Starknet, Sui, and Cosmos.\n\n"
    f"All endpoints from [publicnode.com](https://publicnode.com) — free, no API key needed.\n\n"
    + HELP_TEXT
)

# ── Main processor ────────────────────────────────────────────────────────────
def process(update):
    msg = update.get("message") or update.get("edited_message")
    if not msg:
        return
    chat_id = msg["chat"]["id"]
    text    = msg.get("text", "")
    if not text:
        return

    parts = text.split(maxsplit=1)
    cmd   = parts[0].lstrip("/").split("@")[0].lower()
    arg   = parts[1].strip() if len(parts) > 1 else ""

    try:
        if cmd in ("start", "help"):
            send(chat_id, WELCOME if cmd == "start" else HELP_TEXT)
        elif cmd == "evm":
            cmd_evm(chat_id)
        elif cmd == "l1":
            cmd_l1(chat_id)
        elif cmd == "status":
            cmd_status(chat_id)
        elif cmd == "chains":
            cmd_chains(chat_id)
        elif cmd == "node":
            if not arg:
                send(chat_id,
                    "❌ Usage: `/node <chain>`\n\n"
                    "📖 *Examples:*\n"
                    "• `/node ethereum`\n• `/node solana`\n• `/node bitcoin`\n• `/node ton`\n• `/node base`\n\n"
                    "Use `/chains` to see all 30 supported chains.")
            else:
                cmd_node(chat_id, arg)
        elif cmd == "ping":
            if not arg:
                send(chat_id,
                    "❌ Usage: `/ping <chain>`\n\n"
                    "📖 *Examples:*\n"
                    "• `/ping ethereum`\n• `/ping solana`\n• `/ping arbitrum`")
            else:
                cmd_ping(chat_id, arg)
        elif cmd == "balance":
            if not arg:
                send(chat_id,
                    "❌ Usage: `/balance <0x...>`\n\n"
                    "📖 *Example:*\n"
                    "`/balance 0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045`\n"
                    "↑ Checks Vitalik's ETH balance across all 24 EVM chains")
            else:
                cmd_balance(chat_id, arg)
        elif cmd == "search":
            if not arg:
                send(chat_id, "❌ Usage: `/search <name>`\n\nExample: `/search arb`  or  `/search sol`")
            else:
                cmd_search(chat_id, arg)
        else:
            send(chat_id, f"❓ Unknown command. Send /help to see all commands.")
    except Exception as e:
        send(chat_id, f"❌ Error: `{str(e)[:200]}`")


# ── Setup page ────────────────────────────────────────────────────────────────
def setup_html(host):
    webhook_url = f"https://{host}/webhook"
    has_token   = bool(TOKEN)
    badge_cls   = "badge-ok" if has_token else "badge-err"
    badge_icon  = "✅" if has_token else "❌"

    chains_rows = ""
    for key, c in EVM_CHAINS.items():
        chains_rows += f"<tr><td>{c['emoji']} {c['name']}</td><td><code>{c['url']}</code></td><td>EVM / chainId {c['chainId']}</td></tr>"
    for key, c in NON_EVM_CHAINS.items():
        chains_rows += f"<tr><td>{c['emoji']} {c['name']}</td><td><code>{c['url']}</code></td><td>{c['type'].title()}</td></tr>"

    h = f"""<!DOCTYPE html><html lang="en">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>⚡ RPC Radar Bot Setup</title>
<style>
*{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;background:#0d1117;color:#c9d1d9;padding:32px 16px}}
.wrap{{max-width:900px;margin:auto}}
header{{text-align:center;padding:32px 0 24px}}
header h1{{font-size:2.2rem;color:#f0f6fc;margin-bottom:8px}}
header p{{color:#8b949e;font-size:1rem}}
.card{{background:#161b22;border:1px solid #30363d;border-radius:12px;padding:28px;margin-bottom:20px}}
.card h2{{font-size:.92rem;color:#8b949e;font-weight:600;text-transform:uppercase;letter-spacing:.06em;margin-bottom:16px;display:flex;align-items:center;gap:10px}}
.sn{{background:#1f6feb;color:#fff;border-radius:50%;width:26px;height:26px;display:inline-flex;align-items:center;justify-content:center;font-size:.8rem;font-weight:700;flex-shrink:0}}
p{{color:#8b949e;line-height:1.6;margin-bottom:12px}}
table{{width:100%;border-collapse:collapse;margin:16px 0;font-size:.85rem}}
th{{text-align:left;color:#8b949e;padding:8px 12px;border-bottom:1px solid #30363d;font-weight:600}}
td{{padding:8px 12px;border-bottom:1px solid #21262d;vertical-align:middle}}
code{{background:#21262d;padding:2px 7px;border-radius:5px;font-family:monospace;font-size:.82rem;word-break:break-all}}
.wh{{background:#21262d;border:1px solid #30363d;border-radius:8px;padding:12px 16px;margin:14px 0;font-family:monospace;font-size:.9rem;word-break:break-all;color:#79c0ff}}
.btn{{display:inline-flex;align-items:center;gap:8px;padding:11px 22px;border-radius:8px;font-weight:600;font-size:.95rem;cursor:pointer;text-decoration:none;border:none;transition:.15s}}
.bp{{background:#238636;color:#fff}} .bp:hover{{background:#2ea043}}
.bs{{background:#21262d;color:#c9d1d9;border:1px solid #30363d}} .bs:hover{{background:#30363d}}
.acts{{display:flex;flex-wrap:wrap;gap:10px;margin-top:16px}}
#result{{margin-top:16px;padding:12px 16px;border-radius:8px;display:none}}
.rok{{background:#0d2818;border:1px solid #238636;color:#3fb950}}
.rerr{{background:#2d0000;border:1px solid #b62324;color:#f85149}}
.badge{{display:inline-flex;align-items:center;gap:6px;padding:4px 12px;border-radius:20px;font-size:.82rem;font-weight:600;margin-top:10px}}
.badge-ok{{background:#0d2818;border:1px solid #238636;color:#3fb950}}
.badge-err{{background:#2d0000;border:1px solid #b62324;color:#f85149}}
footer{{text-align:center;margin-top:48px;padding-bottom:32px;color:#484f58;font-size:.88rem}}
footer a{{color:#58a6ff;text-decoration:none}}
</style></head>
<body><div class="wrap">
<header>
  <h1>⚡ RPC Radar Bot Setup</h1>
  <p>Monitor 30 public blockchain RPC nodes directly in Telegram</p>
  <div class="badge {badge_cls}">{badge_icon} BOT_TOKEN: {"Configured" if has_token else "Not set"}</div>
</header>

<div class="card">
  <h2><span class="sn">1</span>Add Environment Variable</h2>
  <p>Add <code>BOT_TOKEN</code> in <strong>Vercel → Settings → Environment Variables</strong>, then redeploy.</p>
  <table><tr><th>Variable</th><th>Description</th><th>Required</th></tr>
  <tr><td><code>BOT_TOKEN</code></td><td>Telegram bot token from @BotFather</td><td style="color:#f85149;font-weight:600">REQUIRED</td></tr>
  </table>
  <p style="font-size:.88rem;color:#6e7681">No Infura or Etherscan keys needed — this bot uses 100% free public RPC endpoints.</p>
</div>

<div class="card">
  <h2><span class="sn">2</span>Register Webhook</h2>
  <div class="wh">🌐 {webhook_url}</div>
  <div class="acts">
    <button class="btn bp" onclick="doWH('set')">✅ Set Webhook</button>
    <button class="btn bs" onclick="doWH('info')">ℹ️ Webhook Info</button>
  </div>
  <div id="result"></div>
</div>

<div class="card">
  <h2><span class="sn">3</span>Supported Chains (30 total)</h2>
  <table><tr><th>Chain</th><th>RPC Endpoint</th><th>Type</th></tr>
  {chains_rows}
  </table>
</div>

<footer>
  <p>⚡ RPC Radar Bot · <a href="{GITHUB_REPO}" target="_blank">View on GitHub</a></p>
  <p style="margin-top:6px">Made with ❤️ by <a href="https://github.com/Lord1Egypt" target="_blank">Lord1Egypt</a> · Data from <a href="https://publicnode.com" target="_blank">publicnode.com</a></p>
</footer>
</div>
<script>
async function doWH(a){{
  const el=document.getElementById('result');
  el.style.display='block';el.className='';el.textContent='⏳ Working…';
  try{{const r=await fetch('/setup?action='+a);const d=await r.json();
  el.className=d.ok?'rok':'rerr';el.textContent=d.ok?'✅ '+d.message:'❌ '+d.message;
  }}catch(e){{el.className='rerr';el.textContent='❌ '+e.message;}}
}}
</script></body></html>"""
    return h


# ── Flask routes ──────────────────────────────────────────────────────────────
@app.route("/", methods=["GET"])
def home():
    host = (
        os.environ.get("VERCEL_PROJECT_PRODUCTION_URL")
        or os.environ.get("VERCEL_URL")
        or request.host
    )
    return setup_html(host)

@app.route("/setup", methods=["GET"])
def setup():
    if not TOKEN:
        return jsonify({"ok": False, "message": "BOT_TOKEN not set."})
    action_type = request.args.get("action", "set")
    host = (
        os.environ.get("VERCEL_PROJECT_PRODUCTION_URL")
        or os.environ.get("VERCEL_URL")
        or request.host
    )
    wh = f"https://{host}/webhook"
    try:
        if action_type == "set":
            r = _session.get(f"{TG}/setWebhook", params={"url": wh}, timeout=10).json()
            return jsonify({"ok": r.get("ok", False),
                "message": f"Webhook set to {wh}" if r.get("ok") else str(r.get("description", r))})
        elif action_type == "info":
            r = _session.get(f"{TG}/getWebhookInfo", timeout=10).json()
            info = r.get("result", {})
            return jsonify({"ok": True,
                "message": f"URL: {info.get('url','none')} | Pending: {info.get('pending_update_count',0)}"})
    except Exception as e:
        return jsonify({"ok": False, "message": str(e)})
    return jsonify({"ok": False, "message": "Unknown action"})

@app.route("/webhook", methods=["POST"])
def webhook():
    update = request.get_json(silent=True)
    if update:
        try:
            process(update)
        except Exception:
            pass
    return jsonify({"ok": True})

handler = app
