package server;

import common.command.CommandRequest;
import common.command.CommandResponse;
import common.models.LabWork;
import server.command.CommandManager;
import server.util.CSVHandler;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.*;
import java.net.InetSocketAddress;
import java.nio.ByteBuffer;
import java.nio.channels.Selector;
import java.nio.channels.SelectionKey;
import java.nio.channels.ServerSocketChannel;
import java.nio.channels.SocketChannel;
import java.util.*;

/**
 * Главный класс.
 */
public class ServerApp {
    private static final Logger logger = LoggerFactory.getLogger(ServerApp.class);
    private static final String CSV_FILE_PATH = "test.csv";

    public static void main(String[] args) {
        logger.info("Сервер запускается...");
        int port = 9999;

        List<LabWork> loaded = CSVHandler.loadFromCSV(CSV_FILE_PATH);
        loaded.forEach(lw -> CommandManager.handle(new CommandRequest("add", lw)));

        Runtime.getRuntime().addShutdownHook(new Thread(() -> {
            logger.info("Сервер завершает работу. Сохраняем коллекцию...");
            CSVHandler.saveToCSV(CSV_FILE_PATH, CommandManager.getCollectionSorted());
        }));

        try (Selector selector = Selector.open();
             ServerSocketChannel serverChannel = ServerSocketChannel.open()) {

            serverChannel.bind(new InetSocketAddress(port));
            serverChannel.configureBlocking(false);
            serverChannel.register(selector, SelectionKey.OP_ACCEPT);

            logger.info("Сервер запущен на порту {}", port);

            while (true) {
                selector.select();
                Iterator<SelectionKey> keys = selector.selectedKeys().iterator();

                while (keys.hasNext()) {
                    SelectionKey key = keys.next();
                    keys.remove();

                    if (key.isAcceptable()) {
                        SocketChannel client = serverChannel.accept();
                        client.configureBlocking(false);
                        client.register(selector, SelectionKey.OP_READ);
                        logger.info("Новое подключение: {}", client);
                    } else if (key.isReadable()) {
                        SocketChannel client = (SocketChannel) key.channel();
                        try {
                            ByteBuffer lengthBuffer = ByteBuffer.allocate(4);
                            while (lengthBuffer.hasRemaining()) {
                                int read = client.read(lengthBuffer);
                                if (read == -1) throw new IOException("Клиент закрыл соединение.");
                            }
                            lengthBuffer.flip();
                            int length = lengthBuffer.getInt();

                            ByteBuffer dataBuffer = ByteBuffer.allocate(length);
                            while (dataBuffer.hasRemaining()) {
                                int read = client.read(dataBuffer);
                                if (read == -1) throw new IOException("Клиент закрыл соединение.");
                            }
                            dataBuffer.flip();

                            byte[] data = new byte[length];
                            dataBuffer.get(data);

                            try (ObjectInputStream ois = new ObjectInputStream(new ByteArrayInputStream(data))) {
                                CommandRequest request = (CommandRequest) ois.readObject();
                                logger.info("Получена команда: {}", request.getCommandName());

                                String result = CommandManager.handle(request);

                                ByteArrayOutputStream bos = new ByteArrayOutputStream();
                                try (ObjectOutputStream oos = new ObjectOutputStream(bos)) {
                                    oos.writeObject(new CommandResponse(result));
                                }

                                byte[] responseData = bos.toByteArray();
                                ByteBuffer responseLength = ByteBuffer.allocate(4).putInt(responseData.length);
                                responseLength.flip();
                                ByteBuffer responseBody = ByteBuffer.wrap(responseData);
                                client.write(responseLength);
                                client.write(responseBody);
                            }
                        } catch (Exception e) {
                            client.close();
                        }
                    }
                }
            }
        } catch (IOException e) {
            logger.error("Ошибка сервера: ", e);
        }
    }
}


//package server;
//
//import common.command.CommandRequest;
//import common.command.CommandResponse;
//import common.models.LabWork;
//import server.command.CommandManager;
//import server.util.CSVHandler;
//import org.slf4j.Logger;
//import org.slf4j.LoggerFactory;
//
//import java.io.*;
//import java.net.InetSocketAddress;
//import java.net.ServerSocket;
//import java.net.Socket;
//import java.nio.ByteBuffer;
//import java.nio.channels.SelectionKey;
//import java.nio.channels.Selector;
//import java.nio.channels.ServerSocketChannel;
//import java.nio.channels.SocketChannel;
//import java.util.Iterator;
//import java.util.List;
//
///**
// * Главный класс сервера
// */
//public class ServerApp {
//    private static final Logger logger = LoggerFactory.getLogger(ServerApp.class);
//    private static final String CSV_FILE_PATH = "test.csv";
//
//    /**
//     * Точка входа в серверное приложение.
//     *
//     * @param args аргументы командной строки (не используются)
//     */
//    public static void main(String[] args) {
//        logger.info("Сервер запускается...");
//        int port = 9999;
//
//        // Загрузка коллекции из файла
//        List<LabWork> loaded = CSVHandler.loadFromCSV(CSV_FILE_PATH);
//        loaded.forEach(lw -> CommandManager.handle(new CommandRequest("add", lw)));
//
//        // Завершение сеанса
//        Runtime.getRuntime().addShutdownHook(new Thread(() -> {
//            System.out.println("Сервер завершает работу...");
////            CSVHandler.saveToCSV(CSV_FILE_PATH, CommandManager.getCollectionSorted());
//        }));
//
//        try (Selector selector = Selector.open();
//             ServerSocketChannel serverChannel = ServerSocketChannel.open()) {
//
//            serverChannel.bind(new InetSocketAddress(port));
//            serverChannel.configureBlocking(false);
//            serverChannel.register(selector, SelectionKey.OP_ACCEPT);
//
//            logger.info("Сервер запущен на порту {}", port);
//
//            while (true) {
//                selector.select(); // Блокируется до события
//                Iterator<SelectionKey> keys = selector.selectedKeys().iterator();
//
//                while (keys.hasNext()) {
//                    SelectionKey key = keys.next();
//                    keys.remove();
//
//                    if (key.isAcceptable()) {
//                        SocketChannel client = serverChannel.accept();
//                        client.configureBlocking(false);
//                        client.register(selector, SelectionKey.OP_READ);
//                        logger.info("Новое подключение: {}", client);
//                    }
//
//                    if (key.isReadable()) {
//                        SocketChannel client = (SocketChannel) key.channel();
//                        ByteBuffer buffer = ByteBuffer.allocate(8192);
//                        int bytesRead = client.read(buffer);
//
//                        if (bytesRead == -1) {
//                            client.close();
//                            continue;
//                        }
//
//                        // Читаем первые 4 байта — длину сообщения
//                        ByteBuffer lengthBuffer = ByteBuffer.allocate(4);
//                        while (lengthBuffer.hasRemaining()) {
//                            client.read(lengthBuffer);
//                        }
//                        lengthBuffer.flip();
//                        int length = lengthBuffer.getInt();
//
//// Затем читаем сам объект длиной length байт
//                        ByteBuffer dataBuffer = ByteBuffer.allocate(length);
//                        while (dataBuffer.hasRemaining()) {
//                            client.read(dataBuffer);
//                        }
//                        dataBuffer.flip();
//
//                        byte[] data = new byte[length];
//                        dataBuffer.get(data);
//
//                        try (ObjectInputStream ois = new ObjectInputStream(new ByteArrayInputStream(data))) {
//                            CommandRequest request = (CommandRequest) ois.readObject();
//                            logger.info("Получена команда: {}", request.getCommandName());
//
//                            String result = CommandManager.handle(request);
//
//                            ByteArrayOutputStream bos = new ByteArrayOutputStream();
//                            try (ObjectOutputStream oos = new ObjectOutputStream(bos)) {
//                                oos.writeObject(new CommandResponse(result));
//                            }
//
//                            byte[] responseData = bos.toByteArray();
//                            ByteBuffer responseLength = ByteBuffer.allocate(4).putInt(responseData.length);
//                            responseLength.flip();
//                            client.write(responseLength);
//                            client.write(ByteBuffer.wrap(responseData));
//                        } catch (Exception e) {
//                            logger.error("Ошибка при обработке запроса: ", e);
//                            client.close();
//                        }
//                    }
//                }
//            }
//
//        } catch (IOException e) {
//            logger.error("Ошибка сервера: ", e);
//        }
//    }
//}
//
////        try (ServerSocket serverSocket = new ServerSocket(port)) {
////            logger.info("Сервер запущен и слушает порт {}", port);
////
////            while (true) {
////                Socket clientSocket = serverSocket.accept(); // Блокирующий
////                logger.info("Подключён клиент: {}", clientSocket.getRemoteSocketAddress());
////
////                try (
////                        ObjectInputStream in = new ObjectInputStream(clientSocket.getInputStream());
////                        ObjectOutputStream out = new ObjectOutputStream(clientSocket.getOutputStream())
////                ) {
////                    Object input = in.readObject();
////                    if (input instanceof CommandRequest request) {
////                        logger.info("Получена команда: {}", request.getCommandName());
////
////                        String result = CommandManager.handle(request);
////                        out.writeObject(new CommandResponse(result));
////                    } else {
////                        logger.warn("Получен неизвестный тип команды.");
////                        out.writeObject(new CommandResponse("Неверный формат команды"));
////                    }
////                } catch (Exception e) {
////                    logger.error("Ошибка обработки запроса от клиента", e);
////                } finally {
////                    clientSocket.close();
////                    logger.info("Соединение с клиентом закрыто.");
////                }
////            }
////        } catch (IOException e) {
////            logger.error("Ошибка при запуске сервера", e);
////        }
////    }
////}
