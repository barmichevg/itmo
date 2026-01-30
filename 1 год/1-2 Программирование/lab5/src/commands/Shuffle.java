package commands;

import managers.CollectionManager;
import utility.Console;

/**
 * Перемешать элементы коллекции в случайном порядке
 */
public class Shuffle extends Command {
    private final Console console;
    private final CollectionManager collectionManager;

    public Shuffle(Console console, CollectionManager collectionManager) {
        super("shuffle", "перемешать элементы коллекции в случайном порядке");
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
        collectionManager.shuffle();
        return true;
    }
}
