package ru.itmo.lab4.common;

import java.math.BigDecimal;

public final class DecimalParser {
    private DecimalParser() {}

    public static BigDecimal parse(String raw) {
        if (raw == null) throw new NumberFormatException("null");
        String normalized = raw.trim().replace(',', '.');
        return new BigDecimal(normalized);
    }
}
