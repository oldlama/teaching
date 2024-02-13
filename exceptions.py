class GetRespStatusBut200Error(Exception):
    """Исключение срабатывает, если статус ответа на get-запрос не равен 200."""

class ProgramRunVariantError(Exception):
    "Исключение срабатывает при некорректном вводе пользователем варианта выполнения программы."