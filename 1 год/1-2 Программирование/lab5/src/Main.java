import commands.*;
import managers.*;
import utility.StandardConsole;
import utility.Runner;

public class Main {
    public static void main(String[] args) {
        StandardConsole console = new StandardConsole();

        if (args.length == 0) {
            console.println("Введите имя загружаемого файла как аргумент командной строки");
            System.exit(1);
        }

        FileManager fileManager = new FileManager(args[0], console);
        CollectionManager collectionManager = new CollectionManager(fileManager);
        if (!collectionManager.loadCollection()) {
            System.exit(1);
        }

        CommandManager commandManager = new CommandManager() {{
            register("help", new Help(console, this));
            register("info", new Info(console, collectionManager));
            register("show", new Show(console, collectionManager));
            register("add", new Add(console, collectionManager));
            register("update", new Update(console, collectionManager));
            register("remove_by_id", new RemoveById(console, collectionManager));
            register("clear", new Clear(console, collectionManager));
            register("save", new Save(console, collectionManager));
            register("execute_script", new ExecuteScript(console));
            register("exit", new Exit(console));
            register("remove_at", new RemoveAt(console, collectionManager));
            register("shuffle", new Shuffle(console, collectionManager));
            register("reorder", new Reorder(console, collectionManager));
            register("min_by_coordinates", new MinByCoordinates(console, collectionManager));
            register("filter_less_than_minimal_point", new FilterLessThanMinimalPoint(console, collectionManager));
            register("print_ascending", new PrintAscending(console, collectionManager));
        }
        };

        new Runner(console, commandManager).interactiveMode();
    }
}
