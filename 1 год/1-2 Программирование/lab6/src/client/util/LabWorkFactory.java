package client.util;

import common.models.Coordinates;
import common.models.Difficulty;
import common.models.Discipline;
import common.models.LabWork;

import java.time.LocalDateTime;
import java.util.Scanner;

/**
 * Класс, отвечающий за создание объектов LabWork.
 */
public class LabWorkFactory {
    private static final Scanner scanner = new Scanner(System.in);

    public static LabWork createLabWork() {
        LabWork lw = new LabWork();

        // name
        String name;
        do {
            System.out.print("Введите имя: ");
            name = scanner.nextLine().trim();
        } while (name.isEmpty());
        lw.setName(name);

        // coordinates.x
        int x;
        while (true) {
            try {
                System.out.print("Введите координату X: ");
                x = Integer.parseInt(scanner.nextLine().trim());
                if (x <= 589) break;
                else System.out.println("X должен быть ≤ 589.");
            } catch (NumberFormatException e) {
                System.out.println("Введите корректное целое число.");
            }
        }

        // coordinates.y
        float y;
        while (true) {
            try {
                System.out.print("Введите координату Y: ");
                y = Float.parseFloat(scanner.nextLine().trim());
                if (y <= 654) break;
                else System.out.println("Y должен быть ≤ 654.");
            } catch (NumberFormatException e) {
                System.out.println("Введите корректное число.");
            }
        }

        lw.setCoordinates(new Coordinates(x, y));
        lw.setCreationDate(LocalDateTime.now());

        // minimalPoint
        long mp;
        while (true) {
            try {
                System.out.print("Введите minimalPoint: ");
                mp = Long.parseLong(scanner.nextLine().trim());
                if (mp > 0) break;
                else System.out.println("Значение должно быть > 0.");
            } catch (NumberFormatException e) {
                System.out.println("Введите корректное число.");
            }
        }
        lw.setMinimalPoint(mp);

        // description
        System.out.print("Введите описание: ");
        String desc = scanner.nextLine().trim();
        lw.setDescription(desc.isEmpty() ? null : desc);

        // tunedInWorks
        System.out.print("Введите tunedInWorks: ");
        String tiwInput = scanner.nextLine().trim();
        try {
            lw.setTunedInWorks(tiwInput.isEmpty() ? null : Integer.parseInt(tiwInput));
        } catch (NumberFormatException e) {
            lw.setTunedInWorks(null);
        }

        // difficulty
        Difficulty diff = null;
        while (diff == null) {
            System.out.print("Введите сложность (NORMAL, VERY_HARD, INSANE, HOPELESS): ");
            try {
                diff = Difficulty.valueOf(scanner.nextLine().trim().toUpperCase());
            } catch (IllegalArgumentException e) {
                System.out.println("Неверное значение. Повторите.");
            }
        }
        lw.setDifficulty(diff);

        // discipline
        System.out.print("Введите название дисциплины: ");
        String dName = scanner.nextLine().trim();
        if (!dName.isEmpty()) {
            Long hours = null;
            while (hours == null) {
                System.out.print("Введите practiceHours: ");
                try {
                    hours = Long.parseLong(scanner.nextLine().trim());
                } catch (NumberFormatException e) {
                    System.out.println("Неверное значение.");
                }
            }
            lw.setDiscipline(new Discipline(dName, hours));
        }
        return lw;
    }
}
