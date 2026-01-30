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
    private static final String HOST = "localhost";
    private static final int PORT = 9999;

    public static void main(String[] args) {
        System.out.println("Клиент запущен. Введите команду login, чтобы войти или команду register, чтобы зарегистрироваться.");
        Scanner scanner = new Scanner(System.in);

        while (true) {
            System.out.print("> ");
            String input = scanner.nextLine().trim();
            if (input.isEmpty()) continue;

            if (input.equalsIgnoreCase("exit")) {
                    System.out.println("Завершение клиента.");
                    break;
            }

            if (input.startsWith("execute_script")) {
                String[] parts = input.split("\\s+", 2);
                if (parts.length < 2) {
                    System.out.println("Формат: execute_script <имя_файла>");
                    continue;
                }
                executeScript(parts[1], new HashSet<>());
                continue;
            }

            CommandRequest request = CommandBuilder.build(input);
            if (request == null) {
                System.out.println("Команда не распознана.");
                continue;
            }

            sendRequestToServer(request);
        }
    }

    private static void executeScript(String filename, Set<String> callStack) {
        if (callStack.contains(filename)) {
            System.out.println("Обнаружена рекурсия: файл " + filename + " уже в процессе исполнения.");
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

                if (command.startsWith("execute_script")) {
                    String[] parts = command.split("\\s+", 2);
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
        try (SocketChannel socketChannel = SocketChannel.open(new InetSocketAddress(HOST, PORT))) {
            // Отправка запроса
            ByteArrayOutputStream bos = new ByteArrayOutputStream();
            try (ObjectOutputStream oos = new ObjectOutputStream(bos)) {
                oos.writeObject(request);
            }

            byte[] requestData = bos.toByteArray();
            ByteBuffer buffer = ByteBuffer.allocate(4 + requestData.length);
            buffer.putInt(requestData.length);
            buffer.put(requestData);
            buffer.flip();
            socketChannel.write(buffer);

            // Получение ответа
            ByteBuffer lengthBuffer = ByteBuffer.allocate(4);
            socketChannel.read(lengthBuffer);
            lengthBuffer.flip();
            int length = lengthBuffer.getInt();

            ByteBuffer dataBuffer = ByteBuffer.allocate(length);
            socketChannel.read(dataBuffer);
            dataBuffer.flip();

            byte[] responseData = new byte[length];
            dataBuffer.get(responseData);

            try (ObjectInputStream ois = new ObjectInputStream(new ByteArrayInputStream(responseData))) {
                CommandResponse response = (CommandResponse) ois.readObject();
                String message = response.getMessage();
                System.out.println(message);

                // Если это login или register — и успешный результат, сохранить логин/пароль
                if ((request.getCommandName().equals("login") || request.getCommandName().equals("register"))
                        && message.toLowerCase().contains("успеш")) {
                    CommandBuilder.setCredentials(request.getUsername(), request.getPassword());
                    System.out.println("Авторизация выполнена как: " + request.getUsername());
                }
            } catch (Exception e) {
                System.out.println("Ошибка при обработке ответа: " + e.getMessage());
            }

        } catch (IOException e) {
            System.err.println("Ошибка соединения с сервером: " + e.getMessage());
        }
    }
}


