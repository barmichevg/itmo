package commands;

import managers.CollectionManager;
import models.Ask;
import models.LabWork;
import utility.Console;

/**
 * Добавить новый элемент в коллекцию
 */
public class Add extends Command {
    private final Console console;
    private final CollectionManager collectionManager;

    public Add(Console console, CollectionManager collectionManager) {
        super("add {element}", "добавить новый элемент в коллекцию");
        this.console = console;
        this.collectionManager = collectionManager;
    }
    /**
     * Выполняет команду
     * @return Успешность выполнения команды.
     */
    @Override
    public boolean apply(String[] arguments) {
        try {
            if (!arguments[1].isEmpty()) {
                console.println("Неправильное количество аргументов!");
                console.println("Использование: '" + getName() + "'");
                return false;
            }
            console.println("* Создание новой Лабораторной:");
            LabWork d = Ask.askLabWork(console, collectionManager);

            if (d != null && d.validate()) {
                collectionManager.add(d);
                console.println("Лабораторная успешно добавлена!");
                return true;
            } else {
                console.printError("Поля Лабораторной не валидны! Лабораторная не создана!");
                return false;
            }
        } catch (Ask.AskBreak e) {
            console.println("Отмена...");
            return false;
        }
    }
}