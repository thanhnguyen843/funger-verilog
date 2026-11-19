import sys
import os
import time
import subprocess
import threading
import msvcrt

# Ensure UTF-8 output and ANSI virtual terminal support on Windows
if os.name == 'nt':
    try:
        import ctypes
        kernel32 = ctypes.windll.kernel32
        hOut = kernel32.GetStdHandle(-11)
        mode = ctypes.c_ulong()
        if kernel32.GetConsoleMode(hOut, ctypes.byref(mode)):
            kernel32.SetConsoleMode(hOut, mode.value | 0x0004)
        kernel32.SetConsoleOutputCP(65001)
        kernel32.SetConsoleCP(65001)
    except Exception:
        pass

import codecs

def stream_output(process):
    decoder = codecs.getincrementaldecoder('utf-8')(errors='replace')
    try:
        while True:
            chunk = process.stdout.read(64)
            if not chunk:
                break
            text = decoder.decode(chunk)
            if text:
                sys.stdout.write(text)
                sys.stdout.flush()
    except Exception:
        pass

def main():
    # Allow specifying target binary via CLI argument
    if len(sys.argv) > 1 and os.path.exists(sys.argv[1]):
        sim_binary = sys.argv[1]
    else:
        # Default priority: funger_play.out -> battle_top.out
        p1 = os.path.join(os.path.dirname(__file__), "sim", "funger_play.out")
        p2 = os.path.join(os.path.dirname(__file__), "sim", "battle_top.out")
        sim_binary = p1 if os.path.exists(p1) else p2

    if not os.path.exists(sim_binary):
        print(f"[ERROR] Simulation binary not found at: {sim_binary}")
        return 1

    process = subprocess.Popen(
        ["vvp", sim_binary],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        bufsize=0
    )

    t = threading.Thread(target=stream_output, args=(process,), daemon=True)
    t.start()

    is_interactive = sys.stdin.isatty()
    last_key_time = 0.0

    try:
        while process.poll() is None:
            if is_interactive:
                if msvcrt.kbhit():
                    ch = msvcrt.getch()
                    now = time.time()
                    if ch in (b'\x00', b'\xe0'):
                        ext = msvcrt.getch()
                        if ext == b'H':    # Up Arrow -> 'w'
                            cmd = b'w\n'
                        elif ext == b'P':  # Down Arrow -> 's'
                            cmd = b's\n'
                        elif ext == b'K':  # Left Arrow -> 'a'
                            cmd = b'a\n'
                        elif ext == b'M':  # Right Arrow -> 'd'
                            cmd = b'd\n'
                        else:
                            continue
                        last_key_time = now
                    elif ch in (b'\r', b'\n'):  # Enter Key
                        # If Enter is pressed right after a character key (< 0.2s), it's the trailing Enter of that key
                        if (now - last_key_time) < 0.2:
                            continue
                        # Independent Enter (e.g., Press [C] or Enter to continue / confirm)
                        cmd = b'c\n'
                        last_key_time = now
                    elif ch == b' ':       # Space Bar -> Confirm / Continue ('c')
                        cmd = b'c\n'
                        last_key_time = now
                    elif ch == b'\x1b':    # Escape -> Cancel / Return ('c')
                        cmd = b'c\n'
                        last_key_time = now
                    elif ch == b'\x03':    # Ctrl+C -> Exit
                        break
                    else:
                        cmd = ch + b'\n'
                        last_key_time = now

                    if process.stdin:
                        try:
                            process.stdin.write(cmd)
                            process.stdin.flush()
                        except (BrokenPipeError, OSError):
                            break
                else:
                    threading.Event().wait(0.01)
            else:
                # Redirected or piped stdin
                line = sys.stdin.readline()
                if not line:
                    break
                if process.stdin:
                    process.stdin.write(line.encode('utf-8'))
                    process.stdin.flush()
    except KeyboardInterrupt:
        pass
    finally:
        if process.poll() is None:
            process.terminate()
        process.wait()
        try:
            t.join(timeout=1.0)
        except Exception:
            pass

    return 0

if __name__ == "__main__":
    sys.exit(main())
