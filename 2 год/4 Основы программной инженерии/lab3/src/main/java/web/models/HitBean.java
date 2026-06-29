package web.models;

import jakarta.enterprise.context.RequestScoped;
import jakarta.faces.application.FacesMessage;
import jakarta.faces.context.FacesContext;
import jakarta.inject.Inject;
import jakarta.inject.Named;

import java.io.Serializable;
import java.math.BigDecimal;
import java.time.Instant;

@Named("hitBean")
@RequestScoped
public class HitBean implements Serializable {

    private static final long serialVersionUID = 1L;

    private String x, y, r;
    private String fromCanvas;
    @Inject
    private ResultsBean results;

    public String getX() { return x; }
    public void setX(String x) { this.x = x; }
    public String getY() { return y; }
    public void setY(String y) { this.y = y; }
    public String getR() { return r; }
    public void setR(String r) { this.r = r; }
    public String getFromCanvas() { return fromCanvas; }
    public void setFromCanvas(String fromCanvas) { this.fromCanvas = fromCanvas; }

    public String check() {
        FacesContext ctx = FacesContext.getCurrentInstance();
        BigDecimal bx = null;
        BigDecimal by = null;
        BigDecimal br = null;
        boolean ok = true;
        boolean skipRangeForXY = Boolean.parseBoolean(fromCanvas);

        // X
        if (x == null || x.trim().isEmpty()) {
            ctx.addMessage("hit-form:xHidden", new FacesMessage(FacesMessage.SEVERITY_ERROR, "Выберите X", null));
            ok = false;
        } else {
            try {
                bx = parseNumber(x);
            } catch (NumberFormatException e) {
                ctx.addMessage("hit-form:xHidden", new FacesMessage(FacesMessage.SEVERITY_ERROR, "Некорректный X", null));
                ok = false;
            }
        }

        // Y
        if (y == null || y.trim().isEmpty()) {
            ctx.addMessage("hit-form:y", new FacesMessage(FacesMessage.SEVERITY_ERROR, "Введите Y", null));
            ok = false;
        } else {
            try {
                by = parseNumber(y);
            } catch (NumberFormatException e) {
                ctx.addMessage("hit-form:y", new FacesMessage(FacesMessage.SEVERITY_ERROR, "Некорректный Y", null));
                ok = false;
            }
        }

        // R
        if (r == null || r.trim().isEmpty()) {
            ctx.addMessage("hit-form:r", new FacesMessage(FacesMessage.SEVERITY_ERROR, "Введите R", null));
            ok = false;
        } else {
            try {
                br = parseNumber(r);
            } catch (NumberFormatException e) {
                ctx.addMessage("hit-form:r", new FacesMessage(FacesMessage.SEVERITY_ERROR, "Некорректный R", null));
                ok = false;
            }
        }

        if (!ok || bx == null || by == null || br == null) {
            ctx.validationFailed();
            fromCanvas = null;
            return null;
        }


        // Проверка диапазонов (скип при клике)
        if (!skipRangeForXY) {
            if (bx.compareTo(BigDecimal.valueOf(-2)) < 0 || bx.compareTo(BigDecimal.valueOf(2)) > 0) {
                ctx.addMessage("hit-form:xHidden", new FacesMessage(FacesMessage.SEVERITY_ERROR, "X должен быть в диапазоне [-2; 2]", null));
                ok = false;
            }

            if (by.compareTo(BigDecimal.valueOf(-3)) < 0 || by.compareTo(BigDecimal.valueOf(5)) > 0) {
                ctx.addMessage("hit-form:y", new FacesMessage(FacesMessage.SEVERITY_ERROR, "Y должен быть в диапазоне [-3; 5]", null));
                ok = false;
            }
        }

        if (br.compareTo(BigDecimal.valueOf(2)) < 0 || br.compareTo(BigDecimal.valueOf(5)) > 0) {
            ctx.addMessage("hit-form:r", new FacesMessage(FacesMessage.SEVERITY_ERROR, "R должен быть в диапазоне [2; 5]", null));
            ok = false;
        }

        if (!ok) {
            ctx.validationFailed();
            fromCanvas = null;
            return null;
        }

        long t0 = System.nanoTime();
        boolean hit = inArea(bx, by, br);
        long micros = (System.nanoTime() - t0) / 1_000L;

        HitResult row = new HitResult();
            row.setX(bx);
            row.setY(by);
            row.setR(br);
            row.setHit(hit);
            row.setAt(Instant.now());
            row.setScriptMicros(micros);
        results.add(row);
        fromCanvas = null;
        return null;
    }

    private BigDecimal parseNumber(String raw) {
        String normalized = raw.trim().replace(',', '.');
        return new BigDecimal(normalized);
    }

    public static boolean inArea(BigDecimal x, BigDecimal y, BigDecimal r) {
        boolean Q1 = x.compareTo(BigDecimal.ZERO) >= 0 && y.compareTo(BigDecimal.ZERO) >= 0 &&
                x.multiply(x).add(y.multiply(y)).compareTo(r.divide(BigDecimal.valueOf(2)).multiply(r.divide(BigDecimal.valueOf(2)))) <= 0;

        boolean Q2 = x.compareTo(BigDecimal.ZERO) <= 0 && y.compareTo(BigDecimal.ZERO) >= 0 &&
                x.compareTo(r.divide(BigDecimal.valueOf(2)).negate()) >= 0 && y.compareTo(r) <= 0;

        boolean Q3 = x.compareTo(BigDecimal.ZERO) <= 0 && y.compareTo(BigDecimal.ZERO) <= 0 &&
                x.compareTo(r.divide(BigDecimal.valueOf(2)).negate()) >= 0 && y.compareTo(r.divide(BigDecimal.valueOf(2)).negate()) >= 0 && x.add(y).compareTo(r.divide(BigDecimal.valueOf(2)).negate()) >= 0;

        return Q1 || Q2 || Q3;
    }

}
