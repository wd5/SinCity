# encoding: utf-8
import datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models

class Migration(DataMigration):

    def forwards(self, orm):
        """Write your forwards methods here."""
        news = (
            ('2011-02-21', u"Ну вот и запущен проект Sin City", u"""Предлагаю ознакомится с анонсом проекта, предварительными правилами и списком ролей."""),
            ('2011-03-23', u"Новое", u"""В правила добавлен раздел касающийся супергероев. Смотреть <a href="/superhero">тут</a>."""),
            ('2011-05-12', u"О персонажах", u"""<div style="text-align: right">Сидит Бильбо дома у камина, греет ноги.
Вдруг дверь с треском вылетает, в комнату
вваливается толпа тяжеловооруженных личностей.
Бильбо удивленно: «Вы кто? Гоблины?»
Гости с гордостью: «Нет! Мы – перумовские хоббиты!»</div>
Это, конечно анекдот, но увы, абсолютно реальный.

Не мне одной, подозреваю, приходилось встречать на играх хоббитов, габаритами «косая сажень в плечах». И знаете, мне это совершенно не нравилось. И не потому, что мой персонаж был во враждебных отношениях с хоббитами, нет, а потому, что игрок не соответствовал своей роли, не соответствовал своему персонажу. Увы, это грустно и печально, но такое на играх встречается сплошь и рядом.

Относительно SinCity. Я категорически не представляю себе в роли Питера Паркера человека, который не умеет фотографировать и, хотя бы изредка, не занимается фотографированием на игре. Я категорически не представляю себе в роли стриптизерши девушку, которая не танцует стриптиз каждый вечер игры в баре. И таких несоответствий может быть много.

По этому от мастерской группы вам, дорогие игроки, настоятельная просьба: прежде чем выбрать роль – подумайте, а действительно ли вы ей соответствуете??? А сможете ли вы показать своего персонажа даже в таких вроде бы мелких деталях, как умение метать дротики или играть в карты, фотографировать или танцевать стриптиз?  Ибо, если вы берете персонажа с его проблемами, умениями, возможностями, привычками, то будьте добры, отыгрывать его полностью. Чтоб для вас не было неожиданностью то, что к вашему персонажу предъявляются какие-то вам непонятные требования.

Да, до игры есть время научиться некоторым из навыков ваших персонажей. Пусть не профессионально, но, главное, чтоб соответствовать."""),
            ('2011-05-12', u"О костюмах супергероев", u"""Начнем с простого: что такое костюм супергероя. Это не просто одежда, защищающая тело от некомфортного для организма климата, нет. Это второе лицо персонажа. То, что отличает простого обывателя и журналиста Питера Паркера от супергероя Человека-паука. Костюм супергероя дает зрителям четкую ассоциацию на того, кто совершил тот или иной поступок.  Не Питер Паркер спас женщину от пьяной компании, а супергерой, Человек-Паук! А Питер Паркер – он тут вовсе и не при чем. Костюм героя это та вещь, которая позволяет герою (или антигерою) остаться неузнанным. И, смотря на человека в полном костюме, вы никогда не узнаете за маской Человека-паука скромного журналиста Питера Паркера, даже если выследили и проводили его до самого убежища. Ну, по крайней мере до тех пор – пока не снимете с него (или он сам не снимет) маску.

Далее. На нашей игре на всей территории Америки действует «Закон о запрете на героев в масках». Что это означает? А означает это только то, что любой полицейский заметив человека в костюме супергероя имеет полное право его задержать, предъявить обвинения в нарушении закона и арестовать. Это не значит, что персонажи имеющие так называемое второе лицо, не имеют право носить костюмы и маски героев, нет. Это означает только то, что надевая костюм супергероя они нарушают закон (и знают об этом) и имеют все шансы огрести последствия.

Ну и финалом. Если вы что-то творите (доброе дело или не доброе – не важно) знайте. Если вы не в костюме, то дела творит «Питер Паркер», а если вы в костюме супергероя – то дела творит уже «Человек-паук». И поверьте, мы очень постараемся донести до журналистов, и читателей газет – правильную информацию."""),
            ('2011-05-18', u"Определена дата игры", u"Игра запланирована на 4-7 октября 2012 года."),
            ('2011-05-18', u"О супергероях и суперзлодеях", u"""Сначала о некоторых особенностях человека.

Человек исследует мир при помощи зрения. Видит, анализирует, и потом уже, при необходимости, более детально изучает другими способами.

Теперь, как это работает на играх. Знаменитая фраза «Кого вижу?» в последние годы несколько ушла из оборота. Разнообразие и качество ролевых костюмов дает прекрасную возможность опознавать персонажа с первого взгляда. А в разговоре позже детали первого впечатления только уточняются. Однако в некоторых ситуациях зрение работает против игрока. Я говорю о ситуациях, когда персонаж не должен что либо видеть, но игрок то видит. Пример – игрока в белом хайратнике не должно быть видно. Но белый хайратник не делает человека невидимым на самом деле. Хотим мы или не хотим, мы все равно видим персонажа и игрока, а в результате, хотим мы того или не хотим, но мы получаем внеигровую информацию, которую получить не должны. И тут уже от профессионализма игрока зависит, как этой информацией пользоваться: бежит он поднимает панику «увидев» невидимку, которого его персонаж не мог увидеть, но игрок то увидел, потому что не обратил внимания на знак, демонстрирующий то, что тут кто-то в невидимости ходит. А может просто сказал кому-то за чашкой чая, что вот такой-то общий знакомый персонаж уже убит, ибо видел его идущим в мертвятник в белом хайратнике.  Это я к чему, собственно. К тому, что нашей МГ не нравится присутствие на нашей игре специальных каких-то знаков, демонстрирующих какие-либо специальные способности, ибо  не все игроки в процессе игры эти знаки замечают… результат – много внеигровой информации, которую приходится отсеивать.

А вот теперь перейдем к всевозможным супергероям и суперзлодеям.

Как вы знаете, в комиксах, всевозможных супергероев и суперзлодеев в достаточном количестве, и у всех них есть какие-то сверхспособнасти, которые на игре иначе как специальными знаками не продемонстрируешь. К примеру – умение летать.

Поскольку человека природа такой способностью не оделила – люди летать не умеют, увы.  А раз  вы не умеете летать, то и персонаж ваш не умеет.  Нет, ваш персонаж может думать, что он умеет летать, быть буквально таки уверенным в этом. Но думать о том, что умеешь, и уметь на самом деле – это совершенно разные вещи. К остальным спецспособностям отношение такое же.

Если вы хотите играть супергероя или суперзлодея, то берите за основу те его способности, которые с одной стороны – хорошо реализуемы на игре, а с другой – характерны вот именно для этого персонажа."""),
            ('2011-08-04', u"Добавления в правилах", u"Добавлены правила относительно сексуальных отношений на игре."),
            ('2011-09-07', u"Обновления в правилах", u"Появились правила по полиции,  и относительно общих моментов игры."),
            ('2011-09-21', u"18+", u"На игру не допускаются несовершеннолетние дети."),
            ('2011-09-28', u"V – значит вендетта.", u"""Вуаля! Пред Вами водевильный ветеран,
которому всевластная судьба давала роли извергов и жертв.
Сей образ не высокомерием выдуман.
Он — смутное воспоминание vox populi,
что в нынешнее время выжжено, мертво.
Приняв великолепный внешний вид,
молвой навеки выдворенный обличитель возвратился,
поклявшись выводить все проявления скверны
своекорыстной, бессовестной, невежественной власти!
Он вынес ей единственно возможный вердикт — Вендетта,
и клятвенно заверил вершить его,
и рвение вознаградится, ведь верность,
нравственность, отвага всегда одерживают верх.
Воистину, я выше всякой меры витиеват и выспрен,
весьма доволен знакомством с Вами,
меня ж зовите просто V.

Гай Фокс (V), знакомство с Иви Хаммонд.

Итак, кто же все-таки он – незнакомец, называющий себя V, носящий маску Гая Фокса, в минуты вдохновения выражающийся стихами? Или что такое?…

1605 год, Англия два года как находится под властью Стюартов. Надежды, возлагавшиеся на новую королевскую династию католиками и пуританами, рухнули с треском. А несбывшиеся надежды – отличный повод для ненависти. И вот находится группа единомышленников, решающая взорвать Парламент. Неизвестно, кто был организатором Порохового заговора, однако после его провала у каждого на слуху одно имя.

Гай Фокс.

Человек, публично заклейменный, но не сломленный. Человек, ставший олицетворением того, что нельзя больше прятаться – нужно сражаться. Человек, сам выбравший на эшафоте свою судьбу и не давший себя выпотрошить и четвертовать, спрыгнувший с верхней ступеньки и сломавший петлей шею. В эту секунду умер смертный Гвидо Фокс и родился V. Воплощенный дух свободы и справедливости. Живая идея.

V носит маску, которая представляет собой пародию на Гая Фокса, пряча под ней лицо. Единственная на то причина состоит в том, что абсолютно неважно, кто под маской – белый мужчина, ребенок, женщина, старик, калека. Тело и плоть слабы, но идея вечна. У нее нет иного имени, кроме этой буквы, означающей Viktoria, Победа. Именно поэтому V вселяет в коррумпированных продажных тварей в официальных кабинетах такой ужас – он каждый раз тот же. Вы можете убивать его, забывать, запрещать – V вернется, ибо он в первую очередь не человек. А такие всегда возвращаются.

V бессмертен. Это не значит, что если его расстреливать из крупнокалиберного пулемета, он будет смеяться и просить добавки. Просто убитое тело под костюмом и маской не имеет ничего общего с V.

V всегда приходит туда, где  в нем нуждаются. Когда среди угнетенного народа кто-то решает, что с него достаточно, что надо встать и бороться за свою свободу – рождается V своего места и своего времени. И для того, чтобы он пришел, достаточно сделать две вещи – встать с колен и надеть маску."""),
            ('2011-09-29', u"Городские легенды.", u"""Разные истории и легенды города. Любой игрок может написать статью и отправить мастерам. Если Ваша легенда соответствует атмосфере мира и идее игры – она появится на сайте. Таким образом, Вы сможете заявить о своем персонаже, рассказать о каких либо событиях, и принять активное участие в жизни города.

Легенды отправлять по адресу: legend@sincity2012.ru"""),
        )

        for announce in news:
            orm.News.objects.create(date_created=announce[0], title=announce[1], content=announce[2])


    def backwards(self, orm):
        """Write your backwards methods here."""


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'core.gallery': {
            'Meta': {'object_name': 'Gallery'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'core.layer': {
            'Meta': {'object_name': 'Layer'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'core.layerconnection': {
            'Meta': {'object_name': 'LayerConnection'},
            'comment': ('django.db.models.fields.TextField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_locked': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'layer': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'roles'", 'to': "orm['core.Layer']"}),
            'role': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Role']"})
        },
        'core.news': {
            'Meta': {'ordering': "('-date_created',)", 'object_name': 'News'},
            'content': ('django.db.models.fields.TextField', [], {}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'core.profile': {
            'Meta': {'object_name': 'Profile'},
            'age': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'bus': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'dream': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'goal': ('django.db.models.fields.TextField', [], {}),
            'gun': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'icq': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'locked_fields': ('django.db.models.fields.CharField', [], {'max_length': "'300'", 'null': 'True', 'blank': 'True'}),
            'med': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'paid': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'photo': ('core.models.ThumbnailImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'quest': ('django.db.models.fields.TextField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'role': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'suggested_role'", 'null': 'True', 'to': "orm['core.Role']"}),
            'special': ('django.db.models.fields.TextField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'tel': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'})
        },
        'core.role': {
            'Meta': {'ordering': "('order',)", 'object_name': 'Role'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '10000'}),
            'profession': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'profile': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'locked_role'", 'null': 'True', 'to': "orm['core.Profile']"})
        },
        'core.roleconnection': {
            'Meta': {'object_name': 'RoleConnection'},
            'comment': ('django.db.models.fields.TextField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_locked': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'role': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'roles'", 'to': "orm['core.Role']"}),
            'role_rel': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'linked_roles'", 'null': 'True', 'to': "orm['core.Role']"})
        }
    }

    complete_apps = ['core']
