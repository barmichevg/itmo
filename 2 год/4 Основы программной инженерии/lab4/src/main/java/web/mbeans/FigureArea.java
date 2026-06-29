package web.mbeans;

public class FigureArea implements FigureAreaMBean {
    private volatile double r = 2.0;

    public void updateR(double r) {
        this.r = r;
    }

    @Override
    public double getR() {
        return r;
    }

    @Override
    public double getArea() {
        return r * r * (Math.PI + 10.0) / 16.0;
    }
}
