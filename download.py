import subprocess
import json
import sys
import logging
from datetime import datetime

# === Konfigurasi ===
LOG_LEVEL = "DEBUG"
TAHUN = "2025"
OUTPUT_FORMAT = "json"
JSON_INPUT_FILE = "lpse_list.json"
SCRIPT_PATH = "scripts/downloader.py"
LOG_FILE = f"run_downloader_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

# === Inisialisasi Logging ===
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format='[%(asctime)s] %(levelname)s: %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
        logging.StreamHandler(sys.stdout)
    ]
)

def baca_domain_dari_file(json_file):
    try:
        with open(json_file, "r", encoding="utf-8") as file:
            data = json.load(file)
        domain_list = [
            entry["link_website"].strip().rstrip("/")
            for entry in data
            if "link_website" in entry and entry["link_website"].startswith("http")
        ]
        logging.info(f"Ditemukan {len(domain_list)} domain LPSE yang valid di '{json_file}'.")
        return domain_list
    except Exception as e:
        logging.error(f"Gagal membaca atau memproses file '{json_file}': {e}")
        sys.exit(1)

def jalankan_downloader(doms):
    if not doms:
        logging.warning("Tidak ditemukan domain LPSE yang valid. Proses dibatalkan.")
        sys.exit(0)

    cmd = [
        "python3", SCRIPT_PATH,
        "--log", LOG_LEVEL,
        "-t", TAHUN,
        "-o", OUTPUT_FORMAT,
        "--non-tender", ",".join(doms)
    ]

    logging.info("Menjalankan downloader.py dengan parameter:")
    logging.debug(" ".join(cmd))

    try:
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )

        with open(LOG_FILE, "a", encoding="utf-8") as logfile:
            for line in iter(process.stdout.readline, ''):
                if line:
                    line_clean = line.strip()
                    print(line_clean)                   # Tampilkan langsung ke terminal
                    logfile.write(line_clean + "\n")    # Simpan ke file log

        process.stdout.close()
        return_code = process.wait()

        if return_code == 0:
            logging.info("Proses downloader selesai tanpa kesalahan.")
        else:
            logging.error(f"Downloader keluar dengan kode {return_code}.")
            sys.exit(return_code)

    except Exception as e:
        logging.error(f"Terjadi kesalahan saat menjalankan '{SCRIPT_PATH}': {e}")
        sys.exit(1)

if __name__ == "__main__":
    logging.info("=== Memulai proses pengambilan data LPSE dari daftar domain ===")
    domain_lpse = baca_domain_dari_file(JSON_INPUT_FILE)
    jalankan_downloader(domain_lpse)
    logging.info(f"📁 Seluruh log proses juga disimpan dalam file: {LOG_FILE}")
