package commands;

import managers.CollectionManager;
import models.LabWork;
import utility.Console;
import models.Ask;

import java.util.Collections;

/**
 * Обновить значение элемента коллекции, id которого равен заданному
 */
public class Update extends Command {
    private final Console console;
    private final CollectionManager collectionManager;

    public Update(Console console, CollectionManager collectionManager) {
        super("update <ID> {element}", "обновить значение элемента коллекции по ID");
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
            if (arguments[1].isEmpty()) {
                console.println("Неправильное количество аргументов!");
                console.println("Использование: '" + getName() + "'");
                return false;
            }
            int id = -1;
            try { id = Integer.parseInt(arguments[1].trim()); } catch (NumberFormatException e) { console.println("ID не распознан"); return false; }

            if (collectionManager.byId(id) == null || !collectionManager.getCollection().contains(collectionManager.byId(id))) {
                console.println("не существующий ID");
                return false;
            }
            console.println("* Обновление Лабораторной:");
            LabWork d = Ask.askLabWork(console, collectionManager);
            if (d != null && d.validate()) {
                collectionManager.add(d);
                collectionManager.update();

                LabWork old = collectionManager.byId(id);
                collectionManager.swap(d.getId(), id);
                collectionManager.update();

                collectionManager.remove(old.getId());
                collectionManager.update();
                return true;
            } else {
                console.println("Поля Лабораторной не валидны! Лабораторная не обновлена!");
                return false;
            }
        } catch (Ask.AskBreak e) {
            console.println("Отмена...");
            return false;
        }
    }
}