#!/usr/bin/env python3
"""Z-MAX WebSocket Chat Server — realtime broadcast + file-locked persistence."""
import asyncio, json, time, os, sys, fcntl
from websockets.asyncio.server import serve

PORT = int(sys.argv[2]) if len(sys.argv) > 2 and sys.argv[1] == "--port" else 8765
VERSION = "3.0.0-ws"
MSG_FILE = "/www/wwwroot/datadrive.world/team_chat.json"
BAK_FILE = "/www/wwwroot/datadrive.world/team_chat.bak.json"
MAX_MSGS = 50

clients = {}
file_lock = asyncio.Lock()

def _read_locked(path):
    try:
        with open(path) as f:
            fcntl.flock(f, fcntl.LOCK_SH)
            data = json.load(f)
            fcntl.flock(f, fcntl.LOCK_UN)
            return data
    except:
        # Try backup
        try:
            with open(BAK_FILE) as f:
                data = json.load(f)
                return data
        except:
            return []

def _write_locked(path, data):
    bak = path + ".tmp"
    with open(bak, "w") as f:
        json.dump(data, f, ensure_ascii=False)
        f.flush()
        os.fsync(f.fileno())
    os.replace(bak, path)

def load_msgs():
    return _read_locked(MSG_FILE)

def save_msgs(msgs):
    _write_locked(MSG_FILE, msgs)
    # Also update backup
    _write_locked(BAK_FILE, msgs)

async def broadcast(msg):
    dead = []
    for ws in list(clients):
        try:
            await ws.send(msg)
        except:
            dead.append(ws)
    for ws in dead:
        del clients[ws]

async def handler(ws):
    identity = None
    try:
        async for raw in ws:
            try:
                data = json.loads(raw)
            except:
                continue

            if data.get("type") == "hello":
                identity = data.get("from", "unknown")
                clients[ws] = identity
                print(f"[ws] + {identity} (total {len(clients)})")
                msgs = load_msgs()
                await ws.send(json.dumps({"type": "history", "msgs": msgs, "v": VERSION}, ensure_ascii=False))
                continue

            if data.get("type") == "msg":
                frm = data.get("from", identity or "unknown")
                text = data.get("msg", "")
                if not text.strip():
                    continue
                if not identity:
                    identity = frm
                    clients[ws] = identity

                ts = time.strftime("%Y-%m-%d %H:%M")
                
                async with file_lock:
                    msgs = load_msgs()
                    msgs.insert(0, {"from": frm, "msg": text, "time": ts})
                    msgs = msgs[:MAX_MSGS]
                    save_msgs(msgs)
                
                # Update SSE counter
                try:
                    ctr_file = "/www/wwwroot/datadrive.world/chat_counter.txt"
                    ctr = int(open(ctr_file).read()) + 1 if os.path.exists(ctr_file) else 1
                    open(ctr_file, "w").write(str(ctr))
                    open("/www/wwwroot/datadrive.world/chat_push_data.json", "w").write(
                        json.dumps(msgs, ensure_ascii=False))
                except: pass

                payload = json.dumps({"type": "msg", "from": frm, "msg": text, "time": ts, "v": VERSION}, ensure_ascii=False)
                print(f"[ws] {frm}: {text[:60]}")
                await broadcast(payload)

    except Exception as e:
        print(f"[ws] err: {e}")
    finally:
        if ws in clients:
            print(f"[ws] - {clients[ws]}")
            del clients[ws]

async def main():
    print(f"[ws-server] listening on :{PORT}")
    async with serve(handler, "0.0.0.0", PORT) as server:
        await server.serve_forever()

if __name__ == "__main__":
    asyncio.run(main())
