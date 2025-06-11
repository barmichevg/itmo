package exceptions;

/**
 * Исключение, вызываемое при необработанном нарушении условий полей.
 */

public class ValidationException extends RuntimeException {
    String name;

    public ValidationException(String name) {
        super();
        this.name = name;
    }

    @Override
    public String getMessage() {
        return "Ошибка при загрузке данных из файла. Объект класса " + name + " введен неверно.";
    }
}