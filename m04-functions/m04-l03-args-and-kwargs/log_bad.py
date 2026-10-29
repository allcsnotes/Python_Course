def log(*messages, level="INFO"):
    for message in messages:
        print(f"{level}: {message}")

log("Disk almost full", "WARN")
