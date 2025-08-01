# Gait Analysis with MediaPipe & OpenCV  

Opis  
Ten skrypt analizuje film mp4 z osobą biegnącą, wykrywa momenty kontaktu stóp z podłożem, rysuje szkielety i kąty oraz zapisuje wyniki do osobnych plików JSON. Dla najlepszych efektów film powinien być nagrany w kącie prostym względem biegacza.  

Wymagania  
-Python 3.8 lub wyższy  
-pip install -r requirements.txt  

Uruchomienie  
python main.py  

Po zakończeniu działałania python main.py w katalogu output pojawią się pliki:  
-analysis.mp4 (przetworzony film z narsowanym szkieletem i kątami)  
-frames.json (lista zdarzeń)  
-summary.json (podsumowanie + średnie kąty)  
