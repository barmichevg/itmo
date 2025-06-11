package server.command;

import common.command.CommandRequest;
import common.models.LabWork;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import server.util.DatabaseManager;
import server.util.LabWorkDAO;

import java.sql.Connection;
import java.util.*;
import java.util.concurrent.ForkJoinPool;
import java.util.concurrent.RecursiveTask;
import java.util.stream.Collectors;

public class CommandManager {
    private static final Logger logger = LoggerFactory.getLogger(CommandManager.class);
    private static final List<LabWork> collection = new Vector<>();
    private static final Date initTime = new Date();
    private static Date lastSaveTime = null;
    private static Connection dbConnection;

    public static void initialize(Connection connection) {
        dbConnection = connection;
        synchronized (collection) {
            collection.clear();
            collection.addAll(LabWorkDAO.loadAllLabWorks(connection));
        }
        logger.info("Инициализация CommandManager завершена. Загружено {} элементов.", collection.size());
    }

    public static String handle(CommandRequest request) {
        return ForkJoinPool.commonPool().invoke(new CommandTask(request));
    }

    public static Connection getDbConnection() {
        return dbConnection;
    }

    public static void updateSaveTime() {
        lastSaveTime = new Date();
    }

    private static class CommandTask extends RecursiveTask<String> {
        private final CommandRequest request;

        public CommandTask(CommandRequest request) {
            this.request = request;
        }

        @Override
        protected String compute() {
            logger.debug("Получена команда: {}", request.getCommandName());
            if (request == null || request.getCommandName() == null || request.getUsername() == null) {
                return "Ошибка: команда или пользователь не распознаны.";
            }

            String commandName = request.getCommandName();
            Object argument = request.getArgument();
            String username = request.getUsername();

            switch (commandName) {
                case "help" -> {
                    return """
                            info                                     вывести информацию о коллекции
                            remove_at <index>                        удалить элемент по индексу
                            execute_script <file_name>               исполнить скрипт из указанного файла
                            remove_by_id <ID>                        удалить элемент по ID
                            exit                                     завершить клиентское приложение
                            add {element}                            добавить новый элемент
                            print_ascending                          вывести элементы в порядке возрастания
                            min_by_coordinates                       вывести элемент с минимальными координатами
                            save                                     в сохранить коллекцию в бд
                            shuffle                                  перемешать элементы коллекции
                            show                                     вывести все элементы коллекции
                            help                                     вывести справку по командам
                            update <ID> {element}                    обновить элемент по ID
                            clear                                    очистить коллекцию
                            reorder                                  отсортировать в обратном порядке
                            filter_less_than_minimal_point <value>   фильтровать по minimalPoint
                            """;
                }
                case "info" -> {
                    synchronized (collection) {
                        return "Тип коллекции: Vector\n" +
                                "Количество элементов: " + collection.size() + "\n" +
                                "Дата инициализации: " + initTime + "\n" +
                                "Последнее сохранение: " + (lastSaveTime != null ? lastSaveTime : "ещё не сохранялось");
                    }
                }
                case "show" -> {
                    synchronized (collection) {
                        return formatCollection(collection);
                    }
                }
                case "save" -> {
                    synchronized (collection) {
                        boolean success = DatabaseManager.saveCollection(collection);
                        if (success) {
                            updateSaveTime();
                            return "Коллекция успешно сохранена в базе данных.";
                        } else {
                            return "Ошибка при сохранении коллекции в базу данных.";
                        }
                    }
                }
                case "add" -> {
                    if (!(argument instanceof LabWork lw)) return "Ошибка: ожидается объект LabWork";
                    LabWork inserted = LabWorkDAO.insertLabWork(dbConnection, lw, username);
                    if (inserted != null) {
                        synchronized (collection) {
                            collection.add(inserted);
                        }
                        return "Элемент добавлен.";
                    } else return "Ошибка при добавлении элемента в БД.";
                }
                case "update" -> {
                    if (!(argument instanceof Map args) || !args.containsKey("id") || !args.containsKey("element"))
                        return "Ошибка: ожидалась пара (id, LabWork)";
                    int id = (Integer) args.get("id");
                    LabWork updated = (LabWork) args.get("element");
                    boolean success = LabWorkDAO.updateLabWork(dbConnection, id, updated, username);
                    if (success) {
                        synchronized (collection) {
                            collection.removeIf(lw -> lw.getId() == id);
                            collection.add(updated);
                        }
                        return "Элемент с id=" + id + " обновлён.";
                    } else return "Элемент не обновлён. Проверьте права доступа или существование элемента.";
                }
                case "remove_by_id" -> {
                    int id = (Integer) argument;
                    boolean success = LabWorkDAO.removeById(dbConnection, id, username);
                    if (success) {
                        synchronized (collection) {
                            collection.removeIf(lw -> lw.getId() == id);
                        }
                        return "Элемент удалён.";
                    } else return "Элемент с id=" + id + " не найден или доступ запрещён.";
                }
                case "remove_at" -> {
                    int index = (Integer) argument;
                    synchronized (collection) {
                        if (index < 0 || index >= collection.size()) return "Индекс вне диапазона.";
                        LabWork target = collection.get(index);
                        boolean success = LabWorkDAO.removeById(dbConnection, target.getId(), username);
                        if (success) {
                            collection.remove(index);
                            return "Элемент на позиции " + index + " удалён.";
                        } else return "Удаление не выполнено. Нет прав доступа.";
                    }
                }
                case "shuffle" -> {
                    synchronized (collection) {
                        Collections.shuffle(collection);
                        return "Коллекция перемешана.";
                    }
                }
                case "reorder" -> {
                    synchronized (collection) {
                        Collections.reverse(collection);
                        return "Коллекция отсортирована в обратном порядке.";
                    }
                }
                case "clear" -> {
                    boolean success = LabWorkDAO.clearUserEntries(dbConnection, username);
                    if (success) {
                        synchronized (collection) {
                            collection.removeIf(lw -> username.equals(lw.getOwner()));
                        }
                        return "Все ваши элементы удалены.";
                    } else return "Ошибка при удалении ваших элементов.";
                }
                case "min_by_coordinates" -> {
                    synchronized (collection) {
                        return collection.stream()
                                .min(Comparator.comparing(lw -> lw.getCoordinates().getX() + lw.getCoordinates().getY()))
                                .map(lw -> formatCollection(List.of(lw)))
                                .orElse("Коллекция пуста");
                    }
                }
                case "filter_less_than_minimal_point" -> {
                    long threshold = (Long) argument;
                    synchronized (collection) {
                        List<LabWork> filtered = collection.stream()
                                .filter(lw -> lw.getMinimalPoint() < threshold)
                                .collect(Collectors.toList());
                        return formatCollection(filtered);
                    }
                }
                case "print_ascending" -> {
                    synchronized (collection) {
                        return formatCollection(collection.stream().sorted().collect(Collectors.toList()));
                    }
                }
                default -> {
                    return "Неизвестная команда: " + commandName;
                }
            }
        }
    }

    private static String formatCollection(List<LabWork> data) {
        if (data.isEmpty()) return "Коллекция пуста.";
        String header = String.format(
                "%-4s | %-15s | %-15s | %-30s | %-13s | %-20s | %-13s | %-10s | %-20s",
                "ID", "Name", "Coordinates", "Creation Date", "MinPoint", "Description", "TunedInWorks", "Difficulty", "Discipline");
        String separator = "-".repeat(header.length());
        String body = data.stream()
                .map(lw -> String.format(
                        "%-4d | %-15s | (%3d, %6.2f)   | %-30s | %-13d | %-20s | %-13s | %-10s | %-20s",
                        lw.getId(),
                        lw.getName(),
                        lw.getCoordinates().getX(),
                        lw.getCoordinates().getY(),
                        lw.getCreationDate(),
                        lw.getMinimalPoint(),
                        lw.getDescription() != null ? lw.getDescription() : "null",
                        lw.getTunedInWorks() != null ? lw.getTunedInWorks().toString() : "null",
                        lw.getDifficulty().name(),
                        lw.getDiscipline() != null ? lw.getDiscipline().toString() : "null"
                ))
                .collect(Collectors.joining("\n"));
        return header + "\n" + separator + "\n" + body;
    }
}

