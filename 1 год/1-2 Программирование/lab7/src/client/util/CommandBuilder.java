package client.util;

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
    private static String username = null;
    private static String password = null;

    public static void enableScriptMode() {
        isScriptMode = true;
    }

    public static void disableScriptMode() {
        isScriptMode = false;
    }

    public static void setCredentials(String login, String pass) {
        username = login;
        password = pass;
    }

    public static String getUsername() {
        return username;
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
                case "login", "register" -> {
                    System.out.print("Введите логин: ");
                    String login = (scanner.nextLine().trim());
                    System.out.print("Введите пароль: ");
                    String pass = scanner.nextLine().trim();
                    return new CommandRequest(command, null, login, pass);
                }

                case "add" -> {
                    LabWork lw = isScriptMode ? parseLabWork(parts, 1) : LabWorkFactory.createLabWork();
                    return new CommandRequest("add", lw, username, password);
                }

                case "update" -> {
                    int id = isScriptMode
                            ? Integer.parseInt(parts[1].trim())
                            : Integer.parseInt(prompt("Введите id для обновления: "));
                    LabWork updated = isScriptMode ? parseLabWork(parts, 2) : LabWorkFactory.createLabWork();
                    Map<String, Object> args = new HashMap<>();
                    args.put("id", id);
                    args.put("element", updated);
                    return new CommandRequest("update", args, username, password);
                }

                case "remove_by_id", "remove_at" -> {
                    int idOrIndex = isScriptMode
                            ? Integer.parseInt(parts[1].trim())
                            : Integer.parseInt(prompt("Введите ID или индекс: "));
                    return new CommandRequest(command, idOrIndex, username, password);
                }

                case "filter_less_than_minimal_point" -> {
                    long point = isScriptMode
                            ? Long.parseLong(parts[1].trim())
                            : Long.parseLong(prompt("Введите значение minimalPoint: "));
                    return new CommandRequest(command, point, username, password);
                }

                case "execute_script" -> {
                    String filename = isScriptMode
                            ? parts[1].trim()
                            : prompt("Введите имя файла скрипта: ");
                    return new CommandRequest(command, filename, username, password);
                }

                case "shuffle", "clear", "reorder", "print_ascending",
                     "min_by_coordinates", "info", "show", "help", "save" -> {
                    return new CommandRequest(command, null, username, password);
                }

                default -> System.out.println("Неизвестная команда: " + command);
            }

        } catch (Exception e) {
            System.out.println("Ошибка при разборе команды: " + e.getMessage());
        }

        return null;
    }

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

    private static String prompt(String message) {
        System.out.print(message);
        return scanner.nextLine().trim();
    }
}
