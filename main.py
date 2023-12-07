from src.news_parsing import Parser

SAMPLE_TEXT = "На сегодня именно камеры дорожного наблюдения регистрируют большую половину нарушений, за которые потом следуют административные штрафы. " \
                "Самое примечательно, что устанавливаются такие камеры в самых неожиданных и не заметных местах. " \
                "Они работают как невидимый капкан, в который водитель попадает через пару недель, когда получает квитанцию штрафа, и таких капканов становится все больше и больше. " \
                "Речь идет именно о том, что камеры не видны и водитель не подозревает о них. " \
                "С июля месяца должно уже вступить в силу постановление госдумы о том, чтобы в местах, где есть видеокамеры, должен обязательно стоять предупреждающий знак. " \
                "Но глупо рассчитывать на то, что подобный знак будет установлен возле каждой камеры, тем более учитывая, что они ставятся где угодно: на столбах, на треногах или прячутся в металлических ящиках у обочин. " \
                "Более того, сотрудники дорожной полиции нередко делают тихие рейды, неприметно устанавливая камеры в автомобилях. " \
                "Впрочем, обо всех уловках водители уже знают, потому что многие, если не каждый, уже получил штраф, подаренный именно такой камерой." \
                "И как же сделать так, чтобы не попадаться, ведь так или иначе хоть немножко нарушить правила приходится. " \
                "При этом всех интересуют «законные» способы ухода от ответственности за превышение скорости или обгона в неустановленном месте. " \
                "Под словом законный метод имеется в виду то, что за ваши действия вам не будет наказания, хотя наказание - это понятие растяжимое, штраф в 5000 рублей можно получить легко. " \
                "Как правило, такие методы подразумевают хитрые манипуляции с номерным знаком, чтобы дорожные камеры не смогли его качественно заснять. " \
                "При самом плохом стечении обстоятельств за подобные укрывательские манипуляции вы можете получить по КоАП РФ лишение прав на вождение на 1-3 месяца, это предусмотрено статьей 12.2 ч.2. " \
                "Так что вам решать, нужно ли вам такое счастье, кроме того, если вы так пытаетесь себя обезопасить, значит, вы намерено уже готовы нарушать ПДД в виде превышения скоростного режима, что чревато. " \
                "Есть ли легальные средства не попасть на камеру?"

SAMPLE_TEXT_KIR = "Первый крупный турнир по магии. Год назад решил войти в формат Pauper по мтг. Там как раз начиналась питерская лига для большого турнира в мск, решил залететь. Начал играть на UR Skred'e. Показывал достаточно хорошие результаты, итогом которых стал топ 2 этой питерской лиги, но в мск решил не ехать на турик. Потом забил на паупер на полгода, и вот совсем недавно вернулся. Вернулся как раз к предстоящему турниру в Питере уже. Порезал UR Skred, в итоге получились Mono u Fae.  До турнира успел протестить колоду всего 3 раза. Результаты были средние: 2-2, 3-0-1, 1-3. На последнем тесте почти разочаровался в колоде, но понимал, почему проебал.В итоге, на турнир шел с чувством \"хотя бы одну выиграть\". Уже был готов к любому исходу, волнения как такого не было. Турнир 4 июня: Вход: 2000 Формат: Pauper Количество участников: 31 Система: швейцарка, потом топ 8 Изначально, примерно, знал сколько будет человек, расстраивало, что так мало, видимо, челы с регионов больше угарают в мск ездить, чем в Питер. Регистрация, ожидания, паринги. 1 раунд RG Ponza: Попарило с челом с Питера, с которым уже играл недавно. Чел играет слабо, поэтому сразу ожидал легкие 2-0. Так и произошло, нехуй добавить 2 - 0 Итого: 1-0 (3 поинта) 2 раунд Jeskai Ephemerate(?): После первой партии был душевный подъём, но внутри было наебалово, что слишком легко далось, дальше будет пиздец. Парят с незнакомым челом, мб московский. 2.1 партия: Выигрываю кубы, хожу первый. Оппонент мулиганится в 5. Внутри уже чувство выигранной 1 партии. После хода: Остров -> Фея -> Ходи, оппонент выразил явное недовольство. Тут моё чувство выигранной партии подтвердилось. Дальше у меня был чистейший голдфиш, колода играла за меня, а я просто смотрел чо за накур у оппонента. 1 - 0 2.2 партия: Увидел красный цвет, пару неприятных карт, засайдился. Оппонент ходит первый. Опять муллиган в 5 с его стороны. Жадный ход с моей стороны на 2 ход, за который меня мгновенно наказали. Из-за этого партия длилась дольше, чем должна была. Победа. Не понял, чем оппонент выигрывает, спросил у него, как я понял он дохуя дровается и дальше что(?), но хз, феек таким не трахнешь. 2 - 0 Имея за плечами 2 победы (очень легкие, но все же победы), уже уверенность прохождения в топ 8 чуть выросла. Дальше меня устраивают из трех следующих раундов победа + ничья. Итого: 2-0 (6 поинтов) 3 раунд Fam'ы: 3.1 партия: Оппонент ходит первым, вижу фамов. У моей колоды положительный винрейт с фамами, но у меня как у игрока винрейта никакого, я ни разу с ними не тестился и не совсем понимал как отыгрывать, В итоге всех моих феек и ниндзя поконтрили/вернули в руку, у оппонента 30+ хп, меня догрызают летунами В ахуе от духоты матчапа, сажусь сайдиться. Взял 2 релика (карта, которая должна убивать фамов) и еще одну опциональную (изгоните существо), на всякий случай, которая мне очень нравится. Избавился в сайде не от тех карт, но это из-за неопытности в данном матчапе. 1-0 3.2 партия. Вижу в стартовой руке релик(!), оставляем похуй. Остров -> Релик -> Ходи. Понимал, что нужно релик выставлять мгновенно, потому что у оппоненты в данных цветах, не будет дальнейшего ответа на него. Партия идет, релик работает. Появляется в какой-то момент слишком много хилящих хуесосов с его стороны, с которыми я ничего не могу сделать. Ситуация в итоге была такая: Конец моего хода - у оппонента 4 хп, начало моего хода - у оппонента 12 хп. И я это существо ебаное, которое хилит в рот ебал. НО тут достается с топ дека та самая опциональная карта, которая ломает ему хил и я добиваю его. 1-1 3.3 партия: Партия началась за 6 минут до окончания раунда, понимал, что не успеем доиграть и все закончится ничьей. Так и произошло, закончили 1-1 Итого: 2-0-1 (7 поинтов) В ахуе от духоты этой колоды иду есть. Из двух раундов мне достаточно выиграть один, чтобы попасть в топ 8. Когда ел, показали паринги, увидел, что против меня опять блять поставили игрока с фамами, в ахуе от такой удачи иду обратно"

if __name__ == "__main__":
    # news_tts = NewsTts()
    # news_summarizer = NewsSummarizer()

    r = 'http://moymotor.ru'
    all_urls = []
    parser = Parser(r)
    parser.get_all_links(r)

    # parser.write_to_file([r])

    # extr_text = news_summarizer.get_text_extract_sum(SAMPLE_TEXT, n=3)
    # abst_text = news_summarizer.get_text_abstract_sum(extr_text)
    #
    # audio_sum = news_tts.get_audio(extr_text)
    # # news_tts.play_audio(audio_sum)
    # news_tts.save_wav_of_tts(audio_sum)

    # print("Original: ", len(SAMPLE_TEXT), "symbols\n", SAMPLE_TEXT.replace(". ", ".\n"))
    # print("\nExtracted summary:", len(extr_text), "symbols\n", extr_text.replace(". ", ".\n"))
    # print("\nAbstracted summary:", len(abst_text[0]), "symbols\n", abst_text)
