package commands;

import managers.CollectionManager;
import models.LabWork;
import utility.Console;

/**
 * Вывести любой объект из коллекции, значение поля coordinates которого является минимальным
 */
public class MinByCoordinates extends Command {
    private final Console console;
    private final CollectionManager collectionManager;

    public MinByCoordinates(Console console, CollectionManager collectionManager) {
        super("min_by_coordinates", "вывести любой объект из коллекции, значение поля coordinates которого является минимальным");
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
        LabWork min = null;
        for (LabWork e : collectionManager.getCollection()) {
            if (min==null || min.getCoordinates().getx() > e.getCoordinates().getx()) min = e;
        }
        if (min == null) {
            console.println("Лабораторных не обнаружено.");
        } else {
            console.println(min.toString() + "\n");
        }
        return true;
    }
}