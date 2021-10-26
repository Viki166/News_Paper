from news.models import Author, Category, Post, Comment
from django.contrib.auth.models import User
from datetime import datetime
1.
user1 = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
user2 = User.objects.create_user('paul', 'mccartney@thebeatles.com', 'paulpassword')
2.
author1 = Author.objects.create(user=user1)
author2 = Author.objects.create(user=user2)
3.
category1 = Category.objects.create(name='Спорт')
category2 = Category.objects.create(name='Туризм')
category3 = Category.objects.create(name='Экономика')
category4 = Category.objects.create(name='Культура')
4.
article1 = Post.objects.create(news_or_article=2, header='Пособие для медных: цены на ключевой цветной металл бьют рекорды', text='Рост цен практически на все сырьевые ресурсы в последние полтора года получил наиболее яркое выражение в секторе цветных металлов. Алюминий, никель, цинк в течение этого года установили рекорды или находятся в непосредственной близости от исторических максимумов. Мощный подъем в октябре пережили и котировки одного из самых распространенных и важных металлов — меди. На минувшей неделе медь стоила дороже $10 тыс. за тонну, в разы больше докризисных показателей. Но этого мало: в ближайшей перспективе цены могут вырасти в 2–2,5 раза, считают аналитики. Учитывая катастрофический дефицит металла в резервах и хроническое недоинвестирование в годы низких цен, этот прогноз еще может стать консервативным.', author=author1)
article2 = Post.objects.create(news_or_article=2, header='На цвет золота: в чем коммерческая тайна великого Пабло Пикассо', text='Его называют чародеем и волшебником, мессией, определившим развитие искусства, «сейсмографом конфликтов, смятений и боли своего времени». Ему посвящены сотни выставок и монографий, но его жизнь и творчество по-прежнему таят в себе неразгаданную до конца тайну. Только в 2020 году на торгах ушло с молотка около 3,4 тыс. работ Пабло Пикассо — в итоге общая стоимость проданных картин художника достигла $600 млн. 25 октября исполняется 140 лет со дня рождения автора «Герники» и других знаковых картин, ставших вехами в истории мировой живописи. О том, в чем заключался (и заключается) коммерческий секрет гения', author=author2)
news1 = Post.objects.create(news_or_article=1, header='Российские фигуристы получили визы Канады для участия в Гран - при' , text='Часть российских фигуристов, заявленных на Гран-при в Канаде, получили в понедельник визы для въезда в эту страну, заявил РИА Новости президент Федерации фигурного катания на коньках России (ФФККР) Александр Горшков.Этап Гран-при в Ванкувере Skate Canada пройдет с29 по 31 октября. В пятницу ФФККР сообщила, что пока паспорта с визами не получили фигуристы Камила Валиева, Елизавета Туктамышева, Алена Косторная, Евгений Семененко, Макар Игнатов, тренеры Алексей Мишин, Евгений Рукавицын и другие. Имеющие визы Александр Самарин и танцевальная пара Елизавета Шанаева/Девид Нарижный уже прибыли в Ванкувер.', author=author2)
5.
article1.category = category2, category3
article1.save()
article2.category = category4, category3
article2.save()
news1.category = category1, category2
news1.save()
6.
comment1 = Comment.objects.create(text='Текст комментария 1', user=user1, post=article1)
comment2 = Comment.objects.create(text='Текст комментария 2', user=user2, post=article1)
comment3 = Comment.objects.create(text='Текст комментария 3', user=user1, post=article2)
comment4 = Comment.objects.create(text='Текст комментария 4', user=user2, post=article2)
comment5 = Comment.objects.create(text='Текст комментария 5', user=user1, post=news1)
comment6 = Comment.objects.create(text='Текст комментария 6', user=user2, post=news1)
7.
article1.like() # 4
article2.like() # 8
news1.like() # 2
article1.save()
article2.save()
news1.save()
comment1.like() # 4
comment2.like() # 3
comment3.like() # 4
comment4.like() # 5
comment5.like() # 4
comment6.like() # 6
comment1.save()
comment2.save()
comment3.save()
comment4.save()
comment5.save()
comment6.save()
8.
author1.update_rating()
author2.update_rating()
9.
# best_user = Author.objects.all().order_by('-rating').values('user','rating')[0]
best_user = Author.objects.all().order_by('-rating')[0]
best_user.user
best_user.rating
10.
# best_post = Post.objects.all().order_by('-rating').values('date_time','author','rating','header')[0]
best_post = Post.objects.all().order_by('-rating')[0]
best_post.date_time.strftime("%m/%d/%Y, %H:%M:%S")
best_post.author.user
best_post.rating
best_post.header
best_post.preview()
11.
# best_post_comments = Comment.objects.filter(post=best_post)
# best_post_comments[1].date_time.strftime("%m/%d/%Y, %H:%M:%S")
# best_post_comments[1].user
# best_post_comments[1].rating
# best_post_comments[1].text
best_post_comments = Comment.objects.filter(post=best_post).values('date_time', 'user', 'rating', 'text')