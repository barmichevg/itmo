package web.mbeans;

import javax.management.MBeanNotificationInfo;
import javax.management.Notification;
import javax.management.NotificationBroadcasterSupport;
import java.util.concurrent.atomic.AtomicInteger;
import java.util.concurrent.atomic.AtomicLong;

public class PointStats extends NotificationBroadcasterSupport implements PointStatsMBean {
    public static final String POINTS_MULTIPLE_OF_15_NOTIFICATION = "web.lab4.points.multiple-of-15";

    private final AtomicInteger totalPoints = new AtomicInteger();
    private final AtomicInteger missedPoints = new AtomicInteger();
    private final AtomicLong sequenceNumber = new AtomicLong();

    public void addPoint(boolean hit) {
        int total = totalPoints.incrementAndGet();

        if (!hit) {
            missedPoints.incrementAndGet();
        }

        if (total % 15 == 0) {
            sendNotification(new Notification(
                    POINTS_MULTIPLE_OF_15_NOTIFICATION,
                    this,
                    sequenceNumber.incrementAndGet(),
                    System.currentTimeMillis(),
                    "Количество установленных точек стало кратно 15: " + total
            ));
        }
    }

    @Override
    public int getTotalPoints() {
        return totalPoints.get();
    }

    @Override
    public int getMissedPoints() {
        return missedPoints.get();
    }

    @Override
    public void reset() {
        totalPoints.set(0);
        missedPoints.set(0);
    }

    @Override
    public MBeanNotificationInfo[] getNotificationInfo() {
        String[] types = {POINTS_MULTIPLE_OF_15_NOTIFICATION};
        String name = Notification.class.getName();
        String description = "Уведомление о том, что количество установленных точек стало кратно 15";
        return new MBeanNotificationInfo[]{new MBeanNotificationInfo(types, name, description)};
    }
}
