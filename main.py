import os
from flask import Flask, jsonify, request
from dotenv import load_dotenv

# Memuat environment variables dari file .env
load_dotenv()

app = Flask(__name__)


@app.route("/")
def home():
  return jsonify({
      "status": "success",
      "message": "Triboma Stepwise Teacher API is running!",
  })


@app.route("/api/grade", methods=["POST"])
def grade_assignment():
  data = request.json
  soal = data.get("soal")
  kunci_jawaban_guru = data.get("kunci_guru")
  jawaban_siswa = data.get("jawaban_siswa")
  langkah_siswa = data.get("langkah_siswa")
  bobot_maksimal = data.get("bobot", 10)

  # Simulasi logika penilaian berbasis AI/Rules
  # Pada implementasi nyata, kamu bisa mengirim prompt khusus ke Gemini/OpenAI API
  nilai = 0
  penjelasan = ""

  if jawaban_siswa == kunci_jawaban_guru["jawaban_akhir"]:
    nilai = bobot_maksimal
    penjelasan = (
        "Jawaban akhir benar dan langkah pengerjaan sesuai dengan acuan guru."
    )
  elif langkah_siswa in kunci_jawaban_guru["langkah_valid"]:
    # Diberikan nilai parsial karena langkah awal benar tapi mungkin ada salah hitung di akhir
    nilai = bobot_maksimal * 0.5
    penjelasan = (
        "Sebagian langkah pengerjaan benar (mendapat nilai parsial), namun"
        " terdapat kekeliruan pada hasil akhir."
    )
  else:
    nilai = 0
    penjelasan = (
        "Jawaban dan langkah pengerjaan belum sesuai dengan acuan guru."
    )

  return jsonify(
      {"soal": soal, "score": nilai, "max_score": bobot_maksimal, "feedback": penjelasan}
  )


if __name__ == "__main__":
  app.run(debug=True)
