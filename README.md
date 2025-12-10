1. Clone Repository
Pastikan kamu sudah berada di folder tujuan, lalu jalankan:
```bash
git clone [https://github.com/drphnd/loan.git](https://github.com/drphnd/loan.git)
cd loan

2. Buat Virtual Environment (Wajib)
Supaya library tidak bentrok dengan sistem laptopmu, buat environment baru:

Untuk Windows:

Bash

python -m venv venv
.\venv\Scripts\activate
Untuk Mac / Linux:

Bash

python3 -m venv venv
source venv/bin/activate

3. Install Dependencies
Install semua library yang dibutuhkan (Streamlit, Pandas, dll) sekaligus:

Bash

pip install -r requirements.txt

4. Jalankan Aplikasi
Bash

streamlit run app.py