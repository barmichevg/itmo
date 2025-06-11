package server.util;

import common.models.*;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.sql.*;
import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;

/**
 * DAO для работы с таблицей labworks в базе данных.
 */
public class LabWorkDAO {
    private static final Logger logger = LoggerFactory.getLogger(LabWorkDAO.class);

    /**
     * Загружает все объекты LabWork из базы данных.
     *
     * @param connection соединение с БД
     * @return список объектов LabWork
     */
    public static List<LabWork> loadAllLabWorks(Connection connection) {
        List<LabWork> labWorks = new ArrayList<>();
        String query = "SELECT lw.*, d.name AS discipline_name, d.practice_hours, u.login AS owner_login " +
                "FROM labworks lw " +
                "JOIN disciplines d ON lw.discipline_id = d.id " +
                "JOIN users u ON lw.owner_id = u.id";

        try (PreparedStatement stmt = connection.prepareStatement(query);
             ResultSet rs = stmt.executeQuery()) {

            while (rs.next()) {
                LabWork lw = new LabWork();
                lw.setId(rs.getInt("id"));
                lw.setName(rs.getString("name"));
                lw.setCoordinates(new Coordinates(
                        rs.getInt("x"),
                        rs.getFloat("y")
                ));
                lw.setCreationDate(rs.getTimestamp("creation_date").toLocalDateTime());
                lw.setMinimalPoint(rs.getLong("minimal_point"));
                lw.setDescription(rs.getString("description"));
                lw.setTunedInWorks(rs.getObject("tuned_in_works") != null ? rs.getInt("tuned_in_works") : null);
                lw.setDifficulty(Difficulty.valueOf(rs.getString("difficulty")));
                lw.setDiscipline(new Discipline(
                        rs.getString("discipline_name"),
                        rs.getLong("practice_hours")
                ));
                lw.setOwner(rs.getInt("owner_login"));
                labWorks.add(lw);
            }

        } catch (SQLException e) {
            logger.error("Ошибка при загрузке LabWork из БД", e);
        }

        return labWorks;
    }

    /**
     * Добавляет объект LabWork в базу данных.
     *
     * @param connection соединение с БД
     * @param lw объект LabWork для добавления
     * @param ownerLogin логин пользователя, добавившего объект
     * @return добавленный объект с назначенным id или null, если ошибка
     */
    public static LabWork insertLabWork(Connection connection, LabWork lw, String ownerLogin) {
        String insertDisciplineSQL = "INSERT INTO disciplines (name, practice_hours) VALUES (?, ?) RETURNING id";
        String insertLabworkSQL = """
            INSERT INTO labworks (
                name, x, y, creation_date, minimal_point, description,
                tuned_in_works, difficulty, discipline_id, owner_id
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?) RETURNING id
        """;

        try {
            connection.setAutoCommit(false);

            int disciplineId;
            try (PreparedStatement discStmt = connection.prepareStatement(insertDisciplineSQL)) {
                discStmt.setString(1, lw.getDiscipline().getName());
                discStmt.setLong(2, lw.getDiscipline().getPracticeHours());
                ResultSet rs = discStmt.executeQuery();
                if (!rs.next()) throw new SQLException("Не удалось вставить дисциплину.");
                disciplineId = rs.getInt(1);
            }

            int ownerId = getUserIdByLogin(connection, ownerLogin);
            if (ownerId == -1) throw new SQLException("Пользователь не найден: " + ownerLogin);

            try (PreparedStatement labStmt = connection.prepareStatement(insertLabworkSQL)) {
                labStmt.setString(1, lw.getName());
                labStmt.setInt(2, lw.getCoordinates().getX());
                labStmt.setFloat(3, lw.getCoordinates().getY());
                labStmt.setTimestamp(4, Timestamp.valueOf(LocalDateTime.now()));
                labStmt.setLong(5, lw.getMinimalPoint());
                labStmt.setString(6, lw.getDescription());
                if (lw.getTunedInWorks() != null)
                    labStmt.setInt(7, lw.getTunedInWorks());
                else
                    labStmt.setNull(7, Types.INTEGER);
                labStmt.setString(8, lw.getDifficulty().name());
                labStmt.setInt(9, disciplineId);
                labStmt.setInt(10, ownerId);

                ResultSet rs = labStmt.executeQuery();
                if (rs.next()) {
                    lw.setId(rs.getInt(1));
                    lw.setCreationDate(LocalDateTime.now());
                    lw.setOwner(ownerId);
                }
            }

            connection.commit();
            return lw;

        } catch (SQLException e) {
            logger.error("Ошибка при добавлении LabWork в БД", e);
            try {
                connection.rollback();
            } catch (SQLException rollbackEx) {
                logger.error("Ошибка при откате транзакции", rollbackEx);
            }
        }
        return null;
    }


    public static boolean updateLabWork(Connection connection, int id, LabWork updated, String ownerLogin) {
        String updateLabworkSQL = """
            UPDATE labworks SET
                name = ?, x = ?, y = ?, minimal_point = ?,
                description = ?, tuned_in_works = ?, difficulty = ?,
                discipline_id = ?
            WHERE id = ? AND owner_id = ?
        """;

        try {
            int disciplineId;
            try (PreparedStatement discStmt = connection.prepareStatement(
                    "INSERT INTO disciplines (name, practice_hours) VALUES (?, ?) RETURNING id")) {
                discStmt.setString(1, updated.getDiscipline().getName());
                discStmt.setLong(2, updated.getDiscipline().getPracticeHours());
                ResultSet rs = discStmt.executeQuery();
                if (!rs.next()) throw new SQLException("Не удалось вставить дисциплину.");
                disciplineId = rs.getInt(1);
            }

            int ownerId = getUserIdByLogin(connection, String.valueOf(ownerLogin));
            if (ownerId == -1) return false;

            try (PreparedStatement stmt = connection.prepareStatement(updateLabworkSQL)) {
                stmt.setString(1, updated.getName());
                stmt.setInt(2, updated.getCoordinates().getX());
                stmt.setFloat(3, updated.getCoordinates().getY());
                stmt.setLong(4, updated.getMinimalPoint());
                stmt.setString(5, updated.getDescription());
                if (updated.getTunedInWorks() != null)
                    stmt.setInt(6, updated.getTunedInWorks());
                else
                    stmt.setNull(6, Types.INTEGER);
                stmt.setString(7, updated.getDifficulty().name());
                stmt.setInt(8, disciplineId);
                stmt.setInt(9, id);
                stmt.setInt(10, ownerId);

                return stmt.executeUpdate() > 0;
            }

        } catch (SQLException e) {
            logger.error("Ошибка при обновлении LabWork", e);
            return false;
        }
    }

    public static boolean removeById(Connection connection, int id, String ownerLogin) {
        try {
            int ownerId = getUserIdByLogin(connection, ownerLogin);
            if (ownerId == -1) return false;

            try (PreparedStatement stmt = connection.prepareStatement(
                    "DELETE FROM labworks WHERE id = ? AND owner_id = ?")) {
                stmt.setInt(1, id);
                stmt.setInt(2, ownerId);
                return stmt.executeUpdate() > 0;
            }
        } catch (SQLException e) {
            logger.error("Ошибка при удалении LabWork", e);
            return false;
        }
    }

    public static boolean clearUserEntries(Connection conn, String login) {
        String deleteSQL = "DELETE FROM labworks WHERE owner_id = (SELECT id FROM users WHERE login = ?)";

        try (PreparedStatement stmt = conn.prepareStatement(deleteSQL)) {
            stmt.setString(1, login);
            int affected = stmt.executeUpdate();
            return affected > 0;
        } catch (SQLException e) {
            logger.error("Ошибка при очистке записей пользователя {}", login, e);
            return false;
        }
    }


    private static int getUserIdByLogin(Connection conn, String login) throws SQLException {
        String query = "SELECT id FROM users WHERE login = ?";
        try (PreparedStatement stmt = conn.prepareStatement(query)) {
            stmt.setString(1, login);
            try (ResultSet rs = stmt.executeQuery()) {
                if (rs.next()) {
                    return rs.getInt("id");
                }
            }
        }
        return -1;
    }
}
