# Gait Analysis with MediaPipe & OpenCV \n

Opis \n
Ten skrypt analizuje film mp4 z osobą biegnącą, wykrywa momenty kontaktu stóp z podłożem, rysuje szkielety i kąty oraz zapisuje wyniki do osobnych plików JSON. Dla najlepszych efektów film powinien być nagrany w kącie prostym względem biegacza.

Wymagania \n
-Python 3.8 lub wyższy \n
-pip install -r requirements.txt \n

Uruchomienie \n
python main.py \n

Po zakończeniu działałania python main.py w katalogu output pojawią się pliki: \n
-analysis.mp4 (przetworzony film z narsowanym szkieletem i kątami) \n
-frames.json (lista zdarzeń) \n
-summary.json (podsumowanie + średnie kąty) \n
