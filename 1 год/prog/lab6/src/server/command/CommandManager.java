package server.command;

import common.command.CommandRequest;
import common.models.LabWork;
import server.util.CSVHandler;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.*;
import java.util.stream.*;

/**
 * Класс для выполнения всех команд, полученных от клиента.
 */
public class CommandManager {
    private static final Logger logger = LoggerFactory.getLogger(CommandManager.class);
    private static final List<LabWork> collection = new Vector<>();
    private static int idCounter = 1;
    private static final Date initTime = new Date();
    private static Date lastSaveTime = null;

    /**
     * Обрабатывает входящий запрос команды от клиента.
     * @param request объект запроса с именем команды и аргументами
     * @return строка с результатом выполнения команды
     */
    public static String handle(CommandRequest request) {
        logger.debug("Получена команда: {}", request.getCommandName());
        String commandName = request != null ? request.getCommandName() : null;
        Object argument = request != null ? request.getArgument() : null;
        if (commandName == null) return "Ошибка: команда не распознана.";

        switch (commandName) {
            case "help" -> {
                return """
                        info                                     вывести информацию о коллекции
                        remove_at <index>                        удалить элемент по индексу
                        execute_script <file_name>               исполнить скрипт из указанного файла
                        remove_by_id <ID>                        удалить элемент по ID
                        save                                     сохранить коллекцию в файл
                        exit                                     завершить клиентское приложение
                        add {element}                            добавить новый элемент
                        print_ascending                          вывести элементы в порядке возрастания
                        min_by_coordinates                       вывести элемент с минимальными координатами
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
                return "Тип коллекции: Vector\n" +
                        "Количество элементов: " + collection.size() + "\n" +
                        "Дата инициализации: " + initTime + "\n" +
                        "Последнее сохранение: " + (lastSaveTime != null ? lastSaveTime : "ещё не сохранялось");
            }
            case "show" -> {
                if (collection.isEmpty()) return "Коллекция пуста.";
                String header = String.format(
                        "%-4s | %-15s | %-15s | %-30s | %-13s | %-20s | %-13s | %-10s | %-20s",
                        "ID", "Name", "Coordinates", "Creation Date", "MinPoint", "Description", "TunedInWorks", "Difficulty", "Discipline");
                String separator = "-".repeat(header.length());
                String body = collection.stream()
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
            case "save" -> {
                CSVHandler.saveToCSV("test.csv", getCollectionSorted());
                updateSaveTime();
                return "Коллекция сохранена в файл.";
            }
            case "add" -> {
                if (!(argument instanceof LabWork)) return "Ошибка: ожидается объект LabWork";
                LabWork lw = (LabWork) argument;
                if (lw.getId() == null || lw.getId() <= 0) {
                    lw.setId(idCounter++);
                } else {
                    if (lw.getId() >= idCounter) {
                        idCounter = lw.getId() + 1;
                    }
                }
                lw.setCreationDate(java.time.LocalDateTime.now());
                collection.add(lw);
                return "Элемент добавлен.";
            }
            case "update" -> {
                if (!(argument instanceof Map)) return "Ошибка: ожидалась пара (id, LabWork)";
                Map<String, Object> args = (Map<String, Object>) argument;
                int id = (Integer) args.get("id");
                LabWork updated = (LabWork) args.get("element");
                for (int i = 0; i < collection.size(); i++) {
                    if (collection.get(i).getId() == id) {
                        updated.setId(id);
                        updated.setCreationDate(collection.get(i).getCreationDate());
                        collection.set(i, updated);
                        return "Элемент с id=" + id + " обновлён.";
                    }
                }
                return "Элемент с id=" + id + " не найден.";
            }
            case "remove_by_id" -> {
                int id = (Integer) argument;
                boolean removed = collection.removeIf(l -> l.getId() == id);
                return removed ? "Элемент удалён." : "Элемент с id=" + id + " не найден.";
            }
            case "remove_at" -> {
                int index = (Integer) argument;
                if (index < 0 || index >= collection.size()) return "Индекс вне диапазона.";
                collection.remove(index);
                return "Элемент на позиции " + index + " удалён.";
            }
            case "shuffle" -> {
                Collections.shuffle(collection);
                return "Коллекция перемешана.";
            }
            case "reorder" -> {
                Collections.reverse(collection);
                return "Коллекция отсортирована в обратном порядке.";
            }
            case "clear" -> {
                collection.clear();
                return "Коллекция очищена.";
            }
            case "min_by_coordinates" -> {
                if (collection.isEmpty()) return "Коллекция пуста.";
                String header = String.format(
                        "%-4s | %-15s | %-15s | %-30s | %-13s | %-20s | %-13s | %-10s | %-20s",
                        "ID", "Name", "Coordinates", "Creation Date", "MinPoint", "Description", "TunedInWorks", "Difficulty", "Discipline");
                String separator = "-".repeat(header.length());
                return collection.stream()
                        .min(Comparator.comparing(l -> l.getCoordinates().getX() + l.getCoordinates().getY()))
                        .map(lw -> header + "\n" + separator + "\n" + String.format(
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
                        .orElse("Коллекция пуста");
            }
            case "filter_less_than_minimal_point" -> {
                long threshold = (Long) argument;
                List<LabWork> filtered = collection.stream()
                        .filter(l -> l.getMinimalPoint() < threshold)
                        .sorted()
                        .collect(Collectors.toList());
                if (filtered.isEmpty()) return "Нет элементов с minimalPoint < " + threshold;
                String header = String.format(
                        "%-4s | %-15s | %-15s | %-30s | %-13s | %-20s | %-13s | %-10s | %-20s",
                        "ID", "Name", "Coordinates", "Creation Date", "MinPoint", "Description", "TunedInWorks", "Difficulty", "Discipline");
                String separator = "-".repeat(header.length());
                String body = filtered.stream()
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
            case "print_ascending" -> {
                if (collection.isEmpty()) return "Коллекция пуста.";
                String header = String.format(
                        "%-4s | %-15s | %-15s | %-30s | %-13s | %-20s | %-13s | %-10s | %-20s",
                        "ID", "Name", "Coordinates", "Creation Date", "MinPoint", "Description", "TunedInWorks", "Difficulty", "Discipline");
                String separator = "-".repeat(header.length());
                String body = collection.stream()
                        .sorted()
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
            default -> {
                return "Неизвестная команда: " + commandName;
            }
        }
    }

    /**
     * Возвращает отсортированную коллекцию.
     * @return отсортированный список объектов LabWork
     */
    public static List<LabWork> getCollectionSorted() {
        return collection.stream()
                .sorted()
                .collect(Collectors.toList());
    }

    /**
     * Обновляет время последнего сохранения коллекции.
     */
    public static void updateSaveTime() {
        lastSaveTime = new Date();
    }
}