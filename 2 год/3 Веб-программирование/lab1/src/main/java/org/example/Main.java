package org.example;

import com.fastcgi.FCGIInterface;

import java.math.BigDecimal;
import java.nio.charset.StandardCharsets;
import java.time.ZoneId;
import java.time.ZonedDateTime;
import java.time.format.DateTimeFormatter;
import java.util.*;

public class Main {
    private static final List<Row> HISTORY = new ArrayList<>();

    static final class Row {
        final BigDecimal x, y, r;
        final boolean hit;
        final String now;
        final long scriptMicros;
        Row(BigDecimal x, BigDecimal y, BigDecimal r, boolean hit, String now, long scriptMicros) {
            this.x = x; this.y = y; this.r = r; this.hit = hit; this.now = now; this.scriptMicros = scriptMicros;
        }
        Map<String, Object> toMap() {
            Map<String, Object> m = new LinkedHashMap<>();
            m.put("x", x);
            m.put("y", y);
            m.put("r", r);
            m.put("hit", hit);
            m.put("now", now);
            m.put("scriptMicros", scriptMicros);
            return m;
        }
    }

    public static void main(String[] args) {
        FCGIInterface fcgi = new FCGIInterface();
        while (fcgi.FCGIaccept() >= 0) {
            long startTime = System.nanoTime();
            String query = System.getProperties().getProperty("QUERY_STRING");
            try {
                Params p = new Params(query);
                boolean hit = inArea(p.getX(), p.getY(), p.getR());
                long micros = (System.nanoTime() - startTime) / 1000;
                String now = ZonedDateTime.now(ZoneId.of("Europe/Moscow")).format(DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss.SSS z"));

                Row row = new Row(p.getX(), p.getY(), p.getR(), hit, now, micros);
                HISTORY.add(0, row);

                Map<String,Object> resp = new LinkedHashMap<>();
                resp.put("ok", true);
                resp.put("data", row.toMap());
                List<Map<String,Object>> hist = new ArrayList<>();
                for (Row r : HISTORY) hist.add(r.toMap());
                resp.put("history", hist);

                System.out.print(buildResponse(toJson(resp), 200, "OK"));
            } catch (ValidationException ex) {
                Map<String,Object> err = new LinkedHashMap<>();
                String now = ZonedDateTime.now(ZoneId.of("Europe/Moscow")).format(DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss.SSS z"));
                err.put("ok", false);
                err.put("now", now);
                err.put("error", ex.getMessage());
                System.out.print(buildResponse(toJson(err), 400, "Bad Request"));
            } catch (Exception ex) {
                Map<String,Object> err = new LinkedHashMap<>();
                err.put("ok", false);
                err.put("error", "internal error");
                System.out.print(buildResponse(toJson(err), 500, "Server Error"));
            }
        }
    }

//    private static boolean inArea(double x, double y, double r) {
//        boolean q1 = ((x>=0 && y>=0) && ((y+2*x)<=r));
//        boolean q2 = ((x>=0 && y<=0) && ((x*x+y*y)<=r*r));
//        boolean q3 = ((x<=0 && y<=0) && (x>=-r && y>=-r));
//        return q1 || q2 || q3;
//    }

    private static boolean inArea(BigDecimal x, BigDecimal y, BigDecimal r) {
        boolean q1 = (x.signum() >= 0 && y.signum() >= 0) && (y.add(BigDecimal.valueOf(2).multiply(x)).compareTo(r) <= 0);
        boolean q2 = (x.signum() >= 0 && y.signum() <= 0) && (x.multiply(x).add(y.multiply(y)).compareTo(r.multiply(r)) <= 0);
        boolean q3 = (x.signum() <= 0 && y.signum() <= 0) && (x.compareTo(r.negate()) >= 0 && y.compareTo(r.negate()) >= 0);
        return q1 || q2 || q3;
    }

    private static String buildResponse(String json, int status, String reason) {
        String headers =
                "Status: " + status + " " + reason + "\r\n" +
                        "Access-Control-Allow-Origin: *\r\n" +
                        "Connection: keep-alive\r\n" +
                        "Content-Type: application/json; charset=utf-8\r\n" +
                        "Content-Length: " + json.getBytes(StandardCharsets.UTF_8).length + "\r\n" +
                        "\r\n";
        return headers + json;
    }

    private static String toJson(Object v) {
        if (v == null) return "null";
        if (v instanceof String) return "\"" + ((String) v).replace("\\","\\\\").replace("\"","\\\"") + "\"";
        if (v instanceof Number || v instanceof Boolean) return v.toString();
        if (v instanceof Map) {
            StringBuilder sb = new StringBuilder("{");
            boolean first = true;
            for (Map.Entry<?,?> e : ((Map<?,?>) v).entrySet()) {
                if (!first) sb.append(",");
                first = false;
                sb.append(toJson(String.valueOf(e.getKey()))).append(":").append(toJson(e.getValue()));
            }
            return sb.append("}").toString();
        }
        if (v instanceof Collection) {
            StringBuilder sb = new StringBuilder("[");
            boolean first = true;
            for (Object o : (Collection<?>) v) {
                if (!first) sb.append(",");
                first = false;
                sb.append(toJson(o));
            }
            return sb.append("]").toString();
        }
        return toJson(String.valueOf(v));
    }
}


////????
//package org.example;
//
//import com.fastcgi.FCGIInterface;
//
//import java.nio.charset.StandardCharsets;
//import java.time.ZoneId;
//import java.time.ZonedDateTime;
//import java.time.format.DateTimeFormatter;
//import java.util.*;
//
//public class Main {
//    private static final List<Row> HISTORY = new ArrayList<>();
//
//    static final class Row {
//        final double x, y, r;
//        final boolean hit;
//        final String now;
//        final long scriptMicros;
//        Row(double x, double y, double r, boolean hit, String now, long scriptMicros) {
//            this.x = x; this.y = y; this.r = r; this.hit = hit; this.now = now; this.scriptMicros = scriptMicros;
//        }
//        Map<String, Object> toMap() {
//            Map<String, Object> m = new LinkedHashMap<>();
//            m.put("x", x);
//            m.put("y", y);
//            m.put("r", r);
//            m.put("hit", hit);
//            m.put("now", now);
//            m.put("scriptMicros", scriptMicros);
//            return m;
//        }
//    }
//
//    public static void main(String[] args) {
//        FCGIInterface fcgi = new FCGIInterface();
//        while (fcgi.FCGIaccept() >= 0) {
//            long startTime = System.nanoTime();
//            String query = System.getProperties().getProperty("QUERY_STRING");
//            try {
//                Params p = new Params(query);
//                boolean hit = inArea(p.getX(), p.getY(), p.getR());
//                long micros = (System.nanoTime() - startTime) / 1000;
//                String now = ZonedDateTime.now(ZoneId.of("Europe/Moscow")).format(DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss.SSS z"));
//                Row row = new Row(p.getX(), p.getY(), p.getR(), hit, now, micros);
//                HISTORY.add(0, row);
//
//                Map<String,Object> resp = new LinkedHashMap<>();
//                resp.put("ok", true);
//                resp.put("data", row.toMap());
//                List<Map<String,Object>> hist = new ArrayList<>();
//                for (Row r : HISTORY) hist.add(r.toMap());
//                resp.put("history", hist);
//
//                System.out.print(buildResponse(toJson(resp), 200, "OK"));
//            } catch (ValidationException ex) {
//                Map<String,Object> err = new LinkedHashMap<>();
//                String now = ZonedDateTime.now(ZoneId.of("Europe/Moscow")).format(DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss.SSS z"));
//                err.put("ok", false);
//                err.put("now", now);
//                err.put("error", ex.getMessage());
//
//                System.out.print(buildResponse(toJson(err), 400, "Bad Request"));
//            } catch (Exception ex) {
//                Map<String,Object> err = new LinkedHashMap<>();
//                err.put("ok", false);
//                err.put("error", "internal error");
//
//                System.out.print(buildResponse(toJson(err), 500, "Server Error"));
//            }
//        }
//    }
//
//    // Проверка попадания
//    private static boolean inArea(double x, double y, double r) {
//        boolean q1 = ((x>=0 && y>=0) && ((y+2*x)<=r));
//        boolean q2 = ((x>=0 && y<=0) && ((x*x+y*y)<=r*r));
//        boolean q3 = ((x<=0 && y<=0) && (x>=-r && y>=-r));
//        return q1 || q2 || q3;
//    }
//
//    // Сборка ответа
//    private static String buildResponse(String json, int status, String reason) {
//        String headers =
//                "Status: " + status + " " + reason + "\r\n" +
//                "Access-Control-Allow-Origin: *\r\n" +
//                "Connection: keep-alive\r\n" +
//                "Content-Type: application/json; charset=utf-8\r\n" +
//                "Content-Length: " + json.getBytes(StandardCharsets.UTF_8).length + "\r\n" +
//                "\r\n";
//        return headers + json;
//    }
//
//    //
//    private static String toJson(Object v) {
//        if (v == null) return "null";
//        if (v instanceof String) return "\"" + ((String) v).replace("\\","\\\\").replace("\"","\\\"") + "\"";
//        if (v instanceof Number || v instanceof Boolean) return v.toString();
//        if (v instanceof Map) {
//            StringBuilder sb = new StringBuilder("{");
//            boolean first = true;
//            for (Map.Entry<?,?> e : ((Map<?,?>) v).entrySet()) {
//                if (!first) sb.append(",");
//                first = false;
//                sb.append(toJson(String.valueOf(e.getKey()))).append(":").append(toJson(e.getValue()));
//            }
//            return sb.append("}").toString();
//        }
//        if (v instanceof Collection) {
//            StringBuilder sb = new StringBuilder("[");
//            boolean first = true;
//            for (Object o : (Collection<?>) v) {
//                if (!first) sb.append(",");
//                first = false;
//                sb.append(toJson(o));
//            }
//            return sb.append("]").toString();
//        }
//        return toJson(String.valueOf(v));
//    }
//}
////????