package commands;

import models.LabWork;
import managers.CollectionManager;
import utility.Console;

import java.util.Comparator;
import java.util.Vector;

/**
 * Вывести элементы коллекции в порядке возрастания
 */
public class PrintAscending extends Command {
    private final Console console;
    private final CollectionManager collectionManager;

    public PrintAscending(Console console, CollectionManager collectionManager) {
        super("print_ascending", "вывести элементы коллекции в порядке возрастания");
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
        Vector<LabWork> CollectionCopy = collectionManager.getCollection();
        Comparator<LabWork> comparator = new Comparator<LabWork>() {
            @Override
            public int compare(LabWork o1, LabWork o2) {
                return Integer.compare(o1.getId(), o2.getId());
            }
        };
        CollectionCopy.sort(comparator);
        for (LabWork labWork : CollectionCopy) {
            console.println(labWork.toString());
        }
        return true;
    }
}