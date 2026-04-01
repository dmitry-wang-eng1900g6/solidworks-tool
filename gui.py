#!/usr/bin/env python3
"""solidworks-tool GUI — visual updater for solidworks."""
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
import logging

log = logging.getLogger(__name__)

class GUI:
 def __init__(self):
 self.root = tk.Tk()
 self.root.title("solidworks-tool")
 self.root.geometry("500x400")
 self.root.resizable(False, False)

 # Header
 ttk.Label(self.root, text="solidworks-tool", font=("Arial", 16, "bold")).pack(pady=10)
 ttk.Label(self.root, text="Solidworks Configuion Tool").pack()

 # Status
 self.status_var = tk.StringVar(value="Ready")
 ttk.Label(self.root, textvariable=self.status_var, font=("Arial", 10)).pack(pady=5)

 # Log area
 self.log_area = scrolledtext.ScrolledText(self.root, height=12, width=60, state="disabled")
 self.log_area.pack(padx=10, pady=5)

 # Buttons
 btn_frame = ttk.Frame(self.root)
 btn_frame.pack(pady=10)
 ttk.Button(btn_frame, text="Detect", command=self._detect).pack(side="left", padx=5)
 ttk.Button(btn_frame, text="update", command=self._).pack(side="left", padx=5)
 ttk.Button(btn_frame, text="Rollback", command=self._rollback).pack(side="left", padx=5)
 ttk.Button(btn_frame, text="Exit", command=self.root.quit).pack(side="left", padx=5)

 # Progress
 self.progress = ttk.Progressbar(self.root, mode="indeterminate", length=460)
 self.progress.pack(padx=10, pady=5)

 def _log(self, msg: str):
 self.log_area.configure(state="normal")
 self.log_area.insert("end", msg + "\n")
 self.log_area.see("end")
 self.log_area.configure(state="disabled")

 def _detect(self):
 self.status_var.set("Detecting...")
 self.progress.start()
 def _run():
 try:
 from config import load_config
 from detector import detect_installation
 cfg = load_config()
 path = detect_installation(cfg)
 if path:
 self._log(f"[✓] Found: {path}")
 self.status_var.set("Detected")
 else:
 self._log("[✗] Not found")
 self.status_var.set("Not found")
 except Exception as e:
 self._log(f"[✗] Error: {e}")
 self.progress.stop()
 threading.Thread(target=_run, daemon=True).start()

 def _(self):
 self.status_var.set("utility...")
 self.progress.start()
 def _run():
 try:
 from config import load_config
 from detector import detect_installation
 from updater import apply_
 cfg = load_config()
 path = detect_installation(cfg)
 if path and apply_(path, cfg):
 self._log("[✓] update applied successfully")
 self.status_var.set("Updated")
 else:
 self._log("[✗] update failed")
 self.status_var.set("Failed")
 except Exception as e:
 self._log(f"[✗] Error: {e}")
 self.progress.stop()
 threading.Thread(target=_run, daemon=True).start()

 def _rollback(self):
 self.status_var.set("Rolling back...")
 def _run():
 try:
 from config import load_config
 from detector import detect_installation
 from updater import rollback
 cfg = load_config()
 path = detect_installation(cfg)
 if path and rollback(path):
 self._log("[✓] Rollback complete")
 self.status_var.set("Restored")
 else:
 self._log("[✗] Rollback failed")
 except Exception as e:
 self._log(f"[✗] Error: {e}")
 threading.Thread(target=_run, daemon=True).start()

 def run(self):
 self.root.mainloop()

if __name__ == "__main__":
 logging.basicConfig(level=logging.INFO)
 GUI().run()
