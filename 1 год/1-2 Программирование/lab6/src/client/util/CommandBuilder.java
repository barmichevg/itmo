package client.util;

import client.util.LabWorkFactory;
import common.command.CommandRequest;
import common.models.Coordinates;
import common.models.Difficulty;
import common.models.Discipline;
import common.models.LabWork;

import java.util.*;

/**
 * Класс, отвечающий за формирование команд на клиенте
 * на основе пользовательского ввода или строк из скрипта.
 */
public class CommandBuilder {
    private static final Scanner scanner = new Scanner(System.in);

    private static boolean isScriptMode = false;

    public static void enableScriptMode() {
        isScriptMode = true;
    }

    public static void disableScriptMode() {
        isScriptMode = false;
    }

    /**
     * Строит объект запроса команды на основе строки.
     * Поддерживает интерактивный и скриптовый режим.
     * @param input команда или команда с аргументами, разделёнными | (для скриптов)
     * @return объект CommandRequest
     */
    public static CommandRequest build(String input) {
        String[] parts = input.split("\\|", -1);
        String command = parts[0].trim().toLowerCase();

        try {
            switch (command) {
                case "add":
                    if (isScriptMode) {
                        return new CommandRequest("add", parseLabWork(parts, 1));
                    } else {
                        return new CommandRequest("add", LabWorkFactory.createLabWork());
                    }
                case "update":
                    if (isScriptMode) {
                        int id = Integer.parseInt(parts[1].trim());
                        LabWork lw = parseLabWork(parts, 2);
                        Map<String, Object> args = new HashMap<>();
                        args.put("id", id);
                        args.put("element", lw);
                        return new CommandRequest("update", args);
                    } else {
                        System.out.print("Введите id для обновления: ");
                        int id = Integer.parseInt(scanner.nextLine().trim());
                        LabWork updated = LabWorkFactory.createLabWork();
                        Map<String, Object> args = new HashMap<>();
                        args.put("id", id);
                        args.put("element", updated);
                        return new CommandRequest("update", args);
                    }
                case "remove_by_id":
                case "remove_at":
                    if (isScriptMode) {
                        return new CommandRequest(command, Integer.parseInt(parts[1].trim()));
                    } else {
                        System.out.print("Введите целочисленный id или index: ");
                        return new CommandRequest(command, Integer.parseInt(scanner.nextLine().trim()));
                    }
                case "filter_less_than_minimal_point":
                    if (isScriptMode) {
                        return new CommandRequest(command, Long.parseLong(parts[1].trim()));
                    } else {
                        System.out.print("Введите значение minimalPoint: ");
                        return new CommandRequest(command, Long.parseLong(scanner.nextLine().trim()));
                    }
                case "execute_script":
                    if (isScriptMode) {
                        return new CommandRequest("execute_script", parts[1].trim());
                    } else {
                        System.out.print("Введите имя файла скрипта: ");
                        String filename = scanner.nextLine().trim();
                        return new CommandRequest("execute_script", filename);
                    }
                case "shuffle":
                case "clear":
                case "reorder":
                case "print_ascending":
                case "min_by_coordinates":
                case "info":
                case "show":
                case "help":
                case "save":
                    return new CommandRequest(command, null);
            }
        } catch (Exception e) {
            if (!isScriptMode) {
                System.out.println("Ошибка при разборе команды: " + e.getMessage());
            }
        }
        return null;
    }

    /**
     * Вспомогательный метод для парсинга LabWork из аргументов
     * @param parts массив строк аргументов
     * @param start индекс, с которого начинаются поля LabWork
     * @return готовый объект LabWork
     */
    private static LabWork parseLabWork(String[] parts, int start) {
        LabWork lw = new LabWork();
        lw.setName(parts[start].trim());
        lw.setCoordinates(new Coordinates(
                Integer.parseInt(parts[start + 1].trim()),
                Float.parseFloat(parts[start + 2].trim())
        ));
        lw.setMinimalPoint(Long.parseLong(parts[start + 3].trim()));
        lw.setDescription(parts[start + 4].trim().isEmpty() ? null : parts[start + 4].trim());
        lw.setTunedInWorks(parts[start + 5].trim().isEmpty() ? null : Integer.parseInt(parts[start + 5].trim()));
        lw.setDifficulty(Difficulty.valueOf(parts[start + 6].trim().toUpperCase()));
        String dName = parts[start + 7].trim();
        String dHours = parts[start + 8].trim();
        if (!dName.isEmpty() && !dHours.isEmpty()) {
            lw.setDiscipline(new Discipline(dName, Long.parseLong(dHours)));
        }
        lw.setCreationDate(java.time.LocalDateTime.now());
        return lw;
    }
}




//package client.util;
//
//import common.command.CommandRequest;
//import common.models.LabWork;
//
//import java.util.*;
//
///**
// * Класс для построения объектов CommandRequest
// * на основе пользовательского ввода из консоли.
// */
//public class CommandBuilder {
//    private static final Scanner scanner = new Scanner(System.in);
//
//    /**
//     * Строит объект запроса команды (CommandRequest).
//     * Для некоторых команд дополнительно запрашиваются аргументы.
//     * @param command строка команды
//     * @return объект CommandRequest, содержащий имя команды и аргументы
//     */
//    public static CommandRequest build(String command) {
//        switch (command) {
//            case "execute_script":
//                System.out.print("Введите имя файла скрипта: ");
//                String filename = scanner.nextLine().trim();
//                return new CommandRequest("execute_script", filename);
//            case "add":
//                return new CommandRequest("add", LabWorkFactory.createLabWork());
//            case "update":
//                System.out.print("Введите id для обновления: ");
//                int id = Integer.parseInt(scanner.nextLine().trim());
//                LabWork updated = LabWorkFactory.createLabWork();
//                Map<String, Object> args = new HashMap<>();
//                args.put("id", id);
//                args.put("element", updated);
//                return new CommandRequest("update", args);
//            case "remove_by_id":
//            case "remove_at":
//                System.out.print("Введите целочисленный id или index: ");
//                return new CommandRequest(command, Integer.parseInt(scanner.nextLine().trim()));
//            case "filter_less_than_minimal_point":
//                System.out.print("Введите значение minimalPoint: ");
//                return new CommandRequest(command, Long.parseLong(scanner.nextLine().trim()));
////            case "shuffle":
////            case "clear":
////            case "reorder":
////            case "print_ascending":
////            case "min_by_coordinates":
////            case "info":
////            case "show":
////            case "help":
////                return new CommandRequest(command, null);
//            default:
//                return new CommandRequest(command, null);
//        }
//    }
//}
