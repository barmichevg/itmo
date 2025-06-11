package common.command;

import java.io.Serializable;

/**
 * Класс объект-запрос команды, содержащий имя команды и её аргумент.
 */
public class CommandRequest implements Serializable {
    private final String commandName;
    private final Object argument;
    private final String username;
    private final String password;

    /**
     * Конструктор
     * @param commandName имя команды
     * @param argument аргумент
     * @param username имя пользователя
     */
    public CommandRequest(String commandName, Object argument, String username, String password) {
        this.commandName = commandName;
        this.argument = argument;
        this.username = username;
        this.password = password;
    }

    public String getCommandName() {return commandName;}
    public Object getArgument() {return argument;}
    public String getUsername() {return username;}
    public String getPassword() {return password;}
}
