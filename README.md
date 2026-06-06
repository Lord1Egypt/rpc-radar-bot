# ⚡ RPC Radar Bot

> Monitor **30 public blockchain RPC nodes** in real-time — directly in Telegram.
> No API keys required. Powered by [publicnode.com](https://publicnode.com) + [TON Hub](https://tonhubapi.com).

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/Lord1Egypt/rpc-radar-bot)

---

## 🤖 What It Does

Send a command to the bot and get live data from public RPC nodes:

- **Block heights** across 24 EVM chains — fetched in parallel in ~1s
- **Non-EVM chains** — Solana, Bitcoin, TON, Starknet, Sui, Cosmos
- **Latency badges** — 🟢 fast / 🟡 ok / 🔴 slow per node
- **Full chain profile** — block, gas price, chain ID, explorer link
- **Health check** — ✅/❌ status for all 30 nodes at once
- **No API key needed** — all endpoints are 100% free and public

---

## 📋 Commands

| Command | Description | Example |
|---------|-------------|---------|
| `/start` | Welcome message + command list | `/start` |
| `/help` | All commands with examples | `/help` |
| `/evm` | Live block heights for all 24 EVM chains | `/evm` |
| `/l1` | Non-EVM chains: Solana, Bitcoin, TON, Starknet, Sui, Cosmos | `/l1` |
| `/status` | Quick ✅/❌ health check for all 30 chains | `/status` |
| `/node <chain>` | Full live stats for one chain | `/node ethereum` |
| `/ping <chain>` | Latency test for a single node | `/ping base` |
| `/chains` | Browse all 30 supported chains | `/chains` |
| `/search <name>` | Find a chain by name or symbol | `/search arb` |

### Chain name shortcuts

You can use short names with `/node` and `/ping`:

| Shortcut | Chain |
|----------|-------|
| `eth` | Ethereum |
| `bnb` / `bsc` | BNB Chain |
| `poly` / `matic` | Polygon |
| `arb` | Arbitrum |
| `op` | Optimism |
| `avax` | Avalanche |
| `sol` | Solana |
| `btc` | Bitcoin |
| `atom` | Cosmos |
| `strk` / `stark` | Starknet |

---

## 💬 Example Interactions

### `/evm` — All EVM chains live
```
⚙️ EVM Chains — Live Block Heights

🟢 🔵 Ethereum   — block #25,261,607  (42ms)
🟢 🟡 BNB Chain  — block #102,734,963 (38ms)
🟢 🟣 Polygon    — block #88,055,404  (51ms)
🟢 🔷 Base       — block #46,999,373  (44ms)
🟢 🌀 Arbitrum   — block #470,811,519 (39ms)
🟢 🔴 Optimism   — block #152,594,659 (47ms)
🟢 🔺 Avalanche  — block #87,357,097  (55ms)
...
✅ 24/24 online  |  publicnode.com
```

### `/l1` — Non-EVM chains
```
🌐 Non-EVM Chains — Live Stats

🟢 🟣 Solana  (SOL)  — Block height  424,775,368  (34ms)
🟢 🟠 Bitcoin (BTC)  — Block height  952,658      (45ms)
🟢 💎 TON     (TON)  — Master seqno  71,674,929   (52ms)
🟢 ⭐ Starknet(STRK) — Block         10,552,413   (61ms)
🟢 💧 Sui     (SUI)  — Checkpoint    283,994,809  (58ms)
🟢 ⚛️ Cosmos  (ATOM) — Block         31,462,242   (67ms)

✅ 6/6 online  |  publicnode.com
```

### `/node ethereum` — Full chain profile
```
🔵 Ethereum

📦 Latest Block: #25,261,607
⛽ Gas Price: 0.0712 Gwei
🔢 Chain ID: 1
💰 Native Token: ETH
🌐 RPC: https://ethereum-rpc.publicnode.com
🟢 Latency: 42ms

🔗 Open Explorer
```

### `/node bitcoin` — Bitcoin node
```
🟠 Bitcoin

📦 Block Height: 952,658
⚙️ Difficulty: 1.20e+14
💰 Token: BTC
🌐 RPC: https://bitcoin-rpc.publicnode.com
🟢 Latency: 45ms

🔗 Mempool.space
```

### `/node ton` — TON node
```
💎 TON

📦 Masterchain Seqno: 71,674,929
💰 Token: TON
🌐 API: https://mainnet-v4.tonhubapi.com
🟢 Latency: 52ms

🔗 TON Viewer
```

### `/ping arbitrum` — Latency test
```
🟢 Ping: 🌀 Arbitrum

🟢 Online — 39ms (Fast)
🌐 https://arbitrum-one-rpc.publicnode.com
```

### `/status` — All nodes health
```
🔍 RPC Status — All Chains

EVM Chains:
✅🔵Ethereum  ✅🟡BNB Chain  ✅🟣Polygon  ✅🔷Base  ✅🌀Arbitrum
✅🔴Optimism  ✅🔺Avalanche  ✅⬛Linea   ✅📜Scroll  ✅💥Blast ...

Non-EVM Chains:
✅ 🟣 Solana
✅ 🟠 Bitcoin
✅ 💎 TON
✅ ⭐ Starknet
✅ 💧 Sui
✅ ⚛️ Cosmos

30/30 nodes online
```

---

## 🌐 All 30 Supported Chains

### EVM Chains (24)

| # | Chain | RPC Endpoint | Chain ID | Symbol |
|---|-------|-------------|----------|--------|
| 1 | 🔵 Ethereum | `https://ethereum-rpc.publicnode.com` | 1 | ETH |
| 2 | 🟡 BNB Chain | `https://bsc-rpc.publicnode.com` | 56 | BNB |
| 3 | 🟣 Polygon | `https://polygon-bor-rpc.publicnode.com` | 137 | MATIC |
| 4 | 🔷 Base | `https://base-rpc.publicnode.com` | 8453 | ETH |
| 5 | 🌀 Arbitrum | `https://arbitrum-one-rpc.publicnode.com` | 42161 | ETH |
| 6 | 🔴 Optimism | `https://optimism-rpc.publicnode.com` | 10 | ETH |
| 7 | 🔺 Avalanche | `https://avalanche-c-chain-rpc.publicnode.com` | 43114 | AVAX |
| 8 | ⬛ Linea | `https://linea-rpc.publicnode.com` | 59144 | ETH |
| 9 | 📜 Scroll | `https://scroll-rpc.publicnode.com` | 534352 | ETH |
| 10 | 💥 Blast | `https://blast-rpc.publicnode.com` | 81457 | ETH |
| 11 | 🦉 Gnosis | `https://gnosis-rpc.publicnode.com` | 100 | xDAI |
| 12 | 🌿 Celo | `https://celo-rpc.publicnode.com` | 42220 | CELO |
| 13 | 🌕 Moonbeam | `https://moonbeam-rpc.publicnode.com` | 1284 | GLMR |
| 14 | 🏛 Metis | `https://metis-rpc.publicnode.com` | 1088 | METIS |
| 15 | 🟨 opBNB | `https://opbnb-rpc.publicnode.com` | 204 | BNB |
| 16 | 💓 PulseChain | `https://pulsechain-rpc.publicnode.com` | 369 | PLS |
| 17 | ⚙️ Mantle | `https://mantle-rpc.publicnode.com` | 5000 | MNT |
| 18 | 🥁 Taiko | `https://taiko-rpc.publicnode.com` | 167000 | ETH |
| 19 | 🐻 Berachain | `https://berachain-rpc.publicnode.com` | 80094 | BERA |
| 20 | 🌊 Soneium | `https://soneium-rpc.publicnode.com` | 1868 | ETH |
| 21 | 🦄 Unichain | `https://unichain-rpc.publicnode.com` | 130 | ETH |
| 22 | ⬜ Fraxtal | `https://fraxtal-rpc.publicnode.com` | 252 | frxETH |
| 23 | 🌶 Chiliz | `https://chiliz-rpc.publicnode.com` | 88888 | CHZ |
| 24 | ⚡ Sonic | `https://sonic-rpc.publicnode.com` | 146 | S |

### Non-EVM Chains (6)

| # | Chain | Endpoint | Protocol | Symbol |
|---|-------|----------|----------|--------|
| 1 | 🟣 Solana | `https://solana-rpc.publicnode.com` | JSON-RPC | SOL |
| 2 | 🟠 Bitcoin | `https://bitcoin-rpc.publicnode.com` | JSON-RPC 1.0 | BTC |
| 3 | 💎 TON | `https://mainnet-v4.tonhubapi.com` | REST API | TON |
| 4 | ⭐ Starknet | `https://starknet-rpc.publicnode.com` | JSON-RPC | STRK |
| 5 | 💧 Sui | `https://sui-rpc.publicnode.com` | JSON-RPC | SUI |
| 6 | ⚛️ Cosmos | `https://cosmos-rest.publicnode.com` | REST API | ATOM |

---

## 🚀 Deploy to Vercel (5 minutes)

### 1. Create a Telegram bot
1. Open [@BotFather](https://t.me/BotFather) in Telegram
2. Send `/newbot` and follow the prompts
3. Copy the bot token

### 2. Deploy
[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/Lord1Egypt/rpc-radar-bot)

Or manually:
```bash
git clone https://github.com/Lord1Egypt/rpc-radar-bot
cd rpc-radar-bot
vercel deploy --prod
```

### 3. Add environment variable
In Vercel → Settings → Environment Variables:

| Variable | Value |
|----------|-------|
| `BOT_TOKEN` | Your bot token from @BotFather |

> ✅ **No other API keys needed.** All RPC endpoints are free and public.

### 4. Set webhook
Open your deployment URL in a browser (e.g. `https://your-bot.vercel.app`) and click **Set Webhook**.

Or via curl:
```bash
curl "https://api.telegram.org/bot<YOUR_TOKEN>/setWebhook?url=https://your-bot.vercel.app/webhook"
```

### 5. Start the bot
Send `/start` to your bot in Telegram. Done! 🎉

---

## 🔧 Local Development

```bash
git clone https://github.com/Lord1Egypt/rpc-radar-bot
cd rpc-radar-bot
pip install -r requirements.txt

export BOT_TOKEN=your_token_here
python api/index.py
```

Then set the webhook to your local tunnel (e.g. ngrok):
```bash
ngrok http 5000
# then set webhook to: https://xxxx.ngrok.io/webhook
```

---

## 📡 RPC Usage Examples (curl)

All endpoints are standard JSON-RPC — no authentication needed:

```bash
# Ethereum — latest block
curl -X POST https://ethereum-rpc.publicnode.com \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"eth_blockNumber","params":[]}'

# Polygon — chain ID
curl -X POST https://polygon-bor-rpc.publicnode.com \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"eth_chainId","params":[]}'

# Arbitrum — gas price
curl -X POST https://arbitrum-one-rpc.publicnode.com \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"eth_gasPrice","params":[]}'

# Solana — block height
curl -X POST https://solana-rpc.publicnode.com \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"getBlockHeight","params":[]}'

# Bitcoin — block count
curl -X POST https://bitcoin-rpc.publicnode.com \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"1.0","id":1,"method":"getblockcount","params":[]}'

# TON — latest masterchain block
curl https://mainnet-v4.tonhubapi.com/block/latest

# Starknet — block number
curl -X POST https://starknet-rpc.publicnode.com \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"starknet_blockNumber","params":[]}'

# Sui — latest checkpoint
curl -X POST https://sui-rpc.publicnode.com \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"sui_getLatestCheckpointSequenceNumber","params":[]}'

# Cosmos — latest block (REST)
curl https://cosmos-rest.publicnode.com/cosmos/base/tendermint/v1beta1/blocks/latest
```

---

## 🏗 Architecture

```
Telegram User
     │
     ▼
Vercel Serverless Function (Python/Flask)
     │
     ├─ /evm, /status ──► ThreadPoolExecutor (30 parallel requests)
     │                         │
     │                    ┌────┴────────────────────────────────────┐
     │                    ▼                                         ▼
     │              EVM JSON-RPC                         Non-EVM APIs
     │         (eth_blockNumber)                  (Solana/Bitcoin/TON/etc.)
     │
     └─ /node, /ping ──► Single targeted request → response
```

**Key design decisions:**
- All `/evm` and `/status` calls use `ThreadPoolExecutor` — 24+ chains queried in parallel, total latency ~1s
- 30s Vercel function timeout (configured in `vercel.json`) — enough for parallel fetches
- Latency color-coding: 🟢 <200ms · 🟡 <600ms · 🔴 600ms+
- Chain aliases (`eth`, `sol`, `btc`, etc.) for fast command typing
- Zero external API keys — all endpoints are public and free

---

## 📁 Project Structure

```
rpc-radar-bot/
├── api/
│   ├── __init__.py      # Required by Vercel Python runtime
│   └── index.py         # Main Flask app — all bot logic
├── requirements.txt     # Flask + requests
├── runtime.txt          # python-3.11
├── vercel.json          # Vercel build + routing config
└── README.md
```

---

## 🤝 Related Projects

| Project | Description |
|---------|-------------|
| [TG-EthExplorer-Bot](https://github.com/Lord1Egypt/TG-EthExplorer-Bot) | Deep Ethereum block/tx/address explorer (same author) |
| [ethsmith](https://github.com/Lord1Egypt/ethsmith) | Local Ethereum dev node — Ganache replacement (same author) |
| [publicnode.com](https://publicnode.com) | Free public RPC nodes for 50+ chains |

---

<p align="center">Made with ❤️ by <a href="https://github.com/Lord1Egypt">Lord1Egypt</a></p>
