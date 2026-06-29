package web.mbeans;

public interface PointStatsMBean {
    int getTotalPoints();
    int getMissedPoints();
    void reset();
}
