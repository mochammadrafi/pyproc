import requests
from bs4 import BeautifulSoup
import json
import time
from datetime import datetime

BASE_URL = "https://eproc.lkpp.go.id/lpse/index/0/0/{}"

HEADERS = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-language": "en-US,en;q=0.9,id;q=0.8",
    "cache-control": "no-cache",
    "content-type": "application/x-www-form-urlencoded",
    "origin": "https://eproc.lkpp.go.id",
    "pragma": "no-cache",
    "priority": "u=0, i",
    "referer": "https://eproc.lkpp.go.id/lpse/index/0/0/88",
    "sec-ch-ua": '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
    "sec-ch-ua-arch": "arm",
    "sec-ch-ua-bitness": "64",
    "sec-ch-ua-full-version": "135.0.7049.95",
    "sec-ch-ua-full-version-list": '"Google Chrome";v="135.0.7049.95", "Not-A.Brand";v="8.0.0.0", "Chromium";v="135.0.7049.95"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-model": '""',
    "sec-ch-ua-platform": "macOS",
    "sec-ch-ua-platform-version": "15.3.2",
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "same-origin",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"
}

COOKIES = {
    "_cfuvid": "tfoJ0N6amhVP9vaFOGojJU58Q5bwuY_WIlyh4ZNpGwA-1744947841312-0.0.1.1-604800000",
    "cf_clearance": "gAHCq0BNKTx1huczqUDmdNzBnaD4exl6gjDPLsJMlNg-1744991837-1.2.1.1-gfmQmc2YqcL4jc7jpP6R37uFdVYdqrF3udEHhNXcKT574tEQEJwFPmlJlzBK08DKfMW112SLSwJnRBUjShQjC1ihrB..HD_fq6eKNRCnU8nAagNRTSdR42yZfLQDOsvDPJn2HhXpw5VkcivE9R0mBXI807mN7rGoSguZnNqpTFvCtWoBmbnSE6Ug1oTFl20Cy3smmM7fEa4eBCMtlpwDk.OLTJwe.O.CTIcHw1UZdq27QC7FnceGnMY6_gsuM5V_ZFiEXis5XiD7OfoL4JYAX.Ap6NqvFRtmRmh6P8wjYdAEZlCWijF4fte5r6PLzEYx4yuFFrBkdLX6HgaOs_GTEONTB2UPk7t7gBiIaK48U.1ke9OddOh1VGMCSHskE_o.",
    "ci_session": "ppkqfdnbn8d8k6vehmvv6r578soa6024"
}

def log(msg):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{now}] {msg}")

results = []
page = 1
total = 0

log("Memulai proses pengambilan data LPSE...")

while True:
    log(f"Mengambil halaman ke-{page}...")
    response = requests.get(BASE_URL.format(page), headers=HEADERS, cookies=COOKIES)
    soup = BeautifulSoup(response.text, "html.parser")
    cards = soup.select(".card.card-small-round")

    if not cards:
        log("Tidak ada data ditemukan pada halaman berikutnya. Pengambilan dihentikan.")
        break

    log(f"{len(cards)} entri ditemukan pada halaman {page}.")

    for i, card in enumerate(cards, 1):
        try:
            nama = card.select_one("h4").text.strip()
            provinsi = card.find("label", string="PROVINSI").find_next("p").text.strip()
            email = card.find("label", string="EMAIL").find_next("p").text.strip()
            tipe = card.find("label", string="TIPE LPSE").find_next("p").text.strip()
            status_aktif = card.find("label", string="STATUS").find_next("p").text.strip()
            std = card.find("label", string="STANDARDISASI").find_next("p").text.strip()
            pegawai = card.find("label", string="PARTISIPASI PEGAWAI").find_next("p").text.strip()
            kegiatan = card.find("label", string="PARTISIPASI KEGIATAN").find_next("p").text.strip()
            versi = card.find("label", string="VERSI SPSE").find_next("p").text.strip()
            update = card.select_one(".item-content-container p").text.strip()
            link_detail = card.select_one("a.btn.btn-primary")["href"]
            link_web = card.select_one("a.btn.btn-success")["href"]
            status_server = "Online" if "Online" in card.text else "Offline"

            results.append({
                "nama_lpse": nama,
                "provinsi": provinsi,
                "email": email,
                "tipe_lpse": tipe,
                "status_aktif": status_aktif,
                "status_server": status_server,
                "standardisasi": std,
                "partisipasi_pegawai": pegawai,
                "partisipasi_kegiatan": kegiatan,
                "versi_spse": versi,
                "tanggal_update": update,
                "link_detail": link_detail,
                "link_website": link_web
            })

            # Insert data into json lpse_list.json
            with open("lpse_list.json", "a", encoding="utf-8") as f:
                json.dump(results, f, ensure_ascii=False, indent=4) 

            total += 1
            log(f"✔️  [{total}] {nama} berhasil diproses.")

        except Exception as e:
            log(f"⚠️  Gagal parsing entri ke-{i} di halaman {page}: {e}")

    page += 1
    time.sleep(1.2)

log(f"Proses selesai. Total {total} entri LPSE telah disimpan ke 'lpse_list.json'.")
