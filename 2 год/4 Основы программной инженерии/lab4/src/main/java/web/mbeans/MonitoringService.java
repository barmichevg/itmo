package web.mbeans;

import jakarta.annotation.PostConstruct;
import jakarta.annotation.PreDestroy;
import jakarta.enterprise.context.ApplicationScoped;
import web.models.HitResult;

import javax.management.ObjectName;
import java.io.Serializable;

@ApplicationScoped
public class MonitoringService implements Serializable {
    private static final long serialVersionUID = 1L;

    private final PointStats pointStats = new PointStats();
    private final FigureArea figureArea = new FigureArea();

    private ObjectName pointStatsName;
    private ObjectName figureAreaName;

    @PostConstruct
    public void init() {
        pointStatsName = MBeanRegistry.register(pointStats, "pointStats");
        figureAreaName = MBeanRegistry.register(figureArea, "figureArea");
    }

    @PreDestroy
    public void destroy() {
        MBeanRegistry.unregister(pointStatsName);
        MBeanRegistry.unregister(figureAreaName);
    }

    public void onPointAdded(HitResult result) {
        if (result == null) {
            return;
        }

        pointStats.addPoint(result.getHit());

        if (result.getR() != null) {
            figureArea.updateR(result.getR().doubleValue());
        }
    }

    public void resetPointStats() {
        pointStats.reset();
    }
}
