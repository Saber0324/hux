import discord
from discord.ext import commands
import subprocess
import asyncio
import functools
from time import time as currenttime


class Eval(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["e"])
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def eval(self, ctx: commands.Context, *, code: str | None = None) -> None:
        if code is None:
            await ctx.send(
                "Correct usage: \n\n"
                + r"\`\`\`py/go/bf"
                + "\n"
                + "<code here>"
                + "\n"
                + r"\`\`\` [stdin if brainf**k]"
            )
            return
        elif code.startswith("```py"):
            loop = asyncio.get_event_loop()
            docker_sub = await loop.run_in_executor(
                None, functools.partial(run_python, code)
            )
        elif code.startswith("```go"):
            loop = asyncio.get_event_loop()
            docker_sub = await loop.run_in_executor(
                None, functools.partial(run_go, code)
            )
        elif code.startswith("```bf"):
            bfinput = code[code.find("\n```")+4:]
            if bfinput.startswith(" "):
                bfinput = bfinput[1:]
            if bfinput == code[3:]:
                bfinput = ""
            loop = asyncio.get_event_loop()
            docker_sub = await loop.run_in_executor(
                None, functools.partial(run_bf, code, bfinput))
        else:
            await ctx.send("Please, use the proper formatting.")
            return

        output = docker_sub.stdout
        if docker_sub.stderr:
            output += f"\nstderr: {docker_sub.stderr}"
        if len(output) >= 500:
            output = f"{output[:500]} \n\nOutput limited to 500 characters."
        else:
            output = output or "(No output)"
        await ctx.send(
            f"Your code returned with code: {docker_sub.returncode}. ```\n{output}\n```",
            allowed_mentions=discord.AllowedMentions.none(),
        )


def run_python(code: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [
            "docker",
            "run",
            "--network",
            "none",
            "--rm",
            "--memory=50m",
            "--memory-swap=50m",
            "--cpus=0.5",
            "--security-opt",
            "no-new-privileges",
            "--read-only",
            "--tmpfs",
            "/tmp:size=50m,noexec",
            "--tmpfs",
            "/dev/shm:size=10m,noexec,nosuid",
            "--user",
            "1000:1000",
            "--pids-limit",
            "50",
            "--cap-drop",
            "all",
            "python:3.12-slim",
            "timeout",
            "15",
            "python",
            "-c",
            f"{code[6:-3]}",
        ],
        capture_output=True,
        text=True,
        timeout=20,
    )


def run_go(code: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [
            "docker",
            "run",
            "--network",
            "none",
            "--rm",
            "--memory=512m",
            "--memory-swap=513m",
            "--cpus=2",
            "--security-opt",
            "no-new-privileges",
            "--tmpfs",
            "/tmp:size=200m,exec",
            "--tmpfs",
            "/dev/shm:size=10m,noexec,nosuid",
            "--user",
            "1000:1000",
            "--pids-limit",
            "100",
            "--cap-drop",
            "all",
            "-e",
            "HOME=/tmp",
            "-e",
            "GOCACHE=/tmp/go-cache",
            "-e",
            "GOPATH=/tmp/gopath",
            "-i",
            "golang:alpine",
            "timeout",
            "45",
            "/bin/sh",
            "-c",
            "cat > /tmp/code.go && go run /tmp/code.go",
        ],
        input=code[6:-3],
        capture_output=True,
        text=True,
        timeout=50,
    )

def run_bf(code: str, bfinput: str) -> subprocess.CompletedProcess[str]:
    starttime = currenttime()
    cells = bytearray(30000) # Memory (30kb)
    bfinput += "\0" # Add a null character to the end of the input
    inputptr = 0 # Pointer that points to a character in the input 
    dp = 0 # Data pointer
    
    stack = [] # Bracket nest stack
    jump = [None]*len(code) # Jump table
    ip = 0 # Instruction pointer
    output = "" # Output
    status = subprocess.CompletedProcess(bfinput, 0, "", "")

    if code.count("[") != code.count("]"):
        status.stderr = "Brackets are unbalanced"
        status.returncode = 1

    # totally not taken from https://stackoverflow.com/a/3041005
    if status.returncode == 0:
        for i,o in enumerate(code):
            if o=='[':
                stack.append(i)
            elif o==']':
                if len(stack) == 0:
                    status.stderr = "Brackets are unbalanced"
                    status.returncode = 1
                    break
                else:
                    jump[i] = stack.pop()
                jump[jump[i]] = i

    while ip < len(code) and status.returncode == 0:
        match code[ip]:
            case "+":
                cells[dp] = (cells[dp] + 1) % 256
            case "-":
                cells[dp] = (cells[dp] - 1) % 256
            case ">":
                dp+=1
                if dp < -1 or dp > 29999:
                    dp -= 30000
            case "<":
                dp-=1
                if dp < -1 or dp > 29999:
                    dp += 30000
            case ".":
                output += chr(cells[dp])
            case ",":
                cells[dp] = ord(bfinput[inputptr])
                inputptr += 1
            case "[":
                if not cells[dp]:
                    ip = jump[ip]
            case "]":
                if cells[dp]:
                    ip = jump[ip]
                    continue
        ip+=1
        if currenttime() - starttime > 30:
            status.returncode = 124
            break
    status.stdout = output
    return status

async def setup(bot) -> None:
    await bot.add_cog(Eval(bot))
