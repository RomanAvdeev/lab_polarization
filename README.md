# lab_polarization
Сервис выделения поляризации

Цель модуля: автоматическое выявление, количественный и качественный анализ эффектов поляризации массового сознания в заданном наборе текстовых новостных сообщений

Входные параметры: Коллекция новостей (без текстов) по одной или нескольким темам с дополнительными признаками (nel, sentiment, ngrams, topics). Важно, что тема должна содержать все новости, которые к ней принадлежат. Нельзя передать сначала половину новостей из темы, а затем вторую половину другим запросом.

Выходные параметры: Информация о принадлежности каждого документа к полюсам мнений

Алгоритм работы: Все шаги, перечисленные ниже, применяются отдельно для каджой темы

Постороение словаря с частотой встречаемости слов в каждом для каждого из дополнительных признаков новости.
Обучение тематической модели
Вычисление сущностей, по котором происходит поляризация мнений
Вычисление оценки напряжённости и значимости поляризации
Формирование ответа
