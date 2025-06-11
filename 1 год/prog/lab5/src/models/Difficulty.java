package models;

/**
 * Перечисление сложностей
 */
public enum Difficulty {
    NORMAL,
    VERY_HARD,
    INSANE,
    HOPELESS;

    /**
     * @return Строка со всеми элементами enum'а через запятую.
     */
    public static String names() {
        StringBuilder nameList = new StringBuilder();
        for (Difficulty difficultyType : values()) {
            nameList.append(difficultyType.name()).append(", ");
        }
        return nameList.substring(0, nameList.length()-2);
    }
}