package common.command;

import java.io.Serializable;

/**
 * Класс объект-ответ сервера, содержащий текстовое сообщение с результатом выполнения команды.
 */
public class CommandResponse implements Serializable {
    private final String message;

    /**
     * Конструктор.
     * @param message передаваемое сообщение.
     */
    public CommandResponse(String message) {this.message = message;}

    /**
     * @return String передаваемое сообщение.
     */
    public String getMessage() {
        return message;
    }
}
