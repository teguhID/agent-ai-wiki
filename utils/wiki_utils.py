import re
import requests

from bs4 import BeautifulSoup


# ------------------ EXTRACT CONTENT ------------------
def extract_content(url: str, session_id: str, chain_with_history) -> str:
    try:
        # Check if URL contains curly braces and extract content inside them
        curly_brace_matches = re.findall(r'\{([^}]*)\}', url)
    
        # Convert the list of matches to a single string (if any matches found)
        curly_brace_content = ""
        if curly_brace_matches:
            curly_brace_content = " ".join(curly_brace_matches)

            response = chain_with_history.invoke(
                {"input": prompt_get_info(curly_brace_content)},
                config={"configurable": {"session_id": session_id}}
            )

            result_parameter = response.content
            url = url.replace(f"{{{curly_brace_content}}}", result_parameter.strip().lower())

        resp = requests.get(url)
        resp.raise_for_status()  # Raise an exception for bad status codes
        soup = BeautifulSoup(resp.text, 'html.parser')
        main = soup.select_one('main')
        return main.get_text(separator='\n') if main else ""
    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL {url}: {e}")
        return f"Untuk data dari url {url} tidak dapat di ambil, data tidak ada atau tidak valid"


def prompt_step(query: str) -> str:
    return f"""
        Kategori tersedia: Kota, Dokumen, BUMN, Layanan Administrasi, Universitas, Air Terjun, Makanan Khas, Pulau, Vaksin, Kesehatan Mental, Lembaga Negara, Provinsi, BUMD, Candi, Taman Kota, Rumah Sakit, Museum, Taman Air, Pajak, Menteri, Penyakit, BUMS, Taman Nasional, Gunung, Danau, Pantai, Gua, Taman Rekreasi

        Contoh format URL:
        - https://wiki.ambisius.com/kota/salatiga (kategori: kota, objek: salatiga)
        - https://wiki.ambisius.com/gunung/gunung-salak (kategori: gunung, objek: gunung-salak)

        Tugas:
        Dari input "{query}", berapa langkah minimal untuk mendapatkan informasi relevan dari wiki?

        Jawab dalam format JSON:
        [
            {{
                "url": "https://wiki.ambisius.com/gunung/gunung-sinabung",
                "action": "Ambil informasi terkait lokasi Gunung Sinabung"
            }}
        ]

        Catatan: 
        - buat langkah seefisien mungkin tanpa spekulasi.
        - sertakan semua kemungkinan jika ada lebih dari satu.
        - jika ada informasi yang harus di ambil dari langkah sebelumnya, buat informasi tersebut menjadi parameter di dalam kurung, misal {{nama_provinsi}}
        """

def prompt_get_info(parameter: str) -> str:
    return f"""
        berdasarkan informasi sebelumnya

        Lakukan tindakan berikut:
        Ambil informasi terkait {parameter} dari informasi sebelumnya

        Catatan:
        - Berikan hanya jawaban saja berupa string tanpa penjelasan
        - Ubah spasi menjadi tanda hubung (-), contoh: "jawa barat" menjadi "jawa-barat"
        """
    
def prompt_result(context: str, question: str) -> str:
    return f"""
        Kamu adalah agen penjawab pertanyaan dari Wiki Ambisius.

        Berikut adalah informasi dari halaman wiki:
        {context}

        Jawablah pertanyaan berikut berdasarkan informasi di atas:
        "{question}"

        Buatlah jawaban yang simple, informatif dengan format text yang mudah di baca
        """
