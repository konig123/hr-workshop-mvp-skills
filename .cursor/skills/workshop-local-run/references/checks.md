# Checks and commands

Agent runs these. Explain first. Ask permission before any command that installs or starts a long process.

Prefer workspace-relative `cd`. Paths may contain spaces, CJK, or a curly apostrophe — quote them.

## Detect OS (read-only)

```bash
uname -s
```

- `Darwin` → macOS
- `Linux` plus `grep -qi microsoft /proc/version` success → WSL
- `Linux` otherwise → Linux
- `uname` missing (cmd.exe): treat as Windows. Confirm with `echo %OS%`

Ask the student which computer only if this is inconclusive.

## Admin (read-only, never prompt for a password)

macOS / Linux / WSL:

```bash
sudo -n true
```

Exit 0 → passwordless sudo. Otherwise treat as no-admin for installs.

Windows (cmd):

```bat
net session >nul 2>&1
```

Exit 0 → admin. Otherwise no-admin.

Never pipe a password. Never ask them to paste it in chat.

## Folder (read-only)

```bash
pwd
```

Next.js app folder = directory that contains `package.json` with a `"dev"` script.

```bash
test -f package.json && node -e "const p=require('./package.json'); process.exit(p.scripts && p.scripts.dev ? 0 : 1)"
```

If `projectDir` is known (Group 6: `talent-mapping-next`), look for it under `pwd` without asking the student to `cd`:

```bash
find . -name package.json -not -path '*/node_modules/*' | head
```

Then `cd` to that directory yourself after permission if you will run `npm`.

HTML: find a workshop `.html` the product skill just created or named. Do not open a random `node_modules` HTML.

## Node (read-only)

```bash
command -v node; node -v
command -v npm; npm -v
```

Need Node 20 or newer for Next.js. Missing command or major < 20 → class `Missing Node`.

HTML-only preflight/repair does not require Node.

## Dev server already running (read-only)

macOS / Linux / WSL:

```bash
lsof -nP -iTCP:3000 -sTCP:LISTEN
lsof -nP -iTCP:3001 -sTCP:LISTEN
```

If either listens, class `Port in use`. Reuse that URL. Do not start another `npm run dev`.

Also check Cursor terminal metadata for an existing `npm run dev` before starting one.

## Install Node — macOS, admin

After permission. Prefer the official LTS pkg from `https://nodejs.org` (LTS 20 or 22).

If `brew` already exists, Agent may run `brew install node@20` — do not install Homebrew first.

Then open a **new** shell and re-run `node -v`.

## Install Node — macOS / Linux, no admin (user-level nvm)

After permission:

```bash
export NVM_DIR="$HOME/.nvm"
if [ ! -s "$NVM_DIR/nvm.sh" ]; then
  curl -fsSL https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.3/install.sh | bash
fi
. "$NVM_DIR/nvm.sh"
nvm install 20
nvm use 20
node -v
```

If curl/nvm/install fails → class `No admin / company-locked`. Stop.

## Install Node — Windows

After permission. Download the LTS installer from `https://nodejs.org`. Choose **Install for me only** / current user if the installer offers it.

If the installer demands admin and the student cannot approve → class `No admin / company-locked`. Stop.

After install, start a **new** terminal. Re-check `node -v`.

## npm install (Next.js, after permission)

Must already be in the folder with `package.json`.

```bash
npm install
```

Network failure → class `Network / proxy`. Explain. Do not change product code. Do not retry forever.

## Start Next.js (after permission; skip if already listening)

```bash
npm run dev
```

Read the log for `Local:` and the port. Never leave an interactive menu hanging.

## Open HTML

macOS:

```bash
open "/absolute/path/to/file.html"
```

Windows:

```bat
start "" "C:\absolute\path\to\file.html"
```

WSL: `wslview` if present, else tell the student the `/mnt/c/...` path converted to `C:\...` and open via `explorer.exe`.

## Open Next.js page

macOS:

```bash
open "http://localhost:3000/login"
```

Replace port and `successPath` from the actual log and caller handshake.

Windows:

```bat
start http://localhost:3000/login
```
