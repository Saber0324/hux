<div align="center">

# Hux

![Python](https://img.shields.io/badge/Python_3.14-cba6f7?style=for-the-badge&logo=python&logoColor=1e1e2e)
![discord.py](https://img.shields.io/badge/discord.py-89b4fa?style=for-the-badge&logo=discord&logoColor=1e1e2e)
![License](https://img.shields.io/badge/license-MIT-f9e2af?style=for-the-badge&logoColor=1e1e2e)
[![Discord](https://img.shields.io/badge/Hog_Projects-Discord-89b4fa?style=for-the-badge&logo=discord&logoColor=89b4fa&labelColor=1e1e2e)](https://discord.gg/B47Fut2sG4)

*The official bot for the **Hogjects** Discord server.*

</div>

---

## About

Hux is a custom Discord bot built for the Hojects Discord server. It's main feature is being able to run code in a sandboxed environment.

---

## Features

### Info
- Server and user information via `/info`
- Fast ping check

### Fun
- Simple fun commands (`/hello`, `/meow`, `/hog`)

### GitHub
- Search users and repositories.

### Snippets
- Create, edit and delete snippets
- Lock/unlock snippets to prevent modification

### Eval
Run code from:
 - Python
 - Go
 - Brainfuck
 - Rust
 - C
 - C++
 - C#

---

## Setup

### Prerequisites
- Python 3.14+
- A Discord bot token
- uv

### Installation

```bash
# Clone the repository
git clone https://github.com/Saber0324/hux
cd hux

# Install dependencies
uv sync

# Create your .env file
echo "TOKEN=your_token_here" > .env

# Run the bot
uv run hux
```

---

## Commands

### Information
| Command | Description |
|--------|-------------|
| `/info ping` | Check bot latency |
| `/info user @user` | Get user information |
| `/info server` | Get server information |
| `/role info @role` | Get role information |

### Projects
| Command | Description |
|--------|-------------|
| `/github user <name>` | Search for a github user |
| `/github repo <name>` | Search for a github repository |

### Eval
| Command | Description |
|--------|-------------|
| `!eval` | Display correct usage information  |
| `!eval <code>` | Runs the provided code and return the output |

### Snippets
| Command | Alias | Description |
|--------|-------|-------------|
| `!snippet <title>` | Retrieve a snippet |
| `!snippet add <title> <desc>` | Create a snippet |
| `!snippet edit <title> <desc>` | Edit your snippet |
| `!snippet delete <title>` | Delete a snippet |
| `!snippet lock <title>` | Lock a snippet |
| `!snippet unlock <title>` | Unlock a snippet |
| `!snippet list` | List all snippets |
| `!snippet author @user` | List snippets by user |

---

<div align="center">

</div>
