package managers;

import au.com.bytecode.opencsv.*;
import models.LabWork;
import utility.Console;

import java.io.*;
import java.util.Collection;
import java.util.Scanner;
import java.util.Vector;


public class FileManager {
    private final String fileName;
    private final Console console;

    public FileManager(String fileName, Console console) {
        this.fileName = fileName;
        this.console = console;
    }

    /**
     * Преобразует коллекцию в CSV-строку.
     * @param collection
     * @return CSV-строка
     */
    private String collection2CSV(Collection<LabWork> collection) {
        try {
            StringWriter sw = new StringWriter();
            CSVWriter csvWriter = new CSVWriter(sw, ',');
            for (LabWork e : collection) {
                csvWriter.writeNext(LabWork.toArray(e));
            }
            String csv = sw.toString();
            return csv;
        } catch (Exception e) {
            console.printError("Ошибка сериализации");
            return null;
        }
    }

    /**
     * Записывает коллекцию в файл.
     * @param collection коллекция
     */
    public void writeCollection(Collection<LabWork> collection) {
        OutputStreamWriter writer = null;
        try {
            String csv = collection2CSV(collection);
            if (csv == null) return;
            writer = new OutputStreamWriter(new FileOutputStream(fileName));
            try {
                writer.write(csv);
                writer.flush();
                console.println("Коллекция успешна сохранена в файл!");
            } catch (IOException e) {
                console.printError("Неожиданная ошибка сохранения");
            }
        } catch (FileNotFoundException | NullPointerException e) {
            console.printError("Файл не найден");
        } finally {
            try {
                writer.close();
            } catch(IOException e) {
                console.printError("Ошибка закрытия файла");
            }
        }
    }

    /**
     * Преобразует CSV-строку в коллекцию.
     * @param s CSV-строка
     * @return коллекция
     */
    private Vector<LabWork> CSV2collection(String s) {
        try {
            StringReader sr = new StringReader(s);
            CSVReader csvReader = new CSVReader(sr, ',');
            Vector<LabWork> ds = new Vector<LabWork>();
            String[] record = null;
            while ((record = csvReader.readNext()) != null) {
                LabWork d = LabWork.fromArray(record);
                if (d.validate())
                    ds.add(d);
                else
                    console.printError("Файл с коллекцией содержит не действительные данные");
            }
            csvReader.close();
            return ds;
        } catch (Exception e) {
            console.printError("Ошибка десериализации");
            return null;
        }
    }

    /**
     * Считывает коллекцию из файла.
     * @return Считанная коллекция
     */
    public void readCollection(Collection<LabWork> collection) {
        if (fileName != null && !fileName.isEmpty()) {
            try (Scanner fileReader = new Scanner(new File(fileName))) {
                StringBuilder s = new StringBuilder("");
                while (fileReader.hasNextLine()) {
                    s.append(fileReader.nextLine());
                    s.append("\n");
                }
                collection.clear();
                for (LabWork e: CSV2collection(s.toString()))
                    collection.add(e);
                if (collection != null) {
                    console.println("Коллекция успешна загружена!");
                    return;
                } else
                    console.printError("В загрузочном файле не обнаружена необходимая коллекция!");
            } catch (FileNotFoundException exception) {
                console.printError("Загрузочный файл не найден!");
            } catch (IllegalStateException exception) {
                console.printError("Непредвиденная ошибка!");
                System.exit(0);
            }
        } else {
            console.printError("Аргумент командной строки с загрузочным файлом не найден!");
        }
        collection = new Vector<LabWork>();
    }
}
