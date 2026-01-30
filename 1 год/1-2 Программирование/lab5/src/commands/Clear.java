package commands;

import managers.CollectionManager;
import models.LabWork;
import utility.Console;

/**
 * Очистить коллекцию
 */
public class Clear extends Command {
    private final Console console;
    private final CollectionManager collectionManager;

    public Clear(Console console, CollectionManager collectionManager) {
        super("clear", "очистить коллекцию");
        this.console = console;
        this.collectionManager = collectionManager;
    }
    /**
     * Выполняет команду
     * @return Успешность выполнения команды.
     */
    @Override
    public boolean apply(String[] arguments) {
        if (!arguments[1].isEmpty()) {
            console.println("Неправильное количество аргументов!");
            console.println("Использование: '" + getName() + "'");
            return false;
        }
        while (collectionManager.getCollection().size() > 0) {
            LabWork labWork = collectionManager.getCollection().lastElement();
            collectionManager.remove(labWork.getId());
        }
        collectionManager.update();
        console.println("Коллекция очищена!");
        return true;
    }
}