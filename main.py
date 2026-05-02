import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import speech_recognition as sr
import random

# База слов
levels = {
    "1": [("Кот", "cat"), ("Собака", "dog"), ("Солнце", "sun"), ("Мама", "mom"), ("Папа", "dad"), ("Птица", "bird")],
    "2": [("Девочка", "girl"), ("Мальчик", "boy"), ("Сумка", "bag"), ("Дочка", "daughter"), ("Сын", "son"), ("Улица", "street")],
    "3": [("Тетрадь", "notebook"), ("Ручка", "pen"), ("Карандаш", "pencil"), ("Учитель", "teacher"), ("Стул", "chair"), ("Стол", "table")]
}

print('--- ДОБРО ПОЖАЛОВАТЬ В ТРЕНАЖЕР ПРОИЗНОШЕНИЯ ---')
lvl = input("Выберите уровень сложности (1, 2, 3): ")

if lvl in levels:
    total_points = 0
    # Выбираем 3 случайных уникальных слова для текущей сессии
    session_words = random.sample(levels[lvl], 3)
    
    recognizer = sr.Recognizer()

    for i, (ru_word, en_word) in enumerate(session_words, 1):
        print(f"\nСлово №{i}: Как переводится **{ru_word}**?")
        word_guessed = False

        for attempt in range(1, 4):
            print(f"Попытка {attempt}/3. Говорите...")
            
            # Запись
            duration = 3
            sample_rate = 44100
            recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype="int16")
            sd.wait()
            wav.write("temp.wav", sample_rate, recording)

            try:
                with sr.AudioFile("temp.wav") as source:
                    audio = recognizer.record(source)
                
                user_speech = recognizer.recognize_google(audio, language="en-US").lower()
                print(f"Вы сказали: {user_speech}")

                if user_speech == en_word:
                    print(f"Правильно! +1 балл.")
                    total_points += 1
                    word_guessed = True
                    break
                else:
                    print(f"❌ Неверно. Попробуйте еще раз.")
            
            except sr.UnknownValueError:
                print("Робот не расслышал. Говорите четче и громче.")
            except sr.RequestError:
                print("Ошибка связи с сервером.")
                break
        
        if not word_guessed:
            print(f"За попытки не удалось. Правильный ответ: {en_word}")

    # Финальный результат
    print(f"\n--- ИГРА ОКОНЧЕНА ---")
    print(f"Вы набрали баллов: {total_points} из 3")
    
    if total_points == 3:
        print("ОГО! Вы настоящий знаток английского! Идеальное произношение!")
    elif total_points > 0:
        print("Хороший результат! Продолжайте тренироваться.")
    else:
        print("Не расстраивайтесь, в следующий раз обязательно получится!")

else:
    print("Ошибка: выбран несуществующий уровень.")