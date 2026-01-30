package web.servlets;

import jakarta.inject.Inject;
import jakarta.servlet.ServletException;
import jakarta.servlet.annotation.WebServlet;
import jakarta.servlet.http.*;
import java.io.IOException;
import java.math.BigDecimal;
import java.time.Instant;

import web.models.HitResult;
import web.models.ResultsBean;

@WebServlet(urlPatterns = "/area")
public class AreaCheckServlet extends HttpServlet {

    @Inject
    private ResultsBean results;

    @Override
    protected void doPost(HttpServletRequest req, HttpServletResponse resp)
            throws ServletException, IOException {
        handle(req, resp);
    }

    private void handle(HttpServletRequest req, HttpServletResponse resp)
            throws ServletException, IOException {
        final long t0 = System.nanoTime();
        try {
            BigDecimal x = new BigDecimal(req.getParameter("x"));
            BigDecimal y = new BigDecimal(req.getParameter("y"));
            BigDecimal r = new BigDecimal(req.getParameter("r"));

            validate(x, y, r);

            boolean hit = inArea(x, y, r);
            long micros = (System.nanoTime() - t0) / 1_000L;

            HitResult row = buildHitResult(x, y, r, hit, Instant.now(), micros);
            if (results != null) results.add(row);
            req.setAttribute("x", x);
            req.setAttribute("y", y);
            req.setAttribute("r", r);
            req.setAttribute("hit", hit);
            req.setAttribute("at", row.getAt());
            req.setAttribute("scriptMicros", micros);

            req.getRequestDispatcher("/result.jsp").forward(req, resp);

        } catch (IllegalArgumentException ex) {
            req.setAttribute("error", ex.getMessage());
            req.getRequestDispatcher("/index.jsp").forward(req, resp);
        }
    }

    private void validate(BigDecimal x, BigDecimal y, BigDecimal r) {
        if (r == null || r.compareTo(BigDecimal.ONE) < 0 || r.compareTo(BigDecimal.valueOf(5)) > 0)
            throw new IllegalArgumentException("R out of range [1;5]");
    }

    public static boolean inArea(BigDecimal x, BigDecimal y, BigDecimal r) {
        boolean q2 = x.signum() <= 0 && y.signum() >= 0
                && y.subtract(x).compareTo(r.divide(BigDecimal.valueOf(2))) <= 0;
        boolean q3 = x.signum() <= 0 && y.signum() <= 0
                && x.multiply(x).add(y.multiply(y)).compareTo(r.multiply(r)) <= 0;
        boolean q4 = x.signum() >= 0 && y.signum() <= 0
                && x.compareTo(r.divide(BigDecimal.valueOf(2))) <= 0 && y.compareTo(r.negate()) >= 0;
        return q2 || q3 || q4;
    }

    private static HitResult buildHitResult(BigDecimal x, BigDecimal y, BigDecimal r, boolean hit, Instant at, long micros) {
        HitResult row = new HitResult();
        row.setX(x);
        row.setY(y);
        row.setR(r);
        row.setHit(hit);
        row.setAt(at);
        row.setScriptMicros(micros);
        return row;
    }
}

