## Чтобы начать работать с сайтом нужно:
1) python manage.py create_superuser - создаст админа 
2) python manage.py create_user - создаст 2х юзеров, 1 верифицированный, 1 нет 
3) python manage.py create_manager - создаст менеджера с определенными правами (только он и админ могут активировать/деактивировать пользователей и т.д.) 
4) python manage.py create_content_manager - создаст контент менеджера для блога (только он и админ могут создавать блоги) 

## Далее, фикстуры: 
1) python manage.py loaddata mailing_list/fixtures/clients.json - добавляем клиентов 
2) python manage.py loaddata mailing_list/fixtures/messages.json - добавляем сообщения 
3) python manage.py loaddata blog/fixtures/blogs.json - добавляем блоги 

## Не сделал фикстуру для рассылок, потому что там настроен сигнал для создания таблицы под логи + при создании рассылки идёт связь с djangojobscheduler, поэтому рассылки нужно создать в ручную.