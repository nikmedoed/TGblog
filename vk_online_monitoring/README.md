Пользователи ВКонтакте достаточно пассивная аудитория. Чтобы ваш пост заметили, нужно опубликовать его в момент нахождения максимального количества ваших знакомых онлайн. Понятно, что есть различные варианты продвижения, но сейчас речь именно о ваших актуальных друзьях (подписчиках).

Эта утилита позволяет определить временные промежутки, в которые стоит публиковать ваши посты, чтобы получить максимальный охват. Ну или разочароваться. 

Анализ состоит из двух этапов.

Сбор
За сбор данных отвечает `vk_online_monitoring.py`. Данный скрипт помогает собрать статистику по онлайну ваших подписчиков, а также подписчиков вашего сообщества Вконтакте.

- Данные могут быть получены только от открытых для вас пользователей
- Значения по онлайну собираются раз в минуту и дописываются в файл

Для запуска скрипта скрипта потребуется:
- Указать логин и пароль
- Пройти двухфакторную авторизацию, при наличии
- Иметь библиотеки `pandas` и `vk_api`

После авторизации `vk_api` создаёт файл с куками (`vk_config.v2.json`), который позволяет проходить аутентификацию без авторизации. Его можно перекинуть со скриптом на ваш сервер, чтобы не проходить авторизацию.

Когда вы наберёте достаточное количество значений, можете приступать к анализу.
