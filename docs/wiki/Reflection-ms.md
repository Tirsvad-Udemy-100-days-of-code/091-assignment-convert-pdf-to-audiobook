[English](Reflection) · [Dansk](Reflection-da) · **Bahasa Malaysia**

# Refleksi

## Bagaimana kita mendekatinya

Kita merancang dahulu: Business Case, pihak berkepentingan, pelan projek dan lima milestone dengan tugas, kemudian satu pull request bagi setiap milestone. Setiap langkah adalah kecil dan berakhir dengan ujian, imbasan keselamatan dan semakan.

## Apa yang sukar

- **Enjin suara.** Coqui TTS tidak mengisytiharkan PyTorch, memerlukan `torchcodec` untuk audio pada PyTorch terkini, dan model bahasa Inggeris memerlukan pakej fonem (`gruut`) atau program `espeak-ng`. Kita menemuinya dengan memasangnya dalam persekitaran sekali guna sebelum menulis sebarang kod enjin.
- **Dua pengimbas.** Imbasan keselamatan hos lebih ketat daripada yang setempat dan menggagalkan pull request pertama kita.
- **Tangkapan skrin yang jujur.** Tangkapan skrin pertama kita bagi langkah 2 dan 3 menunjukkan ralat, kerana alat itu menjalankan Python yang salah. Kita hanya menyedarinya dengan membaca teks dalam imej tersebut.

## Apa yang mudah

- Membaca PDF dengan `pypdf` dan memecahkan teks ialah fungsi tulen yang kecil dan cepat diuji.
- Port dengan enjin palsu menjadikan penukar dan baris perintah mudah diuji.

## Pengajaran terbesar kita

Semak kebergantungan yang paling berisiko dahulu. Segala-galanya dalam pelan bergantung pada satu soalan: adakah Coqui TTS boleh dipasang dan bercakap pada Python 3.13? Bertanya soalan itu dahulu, dalam persekitaran percubaan, adalah murah dan memastikan pelan selebihnya selamat.

## Apa yang akan kita lakukan secara berbeza

- Tetapkan (pin) versi kebergantungan semasa keluaran; projek ini hanya menetapkan versi minimum.
- Tambah pilihan untuk memilih model suara lain pada baris perintah bersama senarai pendek model yang telah diuji.
- Jalankan peraturan imbasan hos secara setempat sejak awal.
