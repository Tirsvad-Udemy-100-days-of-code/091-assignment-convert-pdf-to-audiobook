[English](Reflection) · [Dansk](Reflection-da) · **Bahasa Malaysia**

# Refleksi

## Cara kami mendekatinya

Kami merancang dahulu: kes perniagaan, pihak berkepentingan, pelan projek dan pencapaian dengan tugas, kemudian satu pull request bagi setiap pencapaian. Setiap langkah kecil dan berakhir dengan ujian, imbasan keselamatan, semakan dan binaan hijau pada hos. Lima pencapaian pertama membina penukar dan baris arahan. Kemudian kami menambah empat lagi dengan cara yang sama: tetingkap untuk menaip teks dan mendengarnya, butang Open PDF dengan Stop, konsol senyap dan status pemuatan.

## Apa yang sukar

- **Enjin pertuturan.** Coqui TTS tidak mengisytiharkan PyTorch, memerlukan `torchcodec` untuk audio pada PyTorch terkini, dan model Inggeris memerlukan pakej fonem (`gruut`) atau program `espeak-ng`. Kami mengetahuinya dengan memasangnya dalam persekitaran sementara sebelum menulis kod enjin.
- **Dua pengimbas.** Imbasan keselamatan hos lebih ketat daripada yang setempat dan menggagalkan dua pull request: mula-mula pada panggilan shell, kemudian pada lambda dalam pembina.
- **Tetingkap yang tidak boleh disentuh.** Tetingkap diuji dalam bekas Linux pada paparan maya, tidak pernah pada desktop. Ini membuktikan logik, teks status dan tangkapan skrin, tetapi bukan apa yang berlaku apabila seseorang menutup tetingkap. Penutupan sebenar pertama menimbulkan ralat yang tidak dilihat oleh ujian kami.
- **Bukti yang jujur.** Tangkapan skrin pertama kami bagi langkah 2 dan 3 menunjukkan ralat, kerana alat itu menjalankan Python yang salah. Satu ralat skrip juga memotong sebuah dokumen, dan kami hanya perasan kemudian.

## Apa yang mudah

- Membaca PDF dengan `pypdf` dan memecahkan teks ialah fungsi kecil yang tulen dan cepat diuji.
- Port dengan objek palsu: enjin, pemain audio, pemilih fail dan pengekstrak teks disuntik, jadi 154 ujian berjalan dalam kira-kira satu saat tanpa bunyi, tetingkap atau rangkaian.
- Menambah ciri pada reka bentuk berlapis: setiap pencapaian baharu menyentuh sedikit fail dan tidak mengubah domain.

## Pengajaran terbesar kami

Semak perkara paling berisiko dahulu, dan uji di tempat pengguna sebenarnya bertindak. Seluruh pelan bergantung pada satu soalan: bolehkah Coqui TTS dipasang dan bercakap pada Python 3.13? Bertanya dahulu dalam persekitaran sementara memastikan yang lain selamat. Ralat penutupan tetingkap mengajar separuh lagi: antara muka grafik palsu membuktikan logik, bukan apa yang dilakukan manusia.

## Apa yang akan kami lakukan secara berbeza

- Menjalankan peraturan imbasan hos secara setempat sejak awal.
- Menguji laluan tutup dan batal tetingkap dalam persekitaran Windows sementara, bukan hanya dalam bekas.
- Meminta orang kedua menyemak kes perniagaan dan keputusan; semua semakan dalam projek ini ialah pengganti bagi seorang.
- Menambah pilihan untuk memilih model suara lain pada baris arahan dengan senarai pendek model yang telah diuji.
- Menutup perkara terbuka yang kecil: kes perniagaan mengira dua pakej diperlukan sedangkan projek kini mempunyai lebih, dan status `Loading voice...` turut meliputi ketulan pertama kerana enjin tiada isyarat "dimuatkan".
