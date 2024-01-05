# Суммаризация и озвучка новостных статей в формате телеграмм-бота

## Как работает продукт

1. Собираются данные с новостного автомобильного сайта
2. Текст очищается от html разметки и прочих лишних символов
3. Суммаризируется двумя способами
4. Текст предобразабтывается 
5. Предобработанный текст озвучивается, сохраняется аудиофайл
6. Сохраняется изображение с облаком тегов с "важными" словами
7. Данные сохраняются в постгре
8. Пользователь отправляет запрос боту телеграма
9. Пользователю отправляется аудио, абстрактная суммаризация и облако тегов

![image](https://github.com/wrongserenity/news_sum_to_speech/assets/43683367/7b721627-8f21-4abe-ba52-0795ca2dc61a)  
На скриншоте:
Изображение с облаком тегов текста статьи
Текст абстрактивной суммаризации
Аудио с озвучкой экстрактивной суммаризации
 
## Бэкэнд
 
### PostgreSQL
Простенькая, с одной таблицей для хранения урлов, дат и распаршенного и суммаризированного текста новостей
 
### Bot
Бот в телеге, который отправляет войсы с модифицированным текстом из бд
Несколько кнопок: "за эту неделю", "за день". Соответственно по нажатию на кнопки присылает новости за выбранный период
 
### Парсер
Бежит по сайту и парсит новости и даты их создания
 
### Докер
Три вышеперечисленных микросервиса
Парсер запускается при запуске и с помощью крона раз в сутки
 
## Использованные алгоритмы и модели
 
### TTS
использована vits модель natasha-g2p-vits
 
### tts фронтенд
на основе num2words, pymorphy, spacy, ruaccent
в тексте расшифровываются цифры с адаптацией формы слова 
расшифровываются сокращения (как обычные типа г., так и специфические как об. и квтч)
для слов из этой доменной области подобраны корректные ударения, которые учитываются при озвучке
 
### экстрактная суммаризация
на основе networkx, nltk
выставляет ранки предложений и выдает N самых "важных" предложений
 
### абстрактная суммаризация
используется дообученная модель на основе модели реконструкции замаскированных токенов [rut5-base](https://arxiv.org/abs/2309.10931) 
- на данных с [IlyaGusev/gazeta](https://huggingface.co/datasets/IlyaGusev/gazeta)  
- алгоритм обучения в [news_abstr_sum_training.py](https://github.com/wrongserenity/news_sum_to_speech/blob/main/src/news_abstr_sum_training.py)  
- саму модель можно подгрузить с hugging face: [wrongserenity/news_to_speech_t5_summarizer](https://huggingface.co/wrongserenity/news_to_speech_t5_summarizer)  

Результаты дообучения модели rut5-base на датасете IlyaGusev/gazeta:  
![image](https://github.com/wrongserenity/news_sum_to_speech/assets/43683367/ba2bfa67-7a5a-4863-b611-3e3fdbbfaa39)
 
### облако тегов
на основе tf-idf, nltk и wordcloud
удаляются стоп слова из двух библиотек, токенизация-лемматизация-стемминг слов, ранжирование
далее восстанавливаются изначальные формы слов и отрисовываются в изображение

## Деплой

Для запуска используйте

`docker-compose up --build`


