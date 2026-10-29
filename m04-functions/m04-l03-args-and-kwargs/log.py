def log(*messages, level="INFO"):
    for message in messages:
        print(f"{level}: {message}")

log("Server started")
log("Disk almost full", "90% used", level="WARN")
