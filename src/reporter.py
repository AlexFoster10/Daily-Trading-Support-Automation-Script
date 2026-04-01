
import datetime

def generate_report(txt = ""):
    msg = txt
    important = []
    keep_phrases = ["WARNING", 
            "ERROR",
            "important",
            "arrived",
            "Dropped",
            "RESULT"]
    with open("mainLog.log", "r") as f:
        for line in f:
            if any(phrase in line for phrase in keep_phrases):
                important.append(line)
    msg = msg.join(important)
    with open(f"reports/report_{datetime.datetime.now().strftime('%Y%m%d')}.txt", "w") as f:
        f.write(msg)
    return msg