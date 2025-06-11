package client;

import client.util.CommandBuilder;
import common.command.CommandRequest;
import common.command.CommandResponse;

import java.io.*;
import java.net.InetSocketAddress;
import java.nio.ByteBuffer;
import java.nio.channels.SocketChannel;
import java.util.HashSet;
import java.util.Scanner;
import java.util.Set;

/**
 * Главный класс клиента.
 * Отвечает за ввод команд, передачу их на сервер и вывод результата.
 */
public class ClientApp {
    private static final String SERVER_HOST = "localhost"; //"helios.cs.ifmo.ru"
    private static final int SERVER_PORT = 9999;

    public static void main(String[] args) {
        System.out.println("Клиент запущен. Введите команду (help для списка):");

        try (Scanner scanner = new Scanner(System.in)) {
            while (true) {
                System.out.print("> ");
                String input = scanner.nextLine().trim();

                if (input.equalsIgnoreCase("exit")) {
                    System.out.println("Завершение клиента.");
                    break;
                }

                if (input.startsWith("execute_script")) {
                    String[] parts = input.split(" ");
                    if (parts.length < 2) {
                        System.out.println("Формат: execute_script <имя_файла>");
                        continue;
                    }
                    executeScript(parts[1], new HashSet<>());
                    continue;
                }

                CommandRequest request = CommandBuilder.build(input);
                if (request == null) {
                    System.out.println("Невозможно сформировать запрос. Повторите ввод.");
                    continue;
                }

                sendRequestToServer(request);
            }
        }
    }

    private static void executeScript(String filename, Set<String> callStack) {
        if (callStack.contains(filename)) {
            System.out.println("Обнаружена рекурсия: " + filename + " уже был вызван.");
            return;
        }

        callStack.add(filename);
        CommandBuilder.enableScriptMode();

        try (BufferedReader reader = new BufferedReader(new FileReader(filename))) {
            String line;
            while ((line = reader.readLine()) != null) {
                String command = line.trim();
                if (command.isEmpty()) continue;

                System.out.println(">> " + command);

                if (command.equals("exit")) {
                    System.out.println("Команда exit в скрипте — игнорируется.");
                    continue;
                }

                if (command.startsWith("execute_script")) {
                    String[] parts = command.split(" ");
                    if (parts.length < 2) {
                        System.out.println("Формат: execute_script <имя_файла>");
                        continue;
                    }
                    executeScript(parts[1], callStack);
                    continue;
                }

                CommandRequest request = CommandBuilder.build(command);
                if (request == null) {
                    System.out.println("Ошибка в команде: " + command);
                    continue;
                }
                sendRequestToServer(request);
            }
        } catch (IOException e) {
            System.out.println("Ошибка чтения скрипта: " + e.getMessage());
        } finally {
            callStack.remove(filename);
            CommandBuilder.disableScriptMode();
        }
    }

    private static void sendRequestToServer(CommandRequest request) {
        try (SocketChannel channel = SocketChannel.open()) {
            channel.connect(new InetSocketAddress(SERVER_HOST, SERVER_PORT));

            ByteArrayOutputStream bos = new ByteArrayOutputStream();
            ObjectOutputStream oos = new ObjectOutputStream(bos);
            oos.writeObject(request);
            oos.flush();

            byte[] requestData = bos.toByteArray();
            ByteBuffer requestLength = ByteBuffer.allocate(4).putInt(requestData.length);
            requestLength.flip();
            channel.write(requestLength);
            channel.write(ByteBuffer.wrap(requestData));

            ByteBuffer lengthBuffer = ByteBuffer.allocate(4);
            while (lengthBuffer.hasRemaining()) {
                channel.read(lengthBuffer);
            }
            lengthBuffer.flip();
            int responseLength = lengthBuffer.getInt();

            ByteBuffer responseBuffer = ByteBuffer.allocate(responseLength);
            while (responseBuffer.hasRemaining()) {
                channel.read(responseBuffer);
            }
            responseBuffer.flip();

            byte[] responseData = new byte[responseLength];
            responseBuffer.get(responseData);

            ObjectInputStream ois = new ObjectInputStream(new ByteArrayInputStream(responseData));
            Object response = ois.readObject();

            if (response instanceof CommandResponse cmdResp) {
                System.out.println(cmdResp.getMessage());
            } else {
                System.out.println("Неверный формат ответа от сервера.");
            }
        } catch (IOException | ClassNotFoundException e) {
            System.out.println("Ошибка соединения с сервером: " + e.getMessage());
        }
    }
}

//package client;
//
//import client.util.CommandBuilder;
//import common.command.CommandRequest;
//import common.command.CommandResponse;
//import org.slf4j.Logger;
//import org.slf4j.LoggerFactory;
//
//import java.io.*;
//import java.net.InetSocketAddress;
//import java.net.Socket;
//import java.nio.ByteBuffer;
//import java.util.HashSet;
//import java.util.Scanner;
//import java.util.Set;
//
///**
// * Главный класс клиентского приложения.
// * Отвечает за ввод команд, передачу их на сервер и вывод результата.
// */
//public class ClientApp {
//    private static final Logger logger = LoggerFactory.getLogger(ClientApp.class);
//    private static final String SERVER_HOST = "localhost";
//    private static final int SERVER_PORT = 9999;
//
//    public static void main(String[] args) {
//        System.out.println("Клиент запущен. Введите команду (help для списка):");
//
//        try (Scanner scanner = new Scanner(System.in)) {
//            while (true) {
//                System.out.print("> ");
//                String input = scanner.nextLine().trim();
//
//                if (input.equalsIgnoreCase("exit")) {
//                    System.out.println("Завершение клиента.");
//                    break;
//                }
//
//                if (input.startsWith("execute_script")) {
//                    String[] parts = input.split(" ");
//                    if (parts.length < 2) {
//                        System.out.println("Формат: execute_script <имя_файла>");
//                        continue;
//                    }
//                    executeScript(parts[1], new HashSet<>());
//                    continue;
//                }
//
//                CommandRequest request = CommandBuilder.build(input);
//                if (request == null) {
//                    System.out.println("Невозможно сформировать запрос. Повторите ввод.");
//                    continue;
//                }
//
//                sendRequestToServer(request);
//            }
//        }
//    }
//
//    private static void executeScript(String filename, Set<String> callStack) {
//        if (callStack.contains(filename)) {
//            System.out.println("Обнаружена рекурсия: " + filename + " уже был вызван.");
//            return;
//        }
//
//        callStack.add(filename);
//        CommandBuilder.enableScriptMode();
//
//        try (BufferedReader reader = new BufferedReader(new FileReader(filename))) {
//            String line;
//            while ((line = reader.readLine()) != null) {
//                String command = line.trim();
//                if (command.isEmpty()) continue;
//
//                System.out.println(">> " + command);
//
//                if (command.equals("exit")) {
//                    System.out.println("Команда exit в скрипте — игнорируется.");
//                    continue;
//                }
//
//                if (command.startsWith("execute_script")) {
//                    String[] parts = command.split(" ");
//                    if (parts.length < 2) {
//                        System.out.println("Формат: execute_script <имя_файла>");
//                        continue;
//                    }
//                    executeScript(parts[1], callStack);
//                    continue;
//                }
//
//                CommandRequest request = CommandBuilder.build(command);
//                if (request == null) {
//                    System.out.println("Ошибка в команде: " + command);
//                    continue;
//                }
//
//                sendRequestToServer(request);
//            }
//        } catch (IOException e) {
//            System.out.println("Ошибка чтения скрипта: " + e.getMessage());
//        } finally {
//            callStack.remove(filename);
//            CommandBuilder.disableScriptMode();
//        }
//    }
//
//    private static void sendRequestToServer(CommandRequest request) {
//        try (Socket socket = new Socket()) {
//            socket.connect(new InetSocketAddress(SERVER_HOST, SERVER_PORT), 3000);
//
//            try (
//                    ObjectOutputStream out = new ObjectOutputStream(socket.getOutputStream());
//                    ObjectInputStream in = new ObjectInputStream(socket.getInputStream())
//            ) {
//                // Клиент: сначала отправляет длину, затем объект
//                ByteArrayOutputStream bos = new ByteArrayOutputStream();
//                ObjectOutputStream oos = new ObjectOutputStream(bos);
//                oos.writeObject(request);
//                oos.flush();
//                byte[] data = bos.toByteArray();
//
//                out.write(ByteBuffer.allocate(4).putInt(data.length).array()); // длина
//                out.write(data); // сам объект
//                logger.debug("Команда отправлена: {}", request.getCommandName());
//
//                Object response = in.readObject();
//                if (response instanceof CommandResponse) {
//                    String msg = ((CommandResponse) response).getMessage();
//                    System.out.println(msg);
//                } else {
//                    System.out.println("Неверный формат ответа от сервера.");
//                }
//            }
//        } catch (IOException e) {
//            logger.error("Ошибка подключения к серверу: {}", e.getMessage());
//            System.out.println("Ошибка соединения с сервером: " + e.getMessage());
//        } catch (ClassNotFoundException e) {
//            logger.error("Ошибка чтения ответа от сервера: {}", e.getMessage());
//            System.out.println("Ошибка при получении ответа от сервера.");
//        }
//    }
//}
//
//
////package client;
////
////import client.util.CommandBuilder;
////import common.command.CommandRequest;
////import common.command.CommandResponse;
//////import org.slf4j.Logger;
//////import org.slf4j.LoggerFactory;
////
////import java.io.*;
////import java.net.InetSocketAddress;
////import java.net.Socket;
////import java.util.HashSet;
////import java.util.Scanner;
////import java.util.Set;
////
/////**
//// * Главный класс клиентского приложения.
//// */
////public class ClientApp {
//////    private static final Logger logger = LoggerFactory.getLogger(ClientApp.class);
////    private static final String SERVER_HOST = "localhost"; //"helios.cs.ifmo.ru"
////    private static final int SERVER_PORT = 9999;
////
////    /**
////     * Точка входа клиента. Запускает цикл ввода команд и обработки ответов от сервера.
////     * @param args аргументы командной строки (не используются)
////     */
////    public static void main(String[] args) {
////        System.out.println("Клиент запущен. Введите команду (help для списка):");
////
////        try (Scanner scanner = new Scanner(System.in)) {
////            while (true) {
////                System.out.print("> ");
////                String input = scanner.nextLine().trim();
////
////                if (input.equalsIgnoreCase("exit")) {
////                    System.out.println("Завершение клиента.");
////                    break;
////                }
////
////                if (input.startsWith("execute_script")) {
////                    String[] parts = input.split(" ");
////                    if (parts.length < 2) {
////                        System.out.println("Формат: execute_script <имя_файла>");
////                        continue;
////                    }
////                    executeScript(parts[1], new HashSet<>());
////                    continue;
////                }
////
////                CommandRequest request = CommandBuilder.build(input);
////                if (request == null) {
////                    System.out.println("Невозможно сформировать запрос. Повторите ввод.");
////                    continue;
////                }
////
////                sendRequestToServer(request);
////            }
////        }
////    }
////
////    /**
////     * Обрабатывает команду execute_script.
////     * @param filename имя файла со скриптом
////     * @param callStack множество вызванных скриптов
////     */
////    private static void executeScript(String filename, Set<String> callStack) {
////        CommandBuilder.enableScriptMode();
////        if (callStack.contains(filename)) {
////            System.out.println("Обнаружена рекурсия: " + filename + " уже был вызван.");
////            return;
////        }
////        callStack.add(filename);
////
////        try (BufferedReader reader = new BufferedReader(new FileReader(filename))) {
////            String line;
////            while ((line = reader.readLine()) != null) {
////                String command = line.trim();
////                if (command.isEmpty()) continue;
////                System.out.println(">> " + command);
////
////                if (command.equals("exit")) {
////                    System.out.println("Команда exit в скрипте — игнорируется.");
////                    continue;
////                }
////
////                if (command.startsWith("execute_script")) {
////                    String[] parts = command.split(" ");
////                    if (parts.length < 2) {
////                        System.out.println("Формат: execute_script <имя_файла>");
////                        continue;
////                    }
////                    executeScript(parts[1], callStack); // Рекурсивный вызов
////                    continue;
////                }
////
////                CommandRequest request = CommandBuilder.build(command);
////                if (request == null) {
////                    System.out.println("Ошибка в команде: " + command);
////                    continue;
////                }
////                sendRequestToServer(request);
////            }
////        } catch (IOException e) {
////            System.out.println("Ошибка чтения скрипта: " + e.getMessage());
////        } finally {
////            callStack.remove(filename);
////        }
////        CommandBuilder.disableScriptMode();
////    }
////
////    /**
////     * Отправляет объект команды на сервер.
////     * @param request объект команды
////     */
////    private static void sendRequestToServer(CommandRequest request) {
////        try (Socket socket = new Socket()) {
////            socket.connect(new InetSocketAddress(SERVER_HOST, SERVER_PORT), 0);
//////            logger.info("Подключено к серверу {}:{}", SERVER_HOST, SERVER_PORT);
////
////            try (
////                    ObjectOutputStream out = new ObjectOutputStream(socket.getOutputStream());
////                    ObjectInputStream in = new ObjectInputStream(socket.getInputStream())
////            ) {
////                out.writeObject(request);
////                System.out.println("Команда отправлена: " + request.getCommandName());
//////                logger.debug("Команда отправлена: {}", request.getCommandName());
////
////                Object response = in.readObject();
////                if (response instanceof CommandResponse) {
////                    String msg = ((CommandResponse) response).getMessage();
////                    System.out.println(msg);
//////                    logger.debug("Ответ от сервера: {}", msg);
////                } else {
////                    System.out.println("Неверный формат ответа.");
//////                    logger.warn("Неверный формат ответа от сервера");
////                }
////            }
////        } catch (IOException e) {
//////            logger.error("Ошибка подключения к серверу: {}", e.getMessage());
////            System.out.println("Ошибка соединения с сервером: " + e.getMessage());
////        } catch (ClassNotFoundException e) {
//////            logger.error("Ошибка чтения ответа: {}", e.getMessage());
////            System.out.println("Ошибка при получении ответа от сервера.");
////        }
////    }
////}
