package common.command;

import java.io.Serializable;

/**
 * Класс объект-запрос команды, содержащий имя команды и её аргумент.
 */
public class CommandRequest implements Serializable {
    private String commandName;
    private Object argument;

    /**
     * Конструктор
     * @param commandName имя команды
     * @param argument аргумент
     */
    public CommandRequest(String commandName, Object argument) {
        this.commandName = commandName;
        this.argument = argument;
    }

    public String getCommandName() { return commandName; }
    public Object getArgument() { return argument; }
}