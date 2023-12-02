import datetime
from typing import Generator
from langchain.chat_models.gigachat import GigaChat
from openpyxl import Workbook
from chat import Chat


def try_parse_time(date_str: str) -> datetime.time | None:
    try:
        try:
            dt = datetime.datetime.strptime(date_str, '%H:%M:%S')
        except ValueError:
            dt = datetime.datetime.strptime(date_str, '%M:%S')
        return dt.time()
    except ValueError:
        return None


def parse_dialogs(lines: list[str]) -> Generator[dict[str, any], None, None]:
    """
    Функция для выделения отдельных диалогов из транскрипта дня.

    Формат транскрипта:
    00:00:30
    <Сотрудник>
    Это наше расписание которого мы придерживаемся
    <Клиент>
    У вас нет расписания?
    Как жаль
    00:01:03
    <Пробельная строка>
    <Дальнейшие диалоги в том же формате>
    """

    time_start = None
    barista_name = None
    text = []
    ptr = 0
    while ptr < len(lines):
        line = lines[ptr].strip()
        ptr += 1
        if len(line) == 0:
            continue
        time = try_parse_time(line)
        if time is not None:
            if time_start is None:
                time_start = time
            else:
                yield {"start": time_start, "name": barista_name, "end": time, "text": text}
                time_start = None
                barista_name = None
                text = []
            continue

        if line == "<баристы>" or line == "<Баристы>":
            while try_parse_time(lines[ptr].strip()) is None:
                ptr += 1
            ptr += 1
            time_start = None
            barista_name = None
            text = []
            continue
        if line[0] == "<" and line[-1] == ">":
            if barista_name is None:
                barista_name = line[1:-1]
            # continue
        text.append(line)


def process_dialogs(
    sber_chat: GigaChat,
    input_file: str,
    output_file: str
):
    wb = Workbook()
    additional_sell_fact = Chat(
        "Ты умный ассистент, который умеет определять, предложили ли клиенту кофейни купить что-то дополнительное.",
        'Напиши "1", если клиенту предложили купить что-то дополнительное, иначе - "0". Вот диалог сотрудника с клиентом:"{message}"',
        sber_chat
    )
    additional_sell_result = Chat(
        "Ты умный ассистент, который умеет определять, решил ли клиент кофейни купить что-то дополнительное.",
        'Напиши "1", если клиент решил купить что-то дополнительное, иначе - "0". Вот диалог сотрудника с клиентом:"{message}"',
        sber_chat
    )
    additional_sell_wording = Chat(
        "Ты умный ассистент, который умеет определять, предложили ли клиенту кофейни купить что-то дополнительное.",
        'Выпиши из диалога формулировку, с которой клиенту предложили купить что-то дополнительное. Вот диалог сотрудника с клиентом:"{message}"',
        sber_chat
    )
    additional_sell_item = Chat(
        "Ты умный ассистент и лаконичный, который умеет определять, предложили ли клиенту кофейни купить что-то дополнительное.",
        'Выпиши, что именно предложили купить клиенту. Вот диалог сотрудника с клиентом:"{message}"',
        sber_chat
    )

    upsell_fact = Chat(
        "Ты умный ассистент, который умеет определять, предложили ли клиенту кофейни купить что-то дороже, чем то что он хотел изначально.",
        'Напиши "1", если клиенту предложили купить что-то дороже, чем то, что он хотел изначально, иначе - "0". Вот диалог сотрудника с клиентом:"{message}"',
        sber_chat
    )
    upsell_result = Chat(
        "Ты умный ассистент, который умеет определять, предложили ли клиенту кофейни купить что-то дороже, чем то что он хотел изначально.",
        'Напиши "1", если клиент согласился купить что-то дороже, чем то, что он хотел изначально, иначе - "0". Вот диалог сотрудника с клиентом:"{message}"',
        sber_chat
    )
    upsell_item = Chat(
        "Ты умный и лаконичный ассистент, который умеет определять, предложили ли клиенту кофейни купить что-то дороже, чем то что он хотел изначально.",
        'Выпиши, что именно решил купить человек вместо изначального заказа. Вот диалог сотрудника с клиентом:"{message}"',
        sber_chat
    )

    mobile_fact = Chat(
        "Ты умный ассистент, который умеет определять, предложили ли клиенту кофейни воспользоваться мобильным приложением.",
        'Напиши "1", если клиенту предложили воспользоваться мобильным приложением, иначе - "0". Вот диалог сотрудника с клиентом:"{message}"',
        sber_chat
    )

    comments = Chat(
        "Ты умный ассистент, который умеет определять, произошли ли в диалоге клиента кофейни и сотрудника нужные собития.",
        '''
Перечисли события из списка ниже, если они произошли в диалоге сотрудника с клиентом:
Клиент попросил что-то, а этого не оказалось в наличии. Укажи что именно.
Сломалась какая-то техника. Укажи какая именно.
Вот диалог сотрудника с клиентом:"{message}"
        ''',
        sber_chat
    )
    with open(input_file, "r") as file:
        lines = file.readlines()

    ws = wb.active
    ws.append([
        "Время чека",
        "Сотрудник",
        "Допродажи",
        "Успех допродажи",
        "Формулировка допродажи",
        "Что допродали",
        "Upsell",
        "Успех upsell",
        "Upsell чего",
        "Мобильное приложение",
        "Комментарии"
    ])
    for dialog in parse_dialogs(lines):
        text = dialog["text"]
        add_fact = additional_sell_fact.answer(text)
        if "1" in add_fact:
            add_fact = 1
        else:
            add_fact = 0

        if add_fact == 1:
            add_res = additional_sell_result.answer(text)
            if "1" in add_res:
                add_res = 1
            else:
                add_res = 0
            add_word = additional_sell_wording.answer(text)
        else:
            add_res = 0
            add_word = "-"

        if add_res == 1:
            add_item = additional_sell_item.answer(text)
        else:
            add_item = "-"

        up_fact = upsell_fact.answer(text)
        if "1" in up_fact:
            up_fact = 1
        else:
            up_fact = 0

        if up_fact == 1:
            up_res = upsell_result.answer(text)
            if "1" in up_res:
                up_res = 1
            else:
                up_res = 0
        else:
            up_res = 0

        if up_res == 1:
            up_item = upsell_item.answer(text)
        else:
            up_item = "-"

        mobile = mobile_fact.answer(text)
        if "1" in mobile:
            mobile = 1
        else:
            mobile = 0

        comments_text = comments.answer(text)
        if len(comments_text) == 0:
            comments_text = "-"
        elif isinstance(comments_text, list):
            comments_text = ", ".join(comments_text)

        ws.append([
            dialog['end'],
            dialog['name'],
            add_fact,
            add_res,
            add_word,
            add_item,
            up_fact,
            up_res,
            up_item,
            mobile,
            comments_text
        ])
    wb.save(output_file)
    print(f"------ Report saved to {output_file} ------")
