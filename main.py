import os
from flask import Flask, jsonify, request
from dotenv import load_dotenv

# Memuat environment variables dari file .env
load_dotenv()

app = Flask(__name__)

# Konfigurasi folder upload sementara
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/api/grade-scan', methods=['POST'])
def grade_with_scan():
  # Cek apakah ada file foto yang dikirim dari frontend
  if 'file' not in request.files:
    return jsonify({'error': 'Tidak ada file foto/scan yang diunggah'}), 400

  file = request.files['file']
  soal_id = request.form.get('soal_id')

  if file.filename == '':
    return jsonify({'error': 'Nama file tidak valid'}), 400

  # Simpan file gambar sementara
  file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
  file.save(file_path)

  try:
    # ---------------------------------------------------------
    # DI SINI PROSES AI / OCR BERJALAN
    # ---------------------------------------------------------
    # 1. Kirim file gambar ke OpenAI API (Vision / Codex / GPT-4o)
    # 2. Bandingkan hasil ekstrak teks jawaban siswa dengan kunci guru.
    # ---------------------------------------------------------

    # Simulasi hasil penilaian dari analisis foto:
    nilai_sementara = 5  # Contoh: dapat nilai parsial karena ada langkah yang benar
    feedback_ai = (
        'Berdasarkan scan foto jawaban, langkah pertama hingga kedua sudah'
        ' sesuai dengan acuan guru, namun ada kesalahan perhitungan di bagian'
        ' akhir (kesalahan aljabar).'
    )

    # Hapus file setelah diproses agar tidak menumpuk di server
    os.remove(file_path)

    return jsonify({
        'status': 'success',
        'message': 'Foto berhasil di-scan dan dievaluasi oleh AI',
        'soal_id': soal_id,
        'score': nilai_sementara,
        'max_score': 10,
        'feedback': feedback_ai,
    })

  except Exception as e:
    if os.path.exists(file_path):
      os.remove(file_path)
    return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
  app.run(debug=True)
