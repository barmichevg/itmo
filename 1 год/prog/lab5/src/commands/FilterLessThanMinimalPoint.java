package commands;

import managers.CollectionManager;
import models.LabWork;
import utility.Console;

import java.util.List;
import java.util.stream.Collectors;

/**
 * Вывести элементы, значение поля minimalPoint которых меньше заданного
 */
public class FilterLessThanMinimalPoint extends Command {
    private final Console console;
    private final CollectionManager collectionManager;

    public FilterLessThanMinimalPoint(Console console, CollectionManager collectionManager) {
        super("filter_less_than_minimal_point <minimalPoint>", "вывести элементы, значение поля minimalPoint которых меньше заданного");
        this.console = console;
        this.collectionManager = collectionManager;
    }
    /**
     * Выполняет команду
     * @return Успешность выполнения команды.
     */
    @Override
    public boolean apply(String[] arguments) {
        if (arguments[1].isEmpty()) {
            console.println("Неправильное количество аргументов!");
            console.println("Использование: '" + getName() + "'");
            return false;
        }
        Double minimalPoint = Double.parseDouble(arguments[1]);
        List<LabWork> LabWork = filterLessThanMinimalPoint(minimalPoint);
        if (LabWork.isEmpty()) {console.println("Лабораторных с minimalPoint меньше " + minimalPoint + " не обнаружено.");}
        else {
            console.println("Лабораторных с minimalPoint меньше " + minimalPoint + " встречается " + LabWork.size() + " раз.\n");
            LabWork.forEach(console::println);
        }
        return true;
    }
    private List<LabWork> filterLessThanMinimalPoint(Double minimalPoint) {
        return collectionManager.getCollection().stream()
                .filter(labWork -> (labWork.getMinimalPoint() < (minimalPoint)))
                .collect(Collectors.toList());
    }
}