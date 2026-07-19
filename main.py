from google import genai
from google.genai import errors
import json
import os
import time

client = genai.Client(api_key='AIzaSyDGeNtvpop3_wnLJyOXSTlO2CPyoPYUuOU')

models = ['gemini-3.5-flash', 'gemini-3.1-flash-lite', 'gemini-3.1-pro-preview', 'gemini-3-flash-preview']
languages = ['en', 'fr', 'it', 'pl', 'el', 'fi', 'nb', 'cs', 'de', 'pt', 'hu', 'ni', 'sl', 'ro', 'sk', 'is']
current_model_idx = 0

with open('./example.json', 'r', encoding='utf-8') as f:
    data = json.load(f)


def translate(prompt):
    global current_model_idx
    attempts = 0
    max_retries = 5

    while attempts < max_retries:
        current_model = models[current_model_idx]

        try:
            interaction = client.interactions.create(
                model=current_model,
                input=prompt
            )

            return interaction.output_text
        except errors.ClientError as error:
            if error.code == 429:
                current_model_idx = (current_model_idx + 1) % len(models)
                attempts += 1
                time.sleep(2)
                continue
            else:
                raise error

    raise RuntimeError("Все модели исчерпали лимит")


for language in languages:
    prompt = (
        f'Привет. Есть такой json файл {data}. Мне нужно чтоб ты перевел значения ключей на {language}. '
        f'Если видишь пути картинок, ссылки, или по типу issue/game - не трогай. '
        'Если увидишь UAH или другой знак валюты - заменяй на {currencySymbol}'
        f'Результат просто json файл и без коминтариев по типу '
        f'"Вот переведенный на французский язык JSON-файл. Переменные в фигурных скобках `{{...}}`, '
        f'HTML-теги, пути к изображениям и ссылки остались нетронутыми:".'
    )

    result = translate(prompt)

    os.makedirs('./translate', exist_ok=True)

    with open(f'./translate/{language}.json', 'w', encoding='utf-8') as f:
        f.write(result)

client.close()