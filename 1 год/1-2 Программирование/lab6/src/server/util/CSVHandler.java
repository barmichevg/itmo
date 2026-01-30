package server.util;

import common.models.Coordinates;
import common.models.Difficulty;
import common.models.Discipline;
import common.models.LabWork;
import server.command.CommandManager;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.*;
import java.time.LocalDateTime;
import java.util.*;

/**
 * Класс для работы с CSV файлом.
 */
public class CSVHandler {
    private static final Logger logger = LoggerFactory.getLogger(CSVHandler.class);

    /**
     * Загружает коллекцию LabWork из CSV-файла.
     * @param filePath путь к CSV-файлу
     * @return список загруженных объектов LabWork
     */
    public static Vector<LabWork> loadFromCSV(String filePath) {
        Vector<LabWork> labWorks = new Vector<>();
        logger.info("Загрузка коллекции из файла: {}", filePath);
        try (BufferedReader br = new BufferedReader(new FileReader(filePath))) {
            String line;
            int count = 0;
            while ((line = br.readLine()) != null) {
                String[] parts = line.split(",", -1);
                if (parts.length < 10) continue;
                LabWork lw = new LabWork();
                lw.setId(Integer.parseInt(parts[0]));
                lw.setName(parts[1]);
                lw.setCoordinates(new Coordinates(
                        Integer.parseInt(parts[2]),
                        Float.parseFloat(parts[3])
                ));
                lw.setCreationDate(LocalDateTime.parse(parts[4]));
                lw.setMinimalPoint(Long.parseLong(parts[5]));
                lw.setDescription(parts[6].isEmpty() ? null : parts[6]);
                lw.setTunedInWorks(parts[7].isEmpty() ? null : Integer.parseInt(parts[7]));
                lw.setDifficulty(Difficulty.valueOf(parts[8]));
                lw.setDiscipline(parts[9].isEmpty() ? null : new Discipline(
                        parts[9],
                        Long.parseLong(parts[10])
                ));
                labWorks.add(lw);
                count++;
            }
            logger.info("Загружено {} элементов.", count);
        } catch (IOException | RuntimeException e) {
            logger.error("Ошибка чтения CSV: {}", e.getMessage());
        }
        return labWorks;
    }

    /**
     * Сохраняет коллекцию LabWork в CSV-файл.
     * @param filePath путь к файлу, куда нужно сохранить данные
     * @param labWorks список объектов LabWork
     */
    public static void saveToCSV(String filePath, List<LabWork> labWorks) {
        logger.info("Сохранение коллекции в файл: {}", filePath);
        try (PrintWriter pw = new PrintWriter(new FileWriter(filePath))) {
            for (LabWork lw : labWorks) {
                Discipline d = lw.getDiscipline();
                pw.println(String.join(",",
                        lw.getId().toString(),
                        lw.getName(),
                        lw.getCoordinates().getX().toString(),
                        lw.getCoordinates().getY().toString(),
                        lw.getCreationDate().toString(),
                        String.valueOf(lw.getMinimalPoint()),
                        lw.getDescription() == null ? "" : lw.getDescription(),
                        lw.getTunedInWorks() == null ? "" : lw.getTunedInWorks().toString(),
                        lw.getDifficulty().name(),
                        d == null ? "" : d.getName(),
                        d == null ? "" : d.getPracticeHours().toString()
                ));
            }
            logger.info("Успешно сохранено {} элементов.", labWorks.size());
            CommandManager.updateSaveTime();
        } catch (IOException e) {
            logger.error("Ошибка записи CSV: {}", e.getMessage());
        }
    }
}
