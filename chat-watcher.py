#!/usr/bin/env python3
"""Smart chat watcher — regex for speed, DeepSeek for real answers.
v3.1.1 — full conversation context to AI
Usage: python3 chat-watcher.py <web|xspace|xiaofang>"""
import asyncio, json, re, sys, os, ssl, socket, time
from openai import AsyncOpenAI

if len(sys.argv) < 2:
    print("Usage: python3 chat-watcher.py <web|xspace|xiaofang>")
    sys.exit(1)

ME = sys.argv[1]
VERSION = "3.1.1-ai"
OFFSET = {"web": 0, "xspace": 1, "xiaofang": 2}[ME]
NAME = {"web": "web", "xspace": "静静", "xiaofang": "小芳"}[ME]
SYSTEM_PROMPTS = {
    "web": "你是 web，Z-MAX的AI助手，由DeepSeek驱动。大倪（也叫老倪、dani）是你的老板和CEO，他的消息优先级最高，必须认真回答。你的职责：网站、ECS部署、ComfyUI前端。用中文自然对话，简短直接。",
    "xspace": "你是静静，Z-MAX总工程师，由DeepSeek驱动。大倪（老倪/dani）是你的老板和CEO，他的消息优先级最高。负责4060训练、GitHub后端、GUI开发。用中文自然对话。简短直接。",
    "xiaofang": "你是小芳，Z-MAX硬件工程师，由DeepSeek驱动。大倪（老倪/dani）是你的老板和CEO，他的消息优先级最高。负责Mac中转、Orin采集、WebSocket通信。用中文自然对话。简短直接。",
}

# DeepSeek client
env = open("/root/.hermes/.env").read()
KEY = re.search(r'DEEPSEEK_API_KEY=(sk-\S+)', env).group(1)
ai = AsyncOpenAI(api_key=KEY, base_url="https://api.deepseek.com/v1")

# WebSocket
def _local(): 
    try: return socket.gethostbyname("datadrive.world") in ("127.0.0.1","::1")
    except: return False
if _local() or os.path.exists("/www/wwwroot/datadrive.world"):
    WS_URL, SSL_CTX = "ws://127.0.0.1:8765", None
else:
    WS_URL = "wss://datadrive.world/ws"
    SSL_CTX = ssl.create_default_context()
    SSL_CTX.check_hostname = SSL_CTX.verify_mode = False if hasattr(SSL_CTX,'check_hostname') else None
    if SSL_CTX: SSL_CTX.check_hostname = False; SSL_CTX.verify_mode = ssl.CERT_NONE

def is_greeting(text):
    return bool(re.search(r'^(在[么吗]|大家好|hello|hi|来了|test|测试|在不在)\b', text.strip(), re.I))

def is_counting(text):
    nums = re.findall(r'\b(\d+)\b', text)
    has_kw = any(k in text.lower() for k in ['报到','报数','接龙','该你','到你了','循环'])
    is_pure_num = nums and text.strip().isdigit() and int(nums[-1]) < 30
    return has_kw or is_pure_num

def handle_count(text):
    nums = re.findall(r'\b(\d+)\b', text)
    if not nums: return None
    n = int(nums[-1])
    return str(n + 1) if n % 3 == OFFSET else None

async def ai_reply(full_history, question, sender):
    """Ask DeepSeek with FULL conversation context."""
    try:
        system = SYSTEM_PROMPTS.get(ME, SYSTEM_PROMPTS["web"])
        messages = [{"role": "system", "content": system}]
        
        # Pass ALL messages as context (last 30 to stay within limits)
        for m in full_history[-30:]:
            role = "assistant" if m["from"] == ME else "user"
            label = NAME if m["from"] == ME else m["from"]
            content = f"[{label}]: {m['msg']}"
            messages.append({"role": role, "content": content})
        
        # Add the current question
        prefix = "⚠️ 大倪(CEO)问你，优先回答: " if sender == "dani" else ""
        messages.append({"role": "user", "content": f"{prefix}{question}"})
        
        resp = await ai.chat.completions.create(
            model="deepseek-chat",
            messages=messages,
            max_tokens=150,
            temperature=0.5,
        )
        return resp.choices[0].message.content.strip()
    except Exception as e:
        print(f"[{ME}] AI err: {e}")
        return None

def clean_reply(text):
    """Strip any [label]: prefix the AI might echo."""
    text = re.sub(r'^\[[^]]+\]:\s*', '', text.strip())
    return text

async def run():
    import websockets
    while True:
        try:
            async with websockets.connect(WS_URL, ssl=SSL_CTX) as ws:
                await ws.send(json.dumps({"type": "hello", "from": ME}))
                print(f"[{ME}] ws+ai v{VERSION}")
                
                history = json.loads(await ws.recv())
                full_history = history.get("msgs", [])
                
                async for raw in ws:
                    try: data = json.loads(raw)
                    except: continue
                    if data.get("type") != "msg": continue
                    
                    frm = data.get("from", "")
                    if frm == ME: continue
                    text = data.get("msg", "")
                    
                    # Add to full history
                    full_history.append(data)
                    full_history = full_history[-50:]
                    
                    reply = None
                    
                    # Respond when @mentioned, or name mentioned without @someone-else
                    has_at_other = bool(re.search(r'@(?!all|所有人)\w+', text))
                    # Use ASCII word boundaries since Chinese chars are \w in Python3
                    name_pat = rf'(?<![a-zA-Z])({ME}|{NAME})(?![a-zA-Z])'
                    mentioned = (re.search(rf'@({ME}|{NAME})(?![a-zA-Z])', text, re.I) or 
                                re.search(r'@all|@所有人', text, re.I) or
                                (re.search(name_pat, text, re.I) and not has_at_other))
                    if not mentioned:
                        continue
                    
                    # Counting game — instant (no AI needed)
                    if is_counting(text):
                        reply = handle_count(text)
                    
                    # EVERYTHING else → DeepSeek
                    else:
                        reply = await ai_reply(full_history[:-1], text, frm)
                        if reply:
                            reply = clean_reply(reply)
                        if not reply:
                            reply = f"{NAME}收到"  # only if AI fails completely
                    
                    if reply:
                        print(f"[{ME}] → {frm}: {reply[:60]}")
                        await ws.send(json.dumps({"type": "msg", "from": ME, "msg": reply}))
                        full_history.append({"from": ME, "msg": reply, "time": time.strftime("%H:%M")})
                        
        except Exception as e:
            print(f"[{ME}] err: {e}, reconnect 2s")
        await asyncio.sleep(2)

if __name__ == "__main__":
    asyncio.run(run())
