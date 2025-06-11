package server;

import common.command.CommandRequest;
import common.command.CommandResponse;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import server.command.CommandManager;
import server.util.DatabaseManager;

import java.io.*;
import java.net.InetSocketAddress;
import java.nio.ByteBuffer;
import java.nio.channels.*;
import java.sql.Connection;
import java.sql.SQLException;
import java.util.Iterator;
import java.util.concurrent.*;

public class ServerApp {
    private static final Logger logger = LoggerFactory.getLogger(ServerApp.class);
    private static final String CONFIG_FILE_PATH = "config.txt";
    private static final int PORT = 9999;
    private static final ExecutorService readPool = Executors.newFixedThreadPool(8);

    public static void main(String[] args) {
        logger.info("Сервер запускается...");

        DatabaseManager.loadCredentials(CONFIG_FILE_PATH);

        try (Connection dbConnection = DatabaseManager.getConnection()) {
            logger.info("Подключение к базе данных установлено.");
            CommandManager.initialize(dbConnection);

            Runtime.getRuntime().addShutdownHook(new Thread(() -> {
                logger.info("Сервер завершает работу.");
                readPool.shutdown();
            }));

            try (Selector selector = Selector.open();
                 ServerSocketChannel serverChannel = ServerSocketChannel.open()) {

                serverChannel.bind(new InetSocketAddress(PORT));
                serverChannel.configureBlocking(false);
                serverChannel.register(selector, SelectionKey.OP_ACCEPT);

                logger.info("Сервер запущен на порту {}", PORT);

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
                                readFully(client, lengthBuffer);
                                lengthBuffer.flip();
                                int length = lengthBuffer.getInt();
                                if (length <= 0 || length > 10_000_000)
                                    throw new IOException("Некорректная длина пакета: " + length);

                                ByteBuffer dataBuffer = ByteBuffer.allocate(length);
                                readFully(client, dataBuffer);
                                dataBuffer.flip();

                                byte[] data = new byte[length];
                                dataBuffer.get(data);

                                ObjectInputStream ois = new ObjectInputStream(new ByteArrayInputStream(data));
                                CommandRequest request = (CommandRequest) ois.readObject();

                                readPool.submit(() -> handleClient(client, request));

                            } catch (Exception e) {
                                logger.error("Ошибка при обработке запроса от клиента.", e);
                                try {
                                    client.close();
                                } catch (IOException ex) {
                                    logger.error("Ошибка при закрытии клиентского сокета", ex);
                                }
                            }
                        }
                    }
                }
            } catch (IOException e) {
                logger.error("Ошибка сервера: ", e);
            }
        } catch (SQLException e) {
            logger.error("Ошибка подключения к базе данных", e);
        }
    }

    private static void handleClient(SocketChannel client, CommandRequest request) {
        try {
            logger.info("Получена команда: {}", request.getCommandName());
            String result = switch (request.getCommandName()) {
                case "login" -> DatabaseManager.handleLogin(CommandManager.getDbConnection(), request.getUsername(), request.getPassword())
                        ? "Успешный вход" : "Неверный логин или пароль";
                case "register" -> DatabaseManager.handleRegister(CommandManager.getDbConnection(), request.getUsername(), request.getPassword())
                        ? "Пользователь зарегистрирован" : "Регистрация не удалась (возможно, логин занят)";
                default -> CommandManager.handle(request);
            };

            ByteArrayOutputStream bos = new ByteArrayOutputStream();
            try (ObjectOutputStream oos = new ObjectOutputStream(bos)) {
                oos.writeObject(new CommandResponse(result));
            }

            byte[] responseData = bos.toByteArray();
            ByteBuffer responseLength = ByteBuffer.allocate(4).putInt(responseData.length);
            ByteBuffer responseBody = ByteBuffer.wrap(responseData);
            responseLength.flip();

            new Thread(() -> {
                try {
                    client.write(responseLength);
                    client.write(responseBody);
                } catch (IOException e) {
                    logger.error("Ошибка при отправке ответа клиенту", e);
                }
            }).start();

        } catch (Exception e) {
            logger.error("Ошибка при обработке запроса от клиента.", e);
            try {
                client.close();
            } catch (IOException ex) {
                logger.error("Ошибка при закрытии клиентского сокета", ex);
            }
        }
    }

    private static void readFully(SocketChannel channel, ByteBuffer buffer) throws IOException {
        while (buffer.hasRemaining()) {
            int read = channel.read(buffer);
            if (read == -1) throw new IOException("Клиент закрыл соединение.");
        }
    }
}