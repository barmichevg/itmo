package web.servlets;

import jakarta.servlet.ServletException;
import jakarta.servlet.annotation.WebServlet;
import jakarta.servlet.http.*;
import java.io.IOException;
import jakarta.inject.Inject;
import web.models.ResultsBean;

@WebServlet(urlPatterns = "/controller")
public class ControllerServlet extends HttpServlet {
    @Inject private ResultsBean results;

    @Override
    protected void doPost(HttpServletRequest req, HttpServletResponse resp)
            throws ServletException, IOException {
        if (req.getParameter("clear") != null) {
            results.clear();
            resp.sendRedirect(req.getContextPath() + "/controller");
            return;
        }

        String x = req.getParameter("x");
        String y = req.getParameter("y");
        String r = req.getParameter("r");

        if (x != null && y != null && r != null) {
            req.getRequestDispatcher("/area").forward(req, resp);
        } else {
            req.setAttribute("history", results.getResults());
            req.setAttribute("last", results.getLast());
            req.getRequestDispatcher("/index.jsp").forward(req, resp);
        }
    }

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp)
            throws ServletException, IOException {
        req.setAttribute("history", results.getResults());
        req.setAttribute("last", results.getLast());
        req.getRequestDispatcher("/index.jsp").forward(req, resp);
    }
}
