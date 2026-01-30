package org.example;

import java.net.URLDecoder;
import java.nio.charset.StandardCharsets;
import java.math.BigDecimal;
import java.util.*;
import java.util.stream.Collectors;

final class Params {
    private final BigDecimal x;
    private final BigDecimal y;
    private final BigDecimal r;

    private static BigDecimal bd(String s) { return new BigDecimal(s); }

    private static final List<BigDecimal> ALLOWED_X = List.of(bd("-2"), bd("-1.5"), bd("-1"), bd("-0.5"), bd("0"), bd("0.5"), bd("1"), bd("1.5"), bd("2"));
    private static final List<BigDecimal> ALLOWED_R = List.of(bd("1"), bd("1.5"), bd("2"), bd("2.5"), bd("3"));

    Params(String query) throws ValidationException {
        if (query == null || query.isEmpty()) {
            throw new ValidationException("missing query string");
        }
        Map<String, String> q = splitQuery(query);

        BigDecimal xBD = parseStrict(q.get("x"), "x");
        BigDecimal yBD = parseStrict(q.get("y"), "y");
        BigDecimal rBD = parseStrict(q.get("r"), "r");

        boolean xOk = ALLOWED_X.stream().anyMatch(v -> v.compareTo(xBD) == 0);
        if (!xOk) throw new ValidationException("x forbidden");

        if (yBD.compareTo(bd("-5")) < 0 || yBD.compareTo(bd("5")) > 0)
            throw new ValidationException("y out of range [-5..5]");

        boolean rOk = ALLOWED_R.stream().anyMatch(v -> v.compareTo(rBD) == 0);
        if (!rOk) throw new ValidationException("r forbidden");

        this.x = xBD;
        this.y = yBD;
        this.r = rBD;
    }

    private static Map<String,String> splitQuery(String query) throws ValidationException {
        try {
            return Arrays.stream(query.split("&"))
                    .map(pair -> pair.split("=", 2))
                    .collect(Collectors.toMap(
                            kv -> URLDecoder.decode(kv[0], StandardCharsets.UTF_8),
                            kv -> kv.length > 1 ? URLDecoder.decode(kv[1], StandardCharsets.UTF_8) : "",
                            (a,b) -> b,
                            LinkedHashMap::new
                    ));
        } catch (Exception ex) {
            throw new ValidationException("bad query string");
        }
    }

    private static BigDecimal parseStrict(String raw, String name) throws ValidationException {
        if (raw == null || raw.isEmpty())
            throw new ValidationException(name + " is invalid");
        String s = raw.replace(',', '.').trim();
        try {
            return new BigDecimal(s);
        } catch (NumberFormatException ex) {
            throw new ValidationException(name + " bad format");
        }
    }

    public BigDecimal getX() { return x; }
    public BigDecimal getY() { return y; }
    public BigDecimal getR() { return r; }
}

////?????
//
//import java.net.URLDecoder;
//import java.nio.charset.StandardCharsets;
//import java.util.*;
//import java.util.stream.Collectors;
//
//final class Params {
//    private final double x;
//    private final double y;
//    private final double r;
//    private static final Set<Double> allowedX = new HashSet<>(Arrays.asList(-2.0, -1.5, -1.0, -0.5, 0.0, 0.5, 1.0, 1.5, 2.0));
//    private static final Set<Double> allowedR = new HashSet<>(Arrays.asList(1.0, 1.5, 2.0, 2.5, 3.0));
//
//    Params(String query) throws ValidationException {
//        if (query == null || query.isEmpty()) {
//            throw new ValidationException("missing query string");
//        }
//        Map<String,String> q = splitQuery(query);
//        validate(q);
//        this.x = Double.parseDouble(q.get("x"));
//        this.y = Double.parseDouble(q.get("y"));
//        this.r = Double.parseDouble(q.get("r"));
//    }
//
//    private static Map<String,String> splitQuery(String query) throws ValidationException {
//        try {
//            return Arrays.stream(query.split("&"))
//                    .map(pair -> pair.split("=", 2))
//                    .collect(Collectors.toMap(
//                            kv -> URLDecoder.decode(kv[0], StandardCharsets.UTF_8),
//                            kv -> kv.length > 1 ? URLDecoder.decode(kv[1], StandardCharsets.UTF_8) : "",
//                            (a,b) -> b,
//                            LinkedHashMap::new
//                    ));
//        } catch (Exception ex) {throw new ValidationException("bad query string");
//        }
//    }
//
//    private static void validate(Map<String,String> p) throws ValidationException {
//        String sx = p.get("x"), sy = p.get("y"), sr = p.get("r");
//        if (sx == null || sy == null || sr == null) throw new ValidationException("x/y/r required");
//
//        double x, y, r;
//        try { x = Double.parseDouble(sx); }
//        catch (NumberFormatException e) { throw new ValidationException("x is not a number"); }
//        try { y = Double.parseDouble(sy); }
//        catch (NumberFormatException e) { throw new ValidationException("y is not a number"); }
//        try { r = Double.parseDouble(sr); }
//        catch (NumberFormatException e) { throw new ValidationException("r is not a number"); }
//
//        if (!allowedX.contains(x)) throw new ValidationException("x forbidden");
//        if (y < -5 || y > 5)       throw new ValidationException("y out of range [-5..5]");
//        if (!allowedR.contains(r)) throw new ValidationException("r forbidden");
//    }
//
//    public double getX() { return x; }
//    public double getY() { return y; }
//    public double getR() { return r; }
//}
////?????
