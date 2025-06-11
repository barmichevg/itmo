package managers;


import models.LabWork;
import java.time.LocalDateTime;
import java.util.*;


/**
 * Оперирует коллекцией.
 */
public class CollectionManager {
    private int currentId = 1;
    private Map<Integer, LabWork> labWorks = new HashMap<>();
    private Vector<LabWork> collection = new Vector<LabWork>();
    private LocalDateTime lastInitTime;
    private LocalDateTime lastSaveTime;
    private final FileManager fileManager;
    public boolean isAscendingSort;

    public CollectionManager(FileManager fileManager) {
        this.lastInitTime = null;
        this.lastSaveTime = null;
        this.fileManager = fileManager;
    }

    /**
     * @return коллекция.
     */
    public Vector<LabWork> getCollection() {
        return collection;
    }

    /**
     * @return Последнее время инициализации.
     */
    public LocalDateTime getLastInitTime() {
        return lastInitTime;
    }

    /**
     * @return Последнее время сохранения.
     */
    public LocalDateTime getLastSaveTime() {
        return lastSaveTime;
    }

    /**
     * Сохраняет коллекцию в файл
     */
    public void saveCollection() {
        fileManager.writeCollection(collection);
        lastSaveTime = LocalDateTime.now();
    }

    /**
     * Получить Labwork по ID
     */
    public LabWork byId(int id) { return labWorks.get(id); }

    /**
     * Содержит ли колекции Labwork
     */
    public boolean isСontain(LabWork e) { return e == null || byId(e.getId()) != null; }

    /**
     * Получить свободный ID
     */
    public int getFreeId() {
        while (byId(++currentId) != null);
        return currentId;
    }

    /**???
     * Добавляет Labwork
     */
    public boolean add(LabWork a) {
        if (a == null) return false;
        labWorks.put(a.getId(), a);
        collection.add(a);
        update();
        return true;
    }

    /**
     * @return true в случае успеха.
     */
    public boolean swap(int id, int repId) {
        LabWork e = byId(id);
        LabWork re = byId(repId);
        if (e == null) return false;
        if (re == null) return false;
        int ind = collection.indexOf(e);
        int rind = collection.indexOf(re);
        if (ind < 0) return false;
        if (rind < 0) return false;
        e.setId(repId);
        re.setId(id);
        labWorks.put(e.getId(), e);
        labWorks.put(re.getId(), re);
        update();
        return true;
    }

    /**
     * Удаляет Labwork по ID
     */
    public boolean remove(int id) {
        LabWork ret = byId(id);
        if (ret == null) return false;
        int ind = collection.indexOf(ret);
        if (ind < 0) return false;
        collection.remove(ret);

        update();
        return true;
    }

    /**
     * Метод перемешивает элементы коллекции групп в случайном порядке.
     */
    public String shuffle() {
        Collections.shuffle(collection);
        return null;
    }

    /**
     * Фиксирует изменения коллекции
     */
    public void update() {
        Comparator<LabWork> comparator = new Comparator<LabWork>() {
            public int compare(LabWork o1, LabWork o2) {
                return Integer.compare(o1.getId(), o2.getId());
            }
        };
        Collections.sort(collection, comparator);
        if (isAscendingSort) Collections.reverse(collection);
    }

    /**
     * Загружает коллекцию из файла.
     * @return true в случае успеха.
     */
    public boolean loadCollection() {
        labWorks.clear();
        fileManager.readCollection(collection);
        lastInitTime = LocalDateTime.now();
        for (LabWork e : collection)
            if (byId(e.getId()) != null) {
                collection.clear();
                return false;
            } else {
                if (e.getId()>currentId) currentId = e.getId();
                labWorks.put(e.getId(), e);
            }
        update();
        return true;
    }

    @Override
    public String toString() {
        if (collection.isEmpty()) return "Коллекция пуста!";

        StringBuilder info = new StringBuilder();
        for (LabWork labWork : collection) {
            info.append(labWork+"\n\n");
        }
        return info.toString().trim();
    }
}