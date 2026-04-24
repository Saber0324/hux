<div align="center">

# 🤖 HuxBot

![Python](https://img.shields.io/badge/Python_3.14-cba6f7?style=for-the-badge&logo=python&logoColor=1e1e2e)
![discord.py](https://img.shields.io/badge/discord.py-89b4fa?style=for-the-badge&logo=discord&logoColor=1e1e2e)
![License](https://img.shields.io/badge/license-MIT-f9e2af?style=for-the-badge&logoColor=1e1e2e)
[![Discord](https://img.shields.io/badge/Hog_Projects-Discord-89b4fa?style=for-the-badge&logo=discord&logoColor=89b4fa&labelColor=1e1e2e)](https://discord.gg/B47Fut2sG4)

*The official bot for the **Hog Projects** Discord server.*

</div>

---

## 📖 About

HuxBot is a custom Discord bot built for the Hog Projects server. It handles moderation, server info, fun interactions, project tracking, and a persistent snippet system.

---

## ✨ Features

### 🛡️ Moderation
- Kick, timeout and untimeout members
- Role management (`add` / `remove`)
- Warning system

### ℹ️ Info
- Server, user and role information via `!info`
- Fast ping check

### 🎉 Fun
- Simple fun commands (`!hello`, `!meow`, `!hog`)

### 📁 Projects
- List active projects and their repositories
- Fetch latest releases

### 📝 Snippets
A full persistent snippet system:
- Create, edit and delete snippets
- Lock/unlock snippets to prevent modification
- List all snippets or filter by author


---

## 🚀 Setup

### Prerequisites
- Python 3.14+
- A Discord bot token

### Installation

```bash
# Clone the repository
git clone https://github.com/Saber0324/projects-bot
cd projects-bot

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create your .env file
echo "TOKEN=your_token_here" > .env

# Run the bot
python main.py
```

---

## 📜 Commands

### General
| Command | Description |
|--------|-------------|
| `!ping` | Check bot latency |
| `!info user @user` | Get user information |
| `!info server` | Get server information |
| `!info role @role` | Get role information |

### Fun
| Command | Description |
|--------|-------------|
| `!hello` | Say hello |
| `!meow` | Meow back |
| `!hog` | All hail |
| `!say <text>` | Make the bot say something |

### Moderation
| Command | Description |
|--------|-------------|
| `!kick @user [reason]` | Kick a member |
| `!timeout @user <minutes> [reason]` | Timeout a member |
| `!untimeout @user` | Remove timeout |
| `!role add @user role` | Add a role |
| `!role remove @user role` | Remove a role |
| `!warn @user`| Warns an user |
| `!warn list @user` | Displays all warns from an user|
| `!warn delete <warn id>` | Deletes a warn |

### Projects
| Command | Description |
|--------|-------------|
| `!projects list` | List all projects |
| `!projects release <name>` | Get latest release link |

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

## 🗂️ Project Structure

```
projects-bot/
├── main.py
├── templates
│   └── models.py
├── data/
│   ├── database.py
│   └── bot.db
└──cogs/
    ├── info.py
    ├── moderation.py
    ├── fun.py
    ├── projects.py
    └── snippets.py 
```

---

## 🛠️ Tech Stack

- **Runtime:** Python 3.14
- **Bot Framework:** discord.py
- **Database:** SQLite via aiosqlite
- **Environment:** python-dotenv
---

<div align="center">

*Made with 🩷 for Hog Projects*

</div>
