package server.util;

import common.models.*;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.File;
import java.io.FileNotFoundException;
import java.nio.charset.StandardCharsets;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.sql.*;
import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;

/**
 * Класс для управления подключением к базе данных PostgreSQL с чтением логина и пароля из файла.
 */
public class DatabaseManager {
    private static final Logger logger = LoggerFactory.getLogger(DatabaseManager.class);
    private static final String url = "jdbc:postgresql://localhost:5432/studs";
    private static String username;
    private static String password;
    private static Connection conn;

    /**
     * Загружает учетные данные из указанного файла.
     * Ожидается, что в файле будут 2 строки: логин и пароль.
     *
     * @param filename путь к файлу
     */
    public static void loadCredentials(String filename) {
        try (Scanner scanner = new Scanner(new File(filename))) {
            if (scanner.hasNextLine()) username = scanner.nextLine().trim();
            if (scanner.hasNextLine()) password = scanner.nextLine().trim();
            if (username == null || password == null || username.isEmpty() || password.isEmpty()) {
                logger.error("Файл с данными должен содержать логин и пароль на отдельных строках");
                System.exit(1);
            }
        } catch (FileNotFoundException e) {
            logger.error("Файл с учетными данными не найден: {}", filename);
            System.exit(1);
        }
    }

    /**
     * Устанавливает и возвращает подключение к базе данных.
     *
     * @return активное подключение
     */
    public static Connection getConnection() {
        try {
            if (conn == null || conn.isClosed()) {
                conn = DriverManager.getConnection(url, username, password);
                logger.info("Соединение с базой данных установлено.");
            }
        } catch (SQLException e) {
            logger.error("Ошибка подключения к базе данных: {}", e.getMessage());
            throw new RuntimeException("Ошибка подключения к БД", e);
        }
        return conn;
    }

    /**
     * Загружает текущую коллекцию LabWork из базу данных.
     *
     * @return collection
     */
    public List<LabWork> loadCollection() {
        List<LabWork> collection = new ArrayList<>();
        String query = "SELECT l.*, d.name AS d_name, d.practice_hours FROM labworks l LEFT JOIN disciplines d ON l.discipline_id = d.id";

        try (Connection conn = getConnection();
             PreparedStatement stmt = conn.prepareStatement(query);
             ResultSet rs = stmt.executeQuery()) {

            while (rs.next()) {
                LabWork lw = new LabWork();
                lw.setId(rs.getInt("id"));
                lw.setName(rs.getString("name"));
                lw.setCoordinates(new Coordinates(
                        rs.getInt("x"),
                        rs.getFloat("y")
                ));
                lw.setCreationDate(rs.getObject("creation_date", LocalDateTime.class));
                lw.setMinimalPoint(rs.getLong("minimal_point"));
                lw.setDescription(rs.getString("description"));
                int tiw = rs.getInt("tuned_in_works");
                lw.setTunedInWorks(rs.wasNull() ? null : tiw);
                lw.setDifficulty(Difficulty.valueOf(rs.getString("difficulty")));
                if (rs.getString("d_name") != null) {
                    lw.setDiscipline(new Discipline(
                            rs.getString("d_name"),
                            rs.getLong("practice_hours")
                    ));
                }
                lw.setOwner(rs.getInt("owner"));

                collection.add(lw);
            }

            logger.info("Загружено {} элементов из БД.", collection.size());
            return collection;

        } catch (SQLException e) {
            logger.error("Ошибка загрузки коллекции из базы данных: {}", e.getMessage());
            return collection;
        }
    }



    /**
     * Сохраняет текущую коллекцию LabWork в базу данных.
     *
     * @param labWorks список элементов для сохранения
     * @return true, если успешно
     */
    public static boolean saveCollection(List<LabWork> labWorks) {
        String deleteLabworksSQL = "DELETE FROM labworks";
        String deleteDisciplinesSQL = "DELETE FROM disciplines";

        String insertDisciplineSQL = "INSERT INTO disciplines (name, practice_hours) VALUES (?, ?) RETURNING id";
        String insertLabworkSQL = """
        INSERT INTO labworks (
            name, x, y, creation_date, minimal_point,
            description, tuned_in_works, difficulty,
            discipline_id, owner_id
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """;

        try (Connection conn = getConnection()) {
            conn.setAutoCommit(false); // транзакция

            try (
                    PreparedStatement deleteLabStmt = conn.prepareStatement(deleteLabworksSQL);
                    PreparedStatement deleteDiscStmt = conn.prepareStatement(deleteDisciplinesSQL)
            ) {
                deleteLabStmt.executeUpdate();
                deleteDiscStmt.executeUpdate();
            }

            for (LabWork lw : labWorks) {
                Long disciplineId = null;
                if (lw.getDiscipline() != null) {
                    try (PreparedStatement discStmt = conn.prepareStatement(insertDisciplineSQL)) {
                        discStmt.setString(1, lw.getDiscipline().getName());
                        discStmt.setLong(2, lw.getDiscipline().getPracticeHours());
                        ResultSet rs = discStmt.executeQuery();
                        if (rs.next()) {
                            disciplineId = rs.getLong(1);
                        }
                    }
                }

                try (PreparedStatement labStmt = conn.prepareStatement(insertLabworkSQL)) {
                    labStmt.setString(1, lw.getName());
                    labStmt.setInt(2, lw.getCoordinates().getX());
                    labStmt.setFloat(3, lw.getCoordinates().getY());
                    labStmt.setObject(4, lw.getCreationDate());
                    labStmt.setLong(5, lw.getMinimalPoint());
                    labStmt.setString(6, lw.getDescription());
                    if (lw.getTunedInWorks() != null)
                        labStmt.setInt(7, lw.getTunedInWorks());
                    else
                        labStmt.setNull(7, Types.INTEGER);
                    labStmt.setString(8, lw.getDifficulty().name());
                    if (disciplineId != null)
                        labStmt.setLong(9, disciplineId);
                    else
                        labStmt.setNull(9, Types.BIGINT);
                    if (lw.getOwner() != null)
                        labStmt.setInt(10, lw.getOwner());
                    else
                        labStmt.setNull(10, Types.INTEGER);
                    labStmt.executeUpdate();
                }
            }

            conn.commit();
            logger.info("Коллекция успешно сохранена в БД.");
            return true;
        } catch (SQLException e) {
            logger.error("Ошибка при сохранении коллекции в БД: {}", e.getMessage());
            return false;
        }
    }

    public static boolean handleRegister(Connection conn, String username, String password) {
        try {
            String hashedPassword = hashPassword(password);
            PreparedStatement stmt = conn.prepareStatement("INSERT INTO users (login, password) VALUES (?, ?)");
            stmt.setString(1, String.valueOf(username));
            stmt.setString(2, hashedPassword);
            stmt.executeUpdate();
            return true;
        } catch (SQLException e) {
            logger.error("Ошибка при регистрации пользователя: {}", username, e);
            return false;
        }
    }

    public static boolean handleLogin(Connection conn, String username, String password) {
        try {
            PreparedStatement stmt = conn.prepareStatement("SELECT password FROM users WHERE login = ?");
            stmt.setString(1, String.valueOf(username));
            ResultSet rs = stmt.executeQuery();
            if (rs.next()) {
                String storedHash = rs.getString("password");
                String providedHash = hashPassword(password);
                return storedHash.equals(providedHash);
            }
        } catch (SQLException e) {
            logger.error("Ошибка при входе пользователя: {}", username, e);
        }
        return false;
    }


    private static String hashPassword(String password) {
        try {
            MessageDigest digest = MessageDigest.getInstance("SHA-224");
            byte[] hash = digest.digest(password.getBytes(StandardCharsets.UTF_8));
            StringBuilder hexString = new StringBuilder();
            for (byte b : hash) {
                hexString.append(String.format("%02x", b));
            }
            return hexString.toString();
        } catch (NoSuchAlgorithmException e) {
            throw new RuntimeException("SHA-224 не поддерживается", e);
        }
    }
}
